import numpy as np
import pandas as pd
import pytest
from streamlit_prophet.lib.models.opportunity import (
    get_capture_curve,
    make_opportunity_forecast,
    project_opportunity,
)


@pytest.mark.parametrize(
    "delay, ramp_up, expected",
    [
        (0, 0, [1, 1, 1, 1]),
        (2, 0, [0, 0, 1, 1]),
        (0, 4, [0.25, 0.5, 0.75, 1]),
        (1, 2, [0, 0.5, 1, 1]),
        (5, 2, [0, 0, 0, 0]),
    ],
)
def test_get_capture_curve(delay, ramp_up, expected):
    output = get_capture_curve(4, capture_rate=0.5, delay=delay, ramp_up=ramp_up)
    np.testing.assert_allclose(output, 0.5 * np.array(expected))


def test_project_opportunity_uses_same_period_when_available():
    opportunity_df = pd.DataFrame(
        {"ds": pd.date_range("2025-01-01", periods=3, freq="MS"), "y": [10.0, 20.0, 30.0]}
    )
    future_ds = pd.Series(pd.date_range("2025-02-01", periods=2, freq="MS"))
    output = project_opportunity(opportunity_df, future_ds, "M")
    assert output.tolist() == [20.0, 30.0]


def test_project_opportunity_repeats_most_recent_year():
    opportunity_df = pd.DataFrame(
        {"ds": pd.date_range("2023-01-01", periods=24, freq="MS"), "y": np.arange(24.0)}
    )
    future_ds = pd.Series(pd.date_range("2025-01-01", periods=14, freq="MS"))
    output = project_opportunity(opportunity_df, future_ds, "M")
    # Values of 2024, the most recent year available, repeated each year
    assert output.tolist() == list(np.arange(12.0, 24.0)) + [12.0, 13.0]


def test_project_opportunity_matches_periods_with_different_anchors():
    opportunity_df = pd.DataFrame(
        {"ds": pd.date_range("2025-01-01", periods=12, freq="MS"), "y": np.arange(12.0)}
    )
    future_ds = pd.Series(pd.date_range("2026-01-31", periods=3, freq="ME"))
    output = project_opportunity(opportunity_df, future_ds, "M")
    assert output.tolist() == [0.0, 1.0, 2.0]


def test_project_opportunity_returns_nan_without_matching_period():
    opportunity_df = pd.DataFrame(
        {"ds": pd.date_range("2025-01-01", periods=3, freq="MS"), "y": [10.0, 20.0, 30.0]}
    )
    future_ds = pd.Series(pd.date_range("2026-03-01", periods=2, freq="MS"))
    output = project_opportunity(opportunity_df, future_ds, "M")
    assert output.iloc[0] == 30.0
    assert np.isnan(output.iloc[1])


def test_make_opportunity_forecast():
    forecast = pd.DataFrame(
        {"ds": pd.date_range("2025-10-01", periods=6, freq="MS"), "yhat": [100.0] * 6}
    )
    opportunity = {
        "df": pd.DataFrame(
            {"ds": pd.date_range("2025-01-01", periods=12, freq="MS"), "y": [40.0] * 12}
        ),
        "capture_rate": 0.5,
        "delay": 1,
        "ramp_up": 2,
    }
    dates = {"forecast_start_date": pd.Timestamp("2026-01-01")}
    output = make_opportunity_forecast(forecast, opportunity, dates, {"freq": "M"})
    # Only forecast periods are kept, history is untouched
    assert output["ds"].min() == pd.Timestamp("2026-01-01")
    assert output["uplift"].tolist() == [0.0, 10.0, 20.0]
    assert output["scenario"].tolist() == [100.0, 110.0, 120.0]
