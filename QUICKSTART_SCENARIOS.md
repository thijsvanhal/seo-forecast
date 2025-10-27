# Quick Start: Investment Scenario Simulation

## 5-Minute Setup Guide

### Step 1: Prepare Your Data (2 minutes)

Create a CSV with these columns:
- **date**: Your time series dates
- **target**: What you want to forecast (e.g., organic_traffic)
- **investment metrics**: Columns like seo_investment, content_published, backlinks_acquired

**Download and use our example:** [example_seo_data.csv](example_seo_data.csv)

### Step 2: Load and Configure (1 minute)

1. Run the app: `streamlit_prophet deploy dashboard`
2. Upload your CSV
3. Select date column and target column
4. In sidebar → **Regressors** → Select your investment metrics (e.g., seo_investment, content_published)

### Step 3: Enable Lag Effects (30 seconds)

1. In sidebar → **Lag Effects** 
2. Check "Enable lag effects (recommended for SEO)"
3. Use "Quick (suggested)" for each regressor
4. You'll see: "✓ Applied X lagged features"

### Step 4: Create Scenarios (1 minute)

1. Check "Make forecast on future dates" → Set horizon (e.g., 12 months)
2. In sidebar → **Scenarios** → Check "Enable scenario comparison"
3. Set number of scenarios (try 3):

**Scenario 1: "Baseline"**
- seo_investment: Constant → 0
- content_published: Constant → 0
- backlinks_acquired: Constant → 0

**Scenario 2: "Moderate SEO"**
- seo_investment: Constant → 5000
- content_published: Constant → 10
- backlinks_acquired: Constant → 5

**Scenario 3: "Aggressive SEO"**
- seo_investment: Constant → 15000
- content_published: Constant → 30
- backlinks_acquired: Constant → 15

### Step 5: Run and Analyze (30 seconds)

1. Check "Launch forecast"
2. Scroll to **"Investment Scenario Comparison"** section
3. Explore the 4 tabs:
   - 📊 Forecast Comparison (visual comparison)
   - 💰 ROI Analysis (return on investment)
   - 📈 Growth Metrics (growth rates)
   - 📋 Detailed Data (export data)

## Example Results

With the example dataset, you should see:

- **Baseline**: Declining or flat traffic (no investment)
- **Moderate SEO**: 20-30% growth over 12 months
- **Aggressive SEO**: 50-80% growth over 12 months

The ROI tab shows metrics like "Value per $1K Investment" to compare efficiency.

## Tips for Success

✅ **Do:**
- Use historical data with varying investment levels
- Set realistic scenario values based on budget constraints
- Focus on relative comparison between scenarios, not exact numbers
- Use confidence intervals to communicate uncertainty

❌ **Avoid:**
- Setting scenario values far outside your historical range
- Expecting perfect accuracy (it's a projection, not a guarantee)
- Ignoring the confidence intervals
- Using data without investment variation

## Next Steps

- Read the full guide: [SCENARIO_SIMULATION.md](SCENARIO_SIMULATION.md)
- Experiment with different lag configurations
- Try linear growth and step change input types
- Export scenario data for presentations

## Troubleshooting

**Q: Scenarios show similar results?**
- Your historical data may not have enough investment variation
- Try adjusting lag periods
- Ensure regressors are properly selected

**Q: Unrealistic forecasts?**
- Keep scenario values within reasonable bounds
- Check your historical data quality
- Use evaluation to validate model performance

**Q: Need help?**
- Check tooltips in the app (hover over ℹ️ icons)
- Read [SCENARIO_SIMULATION.md](SCENARIO_SIMULATION.md) for detailed examples
- Review the example dataset structure

Happy forecasting! 🚀

