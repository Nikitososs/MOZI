import os
import sys
from typing import Optional, Tuple

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
from common.io_utils import (
    save_text_file,
    read_text_file,
    format_encryption_record,
    format_bruteforce_records,
    load_text_from_file_or_record,
    extract_key_from_text
)
from variants import VARIANTS_DB

OUTPUTS_DIR = os.path.join(CURRENT_DIR, "outputs")
os.makedirs(OUTPUTS_DIR, exist_ok=True)

current_alphabet: cc.Alphabet = cc.DEFAULT_ALPHABET


def clear_screen() -> None:
    if sys.stdout.isatty():
        os.system("cls" if os.name == "nt" else "clear")


def pause_and_return() -> None:
    input("\nНажмите Enter, чтобы вернуться в меню...")


def print_banner() -> None:
    print("=" * 70)
    print("  ОмГТУ | Кафедра ПМиФИ | Дисциплина: МОЗИ")
    print("  ЛАБОРАТОРНАЯ РАБОТА № 1: ШИФР ЦЕЗАРЯ")
    print("  Студент: Смирнов Н. М. | Группа: ФИТ-242 | Вариант: 1")
    print("=" * 70)


def prompt_text_source_with_key(
    prompt_label: str,
    record_hint: str = "",
    default_filepath: str = ""
) -> Tuple[str, Optional[int]]:
    print(f"\nСпособ ввода ({prompt_label}):")
    print("1 - Ввести вручную с клавиатуры")
    print("2 - Прочитать из файла")
    src_choice = input("Выбор (1/2, по умолчанию 1): ").strip()
    if src_choice == "2":
        hint = f" [по умолчанию: {default_filepath}]" if default_filepath else ""
        filepath = input(f"Путь к файлу{hint}: ").strip() or default_filepath
        if not filepath:
            print(">> Ошибка: путь не может быть пустым.")
            return "", None
        if not os.path.isfile(filepath):
            print(f">> Ошибка: файл '{filepath}' не найден.")
            return "", None
        try:
            raw_content = read_text_file(filepath)
            content = load_text_from_file_or_record(filepath, record_hint)
            key = extract_key_from_text(raw_content)
            if not content:
                print(">> Ошибка: файл пуст.")
                return "", None
            preview = content if len(content) <= 60 else content[:57] + "..."
            key_info = f", обнаружен ключ k={key}" if key is not None else ""
            print(f">> Успешно прочитано ({len(content)} симв.{key_info}): {preview}")
            return content, key
        except Exception as e:
            print(f">> Ошибка при чтении файла: {e}")
            return "", None
    else:
        text = input(f"Введите {prompt_label}: ")
        if not text.strip():
            print(">> Ошибка: введен пустой текст.")
            return "", None
        return text.rstrip("\r\n"), None


def prompt_text_source(prompt_label: str, record_hint: str = "", default_filepath: str = "") -> str:
    text, _ = prompt_text_source_with_key(prompt_label, record_hint, default_filepath=default_filepath)
    return text


def prompt_case_mode(is_encryption: bool = True) -> Tuple[str, bool]:
    op_label = "шифрования" if is_encryption else "расшифрования"
    print(f"\nРежим обработки регистра и символов ({op_label}):")
    print("1 - Оставить как есть (сохранять регистр букв; сторонние символы не трогать)")
    print("2 - Привести к одному регистру (к нижнему регистру; сторонние символы не трогать)")
    print("3 - Канонический вид (только буквы алфавита в нижнем регистре, удалить пробелы и знаки)")
    choice = input("Выбор (1/2/3, по умолчанию 1): ").strip()
    if choice == "2":
        return "lower", False
    elif choice == "3":
        return "lower", True
    return "preserve", False


def inspect_and_prepare_text(
    text: str,
    alpha: cc.Alphabet,
    filter_alpha: bool = False
) -> Optional[str]:
    clean_text = text.rstrip("\r\n")
    if not clean_text:
        print(">> Ошибка: входной текст пуст.")
        return None

    alpha_chars_count = sum(1 for ch in clean_text if alpha.normalize_char(ch) in alpha.char_to_code)
    total_chars = len(clean_text)
    non_alpha_count = total_chars - alpha_chars_count

    if alpha_chars_count == 0:
        print(f"\n>> Предупреждение: ни один символ введенного текста не принадлежит алфавиту '{alpha.name}'.")
        print(">> Возможно, выбрана неверная раскладка или требуется сменить алфавит (пункт 5 меню).")
        if filter_alpha:
            print(">> Ошибка: в каноническом режиме результат будет пустым.")
            return None
        confirm = input("Продолжить операцию без изменений? (y/n, по умолчанию n): ").strip().lower()
        if confirm not in ("y", "yes", "да"):
            return None
        return clean_text

    if filter_alpha:
        if non_alpha_count > 0:
            print(f">> Инфо: отфильтровано {non_alpha_count} спецсимволов/пробелов вне алфавита.")
        canonical = alpha.prepare_canonical_text(clean_text)
        if not canonical:
            print(">> Ошибка: после канонической фильтрации текст пуст.")
            return None
        return canonical

    if non_alpha_count > 0:
        print(f">> Инфо: {alpha_chars_count} симв. из алфавита '{alpha.name}' будут обработаны, {non_alpha_count} сторонних символов (знаки/цифры/иные раскладки) останутся без изменений.")

    return clean_text


def prompt_key(alpha: cc.Alphabet, prompt_text: str = "", default_key: Optional[int] = None) -> int:
    m = alpha.power
    max_k = m - 1
    if not prompt_text:
        if default_key is not None:
            default_eff = default_key % m
            prompt_text = f"Введите ключ k (1..{max_k}, Enter для {default_eff}): "
        else:
            prompt_text = f"Введите ключ k (1..{max_k}): "
    while True:
        try:
            val = input(prompt_text).strip()
            if not val:
                if default_key is not None:
                    k = default_key
                else:
                    print(">> Ошибка: ключ не может быть пустым.")
                    continue
            else:
                k = int(val)

            k_eff = k % m

            if k_eff == 0:
                print(f"\n>> Предупреждение: введенный ключ k = {k} кратен мощности алфавита m = {m} ({k} ≡ 0 mod {m}).")
                print(">> При сдвиге на 0 текст останется неизменным (тождественное преобразование).")
                confirm = input("Продолжить с нулевым сдвигом? (y/n, по умолчанию n): ").strip().lower()
                if confirm in ("y", "yes", "да"):
                    return 0
                continue

            if k != k_eff:
                print(f"\n>> Уведомление: введен ключ k = {k}, превышающий мощность алфавита m = {m} (или выходящий за [1..{max_k}]).")
                print(f">> Выполнено приведение по модулю: {k} ≡ {k_eff} (mod {m}).")
                print(f">> Шифрование будет производиться с числом, сравнимым с ключом по модулю {m} (k = {k_eff}).\n")
                return k_eff

            return k
        except ValueError:
            print(">> Ошибка: ключ должен быть целым числом.")


def handle_encrypt() -> None:
    print("\n--- 1. ШИФРОВАНИЕ ТЕКСТА ---")
    default_src = os.path.join(OUTPUTS_DIR, "plaintext.txt")
    raw_text = prompt_text_source(
        "исходный текст",
        record_hint="ОТКРЫТЫЙ ТЕКСТ",
        default_filepath=default_src if os.path.isfile(default_src) else ""
    )
    if not raw_text:
        return

    case_mode, filter_alpha = prompt_case_mode(is_encryption=True)

    prepared_text = inspect_and_prepare_text(raw_text, current_alphabet, filter_alpha=filter_alpha)
    if prepared_text is None:
        return

    key = prompt_key(current_alphabet)
    ciphertext = cc.encrypt(
        prepared_text,
        key,
        filter_non_alpha=False,
        alphabet=current_alphabet,
        case_mode=case_mode
    )

    print(f"\nАлфавит:        {current_alphabet.name}")
    print(f"Исходный текст: {prepared_text}")
    print(f"Ключ k:         {key}")
    print(f"Шифр-текст:     {ciphertext}")

    default_file = os.path.join(OUTPUTS_DIR, "encrypted.txt")
    save_file = input(f"Файл для сохранения [по умолчанию: {default_file}]: ").strip() or default_file

    record = format_encryption_record(prepared_text, ciphertext, key, is_decryption=False)
    save_text_file(save_file, record)
    print(f">> Сохранено в: {save_file}")


def handle_decrypt() -> None:
    print("\n--- 2. РАСШИФРОВАНИЕ ТЕКСТА ---")
    default_src = os.path.join(OUTPUTS_DIR, "encrypted.txt")
    ciphertext, file_key = prompt_text_source_with_key(
        "шифр-текст",
        record_hint="ШИФР-ТЕКСТ",
        default_filepath=default_src if os.path.isfile(default_src) else ""
    )
    if not ciphertext:
        return

    case_mode, filter_alpha = prompt_case_mode(is_encryption=False)

    prepared_ct = inspect_and_prepare_text(ciphertext, current_alphabet, filter_alpha=filter_alpha)
    if prepared_ct is None:
        return

    if file_key is not None:
        key = prompt_key(current_alphabet, default_key=file_key)
    else:
        key = prompt_key(current_alphabet)

    plaintext = cc.decrypt(prepared_ct, key, alphabet=current_alphabet, case_mode=case_mode)

    print(f"\nАлфавит:              {current_alphabet.name}")
    print(f"Шифр-текст:           {prepared_ct}")
    print(f"Ключ k:               {key}")
    print(f"Расшифрованный текст: {plaintext}")

    default_file = os.path.join(OUTPUTS_DIR, "decrypted.txt")
    save_file = input(f"Файл для сохранения [по умолчанию: {default_file}]: ").strip() or default_file

    record = format_encryption_record(prepared_ct, plaintext, key, is_decryption=True)
    save_text_file(save_file, record)
    print(f">> Сохранено в: {save_file}")


def handle_bruteforce() -> None:
    print("\n--- 3. ПОЛНЫЙ ПЕРЕБОР КЛЮЧЕЙ (ВЗЛОМ) ---")
    default_src = os.path.join(OUTPUTS_DIR, "encrypted.txt")
    ciphertext = prompt_text_source(
        "шифр-текст",
        record_hint="ЗАШИФРОВАННЫЙ ТЕКСТ",
        default_filepath=default_src if os.path.isfile(default_src) else ""
    )
    if not ciphertext:
        return

    case_mode, filter_alpha = prompt_case_mode(is_encryption=False)

    prepared_ct = inspect_and_prepare_text(ciphertext, current_alphabet, filter_alpha=filter_alpha)
    if prepared_ct is None:
        return

    variants = cc.brute_force(prepared_ct, alphabet=current_alphabet, case_mode=case_mode)

    print(f"\nТаблица перебора (k = 1..{current_alphabet.power - 1}, {current_alphabet.name}):")
    print(f"{'Ключ k':<8} | {'Расшифрованный текст'}")
    print("-" * 75)
    for k, dec_text in variants:
        print(f"k = {k:<4} | {dec_text}")

    default_file = os.path.join(OUTPUTS_DIR, "bruteforce_variants.txt")
    save_file = input(f"\nФайл для сохранения [по умолчанию: {default_file}]: ").strip() or default_file

    content = format_bruteforce_records(prepared_ct, variants)
    save_text_file(save_file, content)
    print(f">> Таблица сохранена в: {save_file}")


def handle_variant_task() -> None:
    print("\n--- 4. ЗАДАНИЕ ПО ВАРИАНТУ ---")
    print("1 - Вариант № 1 (Смирнов Н. М., ФИТ-242)")
    print("2 - Другой вариант из базы (1–30)")
    print("3 - Прочитать шифр-текст из файла")
    print("4 - Ввести произвольный шифр-текст с клавиатуры")
    choice = input("Выбор [по умолчанию 1]: ").strip()

    var_num = 1
    custom_ct = None
    default_src = os.path.join(OUTPUTS_DIR, "encrypted.txt")

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
        hint = f" [по умолчанию: {default_src}]" if os.path.isfile(default_src) else ""
        filepath = input(f"Путь к файлу с шифр-текстом{hint}: ").strip() or (default_src if os.path.isfile(default_src) else "")
        if not filepath:
            print(">> Ошибка: путь не может быть пустым.")
            return
        if not os.path.isfile(filepath):
            print(f">> Ошибка: файл '{filepath}' не найден.")
            return
        try:
            loaded_ct = load_text_from_file_or_record(filepath, "ШИФР-ТЕКСТ")
            if not loaded_ct:
                print(">> Ошибка: файл пуст.")
                return
            preview = loaded_ct if len(loaded_ct) <= 60 else loaded_ct[:57] + "..."
            print(f">> Успешно прочитано ({len(loaded_ct)} симв.): {preview}")
            custom_ct = inspect_and_prepare_text(loaded_ct, cc.get_alphabet("ru"), filter_alpha=False)
            if not custom_ct:
                return
        except Exception as e:
            print(f">> Ошибка при чтении файла: {e}")
            return
    elif choice == "4":
        text = input("Введите шифр-текст: ")
        if not text.strip():
            print(">> Ошибка: введен пустой текст.")
            return
        custom_ct = inspect_and_prepare_text(text.rstrip("\r\n"), cc.get_alphabet("ru"), filter_alpha=False)
        if not custom_ct:
            return

    # Задания вариантов методички используют русский алфавит m=32
    ru_alpha = cc.get_alphabet("ru")

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

    variants = cc.brute_force(ciphertext, alphabet=ru_alpha)
    print("\nРезультаты перебора ключей:")
    for k, dec_text in variants:
        marker = " <=== ИСТИННЫЙ ТЕКСТ" if (expected_key and k == expected_key) else ""
        print(f"k = {k:2d}: {dec_text[:65]}...{marker}")

    if expected_key is not None:
        key = expected_key
        plaintext = expected_pt
    else:
        key = prompt_key(ru_alpha, "\nУкажите истинный ключ k по результатам: ")
        plaintext = cc.decrypt(ciphertext, key, alphabet=ru_alpha)
        author = input("Автор произведения: ").strip()
        work = input("Название произведения: ").strip()
        author_work_ot = ru_alpha.prepare_canonical_text(f"{author}{work}")
        author_work_st = ru_alpha.encrypt(author_work_ot, key)

    print("\n" + "=" * 70)
    print("ИТОГОВЫЙ РЕЗУЛЬТАТ:")
    print(f"ШИФР-ТЕКСТ (ШТ):                       {ciphertext}")
    print(f"РАСШИФРОВАННЫЙ ТЕКСТ (ОТ):             {plaintext}")
    print(f"КЛЮЧ:                                  {key}")
    print(f"АВТОР И ПРОИЗВЕДЕНИЕ:                  {author}, «{work}»")
    print(f"АВТОР И ПРОИЗВЕДЕНИЕ (ОТ):             {author_work_ot}")
    print(f"ЗАШИФРОВАННЫЕ ФАМИЛИЯ И НАЗВАНИЕ (ШТ): {author_work_st}")
    print("=" * 70)

    default_name = f"variant_{var_num}_solution.txt" if custom_ct is None else "variant_custom_solution.txt"
    default_res_file = os.path.join(OUTPUTS_DIR, default_name)
    save_file = input(f"\nФайл для сохранения отчета [по умолчанию: {default_res_file}]: ").strip() or default_res_file

    var_title = f"ВАРИАНТУ № {var_num}" if custom_ct is None else "ПОЛЬЗОВАТЕЛЬСКОМУ ШИФР-ТЕКСТУ"
    out_lines = [
        f"ОТЧЕТНЫЙ РЕЗУЛЬТАТ ПО {var_title}",
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

    save_text_file(save_file, "\n".join(out_lines) + "\n")
    print(f">> Результат сохранен в: {save_file}")

    save_cipher = input("Сохранить зашифрованную строку (автор/произведение) в отдельный файл? (y/n, по умолчанию n): ").strip().lower()
    if save_cipher in ("y", "yes", "да"):
        default_cipher_file = os.path.join(OUTPUTS_DIR, f"variant_{var_num}_cipher.txt" if custom_ct is None else "variant_custom_cipher.txt")
        save_cf = input(f"Файл для сохранения шифровки [по умолчанию: {default_cipher_file}]: ").strip() or default_cipher_file
        cipher_rec = format_encryption_record(author_work_ot, author_work_st, key, is_decryption=False)
        save_text_file(save_cf, cipher_rec)
        print(f">> Шифр-текст сохранен в: {save_cf}")


def handle_change_alphabet() -> None:
    global current_alphabet
    print("\n--- 5. ВЫБОР АЛФАВИТА ---")
    print(f"Текущий активный алфавит: {current_alphabet.name}")
    print("\nДоступные пресеты:")
    presets_list = list(cc.PRESETS.items())
    for idx, (code, alpha) in enumerate(presets_list, 1):
        active_mark = " (активен)" if alpha == current_alphabet else ""
        print(f"{idx} - [{code}] {alpha.name}{active_mark}")
    print(f"{len(presets_list) + 1} - Добавить собственный алфавит")

    choice = input("\nВыберите вариант: ").strip()
    try:
        choice_idx = int(choice)
        if 1 <= choice_idx <= len(presets_list):
            selected_code, selected_alpha = presets_list[choice_idx - 1]
            current_alphabet = selected_alpha
            print(f">> Активный алфавит переключен на: {current_alphabet.name}")
            return
        elif choice_idx == len(presets_list) + 1:
            name = input("Название алфавита (например, Digits): ").strip()
            code = input("Краткий код (например, digits): ").strip().lower()
            symbols = input("Символы алфавита без пробелов (например, 0123456789): ").strip()
            if not symbols:
                print(">> Ошибка: символы не могут быть пустыми.")
                return
            new_alpha = cc.Alphabet(name=f"{name} (m={len(symbols)})", symbols=symbols)
            cc.register_alphabet(code or name.lower(), new_alpha)
            current_alphabet = new_alpha
            print(f">> Алфавит зарегистрирован и активирован: {new_alpha.name}")
            return
    except ValueError:
        pass
    print(">> Некорректный выбор.")


def main() -> None:
    while True:
        clear_screen()
        print_banner()
        print(f"\nГЛАВНОЕ МЕНЮ [{current_alphabet.name}]:")
        print("1. Зашифровать текст")
        print("2. Расшифровать текст по ключу")
        print("3. Взломать шифр (полный перебор)")
        print("4. Выполнить задание по варианту")
        print("5. Сменить алфавит (ru / en / свой)")
        print("0. Выход")

        choice = input("\nВыберите действие (0-5): ").strip()
        if choice == "1":
            clear_screen()
            print_banner()
            handle_encrypt()
            pause_and_return()
        elif choice == "2":
            clear_screen()
            print_banner()
            handle_decrypt()
            pause_and_return()
        elif choice == "3":
            clear_screen()
            print_banner()
            handle_bruteforce()
            pause_and_return()
        elif choice == "4":
            clear_screen()
            print_banner()
            handle_variant_task()
            pause_and_return()
        elif choice == "5":
            clear_screen()
            print_banner()
            handle_change_alphabet()
            pause_and_return()
        elif choice == "0":
            print("\nЗавершение работы программы.")
            break
        else:
            print(">> Некорректный выбор. Введите цифру от 0 до 5.")
            pause_and_return()


if __name__ == "__main__":
    main()
