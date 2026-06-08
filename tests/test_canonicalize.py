"""Tests for vaultghost.canonicalize (Cycle 4-A).

These tests define the *supported subset* claimed by the module. Any claim made
in the Cycle 4 documentation must be backed by an assertion here.
"""

import hashlib

import pytest

from vaultghost.canonicalize import (
    canonical_sha256,
    canonicalize_json,
    canonicalize_json_bytes,
)


# --- Required: key ordering is deterministic ------------------------------


def test_key_ordering_is_deterministic_regardless_of_insertion_order():
    a = {"b": 1, "a": 2, "c": 3}
    b = {"c": 3, "a": 2, "b": 1}
    expected = '{"a":2,"b":1,"c":3}'
    assert canonicalize_json(a) == expected
    assert canonicalize_json(b) == expected
    assert canonicalize_json(a) == canonicalize_json(b)


def test_key_ordering_is_repeatable_across_calls():
    obj = {"z": 1, "m": 2, "a": 3, "Z": 4, "A": 5}
    first = canonicalize_json(obj)
    for _ in range(50):
        assert canonicalize_json(obj) == first
    # Uppercase precedes lowercase under code-unit/UTF-16 ordering.
    assert first == '{"A":5,"Z":4,"a":3,"m":2,"z":1}'


def test_object_member_ordering_uses_utf16_code_units():
    # U+FFFF (BMP, code unit 0xFFFF) vs U+10000 (non-BMP, leading surrogate
    # 0xD800). Under Unicode code-point ordering, U+FFFF < U+10000. Under
    # UTF-16 code-unit ordering, the U+10000 key (starts 0xD800) sorts FIRST.
    obj = {"\uffff": 1, "\U00010000": 2}
    out = canonicalize_json(obj)
    assert out.index('"\U00010000"') < out.index('"\uffff"')


def test_object_keys_sort_by_utf16_code_units_not_python_codepoints():
    # U+1F600 (non-BMP, leading surrogate 0xD83D) vs U+E000 (BMP private-use,
    # 0xE000). Code-point order puts U+E000 first; UTF-16 code-unit order puts
    # U+1F600 first because 0xD83D < 0xE000.
    value = {"\ue000": 1, "\U0001F600": 2}
    assert canonicalize_json(value) == '{"\U0001F600":2,"\ue000":1}'


def test_lone_surrogate_value_rejected():
    with pytest.raises(ValueError):
        canonicalize_json(chr(0xD800))


def test_lone_surrogate_key_rejected():
    with pytest.raises(ValueError):
        canonicalize_json({chr(0xD800): 1})


# --- Required: whitespace does not affect canonical output ----------------


def test_whitespace_in_source_does_not_affect_output():
    import json

    dense = '{"a":1,"b":[1,2,3]}'
    spaced = '{\n "a" : 1,\n "b" : [ 1, 2, 3 ]\n}'
    assert canonicalize_json(json.loads(dense)) == canonicalize_json(json.loads(spaced))
    assert canonicalize_json(json.loads(spaced)) == '{"a":1,"b":[1,2,3]}'


def test_output_contains_no_insignificant_whitespace():
    out = canonicalize_json({"a": 1, "b": {"c": 2}})
    assert out == '{"a":1,"b":{"c":2}}'
    assert " " not in out and "\n" not in out and "\t" not in out


# --- Required: nested object keys are recursively sorted ------------------


def test_nested_object_keys_are_recursively_sorted():
    obj = {
        "outer_b": {"y": 1, "x": 2},
        "outer_a": {"n": {"d": 1, "c": 2, "b": 3}},
    }
    expected = '{"outer_a":{"n":{"b":3,"c":2,"d":1}},"outer_b":{"x":2,"y":1}}'
    assert canonicalize_json(obj) == expected


def test_objects_nested_inside_arrays_are_sorted():
    obj = {"items": [{"b": 1, "a": 2}, {"d": 3, "c": 4}]}
    assert canonicalize_json(obj) == '{"items":[{"a":2,"b":1},{"c":4,"d":3}]}'


# --- Required: array order is preserved -----------------------------------


def test_array_order_is_preserved():
    assert canonicalize_json([3, 1, 2, "b", "a"]) == '[3,1,2,"b","a"]'


def test_array_order_preserved_under_nesting():
    assert canonicalize_json({"x": [["c", "a"], ["b"]]}) == '{"x":[["c","a"],["b"]]}'


# --- Required: NaN and Infinity are rejected ------------------------------


def test_nan_is_rejected():
    with pytest.raises(ValueError):
        canonicalize_json(float("nan"))


def test_positive_infinity_is_rejected():
    with pytest.raises(ValueError):
        canonicalize_json(float("inf"))


def test_negative_infinity_is_rejected():
    with pytest.raises(ValueError):
        canonicalize_json(float("-inf"))


def test_nan_nested_inside_structure_is_rejected():
    with pytest.raises(ValueError):
        canonicalize_json({"a": [1, float("inf")]})


# --- Required: non-string object keys are rejected ------------------------


def test_integer_key_is_rejected():
    with pytest.raises(TypeError):
        canonicalize_json({1: "a"})


def test_none_key_is_rejected():
    with pytest.raises(TypeError):
        canonicalize_json({None: "a"})


def test_bool_key_is_rejected():
    with pytest.raises(TypeError):
        canonicalize_json({True: "a"})


def test_float_key_is_rejected():
    with pytest.raises(TypeError):
        canonicalize_json({1.5: "a"})


# --- Required: canonical_sha256 is stable across equivalent objects -------


def test_canonical_sha256_stable_across_equivalent_objects():
    a = {"b": 1, "a": [1, 2, {"y": 1, "x": 2}]}
    b = {"a": [1, 2, {"x": 2, "y": 1}], "b": 1}
    assert canonical_sha256(a) == canonical_sha256(b)


def test_canonical_sha256_matches_manual_hash_of_canonical_bytes():
    obj = {"a": 1, "b": 2}
    manual = hashlib.sha256(canonicalize_json_bytes(obj)).hexdigest()
    assert canonical_sha256(obj) == manual


def test_canonical_sha256_differs_for_different_values():
    assert canonical_sha256({"a": 1}) != canonical_sha256({"a": 2})


# --- Supporting: bytes output, primitives, escaping, numbers --------------


def test_bytes_output_is_utf8():
    obj = {"k": "caf\u00e9"}  # 'é' -> 0xC3 0xA9 in UTF-8
    b = canonicalize_json_bytes(obj)
    assert isinstance(b, (bytes, bytearray))
    assert b == '{"k":"caf\u00e9"}'.encode("utf-8")
    assert b"\xc3\xa9" in b


def test_primitive_literals():
    assert canonicalize_json(True) == "true"
    assert canonicalize_json(False) == "false"
    assert canonicalize_json(None) == "null"


def test_string_control_character_escaping():
    s = "a\tb\nc\rd\"e\\f\x00g\x1fh"
    expected = '"a\\tb\\nc\\rd\\"e\\\\f\\u0000g\\u001fh"'
    assert canonicalize_json(s) == expected


def test_non_ascii_is_emitted_literally_not_escaped():
    assert canonicalize_json("\u00e9\u4e2d") == '"\u00e9\u4e2d"'


@pytest.mark.parametrize(
    "value,expected",
    [
        (0, "0"),
        (-0, "0"),
        (5, "5"),
        (-5, "-5"),
        (10**30, "1" + "0" * 30),  # exact big int, not float64
        (0.0, "0"),
        (-0.0, "0"),
        (1.0, "1"),
        (100.0, "100"),
        (-100.0, "-100"),
        (1.5, "1.5"),
        (-1.5, "-1.5"),
        (0.1, "0.1"),
        (12345.678, "12345.678"),
        (1e16, "10000000000000000"),
        (1e21, "1e+21"),
        (1e-6, "0.000001"),
        (1e-7, "1e-7"),
        (1.5e300, "1.5e+300"),
    ],
)
def test_number_serialization_subset(value, expected):
    assert canonicalize_json(value) == expected


def test_int_and_equivalent_float_converge():
    assert canonicalize_json(1) == canonicalize_json(1.0) == "1"


# --- Supporting: unsupported types are rejected ---------------------------


def test_unsupported_type_is_rejected():
    with pytest.raises(TypeError):
        canonicalize_json({"a", "b"})  # set
    with pytest.raises(TypeError):
        canonicalize_json(b"bytes")


def test_idempotence_of_repeated_serialization():
    obj = {"b": [2, 1], "a": {"d": 4, "c": 3}}
    once = canonicalize_json(obj)
    assert canonicalize_json(obj) == once
