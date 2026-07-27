import argparse
import json

from scene_intelligence_loader import compile_scene_intelligence_runtime_asset


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile CMF container/component runtime assets.")
    parser.add_argument(
        "--stage",
        choices=["scene_builder", "editor_regeneration", "all"],
        default="all",
        help="Which runtime stage to compile.",
    )
    args = parser.parse_args()

    stage_names = ["scene_builder", "editor_regeneration"] if args.stage == "all" else [args.stage]
    compiled = [compile_scene_intelligence_runtime_asset(stage_name) for stage_name in stage_names]

    print(json.dumps({
        "compiled_assets": [
            {
                "runtime_stage": asset["runtime_stage"],
                "asset_id": asset["asset_id"],
                "asset_path": asset["asset_path"],
                "active_containers": asset["active_containers"],
                "active_components": asset["active_components"],
            }
            for asset in compiled
        ]
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())