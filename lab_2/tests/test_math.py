"""Тесты для модуля math_utils: расширенный алгоритм Евклида, обратный элемент, сравнения, системы."""

import math
import pytest

from lab_2.math_utils import (
    extended_gcd,
    mod_inverse,
    solve_linear_congruence,
    solve_system_congruences
)


class TestExtendedEuclid:
    """Тестирование расширенного алгоритма Евклида."""

    @pytest.mark.parametrize("a, b", [
        (27, 32),
        (9, 32),
        (14, 32),
        (5, 32),
        (100, 35),
        (17, 19),
        (48, 18),
        (1, 1),
        (0, 5),
        (7, 0)
    ])
    def test_bezout_identity(self, a, b):
        d, u, v = extended_gcd(a, b)
        expected_gcd = math.gcd(a, b)
        assert d == expected_gcd
        assert a * u + b * v == d


class TestModInverse:
    """Тестирование вычисления мультипликативно обратного элемента."""

    @pytest.mark.parametrize("a, m, expected_inv", [
        (1, 32, 1),
        (3, 32, 11),
        (5, 32, 13),
        (7, 32, 23),
        (9, 32, 25),
        (11, 32, 3),
        (13, 32, 5),
        (15, 32, 15),
        (17, 32, 17),
        (19, 32, 27),
        (21, 32, 29),
        (23, 32, 7),
        (25, 32, 9),
        (27, 32, 19),
        (29, 32, 21),
        (31, 32, 31),
    ])
    def test_invertible_elements(self, a, m, expected_inv):
        is_inv, u, pos_inv, desc = mod_inverse(a, m)
        assert is_inv is True
        assert pos_inv == expected_inv
        assert (a * pos_inv) % m == 1

    @pytest.mark.parametrize("a, m", [
        (2, 32),
        (4, 32),
        (6, 32),
        (8, 32),
        (10, 32),
        (12, 32),
        (14, 32),
        (16, 32),
        (18, 32),
        (20, 32),
        (0, 32)
    ])
    def test_non_invertible_elements(self, a, m):
        is_inv, u, pos_inv, desc = mod_inverse(a, m)
        assert is_inv is False
        assert pos_inv is None
        assert "Необратимо" in desc

    def test_invalid_modulus(self):
        with pytest.raises(ValueError):
            mod_inverse(5, 0)
        with pytest.raises(ValueError):
            mod_inverse(5, -10)


class TestSolveLinearCongruence:
    """Тестирование решения сравнения ax ≡ b (mod m)."""

    def test_no_solution(self):
        # 8x ≡ 6 (mod 32): НОД(8, 32) = 8, 6 не делится на 8 -> решений нет
        st, sols, desc = solve_linear_congruence(8, 6, 32)
        assert st == 1
        assert sols == []
        assert "Решений нет" in desc

    def test_unique_solution(self):
        # 9x ≡ 19 (mod 32): НОД(9, 32) = 1 -> одно решение x = 27
        st, sols, desc = solve_linear_congruence(9, 19, 32)
        assert st == 2
        assert sols == [27]
        assert (9 * 27) % 32 == 19 % 32

    def test_multiple_solutions(self):
        # 6x ≡ 12 (mod 30): НОД(6, 30) = 6, 12 делится на 6 -> 6 решений
        st, sols, desc = solve_linear_congruence(6, 12, 30)
        assert st == 3
        assert len(sols) == 6
        for x in sols:
            assert (6 * x) % 30 == 12

    def test_invalid_modulus(self):
        with pytest.raises(ValueError):
            solve_linear_congruence(2, 3, 0)
        with pytest.raises(ValueError):
            solve_linear_congruence(2, 3, -5)


class TestSolveSystemCongruences:
    """Тестирование решения системы линейных сравнений."""

    def test_invalid_modulus(self):
        with pytest.raises(ValueError):
            solve_system_congruences(1, 2, 3, 4, 0)
        with pytest.raises(ValueError):
            solve_system_congruences(1, 2, 3, 4, -1)

    def test_manual_example_1_system_1(self, manual_examples):
        # 14a + b ≡ 8, 5a + b ≡ 19 (mod 32) -> a = 13, b = 18
        ex = manual_examples["ex1_sys1"]
        st, sols, _ = solve_system_congruences(ex["a"], ex["b"], ex["c"], ex["d"], ex["m"])
        assert st == 2
        assert sols == [ex["expected_key"]]

    def test_manual_example_1_system_2(self, manual_examples):
        # 14a + b ≡ 19, 5a + b ≡ 8 (mod 32) -> a = 19, b = 9
        ex = manual_examples["ex1_sys2"]
        st, sols, _ = solve_system_congruences(ex["a"], ex["b"], ex["c"], ex["d"], ex["m"])
        assert st == 2
        assert sols == [ex["expected_key"]]

    def test_manual_example_2_unsolvable(self, manual_examples):
        # 8a + b ≡ 9, 0a + b ≡ 15 (mod 32) -> неразрешима
        ex = manual_examples["ex2_sys1"]
        st, sols, _ = solve_system_congruences(ex["a"], ex["b"], ex["c"], ex["d"], ex["m"])
        assert st == 1
        assert sols == []

    def test_variant_16_system(self):
        # E(о)=з (14a + b ≡ 7), E(е)=ф (5a + b ≡ 20) mod 32 -> a = 27, b = 13
        st, sols, _ = solve_system_congruences(14, 7, 5, 20, 32)
        assert st == 2
        assert sols == [(27, 13)]

