from __future__ import annotations


class DivisionByZeroError(ValueError):
    """Raised when the divisor is zero."""


class Calculator:
    """Stateless arithmetic calculator supporting the four basic operations."""

    def add(self, a: float, b: float) -> float:
        return a + b

    def subtract(self, a: float, b: float) -> float:
        return a - b

    def multiply(self, a: float, b: float) -> float:
        return a * b

    def divide(self, a: float, b: float) -> float:
        if b == 0:
            raise DivisionByZeroError("Division by zero is not allowed.")
        return a / b
