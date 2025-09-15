# QOL Framework Report Formats

The QOL Framework supports **two specialized report output formats** optimized for different use cases:

## 🎯 Usage Commands

### 1. ReportLab Professional PDF Report ⭐ **DEFAULT**  
```bash
python scripts/scenario_runner.py
```
- **Technology**: ReportLab library with matplotlib integration
- **Strengths**: Professional business formatting, embedded charts, executive summaries, consistent data
- **Best for**: Business presentations, client reports, professional analysis, all standard reporting needs
- **Features**: 
  - Executive summary section
  - Embedded matplotlib charts
  - Professional styling and typography
  - Comprehensive scenario details
  - Methodology explanations

### 2. LaTeX Professional PDF Report (Research Papers Only)
```bash
python scripts/scenario_runner.py --latex
```
- **Technology**: LaTeX typesetting system with BasicTeX
- **Strengths**: Academic-quality typography, mathematical notation, professional layout
- **Best for**: **RESEARCH PAPERS ONLY** - Academic publications, mathematical analysis, formal documentation
- **Requirements**: LaTeX PATH setup via `source setup_latex_path.sh`
- **Note**: ⚠️ **LaTeX is exclusively for research papers, not business reports**

## 📁 Output Locations

All reports are automatically saved to:
```
/output/reports/
├── qol_reportlab_professional_report_[timestamp].pdf  # ReportLab PDF (Default)
└── qol_latex_professional_report_[timestamp].pdf      # LaTeX PDF (Research)
```

## 🔧 Technical Details

### ReportLab PDF ⭐ (Default)
- Professional document generation library
- Combines text, charts, and data tables seamlessly  
- Custom styling with business-appropriate formatting
- Consistent data across all visualizations
- Executive summary and methodology sections
- Superior formatting and presentation
- No external dependencies required

### LaTeX PDF (Research Only)
- Requires BasicTeX installation and PATH configuration
- Uses custom LaTeX templates with professional formatting
- Mathematical notation support
- Academic-style layout
- Optimized for research paper formatting

## 🚀 Enhanced Mode

## 🚀 Enhanced Analysis Options

For advanced analysis, use the dedicated enhanced scenario runner:
```bash
python scripts/enhanced_scenario_runner.py --all --pdf    # Professional enhanced analysis
python scripts/enhanced_scenario_runner.py --list         # See all available scenarios
```

For research papers with LaTeX formatting:
```bash
python scripts/scenario_runner.py --latex                 # LaTeX research papers only
```

## 📋 Report Content Comparison

| Feature | ReportLab (Default) | LaTeX (Research) |
|---------|---------------------|------------------|
| Chart Quality | ⭐ Excellent | ✅ Good |
| Text Formatting | ⭐ Professional Business | ⭐ Academic |  
| Data Consistency | ⭐ Consistent | ⚠️ Demo Data |
| Generation Speed | ✅ Fast | ⚠️ Slower |
| Professional Look | ⭐ Business | ⭐ Academic |
| Setup Required | ✅ None | ⚠️ LaTeX PATH |
| Use Case | Business Reports | Research Papers |

**Default Choice**: ReportLab format provides professional business reports with consistent data and superior formatting.