from typing import Dict, List, Tuple

ALPHABET_SYMBOLS: str = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
ALPHABET_POWER: int = len(ALPHABET_SYMBOLS)

CHAR_TO_CODE: Dict[str, int] = {char: idx for idx, char in enumerate(ALPHABET_SYMBOLS)}
CODE_TO_CHAR: Dict[int, str] = {idx: char for idx, char in enumerate(ALPHABET_SYMBOLS)}


def normalize_char(char: str) -> str:
    c = char.lower()
    return "е" if c == "ё" else c


def A(char: str) -> int:
    norm = normalize_char(char)
    if norm in CHAR_TO_CODE:
        return CHAR_TO_CODE[norm]
    raise ValueError(f"Символ '{char}' не входит в алфавит (m = {ALPHABET_POWER})")


def A_inv(code: int) -> str:
    return CODE_TO_CHAR[code % ALPHABET_POWER]


def E_k(x: int, k: int) -> int:
    return (x + k) % ALPHABET_POWER


def D_k(y: int, k: int) -> int:
    return (y - k) % ALPHABET_POWER


def encrypt_symbol(char: str, k: int) -> str:
    norm = normalize_char(char)
    if norm in CHAR_TO_CODE:
        return A_inv(E_k(A(norm), k))
    return char


def decrypt_symbol(char: str, k: int) -> str:
    norm = normalize_char(char)
    if norm in CHAR_TO_CODE:
        return A_inv(D_k(A(norm), k))
    return char


def prepare_canonical_text(text: str) -> str:
    result = []
    for ch in text:
        norm = normalize_char(ch)
        if norm in CHAR_TO_CODE:
            result.append(norm)
    return "".join(result)


def encrypt(text: str, k: int, filter_non_alpha: bool = False) -> str:
    if filter_non_alpha:
        text = prepare_canonical_text(text)
    return "".join(encrypt_symbol(ch, k) for ch in text)


def decrypt(text: str, k: int) -> str:
    return "".join(decrypt_symbol(ch, k) for ch in text)


def brute_force(ciphertext: str) -> List[Tuple[int, str]]:
    return [(k, decrypt(ciphertext, k)) for k in range(1, ALPHABET_POWER)]
