# ПРИЛОЖЕНИЕ 1

# ОТЧЕТ К ЛАБОРАТОРНОЙ РАБОТЕ № 1

**Дисциплина:** Математические основы защиты информации (МОЗИ)  
**Тема:** Шифр Цезаря  
**Вариант №:** 1  
**Ф. И. О. студента:** Смирнов Никита Михайлович  
**Группа:** ФИТ-242  
**Проверил:** ___________________ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **Дата:** 16.09.2026  

---

## 1. Основные сведения

В шифре Цезаря шифрование сообщения выполняется посимвольно. Все сообщение $M$ представляется в виде символов одного алфавита:
$$M = b_1 b_2 b_3 dots b_n,$$
где $n$ — количество символов в сообщении.

Перед шифрованием естественный текст приводится к каноническому виду:
- все буквы переводятся в нижний регистр;
- буква «ё» отождествляется с буквой «е»;
- пробелы и знаки препинания опускаются.

Используется русский алфавит мощностью $m = 32$.

### Таблица кодировки символов (Таблица 1 методических указаний)

| Буква | Код | Буква | Код | Буква | Код | Буква | Код |
| :---: | :-: | :---: | :-: | :---: | :-: | :---: | :-: |
| **а** | 0  | **б** | 1  | **в** | 2  | **г** | 3  |
| **д** | 4  | **е / ё** | 5  | **ж** | 6  | **з** | 7  |
| **и** | 8  | **й** | 9  | **к** | 10 | **л** | 11 |
| **м** | 12 | **н** | 13 | **о** | 14 | **п** | 15 |
| **р** | 16 | **с** | 17 | **т** | 18 | **у** | 19 |
| **ф** | 20 | **х** | 21 | **ц** | 22 | **ч** | 23 |
| **ш** | 24 | **щ** | 25 | **ъ** | 26 | **ы** | 27 |
| **ь** | 28 | **э** | 29 | **ю** | 30 | **я** | 31 |

### Математические преобразования и композиция функций

1. **Кодирование символов алфавита** (отображение $A$):
   $$A(M) = A(b_1) A(b_2) dots A(b_n) = x_1 x_2 dots x_n, quad x_i in {0, 1, dots, m-1}.$$
2. **Прямое линейное преобразование шифрования** ($E_k$):
   $$y_i = E_k(x_i) = (x_i + k) pmod m,$$
   где $k in {1, 2, dots, m-1}$ — секретный ключ шифрования ($1 le k le 31$).
3. **Обратное декодирование в символы алфавита** ($A^{-1}$):
   $$C = A^{-1}(Y) = A^{-1}(y_1) A^{-1}(y_2) dots A^{-1}(y_n) = c_1 c_2 dots c_n.$$

Шифрование одного символа представляет собой композицию функций:
$$c_i = A^{-1}big(E_k(A(b_i))big).$$

4. **Обратное линейное преобразование расшифрования** ($D_k$):
   $$x_i = D_k(y_i) = (y_i - k) pmod m.$$
Расшифрование одного символа:
$$b_i = A^{-1}big(D_k(A(c_i))big).$$

---

## 2. Результаты выполнения задания (Вариант № 1)

- **ШИФР-ТЕКСТ (ШТ):**  
  `къыуоцльуцнльощьъщпльэрчвэщмжьщщмдуэзнлчъыршръыукэшщрутнрьэурхшлчрпрэырнутщы`
- **РАСШИФРОВАННЫЙ ТЕКСТ (ОТ):**  
  `япригласилвасгосподастемчтобысообщитьвампренеприятноеизвестиекнамедетревизор`
- **КЛЮЧ ($k$):**  
  `11`
- **АВТОР И ПРОИЗВЕДЕНИЕ:**  
  Николай Васильевич Гоголь, комедия «Ревизор»
- **АВТОР И ПРОИЗВЕДЕНИЕ (ОТ):**  
  `гогольревизор`
- **ЗАШИФРОВАННЫЕ ФАМИЛИЯ И НАЗВАНИЕ (ШТ) при $k = 11$:**  
  `ощощцзырнутщы`

### Варианты расшифрования исходного ШТ при различных значениях ключа ($k = 1 dots 31$)

| Ключ $k$ | Расшифрованный текст | Примечание |
| :---: | :--- | :--- |
| **$k = 1$** | `йщътнхкытхмкыншыщшокыьпцбьшлеышшлгтьжмкцщъпчпщътйьчшптсмпыьтпфчкцпопьъпмтсшъ` | |
| **$k = 2$** | `ишщсмфйъсфлйъмчъшчнйъыохаычкдъччквсыелйхшщоцошщсиыцчосрлоъысоуцйхоноыщолсрчщ` | |
| **$k = 3$** | `зчшрлуищрукищлцщчцмищънфяъцйгщццйбръдкифчшнхнчшрзъхцнрпкнщърнтхифнмнъшнкрпцш` | |
| **$k = 4$** | `жцчпктзшптйзшкхшцхлзшщмующхившххиапщгйзуцчмфмцчпжщфхмпоймшщпмсфзумлмщчмйпохч` | |
| **$k = 5$** | `ехцойсжчосижчйфчхфкжчшлтэшфзбчффзяошвижтхцлулхцоешуфлонилчшолружтлклшцлионфц` | |
| **$k = 6$** | `дфхнирецнрзециуцфуйецчксьчужацуужюнчбзесфхкткфхндчтукнмзкцчнкптескйкчхкзнмух` | |
| **$k = 7$** | `гуфмзпдхмпждхзтхутидхцйрыцтеяхттеэмцаждруфйсйуфмгцстймлжйхцмйосдрйийцфйжмлтф` | |
| **$k = 8$** | `втулжогфлоегфжсфтсзгфхипъхсдюфссдьлхяегптуиритулвхрсилкеифхлинргпизихуиелксу` | |
| **$k = 9$** | `бсткенвукндвуерусржвуфзощфргэурргыкфюдвостзпзсткбфпрзкйдзуфкзмпвозжзфтздкйрт` | |
| **$k = 10$** | `арсйдмбтймгбтдптрпебтужншупвьтппвъйуэгбнрсжожрсйауопжйигжтуйжлобнжежусжгйипс` | |
| **$k = 11$** | `япригласилвасгосподастемчтобысообщитьвампренеприятноеизвестиекнамедетревизор` | **Истинный текст** |
| **$k = 12$** | `юопзвкярзкбярвнронгярсдлцснаърннашзсыбялопдмдопзюсмндзжбдрсздймялдгдспдбзжнп` | |
| **$k = 13$** | `эножбйюпжйаюпбмпнмвюпргкхрмящпммячжръаюкноглгножэрлмгжеагпржгилюкгвгрогажемо` | |
| **$k = 14$** | `ьмнеаиэоеияэоаломлбэопвйфплюшоллюцепщяэймнвквмнеьпклведявопевзкэйвбвпнвяедлн` | |
| **$k = 15$** | `ылмдязьндзюьнякнлкаьнобиуокэчнккэхдошюьилмбйблмдыойкбдгюбнодбжйьибабомбюдгкм` | |
| **$k = 16$** | `ъклгюжымгжэымюймкйяымназтнйьцмййьфгнчэызклаиаклгънийагвэамнгаеиызаяанлаэгвйл` | |
| **$k = 17$** | `щйквэеълвеьълэилйиюълмяжсмиыхлииыувмцьъжйкязяйквщмзиявбьялмвядзъжяюямкяьвбик` | |
| **$k = 18$** | `шийбьдщкбдыщкьзкизэщклюерлзъфкззътблхыщеийюжюийбшлжзюбаыюклбюгжщеюэюлйюыбазй` | |
| **$k = 19$** | `чзиаыгшйагъшйыжйзжьшйкэдпкжщуйжжщсакфъшдзиэеэзиачкежэаяъэйкаэвешдэьэкиэъаяжи` | |
| **$k = 20$** | `цжзяъвчиявщчиъеижеычийьгойештиеешряйущчгжзьдьжзяцйдеьяющьийяьбдчгьыьйзьщяюез` | |
| **$k = 21$** | `хежющбцзюбшцзщдзедъцзиывнидчсзддчпюитшцвежыгыежюхигдыюэшызиюыагцвыъыижышюэдж` | |
| **$k = 22$** | `фдеэшахжэачхжшгждгщхжзъбмзгцржггцоэзсчхбдеъвъдеэфзвгъэьчъжзэъявхбъщъзеъчэьге` | |
| **$k = 23$** | `угдьчяфеьяцфечвегвшфежщалжвхпеввхньжрцфагдщбщгдьужбвщьыцщежьщюбфащшщждщцьывд` | |
| **$k = 24$** | `твгыцюудыюхудцбдвбчудешякебфодббфмыепхуявгшашвгытеабшыъхшдеышэауяшчшегшхыъбг` | |
| **$k = 25$** | `сбвъхэтгъэфтгхагбацтгдчюйдаунгааулъдофтюбвчячбвъсдяачъщфчгдъчьятючцчдвчфъщав` | |
| **$k = 26$** | `рабщфьсвщьусвфяваяхсвгцэигятмвяяткщгнусэабцюцабщргюяцщшуцвгщцыюсэцхцгбцущшяб` | |
| **$k = 27$** | `пяашуырбшытрбуюбяюфрбвхьзвюслбююсйшвмтрьяахэхяашпвэюхшчтхбвшхъэрьхфхвахтшчюа` | |
| **$k = 28$** | `оюячтъпачъспатэаюэупабфыжбэркаээричблспыюяфьфюячобьэфчцсфабчфщьпыфуфбяфсчцэя` | |
| **$k = 29$** | `нэюцсщояцщроясьяэьтояауъеаьпйяььпзцакроъэюуыуэюцнаыьуцхруяацушыоъутуаюурцхью` | |
| **$k = 30$** | `мьэхршнюхшпнюрыюьыснюятщдяыоиюыыожхяйпнщьэтътьэхмяъытхфптюяхтчънщтстяэтпхфыэ` | |
| **$k = 31$** | `лыьфпчмэфчомэпъэыърмэюсшгюънзэъънефюиомшыьсщсыьфлющъсфуосэюфсцщмшсрсюьсофуъь` | |

---

## 3. Ответы на контрольные вопросы

### 1. Какое преобразование используется в шифре Цезаря для шифрования текста?
Для шифрования текста используется посимвольное линейное преобразование в кольце вычетов по модулю мощности алфавита $m$:
$$y_i = E_k(x_i) = (x_i + k) pmod m,$$
где $x_i$ — числовой код открытого символа, $k$ — ключ шифрования ($1 le k le m - 1$), $y_i$ — код зашифрованного символа. В терминах символов алфавита это соответствует циклическому сдвигу символа на $k$ позиций вправо.

### 2. Какое преобразование используется в шифре Цезаря для расшифрования текста?
Для расшифрования текста используется обратное линейное преобразование:
$$x_i = D_k(y_i) = (y_i - k) pmod m,$$
где $y_i$ — числовой код шифр-символа, $k$ — ключ, $x_i$ — восстановленный числовой код исходного символа. Это соответствует циклическому сдвигу символа на $k$ позиций влево в алфавите.

### 3. Каким требованиям должен удовлетворять открытый текст, подаваемый на вход алгоритма шифрования?
Исходный открытый текст должен состоять из символов заданного алфавита (русский алфавит из 32 букв). Если сообщение написано на естественном языке, оно предварительно нормализуется:
- все буквы приводятся к единому (нижнему) регистру;
- буква «ё» заменяется на «е» (соответствует объединенному коду 5);
- опускаются пробелы, знаки препинания и любые спецсимволы, не входящие в используемый алфавит (носитель языка при этом однозначно восстанавливает смысл сообщения).

### 4. Какие значения может принимать ключ шифрования?
Ключ шифрования $k$ является целым числом из интервала от $1$ до $m - 1$, где $m$ — мощность используемого алфавита:
$$k in {1, 2, dots, m - 1}.$$
Для русского алфавита ($m = 32$) ключ принимает значения:
$$k in {1, 2, dots, 31}.$$
Значение $k = 0$ (или кратное $m$) не используется, так как оно дает тривиальное тождественное отображение ($y_i = x_i$). Значения, выходящие за пределы $[0; m-1]$, эквивалентны значению $k pmod m$.

### 5. Какова трудоемкость полного перебора для взлома шифра Цезаря?
Мощность пространства возможных ключей равна $m - 1$.
Для русского языка с $m = 32$ мощность пространства ключей составляет:
$$N = 32 - 1 = 31text{ вариант}.$$
Трудоемкость полного перебора крайне мала — $O(m) = 31$ операция расшифрования текста. Даже вручную перебор 31 варианта занимает несколько минут, а на ЭВМ выполняется мгновенно (доли миллисекунды). Поэтому шифр Цезаря обладает нулевой криптографической стойкостью к атаке на основе только шифр-текста (ciphertext-only attack).

---

## 4. Код программы

### Модуль чистого криптографического ядра `caesar_cipher.py`

```python
from typing import Dict, List, Tuple

ALPHABET_SYMBOLS: str = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
ALPHABET_POWER: int = len(ALPHABET_SYMBOLS)

CHAR_TO_CODE: Dict[str, int] = {char: idx for idx, char in enumerate(ALPHABET_SYMBOLS)}
CODE_TO_CHAR: Dict[int, str] = {idx: char for idx, char in enumerate(ALPHABET_SYMBOLS)}


def normalize_char(char: str) -> str:
    c = char.lower()
    return "е" if c == "ё" else c


def A(char: str) -> int:
    norm = normalize_char(char)
    if norm in CHAR_TO_CODE:
        return CHAR_TO_CODE[norm]
    raise ValueError(f"Символ '{char}' не входит в алфавит (m = {ALPHABET_POWER})")


def A_inv(code: int) -> str:
    return CODE_TO_CHAR[code % ALPHABET_POWER]


def E_k(x: int, k: int) -> int:
    return (x + k) % ALPHABET_POWER


def D_k(y: int, k: int) -> int:
    return (y - k) % ALPHABET_POWER


def encrypt_symbol(char: str, k: int) -> str:
    norm = normalize_char(char)
    if norm in CHAR_TO_CODE:
        return A_inv(E_k(A(norm), k))
    return char


def decrypt_symbol(char: str, k: int) -> str:
    norm = normalize_char(char)
    if norm in CHAR_TO_CODE:
        return A_inv(D_k(A(norm), k))
    return char


def prepare_canonical_text(text: str) -> str:
    result = []
    for ch in text:
        norm = normalize_char(ch)
        if norm in CHAR_TO_CODE:
            result.append(norm)
    return "".join(result)


def encrypt(text: str, k: int, filter_non_alpha: bool = False) -> str:
    if filter_non_alpha:
        text = prepare_canonical_text(text)
    return "".join(encrypt_symbol(ch, k) for ch in text)


def decrypt(text: str, k: int) -> str:
    return "".join(decrypt_symbol(ch, k) for ch in text)


def brute_force(ciphertext: str) -> List[Tuple[int, str]]:
    return [(k, decrypt(ciphertext, k)) for k in range(1, ALPHABET_POWER)]
```

### Переиспользуемый модуль ввода-вывода `common/io_utils.py`

```python
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
```

### Модуль консольного интерфейса `main.py`

```python
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
    print("  ОмГТУ | Кафедра ИВТ | Дисциплина: МОЗИ")
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
```
