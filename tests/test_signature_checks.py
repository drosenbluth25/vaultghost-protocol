from vaultghost import signature_checks

def test_raw_rs_signature_rejection():
    valid, reason, gen_req = signature_checks.validate({"signature": "0" * 128})
    assert valid is False
    assert reason == "RAW_RS_SIGNATURE"
    assert gen_req is False

def test_double_hash_generator_required():
    valid, reason, gen_req = signature_checks.validate({}, expected_generator_required=True)
    assert valid is False
    assert reason == "DOUBLE_HASH_GENERATOR_REQUIRED"
    assert gen_req is True
