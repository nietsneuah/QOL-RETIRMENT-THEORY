# Analysis Scripts

This directory contains the **user-facing applications** for the QOL Framework.

## 🏗️ Why Scripts Are Separate from Core Code

This directory follows the **Application Layer** architectural pattern:

### 📂 **What's in `/scripts/`**
- **Ready-to-run programs** with command-line interfaces
- **User workflows** that combine multiple analysis steps
- **File I/O handling** for reports, CSVs, and JSON output
- **Interactive prompts** for parameter selection

### 📂 **What's in `/src/`** (Core Library)
- **Mathematical models** and calculations  
- **Business logic** for QOL analysis
- **Reusable components** that scripts import
- **Core algorithms** without user interface

### 🔄 **The Relationship**
Scripts in this directory **import and use** the core modules from `/src/`:
```python
# Scripts import from src to use the core functionality
from src.enhanced_qol_framework import EnhancedQOLAnalysis
from src.sensitivity_analysis import QOLSensitivityAnalysis
```

This separation means:
- **Users** run scripts for analysis
- **Developers** modify core logic in `/src/`  
- **Integration** is possible by importing `/src/` modules into custom projects

## Enhanced Analysis Scripts (Recommended)

### `enhanced_scenario_runner.py`
Comprehensive scenario analysis with 7 predefined scenarios and enhanced risk assessment.

**Key Features:**
- 7 predefined scenarios (Conservative Retirement to Fat FIRE)
- Portfolio depletion analysis
- Professional PDF reports
- CSV comparison tables

**Usage:**
```bash
# List available scenarios
python scripts/enhanced_scenario_runner.py --list

# Run single scenario with PDF
python scripts/enhanced_scenario_runner.py --scenario conservative_retirement --pdf

# Run all scenarios with comprehensive reporting
python scripts/enhanced_scenario_runner.py --all --pdf --csv
```

### `sensitivity_analysis_runner.py`
Parameter optimization and sensitivity analysis.

**Key Features:**
- Single and multi-parameter sensitivity analysis
- Parameter optimization recommendations
- Professional reporting with visualizations

**Usage:**
```bash
# Single parameter analysis
python scripts/sensitivity_analysis_runner.py --single --scenario conservative_retirement --parameter starting_value --values "500000,750000,1000000"

# Quick analysis suite
python scripts/sensitivity_analysis_runner.py --suite quick
```

### `enhanced_custom_scenario.py`
Interactive custom scenario analysis with full enhancement features.

**Key Features:**
- Interactive parameter input with validation
- Optional sensitivity analysis
- Multiple output formats (PDF, JSON, CSV, PNG)

**Usage:**
```bash
# Interactive mode
python scripts/enhanced_custom_scenario.py

# Load from JSON file
python scripts/enhanced_custom_scenario.py --file my_scenario.json
```

## Original Analysis Scripts (Maintained for Compatibility)

### `scenario_runner.py`
Multi-scenario batch analysis with optional enhanced mode.

**Usage:**
```bash
# Standard analysis
python scripts/scenario_runner.py

# Enhanced analysis with depletion tracking
python scripts/scenario_runner.py --enhanced
```

### `custom_scenario.py`
Original interactive custom parameter analysis.

**Usage:**
```bash
# Interactive custom analysis
python scripts/custom_scenario.py
```

## Environment Setup

All scripts require the conda environment:

```bash
conda activate portfolio-sim
```

## Output

All scripts generate output files in the `output/` directory. See `output/README.md` for details on file types and structure.