# QOL Framework Usage Guide

## 🎯 Quick Start Commands

### For Business Reports & Analysis (Most Common)
```bash
# Standard professional reports (ReportLab - recommended)
python scripts/scenario_runner.py

# Advanced multi-scenario analysis 
python scripts/enhanced_scenario_runner.py --all --pdf
```

### For Research Papers Only
```bash
# LaTeX academic formatting (research only)
python scripts/scenario_runner.py --latex
```

## 📊 Report Types by Use Case

| Use Case | Command | Output Format |
|----------|---------|---------------|
| **Business Reports** | `python scripts/scenario_runner.py` | ReportLab Professional PDF ⭐ |
| **Advanced Analysis** | `python scripts/enhanced_scenario_runner.py --all --pdf` | Enhanced Professional PDF ⭐ |
| **Research Papers** | `python scripts/scenario_runner.py --latex` | LaTeX Academic PDF |

## 🔧 Setup Requirements

### Standard Use (Business Reports)
- ✅ **No setup required** - works out of the box
- Uses conda environment with ReportLab

### Research Papers (LaTeX)
- ⚠️ **Requires LaTeX setup**: `source setup_latex_path.sh`
- ⚠️ **Research use only** - not for business reports

## 📁 Output Locations

All generated files are organized in `/output/`:
```
output/
├── data/           # CSV files, JSON results
├── charts/         # PNG visualizations  
└── reports/        # PDF reports
    ├── qol_reportlab_professional_report_*.pdf      # Business (default)
    ├── enhanced_qol_framework_report_*.pdf          # Advanced analysis
    └── latex_demo_report.pdf                        # Research papers
```

## 🚀 Recommended Workflow

1. **For most analysis**: Use ReportLab (default) - `python scripts/scenario_runner.py`
2. **For deep analysis**: Use enhanced runner - `python scripts/enhanced_scenario_runner.py --all --pdf`  
3. **For research papers**: Use LaTeX - `python scripts/scenario_runner.py --latex` (after setup)

## ⚠️ Important Notes

- **LaTeX is ONLY for research papers** - not business reports
- **ReportLab is the default** for all business and professional use
- **Enhanced runner** provides the most comprehensive analysis capabilities
- All formats use consistent QOL Framework methodology