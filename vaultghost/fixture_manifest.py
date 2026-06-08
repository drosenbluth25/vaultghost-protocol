import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

@dataclass(frozen=True)
class ExpectedFixture:
    fixture: str
    patch_ids: List[str]
    layer: str
    expected_result: str
    existing_error_code: Optional[str]
    proposed_error_code: Optional[str]
    state_context_required: bool
    semantic_check_required: bool
    generator_required: bool
    ratification_status: str
    notes: str = ""

def load_expected_results(path: str | Path) -> Dict[str, ExpectedFixture]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("EXPECTED_RESULTS.json must be a list of objects")
    results: Dict[str, ExpectedFixture] = {}
    for row in data:
        name = row["fixture"]
        results[name] = ExpectedFixture(
            fixture=name,
            patch_ids=list(row.get("patch_ids", [])),
            layer=row.get("layer", "UNKNOWN"),
            expected_result=row.get("expected_result", "PARSE_ERROR"),
            existing_error_code=row.get("existing_error_code"),
            proposed_error_code=row.get("proposed_error_code"),
            state_context_required=bool(row.get("state_context_required", False)),
            semantic_check_required=bool(row.get("semantic_check_required", False)),
            generator_required=bool(row.get("generator_required", False)),
            ratification_status=row.get("ratification_status", "PROPOSED"),
            notes=row.get("notes", ""),
        )
    return results

def get_expected_for_fixture(name: str, manifest: Dict[str, ExpectedFixture]) -> ExpectedFixture:
    if name not in manifest:
        raise KeyError(f"Fixture {name} missing from EXPECTED_RESULTS.json manifest. Failing closed.")
    return manifest[name]
