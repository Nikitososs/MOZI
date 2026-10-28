"""Арифметика и текстовое кодирование для учебной реализации RSA."""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd

ALPHABET = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
SYMBOL_TO_CODE = {symbol: index + 10 for index, symbol in enumerate(ALPHABET)}
CODE_TO_SYMBOL = {code: symbol for symbol, code in SYMBOL_TO_CODE.items()}
SPACE_CODE = 99


def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    """Вернуть (g, x, y), для которых a*x + b*y = g = gcd(a, b)."""
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


def mod_inverse(value: int, modulus: int) -> int:
    """Найти обратный элемент value по положительному модулю modulus."""
    if modulus <= 1:
        raise ValueError("Модуль должен быть больше 1.")
    divisor, coefficient, _ = extended_gcd(value, modulus)
    if divisor != 1:
        raise ValueError(f"Обратный элемент не существует: НОД({value}, {modulus}) = {divisor}.")
    return coefficient % modulus


def modular_power(base: int, exponent: int, modulus: int) -> int:
    """Вычислить base**exponent mod modulus бинарным алгоритмом."""
    if exponent < 0:
        raise ValueError("Показатель степени не может быть отрицательным.")
    if modulus <= 0:
        raise ValueError("Модуль должен быть положительным.")
    result = 1 % modulus
    factor = base % modulus
    power = exponent
    while power:
        if power & 1:
            result = (result * factor) % modulus
        factor = (factor * factor) % modulus
        power >>= 1
    return result


def is_prime(number: int) -> bool:
    """Проверить простоту перебором делителей до квадратного корня числа."""
    if number < 2:
        return False
    if number == 2:
        return True
    if number % 2 == 0:
        return False

    divisor = 3
    while divisor * divisor <= number:
        if number % divisor == 0:
            return False
        divisor += 2
    return True


@dataclass(frozen=True)
class KeyPair:
    """Открытая и соответствующая ей закрытая пара RSA."""

    e: int
    d: int
    n: int
    phi: int

    @property
    def public_key(self) -> tuple[int, int]:
        return self.e, self.n

    @property
    def private_key(self) -> tuple[int, int]:
        return self.d, self.n


def generate_key_pairs(p: int, q: int, count: int = 3) -> list[KeyPair]:
    """Построить count различных пар ключей для заданных простых p и q."""
    if not is_prime(p) or not is_prime(q):
        raise ValueError("p и q должны быть простыми числами больше 1.")
    if p == q:
        raise ValueError("Простые числа p и q должны различаться.")
    n = p * q
    if n <= SPACE_CODE:
        raise ValueError(f"Для кодов символов 10–41 и пробела 99 требуется n > 99 (сейчас n={n}).")
    if count < 3:
        raise ValueError("Для лабораторной требуется не менее трёх пар ключей.")
    phi = (p - 1) * (q - 1)
    pairs: list[KeyPair] = []
    for e in range(2, phi):
        if gcd(e, phi) == 1:
            pairs.append(KeyPair(e=e, d=mod_inverse(e, phi), n=n, phi=phi))
            if len(pairs) == count:
                break
    if len(pairs) < count:
        raise ValueError(f"Для φ(n)={phi} удалось сформировать только {len(pairs)} ключевых пар.")
    return pairs


def encode_text(text: str) -> tuple[str, str]:
    """Нормализовать текст и вернуть (нормализованный текст, строку пар кодов)."""
    normalized: list[str] = []
    canonical_input = (
        text.upper().replace("Ё", "Е").replace("\r\n", " ").replace("\r", " ").replace("\n", " ")
    )
    for char in canonical_input:
        if char in SYMBOL_TO_CODE:
            normalized.append(char)
        elif char in " \t\r\n":
            normalized.append(" ")
    canonical = "".join(normalized)
    digits = "".join(
        f"{SPACE_CODE:02d}" if char == " " else f"{SYMBOL_TO_CODE[char]:02d}" for char in canonical
    )
    return canonical, digits


def split_plaintext_blocks(digits: str, modulus: int) -> list[int]:
    """Жадно собрать максимальные десятичные блоки меньше n без ведущего нуля."""
    if modulus <= SPACE_CODE:
        raise ValueError("Модуль n должен быть больше 99.")
    if not digits or len(digits) % 2:
        raise ValueError("Строка кодов должна быть непустой и содержать целое число пар цифр.")
    blocks: list[int] = []
    if not digits.isdigit():
        raise ValueError("Строка кодов должна содержать только цифры.")
    if digits[0] == "0":
        raise ValueError("Кодируемая строка не должна начинаться с нуля.")
    offset = 0
    while offset < len(digits):
        end = offset + 1
        while end <= len(digits) and int(digits[offset:end]) < modulus:
            end += 1
        end -= 1
        if end < len(digits):
            # Переносим границу влево через ноль, чтобы следующий M не начинался с 0.
            while end > offset and digits[end] == "0":
                end -= 1
        if end <= offset:
            raise ValueError("Не удалось выбрать блок без ведущего нуля и меньше n.")
        blocks.append(int(digits[offset:end]))
        offset = end
    return blocks


@dataclass(frozen=True)
class EncryptionResult:
    plaintext: str
    encoded_digits: str
    plaintext_blocks: tuple[int, ...]
    ciphertext_blocks: tuple[int, ...]
    ciphertext: str


def encrypt_text(text: str, key: KeyPair) -> EncryptionResult:
    """Закодировать, разбить и зашифровать русский текст блоками."""
    plaintext, digits = encode_text(text)
    if not plaintext:
        raise ValueError("После подготовки в тексте не осталось русских букв или пробелов.")
    blocks = split_plaintext_blocks(digits, key.n)
    encrypted = tuple(modular_power(block, key.e, key.n) for block in blocks)
    width = len(str(key.n))
    ciphertext = "".join(f"{block:0{width}d}" for block in encrypted)
    return EncryptionResult(plaintext, digits, tuple(blocks), encrypted, ciphertext)


def decrypt_text(ciphertext: str, key: KeyPair) -> str:
    """Расшифровать конкатенацию шифроблоков фиксированной ширины."""
    width = len(str(key.n))
    if not ciphertext or len(ciphertext) % width:
        raise ValueError(f"Длина шифр-текста должна быть положительна и кратна {width}.")
    if not ciphertext.isdigit():
        raise ValueError("Шифр-текст должен содержать только цифры.")
    decoded_digits: list[str] = []
    for offset in range(0, len(ciphertext), width):
        cipher_block = int(ciphertext[offset : offset + width])
        if cipher_block >= key.n:
            raise ValueError(f"Шифроблок {cipher_block} должен быть меньше n={key.n}.")
        plain_block = modular_power(cipher_block, key.d, key.n)
        block_digits = str(plain_block)
        if block_digits.startswith("0"):
            raise ValueError(
                "Расшифрованный блок начинается с нуля: неверный ключ или повреждённые данные."
            )
        decoded_digits.append(block_digits)
    digit_stream = "".join(decoded_digits)
    if len(digit_stream) % 2:
        raise ValueError("Объединённая строка кодов должна содержать чётное число цифр.")
    decoded: list[str] = []
    for pair_start in range(0, len(digit_stream), 2):
        code = int(digit_stream[pair_start : pair_start + 2])
        if code == SPACE_CODE:
            decoded.append(" ")
        elif code in CODE_TO_SYMBOL:
            decoded.append(CODE_TO_SYMBOL[code])
        else:
            raise ValueError(f"Неизвестный код символа {code}; проверьте закрытый ключ.")
    return "".join(decoded)
