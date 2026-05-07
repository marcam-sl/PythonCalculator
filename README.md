# Python Calculator API

A production-structured REST calculator service built with **FastAPI**.  
Exposes four arithmetic operations (add, subtract, multiply, divide) as JSON endpoints with full OpenAPI documentation, pytest test suite, Docker support, and GitHub Actions CI.

---

## Architecture

```
PythonCalculator/
├── app/
│   ├── calculator.py       # Pure Calculator class — no HTTP dependency
│   ├── models.py           # Pydantic request / response schemas
│   ├── main.py             # FastAPI application factory + health endpoint
│   └── routers/
│       └── calculator.py   # /api/v1/calculator/* route handlers
├── tests/
│   ├── test_calculator.py  # 40 unit tests (logic only)
│   └── test_api.py         # Component / integration tests (HTTP layer)
├── .github/workflows/
│   └── ci.yml              # GitHub Actions CI pipeline
├── Dockerfile
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

**Design principles**

| Layer | Responsibility |
|---|---|
| `Calculator` | Pure arithmetic — raises `DivisionByZeroError` on `/0` |
| `models.py` | Pydantic v2 models — input validation, serialisation |
| `routers/calculator.py` | Maps HTTP ↔ Calculator; translates domain errors to HTTP 400 |
| `main.py` | Wires router into FastAPI; serves health + OpenAPI docs |

---

## API Endpoints

All calculator routes accept and return `application/json`.

### `GET /health`

```json
{"status": "ok"}
```

### `POST /api/v1/calculator/add`

**Request**
```json
{"a": 10, "b": 5}
```
**Response 200**
```json
{"operation": "add", "a": 10.0, "b": 5.0, "result": 15.0}
```

### `POST /api/v1/calculator/subtract`

**Request**
```json
{"a": 10, "b": 4}
```
**Response 200**
```json
{"operation": "subtract", "a": 10.0, "b": 4.0, "result": 6.0}
```

### `POST /api/v1/calculator/multiply`

**Request**
```json
{"a": 6, "b": 7}
```
**Response 200**
```json
{"operation": "multiply", "a": 6.0, "b": 7.0, "result": 42.0}
```

### `POST /api/v1/calculator/divide`

**Request**
```json
{"a": 10, "b": 2}
```
**Response 200**
```json
{"operation": "divide", "a": 10.0, "b": 2.0, "result": 5.0}
```

**Response 400 — Division by zero**
```json
{"error": "DivisionByZero", "detail": "Division by zero is not allowed."}
```

**Response 422 — Invalid / missing fields**
```json
{
  "detail": [
    {"loc": ["body", "b"], "msg": "Field required", "type": "missing"}
  ]
}
```

---

## Local Run (without Docker)

```bash
# 1. Clone
git clone https://github.com/marcam-sl/PythonCalculator.git
cd PythonCalculator

# 2. Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Install runtime dependencies
pip install -r requirements.txt

# 4. Start the server
uvicorn app.main:app --reload --port 8000
```

The API is now available at `http://localhost:8000`.  
Interactive docs: `http://localhost:8000/docs`  
ReDoc: `http://localhost:8000/redoc`

---

## Local Run (with Docker)

### Build

```bash
docker build -t python-calculator .
```

### Run

```bash
docker run --rm -p 8000:8000 python-calculator
```

### Build and run in one step

```bash
docker build -t python-calculator . && docker run --rm -p 8000:8000 python-calculator
```

---

## Example curl Commands

```bash
# Health check
curl http://localhost:8000/health

# Add
curl -s -X POST http://localhost:8000/api/v1/calculator/add \
  -H "Content-Type: application/json" \
  -d '{"a": 10, "b": 5}'

# Subtract
curl -s -X POST http://localhost:8000/api/v1/calculator/subtract \
  -H "Content-Type: application/json" \
  -d '{"a": 10, "b": 4}'

# Multiply
curl -s -X POST http://localhost:8000/api/v1/calculator/multiply \
  -H "Content-Type: application/json" \
  -d '{"a": 6, "b": 7}'

# Divide
curl -s -X POST http://localhost:8000/api/v1/calculator/divide \
  -H "Content-Type: application/json" \
  -d '{"a": 10, "b": 2}'

# Divide by zero (returns HTTP 400)
curl -s -X POST http://localhost:8000/api/v1/calculator/divide \
  -H "Content-Type: application/json" \
  -d '{"a": 10, "b": 0}'
```

---

## Running Tests

```bash
# Install dev dependencies (includes pytest + httpx)
pip install -r requirements-dev.txt

# Run all tests
pytest

# Run only unit tests (no HTTP)
pytest tests/test_calculator.py -v

# Run only integration tests (HTTP layer)
pytest tests/test_api.py -v

# Run with short traceback summary
pytest --tb=short -q
```

Expected output (all 65 tests passing):

```
tests/test_calculator.py  ......................  40 passed
tests/test_api.py         ........................  24 passed
```

---

## CI Overview

The GitHub Actions workflow (`.github/workflows/ci.yml`) runs on every **push** and **pull request** across all branches.

| Step | What it does |
|---|---|
| `actions/checkout@v4` | Checks out the repository |
| `actions/setup-python@v5` | Installs Python (matrix: 3.11, 3.12) with pip cache |
| Install dependencies | `pip install -r requirements-dev.txt` |
| Unit tests | `pytest tests/test_calculator.py` |
| Integration tests | `pytest tests/test_api.py` |
| Full suite | `pytest` — fails the job on any error |

The matrix runs against Python **3.11** and **3.12** in parallel, so a regression in either version is caught immediately.

---

## License

MIT
