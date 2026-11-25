"""Учебная атака на RSA с групповой пробной факторизацией."""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd, isqrt

from lab_5.variants import Variant


@dataclass(frozen=True)
class AttackResult:
    variant: int | None
    e: int
    n: int
    ciphertext: int
    p: int
    q: int
    phi: int
    d: int
    plaintext: int
    factorization_checks: int


def factor_modulus(n: int) -> tuple[int, int, int]:
    """Найти два различных простых множителя RSA-модуля и число проверок НОД."""
    if n < 4:
        raise ValueError("Модуль n должен быть не меньше 4.")

    if is_prime(n):
        raise ValueError(f"Не удалось факторизовать n={n}: число простое.")

    factors, gcd_checks = factor_by_prime_triplets(n)
    if len(factors) != 2:
        raise ValueError("n должно раскладываться на два простых множителя.")
    factor, quotient = factors
    if factor == quotient:
        raise ValueError("Множители RSA-модуля должны быть различными простыми числами.")
    return factor, quotient, gcd_checks


def factor_by_prime_triplets(n: int) -> tuple[list[int], int]:
    """Разложить n по тройкам простых чисел с помощью gcd.

    Степени двойки сначала выделяются двоичным сдвигом. Для нечётного
    остатка последовательно строятся группы (3, 5, 7), (11, 13, 17), ...;
    НОД остатка с произведением группы находит содержащиеся в ней делители;
    деление повторяется с той же группой до получения НОД, равного 1.
    Возвращаются простые множители с кратностями и число вычислений НОД.
    """
    if n < 2:
        raise ValueError("Для факторизации требуется n ≥ 2.")

    remaining = n
    factors: list[int] = []
    while remaining & 1 == 0:
        factors.append(2)
        remaining >>= 1

    gcd_checks = 0
    if remaining == 1:
        return factors, gcd_checks
    if is_prime(remaining):
        factors.append(remaining)
        return factors, gcd_checks

    candidate = 3
    while remaining > 1:
        triplet: list[int] = []
        while len(triplet) < 3:
            if is_prime(candidate):
                triplet.append(candidate)
            candidate += 2

        group_product = triplet[0] * triplet[1] * triplet[2]
        while True:
            common_divisor = gcd(remaining, group_product)
            gcd_checks += 1
            if common_divisor == 1:
                break

            remaining //= common_divisor
            for prime in triplet:
                if common_divisor % prime == 0:
                    factors.append(prime)
                    common_divisor //= prime
            if common_divisor != 1:
                raise ArithmeticError("НОД содержит делитель вне проверяемой тройки простых чисел.")

            if remaining > 1 and is_prime(remaining):
                factors.append(remaining)
                return sorted(factors), gcd_checks

    return sorted(factors), gcd_checks


def is_prime(number: int) -> bool:
    """Проверить простоту пробным делением до квадратного корня."""
    if number < 2:
        return False
    if number == 2:
        return True
    if number % 2 == 0:
        return False
    return all(number % divisor for divisor in range(3, isqrt(number) + 1, 2))


def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    """Вернуть (g, x, y), такие что ax + by = g = НОД(a, b)."""
    old_r, r = a, b
    old_x, x = 1, 0
    old_y, y = 0, 1
    while r:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_x, x = x, old_x - quotient * x
        old_y, y = y, old_y - quotient * y
    if old_r < 0:
        return -old_r, -old_x, -old_y
    return old_r, old_x, old_y


def modular_inverse(value: int, modulus: int) -> int:
    """Найти обратный элемент value modulo modulus расширенным алгоритмом Евклида."""
    if modulus <= 1:
        raise ValueError("Модуль для обратного элемента должен быть больше 1.")
    divisor, coefficient, _ = extended_gcd(value, modulus)
    if divisor != 1:
        raise ValueError(f"Обратный элемент не существует: НОД({value}, {modulus}) = {divisor}.")
    return coefficient % modulus


def modular_power(base: int, exponent: int, modulus: int) -> int:
    """Вычислить base**exponent mod modulus бинарным возведением в степень."""
    if exponent < 0:
        raise ValueError("Показатель степени не может быть отрицательным.")
    if modulus <= 0:
        raise ValueError("Модуль должен быть положительным.")

    result = 1 % modulus
    factor = base % modulus
    power = exponent
    while power:
        if power & 1:
            result = result * factor % modulus
        factor = factor * factor % modulus
        power >>= 1
    return result


def attack_rsa(e: int, n: int, ciphertext: int, variant: int | None = None) -> AttackResult:
    """Факторизовать n, восстановить d и расшифровать один блок ciphertext."""
    if e <= 1:
        raise ValueError("Открытый показатель e должен быть больше 1.")
    if not 0 <= ciphertext < n:
        raise ValueError("Шифротекст C должен удовлетворять условию 0 ≤ C < n.")

    p, q, gcd_checks = factor_modulus(n)
    phi = (p - 1) * (q - 1)
    if e >= phi:
        raise ValueError(f"Открытый показатель e должен быть меньше φ(n)={phi}.")
    d = modular_inverse(e, phi)
    plaintext = modular_power(ciphertext, d, n)
    if modular_power(plaintext, e, n) != ciphertext:
        raise ValueError("Проверка шифрования не пройдена: проверьте исходные данные.")

    return AttackResult(variant, e, n, ciphertext, p, q, phi, d, plaintext, gcd_checks)


def attack_variant(variant: Variant) -> AttackResult:
    """Выполнить атаку для открытого ключа и шифротекста из таблицы вариантов."""
    return attack_rsa(variant.e, variant.n, variant.ciphertext, variant.number)
