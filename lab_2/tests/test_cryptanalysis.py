"""Тесты для модуля cryptanalysis: частотный анализ, подбор гипотез, решение варианта 16."""

import pytest
from lab_2.cryptanalysis import (
    frequency_analysis,
    generate_hypotheses_systems,
    score_russian_text,
    crack_affine_cipher
)
from lab_2.cipher import brute_force


class TestCryptanalysis:
    """Тестирование частотного анализа и криптоанализа."""

    def test_frequency_analysis_top_letters(self, variant_16_data):
        ct = variant_16_data["ciphertext"]
        fa = frequency_analysis(ct)

        top_chars = [item[0] for item in fa["sorted_chars"][:3]]
        # Самые частые буквы шифр-текста варианта 16: 'з', 'м', 'н'
        assert top_chars == ["з", "м", "н"]
        assert fa["counts"]["з"] == 21
        assert fa["total_alpha_chars"] == 168

    def test_hypotheses_generation_contains_correct_key(self, variant_16_data):
        ct = variant_16_data["ciphertext"]
        expected_key = variant_16_data["key"]

        hypotheses = generate_hypotheses_systems(ct, top_ct_count=6, top_pt_count=6)
        all_valid_keys = [k for h in hypotheses for k in h["valid_keys"]]

        assert expected_key in all_valid_keys

    def test_crack_affine_cipher_finds_variant_16(self, variant_16_data):
        ct = variant_16_data["ciphertext"]
        expected_key = variant_16_data["key"]
        expected_pt = variant_16_data["plaintext"]

        ranked = crack_affine_cipher(ct, top_n=3)
        assert len(ranked) > 0
        best_score, best_key, best_mapping, best_text = ranked[0]

        assert best_key == expected_key
        assert best_text == expected_pt

    def test_bruteforce_recovers_key(self, variant_16_data):
        ct = variant_16_data["ciphertext"]
        expected_pt = variant_16_data["plaintext"]

        bf_results = brute_force(ct)
        assert len(bf_results) == 512

        matching = [key for key, text in bf_results if text == expected_pt]
        assert matching == [(27, 13)]

    def test_frequency_analysis_empty_and_non_alpha(self):
        # Пустой ввод
        fa_empty = frequency_analysis("")
        assert fa_empty["total_alpha_chars"] == 0
        assert fa_empty["frequencies"]["а"] == 0.0

        # Ввод без букв алфавита (только цифры и символы)
        fa_punct = frequency_analysis("12345 !@#$")
        assert fa_punct["total_alpha_chars"] == 0

    def test_hypotheses_generation_edge_cases(self):
        # При отсутствии букв или наличии только 1 уникальной буквы системы не строятся
        assert generate_hypotheses_systems("") == []
        assert generate_hypotheses_systems("!!!!") == []
        assert generate_hypotheses_systems("аааааааа") == []

        # crack_affine_cipher возвращает пустой список для нерелевантного текста
        assert crack_affine_cipher("") == []
        assert crack_affine_cipher("12345") == []

    def test_english_cryptanalysis(self):
        from lab_2.alphabet import EN_ALPHABET
        from lab_2.cipher import encrypt

        sample_en = (
            "the mathematical foundations of information security is an essential discipline. "
            "classical cryptography and frequency analysis allow recovering original plaintexts."
        )
        # Для EN m=26; выберем ключ a=5 (НОД(5, 26)=1), b=8
        key_a, key_b = 5, 8
        ct_en = encrypt(sample_en, key_a, key_b, alphabet=EN_ALPHABET)

        # Проверим генерацию гипотез с EN_ALPHABET
        hyps = generate_hypotheses_systems(ct_en, alphabet=EN_ALPHABET, top_ct_count=5, top_pt_count=5)
        all_keys = [k for h in hyps for k in h["valid_keys"]]
        assert (key_a, key_b) in all_keys

        # Проверим ранжирование через crack_affine_cipher
        cracked = crack_affine_cipher(ct_en, alphabet=EN_ALPHABET, top_n=3)
        assert len(cracked) > 0
        best_sc, best_k, _, _ = cracked[0]
        assert best_k == (key_a, key_b)

