from __future__ import annotations

from hashlib import sha256
import json
from typing import Mapping

from cmf_builder.application.productization_contracts import (
    ActivativeInputContract,
    OperatorManifestRequest,
    OperatorManifestResult,
    ProductizationError,
    ProductizationErrorCode,
)
from cmf_builder.domain.operator_manifest import (
    ManifestMode,
    OperatorManifestDocument,
    OperatorManifestInvalid,
    OperatorTaskDefinition,
    normalize_json,
    reject_forbidden_claims,
    reject_identity_dna_mutation,
    require_exact_fields,
    require_immutable_ref,
    require_object,
    require_ref_tuple,
    require_text,
    require_text_tuple,
)


GENERIC_ROOT_FIELDS = frozenset(
    {"manifest_id", "manifest_version", "task_id", "mode", "task"}
)
ACTIVATIVE_ROOT_FIELDS = GENERIC_ROOT_FIELDS | {"category_id", "activative_input"}
ACTIVATIVE_REQUIRED_FIELDS = frozenset(
    {
        "source_premise_ref",
        "identity_dna_ref",
        "context_premise_ref",
        "resonance_map_ref",
        "matrix_of_edging_ref",
        "activative_intelligence_pack_ref",
        "hidden_pressure",
        "activation_directions",
        "roles",
        "stance",
        "stakes",
        "identity_urges",
        "participation_design",
        "intended_reaction",
        "smallest_useful_commitment",
        "evidence_provenance_refs",
        "evaluation_contract_ref",
        "wrong_reading_locks",
    }
)
ACTIVATIVE_OPTIONAL_FIELDS = frozenset(
    {"reaction_receipt_refs", "expression_moment_refs"}
)
ACTIVATIVE_FIELDS = ACTIVATIVE_REQUIRED_FIELDS | ACTIVATIVE_OPTIONAL_FIELDS


class OperatorManifestParser:
    def parse(self, request: OperatorManifestRequest) -> OperatorManifestResult:
        if not isinstance(request, OperatorManifestRequest):
            raise ProductizationError(
                ProductizationErrorCode.INVALID_MANIFEST,
                "Operator manifest request has the wrong contract type.",
            )
        if not isinstance(request.manifest_bytes, bytes) or not request.manifest_bytes:
            raise ProductizationError(
                ProductizationErrorCode.INVALID_MANIFEST,
                "Operator manifest bytes cannot be empty.",
                field_path="manifest_bytes",
            )
        if not isinstance(request.source_name, str) or not request.source_name.strip():
            raise ProductizationError(
                ProductizationErrorCode.INVALID_MANIFEST,
                "Operator manifest source name cannot be empty.",
                field_path="source_name",
            )
        try:
            root = _load_json(request.manifest_bytes)
            manifest = require_object(root, "manifest")
            mode = _parse_mode(manifest.get("mode"))
            require_exact_fields(
                manifest,
                ACTIVATIVE_ROOT_FIELDS
                if mode is ManifestMode.ACTIVATIVE
                else GENERIC_ROOT_FIELDS,
                "manifest",
            )
            reject_forbidden_claims(manifest, "manifest")
            task = OperatorTaskDefinition.from_mapping(manifest["task"])
            reject_identity_dna_mutation(task.canonical_dict(), "task")
            document = OperatorManifestDocument(
                manifest_id=require_text(manifest["manifest_id"], "manifest.manifest_id"),
                manifest_version=require_text(
                    manifest["manifest_version"], "manifest.manifest_version"
                ),
                task_id=require_text(manifest["task_id"], "manifest.task_id"),
                mode=mode,
                category_id=(
                    require_text(manifest["category_id"], "manifest.category_id")
                    if mode is ManifestMode.ACTIVATIVE
                    else None
                ),
                task=task,
            )
            activative_contract, activative_normalized = _parse_activative(
                manifest.get("activative_input"), mode
            )
            normalized = document.canonical_dict(
                activative_input=activative_normalized
            )
            canonical_bytes = _canonical_json(normalized)
        except ProductizationError:
            raise
        except OperatorManifestInvalid as error:
            code = (
                ProductizationErrorCode.INVALID_ACTIVATIVE_INPUT
                if error.field_path.startswith("activative_input")
                else ProductizationErrorCode.INVALID_MANIFEST
            )
            raise ProductizationError(
                code,
                str(error),
                field_path=error.field_path,
                context={"source_name": request.source_name},
            ) from error
        return OperatorManifestResult(
            manifest_id=document.manifest_id,
            manifest_version=document.manifest_version,
            task_id=document.task_id,
            mode=document.mode.value,
            category_id=document.category_id,
            canonical_bytes=canonical_bytes,
            manifest_hash=f"sha256:{sha256(canonical_bytes).hexdigest()}",
            normalized=normalized,
            activative_input=activative_contract,
        )


def parse_operator_manifest(request: OperatorManifestRequest) -> OperatorManifestResult:
    return OperatorManifestParser().parse(request)


def _load_json(content: bytes) -> object:
    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ProductizationError(
            ProductizationErrorCode.INVALID_MANIFEST,
            "Operator manifest must be UTF-8 JSON.",
            field_path="manifest_bytes",
        ) from error
    if text.startswith("\ufeff"):
        raise ProductizationError(
            ProductizationErrorCode.INVALID_MANIFEST,
            "UTF-8 BOM is not accepted in a governed manifest.",
            field_path="manifest_bytes",
        )

    def reject_duplicate(pairs: list[tuple[str, object]]) -> dict[str, object]:
        result: dict[str, object] = {}
        for key, value in pairs:
            if key in result:
                raise ProductizationError(
                    ProductizationErrorCode.INVALID_MANIFEST,
                    "Duplicate JSON object keys are not canonical.",
                    field_path=key,
                )
            result[key] = value
        return result

    def reject_constant(value: str) -> object:
        raise ProductizationError(
            ProductizationErrorCode.INVALID_MANIFEST,
            "Non-finite numbers are not valid governed JSON.",
            field_path="manifest",
            context={"constant": value},
        )

    try:
        return json.loads(
            text,
            object_pairs_hook=reject_duplicate,
            parse_constant=reject_constant,
        )
    except ProductizationError:
        raise
    except (json.JSONDecodeError, RecursionError) as error:
        raise ProductizationError(
            ProductizationErrorCode.INVALID_MANIFEST,
            "Operator manifest is not valid JSON.",
            field_path="manifest_bytes",
            context={"line": getattr(error, "lineno", None)},
        ) from error


def _parse_mode(value: object) -> ManifestMode:
    try:
        return ManifestMode(require_text(value, "manifest.mode"))
    except ValueError as error:
        raise OperatorManifestInvalid(
            "Mode must be exactly 'generic' or 'activative'.",
            field_path="manifest.mode",
        ) from error


def _parse_activative(
    value: object, mode: ManifestMode
) -> tuple[ActivativeInputContract | None, Mapping[str, object] | None]:
    if mode is ManifestMode.GENERIC:
        if value is not None:
            raise OperatorManifestInvalid(
                "Generic manifests must not contain Activative Intelligence input.",
                field_path="activative_input",
            )
        return None, None
    fields = require_object(value, "activative_input")
    observed = frozenset(fields)
    missing = sorted(ACTIVATIVE_REQUIRED_FIELDS - observed)
    unexpected = sorted(observed - ACTIVATIVE_FIELDS)
    if missing or unexpected:
        detail = []
        if missing:
            detail.append(f"missing={','.join(missing)}")
        if unexpected:
            detail.append(f"unexpected={','.join(unexpected)}")
        raise OperatorManifestInvalid(
            f"Activative fields do not match the governed contract ({'; '.join(detail)}).",
            field_path="activative_input",
        )
    reject_forbidden_claims(fields, "activative_input")

    source_premise_ref = require_immutable_ref(
        fields["source_premise_ref"], "activative_input.source_premise_ref"
    )
    identity_dna_ref = require_immutable_ref(
        fields["identity_dna_ref"], "activative_input.identity_dna_ref"
    )
    context_premise_ref = require_immutable_ref(
        fields["context_premise_ref"], "activative_input.context_premise_ref"
    )
    resonance_map_ref = require_immutable_ref(
        fields["resonance_map_ref"], "activative_input.resonance_map_ref"
    )
    matrix_of_edging_ref = require_immutable_ref(
        fields["matrix_of_edging_ref"], "activative_input.matrix_of_edging_ref"
    )
    activative_intelligence_pack_ref = require_immutable_ref(
        fields["activative_intelligence_pack_ref"],
        "activative_input.activative_intelligence_pack_ref",
    )
    hidden_pressure = require_text(
        fields["hidden_pressure"], "activative_input.hidden_pressure"
    )
    activation_directions = require_text_tuple(
        fields["activation_directions"], "activative_input.activation_directions"
    )
    roles = require_text_tuple(fields["roles"], "activative_input.roles")
    stance = require_text(fields["stance"], "activative_input.stance")
    stakes = require_text_tuple(fields["stakes"], "activative_input.stakes")
    identity_urges = require_text_tuple(
        fields["identity_urges"], "activative_input.identity_urges"
    )
    participation_design = require_text(
        fields["participation_design"], "activative_input.participation_design"
    )
    intended_reaction = require_text(
        fields["intended_reaction"], "activative_input.intended_reaction"
    )
    smallest_useful_commitment = require_text(
        fields["smallest_useful_commitment"],
        "activative_input.smallest_useful_commitment",
    )
    evidence_provenance_refs = require_ref_tuple(
        fields["evidence_provenance_refs"],
        "activative_input.evidence_provenance_refs",
    )
    evaluation_contract_ref = require_immutable_ref(
        fields["evaluation_contract_ref"],
        "activative_input.evaluation_contract_ref",
    )
    wrong_reading_locks = require_text_tuple(
        fields["wrong_reading_locks"], "activative_input.wrong_reading_locks"
    )
    reaction_receipt_refs = require_ref_tuple(
        fields.get("reaction_receipt_refs", []),
        "activative_input.reaction_receipt_refs",
        allow_empty=True,
    )
    expression_moment_refs = require_ref_tuple(
        fields.get("expression_moment_refs", []),
        "activative_input.expression_moment_refs",
        allow_empty=True,
    )
    contract = ActivativeInputContract(
        source_premise_ref=source_premise_ref,
        identity_dna_ref=identity_dna_ref,
        context_premise_ref=context_premise_ref,
        resonance_map_ref=resonance_map_ref,
        matrix_of_edging_ref=matrix_of_edging_ref,
        activative_intelligence_pack_ref=activative_intelligence_pack_ref,
        hidden_pressure=hidden_pressure,
        activation_directions=activation_directions,
        roles=roles,
        stance=stance,
        stakes=stakes,
        identity_urges=identity_urges,
        participation_design=participation_design,
        intended_reaction=intended_reaction,
        smallest_useful_commitment=smallest_useful_commitment,
        evidence_provenance_refs=evidence_provenance_refs,
        evaluation_contract_ref=evaluation_contract_ref,
        wrong_reading_locks=wrong_reading_locks,
        reaction_receipt_refs=reaction_receipt_refs,
        expression_moment_refs=expression_moment_refs,
    )
    normalized = {
        "source_premise_ref": source_premise_ref,
        "identity_dna_ref": identity_dna_ref,
        "context_premise_ref": context_premise_ref,
        "resonance_map_ref": resonance_map_ref,
        "matrix_of_edging_ref": matrix_of_edging_ref,
        "activative_intelligence_pack_ref": activative_intelligence_pack_ref,
        "hidden_pressure": hidden_pressure,
        "activation_directions": list(activation_directions),
        "roles": list(roles),
        "stance": stance,
        "stakes": list(stakes),
        "identity_urges": list(identity_urges),
        "participation_design": participation_design,
        "intended_reaction": intended_reaction,
        "smallest_useful_commitment": smallest_useful_commitment,
        "evidence_provenance_refs": list(evidence_provenance_refs),
        "evaluation_contract_ref": evaluation_contract_ref,
        "wrong_reading_locks": list(wrong_reading_locks),
        "reaction_receipt_refs": list(reaction_receipt_refs),
        "expression_moment_refs": list(expression_moment_refs),
    }
    return contract, normalize_json(normalized)


def _canonical_json(value: object) -> bytes:
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        + "\n"
    ).encode("utf-8")
