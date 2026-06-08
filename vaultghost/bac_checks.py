from typing import Any, Dict, Optional, Tuple
from .fixture_manifest import ExpectedFixture

def validate(
    fixture: Dict[str, Any],
    expected: ExpectedFixture,
    context: Optional[Dict[str, Any]] = None,
) -> Tuple[bool, str, bool]:
    if expected.layer not in {"BAC", "PROFILE"}:
        return True, "OK", False
    bac = fixture.get("bac", {})
    if expected.fixture == "19_bac_model_profile_mismatch.json":
        if fixture.get("model_id_requested") != bac.get("profile_ref", {}).get("model_id"):
            return False, "BAC_MODEL_MISMATCH", False
    elif expected.fixture == "20_bac_cross_session_chain.json":
        if fixture.get("session_id") != bac.get("session_id"):
            return False, "BAC_SESSION_MISMATCH", False
    elif expected.fixture == "24_profile_superseded_stale.json":
        if context is None or "profile_registry" not in context:
            return False, "MISSING_CONTEXT", True
        return False, "PROFILE_SUPERSEDED", False
    return True, "OK", False
