# Quick Start: SEO Scenario Forecasting

## 🚀 Getting Started in 5 Minutes

### Step 1: Launch the App
```bash
streamlit_prophet deploy dashboard
```

### Step 2: Load Your Data
- Upload your traffic CSV (date + traffic columns)
- Or select a toy dataset to explore

### Step 3: Configure Basic Forecast
1. **Data**: Select date and target columns
2. **Modelling**: Keep defaults or tune parameters
3. **Evaluation**: Optional - enable to validate model
4. **Forecast**: ✅ Enable "Make forecast on future dates"
   - Set horizon (e.g., 6 months)

### Step 4: Enable Scenarios
In sidebar section **5. Scenarios**:
- ✅ Check "Add scenario analysis"
- Expand "Scenario Configuration"

### Step 5: Create Your First Scenario

#### Quick Example: Simple 25% Increase
1. **Mode**: Select "Simple Percentage"
2. **Number of scenarios**: 1
3. **Scenario name**: "Optimistic Growth"
4. **Target Traffic Increase**: 25%
5. **Delay**: 2 months
6. **Ramp-up Duration**: 6 months

#### Advanced Example: Content Strategy
1. **Mode**: Select "Numeric (Budget/Content/Backlinks)"
2. **Number of scenarios**: 2

**Scenario 1: "Content-First"**
- Budget: $0
- Content: 20 articles/month
- Backlinks: 10/month

**Scenario 2: "Balanced Mix"**
- Budget: $5000
- Content: 10 articles/month
- Backlinks: 20/month

### Step 6: Launch Forecast
Click **"Launch forecast"** at the top of the sidebar

### Step 7: Review Results
Scroll down to the **Scenario Analysis** section to see:
- 📊 Comparison chart with all scenarios
- 📈 Summary table with traffic differences
- 📝 Detailed scenario configurations

### Step 8: Save Your Work
Click **"Save experiment"** to download:
- All charts as images
- Forecast data as CSV
- Scenario configurations

## 💡 Quick Tips

### For Realistic Forecasts:
- **Budget coefficient**: 30-70 per $1000 (depends on industry)
- **Content coefficient**: 50-150 per article (depends on quality)
- **Backlink coefficient**: 5-20 per backlink (depends on quality)
- **Delay**: 1-4 months (typical SEO lag)
- **Acceleration**: 4-8 months (time to full impact)

### Common Scenarios:

**Startup SEO (Bootstrap Budget)**
- Budget: $2000/month
- Content: 15 articles/month
- Backlinks: 8/month
- Delay: 3 months
- Acceleration: 8 months

**Enterprise SEO (Aggressive)**
- Budget: $20000/month
- Content: 30 articles/month
- Backlinks: 40/month
- Delay: 2 months
- Acceleration: 6 months

**Content-Only Strategy**
- Budget: $0
- Content: 25 articles/month
- Backlinks: 0
- Delay: 2 months
- Acceleration: 7 months

## 🎯 What You'll See

### The Scenario Comparison Chart
- **Solid blue line**: Baseline forecast (no changes)
- **Dashed colored lines**: Your scenarios
- **Blue shaded area**: Confidence interval for baseline
- **Interactive**: Hover for details, use range selector to zoom

### The Summary Table
| Scenario | Total Traffic | Difference vs Baseline | % Change |
|----------|--------------|------------------------|----------|
| Baseline | 450,000 | 0 | 0.0% |
| Content-First | 520,000 | +70,000 | +15.6% |
| Balanced Mix | 575,000 | +125,000 | +27.8% |

### Scenario Details
Expandable sections showing:
- All input parameters
- Impact coefficients used
- Timing configuration
- Expected peak effects

## 🔍 Interpreting Results

### Understanding the Growth Curve
```
Traffic
   ↑
   |                           ___---~~~  (Plateau: slow growth)
   |                     ___---
   |                ___--               (S-curve: acceleration)
   |         ___---
   |    ____                            (Delay: no effect)
   |----
   |_________________________________→ Time
   0m      2m         5m         8m
```

### When to Adjust Coefficients
- **Too optimistic?** Reduce coefficients by 20-30%
- **Too conservative?** Increase coefficients by 20-30%
- **Historical data available?** Calculate from past campaigns:
  - Added 10 articles last quarter → gained 800 visitors
  - Coefficient = 800 / 10 / 90 days ≈ 0.89 per article per day
  - Scale to monthly: 0.89 × 30 ≈ 27 per article

## 🐛 Troubleshooting

**"Scenario analysis requires 'Make forecast on future dates'"**
→ Go to section 4, enable future forecasting

**Scenarios look identical to baseline**
→ Check your coefficients aren't set to 0
→ Verify delay isn't longer than forecast horizon

**Chart is too crowded**
→ Reduce number of scenarios to 2-3
→ Use the range selector to focus on forecast period

**Results seem unrealistic**
→ Review and adjust impact coefficients
→ Consider more conservative delay/acceleration periods
→ Compare with industry benchmarks

## 📚 Learn More

- **Full Documentation**: See [SCENARIOS.md](SCENARIOS.md)
- **Technical Details**: See [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)
- **Prophet Documentation**: https://facebook.github.io/prophet/

## 🎓 Example Workflow

```
1. Load historical traffic data (12 months)
   → See baseline: 1000 visitors/day

2. Forecast 6 months ahead
   → Baseline projects: 1050 visitors/day

3. Create scenario: "New Content Strategy"
   → 15 articles/month, 100 traffic/article
   → 2 month delay, 6 month acceleration
   
4. View results:
   → Month 1-2: Same as baseline (delay)
   → Month 3-6: Growing above baseline (acceleration)
   → Month 6: 1050 + 1500 = 2550 visitors/day
   
5. Export and present to stakeholders
   → "If we publish 15 articles/month, we expect
      +140% traffic increase within 6 months"
```

## ✅ You're Ready!

You now know how to:
- ✅ Enable and configure scenario analysis
- ✅ Create numeric and percentage scenarios
- ✅ Interpret the comparison charts
- ✅ Adjust parameters for realistic forecasts
- ✅ Export and share your results

**Happy forecasting! 🚀**

