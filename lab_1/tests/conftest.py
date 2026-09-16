"""
Фикстуры pytest для тестирования лабораторной работы № 1.
"""

import pytest
from lab_1.caesar_cipher import VARIANTS_DB, ALPHABET_POWER, ALPHABET_SYMBOLS


@pytest.fixture
def alphabet_info():
    """Параметры и контрольная таблица кодирования алфавита (Таблица 1 методички)."""
    table = {
        'а': 0, 'б': 1, 'в': 2, 'г': 3, 'д': 4, 'е': 5, 'ж': 6, 'з': 7,
        'и': 8, 'й': 9, 'к': 10, 'л': 11, 'м': 12, 'н': 13, 'о': 14, 'п': 15,
        'р': 16, 'с': 17, 'т': 18, 'у': 19, 'ф': 20, 'х': 21, 'ц': 22, 'ч': 23,
        'ш': 24, 'щ': 25, 'ъ': 26, 'ы': 27, 'ь': 28, 'э': 29, 'ю': 30, 'я': 31
    }
    return {
        "power": ALPHABET_POWER,
        "symbols": ALPHABET_SYMBOLS,
        "table": table
    }


@pytest.fixture
def manual_example():
    """Контрольный пример из методических указаний (стр. 6-8)."""
    return {
        "ot": "асудьикто",
        "st": "шйльфавкж",
        "key": 24,
        "codes": [0, 17, 19, 4, 28, 8, 10, 18, 14],
        "author_work_ot": "грибоедовгореотума",
        "author_work_st": "ыиащжэьжъыжиэжклдш"
    }


@pytest.fixture
def variant_1_data():
    """Данные Варианта № 1 (Н. В. Гоголь, «Ревизор»)."""
    return VARIANTS_DB[1]


@pytest.fixture
def all_variants():
    """База данных всех 30 вариантов из методички."""
    return VARIANTS_DB
