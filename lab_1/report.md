{{json
{
  "discipline": "Математические основы защиты информации",
  "student": {
    "name": "Смирнов Никита Михайлович",
    "course": "2",
    "group": "ФИТ-242",
    "program": "02.03.02 Фундаментальная информатика и информационные технологии"
  },
  "teacher": {
    "title": "канд. пед. наук, доцент",
    "name": "Белим Светлана Юрьевна"
  },
  "institution": {
    "short": "ОмГТУ",
    "full_name": "Омский государственный технический университет",
    "department": "ПМиФИ",
    "city": "Омск",
    "year": "2026"
  },
  "title": "Шифр Цезаря",
  "work": {
    "type": "Лабораторная работа № 1",
    "variant": "16"
  }
}
}}

# СОДЕРЖАНИЕ

# ОСНОВНАЯ ЧАСТЬ

## Результаты варианта 16

Шифр-текст: `юяингщжсадвгмюруюцэьцгтяфдщшуцшхсвшуцшхяпфяуябщг` (48 символов). Для русского алфавита $m=32$ использовано преобразование $D_k(y)=(y-k)\bmod 32$. Проверены все 31 ненулевой ключ.

Таблица: Расшифрования при полном переборе ключей

| Ключ $k$ | Результат |
|---:|---|
| 1 | `эюзмвшерягбвлэптэхьыхвсюугшчтхчфрбчтхчфюоуютюашв` |
| 2 | `ьэжлбчдпювабкьосьфыъфбрэтвчцсфцупацсфцуэнтэсэячб` |
| 3 | `ыьекацгоэбяайынрыуъщуапьсбцхрухтояхрухтьмсьрьюца` |
| 4 | `ъыдйяхвньаюяиъмпътщштяоырахфптфснюфптфсылрыпыэхя` |
| 5 | `щъгиюфбмыяэюзщлощсшчсюнъпяфуосурмэуосуръкпъоъьфю` |
| 6 | `шщвзэуалъюьэжшкншрчцрэмщоюутнртпльтнртпщйощнщыуэ` |
| 7 | `чшбжьтякщэыьечймчпцхпьлшнэтсмпсокысмпсошиншмшъть` |
| 8 | `цчаеысюйшьъыдцилцохфоыкчмьсрлорнйърлорнчзмчлчщсы` |
| 9 | `хцядърэичыщъгхзкхнфунъйцлырпкнпмищпкнпмцжлцкцшръ` |
| 10 | `фхюгщпьзцъшщвфжйфмутмщихкъпоймолзшоймолхекхйхчпщ` |
| 11 | `уфэвшоыжхщчшбуеиултслшзфйщонилнкжчнилнкфдйфифцош` |
| 12 | `туьбчнъефшцчатдзтксркчжуишнмзкмйецмзкмйугиузухнч` |
| 13 | `стыацмщдучхцясгжсйрпйцетзчмлжйлидхлжйлитвзтжтфмц` |
| 14 | `рсъяхлшгтцфхюрверипоихдсжцлкеикзгфкеикзсбжсесулх` |
| 15 | `прщюфкчвсхуфэпбдпзонзфгрехкйдзйжвуйдзйжраердрткф` |
| 16 | `опшэуйцбрфтуьоагожнмжувпдфйигжиебтигжиепядпгпсйу` |
| 17 | `ночьтихапустынявнемлетбогуизвездасзвездоюговорит` |
| 18 | `мнцысзфяотрсъмюбмдлкдсанвтзжбджгяржбджгнэвнбнпзс` |
| 19 | `лмхържуюнспрщлэалгкйгрямбсжеагевюпеагевмьбмаможр` |
| 20 | `клфщпетэмропшкьяквйивпюларедявдбэодявдблыалялнеп` |
| 21 | `йкушодсьлпночйыюйбизбоэкяпдгюбгаьнгюбгакъякюкмдо` |
| 22 | `ийтчнгрыкомнциъэиазжаньйюогвэавяымвэавяйщюйэйлгн` |
| 23 | `зисцмвпъйнлмхзщьзяжеямыиэнвбьябюълбьябюишэиьиквм` |
| 24 | `жзрхлбощимклфжшыжюедюлъзьмбаыюаэщкаыюаэзчьзызйбл` |
| 25 | `ежпфканшзлйкуечъеэдгэкщжылаяъэяьшйяъэяьжцыжъжиак` |
| 26 | `деоуйямчжкийтдцщдьгвьйшеъкяющьюычиющьюыехъещезяй` |
| 27 | `гднтиюлцейзисгхшгывбыичдщйюэшыэъцзэшыэъдфщдшджюи` |
| 28 | `вгмсзэкхдижзрвфчвъбаъзцгшиэьчъьщхжьчъьщгушгчгеэз` |
| 29 | `бвлржьйфгзежпбуцбщаящжхвчзьыцщышфеыцщышвтчвцвдьж` |
| 30 | `абкпеыиувждеоатхашяюшефбцжыъхшъчудъхшъчбсцбхбгые` |
| 31 | `яайодъзтбегднясфячюэчдуахеъщфчщцтгщфчщцархафавъд` |

Осмысленный результат получен при $k=17$:

- открытый текст: `ночьтихапустынявнемлетбогуизвездасзвездоюговорит`;
- автор и произведение: Михаил Юрьевич Лермонтов, «Выхожу один я на дорогу»;
- контрольная строка: `лермонтоввыхожуодинянадорогу`;
- её шифр-текст при $k=17$: `ьцбэяюгяуумжячдяхщюрюсхябяфд`.

Перебор и контрольное шифрование реализованы в `lab_1/caesar_cipher.py`; данные варианта находятся в `lab_1/variants.py`.


## Работа приложения

Запуск: `python -m lab_1.main`. Главное меню открывает шифрование, расшифрование по ключу, полный перебор, задание по варианту и выбор русского, английского или пользовательского алфавита. Для обычной операции текст вводится с клавиатуры или читается из файла; затем выбираются обработка регистра и ключ. Результат показывается в консоли и по умолчанию сохраняется в `lab_1/outputs/`. В задании можно выбрать вариант из базы, загрузить шифр-текст из файла или ввести его вручную.

# СПИСОК ЛИТЕРАТУРЫ

- Математические основы защиты информации : методические указания к лабораторным работам / Минобрнауки России, Омский государственный технический университет ; составители С. Ю. Белим, С. В. Белим. — Омск : Издательство ОмГТУ, 2023. — С. 5–12, приложение 1. — Текст : электронный.

# ПРИЛОЖЕНИЯ

## Приложение А. Фрагмент исходного кода `caesar_cipher.py`

Ядро шифра Цезаря: преобразование символов и полный перебор сдвигов.

Листинг: Основные функции модуля `caesar_cipher.py`

```python
from typing import Dict, List, Optional, Tuple


class Alphabet:
    def __init__(
        self,
        name: str,
        symbols: str,
        normalize_map: Optional[Dict[str, str]] = None,
        case_sensitive: bool = False,
    ):
        if len(symbols) < 2:
            raise ValueError(
                f"Мощность алфавита должна составлять не менее 2 символов (получено: {len(symbols)})"
            )
        self.name = name
        self.symbols = symbols
        self.power = len(symbols)
        self.normalize_map = normalize_map or {}
        self.case_sensitive = case_sensitive
        self.char_to_code: Dict[str, int] = {char: idx for idx, char in enumerate(symbols)}
        self.code_to_char: Dict[int, str] = {idx: char for idx, char in enumerate(symbols)}

    def normalize_char(self, char: str) -> str:
        c = char if self.case_sensitive else char.lower()
        return self.normalize_map.get(c, c)

    def A(self, char: str) -> int:
        norm = self.normalize_char(char)
        if norm in self.char_to_code:
            return self.char_to_code[norm]
        raise ValueError(f"Символ '{char}' не входит в алфавит '{self.name}' (m = {self.power})")

    def A_inv(self, code: int) -> str:
        return self.code_to_char[code % self.power]

    def E_k(self, x: int, k: int) -> int:
        return (x + k) % self.power

    def D_k(self, y: int, k: int) -> int:
        return self.E_k(y, -k)

    def encrypt_symbol(
        self, char: str, k: int, case_mode: str = "lower", preserve_case: Optional[bool] = None
    ) -> str:
        if preserve_case is not None:
            case_mode = "preserve" if preserve_case else "lower"
        norm = self.normalize_char(char)
        if norm in self.char_to_code:
            res_char = self.A_inv(self.E_k(self.char_to_code[norm], k))
            if self.case_sensitive:
                return res_char
            if case_mode == "preserve":
                return res_char.upper() if char.isupper() else res_char.lower()
            elif case_mode == "upper":
                return res_char.upper()
            elif case_mode == "lower":
                return res_char.lower()
            return res_char
        return char

    def decrypt_symbol(
        self, char: str, k: int, case_mode: str = "lower", preserve_case: Optional[bool] = None
    ) -> str:
        return self.encrypt_symbol(char, -k, case_mode=case_mode, preserve_case=preserve_case)

    def prepare_canonical_text(self, text: str) -> str:
        return "".join(
            self.normalize_char(c) for c in text if self.normalize_char(c) in self.char_to_code
        )

    def encrypt(
        self,
        text: str,
        k: int,
        filter_non_alpha: bool = False,
        case_mode: str = "lower",
        preserve_case: Optional[bool] = None,
    ) -> str:
        if preserve_case is not None:
            case_mode = "preserve" if preserve_case else "lower"
        if filter_non_alpha:
            src = self.prepare_canonical_text(text)
            return "".join(self.encrypt_symbol(c, k, case_mode="lower") for c in src)
        return "".join(self.encrypt_symbol(c, k, case_mode=case_mode) for c in text)

    def decrypt(
        self, text: str, k: int, case_mode: str = "lower", preserve_case: Optional[bool] = None
    ) -> str:
        return self.encrypt(
            text, -k, filter_non_alpha=False, case_mode=case_mode, preserve_case=preserve_case
        )

    def brute_force(
        self, ciphertext: str, case_mode: str = "lower", preserve_case: Optional[bool] = None
    ) -> List[Tuple[int, str]]:
        return [
            (k, self.decrypt(ciphertext, k, case_mode=case_mode, preserve_case=preserve_case))
            for k in range(1, self.power)
        ]
```
