import pytest
from common.io_utils import (
    save_text_file,
    format_encryption_record,
    format_bruteforce_records,
    load_text_from_file_or_record,
    extract_key_from_text
)
from lab_1.caesar_cipher import (
    Alphabet,
    EN_ALPHABET,
    get_alphabet,
    register_alphabet,
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
    assert encrypt(data["author_work_ot"], k) == data["author_work_st"]


def test_file_output_helpers(tmp_path):
    test_file = tmp_path / "test_enc.txt"
    record = format_encryption_record("тест", "ужуу", 1, is_decryption=False)
    save_text_file(str(test_file), record)

    assert test_file.exists()
    content = test_file.read_text(encoding="utf-8")
    assert "ШИФРОВАНИЕ" in content
    assert "КЛЮЧ: 1" in content
    assert "ужуу" in content
    # В шифрованном файле не должно быть открытого текста (только ключ и шифровка)
    assert "тест" not in content

    # Проверка чтения шифр-текста из созданной записи
    loaded_st = load_text_from_file_or_record(str(test_file), preferred_prefix="ЗАШИФРОВАННЫЙ ТЕКСТ")
    assert loaded_st == "ужуу"

    # Проверка автоматического извлечения ключа из файла
    assert extract_key_from_text(content) == 1

    # Проверка чтения открытого текста из записи расшифрования
    dec_file = tmp_path / "test_dec.txt"
    dec_record = format_encryption_record("ужуу", "тест", 1, is_decryption=True)
    save_text_file(str(dec_file), dec_record)
    loaded_ot = load_text_from_file_or_record(str(dec_file), preferred_prefix="РАСШИФРОВАННЫЙ ТЕКСТ")
    assert loaded_ot == "тест"

    # Проверка чтения обычного сырого файла
    raw_file = tmp_path / "raw.txt"
    raw_file.write_text("простой секретный текст\n", encoding="utf-8")
    assert load_text_from_file_or_record(str(raw_file)) == "простой секретный текст"


def test_english_alphabet_preset():
    en = get_alphabet("en")
    assert en.power == 26
    raw = "Hello, World!"
    enc = encrypt(raw, 3, alphabet=en)
    assert enc == "khoor, zruog!"
    dec = decrypt(enc, 3, alphabet=en)
    assert dec == "hello, world!"

    bf = brute_force("khoor", alphabet=en)
    assert len(bf) == 25
    found_plaintext = [text for k, text in bf if k == 3]
    assert found_plaintext == ["hello"]


def test_custom_alphabet_registration():
    custom = Alphabet(
        name="Digits (m=10)",
        symbols="0123456789"
    )
    register_alphabet("digits", custom)

    assert get_alphabet("digits").power == 10
    enc = encrypt("12345", 2, alphabet=custom)
    assert enc == "34567"
    assert decrypt(enc, 2, alphabet=custom) == "12345"

    bf = brute_force(enc, alphabet=custom)
    assert len(bf) == 9


def test_case_preservation_and_non_alphabet_symbols():
    raw_text = "Привет, World! 123"
    # 1. Режим сохранения регистра: буквы русского алфавита шифруются с сохранением регистра,
    # знаки препинания, пробелы, цифры и буквы других раскладок остаются нетронутыми
    enc_preserve = encrypt(raw_text, 1, case_mode="preserve")
    assert enc_preserve == "Рсйгжу, World! 123"
    assert decrypt(enc_preserve, 1, case_mode="preserve") == raw_text

    # 2. Режим приведения к нижнему регистру (сторонние символы не трогаем)
    enc_lower = encrypt(raw_text, 1, case_mode="lower")
    assert enc_lower == "рсйгжу, World! 123"

    # 3. Режим приведения к верхнему регистру (сторонние символы не трогаем)
    enc_upper = encrypt(raw_text, 1, case_mode="upper")
    assert enc_upper == "РСЙГЖУ, World! 123"


def test_english_case_preservation_with_cyrillic_symbols():
    en = get_alphabet("en")
    raw = "Hello, Мир! 456"
    enc = encrypt(raw, 3, alphabet=en, case_mode="preserve")
    assert enc == "Khoor, Мир! 456"
    assert decrypt(enc, 3, alphabet=en, case_mode="preserve") == raw


def test_russian_yo_case_preservation():
    raw = "Ёж и Медведь"
    enc = encrypt(raw, 1, case_mode="preserve")
    # 'Ё' -> 'е' (code 5) + 1 = 'ж' (code 6) -> 'Ж'
    assert enc.startswith("Жз")
    dec = decrypt(enc, 1, case_mode="preserve")
    assert dec == "Еж и Медведь"


