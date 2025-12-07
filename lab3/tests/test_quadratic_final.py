import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.quadratic_solver import calculate_discriminant, solve_quadratic

def test_basic():
    """Basic tests"""
    # Test discriminant
    assert calculate_discriminant(1, 0, -1) == 4
    assert calculate_discriminant(1, 2, 1) == 0
    assert calculate_discriminant(1, 1, 1) == -3
    
    # Test solve_quadratic returns dict with required keys
    result = solve_quadratic(1, 0, -1)
    assert isinstance(result, dict)
    assert 'discriminant' in result
    assert 'roots' in result
    assert 'message' in result
    
    # Test values
    assert result['discriminant'] == 4
    assert result['message'] == "Два различных действительных корня"
    assert len(result['roots']) == 2

def test_edge_cases():
    """Test edge cases"""
    # a = 0 should raise error
    import pytest
    with pytest.raises(ValueError):
        solve_quadratic(0, 1, 1)
    
    # Single root case
    result = solve_quadratic(1, 2, 1)
    assert result['discriminant'] == 0
    assert result['message'] == "Один действительный корень (кратный корень)"
    assert result['roots'][0] == result['roots'][1] == -1.0

def test_complex():
    """Test complex roots"""
    result = solve_quadratic(1, 1, 1)
    assert result['discriminant'] == -3
    assert result['message'] == "Два комплексных корня"
    assert all(isinstance(r, complex) for r in result['roots'])
