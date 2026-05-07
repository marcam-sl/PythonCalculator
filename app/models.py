from __future__ import annotations

from pydantic import BaseModel, Field


class OperationRequest(BaseModel):
    a: float = Field(..., description="First operand", examples=[10.0])
    b: float = Field(..., description="Second operand", examples=[5.0])

    model_config = {"json_schema_extra": {"examples": [{"a": 10.0, "b": 5.0}]}}


class OperationResponse(BaseModel):
    operation: str = Field(..., description="Name of the operation performed")
    a: float = Field(..., description="First operand")
    b: float = Field(..., description="Second operand")
    result: float = Field(..., description="Result of the operation")

    model_config = {
        "json_schema_extra": {
            "examples": [{"operation": "add", "a": 10.0, "b": 5.0, "result": 15.0}]
        }
    }


class ErrorResponse(BaseModel):
    error: str = Field(..., description="Error type")
    detail: str = Field(..., description="Human-readable error description")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"error": "DivisionByZero", "detail": "Division by zero is not allowed."}
            ]
        }
    }
