"""
Модуль алфавитов и таблиц частот для аффинного шифра:
- Класс Alphabet для представления алфавитов произвольной мощности;
- Пресеты русского (m=32, е/ё) и английского (m=26) алфавитов;
- Таблица эталонных частот символов русского языка (Таблица 3 методических указаний).
"""

from typing import Dict, List, Optional, Tuple


class Alphabet:
    """Модель алфавита для криптографических преобразований."""

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
        """Приведение символа к нормализованному виду (нижний регистр, замена ё->е)."""
        c = char if self.case_sensitive else char.lower()
        return self.normalize_map.get(c, c)

    def A(self, char: str) -> int:
        """Прямое отображение символа в числовой индекс: A(c) = x."""
        norm = self.normalize_char(char)
        if norm in self.char_to_code:
            return self.char_to_code[norm]
        raise ValueError(f"Символ '{char}' не входит в алфавит '{self.name}' (m = {self.power})")

    def A_inv(self, code: int) -> str:
        """Обратное отображение числового индекса в символ алфавита: A^(-1)(x) = c."""
        return self.code_to_char[code % self.power]

    def prepare_canonical_text(self, text: str) -> str:
        """Извлечение только символов алфавита в нижнем регистре (без пробелов и знаков)."""
        return "".join(self.normalize_char(c) for c in text if self.normalize_char(c) in self.char_to_code)


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
    """Регистрация пользовательского алфавита в пуле пресетов."""
    PRESETS[key.lower()] = alphabet


def get_alphabet(key: str = "ru") -> Alphabet:
    """Получение алфавита по его кодовому названию."""
    key_lower = key.lower()
    if key_lower in PRESETS:
        return PRESETS[key_lower]
    raise KeyError(f"Неизвестный алфавит '{key}'. Доступные: {list(PRESETS.keys())}")


DEFAULT_ALPHABET: Alphabet = RU_ALPHABET

# Таблица эталонных частот букв русского языка (по методичке Табл. 3, отсортированная по убыванию)
RUSSIAN_FREQUENCIES: List[Tuple[str, float]] = [
    ("о", 0.090),
    ("е", 0.072),
    ("а", 0.062),
    ("и", 0.062),
    ("т", 0.053),
    ("н", 0.053),
    ("с", 0.045),
    ("р", 0.040),
    ("в", 0.038),
    ("л", 0.035),
    ("к", 0.028),
    ("м", 0.026),
    ("д", 0.025),
    ("п", 0.023),
    ("у", 0.021),
    ("я", 0.018),
    ("ы", 0.016),
    ("з", 0.016),
    ("ь", 0.014),
    ("б", 0.014),
    ("г", 0.013),
    ("ч", 0.012),
    ("й", 0.010),
    ("х", 0.009),
    ("ж", 0.007),
    ("ю", 0.006),
    ("ш", 0.006),
    ("ц", 0.004),
    ("щ", 0.003),
    ("э", 0.003),
    ("ф", 0.002),
    ("ъ", 0.001)
]
