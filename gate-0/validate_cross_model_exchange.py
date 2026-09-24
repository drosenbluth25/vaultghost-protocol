"""Validate the proposed v1 exchange packet, rejecting duplicate JSON keys.

Run: python gate-0/validate_cross_model_exchange.py gate-0/exchanges/VG-XM-0001.json
Requires: jsonschema >= 4.22

This checks packet shape only. It does not promote project status or resolve a
claim. Human review remains required before merging the proposal.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

SCHEMA_PATH = Path(__file__).with_name("CROSS_MODEL_EXCHANGE.schema.json")


def reject_duplicate_keys(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise ValueError(f"duplicate JSON key: {key}")
        obj[key] = value
    return obj


def validate_packet(path: Path) -> None:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicate_keys)
    Draft202012Validator.check_schema(schema)
    packet = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicate_keys)
    Draft202012Validator(schema).validate(packet)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python gate-0/validate_cross_model_exchange.py PACKET.json")
    validate_packet(Path(sys.argv[1]))
    print("VALID_PACKET_SHAPE_ONLY")
