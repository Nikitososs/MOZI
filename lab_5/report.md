{{json
{
  "discipline": "Математические основы защиты информации",
  "title": "Криптоанализ шифра RSA факторизацией модуля",
  "student": {"name": "Смирнов Никита Михайлович", "course": "2", "group": "ФИТ-242", "program": "02.03.02 Фундаментальная информатика и информационные технологии"},
  "teacher": {"title": "канд. пед. наук, доцент", "name": "Белим Светлана Юрьевна"},
  "institution": {"short": "ОмГТУ", "department": "ПМиФИ", "year": "2026"},
  "work": {"type": "Лабораторная работа № 5", "variant": "16"}
}
}}

# СОДЕРЖАНИЕ

# ВВЕДЕНИЕ

Цель лабораторной работы — исследовать уязвимость учебной системы RSA при факторизации её открытого модуля. Если модуль $n$ разложен на множители $p$ и $q$, можно вычислить функцию Эйлера, восстановить закрытый показатель и расшифровать сообщение.

Программа реализует пробное деление, расширенный алгоритм Евклида и бинарное возведение в степень. Она решает вариант 16 из методички, позволяет выбрать любой из 30 вариантов таблицы, принимает произвольные открытые данные RSA и содержит отдельное меню проверки математических операций.

# ОСНОВНАЯ ЧАСТЬ

## 1 Теоретические сведения

Открытый ключ RSA состоит из показателя $e$ и модуля $n$. При создании ключа модуль задаётся произведением двух различных простых чисел:

$$
n=pq.
$$

Зная разложение модуля, вычисляют функцию Эйлера:

$$
\varphi(n)=(p-1)(q-1).
$$

Закрытый показатель $d$ является обратным к $e$ по модулю $\varphi(n)$:

$$
d=e^{-1}\bmod\varphi(n), \qquad ed\equiv1\pmod{\varphi(n)}.
$$

После этого шифротекст $C$ расшифровывается по формуле:

$$
M=C^d\bmod n.
$$

Пробное деление последовательно проверяет целые делители от 2 до $\lfloor\sqrt n\rfloor$. Если найден делитель $p$, второй множитель равен $q=n/p$. Достаточно проверять числа до квадратного корня: у составного числа обязательно есть делитель, не превосходящий его квадратного корня. Для больших RSA-модулей этот метод непрактичен, но позволяет исследовать принцип атаки на небольших учебных числах.

## 2 Алгоритм программы

1. Получить открытый ключ $(e,n)$ и шифротекст $C$ — из таблицы варианта или из пользовательского ввода.
2. Последовательно проверять делители $2,3,\ldots,\lfloor\sqrt n\rfloor$, пока не найдётся множитель $p$.
3. Вычислить $q=n/p$ и проверить, что множители различны и просты.
4. Вычислить $\varphi(n)=(p-1)(q-1)$.
5. Расширенным алгоритмом Евклида найти коэффициенты $x,y$, для которых $ex+\varphi(n)y=1$. Тогда $d=x\bmod\varphi(n)$.
6. Вычислить $M=C^d\bmod n$ бинарным возведением в степень.
7. Проверить результат повторным шифрованием: $M^e\bmod n=C$.

В меню проверки математики доступны расширенный алгоритм Евклида, поиск обратного элемента, бинарное возведение в степень и факторизация модуля. В режиме произвольных данных можно задать $e$, $n$ и $C$; программа проверяет корректность диапазона шифротекста и пригодность найденных множителей для RSA.

## 3 Результаты варианта 16

По таблице 5 методички для варианта 16 заданы открытый ключ $(e,n)=(251,56549)$ и шифротекст $C=20844$.

Пробное деление обнаруживает делитель $193$. Второй множитель:

$$
q=\frac{56549}{193}=293.
$$

Итак, $n=193\cdot293$. Проверки показывают, что оба множителя простые и различны. При проверке делителей от 2 до 193 включительно выполнено 192 проверки делимости.

Таблица: Восстановление закрытого ключа и исходного блока

| Параметр | Вычисление | Результат |
|:--|:--|--:|
| $n$ | Открытый модуль | 56549 |
| $p,q$ | Факторизация $n$ | 193, 293 |
| $\varphi(n)$ | $(193-1)(293-1)$ | 56064 |
| $e$ | Открытый показатель | 251 |
| $d$ | $251^{-1}\bmod56064$ | 38195 |
| $C$ | Заданный шифротекст | 20844 |
| $M$ | $20844^{38195}\bmod56549$ | 2316 |

Проверка пары показателей:

$$
251\cdot38195=9596945=171\cdot56064+1,
$$

следовательно, $ed\bmod\varphi(n)=1$. Проверка расшифрования повторным шифрованием даёт:

$$
2316^{251}\bmod56549=20844=C.
$$

По формату таблицы методички сообщение представлено одним числовым блоком, поэтому результат расшифрования приводится как число $M=2316$.

## 4 Проверка программы

Тесты проверяют факторизацию варианта 16 и всех записей таблицы 5, тождество Безу, обратный элемент, бинарную степень, валидацию недопустимых параметров, произвольный ввод $(e,n,C)$, пункт факторизации в математическом меню и сохранение результата варианта. Для каждого табличного варианта повторное шифрование восстановленного блока совпадает с исходным шифротекстом.

## 5 Контрольные вопросы

1. **Как факторизация позволяет взломать RSA?** Из множителей $p$ и $q$ вычисляется $\varphi(n)$; зная её и открытый показатель $e$, можно найти закрытый показатель $d$ и расшифровать сообщение.
2. **Как вычислить закрытый ключ по открытому?** Найти $d=e^{-1}\bmod\varphi(n)$ расширенным алгоритмом Евклида. Для этого сначала требуется знать $\varphi(n)$, а значит, факторизовать $n$.
3. **Как факторизовать небольшие числа и сколько нужно шагов?** Проверять делители от 2 до $\lfloor\sqrt n\rfloor$. В худшем случае нужно проверить порядка $\sqrt n$ кандидатов; для варианта 16 найден делитель 193 после 192 проверок.

# ЗАКЛЮЧЕНИЕ

Реализована программа для демонстрации атаки на RSA посредством факторизации модуля. Для варианта 16 найдено разложение $56549=193\cdot293$, вычислено $\varphi(n)=56064$, восстановлен закрытый показатель $d=38195$ и получен исходный блок $M=2316$. Повторное шифрование подтвердило результат. Программа также поддерживает все табличные варианты, произвольные открытые данные и отдельную проверку математических алгоритмов.

# СПИСОК ЛИТЕРАТУРЫ

1. Математические основы защиты информации : методические указания к лабораторным работам / Минобрнауки России, Омский государственный технический университет ; составители С. Ю. Белим, С. В. Белим. — Омск : Издательство ОмГТУ, 2023. — С. 36–38, приложение 5.

# ПРИЛОЖЕНИЯ

## Код программы


Листинг: Модуль факторизации и восстановления ключа (lab_5/rsa_attack.py)

```python
"""Учебная атака на RSA через пробное деление модуля."""

from __future__ import annotations

from dataclasses import dataclass
from math import isqrt

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
    division_checks: int


def factor_modulus(n: int) -> tuple[int, int, int]:
    """Найти простые множители n пробным делением и вернуть (p, q, число проверок)."""
    if n < 4:
        raise ValueError("Модуль n должен быть не меньше 4.")

    checks = 0
    for divisor in range(2, isqrt(n) + 1):
        checks += 1
        if n % divisor == 0:
            quotient = n // divisor
            if not is_prime(divisor) or not is_prime(quotient):
                raise ValueError("n должно раскладываться на два простых множителя.")
            if divisor == quotient:
                raise ValueError("Множители RSA-модуля должны быть различными простыми числами.")
            return divisor, quotient, checks

    raise ValueError(f"Не удалось факторизовать n={n}: число простое.")


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

    p, q, checks = factor_modulus(n)
    phi = (p - 1) * (q - 1)
    if e >= phi:
        raise ValueError(f"Открытый показатель e должен быть меньше φ(n)={phi}.")
    d = modular_inverse(e, phi)
    plaintext = modular_power(ciphertext, d, n)
    if modular_power(plaintext, e, n) != ciphertext:
        raise ValueError("Проверка шифрования не пройдена: проверьте исходные данные.")

    return AttackResult(variant, e, n, ciphertext, p, q, phi, d, plaintext, checks)


def attack_variant(variant: Variant) -> AttackResult:
    """Выполнить атаку для открытого ключа и шифротекста из таблицы вариантов."""
    return attack_rsa(variant.e, variant.n, variant.ciphertext, variant.number)
```

Листинг: Таблица открытых данных (lab_5/variants.py)

```python
"""Открытые ключи и шифротексты из таблицы 5 методических указаний."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Variant:
    number: int
    e: int
    n: int
    ciphertext: int


VARIANTS = {
    1: Variant(1, 131, 21733, 258),
    2: Variant(2, 137, 25199, 19155),
    3: Variant(3, 59, 28829, 16357),
    4: Variant(4, 59, 29999, 21959),
    5: Variant(5, 259, 31921, 28368),
    6: Variant(6, 251, 33221, 25619),
    7: Variant(7, 251, 35909, 28498),
    8: Variant(8, 251, 37901, 238),
    9: Variant(9, 251, 40349, 39620),
    10: Variant(10, 251, 42869, 9491),
    11: Variant(11, 251, 44923, 14134),
    12: Variant(12, 251, 46883, 12351),
    13: Variant(13, 251, 49583, 38076),
    14: Variant(14, 251, 50861, 8261),
    15: Variant(15, 251, 54053, 13047),
    16: Variant(16, 251, 56549, 20844),
    17: Variant(17, 251, 60479, 27990),
    18: Variant(18, 251, 61889, 23824),
    19: Variant(19, 251, 66043, 23262),
    20: Variant(20, 251, 70691, 18291),
    21: Variant(21, 251, 75137, 25028),
    22: Variant(22, 251, 77173, 37325),
    23: Variant(23, 251, 80851, 23313),
    24: Variant(24, 251, 83411, 59021),
    25: Variant(25, 251, 85073, 81019),
    26: Variant(26, 59, 28141, 9148),
    27: Variant(27, 59, 80057, 56943),
    28: Variant(28, 59, 113803, 28184),
    29: Variant(29, 59, 57377, 2948),
    30: Variant(30, 59, 70691, 41370),
}
```

Листинг: Интерфейс и математическое меню (lab_5/main.py)

```python
"""Интерфейс лабораторной работы № 5: факторизация учебного RSA."""

from __future__ import annotations

from pathlib import Path

from lab_5.rsa_attack import (
    AttackResult,
    attack_rsa,
    attack_variant,
    extended_gcd,
    factor_modulus,
    modular_inverse,
    modular_power,
)
from lab_5.variants import VARIANTS

OUTPUT_DIR = Path(__file__).resolve().parent / "outputs"
DEFAULT_VARIANT = 16


def read_integer(prompt: str, default: int | None = None) -> int | None:
    hint = f" [{default}]" if default is not None else ""
    raw = input(f"{prompt}{hint} (q — назад): ").strip()
    if raw.lower() == "q":
        return None
    if not raw and default is not None:
        return default
    try:
        return int(raw)
    except ValueError:
        print("Ошибка: введите целое число.")
        return None


def read_variant(prompt: str, default: int | None = None) -> int | None:
    number = read_integer(prompt, default)
    if number is None:
        return None
    if number not in VARIANTS:
        print("Ошибка: в таблице методички есть варианты от 1 до 30.")
        return None
    return number


def format_result(result: AttackResult) -> str:
    variant_label = f"Вариант: {result.variant}\n" if result.variant is not None else ""
    return (
        "Лабораторная работа № 5 — криптоанализ RSA факторизацией модуля\n"
        f"{variant_label}"
        f"Открытый ключ (e, n): ({result.e}, {result.n})\n"
        f"Факторизация n: p={result.p}, q={result.q}; проверок делителей: {result.division_checks}\n"
        f"φ(n) = (p−1)(q−1) = {result.phi}\n"
        f"Закрытый показатель: d={result.d}\n"
        f"Шифротекст: C={result.ciphertext}\n"
        f"Открытый текст: M={result.plaintext}\n"
        f"Проверка: M^e mod n = {result.ciphertext}\n"
    )


def save_result(result: AttackResult) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    variant_number = result.variant if result.variant is not None else "custom"
    path = OUTPUT_DIR / f"variant_{variant_number}_solution.txt"
    path.write_text(format_result(result), encoding="utf-8")
    return path


def run_variant(variant_number: int) -> None:
    try:
        result = attack_variant(VARIANTS[variant_number])
    except ValueError as error:
        print(f"Ошибка выполнения атаки: {error}")
        return
    print("\n" + format_result(result), end="")
    print(f"Результат сохранён: {save_result(result)}")


def run_custom_attack() -> None:
    print("\nВВОД ОТКРЫТЫХ ДАННЫХ RSA")
    e = read_integer("Открытый показатель e")
    n = read_integer("Модуль n") if e is not None else None
    ciphertext = read_integer("Шифротекст C") if n is not None else None
    if e is None or n is None or ciphertext is None:
        return
    try:
        result = attack_rsa(e, n, ciphertext)
    except ValueError as error:
        print(f"Ошибка выполнения атаки: {error}")
        return
    print("\n" + format_result(result), end="")
    print(f"Результат сохранён: {save_result(result)}")


def math_check_menu() -> None:
    while True:
        print("\nПРОВЕРКА МАТЕМАТИКИ")
        print("1. Расширенный алгоритм Евклида")
        print("2. Обратный элемент по модулю")
        print("3. Бинарное возведение в степень по модулю")
        print("4. Факторизация n пробным делением")
        print("0. Назад")
        choice = input("Выберите действие: ").strip()
        if choice == "0":
            return
        try:
            if choice == "1":
                a = read_integer("Введите a")
                b = read_integer("Введите b") if a is not None else None
                if a is None or b is None:
                    continue
                divisor, x, y = extended_gcd(a, b)
                print(f"НОД({a}, {b}) = {divisor}; коэффициенты Безу: x={x}, y={y}.")
                print(f"Проверка: {a}·{x} + {b}·{y} = {a * x + b * y}.")
            elif choice == "2":
                value = read_integer("Введите число a")
                modulus = read_integer("Введите модуль m") if value is not None else None
                if value is None or modulus is None:
                    continue
                inverse = modular_inverse(value, modulus)
                print(f"Обратный элемент: {value}^(-1) mod {modulus} = {inverse}.")
                print(f"Проверка: {value}·{inverse} mod {modulus} = {value * inverse % modulus}.")
            elif choice == "3":
                base = read_integer("Введите основание a")
                exponent = read_integer("Введите показатель k") if base is not None else None
                modulus = read_integer("Введите модуль n") if exponent is not None else None
                if base is None or exponent is None or modulus is None:
                    continue
                print(
                    f"{base}^{exponent} mod {modulus} = {modular_power(base, exponent, modulus)}."
                )
            elif choice == "4":
                n = read_integer("Введите модуль n")
                if n is None:
                    continue
                p, q, checks = factor_modulus(n)
                print(f"Факторизация: n = p·q = {p}·{q} = {p * q}.")
                print(f"Проверено делителей: {checks}.")
            else:
                print("Выберите 1, 2, 3, 4 или 0.")
        except ValueError as error:
            print(f"Ошибка вычисления: {error}")


def main() -> None:
    while True:
        print("\n" + "=" * 65)
        print("ЛАБОРАТОРНАЯ РАБОТА № 5 — КРИПТОАНАЛИЗ ШИФРА RSA")
        print("1. Выполнить свой вариант (вариант 16 по умолчанию)")
        print("2. Выбрать вариант из таблицы методички")
        print("3. Ввести произвольные e, n и C")
        print("4. Проверка математики")
        print("5. Выход")
        choice = input("Выберите пункт меню: ").strip()
        if choice == "1":
            run_variant(DEFAULT_VARIANT)
        elif choice == "2":
            variant_number = read_variant("Введите номер варианта", DEFAULT_VARIANT)
            if variant_number is not None:
                run_variant(variant_number)
        elif choice == "3":
            run_custom_attack()
        elif choice == "4":
            math_check_menu()
        elif choice == "5":
            print("Работа завершена.")
            return
        else:
            print("Выберите 1, 2, 3, 4 или 5.")


if __name__ == "__main__":
    main()
```
