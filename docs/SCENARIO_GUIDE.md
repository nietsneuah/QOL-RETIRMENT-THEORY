# QOL Framework Scenario Analysis Guide

## 🎯 **Best Ways to Run Simulations with Various Inputs**

The QOL Framework now supports flexible scenario analysis with different starting values, ages, retirement ages, and time horizons. Here are the **3 best approaches**:

---

## **Method 1: Interactive Custom Analysis** ⭐ *Recommended for Single Scenarios*

### **Quick Start:**
```bash
python custom_scenario.py
```

**Choose option 1 for interactive mode:**
- Enter starting portfolio value 
- Enter retirement age
- Enter analysis horizon (years)
- Optionally specify number of simulations

### **Direct Function Call:**
```python
from custom_scenario import run_custom_analysis

results = run_custom_analysis(
    starting_portfolio=800000,    # $800K starting value
    starting_age=67,              # Retire at 67
    retirement_horizon=28,        # Analyze 28 years
    simulations=1000              # 1000 Monte Carlo paths
)
```

### **Example Results:**
```
🏆 QOL Framework Results:
   Success Rate: 100.0%
   Median Final Value: $605,320
   Mean Utility Score: 280,107
   
🚀 QOL Framework Improvement: +12.2% utility enhancement
```

---

## **Method 2: Batch Scenario Comparison** ⭐ *Recommended for Multiple Scenarios*

### **Quick Start:**
```bash
python scenario_runner.py
```

This will run 4 preset scenarios and generate:
- 📄 **scenario_comparison.csv** - Detailed comparison table
- 📊 **Multiple charts** comparing utility, success rates, final values
- 💾 **JSON results file** with full simulation data

### **Custom Batch Analysis:**
```python
from scenario_runner import QOLScenarioRunner

runner = QOLScenarioRunner()

# Add your scenarios
runner.create_scenario("Conservative", 500000, 65, 30)
runner.create_scenario("Aggressive", 1000000, 60, 35) 
runner.create_scenario("Late_Start", 600000, 70, 25)

# Run all and compare
results = runner.run_all_scenarios()
runner.create_comparison_report('my_analysis.csv')
runner.create_visualization('utility_improvement')
```

---

## **Method 3: Preset Scenario Testing** ⭐ *Recommended for Quick Validation*

### **Quick Start:**
```bash
python test_custom_scenarios.py
```

### **Available Preset Scenarios:**
1. **Conservative**: $500K, age 65, 25 years
2. **Aggressive**: $1M, age 60, 35 years  
3. **Late Retirement**: $600K, age 70, 20 years

---

## **📊 Parameter Ranges & Guidelines**

### **Starting Portfolio Value**
- **Typical Range**: $300K - $2M
- **Sweet Spot**: $500K - $1.5M for realistic scenarios
- **Format**: Enter as number (e.g., 750000 for $750K)

### **Starting Age**
- **Typical Range**: 55-75 years old
- **Early Retirement**: 55-62
- **Standard**: 62-67
- **Late Retirement**: 67-75

### **Retirement Horizon**
- **Typical Range**: 20-40 years
- **Conservative**: 20-25 years
- **Standard**: 25-35 years
- **Extended**: 35-40 years

### **Simulations**
- **Quick Testing**: 100-500 simulations
- **Standard Analysis**: 1000 simulations
- **High Precision**: 2000+ simulations

---

## **🎯 Sample Scenarios to Try**

### **Early Retirement Scenarios:**
```python
# FIRE (Financial Independence, Retire Early)
run_custom_analysis(1200000, 55, 40, 1000)

# Moderate Early Retirement  
run_custom_analysis(800000, 60, 35, 1000)
```

### **Standard Retirement Scenarios:**
```python
# Traditional 65 Retirement
run_custom_analysis(750000, 65, 30, 1000)

# Delayed Social Security
run_custom_analysis(600000, 67, 28, 1000)
```

### **Late/Catch-up Scenarios:**
```python
# Late Start, High Savings
run_custom_analysis(500000, 70, 25, 1000)

# Modest Late Retirement
run_custom_analysis(400000, 72, 20, 1000)
```

### **High Net Worth Scenarios:**
```python
# Affluent Early Retirement
run_custom_analysis(2000000, 58, 37, 1000)

# Executive Retirement
run_custom_analysis(1500000, 62, 33, 1000)
```

---

## **📈 Understanding the Results**

### **Key Metrics Explained:**

**Success Rate**: Percentage of simulations where portfolio lasted the full horizon
- **100%**: Portfolio never depleted
- **90-99%**: Very safe
- **80-89%**: Moderately safe
- **<80%**: Consider adjustments

**Utility Improvement**: How much better the QOL Framework performs vs 4% rule
- **+15%+**: Excellent improvement
- **+10-15%**: Very good improvement  
- **+5-10%**: Good improvement
- **<+5%**: Marginal benefit

**Median Final Value**: Middle value of portfolio at end of horizon
- Higher values indicate more wealth preservation
- Compare to starting value for wealth growth/decline

### **QOL Framework Advantages Show Best In:**
- ✅ **Longer horizons** (30+ years): More time for phases to matter
- ✅ **Higher starting ages** (65+): QOL decay becomes significant
- ✅ **Moderate portfolios** ($500K-$1.5M): Sweet spot for strategy
- ✅ **Standard retirement** timing: Framework designed for 60-75 start

---

## **🔧 Advanced Usage**

### **Modify Market Assumptions:**
The framework uses these default assumptions:
- **Equity Return**: 7% annually
- **Bond Return**: 4% annually  
- **Equity Volatility**: 20%
- **Bond Volatility**: 5%
- **Correlation**: 0.1
- **Inflation**: 3%

To modify these, edit the `CustomQOLAnalysis` class in `custom_scenario.py`.

### **Change QOL Decay Function:**
The current QOL function decreases utility with age. To modify:
```python
# In _define_qol_function method
def qol_factor(age):
    # Your custom quality of life decay
    return custom_formula(age)
```

### **Adjust Withdrawal Phases:**
Current phases:
- **65-74**: 5.4% withdrawal rate
- **75-84**: 4.5% withdrawal rate  
- **85+**: 3.5% withdrawal rate

Modify in `hauenstein_qol_strategy()` method.

---

## **📁 Generated Output Files**

### **From scenario_runner.py:**
- `scenario_comparison.csv` - Detailed comparison table
- `utility_improvement_comparison.png` - Utility improvement chart
- `success_rate_comparison.png` - Success rate comparison  
- `final_value_comparison.png` - Final portfolio value comparison
- `qol_scenario_results_[timestamp].json` - Complete raw results

### **From Main Analysis:**
- `hauenstein_qol_anonymized_analysis.png` - Framework visualization
- Individual scenario outputs in terminal

---

## **⚡ Quick Reference Commands**

```bash
# Interactive single scenario
python custom_scenario.py

# Batch scenario runner
python scenario_runner.py

# Test preset scenarios  
python test_custom_scenarios.py

# Original framework (fixed parameters)
python src/qol_framework.py
python example.py
```

---

## **🎯 Best Practices**

1. **Start with presets** to understand the framework
2. **Use 1000+ simulations** for final analysis
3. **Compare multiple scenarios** to find optimal parameters
4. **Consider longer horizons** for early retirement
5. **Validate with conservative assumptions** first
6. **Save results** for future reference

The QOL Framework consistently shows **8-17% utility improvements** across scenarios while maintaining high portfolio success rates!