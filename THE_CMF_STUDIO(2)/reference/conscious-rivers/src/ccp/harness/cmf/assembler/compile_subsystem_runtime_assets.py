import argparse
import json

from subsystem_loader import STAGE_SUBSYSTEM_ID_MAP, compile_subsystem_runtime_asset


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile CMF subsystem runtime assets.")
    parser.add_argument(
        "--stage",
        choices=["scene_builder", "editor_regeneration", "all"],
        default="all",
        help="Which runtime stage to compile.",
    )
    args = parser.parse_args()

    stage_names = list(STAGE_SUBSYSTEM_ID_MAP) if args.stage == "all" else [args.stage]
    compiled = []
    for stage_name in stage_names:
        compiled.append(
            compile_subsystem_runtime_asset(stage_name, STAGE_SUBSYSTEM_ID_MAP[stage_name])
        )

    print(json.dumps({
        "compiled_assets": [
            {
                "runtime_stage": asset["runtime_stage"],
                "asset_id": asset["asset_id"],
                "asset_path": asset["asset_path"],
                "active_subsystems": asset["active_subsystems"],
            }
            for asset in compiled
        ]
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())