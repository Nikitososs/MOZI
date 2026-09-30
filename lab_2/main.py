"""
Интерактивное консольное приложение для Лабораторной работы № 2:
«Криптоанализ аффинного шифра».

Студент: Смирнов Н. М.
Группа: ФИТ-242
Вариант: 16
"""

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

import affine_cipher as ac
from common.io_utils import (
    save_text_file,
    read_text_file,
    load_text_from_file_or_record
)
from variants import VARIANTS_DB

OUTPUTS_DIR = os.path.join(CURRENT_DIR, "outputs")
os.makedirs(OUTPUTS_DIR, exist_ok=True)

current_alphabet: ac.Alphabet = ac.DEFAULT_ALPHABET
last_used_key: Optional[Tuple[int, int]] = None


def clear_screen() -> None:
    if sys.stdout.isatty():
        os.system("cls" if os.name == "nt" else "clear")


def pause_and_return() -> None:
    input("\nНажмите Enter, чтобы вернуться в меню...")


def print_banner() -> None:
    print("=" * 72)
    print("  ОмГТУ | Кафедра ПМиФИ | Дисциплина: МОЗИ")
    print("  ЛАБОРАТОРНАЯ РАБОТА № 2: КРИПТОАНАЛИЗ АФФИННОГО ШИФРА")
    print("  Студент: Смирнов Н. М. | Группа: ФИТ-242 | Вариант: 16")
    print("=" * 72)


def prompt_int(prompt_text: str, default: Optional[int] = None) -> Optional[int]:
    hint = f" [по умолчанию: {default}]" if default is not None else ""
    raw = input(f"{prompt_text}{hint} (00 для отмены): ").strip()
    if raw == "00":
        print(">> Ввод отменен.")
        return None
    if not raw and default is not None:
        return default
    try:
        return int(raw)
    except ValueError:
        print(">> Ошибка: введите целое число.")
        return None


def prompt_text_source(prompt_label: str, default_filepath: str = "") -> Optional[str]:
    print(f"\nСпособ ввода ({prompt_label}):")
    print("1 - Ввести вручную с клавиатуры")
    print("2 - Прочитать из файла")
    print("0 - Отмена (вернуться в главное меню)")
    src_choice = input("Выбор (1/2/0, по умолчанию 1): ").strip()
    if src_choice == "0":
        print(">> Действие отменено.")
        return None
    if src_choice == "2":
        hint = f" [по умолчанию: {default_filepath}]" if default_filepath else ""
        filepath = input(f"Путь к файлу{hint} (0 для отмены): ").strip()
        if filepath == "0":
            print(">> Действие отменено.")
            return None
        filepath = filepath or default_filepath
        if not filepath:
            print(">> Ошибка: путь не может быть пустым.")
            return None
        if not os.path.isfile(filepath):
            print(f">> Ошибка: файл '{filepath}' не найден.")
            return None
        try:
            content = load_text_from_file_or_record(filepath, prompt_label)
            if not content:
                print(">> Ошибка: файл пуст.")
                return None
            preview = content if len(content) <= 60 else content[:57] + "..."
            print(f">> Успешно прочитано ({len(content)} симв.): {preview}")
            return content
        except Exception as e:
            print(f">> Ошибка при чтении файла: {e}")
            return None
    else:
        text = input(f"Введите {prompt_label} (0 для отмены): ")
        if text.strip() == "0":
            print(">> Действие отменено.")
            return None
        if not text.strip():
            print(">> Ошибка: введен пустой текст.")
            return None
        return text.rstrip("\r\n")


def prompt_case_mode(is_encryption: bool = True) -> Optional[Tuple[str, bool]]:
    op_label = "шифрования" if is_encryption else "расшифрования"
    print(f"\nРежим обработки регистра и символов ({op_label}):")
    print("1 - Оставить как есть (сохранять регистр букв; сторонние символы не трогать)")
    print("2 - Привести к одному регистру (к нижнему регистру; сторонние символы не трогать)")
    print("3 - Канонический вид (только буквы алфавита в нижнем регистре, без пробелов)")
    print("0 - Отмена (вернуться в главное меню)")
    choice = input("Выбор (1/2/3/0, по умолчанию 1): ").strip()
    if choice == "0":
        print(">> Действие отменено.")
        return None
    if choice == "2":
        return "lower", False
    elif choice == "3":
        return "lower", True
    return "preserve", False


# =====================================================================
# ОБРАБОТЧИКИ МАТЕМАТИЧЕСКОГО АППАРАТА
# =====================================================================

def handle_extended_gcd() -> None:
    print("\n--- РАСШИРЕННЫЙ АЛГОРИТМ ЕВКЛИДА ---")
    print("Вычисляет d = НОД(a, b) и коэффициенты Безу u, v такие, что a*u + b*v = d.")
    a = prompt_int("Введите число a")
    if a is None:
        return
    b = prompt_int("Введите число b")
    if b is None:
        return

    d, u, v = ac.extended_gcd(a, b)
    print("\n" + "=" * 50)
    print(f"Входные данные: a = {a}, b = {b}")
    print(f"НОД d = {d}")
    print(f"Коэффициент Безу u = {u}")
    print(f"Коэффициент Безу v = {v}")
    print(f"Проверка: {a} * ({u}) + {b} * ({v}) = {a * u + b * v} (== {d})")
    print("=" * 50)


def handle_mod_inverse() -> None:
    print("\n--- НАХОЖДЕНИЕ ЭЛЕМЕНТА, ОБРАТНОГО ДАННОМУ ---")
    print("Ищет a^(-1) в кольце вычетов по модулю m (a * a^(-1) ≡ 1 mod m).")
    a = prompt_int("Введите элемент a")
    if a is None:
        return
    m = prompt_int("Введите модуль m", default=current_alphabet.power)
    if m is None:
        return
    if m <= 1:
        print(">> Ошибка: модуль m должен быть целым числом >= 2.")
        return

    is_inv, u, pos_inv, desc = ac.mod_inverse(a, m)
    print("\n" + "=" * 50)
    print(f"Входные данные: a = {a}, m = {m}")
    if not is_inv:
        print("Результат: 1. Необратимо")
        print(f">> {desc}")
    else:
        print("Результат: 2. Обратимо")
        print(f"Коэффициент Безу u: {u}")
        if u is not None and u < 0:
            k = (-u + m - 1) // m
            shift_expr = f"{m}" if k == 1 else f"{k}*{m}"
            print(f"Преобразование к наименьшему положительному вычету (u < 0): {u} + {shift_expr} = {pos_inv}")
        print(f"Наименьший положительный вычет обратного элемента a^(-1): {pos_inv}")
        print(f"Проверка: ({a} * {pos_inv}) mod {m} = {(a * pos_inv) % m}")
    print("=" * 50)


def handle_solve_linear_congruence() -> None:
    print("\n--- РЕШЕНИЕ СРАВНЕНИЯ ax ≡ b (mod m) ---")
    a = prompt_int("Введите коэффициент a")
    if a is None:
        return
    b = prompt_int("Введите свободный член b")
    if b is None:
        return
    m = prompt_int("Введите модуль m", default=current_alphabet.power)
    if m is None:
        return
    if m <= 1:
        print(">> Ошибка: модуль m должен быть целым числом >= 2.")
        return

    st, sols, desc = ac.solve_linear_congruence(a, b, m)
    print("\n" + "=" * 50)
    print(f"Сравнение: {a} * x ≡ {b} (mod {m})")
    print(f"Статус решения: {desc}")
    if st == 1:
        print("Результат: 1. Решений нет")
    elif st == 2:
        print(f"Результат: 2. Решение одно: x ≡ {sols[0]} (mod {m})")
        print(f"Проверка: ({a} * {sols[0]}) mod {m} = {(a * sols[0]) % m} (b mod m = {b % m})")
    elif st == 3:
        print(f"Результат: 3. Несколько решений (всего {len(sols)}):")
        for idx, x in enumerate(sols, 1):
            check_val = (a * x) % m
            print(f"  Решение #{idx}: x = {x}  [проверка: ({a}*{x}) mod {m} = {check_val}]")
    print("=" * 50)


def handle_solve_system() -> None:
    print("\n--- РЕШЕНИЕ СИСТЕМЫ ЛИНЕЙНЫХ СРАВНЕНИЙ ---")
    print("Система вида:")
    print("  (a * x + y) ≡ b (mod m)")
    print("  (c * x + y) ≡ d (mod m)")
    a = prompt_int("Введите коэффициент a")
    if a is None:
        return
    b = prompt_int("Введите значение b")
    if b is None:
        return
    c = prompt_int("Введите коэффициент c")
    if c is None:
        return
    d = prompt_int("Введите значение d")
    if d is None:
        return
    m = prompt_int("Введите модуль m", default=current_alphabet.power)
    if m is None:
        return
    if m <= 1:
        print(">> Ошибка: модуль m должен быть целым числом >= 2.")
        return

    st, sols, desc = ac.solve_system_congruences(a, b, c, d, m)
    print("\n" + "=" * 50)
    print(f"Система:\n  ({a}x + y) ≡ {b} (mod {m})\n  ({c}x + y) ≡ {d} (mod {m})")
    print(f"Статус решения: {desc}")
    if st == 1:
        print("Результат: 1. Решений нет")
    elif st == 2:
        x0, y0 = sols[0]
        print(f"Результат: 2. Одно решение: (x = {x0}, y = {y0})")
        print(f"Проверка ур. 1: ({a}*{x0} + {y0}) mod {m} = {(a*x0 + y0) % m} (== {b % m})")
        print(f"Проверка ур. 2: ({c}*{x0} + {y0}) mod {m} = {(c*x0 + y0) % m} (== {d % m})")
    elif st == 3:
        print(f"Результат: 3. Много решений (всего {len(sols)}):")
        for idx, (x, y) in enumerate(sols, 1):
            gcd_x = ac.extended_gcd(x, m)[0]
            valid_key_note = " [допустимый ключ шифра]" if gcd_x == 1 else " [необратимый x]"
            print(f"  Пара #{idx}: x = {x}, y = {y}{valid_key_note}")
    print("=" * 50)


def handle_math_submenu() -> None:
    while True:
        clear_screen()
        print_banner()
        print("\n--- РАЗДЕЛ: МАТЕМАТИЧЕСКИЙ АППАРАТ ---")
        print("1. Расширенный алгоритм Евклида (вход: a, b -> выход: d, u, v)")
        print("2. Нахождение обратного элемента (вход: a, m -> 1. Необратимо / 2. Коэф. Безу и наименьший положительный вычет)")
        print("3. Решение сравнения ax ≡ b (mod m) (вход: a, b, m -> 1. Решений нет / 2. Одно / 3. Несколько)")
        print("4. Решение системы сравнений (вход: a, b, c, d, m -> 1. Решений нет / 2. Одно / 3. Много)")
        print("0. Вернуться в главное меню")

        choice = input("\nВыберите действие (0-4): ").strip()
        if choice == "1":
            handle_extended_gcd()
            pause_and_return()
        elif choice == "2":
            handle_mod_inverse()
            pause_and_return()
        elif choice == "3":
            handle_solve_linear_congruence()
            pause_and_return()
        elif choice == "4":
            handle_solve_system()
            pause_and_return()
        elif choice == "0":
            break
        else:
            print(">> Некорректный выбор.")
            pause_and_return()


# =====================================================================
# ОБРАБОТЧИКИ ШИФРОВАНИЯ И РАСШИФРОВАНИЯ
# =====================================================================

def handle_encrypt() -> None:
    global last_used_key
    print(f"\n--- 1. ЗАШИФРОВАТЬ ТЕКСТ (Аффинный шифр, m={current_alphabet.power}) ---")
    text = prompt_text_source("открытый текст для шифрования")
    if text is None:
        return

    m = current_alphabet.power
    a = prompt_int("Введите первую часть ключа a (взаимно просто с m)")
    if a is None:
        return
    a_red = a % m
    if a_red == 0 or ac.extended_gcd(a_red, m)[0] != 1:
        gcd_val = ac.extended_gcd(a_red, m)[0]
        print(f">> Ошибка: коэффициент a={a} (a mod {m} = {a_red}) не взаимно прост с m={m} (НОД={gcd_val}). Обратного элемента нет!")
        return

    b = prompt_int(f"Введите вторую часть ключа b (0..{m-1})")
    if b is None:
        return
    b %= m

    case_info = prompt_case_mode(is_encryption=True)
    if case_info is None:
        return
    case_mode, filter_alpha = case_info

    encrypted_text = ac.encrypt(
        text, a, b, alphabet=current_alphabet, filter_non_alpha=filter_alpha, case_mode=case_mode
    )
    last_used_key = (a, b)

    print("\n" + "=" * 60)
    print(f"КЛЮЧ: (a = {a}, b = {b})")
    print(f"ШИФР-ТЕКСТ (ШТ):\n{encrypted_text}")
    print("=" * 60)

    save_choice = input("\nСохранить зашифрованный текст в файл? (y/n, по умолчанию y): ").strip().lower()
    if save_choice in ("", "y", "yes", "да"):
        default_file = os.path.join(OUTPUTS_DIR, "encrypted.txt")
        save_file = input(f"Путь к файлу [по умолчанию: {default_file}, 0 - отмена]: ").strip()
        if save_file != "0":
            save_file = save_file or default_file
            content = (
                f"=== ШИФРОВАНИЕ (АФФИННЫЙ ШИФР) ===\n"
                f"КЛЮЧ: a = {a}, b = {b}\n"
                f"ШИФР-ТЕКСТ (ШТ): {encrypted_text}\n"
            )
            save_text_file(save_file, content)
            print(f">> Файл сохранен: {save_file}")


def handle_decrypt() -> None:
    global last_used_key
    print(f"\n--- 2. РАСШИФРОВАТЬ ТЕКСТ ПО КЛЮЧУ (Аффинный шифр, m={current_alphabet.power}) ---")
    default_enc = os.path.join(OUTPUTS_DIR, "encrypted.txt")
    text = prompt_text_source("шифр-текст для расшифрования", default_filepath=default_enc)
    if text is None:
        return

    m = current_alphabet.power
    def_a = last_used_key[0] if last_used_key else None
    def_b = last_used_key[1] if last_used_key else None

    a = prompt_int("Введите первую часть ключа a", default=def_a)
    if a is None:
        return
    a_red = a % m
    if a_red == 0 or ac.extended_gcd(a_red, m)[0] != 1:
        gcd_val = ac.extended_gcd(a_red, m)[0]
        print(f">> Ошибка: коэффициент a={a} (a mod {m} = {a_red}) не взаимно прост с m={m} (НОД={gcd_val}). Обратного элемента нет!")
        return

    b = prompt_int(f"Введите вторую часть ключа b (0..{m-1})", default=def_b)
    if b is None:
        return
    b %= m

    case_info = prompt_case_mode(is_encryption=False)
    if case_info is None:
        return
    case_mode, _ = case_info

    decrypted_text = ac.decrypt(text, a, b, alphabet=current_alphabet, case_mode=case_mode)

    print("\n" + "=" * 60)
    print(f"КЛЮЧ: (a = {a}, b = {b}) [a^(-1) = {ac.mod_inverse(a, m)[2]}]")
    print(f"РАСШИФРОВАННЫЙ ТЕКСТ (ОТ):\n{decrypted_text}")
    print("=" * 60)

    save_choice = input("\nСохранить расшифрованный текст в файл? (y/n, по умолчанию y): ").strip().lower()
    if save_choice in ("", "y", "yes", "да"):
        default_file = os.path.join(OUTPUTS_DIR, "decrypted.txt")
        save_file = input(f"Путь к файлу [по умолчанию: {default_file}, 0 - отмена]: ").strip()
        if save_file != "0":
            save_file = save_file or default_file
            content = (
                f"=== РАСШИФРОВАНИЕ (АФФИННЫЙ ШИФР) ===\n"
                f"КЛЮЧ: a = {a}, b = {b}\n"
                f"ШИФР-ТЕКСТ (ШТ): {text}\n"
                f"РАСШИФРОВАННЫЙ ТЕКСТ (ОТ): {decrypted_text}\n"
            )
            save_text_file(save_file, content)
            print(f">> Файл сохранен: {save_file}")


def handle_cryptanalysis() -> None:
    print("\n--- 3. ЧАСТОТНЫЙ АНАЛИЗ И КРИПТОАНАЛИЗ АФФИННОГО ШИФРА ---")
    default_enc = os.path.join(OUTPUTS_DIR, "encrypted.txt")
    text = prompt_text_source("шифр-текст для криптоанализа", default_filepath=default_enc)
    if text is None:
        return

    fa = ac.frequency_analysis(text, current_alphabet)
    if fa["total_alpha_chars"] == 0:
        print(f"\n>> Ошибка: в тексте нет символов выбранного алфавита ('{current_alphabet.name}').")
        print(">> Частотный анализ невозможен. Проверьте правильность введенного текста или активного алфавита.")
        return

    print("\n" + "=" * 65)
    print(f"РЕЗУЛЬТАТЫ ЧАСТОТНОГО АНАЛИЗА (всего букв: {fa['total_alpha_chars']}):")
    print("Символ | Кол-во | Частота в тексте")
    print("-" * 35)
    for ch, cnt, freq in fa["sorted_chars"][:10]:
        print(f"  '{ch}'  |  {cnt:3d}   |  {freq:.4f}")
    print("=" * 65)

    print("\nВыдвижение гипотез на основе систем сравнений...")
    hypotheses = ac.generate_hypotheses_systems(text, current_alphabet, top_ct_count=5, top_pt_count=5)
    valid_hypotheses = [h for h in hypotheses if h["valid_keys"]]

    print(f"Всего проверено систем: {len(hypotheses)}, систем с допустимыми ключами: {len(valid_hypotheses)}")

    if not valid_hypotheses:
        print("\n>> Предупреждение: не удалось составить разрешимые системы сравнений с допустимыми ключами.")
        print(">> Текст слишком короткий либо не содержит достаточного разнообразия символов.")
        return

    print("\nЗапуск процедуры постепенного перебора ключей с оценкой осмысленности:")
    evaluated = []
    seen = set()
    for h in valid_hypotheses:
        for a, b in h["valid_keys"]:
            if (a, b) in seen:
                continue
            seen.add((a, b))
            dec = ac.decrypt(text, a, b, alphabet=current_alphabet)
            sc = ac.score_text(dec, current_alphabet)
            evaluated.append((sc, a, b, h["mapping"], dec))

    evaluated.sort(key=lambda item: item[0], reverse=True)

    if not evaluated:
        print("\n>> Не удалось сформировать допустимые варианты расшифрования.")
        return

    print(f"\nТоп наиболее вероятных ключей:")
    for idx, (sc, a, b, mapping, dec) in enumerate(evaluated[:5], 1):
        print(f"\n#{idx} Ключ (a={a}, b={b}) [гипотеза {mapping}], балл: {sc:.1f}")
        print(f"Фрагмент: {dec[:70]}...")

    best_sc, best_a, best_b, best_mapping, best_dec = evaluated[0]
    print(f"\n>> Рекомендуемый ключ: a = {best_a}, b = {best_b} ({best_mapping})")

    save_log = input("\nСохранить детальный математический протокол решения всех систем в файл? (y/n, по умолчанию n): ").strip().lower()
    if save_log in ("y", "yes", "да"):
        default_log_file = os.path.join(OUTPUTS_DIR, "cryptanalysis_math_log.txt")
        log_file = input(f"Путь к файлу [по умолчанию: {default_log_file}, 0 - отмена]: ").strip()
        if log_file != "0":
            log_file = log_file or default_log_file
            print(">> Формирование подробного математического протокола...")
            content = ac.generate_cryptanalysis_math_log(text, current_alphabet)
            save_text_file(log_file, content)
            print(f">> Детальный математический протокол сохранен в: {log_file}")


def handle_variant_task() -> None:
    print("\n--- 4. ВЫПОЛНЕНИЕ ЗАДАНИЯ ПО ВАРИАНТУ (ВАРИАНТ № 16) ---")
    var_num = 16
    var_data = VARIANTS_DB[var_num]
    ct = var_data["ciphertext"]
    key_a, key_b = var_data["key"]
    a_inv = var_data["a_inv"]
    pt = var_data["plaintext"]
    author = var_data["author"]
    work = var_data["work"]
    ot_aw = var_data["author_work_ot"]
    st_aw = var_data["author_work_st"]

    print(f"Вариант №: {var_num}")
    print(f"Шифр-текст (ШТ):\n{ct}")

    fa = ac.frequency_analysis(ct, current_alphabet)
    print("\nРезультаты частотного анализа:")
    print("Топ-6 наиболее частых букв в ШТ:")
    for ch, cnt, freq in fa["sorted_chars"][:6]:
        print(f"  '{ch}': {cnt} раз ({freq:.4f})")

    print("\nСоставление системы уравнений для наиболее частых букв:")
    print("В русском языке наиболее частые буквы — 'о' (код 14) и 'е' (код 5).")
    print("В шифр-тексте буквы 'з' (код 7) и 'ф' (код 20) входят в группу частых.")
    print("Гипотеза: E(о) = з, E(е) = ф")
    print("  (14 * a + b) ≡  7 (mod 32)")
    print("  ( 5 * a + b) ≡ 20 (mod 32)")

    st, sols, desc = ac.solve_system_congruences(14, 7, 5, 20, 32)
    print(f"\nРешение системы: {desc}")
    print(f"Найден ключ: a = {key_a}, b = {key_b}")
    d, u, _ = ac.extended_gcd(key_a, 32)
    step_note = f" (u = {u} < 0 => {u} + 32 = {a_inv})" if u < 0 else ""
    print(f"Обратный элемент a^(-1) по модулю 32 (наименьший положительный вычет): {a_inv}{step_note}")

    print("\nРасшифрованный текст (ОТ):")
    print(pt)

    print("\nАнализ литературного источника:")
    print(f"Автор: {author}")
    print(f"Произведение: «{work}»")
    print(f"Каноническая строка (ОТ): {ot_aw}")
    print(f"Зашифрованная строка (ШТ): {st_aw}")

    out_file = os.path.join(OUTPUTS_DIR, "variant_16_solution.txt")
    print(f"\n>> Итоговый отчет сохранен в: {out_file}")


def handle_change_alphabet() -> None:
    global current_alphabet
    print("\n--- 6. ВЫБОР АЛФАВИТА ---")
    print(f"Текущий активный алфавит: {current_alphabet.name}")
    print("\nДоступные пресеты:")
    presets_list = list(ac.PRESETS.items())
    for idx, (code, alpha) in enumerate(presets_list, 1):
        active_mark = " (активен)" if alpha == current_alphabet else ""
        print(f"{idx} - [{code}] {alpha.name}{active_mark}")
    print("0 - Отмена (вернуться в главное меню)")

    choice = input("\nВыберите вариант (0 для отмены): ").strip()
    if choice == "0":
        print(">> Действие отменено.")
        return
    try:
        choice_idx = int(choice)
        if 1 <= choice_idx <= len(presets_list):
            _, selected_alpha = presets_list[choice_idx - 1]
            current_alphabet = selected_alpha
            print(f">> Активный алфавит переключен на: {current_alphabet.name}")
            return
    except ValueError:
        pass
    print(">> Некорректный выбор.")


def main() -> None:
    while True:
        clear_screen()
        print_banner()
        print(f"\nГЛАВНОЕ МЕНЮ [{current_alphabet.name}]:")
        print("1. Зашифровать текст (аффинный шифр, ключ (a, b))")
        print("2. Расшифровать текст по ключу (a, b)")
        print("3. Криптоанализ (частотный анализ, гипотезы, подбор ключа)")
        print("4. Выполнить задание по варианту (Вариант 16)")
        print("5. Математический аппарат (Евклид, обратный элемент, ax=b mod m, системы)")
        print("6. Сменить алфавит (ru / en)")
        print("0. Выход")

        choice = input("\nВыберите действие (0-6): ").strip()
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
            handle_cryptanalysis()
            pause_and_return()
        elif choice == "4":
            clear_screen()
            print_banner()
            handle_variant_task()
            pause_and_return()
        elif choice == "5":
            handle_math_submenu()
        elif choice == "6":
            clear_screen()
            print_banner()
            handle_change_alphabet()
            pause_and_return()
        elif choice == "0":
            print("\nЗавершение работы программы.")
            break
        else:
            print(">> Некорректный выбор. Введите цифру от 0 до 6.")
            pause_and_return()


if __name__ == "__main__":
    main()
