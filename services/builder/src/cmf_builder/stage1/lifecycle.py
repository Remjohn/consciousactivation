def derive_stage1_complete(technical_status: str, operator_disposition: str | None) -> bool:
    if technical_status in ("PASS", "REVIEW") and operator_disposition == "APPROVE":
        return True
    return False

def derive_compiler_ready(stage1_complete: bool) -> bool:
    return stage1_complete
