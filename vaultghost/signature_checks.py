import re
from typing import Any, Dict, Optional, Tuple

def validate(
    fixture: Dict[str, Any],
    expected_generator_required: bool = False,
    context: Optional[Dict[str, Any]] = None,
) -> Tuple[bool, str, bool]:
    if expected_generator_required:
        return False, "DOUBLE_HASH_GENERATOR_REQUIRED", True
    sig = fixture.get("signature", "")
    if isinstance(sig, str) and len(re.sub(r"[^0-9a-fA-F]", "", sig)) == 128:
        return False, "RAW_RS_SIGNATURE", False
    return True, "OK", False
