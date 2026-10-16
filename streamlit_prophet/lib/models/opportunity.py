from typing import Any, Dict

import numpy as np
import pandas as pd

PERIOD_ALIASES = {"s": "s", "H": "h", "D": "D", "W": "W", "M": "M", "Q": "Q", "Y": "Y"}


def project_opportunity(
    opportunity_df: pd.DataFrame, future_ds: pd.Series, freq: str
) -> pd.Series:
    """Projects the opportunity volume on future dates.

    Each future date takes the volume observed for the same period if the opportunity dataset
    covers it, otherwise the volume of the same period in the most recent year available.

    Parameters
    ----------
    opportunity_df : pd.DataFrame
        Prepared opportunity dataframe, with 'ds' and 'y' columns.
    future_ds : pd.Series
        Dates to project the opportunity volume on.
    freq : str
        Dataset frequency.

    Returns
    -------
    pd.Series
        Projected volume, aligned on future_ds index. NaN where no matching period was found.
    """
    period = PERIOD_ALIASES[freq[-1]]
    observed = opportunity_df.groupby(opportunity_df["ds"].dt.to_period(period))["y"].sum()
    projected = pd.Series(np.nan, index=future_ds.index, dtype="float")
    max_years_back = future_ds.max().year - opportunity_df["ds"].min().year
    for years_back in range(max_years_back + 1):
        missing = projected.isna()
        if not missing.any():
            break
        periods = (future_ds[missing] - pd.DateOffset(years=years_back)).dt.to_period(period)
        projected[missing] = periods.map(observed).to_numpy(dtype="float")
    return projected


def get_capture_curve(
    n_periods: int, capture_rate: float, delay: int, ramp_up: int
) -> np.ndarray:
    """Computes the share of opportunity volume captured for each forecast period.

    Nothing is captured during the delay, then the share grows linearly to capture_rate
    over the ramp-up periods and stays there.

    Parameters
    ----------
    n_periods : int
        Number of forecast periods.
    capture_rate : float
        Share of the opportunity volume captured once fully ranking (between 0 and 1).
    delay : int
        Number of periods before the new keywords start contributing.
    ramp_up : int
        Number of periods to go from first contribution to full capture.

    Returns
    -------
    np.ndarray
        Captured share for each forecast period.
    """
    periods_since_delay = np.arange(n_periods) - delay + 1
    if ramp_up == 0:
        progress = (periods_since_delay >= 1).astype(float)
    else:
        progress = np.clip(periods_since_delay / ramp_up, 0, 1)
    return capture_rate * progress


def make_opportunity_forecast(
    forecast: pd.DataFrame,
    opportunity: Dict[Any, Any],
    dates: Dict[Any, Any],
    resampling: Dict[Any, Any],
) -> pd.DataFrame:
    """Adds the expected contribution of opportunity keywords on top of the baseline forecast.

    Parameters
    ----------
    forecast : pd.DataFrame
        Baseline future forecast made by Prophet.
    opportunity : Dict
        Prepared opportunity dataframe ('df') and scenario assumptions (capture_rate, delay, ramp_up).
    dates : Dict
        Dictionary containing future forecast dates information.
    resampling : Dict
        Dictionary containing dataset frequency information.

    Returns
    -------
    pd.DataFrame
        One row per forecast period with baseline, opportunity volume, captured share,
        uplift and scenario forecast.
    """
    future = forecast.loc[
        forecast["ds"] >= pd.to_datetime(dates["forecast_start_date"]), ["ds", "yhat"]
    ]
    scenario = future.sort_values("ds").reset_index(drop=True)
    scenario = scenario.rename(columns={"yhat": "baseline"})
    scenario["opportunity_volume"] = project_opportunity(
        opportunity["df"], scenario["ds"], resampling["freq"]
    )
    scenario["captured_share"] = get_capture_curve(
        len(scenario), opportunity["capture_rate"], opportunity["delay"], opportunity["ramp_up"]
    )
    scenario["uplift"] = scenario["opportunity_volume"].fillna(0) * scenario["captured_share"]
    scenario["scenario"] = scenario["baseline"] + scenario["uplift"]
    return scenario
