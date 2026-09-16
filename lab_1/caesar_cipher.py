"""
Модуль криптографического ядра: Шифр Цезаря.
Дисциплина: МОЗИ, Лабораторная работа № 1.
Содержит исключительно математические функции преобразования алфавита и алгоритм шифрования.
"""

from typing import Dict, List, Tuple

ALPHABET_SYMBOLS: str = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
ALPHABET_POWER: int = len(ALPHABET_SYMBOLS)

CHAR_TO_CODE: Dict[str, int] = {char: idx for idx, char in enumerate(ALPHABET_SYMBOLS)}
CODE_TO_CHAR: Dict[int, str] = {idx: char for idx, char in enumerate(ALPHABET_SYMBOLS)}


def normalize_char(char: str) -> str:
    """Приведение символа к нижнему регистру с отождествлением 'ё' -> 'е'."""
    c = char.lower()
    return "е" if c == "ё" else c


def A(char: str) -> int:
    """Отображение символа алфавита в числовой код: A(b_i) = x_i in [0; m-1]."""
    norm = normalize_char(char)
    if norm in CHAR_TO_CODE:
        return CHAR_TO_CODE[norm]
    raise ValueError(f"Символ '{char}' не входит в алфавит (m = {ALPHABET_POWER})")


def A_inv(code: int) -> str:
    """Обратное отображение кода в символ: A^(-1)(y_i) = c_i."""
    return CODE_TO_CHAR[code % ALPHABET_POWER]


def E_k(x: int, k: int) -> int:
    """Прямое линейное преобразование: y_i = (x_i + k) mod m."""
    return (x + k) % ALPHABET_POWER


def D_k(y: int, k: int) -> int:
    """Обратное линейное преобразование: x_i = (y_i - k) mod m."""
    return (y - k) % ALPHABET_POWER


def encrypt_symbol(char: str, k: int) -> str:
    """Шифрование одного символа через композицию функций: c = A^(-1)(E_k(A(b)))."""
    norm = normalize_char(char)
    if norm in CHAR_TO_CODE:
        return A_inv(E_k(A(norm), k))
    return char


def decrypt_symbol(char: str, k: int) -> str:
    """Расшифрование одного символа через композицию функций: b = A^(-1)(D_k(A(c)))."""
    norm = normalize_char(char)
    if norm in CHAR_TO_CODE:
        return A_inv(D_k(A(norm), k))
    return char


def prepare_canonical_text(text: str) -> str:
    """Приведение текста к каноническому виду (нижний регистр, без пробелов и знаков)."""
    result = []
    for ch in text:
        norm = normalize_char(ch)
        if norm in CHAR_TO_CODE:
            result.append(norm)
    return "".join(result)


def encrypt(text: str, k: int, filter_non_alpha: bool = False) -> str:
    """Посимвольное шифрование текста шифром Цезаря с ключом k."""
    if filter_non_alpha:
        text = prepare_canonical_text(text)
    return "".join(encrypt_symbol(ch, k) for ch in text)


def decrypt(text: str, k: int) -> str:
    """Посимвольное расшифрование текста шифром Цезаря с ключом k."""
    return "".join(decrypt_symbol(ch, k) for ch in text)


def brute_force(ciphertext: str) -> List[Tuple[int, str]]:
    """Полный перебор всех 31 возможных ключей."""
    return [(k, decrypt(ciphertext, k)) for k in range(1, ALPHABET_POWER)]
