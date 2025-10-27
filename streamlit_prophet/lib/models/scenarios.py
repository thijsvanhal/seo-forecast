from typing import Any, Dict, List
import numpy as np
import pandas as pd


def calculate_effect_curve(
    dates: pd.DatetimeIndex,
    start_date: pd.Timestamp,
    delay_months: float,
    accel_months: float,
    plateau_rate: float,
    max_effect: float,
) -> np.ndarray:
    """Calculate effect curve with delay, S-curve acceleration, and linear plateau.
    
    Parameters
    ----------
    dates : pd.DatetimeIndex
        Dates for which to calculate the effect curve.
    start_date : pd.Timestamp
        Start date of the scenario intervention.
    delay_months : float
        Number of months before any effect begins.
    accel_months : float
        Number of months for the acceleration (S-curve) phase.
    plateau_rate : float
        Linear growth rate during plateau phase (as fraction, e.g., 0.01 for 1% per month).
    max_effect : float
        Maximum effect reached at end of acceleration phase.
    
    Returns
    -------
    np.ndarray
        Array of effect values for each date.
    """
    # Convert dates to months since start
    days_since_start = (dates - start_date).days
    months_since_start = days_since_start / 30.44  # Average days per month
    
    effect = np.zeros(len(dates))
    
    for i, months in enumerate(months_since_start):
        if months < delay_months:
            # Phase 1: Delay period - no effect
            effect[i] = 0
        elif months < delay_months + accel_months:
            # Phase 2: S-curve acceleration using sigmoid
            # Map to range [0, accel_months]
            t = months - delay_months
            # Sigmoid centered at midpoint with steepness k
            k = 8 / accel_months  # Steepness parameter (adjust for desired curve shape)
            midpoint = accel_months / 2
            sigmoid = 1 / (1 + np.exp(-k * (t - midpoint)))
            effect[i] = max_effect * sigmoid
        else:
            # Phase 3: Linear plateau - continued growth at reduced rate
            months_in_plateau = months - (delay_months + accel_months)
            plateau_growth = max_effect * plateau_rate * months_in_plateau
            effect[i] = max_effect + plateau_growth
    
    return effect


def apply_numeric_scenario(
    baseline_forecast: pd.DataFrame,
    budget: float,
    content: float,
    backlinks: float,
    coefficients: Dict[str, float],
    delay_months: float,
    accel_months: float,
    plateau_rate: float,
    start_date: pd.Timestamp,
) -> pd.DataFrame:
    """Apply numeric scenario with budget, content, and backlink changes.
    
    Parameters
    ----------
    baseline_forecast : pd.DataFrame
        Baseline forecast from Prophet model.
    budget : float
        Monthly budget increase (e.g., 5000 for $5000/month).
    content : float
        Additional content pieces per month.
    backlinks : float
        Additional backlinks per month.
    coefficients : Dict[str, float]
        Coefficients mapping interventions to traffic impact:
        - 'budget': traffic per $1000
        - 'content': traffic per article
        - 'backlinks': traffic per backlink
    delay_months : float
        Delay before effects begin.
    accel_months : float
        Acceleration period in months.
    plateau_rate : float
        Plateau growth rate (fraction per month).
    start_date : pd.Timestamp
        Start date of scenario.
    
    Returns
    -------
    pd.DataFrame
        Forecast with scenario effects applied.
    """
    scenario_forecast = baseline_forecast.copy()
    dates = pd.to_datetime(scenario_forecast['ds'])
    
    # Calculate total maximum effect from all interventions
    budget_effect = (budget / 1000) * coefficients['budget']
    content_effect = content * coefficients['content']
    backlinks_effect = backlinks * coefficients['backlinks']
    total_max_effect = budget_effect + content_effect + backlinks_effect
    
    # Calculate effect curve
    effect_curve = calculate_effect_curve(
        dates, start_date, delay_months, accel_months, plateau_rate, total_max_effect
    )
    
    # Apply effect to forecast
    scenario_forecast['yhat'] = baseline_forecast['yhat'] + effect_curve
    scenario_forecast['yhat_lower'] = baseline_forecast['yhat_lower'] + effect_curve * 0.8
    scenario_forecast['yhat_upper'] = baseline_forecast['yhat_upper'] + effect_curve * 1.2
    
    return scenario_forecast


def apply_percentage_scenario(
    baseline_forecast: pd.DataFrame,
    pct_increase: float,
    delay_months: float,
    duration_months: float,
    start_date: pd.Timestamp,
) -> pd.DataFrame:
    """Apply simple percentage increase scenario.
    
    Parameters
    ----------
    baseline_forecast : pd.DataFrame
        Baseline forecast from Prophet model.
    pct_increase : float
        Target percentage increase (e.g., 25 for 25%).
    delay_months : float
        Delay before effects begin.
    duration_months : float
        Duration to reach target percentage (acceleration period).
    start_date : pd.Timestamp
        Start date of scenario.
    
    Returns
    -------
    pd.DataFrame
        Forecast with scenario effects applied.
    """
    scenario_forecast = baseline_forecast.copy()
    dates = pd.to_datetime(scenario_forecast['ds'])
    
    # Calculate max effect as percentage of baseline at end of forecast
    baseline_mean = baseline_forecast['yhat'].mean()
    max_effect = baseline_mean * (pct_increase / 100)
    
    # Use minimal plateau rate for simple scenarios (0.5% per month)
    plateau_rate = 0.005
    
    # Calculate effect curve
    effect_curve = calculate_effect_curve(
        dates, start_date, delay_months, duration_months, plateau_rate, max_effect
    )
    
    # Apply effect to forecast
    scenario_forecast['yhat'] = baseline_forecast['yhat'] + effect_curve
    scenario_forecast['yhat_lower'] = baseline_forecast['yhat_lower'] + effect_curve * 0.8
    scenario_forecast['yhat_upper'] = baseline_forecast['yhat_upper'] + effect_curve * 1.2
    
    return scenario_forecast


def generate_scenario_forecast(
    baseline_forecast: pd.DataFrame,
    scenario_config: Dict[Any, Any],
    start_date: pd.Timestamp,
) -> pd.DataFrame:
    """Generate forecast for a scenario based on its configuration.
    
    Parameters
    ----------
    baseline_forecast : pd.DataFrame
        Baseline forecast from Prophet model.
    scenario_config : Dict
        Scenario configuration containing mode and parameters.
    start_date : pd.Timestamp
        Start date for the scenario effect.
    
    Returns
    -------
    pd.DataFrame
        Forecast with scenario effects applied.
    """
    if scenario_config['mode'] == 'numeric':
        return apply_numeric_scenario(
            baseline_forecast=baseline_forecast,
            budget=scenario_config['budget'],
            content=scenario_config['content'],
            backlinks=scenario_config['backlinks'],
            coefficients=scenario_config['coefficients'],
            delay_months=scenario_config['delay_months'],
            accel_months=scenario_config['accel_months'],
            plateau_rate=scenario_config['plateau_rate'],
            start_date=start_date,
        )
    elif scenario_config['mode'] == 'percentage':
        return apply_percentage_scenario(
            baseline_forecast=baseline_forecast,
            pct_increase=scenario_config['pct_increase'],
            delay_months=scenario_config['delay_months'],
            duration_months=scenario_config['duration_months'],
            start_date=start_date,
        )
    else:
        raise ValueError(f"Unknown scenario mode: {scenario_config['mode']}")


def generate_scenario_forecasts(
    baseline_forecast: pd.DataFrame,
    scenarios: List[Dict[Any, Any]],
    forecast_start_date: pd.Timestamp,
) -> Dict[str, pd.DataFrame]:
    """Generate forecasts for all scenarios.
    
    Parameters
    ----------
    baseline_forecast : pd.DataFrame
        Baseline forecast from Prophet model.
    scenarios : List[Dict]
        List of scenario configurations.
    forecast_start_date : pd.Timestamp
        Start date of the forecast period.
    
    Returns
    -------
    Dict[str, pd.DataFrame]
        Dictionary mapping scenario names to their forecasts.
    """
    scenario_forecasts = {}
    
    for scenario in scenarios:
        scenario_name = scenario['name']
        scenario_forecast = generate_scenario_forecast(
            baseline_forecast=baseline_forecast,
            scenario_config=scenario,
            start_date=forecast_start_date,
        )
        scenario_forecasts[scenario_name] = scenario_forecast
    
    return scenario_forecasts

