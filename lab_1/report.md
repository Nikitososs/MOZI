{{json
{
  "discipline": "Математические основы защиты информации",
  "title": "Шифр Цезаря",
  "student": {"name": "Смирнов Никита Михайлович", "course": "2", "group": "ФИТ-242", "program": "02.03.02 Фундаментальная информатика и информационные технологии"},
  "teacher": {"title": "канд. пед. наук, доцент", "name": "Белим Светлана Юрьевна"},
  "institution": {"short": "ОмГТУ", "department": "ПМиФИ", "year": "2026"},
  "work": {"type": "Лабораторная работа № 1", "variant": "16"}
}
}}

# ПРИЛОЖЕНИЕ 1. ОТЧЕТ К ЛАБОРАТОРНОЙ РАБОТЕ № 1

**Лабораторная работа № 1**  
**Шифр Цезаря**  
**Вариант №** 16  
**Ф. И. О. студента:** Смирнов Никита Михайлович  
**Группа:** ФИТ-242  
**Проверил:** Белим Светлана Юрьевна  
**Дата:** 29.09.2026  

## Основные сведения

**Прямое преобразование шифра Цезаря:**

$$y = (x + k) \pmod m$$

**Обратное преобразование шифра Цезаря:**

$$x = (y - k) \pmod m$$

где $x \in \{0, 1, \dots, m - 1\}$ — числовой код символа открытого сообщения, $y \in \{0, 1, \dots, m - 1\}$ — числовой код символа зашифрованного сообщения, $k \in \{1, 2, \dots, m - 1\}$ — секретный ключ шифрования, $m = 32$ — мощность используемого алфавита. В соответствии с методическими указаниями для текстов на русском языке применяется алфавит мощностью $m = 32$, в котором буквы «е» и «ё» объединены под единым числовым кодом 5.

**Таблица кодировки символов:**

Таблица: Таблица кодировки символов русского алфавита ($m = 32$)
| Символ | Код | Символ | Код | Символ | Код | Символ | Код |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| а | 0 | и | 8 | р | 16 | ш | 24 |
| б | 1 | й | 9 | с | 17 | щ | 25 |
| в | 2 | к | 10 | т | 18 | ъ | 26 |
| г | 3 | л | 11 | у | 19 | ы | 27 |
| д | 4 | м | 12 | ф | 20 | ь | 28 |
| е/ё | 5 | н | 13 | х | 21 | э | 29 |
| ж | 6 | о | 14 | ц | 22 | ю | 30 |
| з | 7 | п | 15 | ч | 23 | я | 31 |

## Результаты

**ШИФР-ТЕКСТ (ШТ):**  
`юяингщжсадвгмюруюцэьцгтяфдщшуцшхсвшуцшхяпфяуябщг`

**РАСШИФРОВАННЫЙ ТЕКСТ (ОТ):**  
`ночьтихапустынявнемлетбогуизвездасзвездоюговорит`

**КЛЮЧ:**  
17

**АВТОР И ПРОИЗВЕДЕНИЕ (ОТ):**  
М. Ю. Лермонтов, «Выхожу один я на дорогу»

**ЗАШИФРОВАННЫЕ ФАМИЛИЯ И НАЗВАНИЕ (ШТ):**  
`ьцбэяюгяуумжячдяхщюрюсхябяфд`  
*(Исходный текст: «лермонтоввыхожуодинянадорогу», зашифрованный ключом $k = 17$)*

**Варианты расшифрования исходного ШТ при различных значениях ключа:**

$k = 1$: `эюзмвшерягбвлэптэхьыхвсюугшчтхчфрбчтхчфюоуютюашв`  
$k = 2$: `ьэжлбчдпювабкьосьфыъфбрэтвчцсфцупацсфцуэнтэсэячб`  
$k = 3$: `ыьекацгоэбяайынрыуъщуапьсбцхрухтояхрухтьмсьрьюца`  
$k = 4$: `ъыдйяхвньаюяиъмпътщштяоырахфптфснюфптфсылрыпыэхя`  
$k = 5$: `щъгиюфбмыяэюзщлощсшчсюнъпяфуосурмэуосуръкпъоъьфю`  
$k = 6$: `шщвзэуалъюьэжшкншрчцрэмщоюутнртпльтнртпщйощнщыуэ`  
$k = 7$: `чшбжьтякщэыьечймчпцхпьлшнэтсмпсокысмпсошиншмшъть`  
$k = 8$: `цчаеысюйшьъыдцилцохфоыкчмьсрлорнйърлорнчзмчлчщсы`  
$k = 9$: `хцядърэичыщъгхзкхнфунъйцлырпкнпмищпкнпмцжлцкцшръ`  
$k = 10$: `фхюгщпьзцъшщвфжйфмутмщихкъпоймолзшоймолхекхйхчпщ`  
$k = 11$: `уфэвшоыжхщчшбуеиултслшзфйщонилнкжчнилнкфдйфифцош`  
$k = 12$: `туьбчнъефшцчатдзтксркчжуишнмзкмйецмзкмйугиузухнч`  
$k = 13$: `стыацмщдучхцясгжсйрпйцетзчмлжйлидхлжйлитвзтжтфмц`  
$k = 14$: `рсъяхлшгтцфхюрверипоихдсжцлкеикзгфкеикзсбжсесулх`  
$k = 15$: `прщюфкчвсхуфэпбдпзонзфгрехкйдзйжвуйдзйжраердрткф`  
$k = 16$: `опшэуйцбрфтуьоагожнмжувпдфйигжиебтигжиепядпгпсйу`  
$k = 17$: `ночьтихапустынявнемлетбогуизвездасзвездоюговорит` *(ИСТИННЫЙ ТЕКСТ)*  
$k = 18$: `мнцысзфяотрсъмюбмдлкдсанвтзжбджгяржбджгнэвнбнпзс`  
$k = 19$: `лмхържуюнспрщлэалгкйгрямбсжеагевюпеагевмьбмаможр`  
$k = 20$: `клфщпетэмропшкьяквйивпюларедявдбэодявдблыалялнеп`  
$k = 21$: `йкушодсьлпночйыюйбизбоэкяпдгюбгаьнгюбгакъякюкмдо`  
$k = 22$: `ийтчнгрыкомнциъэиазжаньйюогвэавяымвэавяйщюйэйлгн`  
$k = 23$: `зисцмвпъйнлмхзщьзяжеямыиэнвбьябюълбьябюишэиьиквм`  
$k = 24$: `жзрхлбощимклфжшыжюедюлъзьмбаыюаэщкаыюаэзчьзызйбл`  
$k = 25$: `ежпфканшзлйкуечъеэдгэкщжылаяъэяьшйяъэяьжцыжъжиак`  
$k = 26$: `деоуйямчжкийтдцщдьгвьйшеъкяющьюычиющьюыехъещезяй`  
$k = 27$: `гднтиюлцейзисгхшгывбыичдщйюэшыэъцзэшыэъдфщдшджюи`  
$k = 28$: `вгмсзэкхдижзрвфчвъбаъзцгшиэьчъьщхжьчъьщгушгчгеэз`  
$k = 29$: `бвлржьйфгзежпбуцбщаящжхвчзьыцщышфеыцщышвтчвцвдьж`  
$k = 30$: `абкпеыиувждеоатхашяюшефбцжыъхшъчудъхшъчбсцбхбгые`  
$k = 31$: `яайодъзтбегднясфячюэчдуахеъщфчщцтгщфчщцархафавъд`

## Код программы

Листинг: Реализация алгоритмов прямого и обратного шифрования Цезаря и перебора ключей (caesar_cipher.py)
```python
from typing import Dict, List, Optional, Tuple


class Alphabet:
    def __init__(
        self,
        name: str,
        symbols: str,
        normalize_map: Optional[Dict[str, str]] = None,
        case_sensitive: bool = False
    ):
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
        self,
        char: str,
        k: int,
        case_mode: str = "lower",
        preserve_case: Optional[bool] = None
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
        self,
        char: str,
        k: int,
        case_mode: str = "lower",
        preserve_case: Optional[bool] = None
    ) -> str:
        return self.encrypt_symbol(char, -k, case_mode=case_mode, preserve_case=preserve_case)

    def prepare_canonical_text(self, text: str) -> str:
        return "".join(self.normalize_char(c) for c in text if self.normalize_char(c) in self.char_to_code)

    def encrypt(
        self,
        text: str,
        k: int,
        filter_non_alpha: bool = False,
        case_mode: str = "lower",
        preserve_case: Optional[bool] = None
    ) -> str:
        if preserve_case is not None:
            case_mode = "preserve" if preserve_case else "lower"
        if filter_non_alpha:
            src = self.prepare_canonical_text(text)
            return "".join(self.encrypt_symbol(c, k, case_mode="lower") for c in src)
        return "".join(self.encrypt_symbol(c, k, case_mode=case_mode) for c in text)

    def decrypt(
        self,
        text: str,
        k: int,
        case_mode: str = "lower",
        preserve_case: Optional[bool] = None
    ) -> str:
        return self.encrypt(text, -k, filter_non_alpha=False, case_mode=case_mode, preserve_case=preserve_case)

    def brute_force(
        self,
        ciphertext: str,
        filter_non_alpha: bool = False,
        case_mode: str = "lower"
    ) -> List[Tuple[int, str]]:
        return [
            (k, self.decrypt(ciphertext, k, case_mode=case_mode))
            for k in range(1, self.power)
        ]
```
