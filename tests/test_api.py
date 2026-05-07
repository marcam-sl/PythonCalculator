"""Component / integration tests — exercises the HTTP layer end-to-end."""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------


def test_health() -> None:
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


# ---------------------------------------------------------------------------
# OpenAPI docs are served
# ---------------------------------------------------------------------------


def test_openapi_schema_available() -> None:
    r = client.get("/openapi.json")
    assert r.status_code == 200
    assert "Python Calculator API" in r.json()["info"]["title"]


# ---------------------------------------------------------------------------
# /add
# ---------------------------------------------------------------------------


def test_add_happy_path() -> None:
    r = client.post("/api/v1/calculator/add", json={"a": 3, "b": 4})
    assert r.status_code == 200
    body = r.json()
    assert body["result"] == 7
    assert body["operation"] == "add"


def test_add_floats() -> None:
    r = client.post("/api/v1/calculator/add", json={"a": 1.1, "b": 2.2})
    assert r.status_code == 200
    assert r.json()["result"] == pytest.approx(3.3)


def test_add_negative_numbers() -> None:
    r = client.post("/api/v1/calculator/add", json={"a": -10, "b": -5})
    assert r.status_code == 200
    assert r.json()["result"] == -15


def test_add_missing_field_returns_422() -> None:
    r = client.post("/api/v1/calculator/add", json={"a": 5})
    assert r.status_code == 422


def test_add_non_numeric_returns_422() -> None:
    r = client.post("/api/v1/calculator/add", json={"a": "foo", "b": 2})
    assert r.status_code == 422


# ---------------------------------------------------------------------------
# /subtract
# ---------------------------------------------------------------------------


def test_subtract_happy_path() -> None:
    r = client.post("/api/v1/calculator/subtract", json={"a": 10, "b": 4})
    assert r.status_code == 200
    body = r.json()
    assert body["result"] == 6
    assert body["operation"] == "subtract"


def test_subtract_negative_result() -> None:
    r = client.post("/api/v1/calculator/subtract", json={"a": 3, "b": 9})
    assert r.status_code == 200
    assert r.json()["result"] == -6


def test_subtract_floats() -> None:
    r = client.post("/api/v1/calculator/subtract", json={"a": 5.5, "b": 2.2})
    assert r.status_code == 200
    assert r.json()["result"] == pytest.approx(3.3)


def test_subtract_missing_field_returns_422() -> None:
    r = client.post("/api/v1/calculator/subtract", json={"b": 3})
    assert r.status_code == 422


# ---------------------------------------------------------------------------
# /multiply
# ---------------------------------------------------------------------------


def test_multiply_happy_path() -> None:
    r = client.post("/api/v1/calculator/multiply", json={"a": 6, "b": 7})
    assert r.status_code == 200
    body = r.json()
    assert body["result"] == 42
    assert body["operation"] == "multiply"


def test_multiply_by_zero() -> None:
    r = client.post("/api/v1/calculator/multiply", json={"a": 999, "b": 0})
    assert r.status_code == 200
    assert r.json()["result"] == 0


def test_multiply_negative_numbers() -> None:
    r = client.post("/api/v1/calculator/multiply", json={"a": -3, "b": -4})
    assert r.status_code == 200
    assert r.json()["result"] == 12


def test_multiply_floats() -> None:
    r = client.post("/api/v1/calculator/multiply", json={"a": 2.5, "b": 4.0})
    assert r.status_code == 200
    assert r.json()["result"] == pytest.approx(10.0)


def test_multiply_missing_field_returns_422() -> None:
    r = client.post("/api/v1/calculator/multiply", json={"a": 5})
    assert r.status_code == 422


# ---------------------------------------------------------------------------
# /divide
# ---------------------------------------------------------------------------


def test_divide_happy_path() -> None:
    r = client.post("/api/v1/calculator/divide", json={"a": 10, "b": 2})
    assert r.status_code == 200
    body = r.json()
    assert body["result"] == 5.0
    assert body["operation"] == "divide"


def test_divide_float_result() -> None:
    r = client.post("/api/v1/calculator/divide", json={"a": 7, "b": 2})
    assert r.status_code == 200
    assert r.json()["result"] == pytest.approx(3.5)


def test_divide_negative_numbers() -> None:
    r = client.post("/api/v1/calculator/divide", json={"a": -9, "b": 3})
    assert r.status_code == 200
    assert r.json()["result"] == pytest.approx(-3.0)


def test_divide_by_zero_returns_400() -> None:
    r = client.post("/api/v1/calculator/divide", json={"a": 10, "b": 0})
    assert r.status_code == 400
    body = r.json()
    assert body["error"] == "DivisionByZero"
    assert "zero" in body["detail"].lower()


def test_divide_by_zero_negative_numerator_returns_400() -> None:
    r = client.post("/api/v1/calculator/divide", json={"a": -5, "b": 0})
    assert r.status_code == 400
    assert r.json()["error"] == "DivisionByZero"


def test_divide_zero_by_nonzero() -> None:
    r = client.post("/api/v1/calculator/divide", json={"a": 0, "b": 5})
    assert r.status_code == 200
    assert r.json()["result"] == 0.0


def test_divide_missing_field_returns_422() -> None:
    r = client.post("/api/v1/calculator/divide", json={"a": 10})
    assert r.status_code == 422


# ---------------------------------------------------------------------------
# Response schema — operands echo back correctly
# ---------------------------------------------------------------------------


def test_response_echoes_operands() -> None:
    r = client.post("/api/v1/calculator/add", json={"a": 11.0, "b": 22.0})
    body = r.json()
    assert body["a"] == 11.0
    assert body["b"] == 22.0
