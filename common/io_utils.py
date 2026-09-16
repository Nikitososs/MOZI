from typing import Any, List, Optional, Tuple
import os


def save_text_file(filepath: str, content: str) -> None:
    directory = os.path.dirname(filepath)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)


def read_text_file(filepath: str) -> str:
    try:
        with open(filepath, "r", encoding="utf-8-sig") as f:
            return f.read()
    except UnicodeDecodeError:
        with open(filepath, "r", encoding="cp1251") as f:
            return f.read()


def extract_key_from_text(content: str) -> Optional[int]:
    for line in content.splitlines():
        if ":" in line:
            key, _, val = line.partition(":")
            if "КЛЮЧ" in key.upper():
                try:
                    return int(val.strip())
                except ValueError:
                    pass
    return None


def load_text_from_file_or_record(filepath: str, preferred_prefix: str = "") -> str:
    content = read_text_file(filepath).rstrip("\r\n")
    if preferred_prefix:
        pref = preferred_prefix.upper()
        # 1. Прямой поиск префикса
        for line in content.splitlines():
            if ":" in line:
                key, _, val = line.partition(":")
                if pref in key.upper():
                    return val[1:] if val.startswith(" ") else val

        # 2. Нестрогий поиск открытого/расшифрованного текста
        if any(w in pref for w in ["ОТКРЫТ", "РАСШИФР"]):
            for line in content.splitlines():
                if ":" in line:
                    key, _, val = line.partition(":")
                    ku = key.upper()
                    if "ОТКРЫТ" in ku or "РАСШИФР" in ku:
                        return val[1:] if val.startswith(" ") else val

        # 3. Нестрогий поиск шифр-текста / зашифрованного текста
        if "ЗАШИФР" in pref or ("ШИФР" in pref and "РАСШИФР" not in pref):
            for line in content.splitlines():
                if ":" in line:
                    key, _, val = line.partition(":")
                    ku = key.upper()
                    if "РАСШИФР" not in ku and ("ШИФР" in ku or "ЗАШИФР" in ku):
                        return val[1:] if val.startswith(" ") else val

    return content


def format_encryption_record(
    text: str,
    result_text: str,
    key: Any,
    cipher_name: str = "ШИФР ЦЕЗАРЯ",
    is_decryption: bool = False
) -> str:
    if not is_decryption:
        # В шифрованном файле хранятся только ключ и результат шифрования (шифровка)
        return (
            f"=== ШИФРОВАНИЕ ({cipher_name}) ===\n"
            f"КЛЮЧ: {key}\n"
            f"ШИФР-ТЕКСТ (ШТ): {result_text}\n"
        )
    return (
        f"=== РАСШИФРОВАНИЕ ({cipher_name}) ===\n"
        f"КЛЮЧ: {key}\n"
        f"ШИФР-ТЕКСТ (ШТ): {text}\n"
        f"РАСШИФРОВАННЫЙ ТЕКСТ (ОТ): {result_text}\n"
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
