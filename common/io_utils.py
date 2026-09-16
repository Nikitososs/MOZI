from typing import Any, List, Tuple
import os


def save_text_file(filepath: str, content: str) -> None:
    directory = os.path.dirname(filepath)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)


def read_text_file(filepath: str) -> str:
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def load_text_from_file_or_record(filepath: str, preferred_prefix: str = "") -> str:
    content = read_text_file(filepath).strip()
    if preferred_prefix:
        for line in content.splitlines():
            if ":" in line:
                key, _, val = line.partition(":")
                if preferred_prefix.upper() in key.upper():
                    return val.strip()
    return content


def format_encryption_record(
    text: str,
    result_text: str,
    key: Any,
    cipher_name: str = "ШИФР ЦЕЗАРЯ",
    is_decryption: bool = False
) -> str:
    op_name = "РАСШИФРОВАНИЕ" if is_decryption else "ШИФРОВАНИЕ"
    input_label = "ШИФР-ТЕКСТ (ШТ)" if is_decryption else "ОТКРЫТЫЙ ТЕКСТ (ОТ)"
    output_label = "РАСШИФРОВАННЫЙ ТЕКСТ (ОТ)" if is_decryption else "ЗАШИФРОВАННЫЙ ТЕКСТ (ШТ)"
    return (
        f"=== {op_name} ({cipher_name}) ===\n"
        f"КЛЮЧ: {key}\n"
        f"{input_label}: {text}\n"
        f"{output_label}: {result_text}\n"
    )


def format_bruteforce_records(
    ciphertext: str,
    variants: List[Tuple[Any, str]],
    title: str = "РЕЗУЛЬТАТЫ ПОЛНОГО ПЕРЕБОРА КЛЮЧЕЙ",
    key_label: str = "Ключ k"
) -> str:
    lines = [
        f"=== {title} ===",
        f"Исходный ШТ: {ciphertext}\n",
        f"{key_label:<8} | {'Расшифрованный текст'}",
        "-" * 80
    ]
    for k, dec_text in variants:
        lines.append(f"k = {str(k):<4} | {dec_text}")
    return "\n".join(lines) + "\n"


save_result_to_file = save_text_file
