import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)

for path in (PROJECT_ROOT, CURRENT_DIR):
    if path not in sys.path:
        sys.path.insert(0, path)

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass
if sys.stdin.encoding and sys.stdin.encoding.lower() != "utf-8":
    try:
        sys.stdin.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

import caesar_cipher as cc
from common.io_utils import save_text_file, format_encryption_record, format_bruteforce_records
from variants import VARIANTS_DB

OUTPUTS_DIR = os.path.join(CURRENT_DIR, "outputs")
os.makedirs(OUTPUTS_DIR, exist_ok=True)


def print_banner() -> None:
    print("=" * 70)
    print("  ОмГТУ | Кафедра ПМиФИ | Дисциплина: МОЗИ")
    print("  ЛАБОРАТОРНАЯ РАБОТА № 1: ШИФР ЦЕЗАРЯ")
    print("  Студент: Смирнов Н. М. | Группа: ФИТ-242 | Вариант: 1")
    print("=" * 70)


def prompt_key(prompt_text: str = "Введите ключ k (1..31): ") -> int:
    while True:
        try:
            val = input(prompt_text).strip()
            if not val:
                print(">> Ошибка: ключ не может быть пустым.")
                continue
            k = int(val)
            if 1 <= k <= (cc.ALPHABET_POWER - 1):
                return k
            print(f">> Ошибка: ключ должен лежать в диапазоне от 1 до {cc.ALPHABET_POWER - 1}.")
        except ValueError:
            print(">> Ошибка: ключ должен быть целым числом.")


def handle_encrypt() -> None:
    print("\n--- 1. ШИФРОВАНИЕ ТЕКСТА ---")
    raw_text = input("Введите исходный текст: ").strip()
    if not raw_text:
        print(">> Текст пуст.")
        return

    print("Форматирование:")
    print("1 - Сохранить пробелы, знаки препинания и прочие символы (п. 2.1)")
    print("2 - Привести к каноническому виду методички (без пробелов/знаков)")
    fmt_choice = input("Выбор (1 или 2, по умолчанию 1): ").strip()
    filter_alpha = (fmt_choice == "2")

    key = prompt_key()
    ciphertext = cc.encrypt(raw_text, key, filter_non_alpha=filter_alpha)

    print(f"\nИсходный текст: {raw_text}")
    print(f"Ключ k:         {key}")
    print(f"Шифр-текст:     {ciphertext}")

    default_file = os.path.join(OUTPUTS_DIR, "encrypted.txt")
    save_file = input(f"Файл для сохранения [по умолчанию: {default_file}]: ").strip() or default_file

    record = format_encryption_record(raw_text, ciphertext, key, is_decryption=False)
    save_text_file(save_file, record)
    print(f">> Сохранено в: {save_file}")


def handle_decrypt() -> None:
    print("\n--- 2. РАСШИФРОВАНИЕ ТЕКСТА С ЗАДАННЫМ КЛЮЧОМ ---")
    ciphertext = input("Введите шифр-текст: ").strip()
    if not ciphertext:
        print(">> Текст пуст.")
        return

    key = prompt_key("Введите ключ k (1..31): ")
    plaintext = cc.decrypt(ciphertext, key)

    print(f"\nШифр-текст:         {ciphertext}")
    print(f"Ключ k:             {key}")
    print(f"Расшифрованный текст: {plaintext}")

    default_file = os.path.join(OUTPUTS_DIR, "decrypted.txt")
    save_file = input(f"Файл для сохранения [по умолчанию: {default_file}]: ").strip() or default_file

    record = format_encryption_record(ciphertext, plaintext, key, is_decryption=True)
    save_text_file(save_file, record)
    print(f">> Сохранено в: {save_file}")


def handle_bruteforce() -> None:
    print("\n--- 3. ПОЛНЫЙ ПЕРЕБОР КЛЮЧЕЙ (ВЗЛОМ) ---")
    ciphertext = input("Введите шифр-текст: ").strip()
    if not ciphertext:
        print(">> Текст пуст.")
        return

    variants = cc.brute_force(ciphertext)

    print("\nТаблица перебора (k = 1..31):")
    print(f"{'Ключ k':<8} | {'Расшифрованный текст'}")
    print("-" * 75)
    for k, dec_text in variants:
        print(f"k = {k:<4} | {dec_text}")

    default_file = os.path.join(OUTPUTS_DIR, "bruteforce_variants.txt")
    save_file = input(f"\nФайл для сохранения [по умолчанию: {default_file}]: ").strip() or default_file

    content = format_bruteforce_records(ciphertext, variants)
    save_text_file(save_file, content)
    print(f">> Таблица сохранена в: {save_file}")


def handle_variant_task() -> None:
    print("\n--- 4. ВЫПОЛНЕНИЕ ЗАДАНИЯ ПО ВАРИАНТУ (П. 2.3) ---")
    print("1 - Вариант № 1 (Смирнов Н. М., ФИТ-242)")
    print("2 - Другой вариант из методички (1–30)")
    print("3 - Произвольный шифр-текст")
    choice = input("Выбор [по умолчанию 1]: ").strip()

    var_num = 1
    custom_ct = None

    if choice == "2":
        while True:
            try:
                v = int(input("Номер варианта (1–30): ").strip())
                if 1 <= v <= 30:
                    var_num = v
                    break
                print(">> Допустимы варианты от 1 до 30.")
            except ValueError:
                print(">> Введите целое число.")
    elif choice == "3":
        custom_ct = input("Введите шифр-текст: ").strip()
        if not custom_ct:
            print(">> Текст пуст.")
            return

    if custom_ct is None:
        var_data = VARIANTS_DB[var_num]
        ciphertext = var_data["ciphertext"]
        expected_key = var_data["key"]
        expected_pt = var_data["plaintext"]
        author = var_data["author"]
        work = var_data["work"]
        author_work_ot = var_data["author_work_ot"]
        author_work_st = var_data["author_work_st"]
    else:
        ciphertext = custom_ct
        expected_key = None

    variants = cc.brute_force(ciphertext)
    print("\nРезультаты перебора ключей:")
    for k, dec_text in variants:
        marker = " <=== ИСТИННЫЙ ТЕКСТ" if (expected_key and k == expected_key) else ""
        print(f"k = {k:2d}: {dec_text[:65]}...{marker}")

    if expected_key is not None:
        key = expected_key
        plaintext = expected_pt
    else:
        key = prompt_key("\nУкажите истинный ключ k по результатам: ")
        plaintext = cc.decrypt(ciphertext, key)
        author = input("Автор произведения: ").strip()
        work = input("Название произведения: ").strip()
        author_work_ot = cc.prepare_canonical_text(f"{author}{work}")
        author_work_st = cc.encrypt(author_work_ot, key)

    print("\n" + "=" * 70)
    print("ИТОГОВЫЙ РЕЗУЛЬТАТ:")
    print(f"ШИФР-ТЕКСТ (ШТ):                       {ciphertext}")
    print(f"РАСШИФРОВАННЫЙ ТЕКСТ (ОТ):             {plaintext}")
    print(f"КЛЮЧ:                                  {key}")
    print(f"АВТОР И ПРОИЗВЕДЕНИЕ:                  {author}, «{work}»")
    print(f"АВТОР И ПРОИЗВЕДЕНИЕ (ОТ):             {author_work_ot}")
    print(f"ЗАШИФРОВАННЫЕ ФАМИЛИЯ И НАЗВАНИЕ (ШТ): {author_work_st}")
    print("=" * 70)

    res_file = os.path.join(OUTPUTS_DIR, f"variant_{var_num}_solution.txt")
    out_lines = [
        f"ОТЧЕТНЫЙ РЕЗУЛЬТАТ ПО ВАРИАНТУ № {var_num}",
        f"Студент: Смирнов Н. М., группа ФИТ-242\n",
        f"ШИФР-ТЕКСТ (ШТ): {ciphertext}",
        f"РАСШИФРОВАННЫЙ ТЕКСТ (ОТ): {plaintext}",
        f"КЛЮЧ: {key}",
        f"АВТОР И ПРОИЗВЕДЕНИЕ: {author}, «{work}»",
        f"АВТОР И ПРОИЗВЕДЕНИЕ (ОТ): {author_work_ot}",
        f"ЗАШИФРОВАННЫЕ ФАМИЛИЯ И НАЗВАНИЕ (ШТ): {author_work_st}\n",
        "Таблица перебора ключей:",
    ]
    for k, dec_text in variants:
        out_lines.append(f"k = {k:2d}: {dec_text}")

    save_text_file(res_file, "\n".join(out_lines) + "\n")
    print(f">> Результат сохранен в: {res_file}")


def main() -> None:
    print_banner()
    while True:
        print("\nГЛАВНОЕ МЕНЮ:")
        print("1. Зашифровать текст (п. 2.1)")
        print("2. Расшифровать текст с известным ключом (п. 2.2)")
        print("3. Расшифровать текст полным перебором всех 31 ключей (п. 2.2)")
        print("4. Выполнить задание по варианту (криптоанализ цитаты, п. 2.3)")
        print("0. Выход")

        choice = input("\nВыберите действие (0-4): ").strip()
        if choice == "1":
            handle_encrypt()
        elif choice == "2":
            handle_decrypt()
        elif choice == "3":
            handle_bruteforce()
        elif choice == "4":
            handle_variant_task()
        elif choice == "0":
            print("\nЗавершение работы программы.")
            break
        else:
            print(">> Некорректный выбор. Введите цифру от 0 до 4.")


if __name__ == "__main__":
    main()
