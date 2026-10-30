import math

import pytest

from lab_5.rsa_attack import (
    attack_rsa,
    attack_variant,
    extended_gcd,
    factor_modulus,
    modular_inverse,
    modular_power,
)
from lab_5.variants import VARIANTS


def test_pollard_rho_factors_variant_16_modulus():
    p, q, iterations = factor_modulus(56549)
    assert (p, q) == (193, 293)
    assert iterations > 0


def test_pollard_rho_rejects_prime_modulus():
    with pytest.raises(ValueError, match="число простое"):
        factor_modulus(101)


@pytest.mark.parametrize("number", [0, 1, 2, 3, 4, 9, 25, 97])
def test_factor_modulus_rejects_values_without_two_prime_factors(number):
    with pytest.raises(ValueError):
        factor_modulus(number)


def test_extended_gcd_returns_bezout_coefficients():
    divisor, x, y = extended_gcd(251, 56064)
    assert divisor == math.gcd(251, 56064) == 1
    assert 251 * x + 56064 * y == divisor


def test_modular_inverse_rejects_non_coprime_values():
    with pytest.raises(ValueError, match="НОД"):
        modular_inverse(6, 40)


@pytest.mark.parametrize("base,exponent,modulus", [(3, 0, 11), (7, 123, 97), (20844, 38195, 56549)])
def test_binary_modular_power_matches_builtin(base, exponent, modulus):
    assert modular_power(base, exponent, modulus) == pow(base, exponent, modulus)


def test_variant_16_recovers_the_private_key_and_plaintext():
    result = attack_variant(VARIANTS[16])
    assert (result.p, result.q) == (193, 293)
    assert result.phi == 56064
    assert result.d == 38195
    assert result.plaintext == 2316
    assert modular_power(result.plaintext, result.e, result.n) == result.ciphertext


@pytest.mark.parametrize("variant_number", sorted(VARIANTS))
def test_all_methodical_variants_factor_and_decrypt(variant_number):
    result = attack_variant(VARIANTS[variant_number])
    assert result.p * result.q == result.n
    assert modular_power(result.plaintext, result.e, result.n) == result.ciphertext


def test_attack_rejects_ciphertext_outside_residue_range():
    with pytest.raises(ValueError, match="C < n"):
        attack_rsa(251, 56549, 56549)


def test_attack_rejects_public_exponent_outside_valid_range():
    with pytest.raises(ValueError, match="больше 1"):
        attack_rsa(1, 55, 23)
    with pytest.raises(ValueError, match="меньше φ"):
        attack_rsa(40, 55, 23)
