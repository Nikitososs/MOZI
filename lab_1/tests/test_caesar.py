"""
Тестовый набор pytest для шифра Цезаря (Лабораторная работа № 1).
Использует фикстуры, параметризацию и стандартные assert.
"""

import pytest
from lab_1.caesar_cipher import (
    A,
    A_inv,
    E_k,
    D_k,
    encrypt_symbol,
    decrypt_symbol,
    prepare_canonical_text,
    encrypt,
    decrypt,
    brute_force,
    save_result_to_file,
    format_encryption_record,
    format_bruteforce_records
)


def test_alphabet_power_and_mapping(alphabet_info):
    """Проверка мощности алфавита и таблицы взаимно однозначного кодирования."""
    assert alphabet_info["power"] == 32
    assert len(alphabet_info["symbols"]) == 32

    # Проверка кодов каждого символа
    for char, expected_code in alphabet_info["table"].items():
        assert A(char) == expected_code
        assert A_inv(expected_code) == char

    # Проверка отождествления 'ё' -> 'е' (код 5)
    assert A("ё") == 5
    assert A("е") == 5


def test_manual_example_encoding(manual_example):
    """Проверка вектора кодирования примера методички: A(асудьикто)."""
    codes = [A(ch) for ch in manual_example["ot"]]
    assert codes == manual_example["codes"]


def test_manual_example_encryption(manual_example):
    """Проверка шифрования примера методички при k = 24."""
    encrypted = encrypt(manual_example["ot"], manual_example["key"])
    assert encrypted == manual_example["st"]


def test_manual_example_decryption(manual_example):
    """Проверка расшифрования примера методички при k = 24."""
    decrypted = decrypt(manual_example["st"], manual_example["key"])
    assert decrypted == manual_example["ot"]


def test_manual_example_author_work(manual_example):
    """Проверка зашифрования фамилии и названия из примера при k = 24."""
    encrypted = encrypt(manual_example["author_work_ot"], manual_example["key"])
    assert encrypted == manual_example["author_work_st"]


def test_canonical_text_preparation():
    """Проверка нормализации текста естественного языка."""
    raw_text = "А судьи кто?"
    assert prepare_canonical_text(raw_text) == "асудьикто"


def test_preserve_non_alphabet_symbols():
    """Проверка сохранения символов, не входящих в русский алфавит (п. 2.1)."""
    raw_text = "привет, World! 123"
    encrypted = encrypt(raw_text, 1)
    assert encrypted == "рсйгжу, World! 123"
    assert decrypt(encrypted, 1) == raw_text


def test_variant_1_solution(variant_1_data):
    """Проверка криптоанализа и ответа для Варианта № 1 (Гоголь, Ревизор)."""
    decrypted = decrypt(variant_1_data["ciphertext"], variant_1_data["key"])
    assert decrypted == variant_1_data["plaintext"]

    encrypted_author_work = encrypt(variant_1_data["author_work_ot"], variant_1_data["key"])
    assert encrypted_author_work == variant_1_data["author_work_st"]


def test_brute_force_contains_correct_key(variant_1_data):
    """Проверка работы полного перебора: наличие истинного текста в списке вариантов."""
    results = brute_force(variant_1_data["ciphertext"])
    assert len(results) == 31
    found = [text for k, text in results if k == variant_1_data["key"]]
    assert len(found) == 1
    assert found[0] == variant_1_data["plaintext"]


@pytest.mark.parametrize("var_no", list(range(1, 31)))
def test_all_database_variants(var_no, all_variants):
    """Параметризованный тест: проверка обратимости всех 30 вариантов методички."""
    data = all_variants[var_no]
    ct = data["ciphertext"]
    k = data["key"]
    pt = data["plaintext"]

    assert decrypt(ct, k) == pt, f"Ошибка расшифрования для варианта {var_no}"
    assert encrypt(pt, k) == ct, f"Ошибка шифрования для варианта {var_no}"


def test_file_output_helpers(tmp_path):
    """Проверка функций форматирования и сохранения результатов в файл."""
    test_file = tmp_path / "test_enc.txt"
    record = format_encryption_record("тест", "ужуу", 1, is_decryption=False)
    save_result_to_file(str(test_file), record)

    assert test_file.exists()
    content = test_file.read_text(encoding="utf-8")
    assert "ШИФРОВАНИЕ" in content
    assert "КЛЮЧ: 1" in content
    assert "ужуу" in content
