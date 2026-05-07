"""
40 unit tests for Calculator — pure logic, no HTTP.

Coverage breakdown:
  add       — 10 tests
  subtract  — 10 tests
  multiply  — 10 tests
  divide    — 10 tests (including divide-by-zero variants)
"""
from __future__ import annotations

import math

import pytest

from app.calculator import Calculator, DivisionByZeroError

# ---------------------------------------------------------------------------
# Fixture
# ---------------------------------------------------------------------------


@pytest.fixture
def calc() -> Calculator:
    return Calculator()


# ---------------------------------------------------------------------------
# add — 10 tests
# ---------------------------------------------------------------------------


def test_add_two_positive_integers(calc: Calculator) -> None:
    assert calc.add(3, 5) == 8


def test_add_two_negative_integers(calc: Calculator) -> None:
    assert calc.add(-4, -6) == -10


def test_add_positive_and_negative(calc: Calculator) -> None:
    assert calc.add(10, -3) == 7


def test_add_negative_and_positive(calc: Calculator) -> None:
    assert calc.add(-7, 12) == 5


def test_add_zero_and_positive(calc: Calculator) -> None:
    assert calc.add(0, 99) == 99


def test_add_positive_and_zero(calc: Calculator) -> None:
    assert calc.add(42, 0) == 42


def test_add_zero_and_zero(calc: Calculator) -> None:
    assert calc.add(0, 0) == 0


def test_add_two_floats(calc: Calculator) -> None:
    assert calc.add(1.1, 2.2) == pytest.approx(3.3)


def test_add_float_and_integer(calc: Calculator) -> None:
    assert calc.add(2.5, 3) == pytest.approx(5.5)


def test_add_large_numbers(calc: Calculator) -> None:
    assert calc.add(1_000_000, 2_000_000) == 3_000_000


# ---------------------------------------------------------------------------
# subtract — 10 tests
# ---------------------------------------------------------------------------


def test_subtract_larger_minus_smaller(calc: Calculator) -> None:
    assert calc.subtract(10, 4) == 6


def test_subtract_smaller_minus_larger(calc: Calculator) -> None:
    assert calc.subtract(3, 9) == -6


def test_subtract_two_negative_integers(calc: Calculator) -> None:
    assert calc.subtract(-5, -3) == -2


def test_subtract_zero_from_positive(calc: Calculator) -> None:
    assert calc.subtract(7, 0) == 7


def test_subtract_positive_from_zero(calc: Calculator) -> None:
    assert calc.subtract(0, 5) == -5


def test_subtract_zero_from_zero(calc: Calculator) -> None:
    assert calc.subtract(0, 0) == 0


def test_subtract_two_floats(calc: Calculator) -> None:
    assert calc.subtract(5.5, 2.2) == pytest.approx(3.3)


def test_subtract_float_from_integer(calc: Calculator) -> None:
    assert calc.subtract(10, 3.5) == pytest.approx(6.5)


def test_subtract_large_numbers(calc: Calculator) -> None:
    assert calc.subtract(5_000_000, 3_000_000) == 2_000_000


def test_subtract_negative_produces_addition(calc: Calculator) -> None:
    # a - (-b) == a + b
    assert calc.subtract(8, -2) == 10


# ---------------------------------------------------------------------------
# multiply — 10 tests
# ---------------------------------------------------------------------------


def test_multiply_two_positive_integers(calc: Calculator) -> None:
    assert calc.multiply(3, 4) == 12


def test_multiply_two_negative_integers(calc: Calculator) -> None:
    assert calc.multiply(-3, -4) == 12


def test_multiply_positive_and_negative(calc: Calculator) -> None:
    assert calc.multiply(6, -3) == -18


def test_multiply_by_zero(calc: Calculator) -> None:
    assert calc.multiply(999, 0) == 0


def test_multiply_zero_by_zero(calc: Calculator) -> None:
    assert calc.multiply(0, 0) == 0


def test_multiply_by_one(calc: Calculator) -> None:
    assert calc.multiply(55, 1) == 55


def test_multiply_by_negative_one(calc: Calculator) -> None:
    assert calc.multiply(13, -1) == -13


def test_multiply_two_floats(calc: Calculator) -> None:
    assert calc.multiply(2.5, 4.0) == pytest.approx(10.0)


def test_multiply_float_and_integer(calc: Calculator) -> None:
    assert calc.multiply(1.5, 6) == pytest.approx(9.0)


def test_multiply_large_numbers(calc: Calculator) -> None:
    assert calc.multiply(10_000, 10_000) == 100_000_000


# ---------------------------------------------------------------------------
# divide — 10 tests
# ---------------------------------------------------------------------------


def test_divide_exact_integer_result(calc: Calculator) -> None:
    assert calc.divide(10, 2) == 5.0


def test_divide_float_result(calc: Calculator) -> None:
    assert calc.divide(7, 2) == pytest.approx(3.5)


def test_divide_negative_by_positive(calc: Calculator) -> None:
    assert calc.divide(-9, 3) == pytest.approx(-3.0)


def test_divide_positive_by_negative(calc: Calculator) -> None:
    assert calc.divide(9, -3) == pytest.approx(-3.0)


def test_divide_two_negatives(calc: Calculator) -> None:
    assert calc.divide(-8, -4) == pytest.approx(2.0)


def test_divide_by_one(calc: Calculator) -> None:
    assert calc.divide(42, 1) == pytest.approx(42.0)


def test_divide_zero_by_nonzero(calc: Calculator) -> None:
    assert calc.divide(0, 7) == pytest.approx(0.0)


def test_divide_two_floats(calc: Calculator) -> None:
    assert calc.divide(5.5, 2.2) == pytest.approx(2.5)


def test_divide_by_zero_raises(calc: Calculator) -> None:
    with pytest.raises(DivisionByZeroError, match="Division by zero"):
        calc.divide(10, 0)


def test_divide_negative_by_zero_raises(calc: Calculator) -> None:
    with pytest.raises(DivisionByZeroError):
        calc.divide(-5, 0)
