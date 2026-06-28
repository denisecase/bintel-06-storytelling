"""model_builder_case.py - example.

Trains and saves a penguin species classifier.

Author: Denise Case
Date: 2026-06

Process:
    - Load the penguins dataset.
    - Split into train and test sets.
    - Train a RandomForestClassifier.
    - Evaluate on held-out test data.
    - Save the trained model to artifacts/model.joblib.

Terminal command to run this file from the root project folder:

    uv run python -m bizintel.model_builder_case

OBS:
  Don't edit this file - it should remain a working example.
  Copy it, rename it, and modify your copy.
  Include your command to run it in the docstring and in README.md.
"""

# === Section 1a. DECLARE IMPORTS ===

import logging
from pathlib import Path
from typing import Final

from datafun_toolkit.logger import get_logger, log_header
import joblib
import pandas as pd
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

# === Section 1b. CONFIGURE LOGGER ONCE PER MODULE ===

LOG: logging.Logger = get_logger("M06", level="DEBUG")
log_header(LOG, "M06")

# === Section 1c. GLOBAL CONSTANTS AND CONFIGURATION ===

DATASET_NAME: Final[str] = "penguins"

# STEP 1. Pick the target variable we want to predict.
TARGET_COL: Final[str] = "species"

# STEP 2. Define the feature columns used to predict the target.
FEATURE_COLS: Final[list[str]] = [
    "bill_length_mm",
    "bill_depth_mm",
    "flipper_length_mm",
    "body_mass_g",
]

# STEP 3. Define the test size and random state for reproducibility.
TEST_SIZE: Final[float] = 0.20
RANDOM_STATE: Final[int] = 42

# STEP 4. Define where the trained model artifact will be saved.
MODEL_PATH: Final[Path] = Path("artifacts") / "model.joblib"

# === Section 1d. PANDAS DISPLAY CONFIGURATION ===

pd.set_option("display.max_columns", 50)
pd.set_option("display.width", 120)


# === Section 2. Load the Data ===


def load_data() -> pd.DataFrame:
    """Load the penguins dataset and drop rows with missing required values."""
    LOG.info(f"Loading dataset: {DATASET_NAME}")

    df: pd.DataFrame = sns.load_dataset(DATASET_NAME)
    LOG.info(f"Loaded: {df.shape[0]} rows, {df.shape[1]} columns")

    required: list[str] = [TARGET_COL, *FEATURE_COLS]
    df_model: pd.DataFrame = df.dropna(subset=required).copy()
    LOG.info(f"Model rows (after dropping missing): {df_model.shape[0]}")

    return df_model


# === Section 3. Split into Train and Test ===


def split_data(
    df_model: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """Split into stratified train and test sets.

    WHY: Scoring on held-out data is the only honest estimate
    of performance on new data.
    Stratifying preserves the class balance in both splits.
    """
    X: pd.DataFrame = df_model[FEATURE_COLS]
    y: pd.Series = df_model[TARGET_COL]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
    )

    LOG.info(f"Train instances: {len(X_train)}")
    LOG.info(f"Test instances:  {len(X_test)}")

    return X_train, X_test, y_train, y_test


# === Section 4. Train the Model ===


def train_model(X_train: pd.DataFrame, y_train: pd.Series) -> RandomForestClassifier:
    """Train a RandomForestClassifier on the training data."""
    LOG.info(f"Training RandomForestClassifier on {len(X_train)} instances")

    model = RandomForestClassifier(n_estimators=200, random_state=RANDOM_STATE)
    model.fit(X_train, y_train)

    LOG.info("Training complete")
    return model


# === Section 5. Evaluate the Model ===


def evaluate_model(
    model: RandomForestClassifier,
    X_test: pd.DataFrame,
    y_test: pd.Series,
) -> None:
    """Score the model on held-out test data and log the result."""
    test_acc: float = float(accuracy_score(y_test, model.predict(X_test)))
    LOG.info(f"Test accuracy: {test_acc:.3f}")


# === Section 6. Save the Model ===


def save_model(model: RandomForestClassifier) -> None:
    """Persist the trained model to disk with joblib.

    WHY: A server loads the saved artifact once at startup
    rather than retraining on every request.
    """
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    LOG.info(f"Saved model to: {MODEL_PATH}")


# === Section 7. Summary ===


def summarize() -> None:
    """Log a brief summary."""
    LOG.info("========================")
    LOG.info("SUMMARY")
    LOG.info("========================")
    LOG.info(f"Dataset:  {DATASET_NAME}")
    LOG.info(f"Target:   {TARGET_COL}")
    LOG.info(f"Features: {FEATURE_COLS}")
    LOG.info(f"Artifact: {MODEL_PATH}")
    LOG.info("========================")


# === MAIN ===


def main() -> None:
    """Run the model builder workflow."""

    LOG.info("Load data.................")
    df_model = load_data()

    LOG.info("Split data................")
    X_train, X_test, y_train, y_test = split_data(df_model)

    LOG.info("Train model...............")
    model = train_model(X_train, y_train)

    LOG.info("Evaluate model............")
    evaluate_model(model, X_test, y_test)

    LOG.info("Save model................")
    save_model(model)

    LOG.info("Summarize.................")
    summarize()

    LOG.info("========================")
    LOG.info("Executed successfully!")
    LOG.info("========================")


if __name__ == "__main__":
    main()
