"""Тесты для модуля cipher и alphabet: модель алфавита, шифрование и дешифрование."""

import pytest
from lab_2.alphabet import Alphabet, DEFAULT_ALPHABET, RU_ALPHABET, EN_ALPHABET
from lab_2.cipher import AffineCipher, encrypt, decrypt, brute_force


class TestAlphabet:
    """Тестирование модели алфавита."""

    def test_default_alphabet_properties(self):
        assert DEFAULT_ALPHABET.power == 32
        assert DEFAULT_ALPHABET.normalize_char("Ё") == "е"
        assert DEFAULT_ALPHABET.A("а") == 0
        assert DEFAULT_ALPHABET.A("я") == 31
        assert DEFAULT_ALPHABET.A_inv(0) == "а"
        assert DEFAULT_ALPHABET.A_inv(31) == "я"

    def test_unknown_symbol_raises_error(self):
        with pytest.raises(ValueError):
            DEFAULT_ALPHABET.A("$")


class TestAffineCipherTransformations:
    """Тестирование прямого и обратного преобразования аффинного шифра."""

    def test_invalid_key_raises_error(self):
        cipher = AffineCipher(DEFAULT_ALPHABET)
        # 14 не взаимно просто с 32 (НОД=2)
        with pytest.raises(ValueError):
            cipher.E_k(0, a=14, b=5)
        with pytest.raises(ValueError):
            cipher.D_k(0, a=14, b=5)

    def test_encrypt_decrypt_symbol(self, alphabet_info):
        cipher = AffineCipher(DEFAULT_ALPHABET)
        a, b = 27, 13
        for sym in alphabet_info["symbols"]:
            enc = cipher.encrypt_symbol(sym, a, b)
            dec = cipher.decrypt_symbol(enc, a, b)
            assert dec == sym

    def test_encrypt_decrypt_text(self, variant_16_data):
        a, b = variant_16_data["key"]
        plaintext = variant_16_data["plaintext"]
        expected_ct = variant_16_data["ciphertext"]

        ciphertext = encrypt(plaintext, a, b)
        assert ciphertext == expected_ct

        decrypted = decrypt(ciphertext, a, b)
        assert decrypted == plaintext

    def test_author_work_encryption(self, variant_16_data):
        a, b = variant_16_data["key"]
        ot = variant_16_data["author_work_ot"]
        st = variant_16_data["author_work_st"]

        assert encrypt(ot, a, b) == st
        assert decrypt(st, a, b) == ot

    def test_brute_force_keys_count(self):
        # Для m=32 допустимых ключей 16 * 32 = 512
        bf = brute_force("проверка")
        assert len(bf) == 512
