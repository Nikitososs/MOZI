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
        return self.E_k(y, -k)

    def encrypt_symbol(
        self,
        char: str,
        k: int,
        case_mode: str = "lower",
        preserve_case: Optional[bool] = None
    ) -> str:
        if preserve_case is not None:
            case_mode = "preserve" if preserve_case else "lower"
        norm = self.normalize_char(char)
        if norm in self.char_to_code:
            res_char = self.A_inv(self.E_k(self.char_to_code[norm], k))
            if self.case_sensitive:
                return res_char
            if case_mode == "preserve":
                return res_char.upper() if char.isupper() else res_char.lower()
            elif case_mode == "upper":
                return res_char.upper()
            elif case_mode == "lower":
                return res_char.lower()
            return res_char
        return char

    def decrypt_symbol(
        self,
        char: str,
        k: int,
        case_mode: str = "lower",
        preserve_case: Optional[bool] = None
    ) -> str:
        return self.encrypt_symbol(char, -k, case_mode=case_mode, preserve_case=preserve_case)

    def prepare_canonical_text(self, text: str) -> str:
        return "".join(self.normalize_char(c) for c in text if self.normalize_char(c) in self.char_to_code)

    def encrypt(
        self,
        text: str,
        k: int,
        filter_non_alpha: bool = False,
        case_mode: str = "lower",
        preserve_case: Optional[bool] = None
    ) -> str:
        if preserve_case is not None:
            case_mode = "preserve" if preserve_case else "lower"
        if filter_non_alpha:
            src = self.prepare_canonical_text(text)
            return "".join(self.encrypt_symbol(c, k, case_mode="lower") for c in src)
        return "".join(self.encrypt_symbol(c, k, case_mode=case_mode) for c in text)

    def decrypt(
        self,
        text: str,
        k: int,
        case_mode: str = "lower",
        preserve_case: Optional[bool] = None
    ) -> str:
        return self.encrypt(text, -k, filter_non_alpha=False, case_mode=case_mode, preserve_case=preserve_case)

    def brute_force(
        self,
        ciphertext: str,
        case_mode: str = "lower",
        preserve_case: Optional[bool] = None
    ) -> List[Tuple[int, str]]:
        return [
            (k, self.decrypt(ciphertext, k, case_mode=case_mode, preserve_case=preserve_case))
            for k in range(1, self.power)
        ]


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

A = DEFAULT_ALPHABET.A
A_inv = DEFAULT_ALPHABET.A_inv
E_k = DEFAULT_ALPHABET.E_k
D_k = DEFAULT_ALPHABET.D_k
normalize_char = DEFAULT_ALPHABET.normalize_char
encrypt_symbol = DEFAULT_ALPHABET.encrypt_symbol
decrypt_symbol = DEFAULT_ALPHABET.decrypt_symbol
prepare_canonical_text = DEFAULT_ALPHABET.prepare_canonical_text


def encrypt(
    text: str,
    k: int,
    filter_non_alpha: bool = False,
    alphabet: Optional[Alphabet] = None,
    case_mode: str = "lower",
    preserve_case: Optional[bool] = None
) -> str:
    return (alphabet or DEFAULT_ALPHABET).encrypt(
        text, k, filter_non_alpha=filter_non_alpha, case_mode=case_mode, preserve_case=preserve_case
    )


def decrypt(
    text: str,
    k: int,
    alphabet: Optional[Alphabet] = None,
    case_mode: str = "lower",
    preserve_case: Optional[bool] = None
) -> str:
    return (alphabet or DEFAULT_ALPHABET).decrypt(
        text, k, case_mode=case_mode, preserve_case=preserve_case
    )


def brute_force(
    ciphertext: str,
    alphabet: Optional[Alphabet] = None,
    case_mode: str = "lower",
    preserve_case: Optional[bool] = None
) -> List[Tuple[int, str]]:
    return (alphabet or DEFAULT_ALPHABET).brute_force(
        ciphertext, case_mode=case_mode, preserve_case=preserve_case
    )
