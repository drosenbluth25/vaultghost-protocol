from typing import Any, Dict, Tuple

def validate(fixture: Dict[str, Any]) -> Tuple[bool, str]:
    reasoning = fixture.get("vendor_reported", {}).get("token_delta", {}).get("reasoning", {})
    if "content" in reasoning:
        return False, "REASONING_CONTENT"
    if reasoning.get("present") is False and reasoning.get("count") is not None:
        return False, "TOKEN_SENTINEL"
    return True, "OK"
