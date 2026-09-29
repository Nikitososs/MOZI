{{json
{
  "discipline": "Математические основы защиты информации",
  "title": "Криптоанализ аффинного шифра",
  "student": {"name": "Смирнов Никита Михайлович", "course": "2", "group": "ФИТ-242", "program": "02.03.02 Фундаментальная информатика и информационные технологии"},
  "teacher": {"title": "канд. пед. наук, доцент", "name": "Белим Светлана Юрьевна"},
  "institution": {"short": "ОмГТУ", "department": "ПМиФИ", "year": "2026"},
  "work": {"type": "Лабораторная работа № 2", "variant": "16"}
}
}}

# ПРИЛОЖЕНИЕ 2. ОТЧЕТ К ЛАБОРАТОРНОЙ РАБОТЕ № 2

**Лабораторная работа № 2**  
**Криптоанализ аффинного шифра**  
**Вариант №** 16  
**Ф. И. О. студента:** Смирнов Никита Михайлович  
**Группа:** ФИТ-242  
**Проверил:** Белим Светлана Юрьевна  
**Дата:** 29.09.2026  

## Основные сведения

**Формула для зашифрования текста:**

$$y = (a \cdot x + b) \pmod m$$

**Формула для расшифрования текста:**

$$x = a^{-1} \cdot (y - b) \pmod m$$

где $x \in \{0, 1, \dots, m - 1\}$ — числовой код символа открытого сообщения, $y \in \{0, 1, \dots, m - 1\}$ — числовой код символа зашифрованного сообщения, $(a, b)$ — секретный ключ шифрования, $m = 32$ — мощность используемого алфавита (буквы «е» и «ё» объединены). Числовой параметр $a$ должен быть взаимно прост с модулем ($\gcd(a, m) = 1$). Мультипликативно обратный элемент $a^{-1}$ вычисляется с помощью расширенного алгоритма Евклида из тождества Безу: $a \cdot u + m \cdot v = 1$, откуда $a^{-1} = u \pmod m$. Сдвиговый параметр $b$ может принимать любое значение из $\{0, 1, \dots, m - 1\}$.

## Результаты

**ШИФР-ТЕКСТ (ШТ):**  
`эздмоуздрькзэеюхмоыбзсуыжздрякзйзсьздрзвмущорызвзсьзвмоузьздрьзвмоуызюяьемоызвмоущвьузвмоуюзвтмуцыгоомсудздьздрзвмущорызвзсьзвмоуызюяьемоызвмоущвьузвмоу`

**Результаты частотного анализа ШТ:**

Таблица: Результаты частотного анализа шифр-текста варианта 16 (символы а – й)
| буква | а | б | в | г | д | е/ё | ж | з | и | й |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| частота | 0.012 | 0.012 | 0.024 | 0.060 | 0.048 | 0.042 | 0.042 | 0.125 | 0.012 | 0.000 |

Таблица: Результаты частотного анализа шифр-текста варианта 16 (символы к – у)
| буква | к | л | м | н | о | п | р | с | т | у |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| частота | 0.000 | 0.000 | 0.077 | 0.065 | 0.042 | 0.006 | 0.006 | 0.042 | 0.030 | 0.042 |

Таблица: Результаты частотного анализа шифр-текста варианта 16 (символы ф – э)
| буква | ф | х | ц | ч | ш | щ | ъ | ы | ь | э |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| частота | 0.054 | 0.018 | 0.036 | 0.006 | 0.048 | 0.060 | 0.006 | 0.018 | 0.000 | 0.036 |

Таблица: Результаты частотного анализа шифр-текста варианта 16 (символы ю – я)
| буква | ю | я |
| :---: | :---: | :---: |
| частота | 0.024 | 0.012 |

**Наиболее часто встречающиеся символы:**  
- В шифр-тексте (ШТ): `'з'` (21 раз, частота 0.125), `'м'` (13 раз, частота 0.077), `'н'` (11 раз, частота 0.065), `'г'` (10 раз, частота 0.060), `'щ'` (10 раз, частота 0.060), `'ф'` (9 раз, частота 0.054).  
- В русском языке (ОТ, Таблица 3 методических указаний): `'о'` (частота 0.090), `'е'` (частота 0.072), `'а'` (частота 0.062), `'и'` (частота 0.062), `'т'` (частота 0.053), `'н'` (частота 0.053).

**Системы уравнений:**  
На основе частотного анализа выдвигаются гипотезы о соответствии наиболее частых символов открытого текста наиболее частым символам шифр-текста. Преобразование шифрования порождает систему из двух линейных сравнений:
$$\begin{cases} (x_1 \cdot a + b) \equiv y_1 \pmod m \\ (x_2 \cdot a + b) \equiv y_2 \pmod m \end{cases}$$
где $x_1, x_2$ — числовые индексы предполагаемых букв открытого текста, $y_1, y_2$ — числовые индексы наблюдаемых букв шифр-текста, $m = 32$.

Для гипотезы соответствия $E(\text{'о'}) = \text{'з'}$ и $E(\text{'е'}) = \text{'м'}$ при кодах $x_1 = A(\text{'о'}) = 14$, $y_1 = A(\text{'з'}) = 7$, $x_2 = A(\text{'е'}) = 5$, $y_2 = A(\text{'м'}) = 12$ формируется система:
$$\begin{cases} 14a + b \equiv 7 \pmod{32} \\ 5a + b \equiv 12 \pmod{32} \end{cases}$$

Для гипотезы соответствия $E(\text{'д'}) = \text{'з'}$ и $E(\text{'а'}) = \text{'м'}$ при кодах $x_1 = 4, y_1 = 7, x_2 = 0, y_2 = 12$:
$$\begin{cases} 4a + b \equiv 7 \pmod{32} \\ 0a + b \equiv 12 \pmod{32} \end{cases}$$

**Решения систем уравнений:**  
1. Решение системы для гипотезы $E(\text{'о'}) = \text{'з'}$, $E(\text{'е'}) = \text{'м'}$:
Вычитаем второе уравнение из первого:
$$(14 - 5)a \equiv (7 - 12) \pmod{32} \iff 9a \equiv -5 \equiv 27 \pmod{32}$$
Так как $\gcd(9, 32) = 1$, элемент 9 обратим в $\mathbb{Z}_{32}$. Находим обратный элемент расширенным алгоритмом Евклида:
$$9 \cdot (-7) + 32 \cdot 2 = 1 \implies 9^{-1} \equiv -7 \equiv 25 \pmod{32}$$
Умножаем обе части сравнения на 25:
$$a \equiv 25 \cdot 27 = 675 \equiv 27 \pmod{32}$$
Подставляем $a = 27$ во второе уравнение системы:
$$b \equiv 12 - 5 \cdot 27 = 12 - 135 = -123 \equiv 13 \pmod{32}$$
Проверяем взаимную простоту ключа: $\gcd(27, 32) = 1$. Ключ $(a, b) = (27, 13)$ обратим и корректен.

2. Решение системы для гипотезы $E(\text{'д'}) = \text{'з'}$, $E(\text{'а'}) = \text{'м'}$:
$$b \equiv 12 \pmod{32}, \quad 4a \equiv 7 - 12 \equiv 27 \pmod{32}$$
Так как $\gcd(4, 32) = 4$, а число 27 не делится на 4 ($27 \bmod 4 = 3 \neq 0$), сравнение решений не имеет.

**ВЕРНЫЙ КЛЮЧ:**  
$a = 27, \quad b = 13$

**РАСШИФРОВАННЫЙ ТЕКСТ (ОТ):**  
`подругаднеймоихсуровыхголубкадряхлаямояоднавглушилесовсосновыхдавнодавнотыждешьменятыподокномсвоейсветлицыгорюешьбудтоначасахимедлятпоминутноспицывтвоихнаморщенныхруках`  
*(А. С. Пушкин, «Няне»)*

## Код программы

Листинг: Математический аппарат расширенного алгоритма Евклида и модулярных сравнений (math_utils.py)
```python
from typing import List, Optional, Tuple


def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    """Расширенный алгоритм Евклида: d = gcd(a,b), a*u + b*v = d."""
    if b == 0:
        sign = 1 if a >= 0 else -1
        return a * sign, sign, 0

    u0, u1 = 1, 0
    v0, v1 = 0, 1
    r0, r1 = a, b

    while r1 != 0:
        q = r0 // r1
        r0, r1 = r1, r0 - q * r1
        u0, u1 = u1, u0 - q * u1
        v0, v1 = v1, v0 - q * v1

    if r0 < 0:
        r0, u0, v0 = -r0, -u0, -v0

    return r0, u0, v0


def mod_inverse(a: int, m: int) -> Tuple[bool, Optional[int], Optional[int], str]:
    """Нахождение мультипликативно обратного элемента: (is_inv, u, pos_inv, desc)."""
    if m <= 0:
        raise ValueError(f"Модуль m должен быть положительным (получено {m})")

    d, u, _ = extended_gcd(a, m)
    if d != 1:
        return False, None, None, f"Необратимо: НОД({a}, {m}) = {d} ≠ 1"

    pos_inv = u % m
    return True, u, pos_inv, f"Обратимо: u = {u}, a^(-1) mod {m} = {pos_inv}"


def solve_linear_congruence(a: int, b: int, m: int) -> Tuple[int, List[int], str]:
    """Решение сравнения a*x ≡ b (mod m): (status, solutions, desc)."""
    d, u, _ = extended_gcd(a, m)
    b_mod = b % m

    if b_mod % d != 0:
        return 1, [], f"1. Решений нет: b={b} не делится на d={d}"

    m_prime = m // d
    a_prime = (a % m) // d
    b_prime = b_mod // d

    _, u_prime, _ = extended_gcd(a_prime, m_prime)
    x0 = (u_prime * b_prime) % m_prime
    solutions = sorted([(x0 + k * m_prime) % m for k in range(d)])

    status = 2 if d == 1 else 3
    return status, solutions, f"{status}. Найдено решений: {len(solutions)}"


def solve_system_congruences(
    a1: int, b1: int, a2: int, b2: int, m: int
) -> Tuple[int, List[Tuple[int, int]], str]:
    """Решение системы (a1*x + y ≡ b1, a2*x + y ≡ b2 mod m): (status, solutions, desc)."""
    da = (a1 - a2) % m
    db = (b1 - b2) % m

    st, x_solutions, _ = solve_linear_congruence(da, db, m)
    if st == 1:
        return 1, [], "1. Решений нет"

    pairs = []
    for x in x_solutions:
        y = (b1 - a1 * x) % m
        pairs.append((x, y))

    status = 2 if len(pairs) == 1 else 3
    return status, pairs, f"{status}. Найдено пар решений: {len(pairs)}"
```

Листинг: Реализация аффинного шифра (cipher.py)
```python
import math
from typing import List, Optional, Tuple
from lab_2.alphabet import Alphabet, DEFAULT_ALPHABET
from lab_2.math_utils import mod_inverse


class AffineCipher:
    def __init__(self, alphabet: Optional[Alphabet] = None):
        self.alphabet = alphabet or DEFAULT_ALPHABET
        self.power = self.alphabet.power

    def validate_key(self, a: int) -> None:
        gcd_val = math.gcd(a, self.power)
        if gcd_val != 1:
            raise ValueError(f"Коэффициент a={a} необратим по модулю m={self.power} (НОД={gcd_val} ≠ 1)")

    def E_k(self, x: int, a: int, b: int) -> int:
        self.validate_key(a)
        return (a * x + b) % self.power

    def D_k(self, y: int, a: int, b: int) -> int:
        is_inv, _, a_inv, _ = mod_inverse(a, self.power)
        if not is_inv or a_inv is None:
            raise ValueError(f"Коэффициент a={a} необратим по модулю m={self.power}")
        return (a_inv * (y - b)) % self.power

    def encrypt_symbol(self, char: str, a: int, b: int, case_mode: str = "lower") -> str:
        norm = self.alphabet.normalize_char(char)
        if norm in self.alphabet.char_to_code:
            code_x = self.alphabet.char_to_code[norm]
            code_y = self.E_k(code_x, a, b)
            res_char = self.alphabet.A_inv(code_y)
            if case_mode == "preserve":
                return res_char.upper() if char.isupper() else res_char.lower()
            elif case_mode == "upper":
                return res_char.upper()
            return res_char.lower()
        return char

    def decrypt_symbol(self, char: str, a: int, b: int, case_mode: str = "lower") -> str:
        norm = self.alphabet.normalize_char(char)
        if norm in self.alphabet.char_to_code:
            code_y = self.alphabet.char_to_code[norm]
            code_x = self.D_k(code_y, a, b)
            res_char = self.alphabet.A_inv(code_x)
            if case_mode == "preserve":
                return res_char.upper() if char.isupper() else res_char.lower()
            elif case_mode == "upper":
                return res_char.upper()
            return res_char.lower()
        return char

    def encrypt(self, text: str, a: int, b: int, filter_non_alpha: bool = False, case_mode: str = "lower") -> str:
        if filter_non_alpha:
            src = self.alphabet.prepare_canonical_text(text)
            return "".join(self.encrypt_symbol(c, a, b, case_mode="lower") for c in src)
        return "".join(self.encrypt_symbol(c, a, b, case_mode=case_mode) for c in text)

    def decrypt(self, text: str, a: int, b: int, case_mode: str = "lower") -> str:
        return "".join(self.decrypt_symbol(c, a, b, case_mode=case_mode) for c in text)

    def brute_force(self, ciphertext: str) -> List[Tuple[Tuple[int, int], str]]:
        valid_a_values = [a for a in range(1, self.power) if math.gcd(a, self.power) == 1]
        results = []
        for a in valid_a_values:
            for b in range(self.power):
                results.append(((a, b), self.decrypt(ciphertext, a, b)))
        return results
```

Листинг: Частотный анализ, решение систем гипотез и ранжирование ключей (cryptanalysis.py)
```python
from collections import Counter
import math
from typing import Any, Dict, List, Optional, Tuple
from lab_2.alphabet import Alphabet, DEFAULT_ALPHABET, RUSSIAN_FREQUENCIES
from lab_2.cipher import AffineCipher
from lab_2.math_utils import solve_system_congruences

_FREQ_DICT: Dict[str, float] = dict(RUSSIAN_FREQUENCIES)
_COMMON_BIGRAMS = {
    "ст", "но", "то", "на", "ен", "ов", "ни", "ра", "во", "ко",
    "ро", "по", "ал", "пр", "ос", "ли", "ес", "од", "не", "го",
    "ре", "ер", "от", "ва", "ла", "ет", "ит", "та", "те", "ти"
}
_FORBIDDEN_BIGRAMS = {
    "ъъ", "ьь", "ыь", "ъь", "ыы", "йь", "жы", "шы", "чя", "щя",
    "чю", "щю", "оы", "аы", "еы", "иы", "уы", "эы", "юы", "яы",
    "ьы", "ъы", "ъа", "ъо", "ъу", "ъэ", "ъи"
}
_COMMON_WORDS = {
    "и", "в", "не", "на", "я", "с", "что", "а", "по", "он", "как",
    "то", "но", "мы", "к", "у", "вы", "за", "бы", "же", "от", "о",
    "из", "до", "да", "ли", "или", "если", "для", "при", "был", "ты",
    "все", "так", "его", "она", "они", "еще"
}


def frequency_analysis(text: str, alphabet: Optional[Alphabet] = None) -> Dict[str, Any]:
    alpha = alphabet or DEFAULT_ALPHABET
    canonical = alpha.prepare_canonical_text(text)
    total = len(canonical)
    counts = Counter(canonical)
    freqs = {c: counts.get(c, 0) / total if total > 0 else 0.0 for c in alpha.symbols}
    sorted_items = sorted([(c, counts.get(c, 0), freqs[c]) for c in alpha.symbols], key=lambda x: x[1], reverse=True)
    return {
        "counts": dict(counts),
        "frequencies": freqs,
        "sorted_chars": sorted_items,
        "total_alpha_chars": total
    }


def generate_hypotheses_systems(ciphertext: str, alphabet: Optional[Alphabet] = None, top_ct_count: int = 6, top_pt_count: int = 6) -> List[Dict[str, Any]]:
    alpha = alphabet or DEFAULT_ALPHABET
    m = alpha.power
    fa = frequency_analysis(ciphertext, alpha)
    top_ct = [item[0] for item in fa["sorted_chars"][:top_ct_count]]
    top_pt = [item[0] for item in RUSSIAN_FREQUENCIES[:top_pt_count]]

    hypotheses = []
    for y1_char in top_ct:
        for y2_char in top_ct:
            if y1_char == y2_char: continue
            for x1_char in top_pt:
                for x2_char in top_pt:
                    if x1_char == x2_char: continue
                    x1, x2 = alpha.A(x1_char), alpha.A(x2_char)
                    y1, y2 = alpha.A(y1_char), alpha.A(y2_char)
                    st, solutions, desc = solve_system_congruences(x1, y1, x2, y2, m)
                    valid_keys = [(a, b) for a, b in solutions if math.gcd(a, m) == 1]
                    hypotheses.append({
                        "mapping": f"E({x1_char})={y1_char}, E({x2_char})={y2_char}",
                        "status": st,
                        "description": desc,
                        "valid_keys": valid_keys
                    })
    return hypotheses


def score_russian_text(text: str) -> float:
    if not text: return 0.0
    n = len(text)
    counts = Counter(text)
    freq_score = sum((counts[c] / n) * _FREQ_DICT.get(c, 0.0) for c in counts) * 1000.0
    bg_score = 0.0
    for i in range(n - 1):
        bg = text[i:i + 2]
        if bg in _COMMON_BIGRAMS: bg_score += 2.5
        elif bg in _FORBIDDEN_BIGRAMS: bg_score -= 25.0
    word_score = sum(text.count(w) * 1.5 for w in _COMMON_WORDS if len(w) >= 2)
    return freq_score + bg_score + word_score


def crack_affine_cipher(ciphertext: str, alphabet: Optional[Alphabet] = None, top_n: int = 5) -> List[Tuple[float, Tuple[int, int], str, str]]:
    alpha = alphabet or DEFAULT_ALPHABET
    cipher = AffineCipher(alpha)
    hypotheses = generate_hypotheses_systems(ciphertext, alpha)
    evaluated = []
    seen = set()
    for h in hypotheses:
        for a, b in h["valid_keys"]:
            if (a, b) in seen: continue
            seen.add((a, b))
            dec_text = cipher.decrypt(ciphertext, a, b)
            score = score_russian_text(dec_text)
            evaluated.append((score, (a, b), h["mapping"], dec_text))
    evaluated.sort(key=lambda x: x[0], reverse=True)
    return evaluated[:top_n]
```
