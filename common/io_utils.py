"""
Вспомогательный модуль для файловых операций и форматирования результатов.
Переиспользуется во всех лабораторных работах проекта МОЗИ.
"""

from typing import Any, List, Tuple
import os


def save_text_file(filepath: str, content: str) -> None:
    """Сохранение текстовых данных в файл в кодировке UTF-8."""
    directory = os.path.dirname(filepath)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)


def read_text_file(filepath: str) -> str:
    """Чтение текстовых данных из файла в кодировке UTF-8."""
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def format_encryption_record(
    text: str,
    result_text: str,
    key: Any,
    cipher_name: str = "ШИФР ЦЕЗАРЯ",
    is_decryption: bool = False
) -> str:
    """Форматирование записи шифрования/расшифрования для сохранения в файл."""
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
    """Форматирование таблицы перебора ключей для сохранения в файл."""
    lines = [
        f"=== {title} ===",
        f"Исходный ШТ: {ciphertext}\n",
        f"{key_label:<8} | {'Расшифрованный текст'}",
        "-" * 80
    ]
    for k, dec_text in variants:
        lines.append(f"k = {str(k):<4} | {dec_text}")
    return "\n".join(lines) + "\n"


# Псевдоним для обратной совместимости
save_result_to_file = save_text_file
