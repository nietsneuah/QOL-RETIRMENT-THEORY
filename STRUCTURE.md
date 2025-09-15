# Repository Structure

This document provides an overview of the professionally organized QOL Framework repository structure.

## 📁 Directory Organization

```
QOL-RETIREMENT-THEORY/
├── 📂 src/                           # Core framework modules
│   ├── qol_framework.py              # Original Hauenstein QOL Framework
│   ├── enhanced_qol_framework.py     # Enhanced framework with depletion analysis
│   ├── depletion_analysis.py         # Portfolio depletion analysis engine
│   ├── sensitivity_analysis.py       # Parameter sensitivity and optimization
│   ├── enhanced_pdf_report.py        # Enhanced professional PDF generation
│   └── pdf_report_generator.py       # Original PDF report generator
│
├── 📂 scripts/                       # Main analysis and execution scripts
│   ├── enhanced_scenario_runner.py   # 7 predefined scenarios with enhanced analysis
│   ├── sensitivity_analysis_runner.py# Parameter optimization and sensitivity analysis
│   ├── enhanced_custom_scenario.py   # Interactive custom analysis with enhancements
│   ├── scenario_runner.py            # Original multi-scenario runner (enhanced compatible)
│   ├── custom_scenario.py            # Original interactive analysis
│   └── README.md                     # Script documentation and usage guide
│
├── 📂 docs/                          # Documentation and guides
│   ├── ENHANCED_FEATURES_GUIDE.md    # Comprehensive guide to enhanced features
│   ├── PDF_REPORTING_GUIDE.md        # PDF reporting documentation
│   └── SCENARIO_GUIDE.md             # Scenario analysis guide
│
├── 📂 examples/                      # Example scripts and demonstrations
│   ├── example.py                    # Basic framework demonstration
│   ├── test_custom_scenarios.py      # Test scenario examples
│   ├── generate_single_scenario_pdf.py# Single scenario PDF generation example
│   └── README.md                     # Examples documentation
│
├── 📂 research/                      # Academic research materials (preserved)
│   ├── Hauenstein_QOL_Framework_Anonymized.pdf
│   ├── Hauenstein_QOL_Framework_Anonymized.tex
│   └── Hauenstein_QOL_Framework_Anonymized.md
│
├── 📂 output/                        # Generated analysis outputs (auto-organized)
│   ├── 📂 data/                      # CSV and JSON data files
│   ├── 📂 reports/                   # PDF reports and text summaries
│   ├── 📂 charts/                    # PNG, JPG, SVG visualization files
│   └── README.md                     # Output directory documentation
│
├── 📂 tests/                         # Unit tests and testing framework
│   ├── test_framework.py             # Framework unit tests
│   └── README.md                     # Testing documentation
│
├── 📂 data/                          # Input data files (if needed)
├── 📂 results/                       # Legacy results directory
│
└── 📄 Configuration & Setup Files
    ├── README.md                     # Main repository documentation
    ├── requirements.txt              # Python package dependencies
    ├── environment.yml               # Conda environment specification
    ├── setup.py                      # Package installation configuration
    ├── LICENSE                       # Repository license
    ├── .gitignore                    # Git ignore rules
    └── SETUP_COMPLETE.md             # Setup completion guide
```

## 🎯 Quick Start Workflow

### 1. Environment Setup
```bash
conda activate portfolio-sim
```

### 2. Enhanced Analysis (Recommended)
```bash
# Run comprehensive analysis with all scenarios
python scripts/enhanced_scenario_runner.py --all --pdf

# Single scenario with organized outputs
python scripts/enhanced_scenario_runner.py --scenario conservative_retirement --csv --json --pdf

# Interactive custom scenario analysis
python scripts/enhanced_custom_scenario.py

# Parameter optimization
python scripts/sensitivity_analysis_runner.py --suite quick
```

### 3. Original Analysis (Compatible)
```bash
# Original framework demonstration
python src/qol_framework.py

# Basic example
python examples/example.py
```

## 📊 Output Organization

All generated files are automatically organized in the `output/` directory by file type:

### 📊 `output/data/`
- **CSV Files**: Scenario comparison tables, summary statistics
- **JSON Files**: Detailed simulation results, configuration exports

### 📋 `output/reports/`  
- **PDF Reports**: Comprehensive analysis reports with charts and tables
- **TXT Files**: Text-based summaries and analysis reports

### 📈 `output/charts/`
- **PNG Files**: Charts, plots, and visualization images
- **SVG Files**: Vector graphics and scalable visualizations
- **JPG Files**: Compressed images and charts

### Auto-Organization
Files are automatically placed in the correct subdirectory based on extension:
- `.csv`, `.json` → `data/`
- `.pdf`, `.txt` → `reports/` 
- `.png`, `.jpg`, `.jpeg`, `.svg` → `charts/`

## 🏗️ Architectural Design: Why `src/` and `scripts/` Are Separated

This repository follows the **Library + Application** architectural pattern for clear separation of concerns:

### 📚 `src/` - Core Library Modules (The "What")
**Purpose**: Contains the **core business logic** and **reusable components**
- **Mathematical Models**: QOL decay functions, Monte Carlo simulations
- **Analysis Engines**: Depletion analysis, sensitivity analysis  
- **Report Generation**: Professional PDF creation with visualizations
- **Role**: These are **importable modules** that provide functionality
- **Usage**: Other files import these (`from src.qol_framework import ...`)
- **Analogy**: Like a toolbox - contains all the tools but doesn't use them directly

### 🖥️ `scripts/` - User Applications (The "How")  
**Purpose**: Contains **executable applications** that users interact with directly
- **Scenario Analysis**: Predefined and custom scenario runners
- **Parameter Optimization**: Sensitivity analysis and optimization tools
- **Interactive Tools**: User-guided analysis with input validation
- **Role**: These are **runnable programs** with command-line interfaces
- **Usage**: Users execute these (`python scripts/enhanced_scenario_runner.py`)
- **Analogy**: Like specific projects - use the tools from the toolbox to accomplish tasks

### 🔄 The Relationship
```
┌─────────────────┐    imports    ┌──────────────────────────┐
│   scripts/      │ ────────────► │        src/              │
│                 │               │                          │
│ • User Programs │               │ • Core Libraries         │
│ • CLI Interface │               │ • Business Logic         │  
│ • Workflows     │               │ • Mathematical Models    │
└─────────────────┘               └──────────────────────────┘
```

### 🎯 Benefits of This Architecture
1. **Separation of Concerns**: User interface separate from business logic
2. **Reusability**: Multiple scripts can use the same core modules
3. **Maintainability**: Logic changes in `src/`, interface changes in `scripts/`
4. **Testability**: Core logic can be tested independently of user interfaces
5. **Professional Standards**: Follows Python packaging best practices

## 🔍 Key Features by Directory

### `docs/` - Comprehensive Documentation
- **Feature Guides**: Detailed documentation of all capabilities
- **Usage Examples**: Step-by-step instructions and examples
- **Technical Documentation**: API references and methodology

### `examples/` - Learning and Testing
- **Basic Examples**: Simple demonstrations of core functionality
- **Test Scenarios**: Predefined test cases for validation
- **Code Templates**: Starting points for custom analysis

## 🔧 Development Notes

### Cross-Platform Compatibility
All path resolution is designed for cross-platform compatibility:
```python
# Robust cross-platform path resolution
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Cross-platform output path generation with normalization
script_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(script_dir)
output_path = os.path.normpath(os.path.join(repo_root, 'output', subdir, filename))
```

### Import Path Management
- **Absolute Path Resolution**: Uses `os.path.abspath()` for reliable path resolution
- **Cross-Platform Separators**: Uses `os.path.join()` for proper directory separators
- **Working Directory Independent**: Scripts work regardless of current working directory
- **Normalized Paths**: Uses `os.path.normpath()` for consistent path format

### Platform Independence Features
- **Windows Compatible**: Handles Windows path separators and drive letters
- **Unix/Linux Compatible**: Works with Unix-style paths and permissions
- **macOS Compatible**: Handles macOS-specific path requirements
- **Python Environment Independent**: Works with conda, venv, or system Python

### Backward Compatibility
- All original functionality preserved
- Original API fully maintained  
- Enhanced features are additive and optional
- Users can choose analysis complexity level

### Professional Standards
- Clear separation of concerns
- Comprehensive documentation
- Cross-platform path handling
- Organized output management with type-based subdirectories
- Consistent file organization
- Clean, maintainable code structure

### Output File Management
- **Automatic Organization**: Files are automatically placed in appropriate subdirectories
- **Cross-Platform Directory Creation**: Uses `os.makedirs()` with `exist_ok=True`
- **Clean Root Directory**: No generated files accumulate in the repository root
- **Professional Structure**: Organized by file type for easy maintenance and discovery
- **Timestamped Files**: All outputs include timestamps to prevent overwrites
- **Normalized Paths**: All output paths are normalized for the target operating system

---

*This professional structure supports both academic research and practical implementation while maintaining the innovative QOL decay methodology that provides 8.5% utility improvement over traditional approaches. The organized output management ensures a clean, professional appearance suitable for public repository release.*