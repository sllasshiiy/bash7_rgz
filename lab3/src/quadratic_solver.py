def calculate_discriminant(a, b, c):
    """Calculate discriminant for quadratic equation ax^2 + bx + c = 0"""
    if a == 0:
        raise ValueError("Коэффициент 'a' не может быть нулем")
    return b**2 - 4*a*c

def solve_quadratic(a, b, c):
    """Solve quadratic equation ax^2 + bx + c = 0
    Returns: dict with keys 'discriminant', 'roots', and 'message'
    """
    if a == 0:
        raise ValueError("Коэффициент 'a' не может быть нулем")
    
    D = calculate_discriminant(a, b, c)
    
    if D > 0:
        x1 = (-b + D**0.5) / (2*a)
        x2 = (-b - D**0.5) / (2*a)
        roots = (x1, x2)  # Возвращаем кортеж как в тесте
        message = "Два различных действительных корня"
    elif D == 0:
        x = -b / (2*a)
        roots = (x, x)  # Возвращаем кортеж из двух одинаковых значений
        message = "Один действительный корень (кратный корень)"
    else:
        # Комплексные корни
        real_part = -b / (2*a)
        imag_part = (-D)**0.5 / (2*a)
        roots = (complex(real_part, imag_part), complex(real_part, -imag_part))
        message = "Два комплексных корня"
    
    return {
        'discriminant': D,
        'roots': roots,
        'message': message
    }
