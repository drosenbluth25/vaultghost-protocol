# Cycle 4-A — JCS Canonicalization Module

Status: implemented (module + tests; real pytest execution pending CI).
Scope: foundational groundwork only. This cycle adds deterministic JSON
canonicalization. It does **not** add hash-chain recomputation, signing, or
signature verification, and makes no readiness, compliance, patent, external-
validation, or full-cryptographic-verification claims.

## 1. Purpose

Provide a single, deterministic byte serialization for a Python value drawn
from the JSON data model, so that later cycles can compute stable digests over
canonical bytes. Determinism (same input → identical bytes → identical
SHA-256) is the only guarantee asserted here.

## 2. Public API (`vaultghost/canonicalize.py`)

| Function | Signature | Returns |
| --- | --- | --- |
| `canonicalize_json` | `(value) -> str` | canonical JSON text |
| `canonicalize_json_bytes` | `(value) -> bytes` | UTF-8 encoding of the canonical text |
| `canonical_sha256` | `(value) -> str` | lowercase hex SHA-256 of the canonical UTF-8 bytes |

Accepted input types: `dict`, `list`, `tuple`, `str`, `int`, `float`, `bool`,
`None`. All other types raise `TypeError`.

## 3. Canonicalization rules (each backed by a test)

1. **Object member ordering** follows UTF-16 code-unit ordering — the ordering
   rule of RFC 8785 §3.2.3 — implemented via UTF-16-BE byte comparison.
   Verified for ASCII, mixed-case, and BMP-vs-non-BMP cases where code-point
   order and code-unit order diverge.
2. **No insignificant whitespace** in output.
3. **Recursive ordering**: members of nested objects, including objects nested
   inside arrays, are canonicalized recursively.
4. **Array order preserved** exactly, including nested arrays.
5. **`NaN`, `Infinity`, `-Infinity` rejected** with `ValueError`, including when
   nested.
6. **Non-string object keys rejected** with `TypeError` (`int`, `float`, `bool`,
   `None`).
7. **UTF-8 output** from `canonicalize_json_bytes`.
8. **String escaping**: control characters `U+0000..U+001F` use the RFC 8785
   short escapes where defined, otherwise lowercase `\u00XX`. Non-ASCII code
   points are emitted literally, then UTF-8 encoded, not `\u`-escaped. Lone
   surrogate code points (`U+D800..U+DFFF`), in both string values and object
   keys, are rejected with `ValueError` before encoding.
9. **`canonical_sha256` stability** across structurally-equivalent objects that
   differ only in key insertion order.

## 4. Number handling (explicit boundary)

- **Integers** (`int`) serialize to their exact decimal string. This is a
  deliberate divergence from IEEE-754 float64: arbitrary-precision integers are
  preserved exactly rather than rounded. It is therefore **not** ECMAScript /
  RFC 8785 number canonicalization.
- **Floats** (`float`) serialize via an ECMAScript-`Number::toString`-shaped
  shortest form derived from CPython's shortest `repr`. Verified for the
  specific cases enumerated in
  `tests/test_canonicalize.py::test_number_serialization_subset` only.
- Cross-implementation, byte-for-byte equivalence with arbitrary third-party
  JCS implementations is **not** claimed and **not** tested.

## 5. Verification path

- Test file: `tests/test_canonicalize.py`.
- CI gate: `.github/workflows/cycle4a-ci.yml`.
- Required commands:
  - `python -m pytest tests/test_canonicalize.py -v --tb=short`
  - `python -m pytest tests/ -v --tb=short`
- Required merge condition: do not merge until the Cycle 4-A gate check shows
  `49 passed` for `tests/test_canonicalize.py` and the broader `tests/` suite
  completes successfully.

## 6. Out of scope (deferred / not implemented in 4-A)

- P-256 / ECDSA key handling and signing.
- Signature verification.
- Hash-chain recomputation over execution packets.
- Key Registry validation.
- Model Profile Registry validation.
- Hazard Index formalization.
- Any binding of these functions to Cycle 3 evidence artifacts.

## 7. Evidence boundary

This document and the module assert deterministic canonicalization of in-memory
Python values and the SHA-256 of that canonical form, as tested by the included
test file. They assert **no**: production readiness, regulatory or standards
compliance, RFC 8785 certification or full JCS compliance, patent validity or
novelty, external validation, full cryptographic verification, hash-chain
recomputation, key-registry validation, profile-registry validation, or
hazard-index formalization.
