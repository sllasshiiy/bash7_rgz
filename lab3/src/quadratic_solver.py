#!/usr/bin/env python3
"""
Решатель квадратных уравнений
Скрипт для вычисления дискриминанта и корней квадратных уравнений
"""

import math


def calculate_discriminant(a: float, b: float, c: float) -> float:
    """
    Вычисляет дискриминант для квадратного уравнения: ax² + bx + c = 0
    
    Аргументы:
        a (float): Коэффициент при x²
        b (float): Коэффициент при x
        c (float): Свободный член
    
    Возвращает:
        float: Значение дискриминанта
    """
    if a == 0:
        raise ValueError("Коэффициент 'a' не может быть нулем для квадратного уравнения")
    
    # Вычисляем дискриминант по формуле: D = b² - 4ac
    discriminant = b**2 - 4*a*c
    return discriminant


def solve_quadratic(a: float, b: float, c: float) -> dict:
    """
    Решает квадратное уравнение и возвращает подробные результаты
    
    Аргументы:
        a (float): Коэффициент при x²
        b (float): Коэффициент при x
        c (float): Свободный член
    
    Возвращает:
        dict: Результаты с корнями, дискриминантом и сообщением
    """
    # Вычисляем дискриминант
    discriminant = calculate_discriminant(a, b, c)
    
    if discriminant > 0:
        # Два действительных корня
        root1 = (-b + math.sqrt(discriminant)) / (2*a)
        root2 = (-b - math.sqrt(discriminant)) / (2*a)
        message = "Два различных действительных корня"
    elif discriminant == 0:
        # Один действительный корень
        root1 = root2 = -b / (2*a)
        message = "Один действительный корень (кратный корень)"
    else:
        # Комплексные корни
        real_part = -b / (2*a)
        imaginary_part = math.sqrt(-discriminant) / (2*a)
        root1 = complex(real_part, imaginary_part)
        root2 = complex(real_part, -imaginary_part)
        message = "Два комплексных корня"
    
    return {
        'roots': (root1, root2),  # Корни уравнения
        'discriminant': discriminant,  # Значение дискриминанта
        'message': message,  # Сообщение о типе корней
        'equation': f"{a}x² + {b}x + {c} = 0"  # Строковое представление уравнения
    }


def main():
    """Основная функция с взаимодействием с пользователем"""
    print("=== Решатель квадратных уравнений ===")
    print("Форма уравнения: ax² + bx + c = 0")
    
    try:
        # Получаем коэффициенты от пользователя
        a = float(input("Введите коэффициент a: "))
        b = float(input("Введите коэффициент b: "))
        c = float(input("Введите коэффициент c: "))
        
        # Вычисляем и отображаем результаты
        result = solve_quadratic(a, b, c)
        
        print(f"\nРезультаты для уравнения: {result['equation']}")
        print(f"Дискриминант (D) = {result['discriminant']}")
        print(f"Корни: {result['message']}")
        
        root1, root2 = result['roots']
        if isinstance(root1, complex):
            # Форматируем вывод для комплексных чисел
            print(f"Корень 1 = {root1:.2f}")
            print(f"Корень 2 = {root2:.2f}")
        else:
            # Форматируем вывод для действительных чисел
            print(f"Корень 1 = {root1:.4f}")
            print(f"Корень 2 = {root2:.4f}")
    
    except ValueError as e:
        print(f"Ошибка: {e}")
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")


def test_examples():
    """Тестовая функция с примерами"""
    print("\n=== Примеры вычислений ===")
    
    # Примеры уравнений для тестирования
    examples = [
        (1, -3, 2),    # D > 0: два действительных корня
        (1, -2, 1),    # D = 0: один действительный корень  
        (1, 2, 5),     # D < 0: комплексные корни
        (2, -11, 12),  # D > 0: два действительных корня
    ]
    
    for a, b, c in examples:
        result = solve_quadratic(a, b, c)
        print(f"\nУравнение: {result['equation']}")
        print(f"Дискриминант: {result['discriminant']}")
        print(f"Результат: {result['message']}")
        print(f"Корни: {result['roots'][0]:.4f}, {result['roots'][1]:.4f}")


if __name__ == "__main__":
    # Запускаем примеры автоматически
    test_examples()