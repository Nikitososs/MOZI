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
