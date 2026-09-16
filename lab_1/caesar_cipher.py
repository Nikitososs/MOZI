from typing import Dict, List, Optional, Tuple


class Alphabet:
    def __init__(
        self,
        name: str,
        symbols: str,
        normalize_map: Optional[Dict[str, str]] = None,
        case_sensitive: bool = False
    ):
        self.name = name
        self.symbols = symbols
        self.power = len(symbols)
        self.normalize_map = normalize_map or {}
        self.case_sensitive = case_sensitive
        self.char_to_code: Dict[str, int] = {char: idx for idx, char in enumerate(symbols)}
        self.code_to_char: Dict[int, str] = {idx: char for idx, char in enumerate(symbols)}

    def normalize_char(self, char: str) -> str:
        c = char if self.case_sensitive else char.lower()
        return self.normalize_map.get(c, c)

    def A(self, char: str) -> int:
        norm = self.normalize_char(char)
        if norm in self.char_to_code:
            return self.char_to_code[norm]
        raise ValueError(f"Символ '{char}' не входит в алфавит '{self.name}' (m = {self.power})")

    def A_inv(self, code: int) -> str:
        return self.code_to_char[code % self.power]

    def E_k(self, x: int, k: int) -> int:
        return (x + k) % self.power

    def D_k(self, y: int, k: int) -> int:
        return (y - k) % self.power

    def encrypt_symbol(self, char: str, k: int) -> str:
        norm = self.normalize_char(char)
        if norm in self.char_to_code:
            return self.A_inv(self.E_k(self.char_to_code[norm], k))
        return char

    def decrypt_symbol(self, char: str, k: int) -> str:
        norm = self.normalize_char(char)
        if norm in self.char_to_code:
            return self.A_inv(self.D_k(self.char_to_code[norm], k))
        return char

    def prepare_canonical_text(self, text: str) -> str:
        res = []
        for ch in text:
            norm = self.normalize_char(ch)
            if norm in self.char_to_code:
                res.append(norm)
        return "".join(res)

    def encrypt(self, text: str, k: int, filter_non_alpha: bool = False) -> str:
        if filter_non_alpha:
            text = self.prepare_canonical_text(text)
        return "".join(self.encrypt_symbol(ch, k) for ch in text)

    def decrypt(self, text: str, k: int) -> str:
        return "".join(self.decrypt_symbol(ch, k) for ch in text)

    def brute_force(self, ciphertext: str) -> List[Tuple[int, str]]:
        return [(k, self.decrypt(ciphertext, k)) for k in range(1, self.power)]


RU_ALPHABET = Alphabet(
    name="Русский (ru, m=32, е/ё)",
    symbols="абвгдежзийклмнопрстуфхцчшщъыьэюя",
    normalize_map={"ё": "е"}
)

EN_ALPHABET = Alphabet(
    name="English (en, m=26)",
    symbols="abcdefghijklmnopqrstuvwxyz"
)

PRESETS: Dict[str, Alphabet] = {
    "ru": RU_ALPHABET,
    "en": EN_ALPHABET
}


def register_alphabet(key: str, alphabet: Alphabet) -> None:
    PRESETS[key.lower()] = alphabet


def get_alphabet(key: str = "ru") -> Alphabet:
    key_lower = key.lower()
    if key_lower in PRESETS:
        return PRESETS[key_lower]
    raise KeyError(f"Неизвестный алфавит '{key}'. Доступные: {list(PRESETS.keys())}")


DEFAULT_ALPHABET: Alphabet = RU_ALPHABET
ALPHABET_SYMBOLS: str = DEFAULT_ALPHABET.symbols
ALPHABET_POWER: int = DEFAULT_ALPHABET.power
CHAR_TO_CODE: Dict[str, int] = DEFAULT_ALPHABET.char_to_code
CODE_TO_CHAR: Dict[int, str] = DEFAULT_ALPHABET.code_to_char


def normalize_char(char: str, alphabet: Optional[Alphabet] = None) -> str:
    return (alphabet or DEFAULT_ALPHABET).normalize_char(char)


def A(char: str, alphabet: Optional[Alphabet] = None) -> int:
    return (alphabet or DEFAULT_ALPHABET).A(char)


def A_inv(code: int, alphabet: Optional[Alphabet] = None) -> str:
    return (alphabet or DEFAULT_ALPHABET).A_inv(code)


def E_k(x: int, k: int, alphabet: Optional[Alphabet] = None) -> int:
    return (alphabet or DEFAULT_ALPHABET).E_k(x, k)


def D_k(y: int, k: int, alphabet: Optional[Alphabet] = None) -> int:
    return (alphabet or DEFAULT_ALPHABET).D_k(y, k)


def encrypt_symbol(char: str, k: int, alphabet: Optional[Alphabet] = None) -> str:
    return (alphabet or DEFAULT_ALPHABET).encrypt_symbol(char, k)


def decrypt_symbol(char: str, k: int, alphabet: Optional[Alphabet] = None) -> str:
    return (alphabet or DEFAULT_ALPHABET).decrypt_symbol(char, k)


def prepare_canonical_text(text: str, alphabet: Optional[Alphabet] = None) -> str:
    return (alphabet or DEFAULT_ALPHABET).prepare_canonical_text(text)


def encrypt(
    text: str,
    k: int,
    filter_non_alpha: bool = False,
    alphabet: Optional[Alphabet] = None
) -> str:
    return (alphabet or DEFAULT_ALPHABET).encrypt(text, k, filter_non_alpha=filter_non_alpha)


def decrypt(text: str, k: int, alphabet: Optional[Alphabet] = None) -> str:
    return (alphabet or DEFAULT_ALPHABET).decrypt(text, k)


def brute_force(ciphertext: str, alphabet: Optional[Alphabet] = None) -> List[Tuple[int, str]]:
    return (alphabet or DEFAULT_ALPHABET).brute_force(ciphertext)
