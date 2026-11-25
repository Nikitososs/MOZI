"""Учебная атака на RSA с групповой пробной факторизацией."""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd, isqrt, prod

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
    factorization_trace: tuple[str, ...]


def factor_modulus(n: int, trace: list[str] | None = None) -> tuple[int, int, int]:
    """Найти два различных простых множителя RSA-модуля и число проверок НОД."""
    if n < 4:
        raise ValueError("Модуль n должен быть не меньше 4.")

    factors, gcd_checks = factor_by_prime_triplets(n, trace)
    if len(factors) == 1:
        raise ValueError(f"Не удалось факторизовать n={n}: число простое.")
    if len(factors) != 2:
        raise ValueError("n должно раскладываться на два простых множителя.")
    factor, quotient = factors
    if factor == quotient:
        raise ValueError("Множители RSA-модуля должны быть различными простыми числами.")
    return factor, quotient, gcd_checks


def factor_by_prime_triplets(
    n: int, trace: list[str] | None = None
) -> tuple[list[int], int]:
    """Разложить n по тройкам простых чисел с помощью gcd.

    Степени двойки сначала выделяются двоичным сдвигом. Для нечётного
    остатка последовательно строятся группы (3, 5, 7), (11, 13, 17), ...;
    Кандидаты отбираются решетом Эратосфена. НОД остатка с произведением
    группы находит содержащиеся в ней делители;
    деление повторяется с той же группой до получения НОД, равного 1.
    Возвращаются простые множители с кратностями и число вычислений НОД.
    """
    if n < 2:
        raise ValueError("Для факторизации требуется n ≥ 2.")

    if trace is not None:
        trace.append(f"Начальное число: n = {n}.")
    remaining = n
    factors: list[int] = []
    while remaining & 1 == 0:
        factors.append(2)
        if trace is not None:
            trace.append(f"Остаток чётный: выделен множитель 2; {remaining} >> 1.")
        remaining >>= 1

    gcd_checks = 0
    if trace is not None:
        trace.append(f"После выделения двоек остаток: {remaining}.")
    if remaining == 1:
        if trace is not None:
            trace.append("Остаток равен 1; факторизация завершена.")
        return factors, gcd_checks
    limit = isqrt(remaining)
    sieve_primes = primes_up_to(limit)
    sieve_prime_set = set(sieve_primes)
    if _is_prime_from_sieve_primes(remaining, sieve_primes):
        factors.append(remaining)
        if trace is not None:
            trace.append(f"Остаток {remaining} простое; добавлен последний множитель.")
        return factors, gcd_checks
    if trace is not None:
        trace.append(f"Остаток {remaining} составной; начинаем перебор троек простых.")

    candidate = 3
    while remaining > 1 and candidate <= limit:
        triplet: list[int] = []
        while len(triplet) < 3 and candidate <= limit:
            candidate_is_prime = candidate in sieve_prime_set
            if trace is not None:
                verdict = "простое, добавлено в тройку" if candidate_is_prime else "составное, пропущено"
                trace.append(f"Проверка кандидата {candidate}: {verdict}.")
            if candidate_is_prime:
                triplet.append(candidate)
            candidate += 2

        if not triplet:
            break
        group_product = prod(triplet)
        if trace is not None:
            trace.append(
                f"Сформирована тройка {tuple(triplet)}; произведение q = {group_product}."
            )
        while True:
            before = remaining
            common_divisor = gcd(before, group_product)
            gcd_checks += 1
            if trace is not None:
                trace.append(f"НОД({before}, {group_product}) = {common_divisor}.")
            if common_divisor == 1:
                if trace is not None:
                    trace.append("Общих делителей в этой тройке больше нет; переходим к следующей.")
                break

            remaining //= common_divisor
            found_factors: list[int] = []
            for prime in triplet:
                if common_divisor % prime == 0:
                    factors.append(prime)
                    found_factors.append(prime)
                    common_divisor //= prime
            if common_divisor != 1:
                raise ArithmeticError("НОД содержит делитель вне проверяемой тройки простых чисел.")
            if trace is not None:
                trace.append(
                    f"Делим {before} на найденный НОД: получаем {remaining}; "
                    f"добавлены множители {found_factors}."
                )

            if remaining > 1 and _is_prime_from_sieve_primes(remaining, sieve_primes):
                factors.append(remaining)
                if trace is not None:
                    trace.append(f"Остаток {remaining} простое; факторизация завершена.")
                return sorted(factors), gcd_checks

        if remaining > 1 and _is_prime_from_sieve_primes(remaining, sieve_primes):
            factors.append(remaining)
            if trace is not None:
                trace.append(f"Остаток {remaining} простое; факторизация завершена.")
            return sorted(factors), gcd_checks

    if remaining > 1:
        if _is_prime_from_sieve_primes(remaining, sieve_primes):
            factors.append(remaining)
        else:
            raise ArithmeticError("Не удалось выделить составной остаток проверенными простыми числами.")
    if trace is not None:
        trace.append("Факторизация завершена; все простые множители найдены.")
    return sorted(factors), gcd_checks


def is_prime(number: int) -> bool:
    """Проверить простоту делением на простые числа из решета до sqrt(number)."""
    if number < 2:
        return False
    return _is_prime_from_sieve_primes(number, primes_up_to(isqrt(number)))


def _is_prime_from_sieve_primes(number: int, primes: list[int]) -> bool:
    """Проверить число делителями из готового списка простых до его корня."""
    if number < 2:
        return False
    for prime in primes:
        if prime * prime > number:
            break
        if number % prime == 0:
            return number == prime
    return True


def primes_up_to(limit: int) -> list[int]:
    """Вернуть все простые числа до limit решетом Эратосфена."""
    if limit < 2:
        return []

    sieve = [True] * (limit + 1)
    sieve[0] = False
    if limit >= 1:
        sieve[1] = False
    for candidate in range(2, isqrt(limit) + 1):
        if sieve[candidate]:
            first_composite = candidate * candidate
            for multiple in range(first_composite, limit + 1, candidate):
                sieve[multiple] = False
    return [number for number, is_prime_candidate in enumerate(sieve) if is_prime_candidate]


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

    factorization_trace: list[str] = []
    p, q, gcd_checks = factor_modulus(n, factorization_trace)
    phi = (p - 1) * (q - 1)
    if e >= phi:
        raise ValueError(f"Открытый показатель e должен быть меньше φ(n)={phi}.")
    d = modular_inverse(e, phi)
    plaintext = modular_power(ciphertext, d, n)
    if modular_power(plaintext, e, n) != ciphertext:
        raise ValueError("Проверка шифрования не пройдена: проверьте исходные данные.")

    return AttackResult(
        variant,
        e,
        n,
        ciphertext,
        p,
        q,
        phi,
        d,
        plaintext,
        gcd_checks,
        tuple(factorization_trace),
    )


def attack_variant(variant: Variant) -> AttackResult:
    """Выполнить атаку для открытого ключа и шифротекста из таблицы вариантов."""
    return attack_rsa(variant.e, variant.n, variant.ciphertext, variant.number)
