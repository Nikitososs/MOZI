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
  "title": "Шифрование с открытым ключом. Алгоритм RSA",
  "work": {
    "type": "Лабораторная работа № 4",
    "variant": "16"
  }
}
}}

# СОДЕРЖАНИЕ

# ОСНОВНАЯ ЧАСТЬ

## Результаты варианта 16

Заданы $p=167$, $q=311$. Получены $n=pq=51937$ и $\varphi(n)=(p-1)(q-1)=51460$. Сформированы три пары; для каждой выполнено $ed\bmod\varphi(n)=1$.

Таблица: Сформированные пары ключей

| № | $e$ | $d$ | $n$ | $ed\bmod\varphi(n)$ |
|---:|---:|---:|---:|---:|
| 1 | 3 | 34307 | 51937 | 1 |
| 2 | 7 | 14703 | 51937 | 1 |
| 3 | 9 | 28589 | 51937 | 1 |

Для контрольного текста `ВАСЯ МОЛОДЕЦ` использована первая пара ключей. Буквы кодируются двухзначными кодами, пробел — `99`; блоки собираются так, чтобы каждое число было меньше $n$ и не начиналось с нуля.

- цифровая строка: `121027419922242124141532`;
- блоки открытого текста: `12102, 7419, 9222, 42124, 14153, 2`;
- шифроблоки: `44694, 28921, 8235, 26258, 49659, 8`;
- конкатенированный шифр-текст: `446942892108235262584965900008`;
- результат расшифрования: `ВАСЯ МОЛОДЕЦ`.

Для каждого блока выполняются $C=M^e\bmod n$ и $M=C^d\bmod n$. Кодирование, разбиение и проверка обратного преобразования находятся в `lab_4/rsa.py`; меню — в `lab_4/main.py`.


---

## Работа приложения

Запуск: `python -m lab_4.main`. Главный экран содержит проверку арифметики, шифрование/расшифрование для введённых $p,q$, отдельное выполнение варианта 16 и выход. В пункте шифрования программа проверяет простоту и различие $p,q$, выводит три пары ключей; затем принимает открытый текст, кодирует его парами цифр, собирает блоки меньше $n$, шифрует их и расшифровывает для проверки. На экране показываются цифровая строка, открытые и зашифрованные блоки, итоговая строка и результат обратного преобразования; запись сохраняется в `lab_4/outputs/rsa_result.txt`.

# СПИСОК ЛИТЕРАТУРЫ

- Математические основы защиты информации : методические указания к лабораторным работам / Минобрнауки России, Омский государственный технический университет ; составители С. Ю. Белим, С. В. Белим. — Омск : Издательство ОмГТУ, 2023. — С. 32–35, приложение 4. — Текст : электронный.

# ПРИЛОЖЕНИЯ

## Приложение А. Фрагмент исходного кода `rsa.py`

Кодирование русского текста, разбиение на допустимые блоки, шифрование и обратное декодирование.

Листинг: Основные функции модуля `rsa.py`

```python
from __future__ import annotations

from dataclasses import dataclass
from math import gcd

ALPHABET = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
SYMBOL_TO_CODE = {symbol: index + 10 for index, symbol in enumerate(ALPHABET)}
CODE_TO_SYMBOL = {code: symbol for symbol, code in SYMBOL_TO_CODE.items()}
SPACE_CODE = 99


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
```
