from datetime import datetime, timezone
from typing import Any, Dict, Optional, Tuple

def _parse_utc_z(ts: Any) -> Optional[datetime]:
    if not isinstance(ts, str) or not ts.endswith("Z"):
        return None
    try:
        parsed = datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return None
    return parsed.astimezone(timezone.utc)

def validate(
    fixture: Dict[str, Any],
    expected_time_context_required: bool = False,
    context: Optional[Dict[str, Any]] = None,
) -> Tuple[bool, str, bool]:
    ts = fixture.get("timestamp_iso8601", "")
    current_dt = _parse_utc_z(ts)
    if current_dt is None:
        return False, "NON_UTC_TIMESTAMP", False
    if expected_time_context_required:
        if context is None or "prior_timestamp" not in context:
            return False, "MISSING_CONTEXT", True
        prior_dt = _parse_utc_z(context["prior_timestamp"])
        if prior_dt is None:
            return False, "MISSING_CONTEXT", True
        if current_dt < prior_dt:
            return False, "TIMESTAMP_REGRESSION", False
    return True, "OK", False
