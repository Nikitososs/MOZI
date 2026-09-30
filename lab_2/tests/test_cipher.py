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

    def test_invalid_keys_edge_cases(self):
        cipher = AffineCipher(DEFAULT_ALPHABET)
        # a кратно m (a % 32 == 0)
        with pytest.raises(ValueError, match="кратен модулю"):
            cipher.validate_key(0, 5)
        with pytest.raises(ValueError, match="кратен модулю"):
            cipher.validate_key(32, 5)
        with pytest.raises(ValueError, match="кратен модулю"):
            cipher.validate_key(64, 5)
        # a не взаимно просто с 32
        with pytest.raises(ValueError, match="необратим"):
            cipher.validate_key(2, 5)
        with pytest.raises(ValueError, match="необратим"):
            cipher.validate_key(16, 5)

    def test_key_modulo_equivalence(self):
        cipher = AffineCipher(DEFAULT_ALPHABET)
        # a=35 эквивалентно a=3 (НОД(3, 32)=1)
        a_eff, b_eff = cipher.validate_key(35, 33)
        assert a_eff == 3
        assert b_eff == 1
        # шифрование с (35, 33) идентично шифрованию с (3, 1)
        txt = "тест"
        assert cipher.encrypt(txt, 35, 33) == cipher.encrypt(txt, 3, 1)

    def test_alphabet_validation(self):
        # Алфавит менее чем из 2 символов недопустим
        with pytest.raises(ValueError, match="не менее 2"):
            Alphabet("single", "a")
        with pytest.raises(ValueError, match="не менее 2"):
            Alphabet("empty", "")
        # Проверка неизвестного символа
        with pytest.raises(ValueError, match="не входит в алфавит"):
            DEFAULT_ALPHABET.A("~")
        # Проверка нечислового индекса
        with pytest.raises(TypeError, match="целым числом"):
            DEFAULT_ALPHABET.A_inv("0")  # type: ignore
        # Проверка циклического взятия по модулю
        assert DEFAULT_ALPHABET.A_inv(32) == DEFAULT_ALPHABET.A_inv(0)
        assert DEFAULT_ALPHABET.A_inv(-1) == DEFAULT_ALPHABET.A_inv(31)

    def test_alphabet_delegate_methods(self):
        # Проверка удобных методов Alphabet.encrypt и Alphabet.decrypt
        txt = "привет"
        enc = DEFAULT_ALPHABET.encrypt(txt, 27, 13)
        dec = DEFAULT_ALPHABET.decrypt(enc, 27, 13)
        assert dec == txt

    def test_non_alphabet_symbols_handling(self):
        txt = "Привет, мир! 123"
        # Режим preserve: знаки препинания и пробелы сохраняются
        enc = encrypt(txt, 27, 13, case_mode="preserve", filter_non_alpha=False)
        assert "!" in enc and "123" in enc and "," in enc
        dec = decrypt(enc, 27, 13, case_mode="preserve")
        assert dec == txt

        # Режим filter_non_alpha: только буквы алфавита
        enc_filtered = encrypt(txt, 27, 13, filter_non_alpha=True)
        assert "!" not in enc_filtered and " " not in enc_filtered

