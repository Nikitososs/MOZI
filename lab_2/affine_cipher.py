"""
Фасадный модуль аффинного шифра (обратная совместимость):
Объединяет функциональность специализированных модулей:
- lab_2.math_utils: математический аппарат (алгоритм Евклида, Безу, обратный элемент, сравнения, системы);
- lab_2.alphabet: модели алфавитов, пресеты, эталонные частоты;
- lab_2.cipher: операции прямого и обратного преобразования аффинного шифра;
- lab_2.cryptanalysis: частотный анализ, подбор гипотез, оценка осмысленности.
"""

from lab_2.math_utils import (
    extended_gcd,
    mod_inverse,
    solve_linear_congruence,
    solve_system_congruences
)

from lab_2.alphabet import (
    Alphabet,
    RU_ALPHABET,
    EN_ALPHABET,
    PRESETS,
    register_alphabet,
    get_alphabet,
    DEFAULT_ALPHABET,
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
    "RU_ALPHABET",
    "EN_ALPHABET",
    "PRESETS",
    "register_alphabet",
    "get_alphabet",
    "DEFAULT_ALPHABET",
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
