"""Интерактивное меню лабораторной работы № 4 по алгоритму RSA."""

from __future__ import annotations

from pathlib import Path

from lab_4.rsa import (
    ALPHABET,
    KeyPair,
    encode_text,
    encrypt_text,
    extended_gcd,
    generate_key_pairs,
    mod_inverse,
    modular_power,
    decrypt_text,
)

OUTPUT_DIR = Path(__file__).resolve().parent / "outputs"
DEFAULT_P = 167  # Вариант 16 по таблице методических указаний.
DEFAULT_Q = 311


def read_int(prompt: str, default: int | None = None) -> int | None:
    """Прочитать целое число; пустой ввод выбирает default, q возвращает назад."""
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


def read_primes() -> tuple[int, int] | None:
    """Запросить два простых числа, предлагая p и q варианта 16."""
    print(f"Параметры варианта 16: p={DEFAULT_P}, q={DEFAULT_Q}.")
    p = read_int("Введите простое p", DEFAULT_P)
    if p is None:
        return None
    q = read_int("Введите простое q", DEFAULT_Q)
    if q is None:
        return None
    return p, q


def show_keys(p: int, q: int) -> list[KeyPair] | None:
    try:
        keys = generate_key_pairs(p, q)
    except ValueError as error:
        print(f"Ошибка формирования ключей: {error}")
        return None
    first = keys[0]
    print(f"\nn = p·q = {first.n}; φ(n) = (p−1)(q−1) = {first.phi}")
    print("№   Открытый ключ (e, n)       Закрытый ключ (d, n)       Проверка e·d mod φ(n)")
    for index, key in enumerate(keys, start=1):
        print(f"{index:<3} ({key.e}, {key.n}){(20 - len(str(key.e)) - len(str(key.n))) * ' '}"
              f"({key.d}, {key.n}){(20 - len(str(key.d)) - len(str(key.n))) * ' '}"
              f"{(key.e * key.d) % key.phi}")
    return keys


def arithmetic_menu() -> None:
    while True:
        print("\nПРОВЕРКА АРИФМЕТИКИ RSA")
        print("1. Расширенный алгоритм Евклида и обратный элемент")
        print("2. Бинарное возведение в степень по модулю")
        print("0. Назад")
        choice = input("Выберите действие: ").strip()
        if choice == "0":
            return
        if choice == "1":
            a = read_int("Введите a")
            b = read_int("Введите b") if a is not None else None
            if a is None or b is None:
                continue
            divisor, x, y = extended_gcd(a, b)
            print(f"НОД({a}, {b}) = {divisor}; коэффициенты Безу: x={x}, y={y}.")
            print(f"Проверка: {a}·({x}) + {b}·({y}) = {a*x + b*y}.")
            value = read_int("Число для нахождения обратного")
            if value is None:
                continue
            modulus = read_int("Модуль для обратного элемента")
            if modulus is None:
                continue
            try:
                inverse = mod_inverse(value, modulus)
                print(f"{value}^(-1) mod {modulus} = {inverse}; проверка: {value*inverse % modulus}.")
            except ValueError as error:
                print(f"Обратный элемент не найден: {error}")
        elif choice == "2":
            base = read_int("Введите основание a")
            exponent = read_int("Введите показатель степени k") if base is not None else None
            modulus = read_int("Введите модуль n") if exponent is not None else None
            if base is None or exponent is None or modulus is None:
                continue
            try:
                print(f"{base}^{exponent} mod {modulus} = {modular_power(base, exponent, modulus)}")
            except ValueError as error:
                print(f"Ошибка вычисления: {error}")
        else:
            print("Выберите 1, 2 или 0.")


def save_demo(plaintext: str, encoded: str, blocks: tuple[int, ...], cipher_blocks: tuple[int, ...],
              ciphertext: str, decoded: str, key: KeyPair) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUTPUT_DIR / "rsa_result.txt"
    report = (
        "Лабораторная работа № 4 — демонстрационный расчёт RSA\n"
        f"Открытый ключ (e, n): {key.public_key}\n"
        f"Закрытый ключ (d, n): {key.private_key}\n"
        f"Допустимые символы: {ALPHABET}; пробел кодируется числом 99; Ё заменяется на Е.\n"
        f"Открытый текст: {plaintext}\n"
        f"Двухзначное представление: {encoded}\n"
        f"Блоки открытого текста: {', '.join(map(str, blocks))}\n"
        f"Блоки шифр-текста: {', '.join(map(str, cipher_blocks))}\n"
        f"Конкатенация шифроблоков: {ciphertext}\n"
        f"Результат расшифрования: {decoded}\n"
    )
    path.write_text(report, encoding="utf-8")
    return path


def run_text_roundtrip(raw: str, keys: list[KeyPair]) -> None:
    """Шифровать и расшифровать введённый текст выбранной парой ключей."""
    try:
        key_number = read_int("Номер пары ключей для шифрования и расшифрования", 1)
        if key_number is None:
            return
        if not 1 <= key_number <= len(keys):
            raise ValueError(f"Номер пары должен быть от 1 до {len(keys)}.")
        key = keys[key_number - 1]
        result = encrypt_text(raw, key)
        decoded = decrypt_text(result.ciphertext, key)
        print(f"\nНормализованный открытый текст: {result.plaintext}")
        print(f"Коды символов (пары цифр): {result.encoded_digits}")
        print("Блоки M < n: " + " | ".join(map(str, result.plaintext_blocks)))
        print("Шифроблоки C = M^e mod n: " + " | ".join(map(str, result.ciphertext_blocks)))
        print(f"Шифр-текст (блоки конкатенированы): {result.ciphertext}")
        print(f"После расшифрования: {decoded}")
        if decoded != result.plaintext:
            raise ValueError("Расшифрованный текст не совпал с исходным.")
        print("Проверка пройдена: открытый текст восстановлен без изменений.")
        print(f"Результат сохранён: {save_demo(result.plaintext, result.encoded_digits, result.plaintext_blocks, result.ciphertext_blocks, result.ciphertext, decoded, key)}")
    except ValueError as error:
        print(f"Ошибка: {error}")


def execute_variant() -> None:
    """Запустить полный расчёт варианта 16 отдельным пунктом главного меню."""
    print("\nВЫПОЛНЕНИЕ ВАРИАНТА 16")
    print(f"Используются заданные вариантом числа: p={DEFAULT_P}, q={DEFAULT_Q}.")
    keys = show_keys(DEFAULT_P, DEFAULT_Q)
    if not keys:
        return
    print(f"\nПреамбула допустимых символов: {ALPHABET} и пробел (99).")
    print("Регистр приводится к верхнему, Ё заменяется на Е; прочие символы пропускаются.")
    run_text_roundtrip(input("Введите открытый текст: "), keys)


def encrypt_decrypt_menu() -> None:
    while True:
        print("\nШИФРОВАНИЕ И РАСШИФРОВАНИЕ")
        print("1. Сформировать и показать не менее трёх пар ключей для p и q")
        print("2. Зашифровать и расшифровать русский текст выбранной парой")
        print("0. Назад")
        choice = input("Выберите действие: ").strip()
        if choice == "0":
            return
        if choice not in {"1", "2"}:
            print("Выберите 1, 2 или 0.")
            continue
        primes = read_primes()
        if primes is None:
            continue
        keys = show_keys(*primes)
        if not keys or choice == "1":
            continue

        print(f"\nПреамбула допустимых символов: {ALPHABET} и пробел (99).")
        print("Регистр приводится к верхнему, Ё заменяется на Е; прочие символы пропускаются.")
        run_text_roundtrip(input("Введите открытый текст: "), keys)


def main() -> None:
    while True:
        print("\n" + "=" * 65)
        print("ЛАБОРАТОРНАЯ РАБОТА № 4 — ШИФРОВАНИЕ С ОТКРЫТЫМ КЛЮЧОМ RSA")
        print("1. Проверка арифметики")
        print("2. Шифровка/дешифровка")
        print("3. Выполнение варианта 16")
        print("4. Выход")
        choice = input("Выберите пункт меню: ").strip()
        if choice == "1":
            arithmetic_menu()
        elif choice == "2":
            encrypt_decrypt_menu()
        elif choice == "3":
            execute_variant()
        elif choice == "4":
            print("Работа завершена.")
            return
        else:
            print("Выберите 1, 2, 3 или 4.")


if __name__ == "__main__":
    main()
