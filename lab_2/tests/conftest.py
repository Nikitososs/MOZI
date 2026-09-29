import pytest
from lab_2 import affine_cipher as ac
from lab_2.variants import VARIANTS_DB


@pytest.fixture
def alphabet_info():
    table = {
        'а': 0, 'б': 1, 'в': 2, 'г': 3, 'д': 4, 'е': 5, 'ж': 6, 'з': 7,
        'и': 8, 'й': 9, 'к': 10, 'л': 11, 'м': 12, 'н': 13, 'о': 14, 'п': 15,
        'р': 16, 'с': 17, 'т': 18, 'у': 19, 'ф': 20, 'х': 21, 'ц': 22, 'ч': 23,
        'ш': 24, 'щ': 25, 'ъ': 26, 'ы': 27, 'ь': 28, 'э': 29, 'ю': 30, 'я': 31
    }
    return {
        "power": ac.DEFAULT_ALPHABET.power,
        "symbols": ac.DEFAULT_ALPHABET.symbols,
        "table": table
    }


@pytest.fixture
def variant_16_data():
    return VARIANTS_DB[16]


@pytest.fixture
def manual_examples():
    return {
        "ex1_sys1": {"a": 14, "b": 8, "c": 5, "d": 19, "m": 32, "expected_key": (13, 18)},
        "ex1_sys2": {"a": 14, "b": 19, "c": 5, "d": 8, "m": 32, "expected_key": (19, 9)},
        "ex2_sys1": {"a": 8, "b": 9, "c": 0, "d": 15, "m": 32, "has_solution": False},
        "ex2_sys2": {"a": 0, "b": 9, "c": 8, "d": 15, "m": 32, "has_solution": False}
    }
