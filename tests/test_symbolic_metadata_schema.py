import json
import unicodedata
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = REPO_ROOT / "schemas" / "symbolic_metadata.schema.json"
EXAMPLE_PATH = REPO_ROOT / "examples" / "symbolic_metadata.example.json"


def load_json(path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def test_example_manifest_validates_against_schema():
    schema = load_json(SCHEMA_PATH)
    instance = load_json(EXAMPLE_PATH)

    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(instance), key=lambda e: e.path)

    assert not errors, [error.message for error in errors]


def test_authorship_signal_is_nfc_normalized():
    instance = load_json(EXAMPLE_PATH)
    signal = instance["symbolic_metadata"]["associated_signals"][0]["authorship_signal"]

    assert signal == unicodedata.normalize("NFC", signal)


def test_uncertified_crypto_fields_are_null():
    instance = load_json(EXAMPLE_PATH)
    crypto = instance["cryptographic_signatures"]

    assert crypto["certified"] is False
    assert crypto["method"] is None
    assert crypto["hash_sha256"] is None
    assert crypto["signature"] is None
    assert crypto["public_key_id"] is None
    assert crypto["timestamp_receipt"] is None
