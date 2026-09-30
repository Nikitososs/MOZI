"""
Модуль алфавитов и таблиц частот для аффинного шифра:
- Класс Alphabet для представления алфавитов произвольной мощности;
- Пресеты русского (m=32, е/ё) и английского (m=26) алфавитов;
- Таблицы эталонных частот символов русского и английского языков;
- Получение эталонного распределения по активному алфавиту.
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
        if len(symbols) < 2:
            raise ValueError(f"Алфавит '{name}' должен содержать не менее 2 символов (получено: {len(symbols)})")
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
        if not isinstance(code, int):
            raise TypeError(f"Индекс должен быть целым числом, получено {type(code).__name__}")
        return self.code_to_char[code % self.power]

    def prepare_canonical_text(self, text: str) -> str:
        """Извлечение только символов алфавита в нижнем регистре (без пробелов и знаков)."""
        return "".join(self.normalize_char(c) for c in text if self.normalize_char(c) in self.char_to_code)

    def encrypt(
        self,
        text: str,
        a: int,
        b: int,
        filter_non_alpha: bool = False,
        case_mode: str = "lower"
    ) -> str:
        """Удобная обертка для шифрования данным алфавитом."""
        from lab_2.cipher import AffineCipher
        return AffineCipher(self).encrypt(text, a, b, filter_non_alpha=filter_non_alpha, case_mode=case_mode)

    def decrypt(
        self,
        text: str,
        a: int,
        b: int,
        case_mode: str = "lower"
    ) -> str:
        """Удобная обертка для расшифрования данным алфавитом."""
        from lab_2.cipher import AffineCipher
        return AffineCipher(self).decrypt(text, a, b, case_mode=case_mode)


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

# Таблица эталонных частот букв английского языка (отсортированная по убыванию)
ENGLISH_FREQUENCIES: List[Tuple[str, float]] = [
    ("e", 0.127),
    ("t", 0.091),
    ("a", 0.082),
    ("o", 0.075),
    ("i", 0.070),
    ("n", 0.067),
    ("s", 0.063),
    ("h", 0.061),
    ("r", 0.060),
    ("d", 0.043),
    ("l", 0.040),
    ("c", 0.028),
    ("u", 0.028),
    ("m", 0.024),
    ("w", 0.023),
    ("f", 0.022),
    ("g", 0.020),
    ("y", 0.020),
    ("p", 0.019),
    ("b", 0.015),
    ("v", 0.010),
    ("k", 0.008),
    ("j", 0.002),
    ("x", 0.002),
    ("q", 0.001),
    ("z", 0.001)
]


def get_reference_frequencies(alphabet: Alphabet) -> List[Tuple[str, float]]:
    """Возвращает эталонные частоты для указанного алфавита."""
    name_low = alphabet.name.lower()
    if name_low.startswith("рус") or "ru" in name_low or "абв" in alphabet.symbols:
        return RUSSIAN_FREQUENCIES
    elif name_low.startswith("eng") or "en" in name_low or "abc" in alphabet.symbols:
        return ENGLISH_FREQUENCIES
    else:
        # Для пользовательских алфавитов: равномерное распределение
        uniform_p = 1.0 / alphabet.power
        return [(s, uniform_p) for s in alphabet.symbols]
