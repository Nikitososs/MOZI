{{json
{
  "discipline": "Математические основы защиты информации",
  "title": "Шифрование с открытым ключом. Алгоритм RSA",
  "student": {"name": "Смирнов Никита Михайлович", "course": "2", "group": "ФИТ-242", "program": "02.03.02 Фундаментальная информатика и информационные технологии"},
  "teacher": {"title": "канд. пед. наук, доцент", "name": "Белим Светлана Юрьевна"},
  "institution": {"short": "ОмГТУ", "department": "ПМиФИ", "year": "2026"},
  "work": {"type": "Лабораторная работа № 4", "variant": "16"}
}
}}

# СОДЕРЖАНИЕ

# ВВЕДЕНИЕ

Цель лабораторной работы — реализовать учебную программу для проверки арифметических операций RSA, формирования пар ключей и проверки шифрования с открытым ключом и последующего расшифрования. Вариант 16 использует простые числа $p=167$ и $q=311$, указанные в методических рекомендациях.

Для достижения цели реализованы расширенный алгоритм Евклида и бинарное возведение в степень по модулю; формирование трёх пар ключей для заданных простых $p$ и $q$; перевод русского текста в цифровую форму, разбиение на блоки меньше $n$ с учётом нулей на границе, шифрование и обратное преобразование.

# ОСНОВНАЯ ЧАСТЬ

## 1 Теоретические сведения

В RSA выбираются различные простые числа $p$ и $q$. Модуль и значение функции Эйлера вычисляются по формулам:

$$
n=pq, \qquad \varphi(n)=(p-1)(q-1).
$$

Открытый показатель $e$ выбирается взаимно простым с $\varphi(n)$. Закрытый показатель $d$ является обратным к $e$ по модулю $\varphi(n)$:

$$
\gcd(e,\varphi(n))=1, \qquad ed \equiv 1 \pmod{\varphi(n)}.
$$

Открытый ключ — $(e,n)$, закрытый — $(d,n)$. Число $M$ шифруется и расшифровывается независимо в каждом блоке:

$$
C=M^e \bmod n, \qquad M=C^d \bmod n, \qquad 0 \le M < n.
$$

Расширенный алгоритм Евклида находит целые $x$ и $y$, для которых $ax+by=\gcd(a,b)$. Если $\gcd(e,\varphi(n))=1$, коэффициент $x$ по модулю $\varphi(n)$ даёт значение $d$. Бинарное возведение в степень последовательно возводит основание в квадрат и обрабатывает двоичные разряды показателя; число операций умножения пропорционально $\log_2 e$.

## 2 Кодирование и разбиение открытого текста

Текст приводится к верхнему регистру, буква «ё» заменяется на «е». Допустимые символы — 32 русские буквы и пробел; остальные символы при подготовке пропускаются. Каждому символу соответствует двухзначный код, пробелу — число 99.

Таблица: Коды символов русского алфавита

| Буква | Код | Буква | Код | Буква | Код | Буква | Код |
|:--:|--:|:--:|--:|:--:|--:|:--:|--:|
| А | 10 | Б | 11 | В | 12 | Г | 13 |
| Д | 14 | Е | 15 | Ж | 16 | З | 17 |
| И | 18 | Й | 19 | К | 20 | Л | 21 |
| М | 22 | Н | 23 | О | 24 | П | 25 |
| Р | 26 | С | 27 | Т | 28 | У | 29 |
| Ф | 30 | Х | 31 | Ц | 32 | Ч | 33 |
| Ш | 34 | Щ | 35 | Ъ | 36 | Ы | 37 |
| Ь | 38 | Э | 39 | Ю | 40 | Я | 41 |
| пробел | 99 |  |  |  |  |  |  |

Коды символов соединяются в одну десятичную строку. Из её начала последовательно выбирается наибольший блок, числовое значение которого меньше $n$. Если следующая граница оставила бы ведущий ноль у нового блока, текущий блок укорачивается до позиции перед нулём, как требует методичка. Границы блоков могут проходить внутри двухзначного кода; при расшифровании десятичные строки восстановленных блоков сначала конкатенируются, затем разбиваются на пары цифр. Для надёжного выделения шифроблоков каждый результат шифрования записывается с дополнением слева нулями до числа разрядов $n$; при расшифровании эта фиксированная ширина снимается.

Для строки «ВАСЯ МОЛОДЕЦ» цифровое представление равно `121027419922242124141532`. В методическом примере с $n=22213$ разбиение даёт `12102`, `7419`, `9222`, `4212`, `4141`, `532`.

## 3 Алгоритм и интерфейс программы

Главное меню содержит четыре пункта: «Проверка арифметики», «Шифровка/дешифровка», «Выполнение варианта 16» и «Выход». В первом пункте вычисляются НОД и коэффициенты Безу расширенным алгоритмом Евклида, обратный элемент и значение $a^k \bmod n$ бинарным методом. Во втором можно сформировать ключи и выполнить шифрование/расшифрование для введённых простых $p$ и $q$. Третий пункт запускает полный расчёт варианта 16 с параметрами $p=167$, $q=311$; пользователь вводит открытый текст, выбирает пару ключей, после чего программа показывает шифрование и расшифрование и сохраняет результат.

Алгоритм полного цикла:

1. Проверить простоту $p$ и $q$, их различие и достаточный размер $n$ для кодов алфавита.
2. Вычислить $n$ и $\varphi(n)$; подобрать не менее трёх различных $e$, взаимно простых с $\varphi(n)$, и найти соответствующие $d$ расширенным алгоритмом Евклида.
3. Выбрать номер пары ключей и подготовить введённый текст согласно таблице замен.
4. Собрать блоки $M<n$, избегая ведущего нуля у каждого блока.
5. Зашифровать каждый блок бинарным возведением в степень, вывести блоки и конкатенированный шифр-текст.
6. Расшифровать фиксированные по ширине шифроблоки, склеить восстановленные цифровые строки, преобразовать пары кодов обратно в текст и сравнить с подготовленной строкой.
7. Сохранить параметры и результаты последнего расчёта в `lab_4/outputs/rsa_result.txt`.

Программа использует тест Миллера—Рабина для проверки простоты. Для целых чисел меньше $2^{64}$ используемый набор оснований детерминирован; для больших значений тест является вероятностным. Реализация RSA предназначена для изучения алгоритма и не использует криптографически стойкую генерацию ключей или дополнение сообщения.

## 4 Результаты для варианта 16

Для $p=167$ и $q=311$:

$$
n=167\cdot311=51937, \qquad \varphi(n)=166\cdot310=51460.
$$

Таблица: Сформированные пары ключей варианта 16

| № | $e$ | Открытый ключ $(e,n)$ | $d=e^{-1}\bmod\varphi(n)$ | Закрытый ключ $(d,n)$ | $ed\bmod\varphi(n)$ |
|--:|--:|:--|--:|:--|--:|
| 1 | 3 | (3, 51937) | 34307 | (34307, 51937) | 1 |
| 2 | 7 | (7, 51937) | 14703 | (14703, 51937) | 1 |
| 3 | 9 | (9, 51937) | 28589 | (28589, 51937) | 1 |

Для проверки выбрана первая пара ключей. Открытый текст «ВАСЯ МОЛОДЕЦ» кодируется строкой `121027419922242124141532` и разбивается на максимальные блоки, меньшие 51937.

Таблица: Шифрование и расшифрование блоков

| № | $M$ | $C=M^3\bmod51937$ | Фиксированный шифроблок | $C^{34307}\bmod51937$ |
|--:|--:|--:|:--:|--:|
| 1 | 12102 | 44694 | 44694 | 12102 |
| 2 | 7419 | 28921 | 28921 | 7419 |
| 3 | 9222 | 8235 | 08235 | 9222 |
| 4 | 42124 | 26258 | 26258 | 42124 |
| 5 | 14153 | 49659 | 49659 | 14153 |
| 6 | 2 | 8 | 00008 | 2 |

Конкатенированный шифр-текст: `446942892108235262584965900008`. После расшифрования и объединения блоков восстановлена цифровая строка `121027419922242124141532`, которая преобразуется в исходный текст «ВАСЯ МОЛОДЕЦ».

## 5 Проверка корректности

Автоматические тесты проверяют тождество Безу для положительных, отрицательных и нулевых входов; модульную степень сравнением с независимой операцией Python `pow`; корректность обратного элемента и обработку необратимого значения; проверку простоты; генерацию трёх ключевых пар; совпадение разбиения с примером методички; корректировку границы перед нулём; шифрование-дешифрование текста, включая пробелы и нормализацию символов; обработку ошибочного ввода.

При ручной проверке вариант 16 формирует три различные пары ключей, для каждой выполняется $ed\bmod\varphi(n)=1$. Все блоки шифруются значениями меньше $n$, а поблочное возведение в степень закрытым показателем восстанавливает исходные блоки. Полная строка после дешифрования совпадает с нормализованным открытым текстом.

## 6 Контрольные вопросы

1. **Каким требованиям должно удовлетворять число $n$?** Оно должно быть произведением двух различных простых множителей $p$ и $q$. Числа $p$ и $q$ следует держать в секрете; в учебной программе дополнительно требуется $n>99$, чтобы все коды символов алфавита были допустимыми блоками.
2. **Что является открытым ключом шифрования?** Пара $(e,n)$.
3. **Как вычисляется закрытый ключ?** Выбирается $e$, взаимно простое с $\varphi(n)$; затем расширенным алгоритмом Евклида находится $d=e^{-1}\bmod\varphi(n)$.
4. **Как сообщение разбивается на блоки?** Текст заменяется строкой двухзначных кодов; слева направо выбираются максимальные десятичные блоки меньше $n$. Ни один блок не должен начинаться с нуля; при необходимости предыдущий блок укорачивают.
5. **Как выполняется шифрование?** Для каждого блока вычисляется $C=M^e\bmod n$.
6. **Как выполняется расшифрование?** Для каждого шифроблока вычисляется $M=C^d\bmod n$, десятичные блоки объединяются и переводятся обратно в пары кодов символов.

# ЗАКЛЮЧЕНИЕ

Реализована программа с отдельными пунктами меню для арифметической проверки, произвольного шифрования/расшифрования и полного выполнения варианта 16. В пункте варианта используются $p=167$, $q=311$, формируются три пары ключей и выполняется полный цикл для введённого текста. В контрольном запуске для строки «ВАСЯ МОЛОДЕЦ» разбиение удовлетворяет ограничениям $M<n$ и отсутствия ведущего нуля, а после обратного преобразования текст полностью восстановлен.

# СПИСОК ЛИТЕРАТУРЫ

1. Математические основы защиты информации : методические указания к лабораторным работам / Минобрнауки России, Омский государственный технический университет ; составители С. Ю. Белим, С. В. Белим. — Омск : Издательство ОмГТУ, 2023. — С. 32–35, приложение 4.

# ПРИЛОЖЕНИЯ

## Код программы

Ниже приведён исходный код вычислительного модуля RSA и интерактивной программы лабораторной работы.

Листинг: Вычислительное ядро RSA (lab_4/rsa.py)

```python
"""Арифметика и текстовое кодирование для учебной реализации RSA."""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd

ALPHABET = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
SYMBOL_TO_CODE = {symbol: index + 10 for index, symbol in enumerate(ALPHABET)}
CODE_TO_SYMBOL = {code: symbol for symbol, code in SYMBOL_TO_CODE.items()}
SPACE_CODE = 99


def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    """Вернуть (g, x, y), для которых a*x + b*y = g = gcd(a, b)."""
    old_r, r = a, b
    old_x, x = 1, 0
    old_y, y = 0, 1
    while r:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_x, x = x, old_x - quotient * x
        old_y, y = y, old_y - quotient * y
    if old_r < 0:
        return -old_r, -old_x, -old_y
    return old_r, old_x, old_y


def mod_inverse(value: int, modulus: int) -> int:
    """Найти обратный элемент value по положительному модулю modulus."""
    if modulus <= 1:
        raise ValueError("Модуль должен быть больше 1.")
    divisor, coefficient, _ = extended_gcd(value, modulus)
    if divisor != 1:
        raise ValueError(f"Обратный элемент не существует: НОД({value}, {modulus}) = {divisor}.")
    return coefficient % modulus


def modular_power(base: int, exponent: int, modulus: int) -> int:
    """Вычислить base**exponent mod modulus бинарным алгоритмом."""
    if exponent < 0:
        raise ValueError("Показатель степени не может быть отрицательным.")
    if modulus <= 0:
        raise ValueError("Модуль должен быть положительным.")
    result = 1 % modulus
    factor = base % modulus
    power = exponent
    while power:
        if power & 1:
            result = (result * factor) % modulus
        factor = (factor * factor) % modulus
        power >>= 1
    return result


def is_prime(number: int) -> bool:
    """Тест Миллера—Рабина; точен для n < 2**64, вероятностный выше."""
    if number < 2:
        return False
    small_primes = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    for prime in small_primes:
        if number == prime:
            return True
        if number % prime == 0:
            return False
    odd_part = number - 1
    shifts = 0
    while odd_part % 2 == 0:
        shifts += 1
        odd_part //= 2
    bases = (2, 325, 9375, 28178, 450775, 9780504, 1795265022)
    for base in bases:
        if base % number == 0:
            continue
        residue = modular_power(base, odd_part, number)
        if residue in (1, number - 1):
            continue
        for _ in range(shifts - 1):
            residue = (residue * residue) % number
            if residue == number - 1:
                break
        else:
            return False
    return True


@dataclass(frozen=True)
class KeyPair:
    """Открытая и соответствующая ей закрытая пара RSA."""

    e: int
    d: int
    n: int
    phi: int

    @property
    def public_key(self) -> tuple[int, int]:
        return self.e, self.n

    @property
    def private_key(self) -> tuple[int, int]:
        return self.d, self.n


def generate_key_pairs(p: int, q: int, count: int = 3) -> list[KeyPair]:
    """Построить count различных пар ключей для заданных простых p и q."""
    if not is_prime(p) or not is_prime(q):
        raise ValueError("p и q должны быть простыми числами больше 1.")
    if p == q:
        raise ValueError("Простые числа p и q должны различаться.")
    n = p * q
    if n <= SPACE_CODE:
        raise ValueError(f"Для кодов символов 10–41 и пробела 99 требуется n > 99 (сейчас n={n}).")
    if count < 3:
        raise ValueError("Для лабораторной требуется не менее трёх пар ключей.")
    phi = (p - 1) * (q - 1)
    pairs: list[KeyPair] = []
    for e in range(2, phi):
        if gcd(e, phi) == 1:
            pairs.append(KeyPair(e=e, d=mod_inverse(e, phi), n=n, phi=phi))
            if len(pairs) == count:
                break
    if len(pairs) < count:
        raise ValueError(f"Для φ(n)={phi} удалось сформировать только {len(pairs)} ключевых пар.")
    return pairs


def encode_text(text: str) -> tuple[str, str]:
    """Нормализовать текст и вернуть (нормализованный текст, строку пар кодов)."""
    normalized: list[str] = []
    canonical_input = text.upper().replace("Ё", "Е").replace("\r\n", " ").replace("\r", " ").replace("\n", " ")
    for char in canonical_input:
        if char in SYMBOL_TO_CODE:
            normalized.append(char)
        elif char in " \t\r\n":
            normalized.append(" ")
    canonical = "".join(normalized)
    digits = "".join(
        f"{SPACE_CODE:02d}" if char == " " else f"{SYMBOL_TO_CODE[char]:02d}"
        for char in canonical
    )
    return canonical, digits


def split_plaintext_blocks(digits: str, modulus: int) -> list[int]:
    """Жадно собрать максимальные десятичные блоки меньше n без ведущего нуля."""
    if modulus <= SPACE_CODE:
        raise ValueError("Модуль n должен быть больше 99.")
    if not digits or len(digits) % 2:
        raise ValueError("Строка кодов должна быть непустой и содержать целое число пар цифр.")
    blocks: list[int] = []
    if not digits.isdigit():
        raise ValueError("Строка кодов должна содержать только цифры.")
    if digits[0] == "0":
        raise ValueError("Кодируемая строка не должна начинаться с нуля.")
    offset = 0
    while offset < len(digits):
        end = offset + 1
        while end <= len(digits) and int(digits[offset:end]) < modulus:
            end += 1
        end -= 1
        if end < len(digits):
            # Переносим границу влево через ноль, чтобы следующий M не начинался с 0.
            while end > offset and digits[end] == "0":
                end -= 1
        if end <= offset:
            raise ValueError("Не удалось выбрать блок без ведущего нуля и меньше n.")
        blocks.append(int(digits[offset:end]))
        offset = end
    return blocks


@dataclass(frozen=True)
class EncryptionResult:
    plaintext: str
    encoded_digits: str
    plaintext_blocks: tuple[int, ...]
    ciphertext_blocks: tuple[int, ...]
    ciphertext: str


def encrypt_text(text: str, key: KeyPair) -> EncryptionResult:
    """Закодировать, разбить и зашифровать русский текст блоками."""
    plaintext, digits = encode_text(text)
    if not plaintext:
        raise ValueError("После подготовки в тексте не осталось русских букв или пробелов.")
    blocks = split_plaintext_blocks(digits, key.n)
    encrypted = tuple(modular_power(block, key.e, key.n) for block in blocks)
    width = len(str(key.n))
    ciphertext = "".join(f"{block:0{width}d}" for block in encrypted)
    return EncryptionResult(plaintext, digits, tuple(blocks), encrypted, ciphertext)


def decrypt_text(ciphertext: str, key: KeyPair) -> str:
    """Расшифровать конкатенацию шифроблоков фиксированной ширины."""
    width = len(str(key.n))
    if not ciphertext or len(ciphertext) % width:
        raise ValueError(f"Длина шифр-текста должна быть положительна и кратна {width}.")
    if not ciphertext.isdigit():
        raise ValueError("Шифр-текст должен содержать только цифры.")
    decoded_digits: list[str] = []
    for offset in range(0, len(ciphertext), width):
        cipher_block = int(ciphertext[offset:offset + width])
        if cipher_block >= key.n:
            raise ValueError(f"Шифроблок {cipher_block} должен быть меньше n={key.n}.")
        plain_block = modular_power(cipher_block, key.d, key.n)
        block_digits = str(plain_block)
        if block_digits.startswith("0"):
            raise ValueError("Расшифрованный блок начинается с нуля: неверный ключ или повреждённые данные.")
        decoded_digits.append(block_digits)
    digit_stream = "".join(decoded_digits)
    if len(digit_stream) % 2:
        raise ValueError("Объединённая строка кодов должна содержать чётное число цифр.")
    decoded: list[str] = []
    for pair_start in range(0, len(digit_stream), 2):
        code = int(digit_stream[pair_start:pair_start + 2])
        if code == SPACE_CODE:
            decoded.append(" ")
        elif code in CODE_TO_SYMBOL:
            decoded.append(CODE_TO_SYMBOL[code])
        else:
            raise ValueError(f"Неизвестный код символа {code}; проверьте закрытый ключ.")
    return "".join(decoded)
```

Листинг: Интерактивное меню (lab_4/main.py)

```python
"""Интерактивное меню лабораторной работы № 4 по алгоритму RSA."""

from __future__ import annotations

from pathlib import Path

from lab_4.rsa import (
    ALPHABET,
    KeyPair,
    encode_text,
    encrypt_text,
    extended_gcd,
    generate_key_pairs,
    mod_inverse,
    modular_power,
    decrypt_text,
)

OUTPUT_DIR = Path(__file__).resolve().parent / "outputs"
DEFAULT_P = 167  # Вариант 16 по таблице методических указаний.
DEFAULT_Q = 311


def read_int(prompt: str, default: int | None = None) -> int | None:
    """Прочитать целое число; пустой ввод выбирает default, q возвращает назад."""
    hint = f" [{default}]" if default is not None else ""
    raw = input(f"{prompt}{hint} (q — назад): ").strip()
    if raw.lower() == "q":
        return None
    if not raw and default is not None:
        return default
    try:
        return int(raw)
    except ValueError:
        print("Ошибка: введите целое число.")
        return None


def read_primes() -> tuple[int, int] | None:
    """Запросить два простых числа, предлагая p и q варианта 16."""
    print(f"Параметры варианта 16: p={DEFAULT_P}, q={DEFAULT_Q}.")
    p = read_int("Введите простое p", DEFAULT_P)
    if p is None:
        return None
    q = read_int("Введите простое q", DEFAULT_Q)
    if q is None:
        return None
    return p, q


def show_keys(p: int, q: int) -> list[KeyPair] | None:
    try:
        keys = generate_key_pairs(p, q)
    except ValueError as error:
        print(f"Ошибка формирования ключей: {error}")
        return None
    first = keys[0]
    print(f"\nn = p·q = {first.n}; φ(n) = (p−1)(q−1) = {first.phi}")
    print("№   Открытый ключ (e, n)       Закрытый ключ (d, n)       Проверка e·d mod φ(n)")
    for index, key in enumerate(keys, start=1):
        print(f"{index:<3} ({key.e}, {key.n}){(20 - len(str(key.e)) - len(str(key.n))) * ' '}"
              f"({key.d}, {key.n}){(20 - len(str(key.d)) - len(str(key.n))) * ' '}"
              f"{(key.e * key.d) % key.phi}")
    return keys


def arithmetic_menu() -> None:
    while True:
        print("\nПРОВЕРКА АРИФМЕТИКИ RSA")
        print("1. Расширенный алгоритм Евклида и обратный элемент")
        print("2. Бинарное возведение в степень по модулю")
        print("0. Назад")
        choice = input("Выберите действие: ").strip()
        if choice == "0":
            return
        if choice == "1":
            a = read_int("Введите a")
            b = read_int("Введите b") if a is not None else None
            if a is None or b is None:
                continue
            divisor, x, y = extended_gcd(a, b)
            print(f"НОД({a}, {b}) = {divisor}; коэффициенты Безу: x={x}, y={y}.")
            print(f"Проверка: {a}·({x}) + {b}·({y}) = {a*x + b*y}.")
            value = read_int("Число для нахождения обратного")
            if value is None:
                continue
            modulus = read_int("Модуль для обратного элемента")
            if modulus is None:
                continue
            try:
                inverse = mod_inverse(value, modulus)
                print(f"{value}^(-1) mod {modulus} = {inverse}; проверка: {value*inverse % modulus}.")
            except ValueError as error:
                print(f"Обратный элемент не найден: {error}")
        elif choice == "2":
            base = read_int("Введите основание a")
            exponent = read_int("Введите показатель степени k") if base is not None else None
            modulus = read_int("Введите модуль n") if exponent is not None else None
            if base is None or exponent is None or modulus is None:
                continue
            try:
                print(f"{base}^{exponent} mod {modulus} = {modular_power(base, exponent, modulus)}")
            except ValueError as error:
                print(f"Ошибка вычисления: {error}")
        else:
            print("Выберите 1, 2 или 0.")


def save_demo(plaintext: str, encoded: str, blocks: tuple[int, ...], cipher_blocks: tuple[int, ...],
              ciphertext: str, decoded: str, key: KeyPair) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUTPUT_DIR / "rsa_result.txt"
    report = (
        "Лабораторная работа № 4 — демонстрационный расчёт RSA\n"
        f"Открытый ключ (e, n): {key.public_key}\n"
        f"Закрытый ключ (d, n): {key.private_key}\n"
        f"Допустимые символы: {ALPHABET}; пробел кодируется числом 99; Ё заменяется на Е.\n"
        f"Открытый текст: {plaintext}\n"
        f"Двухзначное представление: {encoded}\n"
        f"Блоки открытого текста: {', '.join(map(str, blocks))}\n"
        f"Блоки шифр-текста: {', '.join(map(str, cipher_blocks))}\n"
        f"Конкатенация шифроблоков: {ciphertext}\n"
        f"Результат расшифрования: {decoded}\n"
    )
    path.write_text(report, encoding="utf-8")
    return path


def run_text_roundtrip(raw: str, keys: list[KeyPair]) -> None:
    """Шифровать и расшифровать введённый текст выбранной парой ключей."""
    try:
        key_number = read_int("Номер пары ключей для шифрования и расшифрования", 1)
        if key_number is None:
            return
        if not 1 <= key_number <= len(keys):
            raise ValueError(f"Номер пары должен быть от 1 до {len(keys)}.")
        key = keys[key_number - 1]
        result = encrypt_text(raw, key)
        decoded = decrypt_text(result.ciphertext, key)
        print(f"\nНормализованный открытый текст: {result.plaintext}")
        print(f"Коды символов (пары цифр): {result.encoded_digits}")
        print("Блоки M < n: " + " | ".join(map(str, result.plaintext_blocks)))
        print("Шифроблоки C = M^e mod n: " + " | ".join(map(str, result.ciphertext_blocks)))
        print(f"Шифр-текст (блоки конкатенированы): {result.ciphertext}")
        print(f"После расшифрования: {decoded}")
        if decoded != result.plaintext:
            raise ValueError("Расшифрованный текст не совпал с исходным.")
        print("Проверка пройдена: открытый текст восстановлен без изменений.")
        print(f"Результат сохранён: {save_demo(result.plaintext, result.encoded_digits, result.plaintext_blocks, result.ciphertext_blocks, result.ciphertext, decoded, key)}")
    except ValueError as error:
        print(f"Ошибка: {error}")


def execute_variant() -> None:
    """Запустить полный расчёт варианта 16 отдельным пунктом главного меню."""
    print("\nВЫПОЛНЕНИЕ ВАРИАНТА 16")
    print(f"Используются заданные вариантом числа: p={DEFAULT_P}, q={DEFAULT_Q}.")
    keys = show_keys(DEFAULT_P, DEFAULT_Q)
    if not keys:
        return
    print(f"\nПреамбула допустимых символов: {ALPHABET} и пробел (99).")
    print("Регистр приводится к верхнему, Ё заменяется на Е; прочие символы пропускаются.")
    run_text_roundtrip(input("Введите открытый текст: "), keys)


def encrypt_decrypt_menu() -> None:
    while True:
        print("\nШИФРОВАНИЕ И РАСШИФРОВАНИЕ")
        print("1. Сформировать и показать не менее трёх пар ключей для p и q")
        print("2. Зашифровать и расшифровать русский текст выбранной парой")
        print("0. Назад")
        choice = input("Выберите действие: ").strip()
        if choice == "0":
            return
        if choice not in {"1", "2"}:
            print("Выберите 1, 2 или 0.")
            continue
        primes = read_primes()
        if primes is None:
            continue
        keys = show_keys(*primes)
        if not keys or choice == "1":
            continue

        print(f"\nПреамбула допустимых символов: {ALPHABET} и пробел (99).")
        print("Регистр приводится к верхнему, Ё заменяется на Е; прочие символы пропускаются.")
        run_text_roundtrip(input("Введите открытый текст: "), keys)


def main() -> None:
    while True:
        print("\n" + "=" * 65)
        print("ЛАБОРАТОРНАЯ РАБОТА № 4 — ШИФРОВАНИЕ С ОТКРЫТЫМ КЛЮЧОМ RSA")
        print("1. Проверка арифметики")
        print("2. Шифровка/дешифровка")
        print("3. Выполнение варианта 16")
        print("4. Выход")
        choice = input("Выберите пункт меню: ").strip()
        if choice == "1":
            arithmetic_menu()
        elif choice == "2":
            encrypt_decrypt_menu()
        elif choice == "3":
            execute_variant()
        elif choice == "4":
            print("Работа завершена.")
            return
        else:
            print("Выберите 1, 2, 3 или 4.")


if __name__ == "__main__":
    main()
```
