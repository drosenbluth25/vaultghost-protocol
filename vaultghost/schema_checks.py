import re
from typing import Any, Dict, Tuple

KNOWN_ANOMALIES = {"ANOMALY_MODEL_MISMATCH", "ANOMALY_FINGERPRINT_DRIFT", "FATAL_ANOMALY"}

def _is_64_hex(value: Any) -> bool:
    return isinstance(value, str) and bool(re.fullmatch(r"[0-9a-fA-F]{64}", value))

def validate(fixture: Dict[str, Any]) -> Tuple[bool, str]:
    if "model_id_confirmed" in fixture or "token_delta" in fixture:
        return False, "LEGACY_FIELD"
    if not fixture.get("provider_binding_ref"):
        return False, "MISSING_PROVIDER_BINDING"
    if fixture.get("packet_sequence") == 0 and fixture.get("prior_packet_hash") == "0" * 64:
        return False, "GENESIS_ZERO_PRIOR_HASH"
    for field in ("packet_hash", "prior_packet_hash"):
        if field in fixture and not _is_64_hex(fixture[field]):
            return False, "INVALID_HASH_FORMAT"
    for flag in fixture.get("anomaly_flags", []):
        if flag not in KNOWN_ANOMALIES:
            return False, "UNKNOWN_ANOMALY"
    if isinstance(fixture.get("confidence_interval"), str):
        return False, "CONFIDENCE_AMBIGUOUS"
    if fixture.get("hazard_index") is not None:
        return False, "HAZARD_INDEX_PRE_OI003"
    return True, "OK"
