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
        f"Факторизация n: p={result.p}, q={result.q}; итераций rho: {result.factorization_iterations}\n"
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
        print("4. Факторизация n методом Полларда rho")
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
                p, q, iterations = factor_modulus(n)
                print(f"Факторизация: n = p·q = {p}·{q} = {p * q}.")
                print(f"Итераций алгоритма Полларда rho: {iterations}.")
            else:
                print("Выберите 1, 2, 3, 4 или 0.")
        except ValueError as error:
            print(f"Ошибка вычисления: {error}")


def main() -> None:
    while True:
        print("\n" + "=" * 65)
        print("ЛАБОРАТОРНАЯ РАБОТА № 5 — КРИПТОАНАЛИЗ ШИФРА RSA")
        print("1. Решить вариант из таблицы методички (1–30; по умолчанию 16)")
        print("2. Ввести произвольные e, n и C")
        print("3. Проверка математики")
        print("4. Выход")
        choice = input("Выберите пункт меню: ").strip()
        if choice == "1":
            variant_number = read_variant("Введите номер варианта", DEFAULT_VARIANT)
            if variant_number is not None:
                run_variant(variant_number)
        elif choice == "2":
            run_custom_attack()
        elif choice == "3":
            math_check_menu()
        elif choice == "4":
            print("Работа завершена.")
            return
        else:
            print("Выберите 1, 2, 3 или 4.")


if __name__ == "__main__":
    main()
