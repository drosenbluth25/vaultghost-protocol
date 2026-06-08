from typing import Any, Dict, Optional, Tuple

def validate(
    fixture: Dict[str, Any],
    expected_state_context_required: bool = False,
    context: Optional[Dict[str, Any]] = None,
) -> Tuple[bool, str, bool]:
    if expected_state_context_required and not context:
        return False, "MISSING_CONTEXT", True
    state = fixture.get("state", "UNKNOWN")
    if state == "SEALED" and fixture.get("fault_type") is not None:
        return False, "STATE_CONSISTENCY", False
    if state == "VOIDED" and not fixture.get("void_reason"):
        return False, "STATE_CONSISTENCY", False
    if "FATAL_ANOMALY" in fixture.get("anomaly_flags", []) and state != "VOIDED":
        return False, "FATAL_NOT_VOIDED", False
    return True, "OK", False
