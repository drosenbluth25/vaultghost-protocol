"""Adversarial shape checks for the proposed cross-model exchange packet.

These tests deliberately do not treat packet validity or model agreement as
evidence that a canonical VaultGhost state has changed.
"""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

from jsonschema import ValidationError

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "gate-0" / "validate_cross_model_exchange.py"
spec = importlib.util.spec_from_file_location("vg_exchange_validator", MODULE)
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)
SOURCE = ROOT / "gate-0" / "exchanges" / "VG-XM-0001.json"


class ExchangeSchemaTests(unittest.TestCase):
    def check(self, obj):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "packet.json"
            path.write_text(json.dumps(obj), encoding="utf-8")
            validator.validate_packet(path)

    def test_candidate_packet_passes_shape_check(self):
        validator.validate_packet(SOURCE)

    def test_model_consensus_cannot_be_inserted_as_canonical_status_field(self):
        obj = json.loads(SOURCE.read_text())
        obj["canonical_state_changed"] = True
        with self.assertRaises(ValidationError):
            self.check(obj)

    def test_invalid_commit_is_rejected(self):
        obj = json.loads(SOURCE.read_text())
        obj["canonical_commit"] = "3f8a12"
        with self.assertRaises(ValidationError):
            self.check(obj)

    def test_unknown_disposition_is_rejected(self):
        obj = json.loads(SOURCE.read_text())
        obj["output_contract"]["claim_dispositions"].append("VERIFIED_BY_MODEL_CONSENSUS")
        with self.assertRaises(ValidationError):
            self.check(obj)

    def test_duplicate_json_key_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "packet.json"
            path.write_text('{"schema_version":"1.0","schema_version":"2.0"}', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "duplicate JSON key"):
                validator.validate_packet(path)


if __name__ == "__main__":
    unittest.main()
