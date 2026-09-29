"""
Лабораторная работа № 2: Криптоанализ аффинного шифра.

Пакет состоит из логических модулей:
- math_utils: расширенный алгоритм Евклида, коэффициенты Безу, обратный элемент, сравнения, системы;
- alphabet: модель алфавита, таблица кодировок, эталонные частоты букв русского языка;
- cipher: аффинный шифр (класс AffineCipher, encrypt, decrypt, brute_force);
- cryptanalysis: частотный анализ, подбор гипотез, оценка осмысленности;
- variants: база данных вариантов заданий (вариант 16 решен);
- main: консольное интерактивное приложение.
"""

from lab_2.math_utils import (
    extended_gcd,
    mod_inverse,
    solve_linear_congruence,
    solve_system_congruences
)
from lab_2.alphabet import (
    Alphabet,
    DEFAULT_ALPHABET,
    RU_ALPHABET,
    EN_ALPHABET,
    RUSSIAN_FREQUENCIES
)
from lab_2.cipher import (
    AffineCipher,
    encrypt,
    decrypt,
    brute_force
)
from lab_2.cryptanalysis import (
    frequency_analysis,
    generate_hypotheses_systems,
    score_russian_text,
    crack_affine_cipher
)

__all__ = [
    "extended_gcd",
    "mod_inverse",
    "solve_linear_congruence",
    "solve_system_congruences",
    "Alphabet",
    "DEFAULT_ALPHABET",
    "RU_ALPHABET",
    "EN_ALPHABET",
    "RUSSIAN_FREQUENCIES",
    "AffineCipher",
    "encrypt",
    "decrypt",
    "brute_force",
    "frequency_analysis",
    "generate_hypotheses_systems",
    "score_russian_text",
    "crack_affine_cipher",
]
