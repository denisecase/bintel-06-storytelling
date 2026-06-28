r"""serve_case.py - example.

A FastAPI service that loads
a trained penguin species classifier
and exposes a /predict endpoint.

Author: Denise Case
Date: 2026-06

Process:
    - Load a saved model from artifacts/.
    - Accept a POST request with penguin measurements.
    - Return the predicted species.

Data Source:
    - artifacts/model.joblib (trained in the notebook or app_case.py)

Terminal commands to run this service from the root project folder:

uv run fastapi dev src/bizintel/serve_case.py      # development (auto-reload)
uv run fastapi run src/bizintel/serve_case.py      # production

- OR -

uv run uvicorn bizintel.serve_case:app --reload    # development (auto-reload)
uv run uvicorn bizintel.serve_case:app             # production

Then send a request - open a new terminal and run

If macOS or Linux, use \ line continuation characters:

    curl -X POST http://127.0.0.1:8000/predict \
         -H "Content-Type: application/json" \
         -d '{"bill_length_mm": 39.1, "bill_depth_mm": 18.7, "flipper_length_mm": 181, "body_mass_g": 3750}'

If Windows (PowerShell), use ` instead of \ for line continuation:

    curl -X POST http://127.0.0.1:8000/predict `
         -H "Content-Type: application/json" `
         -d '{"bill_length_mm": 39.1, "bill_depth_mm": 18.7, "flipper_length_mm": 181, "body_mass_g": 3750}'
OBS:
  Don't edit this file - it should remain a working example.
  Copy it, rename it, and modify your copy if you want to experiment.
  Include your command to run it in the docstring and in README.md.
"""

# === Section 1. IMPORTS ===

import logging
from pathlib import Path
from typing import Any, Final

from datafun_toolkit.logger import get_logger, log_header
from fastapi import FastAPI, HTTPException
import joblib  # for serializing and deserializing the model
from sklearn.ensemble import RandomForestClassifier

__all__ = ["app", "predict_from_features", "predict"]

# === Section 2. CONFIGURE LOGGER ===

LOG: logging.Logger = get_logger("M06", level="DEBUG")
log_header(LOG, "M06")

# === Section 3. CONSTANTS AND CONFIGURATION ===

# The path to the saved model artifact.
MODEL_PATH: Final[Path] = Path("artifacts") / "model.joblib"

# The feature columns the model was trained on.
# These must match exactly what was used during training.
FEATURE_COLS: Final[list[str]] = [
    "bill_length_mm",
    "bill_depth_mm",
    "flipper_length_mm",
    "body_mass_g",
]

# === Section 4. LOAD THE MODEL ===

LOG.info(f"Loading model from: {MODEL_PATH}")

if not MODEL_PATH.exists():
    LOG.error(f"Model file not found: {MODEL_PATH}")
    raise FileNotFoundError(
        f"Model not found at {MODEL_PATH}. "
        "Run the training notebook or app_case.py first."
    )

MODEL = joblib.load(MODEL_PATH)
LOG.info("Model loaded successfully")

# === Section 5. CREATE THE APP ===

app = FastAPI(title="Penguin species classifier")

# === Section 6. DEFINE THE PREDICT ENDPOINT ===


def predict_from_features(
    model: RandomForestClassifier, payload: dict[str, Any]
) -> dict[str, Any]:
    """Pure prediction function - testable outside the web framework."""
    try:
        features = [float(payload[c]) for c in FEATURE_COLS]
    except KeyError as exc:
        raise ValueError(f"Missing required feature: {exc}") from exc
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Invalid feature value: {exc}") from exc

    label: str = str(model.predict([features])[0])
    return {"prediction": label}


@app.post("/predict")
def predict(payload: dict[str, Any]) -> dict[str, Any]:
    try:
        return predict_from_features(MODEL, payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
