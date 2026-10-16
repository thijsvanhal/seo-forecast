from typing import Any, Dict

import streamlit as st
from streamlit_prophet.lib.utils.load import load_dataset
from streamlit_prophet.lib.utils.mapping import convert_into_nb_of_seconds, mapping_freq_names


def input_opportunity(
    config: Dict[Any, Any],
    readme: Dict[Any, Any],
    load_options: Dict[Any, Any],
    resampling: Dict[Any, Any],
    date_col: str,
    target_col: str,
) -> Dict[Any, Any]:
    """Lets the user upload a dataset of keyword opportunities and enter scenario assumptions.

    Parameters
    ----------
    config : Dict
        Lib config dictionary containing default scenario assumptions.
    readme : Dict
        Dictionary containing tooltips to guide user's choices.
    load_options : Dict
        Loading options selected by user (separator, date format).
    resampling : Dict
        Dictionary containing dataset frequency information.
    date_col : str
        Name of date column in main dataset, used as default for the opportunity dataset.
    target_col : str
        Name of target column in main dataset, used as default for the opportunity dataset.

    Returns
    -------
    dict
        Opportunity specifications, empty if no file was uploaded.
    """
    opportunity: Dict[Any, Any] = dict()
    file = st.file_uploader(
        "Upload a csv file with keyword opportunities",
        type="csv",
        help=readme["tooltips"]["opportunity_upload"],
    )
    if not file:
        return opportunity
    df = load_dataset(file, load_options)
    cols = sorted(df.columns)
    opportunity["date_col"] = st.selectbox(
        "Opportunity date column",
        cols,
        index=cols.index(date_col) if date_col in cols else 0,
        help=readme["tooltips"]["date_column"],
    )
    volume_cols = [col for col in cols if col != opportunity["date_col"]]
    opportunity["volume_col"] = st.selectbox(
        "Opportunity volume column",
        volume_cols,
        index=volume_cols.index(target_col) if target_col in volume_cols else 0,
        help=readme["tooltips"]["opportunity_volume_column"],
    )
    defaults = config["opportunity"]
    freq = resampling["freq"][-1]
    freq_name = mapping_freq_names(freq)
    seconds_per_period = convert_into_nb_of_seconds(freq, 1)
    opportunity["capture_rate"] = (
        st.slider(
            "Share of opportunity volume captured (%)",
            min_value=0,
            max_value=100,
            value=defaults["capture_rate"],
            help=readme["tooltips"]["opportunity_capture_rate"],
        )
        / 100
    )
    opportunity["delay"] = st.number_input(
        f"Delay before ranking (in {freq_name})",
        min_value=0,
        value=defaults["delay_days"] * 86400 // seconds_per_period,
        help=readme["tooltips"]["opportunity_delay"],
    )
    opportunity["ramp_up"] = st.number_input(
        f"Ramp-up to full capture (in {freq_name})",
        min_value=0,
        value=defaults["ramp_up_days"] * 86400 // seconds_per_period,
        help=readme["tooltips"]["opportunity_ramp_up"],
    )
    opportunity["uploaded"] = df
    return opportunity
