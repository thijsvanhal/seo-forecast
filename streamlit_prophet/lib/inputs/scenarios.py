from typing import Any, Dict, List
import streamlit as st


def input_scenarios(
    config: Dict[Any, Any],
    readme: Dict[Any, Any],
) -> List[Dict[Any, Any]]:
    """Let user configure SEO scenarios for forecasting.
    
    Parameters
    ----------
    config : Dict
        Configuration dictionary with default values.
    readme : Dict
        Dictionary containing tooltips for user guidance.
    
    Returns
    -------
    List[Dict]
        List of scenario configurations.
    """
    scenarios = []
    
    # Initialize session state for scenarios if not exists
    if 'scenario_count' not in st.session_state:
        st.session_state.scenario_count = 0
    if 'scenarios_list' not in st.session_state:
        st.session_state.scenarios_list = []
    
    # Mode selection
    scenario_mode = st.selectbox(
        "Scenario Mode",
        ["Numeric (Budget/Content/Backlinks)", "Simple Percentage"],
        help=readme["tooltips"]["scenario_mode"],
    )
    
    mode = "numeric" if "Numeric" in scenario_mode else "percentage"
    
    # Number of scenarios
    num_scenarios = st.number_input(
        "Number of scenarios",
        min_value=1,
        max_value=config["scenarios"]["max_scenarios"],
        value=1,
        help=readme["tooltips"]["num_scenarios"],
    )
    
    # Create scenarios
    for i in range(num_scenarios):
        st.markdown(f"### Scenario {i+1}")
        
        scenario_name = st.text_input(
            f"Scenario name",
            value=f"Scenario {i+1}",
            key=f"scenario_name_{i}",
            help=readme["tooltips"]["scenario_name"],
        )
        
        scenario = {
            'name': scenario_name,
            'mode': mode,
        }
        
        if mode == 'numeric':
            scenario.update(_input_numeric_scenario(i, config, readme))
        else:
            scenario.update(_input_percentage_scenario(i, config, readme))
        
        scenarios.append(scenario)
        
        if i < num_scenarios - 1:
            st.markdown("---")
    
    return scenarios


def _input_numeric_scenario(
    index: int,
    config: Dict[Any, Any],
    readme: Dict[Any, Any],
) -> Dict[Any, Any]:
    """Input parameters for numeric scenario.
    
    Parameters
    ----------
    index : int
        Scenario index for unique keys.
    config : Dict
        Configuration with defaults.
    readme : Dict
        Tooltips dictionary.
    
    Returns
    -------
    Dict
        Numeric scenario parameters.
    """
    defaults = config["scenarios"]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        budget = st.number_input(
            "Monthly Budget ($)",
            min_value=0.0,
            value=defaults["default_budget"],
            step=1000.0,
            key=f"budget_{index}",
            help=readme["tooltips"]["scenario_budget"],
        )
    
    with col2:
        content = st.number_input(
            "Content Pieces/Month",
            min_value=0.0,
            value=defaults["default_content"],
            step=1.0,
            key=f"content_{index}",
            help=readme["tooltips"]["scenario_content"],
        )
    
    with col3:
        backlinks = st.number_input(
            "Backlinks/Month",
            min_value=0.0,
            value=defaults["default_backlinks"],
            step=1.0,
            key=f"backlinks_{index}",
            help=readme["tooltips"]["scenario_backlinks"],
        )
    
    # Advanced parameters in expander
    with st.expander("Advanced Parameters", expanded=False):
        st.markdown("**Impact Coefficients** (Traffic increase per unit)")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            budget_coef = st.number_input(
                "Traffic per $1000",
                min_value=0.0,
                value=defaults["budget_coefficient"],
                step=10.0,
                key=f"budget_coef_{index}",
                help=readme["tooltips"]["budget_coefficient"],
            )
        
        with col2:
            content_coef = st.number_input(
                "Traffic per Article",
                min_value=0.0,
                value=defaults["content_coefficient"],
                step=10.0,
                key=f"content_coef_{index}",
                help=readme["tooltips"]["content_coefficient"],
            )
        
        with col3:
            backlinks_coef = st.number_input(
                "Traffic per Backlink",
                min_value=0.0,
                value=defaults["backlink_coefficient"],
                step=1.0,
                key=f"backlinks_coef_{index}",
                help=readme["tooltips"]["backlink_coefficient"],
            )
        
        st.markdown("**Effect Timing**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            delay_months = st.number_input(
                "Delay (months)",
                min_value=0.0,
                value=defaults["default_delay"],
                step=0.5,
                key=f"delay_{index}",
                help=readme["tooltips"]["scenario_delay"],
            )
        
        with col2:
            accel_months = st.number_input(
                "Acceleration Period (months)",
                min_value=1.0,
                value=defaults["default_acceleration"],
                step=1.0,
                key=f"accel_{index}",
                help=readme["tooltips"]["scenario_acceleration"],
            )
        
        with col3:
            plateau_rate = st.number_input(
                "Plateau Growth Rate (%/month)",
                min_value=0.0,
                max_value=10.0,
                value=defaults["default_plateau_rate"] * 100,
                step=0.1,
                key=f"plateau_{index}",
                help=readme["tooltips"]["scenario_plateau"],
            ) / 100  # Convert percentage to fraction
    
    return {
        'budget': budget,
        'content': content,
        'backlinks': backlinks,
        'coefficients': {
            'budget': budget_coef,
            'content': content_coef,
            'backlinks': backlinks_coef,
        },
        'delay_months': delay_months,
        'accel_months': accel_months,
        'plateau_rate': plateau_rate,
    }


def _input_percentage_scenario(
    index: int,
    config: Dict[Any, Any],
    readme: Dict[Any, Any],
) -> Dict[Any, Any]:
    """Input parameters for simple percentage scenario.
    
    Parameters
    ----------
    index : int
        Scenario index for unique keys.
    config : Dict
        Configuration with defaults.
    readme : Dict
        Tooltips dictionary.
    
    Returns
    -------
    Dict
        Percentage scenario parameters.
    """
    defaults = config["scenarios"]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        pct_increase = st.number_input(
            "Target Traffic Increase (%)",
            min_value=0.0,
            max_value=500.0,
            value=defaults["default_pct_increase"],
            step=5.0,
            key=f"pct_{index}",
            help=readme["tooltips"]["scenario_percentage"],
        )
    
    with col2:
        delay_months = st.number_input(
            "Delay (months)",
            min_value=0.0,
            value=defaults["default_delay"],
            step=0.5,
            key=f"pct_delay_{index}",
            help=readme["tooltips"]["scenario_delay"],
        )
    
    with col3:
        duration_months = st.number_input(
            "Ramp-up Duration (months)",
            min_value=1.0,
            value=defaults["default_acceleration"],
            step=1.0,
            key=f"duration_{index}",
            help=readme["tooltips"]["scenario_duration"],
        )
    
    return {
        'pct_increase': pct_increase,
        'delay_months': delay_months,
        'duration_months': duration_months,
    }

