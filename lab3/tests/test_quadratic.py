#!/usr/bin/env python3
"""
Тесты для решателя квадратных уравнений
"""

import pytest
import math
from src.quadratic_solver import calculate_discriminant, solve_quadratic


class TestCalculateDiscriminant:
    """Тесты для функции calculate_discriminant"""
    
    def test_positive_discriminant(self):
        """Тест положительного дискриминанта: D > 0"""
        #x² - 3x + 2 = 0
        result = calculate_discriminant(1, -3, 2)
        assert result == 1  # D = (-3)² - 4*1*2 = 9 - 8 = 1
    
    def test_zero_discriminant(self):
        """Тест нулевого дискриминанта: D = 0"""
        # x² - 2x + 1 = 0
        result = calculate_discriminant(1, -2, 1)
        assert result == 0  # D = (-2)² - 4*1*1 = 4 - 4 = 0
    
    def test_negative_discriminant(self):
        """Тест отрицательного дискриминанта: D < 0"""
        #x² + 2x + 5 = 0
        result = calculate_discriminant(1, 2, 5)
        assert result == -16  # D = 2² - 4*1*5 = 4 - 20 = -16
    
    def test_fractional_coefficients(self):
        """Тест с дробными коэффициентами"""
        # 2x² - 5x + 2 = 0
        result = calculate_discriminant(2, -5, 2)
        assert result == 9  # D = (-5)² - 4*2*2 = 25 - 16 = 9
    
    def test_zero_coefficient_a_error(self):
        """Тест ошибки при a = 0"""
        with pytest.raises(ValueError, match="Коэффициент 'a' не может быть нулем"):
            calculate_discriminant(0, 2, 3)


class TestSolveQuadraticPositive:
    """ПОЛОЖИТЕЛЬНЫЕ ТЕСТЫ: дискриминант >= 0"""
    
    def test_two_real_roots_positive_discriminant(self):
        """Тест двух действительных корней (D > 0)"""
        # x² - 3x + 2 = 0 → корни: 2 и 1
        result = solve_quadratic(1, -3, 2)
        
        assert result['discriminant'] == 1
        assert result['message'] == "Два различных действительных корня"
        assert result['roots'] == (2.0, 1.0)
        assert result['equation'] == "1x² + -3x + 2 = 0"
    
    def test_one_real_root_zero_discriminant(self):
        """Тест одного действительного корня (D = 0)"""
        #x² - 2x + 1 = 0 → корень: 1
        result = solve_quadratic(1, -2, 1)
        
        assert result['discriminant'] == 0
        assert result['message'] == "Один действительный корень (кратный корень)"
        assert result['roots'] == (1.0, 1.0)
        assert result['equation'] == "1x² + -2x + 1 = 0"
    
    def test_fractional_roots(self):
        """Тест дробных корней"""
        #2x² - 11x + 12 = 0 → корни: 4 и 1.5
        result = solve_quadratic(2, -11, 12)
        
        assert result['discriminant'] == 25
        assert result['message'] == "Два различных действительных корня"
        assert result['roots'] == (4.0, 1.5)
    
    def test_negative_roots(self):
        """Тест отрицательных корней"""
        #x² + 5x + 6 = 0 → корни: -2 и -3
        result = solve_quadratic(1, 5, 6)
        
        assert result['discriminant'] == 1
        assert result['roots'] == (-2.0, -3.0)


class TestSolveQuadraticNegative:
    """НЕГАТИВНЫЕ ТЕСТЫ: дискриминант < 0 (комплексные корни)"""
    
    def test_complex_roots_negative_discriminant(self):
        """Тест комплексных корней (D < 0)"""
        # x² + 2x + 5 = 0 → корни: -1 ± 2i
        result = solve_quadratic(1, 2, 5)
        
        assert result['discriminant'] == -16
        assert result['message'] == "Два комплексных корня"
        
        root1, root2 = result['roots']
        
        # Проверяем что корни комплексные
        assert isinstance(root1, complex)
        assert isinstance(root2, complex)
        
        # Проверяем действительные части
        assert abs(root1.real - (-1.0)) < 0.0001
        assert abs(root2.real - (-1.0)) < 0.0001
        
        # Проверяем мнимые части
        assert abs(root1.imag - 2.0) < 0.0001
        assert abs(root2.imag - (-2.0)) < 0.0001
    
    def test_another_complex_case(self):
        """Другой тест с комплексными корнями"""
        # x² + 4x + 13 = 0 → корни: -2 ± 3i
        result = solve_quadratic(1, 4, 13)
        
        assert result['discriminant'] == -36
        assert result['message'] == "Два комплексных корня"
        
        root1, root2 = result['roots']
        assert isinstance(root1, complex)
        assert isinstance(root2, complex)
        
        # Проверяем что корни комплексно-сопряженные
        assert abs(root1.real - root2.real) < 0.0001
        assert abs(root1.imag + root2.imag) < 0.0001
    
    def test_purely_imaginary_roots(self):
        """Тест с чисто мнимыми корнями"""
        # x² + 9 = 0 → корни: ±3i
        result = solve_quadratic(1, 0, 9)
        
        assert result['discriminant'] == -36
        assert result['message'] == "Два комплексных корня"
        
        root1, root2 = result['roots']
        assert root1 == complex(0, 3)
        assert root2 == complex(0, -3)


class TestEdgeCases:
    """Тесты граничных случаев"""
    
    def test_large_coefficients(self):
        """Тест с большими коэффициентами"""
        result = solve_quadratic(1e6, 2e6, 1e6)
        assert result['discriminant'] == 0
        assert result['roots'] == (-1.0, -1.0)
    
    def test_small_coefficients(self):
        """Тест с маленькими коэффициентами"""
        result = solve_quadratic(0.001, 0.002, 0.001)
        assert abs(result['discriminant']) < 0.0000001  # Почти 0
        assert abs(result['roots'][0] - (-1.0)) < 0.0001


def test_multiple_equations():
    """Тест нескольких уравнений подряд"""
    test_cases = [
        (1, 0, -4, 16, (2.0, -2.0)),     # x² - 4 = 0
        (1, 4, 4, 0, (-2.0, -2.0)),      # x² + 4x + 4 = 0
        (1, 1, 1, -3, None),             # x² + x + 1 = 0 (комплексные)
    ]
    
    for a, b, c, exp_d, exp_roots in test_cases:
        result = solve_quadratic(a, b, c)
        assert result['discriminant'] == exp_d
        
        if exp_roots is not None:
            root1, root2 = result['roots']
            exp1, exp2 = exp_roots
            assert abs(root1 - exp1) < 0.0001
            assert abs(root2 - exp2) < 0.0001
if __name__ == "__main__":
    pytest.main([__file__, "-v"])