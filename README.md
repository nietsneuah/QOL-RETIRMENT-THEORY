# QOL Retirement Theory Framework

A revolutionary approach to retirement planning that integrates Quality of Life (QOL) decay with age into withdrawal strategies, developed by Doug Hauenstein.

## 🚀 Enhanced Features Now Available!

The QOL Framework has been significantly enhanced with comprehensive risk analysis, depletion timeline tracking, sensitivity analysis, and professional reporting capabilities.

### 🆕 New Enhanced Features

- **📊 Portfolio Depletion Analysis**: Timeline tracking, survival curves, comprehensive risk metrics
- **🔍 Sensitivity Analysis**: Parameter optimization and multi-dimensional risk assessment  
- **📄 Enhanced PDF Reports**: Professional reports with comprehensive visualizations
- **🎯 7 Predefined Scenarios**: Conservative to Aggressive retirement scenarios plus FIRE options
- **💻 Interactive Analysis**: User-friendly interfaces for custom scenario development
- **🔄 Backward Compatibility**: All original functionality preserved and enhanced

## Overview

Traditional retirement planning assumes constant utility from spending throughout retirement. The Hauenstein QOL Framework recognizes that our ability to enjoy life naturally decreases with age, leading to a more optimized withdrawal strategy.

### Key Innovation

**Quality of Life Decay**: As we age, our capacity to enjoy activities diminishes due to:
- Physical limitations
- Health constraints  
- Reduced energy levels
- Cognitive changes

**Mathematical Framework**: QOL(age) = 1 - (age - 65)³ / 50,000

**Result**: 8.5% improvement in lifetime utility compared to traditional 4% rule

## Installation

### Option 1: Conda Environment (Recommended)
```bash
git clone <repository-url>
cd QOL-RETIREMENT-THEORY
conda env create -f environment.yml
conda activate portfolio-sim
```

### Option 2: pip
```bash
git clone <repository-url>
cd QOL-RETIREMENT-THEORY
pip install -r requirements.txt
pip install -e .
```

## Dependencies

### Core Runtime Dependencies
The following packages are required for all functionality:
- **numpy>=1.21.0** - Numerical computing foundation
- **pandas>=1.3.0** - Data manipulation and analysis
- **matplotlib>=3.4.0** - Plotting and visualization
- **scipy>=1.7.0** - Scientific computing (statistics, optimization)
- **seaborn>=0.11.0** - Statistical data visualization

### Development Dependencies
Additional packages for development and interactive use:
- **jupyter>=1.0.0** - Interactive notebook environment
- **notebook>=6.4.0** - Jupyter notebook interface
- **pytest>=6.0** - Testing framework

### Current Conda Environment (`portfolio-sim`)
The conda environment includes additional packages for enhanced functionality:
- **Data Sources**: `yfinance`, `pandas-datareader`, `tiingo` - Financial data APIs
- **PDF Generation**: `reportlab` - Fast matplotlib-based reports
- **LaTeX Reports**: Optional publication-quality reports with superior typography
- **Research Papers**: LaTeX source files for academic documentation
- **Web Scraping**: `beautifulsoup4`, `requests` - Data collection
- **Statistical Analysis**: `statsmodels`, `patsy` - Advanced statistics
- **Performance**: `multitasking` - Concurrent processing
- **Configuration**: `python-dotenv` - Environment variables

> **Note**: The conda environment provides a complete, batteries-included setup with all optional dependencies pre-installed for maximum functionality.

📋 **For complete dependency details, version information, and troubleshooting, see [DEPENDENCIES.md](DEPENDENCIES.md)**

## Quick Start

### Option 3: Python venv
```bash
git clone <repository-url>
cd QOL-RETIREMENT-THEORY
python -m venv qol-env
source qol-env/bin/activate  # On Windows: qol-env\Scripts\activate
pip install -r requirements.txt
pip install -e .
```

## 🖥️ Cross-Platform Compatibility

This framework is designed to work seamlessly across different operating systems and environments:

### ✅ **Supported Platforms**
- **Windows** (Windows 10, 11, Server)
- **macOS** (Intel and Apple Silicon)  
- **Linux** (Ubuntu, CentOS, RHEL, Debian)

### ✅ **Python Environments**
- **Conda/Miniconda** (Recommended)
- **Python venv** (Standard virtual environments)
- **System Python** (3.8+)
- **Docker** (Via container deployment)

### ✅ **Path Resolution Features**
- **Absolute Path Resolution**: Works regardless of current working directory
- **Cross-Platform Separators**: Handles Windows `\` and Unix `/` path separators automatically
- **Normalized Output Paths**: All generated files use OS-appropriate path formats
- **Directory Independence**: Scripts can be run from any directory location

### ✅ **File System Compatibility**
- **Automatic Directory Creation**: Creates output directories on any file system
- **Permission Handling**: Respects OS-specific file permissions
- **Long Path Support**: Handles extended path lengths on Windows
- **Unicode Filenames**: Supports international characters in file paths

## Quick Start

### 🎯 Enhanced Analysis (Recommended)

```bash
# Activate conda environment
conda activate portfolio-sim

# Run all predefined scenarios with comprehensive reporting
python scripts/enhanced_scenario_runner.py --all --pdf

# Interactive custom scenario with enhanced features
python scripts/enhanced_custom_scenario.py

# Parameter sensitivity analysis
python scripts/sensitivity_analysis_runner.py --suite quick
```

### 📊 Original Analysis (Still Available)

```bash
# Run original QOL framework analysis
python src/qol_framework.py

# Original scenario runner
python scripts/scenario_runner.py

# Original custom scenario analysis
python scripts/custom_scenario.py
```

### 🚀 Enhanced Features Overview

The enhanced framework provides:
1. **Portfolio Depletion Analysis**: Track when and how portfolios become exhausted
2. **Risk Assessment**: Comprehensive survival rates and risk metrics
3. **Sensitivity Analysis**: Parameter optimization and risk assessment
4. **Professional PDF Reports**: Stakeholder-ready analysis reports
5. **7 Predefined Scenarios**: From Conservative Retirement to Fat FIRE
6. **Interactive Analysis**: User-guided parameter selection and optimization

## 🏗️ Repository Architecture

This framework is organized using the **Library + Application** pattern for professional software development:

### 📚 `src/` Directory - Core Library
- **What it contains**: The mathematical models, analysis engines, and business logic
- **Purpose**: Reusable modules that can be imported by other Python code
- **When to use**: When you want to integrate QOL analysis into your own Python applications
- **Examples**: `qol_framework.py`, `enhanced_qol_framework.py`, `depletion_analysis.py`

### 🖥️ `scripts/` Directory - User Applications  
- **What it contains**: Ready-to-use programs with command-line interfaces
- **Purpose**: Complete applications that end users can run directly
- **When to use**: When you want to perform analysis without writing Python code
- **Examples**: `enhanced_scenario_runner.py`, `sensitivity_analysis_runner.py`

### 🔄 How They Work Together
```
User runs: python scripts/enhanced_scenario_runner.py --scenario conservative_retirement
     ↓
Script imports: from src.enhanced_qol_framework import EnhancedQOLAnalysis  
     ↓
Core library performs: Mathematical calculations, Monte Carlo simulations
     ↓
Script generates: Professional PDF reports, CSV data, JSON results
```

This separation allows developers to use the core library (`src/`) in their own projects while providing ready-made applications (`scripts/`) for immediate use.

## 📚 Available Analysis Tools

### Enhanced Tools (New)
- **`scripts/enhanced_scenario_runner.py`**: 7 predefined scenarios with comprehensive analysis
- **`scripts/enhanced_custom_scenario.py`**: Interactive custom analysis with full enhancement features  
- **`scripts/sensitivity_analysis_runner.py`**: Parameter optimization and sensitivity analysis
- **Enhanced PDF Reports**: Professional-quality reports with risk analysis

### Original Tools (Maintained)
- **`scripts/scenario_runner.py`**: Multi-scenario batch analysis (now supports `--enhanced` mode)
- **`scripts/custom_scenario.py`**: Interactive custom parameter analysis
- **`src/qol_framework.py`**: Core framework demonstration

### Python API for Custom Parameters
```python
# Enhanced API
from src.enhanced_qol_framework import EnhancedQOLAnalysis

analyzer = EnhancedQOLAnalysis(
    starting_value=750000,
    starting_age=65,
    horizon_years=30
)
results = analyzer.run_enhanced_simulation()

# Original API  
from custom_scenario import run_custom_analysis

# Run analysis with custom parameters
results = run_custom_analysis(
    starting_portfolio=800000,    # $800K portfolio
    starting_age=67,              # Retire at 67  
    retirement_horizon=28,        # 28-year horizon
    simulations=1000              # 1000 Monte Carlo paths
)

# View results
print(f"Utility Improvement: {results['utility_improvement']:.1f}%")
print(f"Success Rate: {results['hauenstein_metrics']['success_rate']:.1%}")
```

📖 **See [SCENARIO_GUIDE.md](SCENARIO_GUIDE.md) for comprehensive usage examples**

## 🎯 Quick Asset Allocation Reference

For immediate guidance on portfolio construction within the QOL framework:

**Most Common Starting Point:**
- **50% Stocks, 30% Bonds, 15% Gold, 5% TIPS** (Enhanced Moderate)
- Suitable for ages 65-75 with moderate risk tolerance

**Adjust Based on Your Situation:**
- **More Conservative**: Reduce stocks to 30-40%, increase bonds
- **More Aggressive**: Increase stocks to 60-70%, reduce bonds
- **High Inflation Concern**: Increase Gold to 20-25%, TIPS to 10-15%
- **Advanced Age (75+)**: Reduce stocks to 20-40%, increase stability assets

📖 **See [Asset Allocation Guide](docs/ASSET_ALLOCATION_GUIDE.md) for complete decision framework**

### 📋 **NEW: Automated PDF Reports**
All analysis tools now automatically generate **consolidated PDF reports**:
```bash
# Multi-scenario analysis with professional PDF report
python scenario_runner.py

# Single scenario with custom parameters + PDF
python generate_single_scenario_pdf.py --portfolio 800000 --age 67 --horizon 28
```

**PDF Features:**
- 📄 Executive summary with key metrics
- 📊 Professional charts and visualizations  
- 📋 Detailed scenario analysis pages
- 📚 Complete methodology documentation

📋 **See [PDF_REPORTING_GUIDE.md](PDF_REPORTING_GUIDE.md) for complete PDF documentation**

## Research Materials

The `research/` directory contains:

- **Academic Paper**: `Hauenstein_QOL_Framework_Anonymized.pdf` - Publication-ready research paper
- **LaTeX Source**: `Hauenstein_QOL_Framework_Anonymized.tex` - Source for academic paper
- **Documentation**: `Hauenstein_QOL_Framework_Anonymized.md` - Detailed framework explanation
- **Asset Allocation Guide**: `Asset_Allocation_Decision_Framework.pdf` - Comprehensive portfolio construction guide
- **Quick Reference**: `Asset_Allocation_Quick_Reference.pdf` - Concise allocation decision card

## Framework Components

### 1. Quality of Life Function
```python
def quality_of_life_factor(age):
    """Calculate QOL decay factor based on age"""
    return max(0.2, 1 - ((age - 65) ** 3) / 50000)
```

### 2. Dynamic Asset Allocation
- **Age 65-75**: 45% Equity / 55% Bonds
- **Age 75-85**: 30% Equity / 70% Bonds  
- **Age 85+**: 20% Equity / 80% Bonds

### 3. Three-Phase Withdrawal Strategy
- **Phase 1 (65-75)**: 5.4% withdrawal rate
- **Phase 2 (75-85)**: 4.5% withdrawal rate
- **Phase 3 (85+)**: 3.5% withdrawal rate

### 4. Asset Allocation Decision Framework
The QOL framework includes comprehensive guidance for structuring portfolios:
- **Individual assessment tools** for risk tolerance and circumstances
- **Decision matrices** for different investor profiles
- **Gold and TIPS integration analysis** for inflation protection
- **Implementation strategies** with practical guidance

📖 **See [Asset Allocation Guide](docs/ASSET_ALLOCATION_GUIDE.md) for comprehensive portfolio construction guidance**

## Key Results

Using a hypothetical $750,000 portfolio:

| Metric | Traditional 4% | QOL Framework | Improvement |
|--------|---------------|---------------|-------------|
| Lifetime Utility | 279.2 | 302.9 | +8.5% |
| Portfolio Survival | 87% | 100% | +15% |
| Total Withdrawals | $787,500 | $967,500 | +23% |

## Academic Impact

This framework challenges fundamental assumptions in the $30+ trillion retirement industry by:

1. **Incorporating aging reality** into financial models
2. **Optimizing for utility** rather than just portfolio longevity
3. **Providing mathematical rigor** to intuitive aging effects
4. **Demonstrating significant improvement** over traditional approaches

## Repository Structure

**Architecture**: Library + Application pattern with clear separation of concerns

```
QOL-RETIREMENT-THEORY/
├── src/                              # Core library modules (importable)
│   ├── __init__.py                   # Package initialization
│   ├── qol_framework.py              # Core framework implementation  
│   ├── enhanced_qol_framework.py     # Enhanced framework with depletion analysis
│   ├── depletion_analysis.py         # Portfolio depletion analysis engine
│   ├── sensitivity_analysis.py       # Parameter sensitivity analysis
│   ├── enhanced_pdf_report.py        # Enhanced PDF report generation
│   └── pdf_report_generator.py       # Original PDF report generator
├── scripts/                          # User applications (executable)
│   ├── enhanced_scenario_runner.py   # 7 predefined scenarios with enhanced analysis
│   ├── sensitivity_analysis_runner.py# Parameter optimization and sensitivity analysis
│   ├── enhanced_custom_scenario.py   # Interactive custom analysis with enhancements
│   ├── scenario_runner.py            # Original multi-scenario runner (enhanced compatible)
│   ├── custom_scenario.py            # Original interactive analysis
│   └── README.md                     # Scripts documentation
├── docs/                             # Documentation
│   ├── ENHANCED_FEATURES_GUIDE.md    # Comprehensive guide to enhanced features
│   ├── PDF_REPORTING_GUIDE.md        # PDF reporting documentation
│   ├── SCENARIO_GUIDE.md             # Scenario analysis guide
│   └── ASSET_ALLOCATION_GUIDE.md     # Asset allocation decision framework
├── examples/                         # Example scripts and demonstrations
│   ├── example.py                    # Basic framework example
│   ├── test_custom_scenarios.py      # Test scenarios
│   ├── generate_single_scenario_pdf.py# Single scenario PDF generation
│   └── README.md                     # Examples documentation
├── research/                         # Academic research materials
│   ├── Hauenstein_QOL_Framework_Anonymized.pdf
│   ├── Hauenstein_QOL_Framework_Anonymized.tex
│   ├── Hauenstein_QOL_Framework_Anonymized.md
│   ├── Asset_Allocation_Decision_Framework.pdf
│   └── Asset_Allocation_Quick_Reference.pdf
├── output/                           # Generated analysis outputs (auto-created)
│   └── README.md                     # Output directory documentation
├── tests/                            # Unit tests
├── data/                             # Input data files
├── results/                          # Legacy results directory
├── requirements.txt                  # Python dependencies (core)
├── environment.yml                   # Conda environment
├── setup.py                          # Package installation
├── DEPENDENCIES.md                   # Complete dependency documentation
└── README.md                         # This file
```

## 🔍 Enhanced Features Deep Dive

### Portfolio Depletion Analysis

The enhanced framework provides comprehensive depletion timeline analysis:

```bash
# Run extreme stress test to see depletion in action
echo '{
  "starting_value": 300000,
  "starting_age": 50,
  "horizon_years": 50,
  "n_simulations": 1000,
  "return_volatility": 0.30,
  "withdrawal_strategy": "fixed_4pct"
}' > stress_test.json

python scripts/enhanced_custom_scenario.py --file stress_test.json
```

**Results include:**
- Depletion rate (% of simulations that exhaust portfolio)
- Survival curves showing portfolio longevity probability  
- Age-specific survival rates (to ages 80, 90, 100)
- Median depletion age for failed scenarios
- 5% worst-case depletion timeline

### Sensitivity Analysis

Optimize your retirement strategy with multi-parameter analysis:

```bash
# Find optimal portfolio size
python scripts/sensitivity_analysis_runner.py --single \
  --scenario conservative_retirement \
  --parameter starting_value \
  --values "400000,500000,600000,750000,900000,1000000"

# Analyze portfolio size vs volatility interaction
python scripts/sensitivity_analysis_runner.py --two-param \
  --scenario moderate_retirement \
  --param1 starting_value --values1 "750000,1000000,1250000" \
  --param2 return_volatility --values2 "0.12,0.15,0.18"
```

### Predefined Scenarios

Seven professionally crafted scenarios covering common retirement patterns:

- **Conservative Retirement**: $750K, age 65, low volatility
- **Moderate Retirement**: $1M, age 65, moderate risk  
- **Aggressive Retirement**: $1.5M, age 60, higher returns
- **Lean FIRE**: $500K, age 55, minimal expenses
- **Fat FIRE**: $2.5M, age 55, luxury lifestyle
- **Early Retirement (Modest)**: $800K, age 60, balanced approach
- **Traditional Retirement**: $1.2M, age 67, standard timeline

### Professional PDF Reports

Enhanced reports include:
- Executive summary with risk assessment
- Portfolio depletion timeline analysis  
- Sensitivity analysis with optimization recommendations
- Comprehensive visualizations and risk matrices
- Stakeholder-ready professional formatting

See the **[Enhanced Features Guide](ENHANCED_FEATURES_GUIDE.md)** for complete documentation.

## Contributing

This is an academic research framework. For contributions or questions:

1. Review the academic paper in `research/`
2. Understand the mathematical foundations
3. Ensure any modifications maintain academic rigor
4. Add appropriate tests for new functionality

## Citation

If you use this framework in academic work, please cite:

```
Hauenstein, D. (2025). "Quality of Life Adjusted Retirement Withdrawal Strategies: 
A Mathematical Framework for Age-Aware Financial Planning." 
```

## License

MIT License - See LICENSE file for details.

## Author

**Doug Hauenstein**
- Creator of the QOL Retirement Framework
- Developer of age-adjusted utility optimization

---

*"The traditional 4% rule assumes you'll enjoy your money equally at 65 and 95. Life doesn't work that way."* - Doug Hauenstein