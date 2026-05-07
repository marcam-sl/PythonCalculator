from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.calculator import Calculator, DivisionByZeroError
from app.models import ErrorResponse, OperationRequest, OperationResponse

router = APIRouter(prefix="/calculator", tags=["calculator"])
_calc = Calculator()


def _ok(operation: str, req: OperationRequest, result: float) -> OperationResponse:
    return OperationResponse(operation=operation, a=req.a, b=req.b, result=result)


@router.post(
    "/add",
    response_model=OperationResponse,
    summary="Add two numbers",
)
def add(req: OperationRequest) -> OperationResponse:
    return _ok("add", req, _calc.add(req.a, req.b))


@router.post(
    "/subtract",
    response_model=OperationResponse,
    summary="Subtract b from a",
)
def subtract(req: OperationRequest) -> OperationResponse:
    return _ok("subtract", req, _calc.subtract(req.a, req.b))


@router.post(
    "/multiply",
    response_model=OperationResponse,
    summary="Multiply two numbers",
)
def multiply(req: OperationRequest) -> OperationResponse:
    return _ok("multiply", req, _calc.multiply(req.a, req.b))


@router.post(
    "/divide",
    response_model=OperationResponse,
    responses={400: {"model": ErrorResponse, "description": "Division by zero"}},
    summary="Divide a by b",
)
def divide(req: OperationRequest) -> OperationResponse | JSONResponse:
    try:
        result = _calc.divide(req.a, req.b)
    except DivisionByZeroError as exc:
        return JSONResponse(
            status_code=400,
            content=ErrorResponse(
                error="DivisionByZero", detail=str(exc)
            ).model_dump(),
        )
    return _ok("divide", req, result)
