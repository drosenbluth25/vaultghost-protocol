from typing import Any, Dict, List, Tuple

def validate(fixture: Dict[str, Any]) -> Tuple[List[str], str]:
    anomalies: List[str] = []
    req = fixture.get("model_id_requested")
    asserted = fixture.get("model_id_asserted_by_response")
    if req and asserted and req != asserted:
        anomalies.append("ANOMALY_MODEL_MISMATCH")
    anchor = fixture.get("anchor", {})
    asserted_anchor = anchor.get("asserted", {})
    computed_anchor = anchor.get("computed", {})
    sys_fp = asserted_anchor.get("system_fingerprint")
    prior_fp = asserted_anchor.get("fingerprint_prior")
    drifted = computed_anchor.get("fingerprint_drifted", False)
    if sys_fp and prior_fp and sys_fp != prior_fp and not drifted:
        anomalies.append("ANOMALY_FINGERPRINT_DRIFT")
    return anomalies, "OK"
