"""
Модуль ядра аффинного шифра:
- Прямое и обратное аффинные преобразования;
- Посимвольное и потоковое шифрование и дешифрование;
- Полный перебор допустимых ключей шифрования (brute-force).
"""

import math
from typing import List, Optional, Tuple

from lab_2.alphabet import Alphabet, DEFAULT_ALPHABET
from lab_2.math_utils import mod_inverse


class AffineCipher:
    """Класс для выполнения операций шифрования и расшифрования аффинным шифром."""

    def __init__(self, alphabet: Optional[Alphabet] = None):
        self.alphabet: Alphabet = alphabet or DEFAULT_ALPHABET

    @property
    def power(self) -> int:
        return self.alphabet.power

    def validate_key(self, a: int, b: Optional[int] = None) -> Tuple[int, int]:
        """Проверка обратимости коэффициента a по модулю мощности алфавита и приведение ключа."""
        a_eff = a % self.power
        if a_eff == 0:
            raise ValueError(
                f"Коэффициент a={a} кратен модулю m={self.power} (необратим)"
            )
        gcd_val = math.gcd(a_eff, self.power)
        if gcd_val != 1:
            raise ValueError(
                f"Коэффициент a={a} необратим по модулю m={self.power} (НОД={gcd_val} != 1)"
            )
        b_eff = (b % self.power) if b is not None else 0
        return a_eff, b_eff

    def E_k(self, x: int, a: int, b: int) -> int:
        """
        Прямое преобразование аффинного шифра:
          y = (a * x + b) mod m
        """
        self.validate_key(a)
        return (a * x + b) % self.power

    def D_k(self, y: int, a: int, b: int) -> int:
        """
        Обратное преобразование аффинного шифра:
          x = a^(-1) * (y - b) mod m
        """
        is_inv, _, a_inv, _ = mod_inverse(a, self.power)
        if not is_inv or a_inv is None:
            raise ValueError(f"Коэффициент a={a} необратим по модулю m={self.power}")
        return (a_inv * (y - b)) % self.power

    def encrypt_symbol(
        self,
        char: str,
        a: int,
        b: int,
        case_mode: str = "lower"
    ) -> str:
        """Шифрование одного символа."""
        norm = self.alphabet.normalize_char(char)
        if norm in self.alphabet.char_to_code:
            code_x = self.alphabet.char_to_code[norm]
            code_y = self.E_k(code_x, a, b)
            res_char = self.alphabet.A_inv(code_y)
            if self.alphabet.case_sensitive:
                return res_char
            if case_mode == "preserve":
                return res_char.upper() if char.isupper() else res_char.lower()
            elif case_mode == "upper":
                return res_char.upper()
            return res_char.lower()
        return char

    def decrypt_symbol(
        self,
        char: str,
        a: int,
        b: int,
        case_mode: str = "lower"
    ) -> str:
        """Расшифрование одного символа."""
        norm = self.alphabet.normalize_char(char)
        if norm in self.alphabet.char_to_code:
            code_y = self.alphabet.char_to_code[norm]
            code_x = self.D_k(code_y, a, b)
            res_char = self.alphabet.A_inv(code_x)
            if self.alphabet.case_sensitive:
                return res_char
            if case_mode == "preserve":
                return res_char.upper() if char.isupper() else res_char.lower()
            elif case_mode == "upper":
                return res_char.upper()
            return res_char.lower()
        return char

    def encrypt(
        self,
        text: str,
        a: int,
        b: int,
        filter_non_alpha: bool = False,
        case_mode: str = "lower"
    ) -> str:
        """Шифрование строки текста."""
        if filter_non_alpha:
            src = self.alphabet.prepare_canonical_text(text)
            return "".join(self.encrypt_symbol(c, a, b, case_mode="lower") for c in src)
        return "".join(self.encrypt_symbol(c, a, b, case_mode=case_mode) for c in text)

    def decrypt(
        self,
        text: str,
        a: int,
        b: int,
        case_mode: str = "lower"
    ) -> str:
        """Расшифрование строки текста."""
        return "".join(self.decrypt_symbol(c, a, b, case_mode=case_mode) for c in text)

    def brute_force(self, ciphertext: str) -> List[Tuple[Tuple[int, int], str]]:
        """
        Полный перебор всех допустимых ключей (a, b).
        Для русского алфавита мощностью m=32 число ключей составляет 16 * 32 = 512.
        """
        valid_a_values = [a for a in range(1, self.power) if math.gcd(a, self.power) == 1]
        results: List[Tuple[Tuple[int, int], str]] = []
        for a in valid_a_values:
            for b in range(self.power):
                dec_text = self.decrypt(ciphertext, a, b)
                results.append(((a, b), dec_text))
        return results


# Глобальный инстанс по умолчанию для упрощенного процедурного вызова
_default_cipher = AffineCipher(DEFAULT_ALPHABET)


def encrypt(
    text: str,
    a: int,
    b: int,
    alphabet: Optional[Alphabet] = None,
    filter_non_alpha: bool = False,
    case_mode: str = "lower"
) -> str:
    cipher = AffineCipher(alphabet) if alphabet else _default_cipher
    return cipher.encrypt(text, a, b, filter_non_alpha=filter_non_alpha, case_mode=case_mode)


def decrypt(
    text: str,
    a: int,
    b: int,
    alphabet: Optional[Alphabet] = None,
    case_mode: str = "lower"
) -> str:
    cipher = AffineCipher(alphabet) if alphabet else _default_cipher
    return cipher.decrypt(text, a, b, case_mode=case_mode)


def brute_force(
    ciphertext: str,
    alphabet: Optional[Alphabet] = None
) -> List[Tuple[Tuple[int, int], str]]:
    cipher = AffineCipher(alphabet) if alphabet else _default_cipher
    return cipher.brute_force(ciphertext)
