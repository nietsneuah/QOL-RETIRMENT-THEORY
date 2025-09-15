# Complete Dependency Information

## Overview
This document provides comprehensive information about all dependencies in the QOL Retirement Theory project, including what's installed in the conda environment and why each package is needed.

## Core Dependencies (Always Required)

### Computational Foundation
- **numpy>=1.21.0** - Fundamental numerical computing, array operations, mathematical functions
- **scipy>=1.7.0** - Scientific computing library for statistics, optimization, and advanced math
- **pandas>=1.3.0** - Data manipulation, analysis, and time series handling

### Visualization
- **matplotlib>=3.4.0** - Core plotting library for charts, graphs, and visualizations
- **seaborn>=0.11.0** - Statistical visualization, heatmaps, and enhanced plotting aesthetics

## Development Dependencies

### Interactive Development
- **jupyter>=1.0.0** - Interactive computing environment for notebooks
- **notebook>=6.4.0** - Web-based notebook interface for development and analysis

### Testing
- **pytest>=6.0** - Testing framework for unit tests and validation

## Current Conda Environment (`portfolio-sim`) - Complete Package List

### Core Scientific Computing
- **numpy=2.3.2** - Advanced numerical arrays and mathematical functions
- **scipy=1.16.1** - Scientific computing (stats, optimization, linear algebra)
- **pandas=2.3.2** - Data structures and analysis tools
- **matplotlib=3.10.6** - Plotting and visualization
- **seaborn=0.13.2** - Statistical data visualization

### Financial Data Sources
- **yfinance=0.2.57** - Yahoo Finance API for market data
- **pandas-datareader=0.10.0** - Financial data readers from multiple sources
- **tiingo=0.16.1** - Professional financial data API

### Statistical Analysis
- **statsmodels=0.14.5** - Statistical modeling and econometrics
- **patsy=1.0.1** - Statistical model formula language

### PDF and Reporting
- **reportlab=4.4.3** - Professional PDF generation for analysis reports
- **pillow=11.3.0** - Image processing for charts in PDFs
- **LaTeX (optional)** - For compiling research papers (requires separate installation)

### Web and Data Collection
- **requests=2.32.5** - HTTP library for API calls
- **beautifulsoup4=4.13.5** - HTML/XML parsing and web scraping
- **lxml=6.0.1** - Fast XML/HTML parsing

### Development Tools
- **pytest=8.4.2** - Testing framework
- **python-dotenv=1.1.1** - Environment variable management

### Performance and Concurrency
- **multitasking=0.0.12** - Concurrent processing for data downloads

### System and Utility
- **setuptools=80.9.0** - Package installation and distribution
- **pip=25.2** - Python package installer
- **wheel=0.45.1** - Built-package format for Python

### Graphics and UI Libraries
- **cairo=1.18.4**, **pycairo=1.28.0** - 2D graphics library
- **fonttools=4.59.2** - Font utilities for PDF generation
- **freetype=2.13.3** - Font rendering

### LaTeX Graphics Support
- **matplotlib>=3.4.0** - Chart generation for LaTeX reports (PNG output at 300 DPI)
- **pillow>=11.0.0** - Image processing and format conversion for LaTeX embedding
- **LaTeX graphicx package** - Included in BasicTeX/MacTeX for image inclusion

## Installation Methods

### Method 1: Conda (Recommended)
```bash
conda env create -f environment.yml
conda activate portfolio-sim
```
**Advantages:**
- Complete environment with all optional packages
- Optimized binary packages for performance
- Automatic dependency resolution
- Includes system libraries (Cairo, FontConfig, etc.)
- **Runs all simulations regardless of LaTeX availability**

### Method 2: pip
```bash
pip install -r requirements.txt
pip install -e .
```
**Advantages:**
- Minimal installation with core dependencies only
- Faster installation
- Compatible with any Python environment

### Method 3: Development Installation
```bash
pip install -e .[dev,test]
```
**Includes:**
- Core dependencies
- Development tools (jupyter, notebook)
- Testing framework (pytest)

## Report Generation Options

The QOL Framework supports multiple report formats - all simulations work regardless of which options are available:

### Standard PDF Report Generation (Always Available)
- **Required**: `reportlab`, `pillow`, `matplotlib` (included in all installation methods)
- **Purpose**: Generate professional portfolio analysis reports
- **Features**: Charts, tables, analysis summaries in PDF format
- **Command**: All standard simulation scripts generate these automatically

### Optional Features and Their Dependencies

### LaTeX PDF Report Generation (Enhanced, Optional)
- **Required**: LaTeX distribution + `matplotlib`, `seaborn`, `pillow`
- **Purpose**: Publication-quality reports with superior typography
- **Features**: Mathematical equations, professional formatting, embedded high-res graphics
- **Command**: `python examples/generate_latex_report_example.py --generate-sample`
- **Fallback**: If LaTeX unavailable, simulations still run with standard PDF reports

### Research Paper Generation (LaTeX)
- **Required**: LaTeX distribution (TeXLive, MiKTeX, or MacTeX)
- **Purpose**: Compile research documents from .tex source files
- **Location**: `research/Hauenstein_QOL_Framework_Anonymized.tex`
- **Note**: Separate installation required, not included in Python environment

### Professional LaTeX Report Generation (Optional)
- **Required**: LaTeX distribution (TeXLive, MiKTeX, or MacTeX) 
- **Python Dependencies**: `matplotlib`, `seaborn`, `pillow` (for chart generation and image processing)
- **Purpose**: Generate publication-quality PDF reports with superior typography
- **Python Module**: `src/latex_report_generator.py`
- **Features**: Mathematical equations, professional tables, enhanced formatting, embedded charts/graphics
- **Graphics Support**: Automatically includes portfolio charts, survival curves, sensitivity heatmaps
- **Fallback**: All simulations work with standard matplotlib/reportlab reports if LaTeX unavailable
- **Note**: Completely optional - simulations run normally without LaTeX installation

### Financial Data Integration
- **Required**: `yfinance`, `pandas-datareader`, `tiingo`
- **Purpose**: Download real market data for analysis

### Advanced Statistical Analysis
- **Required**: `statsmodels`, `patsy`
- **Purpose**: Sophisticated statistical modeling beyond basic scipy

### Web Data Collection
- **Required**: `requests`, `beautifulsoup4`, `lxml`
- **Purpose**: Scrape financial data from web sources

## Version Compatibility

### Python Versions
- **Minimum**: Python 3.9
- **Recommended**: Python 3.11+ (used in conda environment)
- **Tested**: Python 3.11.13

### Platform Support
- **macOS**: Full support (tested on ARM64)
- **Windows**: Full support via conda
- **Linux**: Full support via conda or pip

## Troubleshooting Dependencies

### Common Issues
1. **Seaborn Import Error**: Ensure `seaborn>=0.11.0` is installed
2. **PDF Generation Fails**: Install `reportlab` and system fonts
3. **Financial Data Errors**: Check internet connection and API limits
4. **Font Rendering Issues**: Install system font packages

## LaTeX Installation (Optional)

For compiling research papers, you'll need a LaTeX distribution:

### macOS
```bash
# Install MacTeX (full distribution)
brew install --cask mactex

# Or install BasicTeX (minimal)
brew install --cask basictex
```

### Windows
- Download and install MiKTeX from https://miktex.org/
- Or install TeX Live from https://www.tug.org/texlive/

### Linux
```bash
# Ubuntu/Debian
sudo apt-get install texlive-full

# CentOS/RHEL/Fedora
sudo dnf install texlive-scheme-full
```

### Compile Research Paper
```bash
cd research/
pdflatex Hauenstein_QOL_Framework_Anonymized.tex
```

### Generate LaTeX-based Analysis Reports
```bash
# Check LaTeX availability
python -c "from src.latex_report_generator import check_latex_availability; print(check_latex_availability())"

# Generate sample LaTeX report with graphics
python examples/generate_latex_report_example.py --generate-sample

# Generate LaTeX report from existing analysis results
python -c "from src.latex_report_generator import create_latex_pdf_from_results; # use with your analysis results"
```

**Note**: LaTeX reports automatically include:
- Portfolio performance summary charts (PNG format, 300 DPI)
- Multi-scenario comparison visualizations
- Depletion risk analysis charts
- Success rate comparisons across scenarios
- All graphics are embedded directly in the PDF for publication-quality output
- Graphics are generated dynamically from analysis results

## Running Simulations (With or Without LaTeX)

### Standard Simulation Commands (Always Work)
```bash
# Run predefined scenarios - generates standard PDF reports
python enhanced_scenario_runner.py --list
python enhanced_scenario_runner.py --scenario conservative

# Run custom scenarios - generates standard PDF reports  
python enhanced_custom_scenario.py

# Original QOL analysis - generates matplotlib-based reports
python scenario_runner.py
```

### LaTeX-Enhanced Reports (Optional)
```bash
# Check if LaTeX is available
python examples/generate_latex_report_example.py --check-latex

# Generate LaTeX report (only if LaTeX installed)
python examples/generate_latex_report_example.py --generate-sample

# If LaTeX not available, get installation instructions
python examples/generate_latex_report_example.py --install-guide
```

### Verification Commands
```bash
# Check Python environment
conda list | grep -E "(numpy|pandas|matplotlib|scipy|seaborn)"

# Test core imports (required for all simulations)
python -c "import numpy, pandas, matplotlib.pyplot, scipy, seaborn; print('All core packages imported successfully')"

# Test optional imports
python -c "import yfinance, reportlab; print('Optional packages available')"

# Test LaTeX availability (optional)
pdflatex --version 2>/dev/null && echo "LaTeX available for enhanced reports" || echo "LaTeX not available - simulations still work with standard reports"
```

**Key Point**: All QOL Framework simulations and analyses work perfectly without LaTeX. LaTeX only enhances the report quality when available.

### What Works Without LaTeX:
✅ All simulation scenarios and analysis  
✅ Portfolio depletion risk assessment  
✅ Sensitivity analysis and optimization  
✅ Professional PDF reports with charts  
✅ Interactive scenario builders  
✅ Risk metrics and longevity analysis  
✅ Complete functionality of the framework  

### What LaTeX Adds (Optional):  
🎯 Superior typography and formatting  
🎯 Publication-quality mathematical equations  
🎯 Enhanced table layouts  
🎯 Professional academic/business presentation  

**Bottom Line**: Install LaTeX only if you want enhanced report aesthetics. All core functionality works without it.