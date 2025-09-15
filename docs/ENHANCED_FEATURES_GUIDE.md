# Enhanced QOL Framework Features Guide

This guide documents the comprehensive enhancements added to the Hauenstein QOL Framework, including portfolio depletion analysis, sensitivity analysis, and enhanced reporting capabilities.

## 📋 Table of Contents

1. [Overview](#overview)
2. [Enhanced Features](#enhanced-features)  
3. [Core Modules](#core-modules)
4. [Enhanced Scripts](#enhanced-scripts)
5. [Usage Examples](#usage-examples)
6. [Advanced Analysis](#advanced-analysis)
7. [Backward Compatibility](#backward-compatibility)
8. [Output Files](#output-files)

## Overview

The Enhanced QOL Framework extends the original Hauenstein QOL analysis with comprehensive risk assessment, depletion timeline analysis, parameter sensitivity analysis, and professional PDF reporting. These enhancements provide deeper insights into retirement portfolio sustainability and optimization opportunities.

### Key Enhancements

- **Portfolio Depletion Analysis**: Timeline tracking, survival curves, risk metrics
- **Sensitivity Analysis**: Parameter optimization and risk assessment
- **Enhanced PDF Reports**: Professional reporting with comprehensive visualizations
- **Scenario Management**: 7 predefined scenarios plus custom scenario support
- **Interactive Analysis**: User-friendly interfaces for custom analysis
- **Backward Compatibility**: All original functionality preserved

## Enhanced Features

### 🔍 Portfolio Depletion Analysis

The depletion analysis provides detailed insights into when and how portfolios may become exhausted:

- **Depletion Timeline Tracking**: Year-by-year portfolio sustainability assessment
- **Survival Curves**: Probability of portfolio survival over time
- **Risk Metrics**: Comprehensive risk assessment including:
  - Depletion rate (percentage of simulations that deplete)
  - Survival rate (percentage that never deplete)  
  - Median depletion age for portfolios that fail
  - 5% worst-case scenario analysis
  - Age-specific survival probabilities (80, 90, 100)

### 📊 Sensitivity Analysis

Multi-parameter sensitivity analysis identifies optimal portfolio configurations:

- **Single Parameter Analysis**: Test one variable across multiple values
- **Two-Parameter Analysis**: Heatmap analysis of parameter interactions
- **Comprehensive Analysis**: Test multiple parameters simultaneously
- **Optimization Recommendations**: Identify optimal parameter combinations
- **Visual Analysis**: Charts and heatmaps for easy interpretation

### 📄 Enhanced PDF Reporting

Professional-quality PDF reports with comprehensive analysis:

- **Enhanced Executive Summary**: Risk assessment and key metrics
- **Depletion Analysis Pages**: Timeline charts, survival curves, risk tables
- **Sensitivity Analysis Pages**: Parameter optimization results and recommendations
- **Comprehensive Visualizations**: Portfolio paths, allocation strategies, QOL adjustments
- **Risk Assessment Matrix**: Detailed risk categorization and recommendations

## Core Modules

### `src/depletion_analysis.py`

**Purpose**: Portfolio depletion timeline analysis and risk assessment

**Key Classes**:
- `PortfolioDepletionAnalysis`: Main depletion analysis engine

**Key Methods**:
```python
# Analyze depletion patterns across all simulation paths
results = analyzer.analyze_depletion_patterns(portfolio_paths)

# Get risk metrics summary
risk_metrics = analyzer.get_risk_metrics()

# Generate survival curve visualization  
fig = analyzer.plot_survival_curve()
```

### `src/enhanced_qol_framework.py` 

**Purpose**: Enhanced QOL analysis with integrated depletion tracking

**Key Classes**:
- `EnhancedQOLAnalysis`: Enhanced analysis engine combining QOL framework with depletion analysis

**Key Methods**:
```python
# Run enhanced simulation with depletion tracking
enhanced_results = analyzer.run_enhanced_simulation(
    withdrawal_strategy='hauenstein',
    qol_variability=True,
    return_volatility=0.15,
    inflation_variability=True
)

# Get comprehensive analysis including depletion metrics
comprehensive_analysis = analyzer.get_comprehensive_analysis()
```

### `src/sensitivity_analysis.py`

**Purpose**: Multi-parameter sensitivity analysis and optimization

**Key Classes**:
- `QOLSensitivityAnalysis`: Parameter sensitivity and optimization engine

**Key Methods**:
```python
# Single parameter sensitivity sweep
results = analyzer.run_single_parameter_sweep(
    parameter_name='starting_value',
    parameter_values=[500000, 750000, 1000000],
    metric='depletion_rate'
)

# Two parameter heatmap analysis
heatmap_results = analyzer.run_two_parameter_sweep(
    param1_name='starting_value',
    param1_values=[500000, 750000, 1000000],
    param2_name='return_volatility', 
    param2_values=[0.12, 0.15, 0.18],
    metric='depletion_rate'
)
```

### `src/enhanced_pdf_report.py`

**Purpose**: Professional PDF report generation with enhanced features

**Key Functions**:
```python
# Create enhanced PDF report from analysis results
pdf_filename = create_enhanced_pdf_from_results(
    enhanced_results=enhanced_results_list,
    depletion_analyses=depletion_analysis_list,
    sensitivity_results=sensitivity_results_list,
    scenario_infos=scenario_info_list,
    report_title="Enhanced QOL Analysis Report"
)
```

## Enhanced Scripts

### `enhanced_scenario_runner.py`

**Purpose**: Comprehensive scenario analysis with 7 predefined scenarios

**Predefined Scenarios**:
- **Conservative Retirement**: $750K, age 65, 30 years, 12% volatility
- **Moderate Retirement**: $1M, age 65, 30 years, 15% volatility  
- **Aggressive Retirement**: $1.5M, age 60, 35 years, 18% volatility
- **Lean FIRE**: $500K, age 55, 40 years, 15% volatility
- **Fat FIRE**: $2.5M, age 55, 40 years, 16% volatility
- **Early Retirement (Modest)**: $800K, age 60, 35 years, 14% volatility
- **Traditional Retirement**: $1.2M, age 67, 28 years, 13% volatility

**Usage Examples**:
```bash
# List all available scenarios
python enhanced_scenario_runner.py --list

# Run single scenario with PDF report
python enhanced_scenario_runner.py --scenario conservative_retirement --pdf

# Run all scenarios with comprehensive reporting
python enhanced_scenario_runner.py --all --pdf --json

# Run multiple specific scenarios
python enhanced_scenario_runner.py --scenarios "conservative_retirement,moderate_retirement" --pdf
```

### `sensitivity_analysis_runner.py`

**Purpose**: Dedicated sensitivity analysis with predefined parameter ranges

**Analysis Types**:
- **Single Parameter**: Test one parameter across multiple values
- **Two Parameter**: Heatmap analysis of parameter interactions
- **Comprehensive**: Multi-parameter optimization analysis
- **Suite Analysis**: Predefined analysis suites (quick/standard/comprehensive)

**Usage Examples**:
```bash
# List available scenarios and parameter ranges
python sensitivity_analysis_runner.py --list-scenarios
python sensitivity_analysis_runner.py --list-ranges

# Single parameter sensitivity analysis
python sensitivity_analysis_runner.py --single --scenario conservative_retirement \
  --parameter starting_value --values "500000,750000,1000000,1250000,1500000"

# Two parameter heatmap analysis
python sensitivity_analysis_runner.py --two-param --scenario moderate_retirement \
  --param1 starting_value --values1 "750000,1000000,1250000" \
  --param2 return_volatility --values2 "0.12,0.15,0.18"

# Quick analysis suite
python sensitivity_analysis_runner.py --suite quick
```

### `enhanced_custom_scenario.py`

**Purpose**: Interactive custom scenario analysis with full enhancement features

**Features**:
- **Interactive Parameter Input**: Guided parameter selection with validation
- **Enhanced Analysis**: Full depletion and risk analysis
- **Optional Sensitivity Analysis**: Parameter optimization for custom scenarios  
- **Multiple Report Formats**: JSON, CSV, PDF, and visualization outputs
- **File-Based Input**: Support for JSON parameter files

**Usage Examples**:
```bash
# Interactive mode (default)
python enhanced_custom_scenario.py

# Load parameters from JSON file
python enhanced_custom_scenario.py --file my_scenario.json

# Skip sensitivity analysis for faster processing
python enhanced_custom_scenario.py --file my_scenario.json --no-sensitivity

# Quiet mode with no report generation
python enhanced_custom_scenario.py --file my_scenario.json --no-reports --quiet
```

### Updated `scenario_runner.py`

**Purpose**: Original scenario runner with optional enhanced analysis

The original scenario runner now supports enhanced analysis while maintaining full backward compatibility:

**Usage Examples**:
```bash
# Standard analysis (original functionality)
python scenario_runner.py

# Enhanced analysis with depletion tracking
python scenario_runner.py --enhanced
```

## Usage Examples

### Example 1: Quick Scenario Comparison

```bash
# Run all predefined scenarios with comprehensive reporting
conda activate portfolio-sim
python scripts/enhanced_scenario_runner.py --all --pdf --csv
```

This generates:
- Enhanced CSV comparison table
- Professional PDF report with depletion analysis
- Individual scenario visualizations

### Example 2: Custom Scenario with Optimization

```bash
# Create custom scenario JSON file
echo '{
  "starting_value": 800000,
  "starting_age": 62,
  "horizon_years": 35,
  "n_simulations": 1000,
  "return_volatility": 0.16,
  "qol_variability": true,
  "inflation_variability": true,
  "withdrawal_strategy": "hauenstein"
}' > my_scenario.json

# Run enhanced analysis with sensitivity analysis
python scripts/enhanced_custom_scenario.py --file my_scenario.json
```

### Example 3: Parameter Optimization

```bash
# Find optimal portfolio size for conservative retirement
python sensitivity_analysis_runner.py --single \
  --scenario conservative_retirement \
  --parameter starting_value \
  --values "400000,500000,600000,750000,900000,1000000"

# Analyze interaction between portfolio size and volatility
python sensitivity_analysis_runner.py --two-param \
  --scenario moderate_retirement \
  --param1 starting_value \
  --values1 "750000,1000000,1250000,1500000" \
  --param2 return_volatility \
  --values2 "0.10,0.12,0.15,0.18,0.20"
```

## Advanced Analysis

### Stress Testing

Create extreme scenarios to test framework limits:

```json
{
  "starting_value": 300000,
  "starting_age": 50, 
  "horizon_years": 50,
  "n_simulations": 1000,
  "return_volatility": 0.30,
  "withdrawal_strategy": "fixed_4pct"
}
```

### High-Risk Scenarios

Test scenarios that may produce depletion:
- Very long horizons (40-50 years)
- Small starting portfolios (<$500K)
- High volatility (>20%)
- Fixed withdrawal strategies
- Very early retirement (age 50-55)

## Backward Compatibility

All original functionality is preserved:

- **Original Scripts**: `scenario_runner.py`, `custom_scenario.py` work unchanged
- **Original Classes**: `HypotheticalPortfolioQOLAnalysis` unchanged
- **Original Methods**: All existing method signatures preserved
- **Original Outputs**: Standard PDF reports and CSV files still generated

Enhanced features are additive and optional.

## Output Files

### Enhanced Scenario Runner
- `enhanced_scenario_comparison_[timestamp].csv`: Comprehensive scenario comparison
- `enhanced_qol_framework_report_[timestamp].pdf`: Professional PDF report
- Optional JSON exports with detailed results

### Sensitivity Analysis Runner  
- `sensitivity_analysis_[scenario]_[parameter]_[timestamp].pdf`: Analysis report
- `sensitivity_plot_[scenario]_[parameter]_[timestamp].png`: Visualization
- `sensitivity_report_[scenario]_[parameter]_[timestamp].txt`: Text summary
- `sensitivity_suite_[suite]_[timestamp].json`: Comprehensive results

### Enhanced Custom Scenario
- `custom_scenario_report_[timestamp].pdf`: Enhanced PDF report
- `custom_scenario_results_[timestamp].json`: Detailed JSON results
- `custom_scenario_summary_[timestamp].txt`: Text summary
- `custom_scenario_charts_[timestamp].png`: Visualization charts
- Optional sensitivity analysis charts and reports

### Updated Scenario Runner
- **Standard Mode**: Original outputs (CSV, PNG charts, standard PDF)
- **Enhanced Mode**: Enhanced JSON results with depletion analysis

## Best Practices

### Performance Optimization
- Use 500-1000 simulations for development/testing
- Use 5000+ simulations for production analysis
- Enable quiet mode for batch processing
- Use predefined scenarios for consistent comparisons

### Risk Analysis
- Always test extreme scenarios alongside normal cases
- Pay attention to depletion rates above 10%
- Consider longevity risk (survival to age 90+)
- Validate results with sensitivity analysis

### Report Generation
- Generate PDF reports for stakeholder communication
- Use CSV exports for further analysis in Excel/Python
- Save JSON results for programmatic processing
- Keep visualization files for presentations

## Troubleshooting

### Common Issues
- **ImportError**: Ensure conda environment `portfolio-sim` is activated
- **PDF Generation Fails**: Check matplotlib backend and font availability
- **Memory Issues**: Reduce number of simulations for large parameter sweeps
- **Slow Performance**: Use `--quiet` mode and reduce simulation count

### Environment Setup
```bash
# Activate the correct environment
conda activate portfolio-sim

# Verify key packages are installed
python -c "import numpy, pandas, matplotlib, scipy; print('All packages available')"

# Test enhanced features availability
python -c "from src.enhanced_qol_framework import EnhancedQOLAnalysis; print('Enhanced features available')"
```

---

*This guide covers the comprehensive enhancements to the Hauenstein QOL Framework. For questions or issues, refer to the individual module documentation or the main README.*