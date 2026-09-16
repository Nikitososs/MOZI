import pytest
from common.io_utils import save_text_file, format_encryption_record, format_bruteforce_records
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
    brute_force
)


def test_alphabet_power_and_mapping(alphabet_info):
    assert alphabet_info["power"] == 32
    assert len(alphabet_info["symbols"]) == 32

    for char, expected_code in alphabet_info["table"].items():
        assert A(char) == expected_code
        assert A_inv(expected_code) == char

    assert A("ё") == 5
    assert A("е") == 5


def test_manual_example_encoding(manual_example):
    codes = [A(ch) for ch in manual_example["ot"]]
    assert codes == manual_example["codes"]


def test_manual_example_encryption(manual_example):
    encrypted = encrypt(manual_example["ot"], manual_example["key"])
    assert encrypted == manual_example["st"]


def test_manual_example_decryption(manual_example):
    decrypted = decrypt(manual_example["st"], manual_example["key"])
    assert decrypted == manual_example["ot"]


def test_manual_example_author_work(manual_example):
    encrypted = encrypt(manual_example["author_work_ot"], manual_example["key"])
    assert encrypted == manual_example["author_work_st"]


def test_canonical_text_preparation():
    raw_text = "А судьи кто?"
    assert prepare_canonical_text(raw_text) == "асудьикто"


def test_preserve_non_alphabet_symbols():
    raw_text = "привет, World! 123"
    encrypted = encrypt(raw_text, 1)
    assert encrypted == "рсйгжу, World! 123"
    assert decrypt(encrypted, 1) == raw_text


def test_variant_1_solution(variant_1_data):
    decrypted = decrypt(variant_1_data["ciphertext"], variant_1_data["key"])
    assert decrypted == variant_1_data["plaintext"]

    encrypted_author_work = encrypt(variant_1_data["author_work_ot"], variant_1_data["key"])
    assert encrypted_author_work == variant_1_data["author_work_st"]


def test_brute_force_contains_correct_key(variant_1_data):
    results = brute_force(variant_1_data["ciphertext"])
    assert len(results) == 31
    found = [text for k, text in results if k == variant_1_data["key"]]
    assert len(found) == 1
    assert found[0] == variant_1_data["plaintext"]


@pytest.mark.parametrize("var_no", list(range(1, 31)))
def test_all_database_variants(var_no, all_variants):
    data = all_variants[var_no]
    ct = data["ciphertext"]
    k = data["key"]
    pt = data["plaintext"]

    assert decrypt(ct, k) == pt
    assert encrypt(pt, k) == ct


def test_file_output_helpers(tmp_path):
    test_file = tmp_path / "test_enc.txt"
    record = format_encryption_record("тест", "ужуу", 1, is_decryption=False)
    save_text_file(str(test_file), record)

    assert test_file.exists()
    content = test_file.read_text(encoding="utf-8")
    assert "ШИФРОВАНИЕ" in content
    assert "КЛЮЧ: 1" in content
    assert "ужуу" in content
