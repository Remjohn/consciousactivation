from __future__ import annotations

import sys
from pathlib import Path
from uuid import UUID, uuid4

import pytest

ROOT = Path(__file__).resolve().parents[2]

if "psycopg" not in sys.modules:
    import types
    psycopg = types.ModuleType("psycopg")
    class _Generic:
        @classmethod
        def __class_getitem__(cls, _item):
            return cls
    psycopg.Connection = _Generic
    psycopg.Cursor = _Generic
    psycopg.connect = lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError("PostgreSQL dependency unavailable in tests"))
    psycopg.types = types.ModuleType("psycopg.types")
    psycopg.types.json = types.ModuleType("psycopg.types.json")
    psycopg.types.json.Jsonb = lambda value: value
    sys.modules["psycopg"] = psycopg
    sys.modules["psycopg.types"] = psycopg.types
    sys.modules["psycopg.types.json"] = psycopg.types.json

src_roots = [p for root_name in ("packages", "services") for p in (ROOT / root_name).glob("*/src") if p.is_dir()]
src_roots.extend([ROOT / "packages" / "ca_contracts" / "src", ROOT / "packages" / "ca_runtime" / "src"])
for path in reversed(src_roots):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from ca_runtime.agent_invocation import (  # noqa: E402
    AgentInvocation,
    AgentInvocationRuntime,
    EconomicAccountingRequiredError,
    EconomicInvocationAlreadySettledError,
    EconomicUsage,
    ExecutionMode,
)
from ca_runtime.program_state_runtime import (  # noqa: E402
    EconomicCircuitState,
    EconomicPolicy,
    EconomicProviderRateLimit,
    InMemoryProgramStateStore,
    ProgramStateAggregate,
    ProgramStateEconomicQuotaController,
    ProgramStateLifecycle,
    SqliteProgramStateStore,
)
from ca_runtime.tenancy import TenantContext, tenant_scope  # noqa: E402


def _aggregate(workspace_id: UUID, aggregate_id: UUID | None = None) -> ProgramStateAggregate:
    aggregate_id = aggregate_id or uuid4()
    now = "2026-01-01T00:00:00Z"
    return ProgramStateAggregate(
        aggregate_id=str(aggregate_id),
        workspace_id=str(workspace_id),
        cae_run_id=str(uuid4()),
        program_id="economics-program",
        program_version="1.0.0",
        current_state="RUNNING",
        state_data={},
        version=0,
        state_hash="",
        lifecycle=ProgramStateLifecycle.RUNNING,
        last_receipt_id=None,
        created_at=now,
        updated_at=now,
    )


def _clock_box(initial: str = "2026-01-01T00:00:00Z"):
    value = [initial]
    return value, lambda: value[0]


def _controller(store, workspace_id, policy, clock):
    aggregate = _aggregate(workspace_id)
    store.save_aggregate(aggregate)
    return aggregate, ProgramStateEconomicQuotaController(store, policy, clock=clock)


def _tenant(workspace_id: UUID):
    return TenantContext(workspace_id=workspace_id, actor_id="ca-m051-test")


def _settle(controller, invocation_id, workspace_id, aggregate_id, provider, cost, total_tokens):
    reservation = controller.authorize_invocation(
        invocation_id=invocation_id,
        workspace_id=workspace_id,
        aggregate_id=str(aggregate_id),
        provider_name=provider,
        reserved_tokens=total_tokens,
        reserved_cost_usd_micros=cost,
    )
    return controller.settle_invocation(
        reservation=reservation,
        usage=EconomicUsage(
            provider_name=provider,
            prompt_tokens=total_tokens // 2,
            completion_tokens=total_tokens - (total_tokens // 2),
            total_tokens=total_tokens,
            cost_usd_micros=cost,
            observed_at="2026-01-01T00:00:00Z",
        ),
    )


def _make_invocation(workspace_id: UUID, state_id: UUID) -> AgentInvocation:
    invocation = AgentInvocation(
        invocation_id=str(uuid4()),
        workspace_id=workspace_id,
        run_id=str(uuid4()),
        lane=__import__("ca_runtime.pi_adapter", fromlist=["AuthorityLane"]).AuthorityLane.COMMANDER,
        agent_id="agent-a",
        agent_version="1",
        state_id=str(state_id),
        package_sha256="pkg",
        capsule_sha256="capsule",
        model_id="model",
        model_provider="provider-a",
        temperature_bps=0,
        timeout_ms=1000,
        skills=(),
        tools=(),
        forbidden_actions=(),
        capabilities=(),
        output_contract={"_max_cost_usd_micros": 50},
        assembled_prompt="hello",
        system_prompt="system",
        invocation_sha256="",
        created_at="2026-01-01T00:00:00Z",
    )
    object.__setattr__(invocation, "invocation_sha256", invocation.compute_sha256())
    return invocation


def test_real_time_provider_usage_is_charged_and_receipt_is_hashed():
    workspace_id, aggregate_id = uuid4(), uuid4()
    store = InMemoryProgramStateStore(); aggregate = _aggregate(workspace_id, aggregate_id); store.save_aggregate(aggregate)
    policy = EconomicPolicy(1_000, 500); _, clock = _clock_box(); controller = ProgramStateEconomicQuotaController(store, policy, clock=clock)
    with tenant_scope(_tenant(workspace_id)):
        receipt = _settle(controller, str(uuid4()), workspace_id, aggregate_id, "provider-a", 125, 50)
    economics = store.get_aggregate(str(aggregate_id)).state_data["economics"]
    assert economics["spent_usd_micros"] == 125 and economics["total_tokens"] == 50
    assert receipt.status == "CHARGED" and len(receipt.receipt_sha256) == 64


def test_aggregate_hard_budget_cap_blocks_before_dispatch_and_emits_overrun_receipt():
    workspace_id = uuid4(); store = InMemoryProgramStateStore(); aggregate = _aggregate(workspace_id); store.save_aggregate(aggregate)
    _, clock = _clock_box(); controller = ProgramStateEconomicQuotaController(store, EconomicPolicy(1_000, 100), clock=clock)
    with tenant_scope(_tenant(workspace_id)):
        _settle(controller, str(uuid4()), workspace_id, aggregate.aggregate_id, "provider-a", 80, 80)
        with pytest.raises(Exception) as exc:
            controller.authorize_invocation(invocation_id=str(uuid4()), workspace_id=workspace_id, aggregate_id=aggregate.aggregate_id, provider_name="provider-a", reserved_tokens=20, reserved_cost_usd_micros=30)
    assert exc.value.__class__.__name__ == "BudgetCeilingExceededError"
    economics = store.get_aggregate(aggregate.aggregate_id).state_data["economics"]
    assert economics["receipts"] and next(iter(economics["receipts"].values()))["receipt_type"] == "economic_usage_receipt"
    assert any(r["status"] == "BUDGET_CEILING_EXCEEDED" for r in economics["receipts"].values())


def test_workspace_budget_is_shared_across_aggregates():
    workspace_id = uuid4(); store = InMemoryProgramStateStore(); a1 = _aggregate(workspace_id); a2 = _aggregate(workspace_id); store.save_aggregate(a1); store.save_aggregate(a2)
    policy = EconomicPolicy(100, 100); controller = ProgramStateEconomicQuotaController(store, policy, clock=_clock_box()[1])
    with tenant_scope(_tenant(workspace_id)):
        _settle(controller, str(uuid4()), workspace_id, a1.aggregate_id, "provider-a", 70, 30)
        with pytest.raises(Exception) as exc:
            controller.authorize_invocation(invocation_id=str(uuid4()), workspace_id=workspace_id, aggregate_id=a2.aggregate_id, provider_name="provider-a", reserved_tokens=10, reserved_cost_usd_micros=40)
    assert exc.value.__class__.__name__ == "BudgetCeilingExceededError"


def test_provider_request_rate_limit_blocks_second_request():
    workspace_id = uuid4(); store = InMemoryProgramStateStore(); aggregate = _aggregate(workspace_id); store.save_aggregate(aggregate)
    policy = EconomicPolicy(1_000, 1_000, provider_rate_limits={"provider-a": EconomicProviderRateLimit(1, 1_000)})
    controller = ProgramStateEconomicQuotaController(store, policy, clock=_clock_box()[1])
    with tenant_scope(_tenant(workspace_id)):
        _settle(controller, str(uuid4()), workspace_id, aggregate.aggregate_id, "provider-a", 20, 50)
        with pytest.raises(Exception) as exc:
            controller.authorize_invocation(invocation_id=str(uuid4()), workspace_id=workspace_id, aggregate_id=aggregate.aggregate_id, provider_name="provider-a", reserved_tokens=50, reserved_cost_usd_micros=20)
    assert exc.value.__class__.__name__ == "ProviderRateLimitExceededError"


def test_provider_token_rate_limit_blocks_when_window_is_exhausted():
    workspace_id = uuid4(); store = InMemoryProgramStateStore(); aggregate = _aggregate(workspace_id); store.save_aggregate(aggregate)
    policy = EconomicPolicy(1_000, 1_000, provider_rate_limits={"provider-a": EconomicProviderRateLimit(10, 100)})
    controller = ProgramStateEconomicQuotaController(store, policy, clock=_clock_box()[1])
    with tenant_scope(_tenant(workspace_id)):
        _settle(controller, str(uuid4()), workspace_id, aggregate.aggregate_id, "provider-a", 20, 90)
        with pytest.raises(Exception) as exc:
            controller.authorize_invocation(invocation_id=str(uuid4()), workspace_id=workspace_id, aggregate_id=aggregate.aggregate_id, provider_name="provider-a", reserved_tokens=20, reserved_cost_usd_micros=20)
    assert exc.value.__class__.__name__ == "ProviderRateLimitExceededError"


def test_three_state_circuit_breaker_transitions_closed_open_half_open_closed():
    workspace_id = uuid4(); store = InMemoryProgramStateStore(); aggregate = _aggregate(workspace_id); store.save_aggregate(aggregate); now, clock = _clock_box()
    policy = EconomicPolicy(1_000, 1_000, breaker_failure_threshold=2, breaker_half_open_after_seconds=60)
    controller = ProgramStateEconomicQuotaController(store, policy, clock=clock)
    with tenant_scope(_tenant(workspace_id)):
        r1 = controller.authorize_invocation(invocation_id=str(uuid4()), workspace_id=workspace_id, aggregate_id=aggregate.aggregate_id, provider_name="provider-a", reserved_tokens=10, reserved_cost_usd_micros=10); controller.record_failure(reservation=r1, invocation_id=r1.invocation_id, provider_name="provider-a", reason="timeout")
        r2 = controller.authorize_invocation(invocation_id=str(uuid4()), workspace_id=workspace_id, aggregate_id=aggregate.aggregate_id, provider_name="provider-a", reserved_tokens=10, reserved_cost_usd_micros=10); controller.record_failure(reservation=r2, invocation_id=r2.invocation_id, provider_name="provider-a", reason="timeout")
        assert store.get_aggregate(aggregate.aggregate_id).state_data["economics"]["circuit_breaker"]["state"] == EconomicCircuitState.OPEN.value
        with pytest.raises(Exception) as exc: controller.authorize_invocation(invocation_id=str(uuid4()), workspace_id=workspace_id, aggregate_id=aggregate.aggregate_id, provider_name="provider-a", reserved_tokens=10, reserved_cost_usd_micros=10)
        assert exc.value.__class__.__name__ == "EconomicCircuitOpenError"
        now[0] = "2026-01-01T00:01:01Z"; probe = controller.authorize_invocation(invocation_id=str(uuid4()), workspace_id=workspace_id, aggregate_id=aggregate.aggregate_id, provider_name="provider-a", reserved_tokens=10, reserved_cost_usd_micros=10)
        assert probe.half_open_probe
        controller.settle_invocation(reservation=probe, invocation_id=probe.invocation_id, usage=EconomicUsage("provider-a", 5, 5, 10, 10, now[0])) if False else controller.settle_invocation(reservation=probe, usage=EconomicUsage("provider-a", 5, 5, 10, 10, now[0]))
    assert store.get_aggregate(aggregate.aggregate_id).state_data["economics"]["circuit_breaker"]["state"] == EconomicCircuitState.CLOSED.value


def test_retries_cannot_double_charge_same_invocation():
    workspace_id = uuid4(); store = InMemoryProgramStateStore(); aggregate = _aggregate(workspace_id); store.save_aggregate(aggregate); controller = ProgramStateEconomicQuotaController(store, EconomicPolicy(1_000, 1_000), clock=_clock_box()[1]); invocation_id = str(uuid4())
    with tenant_scope(_tenant(workspace_id)):
        reservation = controller.authorize_invocation(invocation_id=invocation_id, workspace_id=workspace_id, aggregate_id=aggregate.aggregate_id, provider_name="provider-a", reserved_tokens=10, reserved_cost_usd_micros=10); controller.settle_invocation(reservation=reservation, usage=EconomicUsage("provider-a", 4, 6, 10, 10, "2026-01-01T00:00:00Z"))
        with pytest.raises(EconomicInvocationAlreadySettledError): controller.authorize_invocation(invocation_id=invocation_id, workspace_id=workspace_id, aggregate_id=aggregate.aggregate_id, provider_name="provider-a", reserved_tokens=10, reserved_cost_usd_micros=10)
    assert store.get_aggregate(aggregate.aggregate_id).state_data["economics"]["spent_usd_micros"] == 10


def test_cross_workspace_tenant_binding_is_rejected():
    workspace_a, workspace_b = uuid4(), uuid4(); store = InMemoryProgramStateStore(); aggregate = _aggregate(workspace_a); store.save_aggregate(aggregate); controller = ProgramStateEconomicQuotaController(store, EconomicPolicy(1_000, 1_000), clock=_clock_box()[1])
    with tenant_scope(_tenant(workspace_a)):
        with pytest.raises(Exception) as exc: controller.authorize_invocation(invocation_id=str(uuid4()), workspace_id=workspace_b, aggregate_id=aggregate.aggregate_id, provider_name="provider-a", reserved_tokens=10, reserved_cost_usd_micros=10)
    assert exc.value.__class__.__name__ == "TenancyViolationError"


def test_sqlite_persists_aggregate_economics(tmp_path):
    workspace_id = uuid4(); db = tmp_path / "ca051.db"; store = SqliteProgramStateStore(db); aggregate = _aggregate(workspace_id); store.save_aggregate(aggregate); controller = ProgramStateEconomicQuotaController(store, EconomicPolicy(1_000, 1_000), clock=_clock_box()[1])
    with tenant_scope(_tenant(workspace_id)):
        _settle(controller, str(uuid4()), workspace_id, aggregate.aggregate_id, "provider-a", 55, 25)
    persisted = SqliteProgramStateStore(db).get_aggregate(aggregate.aggregate_id)
    assert persisted.state_data["economics"]["spent_usd_micros"] == 55 and persisted.state_data["economics"]["total_tokens"] == 25




def test_unmetered_provider_cost_fails_closed():
    workspace_id = uuid4(); store = InMemoryProgramStateStore(); aggregate = _aggregate(workspace_id); store.save_aggregate(aggregate)
    controller = ProgramStateEconomicQuotaController(store, EconomicPolicy(1_000, 100), clock=_clock_box()[1])
    with tenant_scope(_tenant(workspace_id)):
        reservation = controller.authorize_invocation(invocation_id=str(uuid4()), workspace_id=workspace_id, aggregate_id=aggregate.aggregate_id, provider_name="provider-a", reserved_tokens=100, reserved_cost_usd_micros=40)
        with pytest.raises(Exception) as exc:
            controller.settle_invocation(reservation=reservation, usage=EconomicUsage("provider-a", 60, 40, 100, None, "2026-01-01T00:00:00Z"))
    assert exc.value.__class__.__name__ == "EconomicCostUnmeteredError"
    assert store.get_aggregate(aggregate.aggregate_id).state_data["economics"]["spent_usd_micros"] == 0


def test_measured_provider_cost_overrun_is_receipted_and_rejected():
    workspace_id = uuid4(); store = InMemoryProgramStateStore(); aggregate = _aggregate(workspace_id); store.save_aggregate(aggregate)
    controller = ProgramStateEconomicQuotaController(store, EconomicPolicy(1_000, 100), clock=_clock_box()[1])
    with tenant_scope(_tenant(workspace_id)):
        reservation = controller.authorize_invocation(invocation_id=str(uuid4()), workspace_id=workspace_id, aggregate_id=aggregate.aggregate_id, provider_name="provider-a", reserved_tokens=100, reserved_cost_usd_micros=40)
        with pytest.raises(Exception) as exc:
            controller.settle_invocation(reservation=reservation, usage=EconomicUsage("provider-a", 60, 40, 100, 75, "2026-01-01T00:00:00Z"))
    assert exc.value.__class__.__name__ == "BudgetCeilingExceededError"
    economics = store.get_aggregate(aggregate.aggregate_id).state_data["economics"]
    assert any(r["receipt_type"] == "budget_overrun_receipt" and r["cost_usd_micros"] == 75 for r in economics["receipts"].values())



def test_agent_invocation_runtime_settles_provider_usage_into_economic_state():
    workspace_id = uuid4(); state_id = uuid4(); store = InMemoryProgramStateStore(); store.save_aggregate(_aggregate(workspace_id, state_id))
    controller = ProgramStateEconomicQuotaController(store, EconomicPolicy(1_000, 100), clock=_clock_box()[1]); runtime = AgentInvocationRuntime(); invocation = _make_invocation(workspace_id, state_id)
    class LiveEngine:
        def infer(self, *, prompt, system_prompt, temperature, max_tokens):
            return type("Response", (), {"response_text": "live", "parsed_json": {"status": "SUCCESS"}, "prompt_tokens": 8, "completion_tokens": 4, "total_tokens": 12, "latency_micros": 100, "provider_class": "LiveProvider", "cost_usd_micros": 25})()
    with tenant_scope(_tenant(workspace_id)):
        receipt = runtime.execute(invocation, mode=ExecutionMode.PRODUCTION, model_reasoning_engine=LiveEngine(), economic_controller=controller, economic_max_cost_usd_micros=50, economic_provider_name="provider-a")
    economics = store.get_aggregate(str(state_id)).state_data["economics"]
    assert receipt.economic_status == "CHARGED" and receipt.cost_usd_micros == 25
    assert economics["spent_usd_micros"] == 25 and economics["total_tokens"] == 12


def test_invocation_runtime_requires_economics_for_state_bound_production_execution():
    runtime = AgentInvocationRuntime(); workspace_id = uuid4(); invocation = _make_invocation(workspace_id, uuid4())
    with pytest.raises(EconomicAccountingRequiredError): runtime.execute(invocation, mode=ExecutionMode.PRODUCTION)


def test_false_proof_synthetic_inference_cannot_satisfy_live_economic_accounting():
    runtime = AgentInvocationRuntime(); workspace_id = uuid4(); state_id = uuid4(); store = InMemoryProgramStateStore(); store.save_aggregate(_aggregate(workspace_id, state_id)); controller = ProgramStateEconomicQuotaController(store, EconomicPolicy(1_000, 1_000), clock=_clock_box()[1]); called = []
    def fake(_):
        called.append(True); return {"response_text": "fake", "prompt_tokens": 10, "completion_tokens": 10, "cost_usd_micros": 999}
    invocation = _make_invocation(workspace_id, state_id)
    with tenant_scope(_tenant(workspace_id)):
        with pytest.raises(EconomicAccountingRequiredError): runtime.execute(invocation, mode=ExecutionMode.PRODUCTION, inference_fn=fake, economic_controller=controller, economic_max_cost_usd_micros=50, economic_provider_name="provider-a")
    assert called == []
    assert store.get_aggregate(str(state_id)).state_data.get("economics", {}).get("spent_usd_micros", 0) == 0
