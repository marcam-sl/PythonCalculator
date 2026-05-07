from __future__ import annotations

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.routers.calculator import router as calculator_router

app = FastAPI(
    title="Python Calculator API",
    description=(
        "A production-structured REST calculator service exposing add, subtract, "
        "multiply, and divide operations via JSON endpoints."
    ),
    version="1.0.0",
    contact={"name": "DAP Team"},
    license_info={"name": "MIT"},
)

app.include_router(calculator_router, prefix="/api/v1")


@app.get("/health", tags=["health"], summary="Health check")
def health() -> JSONResponse:
    return JSONResponse(content={"status": "ok"})
