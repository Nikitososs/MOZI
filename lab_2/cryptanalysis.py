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

from lab_2.alphabet import Alphabet, DEFAULT_ALPHABET, RUSSIAN_FREQUENCIES, get_reference_frequencies
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

                    hypotheses.append({
                        "mapping": f"E({x1_char})={y1_char}, E({x2_char})={y2_char}",
                        "equations": f"({x1}a + b) ≡ {y1} (mod {m}); ({x2}a + b) ≡ {y2} (mod {m})",
                        "status": st,
                        "description": desc,
                        "valid_keys": valid_keys
                    })

    return hypotheses


_RU_FREQ_DICT: Dict[str, float] = dict(RUSSIAN_FREQUENCIES)
_RU_COMMON_BIGRAMS = {
    "ст", "но", "то", "на", "ен", "ов", "ни", "ра", "во", "ко",
    "ро", "по", "ал", "пр", "ос", "ли", "ес", "од", "не", "го",
    "ре", "ер", "от", "ва", "ла", "ет", "ит", "та", "те", "ти"
}
_RU_FORBIDDEN_BIGRAMS = {
    "ъъ", "ьь", "ыь", "ъь", "ыы", "йь", "жы", "шы", "чя", "щя",
    "чю", "щю", "оы", "аы", "еы", "иы", "уы", "эы", "юы", "яы",
    "ьы", "ъы", "ъа", "ъо", "ъу", "ъэ", "ъи"
}
_RU_COMMON_WORDS = {
    "и", "в", "не", "на", "я", "с", "что", "а", "по", "он", "как",
    "то", "но", "мы", "к", "у", "вы", "за", "бы", "же", "от", "о",
    "из", "до", "да", "ли", "или", "если", "для", "при", "был", "ты",
    "все", "так", "его", "она", "они", "еще"
}

_EN_COMMON_BIGRAMS = {
    "th", "he", "in", "er", "an", "re", "nd", "at", "on", "nt",
    "ha", "es", "st", "en", "ed", "to", "it", "ou", "ea", "hi",
    "is", "or", "ti", "as", "te", "et", "ng", "of", "al", "de"
}
_EN_FORBIDDEN_BIGRAMS = {
    "qj", "qx", "qz", "jq", "jx", "jz", "wq", "wv", "wx", "wz",
    "zj", "zq", "zx"
}
_EN_COMMON_WORDS = {
    "the", "be", "to", "of", "and", "a", "in", "that", "have", "i",
    "it", "for", "not", "on", "with", "he", "as", "you", "do", "at",
    "this", "but", "his", "by", "from", "they", "we", "say", "her",
    "she", "or", "an", "will", "my", "one", "all", "would", "there", "their"
}


def score_text(text: str, alphabet: Optional[Alphabet] = None) -> float:
    """
    Статистическая и n-граммная оценка правдоподобия расшифрованного текста
    с адаптацией под русский либо английский язык:
    - скалярное произведение частот букв с эталонным распределением языка;
    - учет характерных частых биграмм;
    - штраф за запрещенные и нехарактерные буквосочетания;
    - наличие общеупотребительных служебных слов и морфем.
    """
    if not text:
        return 0.0

    alpha = alphabet or DEFAULT_ALPHABET
    is_english = "e" in alpha.symbols or "a" in alpha.symbols

    lower_text = text.lower()
    n = len(lower_text)
    counts = Counter(lower_text)

    ref_freq_map = dict(get_reference_frequencies(alpha))
    freq_score = sum((counts[c] / n) * ref_freq_map.get(c, 0.0) for c in counts) * 1000.0

    common_bigrams = _EN_COMMON_BIGRAMS if is_english else _RU_COMMON_BIGRAMS
    forbidden_bigrams = _EN_FORBIDDEN_BIGRAMS if is_english else _RU_FORBIDDEN_BIGRAMS
    common_words = _EN_COMMON_WORDS if is_english else _RU_COMMON_WORDS

    bg_score = 0.0
    for i in range(n - 1):
        bg = lower_text[i:i + 2]
        if bg in common_bigrams:
            bg_score += 2.5
        elif bg in forbidden_bigrams:
            bg_score -= 25.0

    word_score = sum(lower_text.count(w) * 1.5 for w in common_words if len(w) >= 2)

    return freq_score + bg_score + word_score


def score_russian_text(text: str) -> float:
    """Обратная совместимость: оценка текста по критериям русского языка."""
    return score_text(text, DEFAULT_ALPHABET)


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
            score = score_text(dec_text, alpha)
            evaluated.append((score, (a, b), h["mapping"], dec_text))

    evaluated.sort(key=lambda item: item[0], reverse=True)
    return evaluated[:top_n]
