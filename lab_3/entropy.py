"""Предобработка и эмпирическая энтропия перекрывающихся k-грамм."""

from collections import Counter
from dataclasses import dataclass
from math import fsum, log2

from lab_2.alphabet import get_alphabet


@dataclass
class GramStatistics:
    """Число окон, абсолютные частоты и энтропия для одного k."""

    k: int
    counts: Counter[str]
    total: int
    entropy: float | None

    @property
    def normalized(self) -> float | None:
        """Средняя энтропия на символ Hk/k; None при отсутствии окон."""
        return None if self.entropy is None else self.entropy / self.k


def prepare_text(text: str, language: str = "ru") -> str:
    """Склеить буквы выбранного алфавита, учитывая нормализацию ЛР2."""
    return get_alphabet(language).prepare_canonical_text(text)


def analyze(text: str) -> list[GramStatistics]:
    """Рассчитать частоты и Hk для k=1..5 по уже очищенной строке.

    Окна идут с шагом 1. Знаменатель вероятности равен N-k+1.
    Короткий текст не дополняется символами; неполных окон нет.
    """
    if not text:
        raise ValueError("После предобработки не осталось букв выбранного языка.")
    results = []
    for k in range(1, 6):
        counts = Counter(text[i:i + k] for i in range(len(text) - k + 1))
        total = sum(counts.values())
        entropy = (
            -fsum((n / total) * log2(n / total) for n in counts.values())
            if total else None
        )
        results.append(GramStatistics(k, counts, total, entropy))
    return results
