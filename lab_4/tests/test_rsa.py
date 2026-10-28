import math

import pytest

from lab_4.rsa import (
    KeyPair,
    decrypt_text,
    encode_text,
    encrypt_text,
    extended_gcd,
    generate_key_pairs,
    is_prime,
    mod_inverse,
    modular_power,
    split_plaintext_blocks,
)


@pytest.mark.parametrize("a,b", [(240, 46), (-35, 15), (0, 17), (17, 0), (0, 0)])
def test_extended_gcd_bezout_identity(a, b):
    divisor, x, y = extended_gcd(a, b)
    assert divisor == math.gcd(a, b)
    assert a * x + b * y == divisor


@pytest.mark.parametrize("base,exponent,modulus", [
    (2, 0, 7), (2, 10, 1000), (51936, 65537, 51937), (-9, 13, 101),
])
def test_binary_modular_power_matches_builtin(base, exponent, modulus):
    assert modular_power(base, exponent, modulus) == pow(base, exponent, modulus)


def test_modular_power_rejects_invalid_arguments():
    with pytest.raises(ValueError):
        modular_power(2, -1, 7)
    with pytest.raises(ValueError):
        modular_power(2, 3, 0)


def test_mod_inverse_and_noninvertible_value():
    assert mod_inverse(3, 40) == 27
    with pytest.raises(ValueError, match="НОД"):
        mod_inverse(6, 40)


@pytest.mark.parametrize("number,expected", [(2, True), (311, True), (1, False), (221, False), (167 * 311, False)])
def test_is_prime(number, expected):
    assert is_prime(number) is expected


def test_variant_16_forms_at_least_three_distinct_key_pairs():
    pairs = generate_key_pairs(167, 311)
    assert len(pairs) >= 3
    assert len({pair.e for pair in pairs}) == len(pairs)
    assert all(pair.n == 167 * 311 for pair in pairs)
    assert all(math.gcd(pair.e, pair.phi) == 1 for pair in pairs)
    assert all((pair.e * pair.d) % pair.phi == 1 for pair in pairs)


def test_custom_prime_pair_can_generate_keys_and_encrypt_text():
    key = generate_key_pairs(11, 13)[0]
    result = encrypt_text("АБ В", key)
    assert key.n == 143
    assert decrypt_text(result.ciphertext, key) == "АБ В"


@pytest.mark.parametrize("p,q", [(4, 7), (167, 167), (7, 11)])
def test_invalid_rsa_primes_or_too_small_modulus(p, q):
    with pytest.raises(ValueError):
        generate_key_pairs(p, q)


def test_text_encoding_matches_manual_example_and_drops_unsupported_symbols():
    normalized, digits = encode_text("Вася молодец! ёж")
    assert normalized == "ВАСЯ МОЛОДЕЦ ЕЖ"
    assert digits == "121027419922242124141532991516"


def test_blocks_match_manual_example_and_are_less_than_modulus():
    blocks = split_plaintext_blocks("121027419922242124141532", 22213)
    assert blocks == [12102, 7419, 9222, 4212, 4141, 532]
    assert all(block < 22213 for block in blocks)
    assert split_plaintext_blocks("121027", 51937) == [12102, 7]


def test_block_boundary_moves_left_when_the_next_block_would_start_with_zero():
    # The greedy boundary falls before 0; move it left so the next block starts at 1.
    blocks = split_plaintext_blocks("1210271011", 120)
    assert blocks == [12, 102, 7, 101, 1]
    assert all(block < 120 for block in blocks)
    assert all(not str(block).startswith("0") for block in blocks)


@pytest.mark.parametrize("key_index", [0, 1, 2])
def test_rsa_encrypt_decrypt_round_trip_for_variant_16(key_index):
    key = generate_key_pairs(167, 311)[key_index]
    result = encrypt_text("Вася молодец!\nЁЖ", key)
    assert result.plaintext == "ВАСЯ МОЛОДЕЦ ЕЖ"
    assert all(block < key.n for block in result.plaintext_blocks)
    assert all(block < key.n for block in result.ciphertext_blocks)
    assert len(result.ciphertext) == len(result.ciphertext_blocks) * len(str(key.n))
    assert decrypt_text(result.ciphertext, key) == result.plaintext


def test_encrypt_requires_nonempty_supported_text():
    with pytest.raises(ValueError, match="не осталось"):
        encrypt_text("123!?", generate_key_pairs(167, 311)[0])


def test_decrypt_validates_stream_and_blocks():
    key = KeyPair(e=3, d=27, n=55, phi=40)  # not a text-compatible key, for input checks only
    with pytest.raises(ValueError, match="кратна"):
        decrypt_text("123", key)
    with pytest.raises(ValueError, match="только цифры"):
        decrypt_text("ab55", key)
    with pytest.raises(ValueError, match="меньше n"):
        decrypt_text("5555", key)
