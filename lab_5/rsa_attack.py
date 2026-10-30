"""Учебная атака на RSA с факторизацией модуля методом Полларда rho."""

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
    factorization_iterations: int


def factor_modulus(n: int) -> tuple[int, int, int]:
    """Найти простые множители n методом Полларда rho и число итераций."""
    if n < 4:
        raise ValueError("Модуль n должен быть не меньше 4.")

    if is_prime(n):
        raise ValueError(f"Не удалось факторизовать n={n}: число простое.")

    factor, iterations = pollard_rho_factor(n)
    quotient = n // factor
    if not is_prime(factor) or not is_prime(quotient):
        raise ValueError("n должно раскладываться на два простых множителя.")
    if factor == quotient:
        raise ValueError("Множители RSA-модуля должны быть различными простыми числами.")
    return min(factor, quotient), max(factor, quotient), iterations


def pollard_rho_factor(n: int) -> tuple[int, int]:
    """Найти нетривиальный делитель n циклическим методом Полларда rho."""
    if n % 2 == 0:
        return 2, 1
    if n % 3 == 0:
        return 3, 1

    total_iterations = 0
    constant = 1
    while True:
        x = y = 2
        divisor = 1
        while divisor == 1:
            x = (x * x + constant) % n
            y = (y * y + constant) % n
            y = (y * y + constant) % n
            divisor = gcd(abs(x - y), n)
            total_iterations += 1
        if divisor != n:
            return divisor, total_iterations
        constant += 1


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

    p, q, iterations = factor_modulus(n)
    phi = (p - 1) * (q - 1)
    if e >= phi:
        raise ValueError(f"Открытый показатель e должен быть меньше φ(n)={phi}.")
    d = modular_inverse(e, phi)
    plaintext = modular_power(ciphertext, d, n)
    if modular_power(plaintext, e, n) != ciphertext:
        raise ValueError("Проверка шифрования не пройдена: проверьте исходные данные.")

    return AttackResult(variant, e, n, ciphertext, p, q, phi, d, plaintext, iterations)


def attack_variant(variant: Variant) -> AttackResult:
    """Выполнить атаку для открытого ключа и шифротекста из таблицы вариантов."""
    return attack_rsa(variant.e, variant.n, variant.ciphertext, variant.number)
