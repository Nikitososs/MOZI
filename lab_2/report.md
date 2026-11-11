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
  "title": "Криптоанализ аффинного шифра",
  "work": {
    "type": "Лабораторная работа № 2",
    "variant": "16"
  }
}
}}

# СОДЕРЖАНИЕ

# ОСНОВНАЯ ЧАСТЬ

## Результаты частотного криптоанализа варианта 16

Длина шифр-текста — 168 символов. Частота вычислена как число вхождений буквы, делённое на длину текста.

Шифр-текст: `взщэоюнщмфасзедшоэзгждюзцоиынщэтдцнтсзтзщмнгюцохецфшзгшзшмзгждщнгмзщнгмзужпщфхбсфмтужвзщзымзсшгзфашгфуцеяжюзэчфхбиощузмнъншндесфщцтувзсемоумзшвеяжгугзедмнсзэрфммждэоынд`

Таблица: Частоты символов шифр-текста

| Буква | Количество | Относительная частота |
|:---:|---:|---:|
| а | 2 | 0.011905 |
| б | 2 | 0.011905 |
| в | 4 | 0.023810 |
| г | 10 | 0.059524 |
| д | 8 | 0.047619 |
| е | 7 | 0.041667 |
| ж | 7 | 0.041667 |
| з | 21 | 0.125000 |
| и | 2 | 0.011905 |
| й | 0 | 0.000000 |
| к | 0 | 0.000000 |
| л | 0 | 0.000000 |
| м | 13 | 0.077381 |
| н | 11 | 0.065476 |
| о | 7 | 0.041667 |
| п | 1 | 0.005952 |
| р | 1 | 0.005952 |
| с | 7 | 0.041667 |
| т | 5 | 0.029762 |
| у | 7 | 0.041667 |
| ф | 9 | 0.053571 |
| х | 3 | 0.017857 |
| ц | 6 | 0.035714 |
| ч | 1 | 0.005952 |
| ш | 8 | 0.047619 |
| щ | 10 | 0.059524 |
| ъ | 1 | 0.005952 |
| ы | 3 | 0.017857 |
| ь | 0 | 0.000000 |
| э | 6 | 0.035714 |
| ю | 4 | 0.023810 |
| я | 2 | 0.011905 |

Наиболее частые символы шифр-текста: `з` — 21, `м` — 13, `н` — 11. Проверяем гипотезу $E(о)=з$, $E(н)=м$. При кодах $о=14$, $н=13$, $з=7$, $м=12$ получаем систему:

$$
14a+b\equiv7\pmod{32},\qquad13a+b\equiv12\pmod{32}.
$$

Вычитание уравнений даёт $a\equiv-5\equiv27\pmod{32}$. Подстановка даёт $b\equiv7-14\cdot27\equiv13\pmod{32}$. Поскольку $\gcd(27,32)=1$, ключ допустим; $27^{-1}\bmod32=19$. Расшифрование выполняется по формуле $x=19(y-13)\bmod32$.

- ключ: $(a,b)=(27,13)$;
- открытый текст: `подругаднеймоихсуровыхголубкадряхлаямояоднавглушилесовсосновыхдавнодавнотыждешьменятыподокномсвоейсветлицыгорюешьбудтоначасахимедлятпоминутноспицывтвоихнаморщенныхруках`;
- автор и произведение: Александр Сергеевич Пушкин, «Няне».

Частотный анализ, построение гипотез и проверка ключей реализованы в `lab_2/cryptanalysis.py`; арифметика и преобразования — в модулях `lab_2/math_utils.py` и `lab_2/cipher.py`.


## Работа приложения

Запуск: `python -m lab_2.main`. В главном меню доступны шифрование и расшифрование с ключом $(a,b)$, частотный криптоанализ, решение варианта 16, математические операции и переключение русского/английского алфавита. Текст вводится с клавиатуры или из файла. При криптоанализе программа считает частоты, строит системы сравнений для гипотез о буквах, отбрасывает недопустимые ключи и ранжирует расшифровки. В режиме варианта она выводит протокол и сохраняет результат в каталоге `lab_2/outputs/`.

# СПИСОК ЛИТЕРАТУРЫ

- Математические основы защиты информации : методические указания к лабораторным работам / Минобрнауки России, Омский государственный технический университет ; составители С. Ю. Белим, С. В. Белим. — Омск : Издательство ОмГТУ, 2023. — С. 13–23, приложение 2. — Текст : электронный.

# ПРИЛОЖЕНИЯ

## Приложение А. Фрагмент исходного кода `cryptanalysis.py`

Частотный профиль, построение допустимых ключей и отбор расшифровок. Фрагмент использует `score_text`, класс `AffineCipher` и решатель сравнений, реализованные в соседних частях проекта. Полная реализация вспомогательной оценки `score_text` находится в `lab_2/cryptanalysis.py`; здесь приведён фрагмент, который вызывает её для ранжирования кандидатов.

Листинг: Основные функции модуля `cryptanalysis.py`

```python
from collections import Counter
import math
from typing import Any, Dict, List, Optional, Tuple

from lab_2.alphabet import Alphabet, DEFAULT_ALPHABET, RUSSIAN_FREQUENCIES, get_reference_frequencies
from lab_2.cipher import AffineCipher
from lab_2.math_utils import solve_system_congruences


def frequency_analysis(text: str, alphabet: Optional[Alphabet] = None) -> Dict[str, Any]:
    """
    Выполняет частотный анализ символов текста.

    Возвращает структуру:
      - 'counts': Dict[символ, количество]
      - 'frequencies': Dict[символ, относительная частота]
      - 'sorted_chars': List[Tuple[символ, количество, частота]] по убыванию частоты
      - 'total_alpha_chars': общее количество букв алфавита в тексте
    """
    alpha = alphabet or DEFAULT_ALPHABET
    canonical = "".join(
        alpha.normalize_char(c) for c in text if alpha.normalize_char(c) in alpha.char_to_code
    )
    total = len(canonical)
    counts_map = Counter(canonical)

    frequencies = {}
    for sym in alpha.symbols:
        cnt = counts_map.get(sym, 0)
        frequencies[sym] = (cnt / total) if total > 0 else 0.0

    sorted_chars = sorted(
        [(sym, counts_map.get(sym, 0), frequencies[sym]) for sym in alpha.symbols],
        key=lambda x: x[1],
        reverse=True,
    )

    return {
        "counts": counts_map,
        "frequencies": frequencies,
        "sorted_chars": sorted_chars,
        "total_alpha_chars": total,
    }

def generate_hypotheses_systems(
    ciphertext: str,
    alphabet: Optional[Alphabet] = None,
    top_ct_count: int = 2,
    top_pt_count: int = 6,
) -> List[Dict[str, Any]]:
    """
    Формирует и аналитически решает системы сравнений:
      (x1 * a + b) ≡ y1 (mod m)
      (x2 * a + b) ≡ y2 (mod m)
    где (y1, y2) — пара частых символов шифр-текста, а (x1, x2) — пара частых букв языка.
    """
    alpha = alphabet or DEFAULT_ALPHABET
    m = alpha.power
    fa = frequency_analysis(ciphertext, alpha)
    if fa["total_alpha_chars"] == 0:
        return []

    # Берем только фактически встретившиеся в шифр-тексте символы алфавита
    non_zero_ct = [item[0] for item in fa["sorted_chars"] if item[1] > 0]
    if len(non_zero_ct) < 2:
        return []

    top_ct = non_zero_ct[:top_ct_count]
    ref_freq = get_reference_frequencies(alpha)
    top_pt = [item[0] for item in ref_freq[:top_pt_count] if item[0] in alpha.char_to_code]
    if len(top_pt) < 2:
        return []

    hypotheses: List[Dict[str, Any]] = []

    for i in range(len(top_ct)):
        for j in range(i + 1, len(top_ct)):
            y1_char, y2_char = top_ct[i], top_ct[j]
            y1, y2 = alpha.A(y1_char), alpha.A(y2_char)

            for p1_idx in range(len(top_pt)):
                for p2_idx in range(len(top_pt)):
                    if p1_idx == p2_idx:
                        continue
                    x1_char, x2_char = top_pt[p1_idx], top_pt[p2_idx]
                    x1, x2 = alpha.A(x1_char), alpha.A(x2_char)

                    st, solutions, desc = solve_system_congruences(x1, y1, x2, y2, m)
                    valid_keys = [(a, b) for a, b in solutions if math.gcd(a, m) == 1]

                    hypotheses.append(
                        {
                            "mapping": f"E({x1_char})={y1_char}, E({x2_char})={y2_char}",
                            "equations": f"({x1}a + b) ≡ {y1} (mod {m}); ({x2}a + b) ≡ {y2} (mod {m})",
                            "status": st,
                            "description": desc,
                            "valid_keys": valid_keys,
                        }
                    )

    return hypotheses

def crack_affine_cipher(
    ciphertext: str, alphabet: Optional[Alphabet] = None, top_n: int = 5
) -> List[Tuple[float, Tuple[int, int], str, str]]:
    """
    Автоматический криптоанализ аффинного шифра:
    перебор сформированных гипотез, дешифрование и ранжирование по баллу осмысленности.
    Возвращает список кортежей: (score, (a, b), mapping, decrypted_preview).
    """
    alpha = alphabet or DEFAULT_ALPHABET
    cipher = AffineCipher(alpha)
    hypotheses = generate_hypotheses_systems(ciphertext, alpha)

    evaluated = []
    seen_keys = set()

    for h in hypotheses:
        for a, b in h["valid_keys"]:
            if (a, b) in seen_keys:
                continue
            seen_keys.add((a, b))
            dec_text = cipher.decrypt(ciphertext, a, b)
            score = score_text(dec_text, alpha)
            evaluated.append((score, (a, b), h["mapping"], dec_text))

    evaluated.sort(key=lambda item: item[0], reverse=True)
    return evaluated[:top_n]
```
