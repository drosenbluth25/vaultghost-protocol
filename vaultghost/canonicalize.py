"""Deterministic JSON canonicalization for VaultGhost (Cycle 4-A).

This module emits a single, deterministic byte serialization for a Python value
drawn from the JSON data model (``dict`` / ``list`` / ``str`` / ``int`` /
``float`` / ``bool`` / ``None``). It is foundational groundwork for later
hash-chain recomputation and signature verification work. It does **not**
itself perform hashing of execution packets, signing, signature verification,
or hash-chain recomputation, and it does **not** assert RFC 8785 compliance.

Supported, tested canonicalization properties (see ``tests/test_canonicalize.py``):

* Object member ordering follows UTF-16 code-unit ordering (the ordering rule
  of RFC 8785 sec. 3.2.3). This ordering rule is tested; matching one rule is
  not equivalent to full RFC 8785 compliance.
* Insignificant whitespace is absent from output (there is no place to emit it).
* Object members are recursively canonicalized; nesting is fully ordered.
* Array element order is preserved exactly.
* ``NaN``, ``Infinity`` and ``-Infinity`` are rejected (``ValueError``).
* Non-string object keys are rejected (``TypeError``).
* Output is UTF-8 encoded by ``canonicalize_json_bytes``.

Number handling is documented in ``_serialize_float`` / ``_serialize_int``.
Determinism (same input -> identical output -> identical SHA-256) is the
property this module guarantees and tests. Cross-implementation byte-for-byte
equivalence with arbitrary third-party JCS implementations is NOT claimed.
"""

from __future__ import annotations

import hashlib
import math
from typing import Any

__all__ = [
    "canonicalize_json",
    "canonicalize_json_bytes",
    "canonical_sha256",
    "CanonicalizationError",
]


class CanonicalizationError(Exception):
    """Base class for canonicalization failures.

    ``TypeError`` and ``ValueError`` are raised for the specific rejection
    cases mandated by the spec (non-string keys; non-finite floats). This
    class exists for callers that prefer a single catchable type.
    """


# RFC 8785 sec. 3.2.2.2 short escapes plus the two mandatory JSON escapes.
_SHORT_ESCAPES = {
    0x08: "\\b",
    0x09: "\\t",
    0x0A: "\\n",
    0x0C: "\\f",
    0x0D: "\\r",
    0x22: '\\"',
    0x5C: "\\\\",
}


def _reject_lone_surrogates(value: str) -> None:
    for ch in value:
        cp = ord(ch)
        if 0xD800 <= cp <= 0xDFFF:
            raise ValueError("lone surrogate code points are not permitted")


def _serialize_string(value: str) -> str:
    """Serialize a string with minimal JSON escaping.

    Lone surrogate code points (U+D800..U+DFFF) are rejected up front with
    ``ValueError`` so the failure is deterministic and early rather than
    deferred to UTF-8 encode time. Control characters U+0000..U+001F use short
    escapes where defined, else a lowercase ``\\u00XX`` escape. All other code
    points (including non-ASCII) are emitted literally; final UTF-8 encoding
    happens in ``canonicalize_json_bytes``.
    """

    _reject_lone_surrogates(value)

    out = ['"']
    append = out.append
    for ch in value:
        cp = ord(ch)
        short = _SHORT_ESCAPES.get(cp)
        if short is not None:
            append(short)
        elif cp < 0x20:
            append("\\u%04x" % cp)
        else:
            append(ch)
    append('"')
    return "".join(out)


def _serialize_int(value: int) -> str:
    """Serialize a Python ``int`` as an exact decimal string.

    Deliberate divergence from IEEE-754: Python integers are arbitrary
    precision, and the exact decimal form is preserved (no float64 rounding).
    This favors exact-value fidelity for the integer subset over ECMAScript
    Number semantics, and is therefore NOT a claim of RFC 8785 number
    canonicalization.
    """

    return str(value)


def _serialize_float(value: float) -> str:
    """Serialize a finite ``float`` to a deterministic shortest form.

    Uses a CPython repr-derived deterministic finite-float serialization with
    ECMAScript-shaped fixed/exponential thresholds for the tested cases. This
    is not a certified implementation of the full RFC 8785 / ECMAScript number
    grammar.

    Non-finite values are rejected by the caller (``_serialize``).
    """

    if value == 0.0:
        # Covers +0.0 and -0.0; ECMAScript renders both as "0".
        return "0"

    if value < 0:
        return "-" + _serialize_float(-value)

    r = repr(value)  # shortest round-trip decimal in CPython 3
    if "e" in r:
        mant, exp_str = r.split("e")
        exp = int(exp_str)
    else:
        mant, exp = r, 0

    if "." in mant:
        int_part, frac_part = mant.split(".")
    else:
        int_part, frac_part = mant, ""

    digits = int_part + frac_part

    # value == int(digits) * 10**point_exp
    point_exp = exp - len(frac_part)

    # Strip leading zeros.
    stripped = digits.lstrip("0")
    digits = stripped

    # Strip trailing zeros, compensating the exponent.
    before = len(digits)
    digits = digits.rstrip("0")
    point_exp += before - len(digits)

    # digits now has no leading/trailing zeros (and is non-empty: value != 0).
    k = len(digits)  # significant digit count
    n = k + point_exp  # value == 0.<digits> * 10**n (ES "k/n" framing)
    s = digits

    if k <= n <= 21:
        return s + "0" * (n - k)

    if 0 < n <= 21:
        return s[:n] + "." + s[n:]

    if -6 < n <= 0:
        return "0." + "0" * (-n) + s

    # Exponential form.
    mant_str = s if k == 1 else s[0] + "." + s[1:]
    e_val = n - 1
    sign = "+" if e_val >= 0 else "-"
    return mant_str + "e" + sign + str(abs(e_val))


def _sort_key(key: str) -> bytes:
    """UTF-16 code-unit sort key (RFC 8785 sec. 3.2.3 ordering rule).

    UTF-16-BE byte order equals UTF-16 code-unit order, so lexicographic
    comparison of these byte strings reproduces code-unit ordering, including
    correct surrogate-pair behavior for non-BMP keys. Lone surrogate code
    points in keys are rejected with ``ValueError`` before encoding.
    """

    _reject_lone_surrogates(key)
    return key.encode("utf-16-be")


def _serialize(value: Any) -> str:
    # bool is a subclass of int -> must precede the int branch.
    if value is True:
        return "true"

    if value is False:
        return "false"

    if value is None:
        return "null"

    if isinstance(value, str):
        return _serialize_string(value)

    if isinstance(value, int):
        return _serialize_int(value)

    if isinstance(value, float):
        if math.isnan(value):
            raise ValueError("NaN is not permitted in canonical JSON")
        if math.isinf(value):
            raise ValueError("Infinity is not permitted in canonical JSON")
        return _serialize_float(value)

    if isinstance(value, dict):
        for key in value:
            if not isinstance(key, str):
                raise TypeError(
                    "object keys must be strings, got %s" % type(key).__name__
                )
        members = (
            _serialize_string(key) + ":" + _serialize(value[key])
            for key in sorted(value, key=_sort_key)
        )
        return "{" + ",".join(members) + "}"

    if isinstance(value, (list, tuple)):
        return "[" + ",".join(_serialize(item) for item in value) + "]"

    raise TypeError("unsupported type for canonical JSON: %s" % type(value).__name__)


def canonicalize_json(value: Any) -> str:
    """Return the canonical JSON text for ``value``.

    Input is a Python value from the JSON data model (``dict``/``list``/
    ``tuple``/``str``/``int``/``float``/``bool``/``None``). Raises ``TypeError``
    for unsupported types or non-string object keys, and ``ValueError`` for
    non-finite floats.
    """

    return _serialize(value)


def canonicalize_json_bytes(value: Any) -> bytes:
    """Return the canonical JSON serialization of ``value`` as UTF-8 bytes."""

    return canonicalize_json(value).encode("utf-8")


def canonical_sha256(value: Any) -> str:
    """Return the lowercase hex SHA-256 of the canonical UTF-8 serialization.

    This hashes the canonical form of an in-memory value for determinism
    checks. It is NOT execution-packet hashing, NOT hash-chain recomputation,
    and NOT signature verification.
    """

    return hashlib.sha256(canonicalize_json_bytes(value)).hexdigest()
