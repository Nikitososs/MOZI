{{json
{
  "discipline": "Математические основы защиты информации",
  "student": {
    "name": "Смирнов Никита Михайлович",
    "course": "2",
    "group": "ФИТ-242",
    "program": "02.03.02 Фундаментальная информатика и информационные технологии"
  },
  "teacher": {
    "title": "канд. пед. наук, доцент",
    "name": "Белим Светлана Юрьевна"
  },
  "institution": {
    "short": "ОмГТУ",
    "full_name": "Омский государственный технический университет",
    "department": "ПМиФИ",
    "city": "Омск",
    "year": "2026"
  },
  "title": "Криптоанализ шифра RSA факторизацией модуля",
  "work": {
    "type": "Лабораторная работа № 5",
    "variant": "16"
  }
}
}}

# СОДЕРЖАНИЕ

# ОСНОВНАЯ ЧАСТЬ

## Результаты криптоанализа варианта 16

Открытый ключ $(e,n)=(251,56549)$, шифротекст $C=20844$. Групповая пробная факторизация выделила $p=193$ и $q=293$ за 15 вычислений НОД для групп простых чисел.

Таблица: Восстановление ключа и открытого блока

| Параметр | Вычисление | Результат |
|:---|:---|---:|
| $n$ | открытый модуль | 56549 |
| $p,q$ | факторизация $n$ | 193, 293 |
| $\varphi(n)$ | $(193-1)(293-1)$ | 56064 |
| $d$ | $e^{-1}\bmod\varphi(n)$ | 38195 |
| $M$ | $C^d\bmod n$ | 2316 |

Проверка обратного показателя: $251\cdot38195=9586945=171\cdot56064+1$, поэтому $ed\bmod\varphi(n)=1$. Повторное шифрование подтверждает результат: $2316^{251}\bmod56549=20844=C$.

Для учебного варианта результат расшифрования — числовой блок $M=2316$. В проверочном примере методички $84\,257\,901$ разложено по группам $q_1=105$, $q_2=2431$, $q_3=12673$: НОД с $q_1$ даёт $21,21,3,3$, затем с $q_2$ — $13$, с $q_3$ — $23$; остаток $71$ прост. Получено $84\,257\,901=3^4\cdot7^2\cdot13\cdot23\cdot71$. Алгоритм предварительно выделяет степени двойки, а НОД с произведением тройки повторяется для текущего остатка до результата 1. Простота исходного и конечного остатка проверяется пробным делением. Реализация находится в `lab_5/rsa_attack.py`; исходные варианты — в `lab_5/variants.py`.


---

## Работа приложения

Запуск: `python -m lab_5.main`. Пункт 1 решает выбранный вариант из таблицы 1–30 (по умолчанию 16); пункт 2 принимает произвольные $e,n,C$; пункт 3 открывает математические проверки, включая расширенный алгоритм Евклида, обратный элемент, бинарное возведение в степень и факторизацию группами простых троек. При факторизации программа удаляет степени двойки, проверяет простоту и затем вычисляет НОД остатка с произведением очередной тройки простых чисел. После атаки выводятся найденные множители, число вычислений НОД, $\varphi(n)$, закрытый показатель, расшифрованный блок и результат повторного шифрования. Расчёт сохраняется в `lab_5/outputs/variant_<номер>_solution.txt`.

# СПИСОК ЛИТЕРАТУРЫ

- Математические основы защиты информации : методические указания к лабораторным работам / Минобрнауки России, Омский государственный технический университет ; составители С. Ю. Белим, С. В. Белим. — Омск : Издательство ОмГТУ, 2023. — С. 36–38, приложение 5. — Текст : электронный.

# ПРИЛОЖЕНИЯ

## Приложение А. Фрагмент исходного кода `rsa_attack.py`

Проверка простоты, факторизация произведениями троек простых чисел, восстановление закрытого показателя и проверка расшифрования.

Листинг: Факторизация RSA-модуля и выполнение атаки

```python
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
```
