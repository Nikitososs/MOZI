"""Проверки частот, знаменателя вероятностей и граничных входов."""

import math
import pytest
from lab_3.entropy import analyze, prepare_text


def test_preprocessing():
    assert prepare_text("Ёж, ЕЖ! Abc 123\nЯ") == "ежежя"
    assert prepare_text("Ёж, AbC! 123", "en") == "abc"


def test_overlapping_windows():
    results = analyze("абаба")
    assert results[1].counts == {"аб": 2, "ба": 2}
    assert results[1].total == 4
    assert results[1].entropy == 1
    assert results[1].normalized == 0.5
    assert results[0].entropy == pytest.approx(
        -0.6 * math.log2(0.6) - 0.4 * math.log2(0.4))
    assert [r.total for r in results] == [5, 4, 3, 2, 1]


def test_constant_and_short_text():
    assert all(r.entropy == 0 for r in analyze("аааааа"))
    results = analyze("а")
    assert results[0].entropy == 0
    assert all(r.entropy is None and r.normalized is None for r in results[1:])


def test_empty_text():
    with pytest.raises(ValueError):
        analyze(prepare_text("123!?"))


def test_simple_substitution_preserves_entropy():
    text = "абракадабра"
    encoded = text.translate(str.maketrans("абркд", "вгжзе"))
    assert [r.entropy for r in analyze(text)] == [r.entropy for r in analyze(encoded)]
