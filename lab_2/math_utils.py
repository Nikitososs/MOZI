"""
Модуль математического аппарата модулярной арифметики:
- Расширенный алгоритм Евклида (коэффициенты Безу);
- Вычисление мультипликативно обратного элемента в кольце вычетов;
- Решение линейного сравнения вида ax ≡ b (mod m);
- Решение системы линейных сравнений с двумя неизвестными.
"""

import math
from typing import List, Optional, Tuple


def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    """
    Расширенный алгоритм Евклида.

    Вход: a, b
    Выход: (d, u, v), где:
      d = НОД(|a|, |b|)
      u, v — коэффициенты Безу, удовлетворяющие тождеству a * u + b * v = d.
    """
    if b == 0:
        sign = 1 if a >= 0 else -1
        return a * sign, sign, 0

    u0, u1 = 1, 0
    v0, v1 = 0, 1
    r0, r1 = a, b

    while r1 != 0:
        q = r0 // r1
        r0, r1 = r1, r0 - q * r1
        u0, u1 = u1, u0 - q * u1
        v0, v1 = v1, v0 - q * v1

    if r0 < 0:
        r0, u0, v0 = -r0, -u0, -v0

    return r0, u0, v0


def mod_inverse(a: int, m: int) -> Tuple[bool, Optional[int], Optional[int], str]:
    """
    Нахождение мультипликативно обратного элемента к 'a' по модулю 'm'.

    Вход: a, m
    Выход: (is_invertible, bezout_u, pos_inverse, description)
      1. Если НОД(a, m) != 1:
         (False, None, None, "Необратимо: НОД(a, m) = d != 1")
      2. Если НОД(a, m) == 1:
         (True, u, u % m, "Обратимо: коэффициент Безу u, положительное обратное u % m")
    """
    if m <= 0:
        raise ValueError(f"Модуль m должен быть строго положительным (получено m = {m})")

    d, u, _ = extended_gcd(a, m)
    if d != 1:
        return False, None, None, f"Необратимо: НОД({a}, {m}) = {d} ≠ 1"

    pos_inv = u % m
    return True, u, pos_inv, (
        f"Обратимо: коэффициент Безу u = {u}; "
        f"наименьшее неотрицательное обратное = {pos_inv}"
    )


def solve_linear_congruence(a: int, b: int, m: int) -> Tuple[int, List[int], str]:
    """
    Решение линейного сравнения вида:
      a * x ≡ b (mod m)

    Вход: a, b, m
    Выход: (status, solutions, description)
      status:
        1 - Решений нет (если b не делится на d = НОД(a, m))
        2 - Решение одно (если d = 1)
        3 - Несколько решений (если d > 1 и b делится на d, ровно d решений)
    """
    if m <= 0:
        raise ValueError(f"Модуль m должен быть положительным (получено m = {m})")

    d, u, _ = extended_gcd(a, m)
    b_mod = b % m

    if b_mod % d != 0:
        return (
            1,
            [],
            f"1. Решений нет: свободный член b={b} (mod {m}) не делится на НОД(a, m) = {d}"
        )

    # Приводим к эквивалентному сравнению: (a/d) * x ≡ (b/d) (mod m/d)
    m_prime = m // d
    a_prime = (a % m) // d
    b_prime = b_mod // d

    _, u_prime, _ = extended_gcd(a_prime, m_prime)
    x0 = (u_prime * b_prime) % m_prime

    solutions = sorted([(x0 + k * m_prime) % m for k in range(d)])

    if d == 1:
        return (
            2,
            solutions,
            f"2. Решение одно по модулю {m}: x ≡ {solutions[0]} (mod {m})"
        )
    else:
        sols_str = ", ".join(map(str, solutions))
        return (
            3,
            solutions,
            f"3. Несколько решений (всего {d} реш. по модулю {m}): x ∈ {{{sols_str}}}"
        )


def solve_system_congruences(
    a: int,
    b: int,
    c: int,
    d_val: int,
    m: int
) -> Tuple[int, List[Tuple[int, int]], str]:
    """
    Решение системы линейных сравнений вида:
      (a * x + y) ≡ b (mod m)
      (c * x + y) ≡ d_val (mod m)

    В контексте аффинного шифра:
      x играет роль первой части ключа 'a',
      y играет роль второй части ключа 'b'.

    Вычитая второе сравнение из первого, получаем:
      (a - c) * x ≡ (b - d_val) (mod m)

    Вход: a, b, c, d_val, m
    Выход: (status, solutions, description)
      status:
        1 - Решений нет
        2 - Одно решение [(x0, y0)]
        3 - Много решений [(x0, y0), (x1, y1), ...]
    """
    if m <= 0:
        raise ValueError(f"Модуль m должен быть положительным (получено m = {m})")

    diff_coeff = (a - c) % m
    diff_val = (b - d_val) % m

    st, x_solutions, _ = solve_linear_congruence(diff_coeff, diff_val, m)

    if st == 1:
        return (
            1,
            [],
            f"1. Решений нет: разностное сравнение ({a} - {c})x ≡ ({b} - {d_val}) (mod {m}) неразрешимо"
        )

    pairs: List[Tuple[int, int]] = []
    for x in x_solutions:
        y = (b - a * x) % m
        pairs.append((x, y))

    if st == 2:
        x0, y0 = pairs[0]
        gcd_x = math.gcd(x0, m)
        inv_note = " (обратимо, допустимый ключ)" if gcd_x == 1 else f" (необратимо, т.к. НОД(x,m)={gcd_x})"
        return (
            2,
            pairs,
            f"2. Одно решение: x={x0}{inv_note}, y={y0}"
        )
    else:
        pairs_str = ", ".join(f"(x={x}, y={y})" for x, y in pairs)
        return (
            3,
            pairs,
            f"3. Много решений (всего {len(pairs)} пар): {pairs_str}"
        )
