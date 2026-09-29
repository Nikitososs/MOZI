"""
Модуль криптоанализа аффинного шифра:
- Частотный анализ текста (подсчет абсолютных и относительных частот);
- Генерация и аналитическое решение систем модулярных сравнений для пар частых букв;
- Лингвистическая оценка осмысленности расшифрованного текста;
- Процедура автоматического подбора ключа.
"""

from collections import Counter
import math
from typing import Any, Dict, List, Optional, Tuple

from lab_2.alphabet import Alphabet, DEFAULT_ALPHABET, RUSSIAN_FREQUENCIES
from lab_2.cipher import AffineCipher
from lab_2.math_utils import solve_system_congruences


def frequency_analysis(
    text: str,
    alphabet: Optional[Alphabet] = None
) -> Dict[str, Any]:
    """
    Выполняет частотный анализ символов текста.

    Возвращает структуру:
      - 'counts': Dict[символ, количество]
      - 'frequencies': Dict[символ, относительная частота]
      - 'sorted_chars': List[Tuple[символ, количество, частота]] по убыванию частоты
      - 'total_alpha_chars': общее количество букв алфавита в тексте
    """
    alpha = alphabet or DEFAULT_ALPHABET
    canonical = "".join(alpha.normalize_char(c) for c in text if alpha.normalize_char(c) in alpha.char_to_code)
    total = len(canonical)
    counts_map = Counter(canonical)

    frequencies = {}
    for sym in alpha.symbols:
        cnt = counts_map.get(sym, 0)
        frequencies[sym] = (cnt / total) if total > 0 else 0.0

    sorted_chars = sorted(
        [(sym, counts_map.get(sym, 0), frequencies[sym]) for sym in alpha.symbols],
        key=lambda x: x[1],
        reverse=True
    )

    return {
        "counts": counts_map,
        "frequencies": frequencies,
        "sorted_chars": sorted_chars,
        "total_alpha_chars": total
    }


def generate_hypotheses_systems(
    ciphertext: str,
    alphabet: Optional[Alphabet] = None,
    top_ct_count: int = 6,
    top_pt_count: int = 6
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
    top_ct = [item[0] for item in fa["sorted_chars"][:top_ct_count]]
    top_pt = [item[0] for item in RUSSIAN_FREQUENCIES[:top_pt_count]]

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

                    hypotheses.append({
                        "mapping": f"E({x1_char})={y1_char}, E({x2_char})={y2_char}",
                        "equations": f"({x1}a + b) ≡ {y1} (mod {m}); ({x2}a + b) ≡ {y2} (mod {m})",
                        "status": st,
                        "description": desc,
                        "valid_keys": valid_keys
                    })

    return hypotheses


_FREQ_DICT: Dict[str, float] = dict(RUSSIAN_FREQUENCIES)

# Наиболее частотные биграммы русского языка (НКРЯ / частотные словари)
_COMMON_BIGRAMS = {
    "ст", "но", "то", "на", "ен", "ов", "ни", "ра", "во", "ко",
    "ро", "по", "ал", "пр", "ос", "ли", "ес", "од", "не", "го",
    "ре", "ер", "от", "ва", "ла", "ет", "ит", "та", "те", "ти"
}

# Нехарактерные и запрещенные буквосочетания в русском языке
_FORBIDDEN_BIGRAMS = {
    "ъъ", "ьь", "ыь", "ъь", "ыы", "йь", "жы", "шы", "чя", "щя",
    "чю", "щю", "оы", "аы", "еы", "иы", "уы", "эы", "юы", "яы",
    "ьы", "ъы", "ъа", "ъо", "ъу", "ъэ", "ъи"
}

# Общеупотребительные служебные слова и союзы (частотный словарь русского языка)
_COMMON_WORDS = {
    "и", "в", "не", "на", "я", "с", "что", "а", "по", "он", "как",
    "то", "но", "мы", "к", "у", "вы", "за", "бы", "же", "от", "о",
    "из", "до", "да", "ли", "или", "если", "для", "при", "был", "ты",
    "все", "так", "его", "она", "они", "еще"
}


def score_russian_text(text: str) -> float:
    """
    Статистическая и n-граммная оценка правдоподобия русского текста:
    - скалярное произведение частот букв с эталонным распределением языка;
    - учет частотных биграмм русского языка;
    - штраф за запрещенные и невозможные буквосочетания;
    - наличие общеупотребительных служебных слов и морфем.
    """
    if not text:
        return 0.0

    n = len(text)
    counts = Counter(text)

    # 1. Корреляция монограмм с эталонными частотами русского языка
    freq_score = sum((counts[c] / n) * _FREQ_DICT.get(c, 0.0) for c in counts) * 1000.0

    # 2. Оценка биграмм и штраф за запрещенные сочетания
    bg_score = 0.0
    for i in range(n - 1):
        bg = text[i:i + 2]
        if bg in _COMMON_BIGRAMS:
            bg_score += 2.5
        elif bg in _FORBIDDEN_BIGRAMS:
            bg_score -= 25.0

    # 3. Наличие общеупотребительных слов (длиной >= 2)
    word_score = sum(text.count(w) * 1.5 for w in _COMMON_WORDS if len(w) >= 2)

    return freq_score + bg_score + word_score


def crack_affine_cipher(
    ciphertext: str,
    alphabet: Optional[Alphabet] = None,
    top_n: int = 5
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
            score = score_russian_text(dec_text)
            evaluated.append((score, (a, b), h["mapping"], dec_text))

    evaluated.sort(key=lambda item: item[0], reverse=True)
    return evaluated[:top_n]
