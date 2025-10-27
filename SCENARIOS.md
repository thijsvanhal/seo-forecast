# SEO Scenario Forecasting

## Overview

This feature extends the Streamlit Prophet app with SEO scenario forecasting capabilities. It allows you to model the impact of different SEO strategies (budget increases, content production, backlink acquisition) on your traffic forecast with delayed effects and realistic growth curves.

## Features

### Two Scenario Modes

1. **Numeric Mode** (Budget/Content/Backlinks)
   - Define specific interventions: monthly budget, content pieces, and backlinks
   - Customize impact coefficients (traffic per $1000, per article, per backlink)
   - Combine multiple interventions in a single scenario
   - Fine-tune timing parameters (delay, acceleration, plateau growth)

2. **Simple Percentage Mode**
   - Define a target traffic increase as a percentage
   - Set delay and ramp-up duration
   - Quick way to model overall SEO improvements

### Realistic Effect Modeling

All scenarios use a three-phase growth model:

1. **Delay Phase**: No effect (typical SEO delay: 2-4 months)
2. **Acceleration Phase**: S-curve growth using sigmoid function (typical: 4-8 months)
3. **Plateau Phase**: Continued linear growth at reduced rate (typical: 0.5-2% per month)

This models real SEO behavior where:
- Changes take time to be indexed and ranked
- Effects accelerate as rankings improve
- Growth continues but slows after reaching peak

## How to Use

### Step 1: Enable Future Forecast
Scenario analysis requires future forecasting to be enabled. Check "Make forecast on future dates" in section 4 of the sidebar.

### Step 2: Enable Scenario Analysis
In section 5 of the sidebar, check "Add scenario analysis".

### Step 3: Configure Scenarios

#### For Numeric Mode:
1. Select "Numeric (Budget/Content/Backlinks)" as the scenario mode
2. Set the number of scenarios (1-10)
3. For each scenario:
   - Give it a descriptive name
   - Set intervention levels:
     - Monthly budget increase ($)
     - Content pieces per month
     - Backlinks per month
   - Adjust impact coefficients in "Advanced Parameters":
     - Traffic per $1000 budget (default: 50)
     - Traffic per article (default: 100)
     - Traffic per backlink (default: 10)
   - Configure timing:
     - Delay before effects begin (default: 2 months)
     - Acceleration period (default: 6 months)
     - Plateau growth rate (default: 1% per month)

#### For Simple Percentage Mode:
1. Select "Simple Percentage" as the scenario mode
2. Set the number of scenarios
3. For each scenario:
   - Give it a descriptive name
   - Set target traffic increase (%)
   - Set delay period (months)
   - Set ramp-up duration (months)

### Step 4: Launch Forecast
Click "Launch forecast" to generate the baseline forecast and all scenarios.

### Step 5: Review Results
The scenario analysis section shows:
- **Scenario Comparison Chart**: All scenarios overlaid on baseline with interactive legend
- **Scenario Summary Table**: Total traffic, difference vs baseline, and % change
- **Scenario Details**: Expandable sections with full configuration for each scenario

## Example Scenarios

### Example 1: Aggressive Content Strategy (Numeric)
- **Budget**: $0
- **Content**: 20 articles/month
- **Backlinks**: 5/month
- **Expected Peak Impact**: 2,050 visitors/day (20×100 + 5×10)

### Example 2: Paid + Content Mix (Numeric)
- **Budget**: $10,000/month
- **Content**: 10 articles/month
- **Backlinks**: 15/month
- **Expected Peak Impact**: 1,650 visitors/day (10×50 + 10×100 + 15×10)

### Example 3: Overall Growth Target (Percentage)
- **Target Increase**: 30%
- **Delay**: 3 months
- **Ramp-up**: 9 months

## Customizing Impact Coefficients

The default coefficients are starting points. Adjust them based on:

### Budget Coefficient (default: 50 per $1000)
- Industry competitiveness
- Geographic targeting
- Channel mix (paid search, tools, agencies)
- Historical ROI data

### Content Coefficient (default: 100 per article)
- Average article word count and quality
- Topic relevance and search volume
- Historical article performance
- Content promotion strategy

### Backlink Coefficient (default: 10 per backlink)
- Backlink quality (DR/DA of linking sites)
- Relevance to your niche
- Link placement (contextual vs footer)
- Historical correlation with traffic

## Technical Details

### Effect Curve Formula

The S-curve acceleration uses a sigmoid function:

```
effect(t) = max_effect / (1 + exp(-k × (t - midpoint)))
```

Where:
- `k = 8 / acceleration_months` (steepness parameter)
- `midpoint = acceleration_months / 2`
- `t` = months since end of delay period

### Confidence Intervals

Scenario forecasts include adjusted confidence intervals:
- Lower bound: baseline_lower + effect × 0.8
- Upper bound: baseline_upper + effect × 1.2

This accounts for additional uncertainty in intervention impacts.

## Tips for Accurate Forecasts

1. **Use Historical Data**: Base coefficients on your past performance
2. **Start Conservative**: It's better to underestimate than overestimate
3. **Test Multiple Scenarios**: Compare optimistic, realistic, and conservative cases
4. **Consider Seasonality**: The baseline forecast already includes seasonality
5. **Update Regularly**: Refine coefficients as you gather more data

## Export and Reporting

All scenario data is included when you save the experiment:
- Scenario comparison chart
- Summary metrics table
- Individual scenario forecasts
- Full scenario configurations

## Limitations

- Maximum 10 scenarios per analysis
- Scenarios only apply to future forecast period
- Linear combination of intervention effects (no interaction modeling)
- Assumes consistent intervention levels throughout forecast period

## Support

For questions or issues with scenario forecasting:
1. Check the tooltips in the app (hover over ⓘ icons)
2. Review this documentation
3. Verify your baseline forecast is reasonable before adding scenarios
4. Start with simple percentage scenarios to understand the feature

## Version

SEO Scenario Forecasting v1.0 (October 2025)

