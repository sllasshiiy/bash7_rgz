#!/usr/bin/env python3
"""
Тесты для модуля quadratic_solver
"""

import pytest
import math
from quadratic_solver import calculate_discriminant, solve_quadratic


class TestCalculateDiscriminant:
    """Тесты для функции calculate_discriminant"""
    
# ИЗМЕНИТЕ этот тест чтобы он падал
    def test_positive_discriminant(self):
        """Тест положительного дискриминанта - СДЕЛАЕМ ОШИБКУ"""
    # Было: assert calculate_discriminant(1, 5, 6) == 999
    # Стало (неправильное значение):
        assert calculate_discriminant(1, 5, 6) == 999  # Должно быть 1, но ставим 999
    
    def test_zero_discriminant(self):
        """Тест нулевого дискриминанта"""
        assert calculate_discriminant(1, 2, 1) == 0  # 4 - 4 = 0
    
    def test_negative_discriminant(self):
        """Тест отрицательного дискриминанта"""
        assert calculate_discriminant(2, 1, 3) == -23  # 1 - 24 = -23
    
    def test_fractional_coefficients(self):
        """Тест с дробными коэффициентами"""
        result = calculate_discriminant(0.5, 1.5, 2)
        expected = 1.5**2 - 4*0.5*2
        assert math.isclose(result, expected)
    
    # Негативные тесты
    def test_zero_a_coefficient(self):
        """Тест с нулевым коэффициентом a"""
        with pytest.raises(ValueError, match="Коэффициент a не может быть равен нулю"):
            calculate_discriminant(0, 1, 1)


class TestSolveQuadratic:
    """Тесты для функции solve_quadratic"""
    
    # Положительные тесты
    def test_two_real_roots(self):
        """Тест с двумя действительными корнями"""
        roots = solve_quadratic(1, -3, 2)  # x² - 3x + 2 = 0
        assert roots == (2.0, 1.0)
    
    def test_one_real_root(self):
        """Тест с одним действительным корнем"""
        roots = solve_quadratic(1, 2, 1)  # x² + 2x + 1 = 0
        assert roots == (-1.0, -1.0)
    
    def test_fractional_roots(self):
        """Тест с дробными корнями"""
        roots = solve_quadratic(2, -5, 2)  # 2x² - 5x + 2 = 0
        expected = (2.0, 0.5)
        assert all(math.isclose(r, e) for r, e in zip(roots, expected))
    
    # Негативные тесты
    def test_no_real_roots(self):
        """Тест без действительных корней"""
        roots = solve_quadratic(1, 0, 1)  # x² + 1 = 0
        assert roots is None
    
    def test_complex_roots_case(self):
        """Тест случая с комплексными корнями"""
        roots = solve_quadratic(1, 1, 1)  # x² + x + 1 = 0
        assert roots is None


def test_integration():
    """Интеграционный тест полного решения"""
    # Уравнение: x² - 5x + 6 = 0
    discriminant = calculate_discriminant(1, -5, 6)
    assert discriminant == 1
    
    roots = solve_quadratic(1, -5, 6)
    assert roots == (3.0, 2.0)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
