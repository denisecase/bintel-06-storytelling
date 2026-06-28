"""test_model_builder_case.py - example.

Tests for model_builder_case.py.

Author: Denise Case
Date: 2026-06

Terminal command to run tests from the root project folder:

    uv run pytest tests/test_model_builder_case.py -v

OBS:
  Don't edit this file - it should remain a working example.
  Copy it, rename it, and modify your copy.
"""

# === IMPORTS ===

from pathlib import Path

import joblib
import pandas as pd
import pytest
from pytest import MonkeyPatch
from sklearn.ensemble import RandomForestClassifier

import bizintel.model_builder_case as mb
from bizintel.model_builder_case import (
    FEATURE_COLS,
    TARGET_COL,
    TEST_SIZE,
    evaluate_model,
    load_data,
    split_data,
    train_model,
)

# === TYPE ALIAS ===

SplitResult = tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]

# === FIXTURES ===


@pytest.fixture
def df_model() -> pd.DataFrame:
    """Load the model-ready dataframe once for all tests."""
    return load_data()


@pytest.fixture
def split(df_model: pd.DataFrame) -> SplitResult:
    """Split the data once for all tests that need train/test sets."""
    return split_data(df_model)


@pytest.fixture
def model(split: SplitResult) -> RandomForestClassifier:
    """Train the model once for all tests that need a fitted model."""
    X_train, _, y_train, _ = split
    return train_model(X_train, y_train)


# === SECTION 2. LOAD DATA TESTS ===


def test_load_data_returns_dataframe(df_model: pd.DataFrame) -> None:
    """load_data returns a non-empty DataFrame."""
    assert isinstance(df_model, pd.DataFrame)
    assert df_model.shape[0] > 0


def test_load_data_has_required_columns(df_model: pd.DataFrame) -> None:
    """load_data returns a DataFrame with all required columns."""
    required = [TARGET_COL, *FEATURE_COLS]
    for col in required:
        assert col in df_model.columns, f"Missing column: {col}"


def test_load_data_no_missing_values(df_model: pd.DataFrame) -> None:
    """load_data returns a DataFrame with no missing values in required columns."""
    required = [TARGET_COL, *FEATURE_COLS]
    assert df_model[required].isna().sum().sum() == 0


# === SECTION 3. SPLIT DATA TESTS ===


def test_split_returns_four_parts(split: SplitResult) -> None:
    """split_data returns exactly four parts."""
    assert len(split) == 4


def test_split_sizes(df_model: pd.DataFrame, split: SplitResult) -> None:
    """Train and test sizes match TEST_SIZE."""
    X_train, X_test, _, _ = split
    total = len(df_model)
    expected_test = round(total * TEST_SIZE)
    assert len(X_test) == pytest.approx(expected_test, abs=1)
    assert len(X_train) + len(X_test) == total


def test_split_feature_columns(split: SplitResult) -> None:
    """X_train and X_test contain exactly FEATURE_COLS."""
    X_train, X_test, _, _ = split
    assert list(X_train.columns) == FEATURE_COLS
    assert list(X_test.columns) == FEATURE_COLS


def test_split_target_values(split: SplitResult) -> None:
    """y_train and y_test contain only known species labels."""
    _, _, y_train, y_test = split
    known = {"Adelie", "Chinstrap", "Gentoo"}
    assert set(y_train.unique()).issubset(known)
    assert set(y_test.unique()).issubset(known)


# === SECTION 4. TRAIN MODEL TESTS ===


def test_train_model_returns_classifier(model: RandomForestClassifier) -> None:
    """train_model returns a fitted RandomForestClassifier."""
    assert isinstance(model, RandomForestClassifier)


def test_train_model_has_feature_names(model: RandomForestClassifier) -> None:
    """The fitted model knows its feature names."""
    assert list(model.feature_names_in_) == FEATURE_COLS


def test_train_model_classes(model: RandomForestClassifier) -> None:
    """The fitted model knows all three species."""
    assert set(model.classes_) == {"Adelie", "Chinstrap", "Gentoo"}


# === SECTION 5. EVALUATE MODEL TESTS ===


def test_evaluate_model_runs(model: RandomForestClassifier, split: SplitResult) -> None:
    """evaluate_model runs without raising an exception."""
    _, X_test, _, y_test = split
    evaluate_model(model, X_test, y_test)  # should not raise


def test_evaluate_model_reasonable_accuracy(
    model: RandomForestClassifier, split: SplitResult
) -> None:
    """Test accuracy on penguins should be well above chance (> 0.80)."""
    from sklearn.metrics import accuracy_score

    _, X_test, _, y_test = split
    acc: float = float(accuracy_score(y_test, model.predict(X_test)))
    assert acc > 0.80, f"Accuracy too low: {acc:.3f}"


# === SECTION 6. SAVE MODEL TESTS ===


def test_save_model_creates_file(
    model: RandomForestClassifier,
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """save_model writes a file to MODEL_PATH."""
    import bizintel.model_builder_case as mb

    tmp_model_path = tmp_path / "model.joblib"
    monkeypatch.setattr(mb, "MODEL_PATH", tmp_model_path)

    mb.save_model(model)

    assert tmp_model_path.exists()
    assert tmp_model_path.stat().st_size > 0


def test_save_model_reloadable(
    model: RandomForestClassifier,
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """The saved artifact can be reloaded with joblib and still predicts."""

    tmp_model_path = tmp_path / "model.joblib"
    monkeypatch.setattr(mb, "MODEL_PATH", tmp_model_path)

    mb.save_model(model)

    reloaded = joblib.load(tmp_model_path)
    sample = pd.DataFrame(
        [
            {
                "bill_length_mm": 45.0,
                "bill_depth_mm": 17.0,
                "flipper_length_mm": 200.0,
                "body_mass_g": 4000.0,
            }
        ]
    )
    prediction = reloaded.predict(sample)
    assert prediction[0] in {"Adelie", "Chinstrap", "Gentoo"}
