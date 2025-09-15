# LaTeX Setup Guide

## Current Status
✅ LaTeX (BasicTeX) is installed on the system  
⚠️ LaTeX is not automatically available in PATH

## Quick Setup

To enable LaTeX for report generation, source the setup script:

```bash
source setup_latex_path.sh
```

This will:
- Add LaTeX to your current session PATH
- Verify LaTeX installation
- Show LaTeX version information

## Permanent Setup

To make LaTeX permanently available, you would need to add the following line to your shell configuration file:

```bash
export PATH="/usr/local/texlive/2025basic/bin/universal-darwin:$PATH"
```

**Note:** The current `.zshrc` file has root permissions, so manual editing may require administrator access.

## Usage with QOL Framework

Once LaTeX is configured:

```bash
# Generate standard PDF reports
python scripts/scenario_runner.py

# Generate LaTeX PDF reports  
source setup_latex_path.sh
python scripts/scenario_runner.py --latex
```

## Report Comparison

- **Standard PDF**: ~81 KB, matplotlib-based charts, scenario-specific data
- **LaTeX PDF**: ~467 KB, professional typography, comprehensive enhanced charts

## Troubleshooting

If LaTeX is not working:
1. Verify installation: `ls -la /usr/local/texlive/*/bin/*/pdflatex`
2. Source the setup script: `source setup_latex_path.sh`
3. Test availability: `which pdflatex`
4. Reinstall if needed: `brew install basictex`