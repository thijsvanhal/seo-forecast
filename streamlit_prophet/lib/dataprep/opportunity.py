from typing import Any, Dict

import pandas as pd
import streamlit as st
from streamlit_prophet.lib.dataprep.format import (
    format_date_and_target,
    format_datetime,
    resample_df,
)
from streamlit_prophet.lib.inputs.dataprep import _autodetect_freq
from streamlit_prophet.lib.utils.mapping import mapping_freq_names

FREQ_ORDER = ["s", "H", "D", "W", "M", "Q", "Y"]


def prepare_opportunity_df(
    opportunity: Dict[Any, Any],
    config: Dict[Any, Any],
    load_options: Dict[Any, Any],
    resampling: Dict[Any, Any],
) -> pd.DataFrame:
    """Formats the opportunity dataset into a single time series at the main dataset frequency.

    Parameters
    ----------
    opportunity : Dict
        Opportunity specifications (uploaded dataframe, date and volume column names).
    config : Dict
        Lib configuration dictionary.
    load_options : Dict
        Loading options selected by user.
    resampling : Dict
        Resampling specifications of the main dataset.

    Returns
    -------
    pd.DataFrame
        Opportunity dataframe with 'ds' and 'y' columns, one row per period.
    """
    df = format_date_and_target(
        opportunity["uploaded"],
        opportunity["date_col"],
        opportunity["volume_col"],
        config,
        load_options,
    )
    # Sum all keywords at each date into one opportunity series
    df = df.groupby("ds", as_index=False)["y"].sum()
    if len(df) < 2:
        st.error("The opportunity dataset should contain at least 2 distinct dates.")
        st.stop()
    target_freq = resampling["freq"][-1]
    opportunity_freq = _autodetect_freq(df)[-1]
    if FREQ_ORDER.index(opportunity_freq) > FREQ_ORDER.index(target_freq):
        st.error(
            f"The opportunity dataset is in {mapping_freq_names(opportunity_freq)} while the forecast "
            f"is in {mapping_freq_names(target_freq)}. Please resample the main dataset to "
            f"{mapping_freq_names(opportunity_freq)} or upload opportunity data at the same frequency."
        )
        st.stop()
    if opportunity_freq != target_freq:
        agg = resampling["agg"] if resampling["resample"] else "Sum"
        df = resample_df(df, {"resample": True, "freq": target_freq, "agg": agg})
    return format_datetime(df, resampling)
