"""
QOL Retirement Theory Framework

This package contains the Hauenstein Quality of Life (QOL) Framework for retirement planning,
which introduces age-based quality of life decay into traditional withdrawal strategies.

Key Innovation:
- Quality of Life decreases with age (empirically supported)
- Traditional 4% rule ignores this fundamental reality
- QOL-adjusted withdrawal strategy optimizes utility over lifetime

Author: Doug Hauenstein
"""

from .qol_framework import HypotheticalPortfolioQOLAnalysis

__version__ = "1.0.0"
__author__ = "Doug Hauenstein"

__all__ = ["HypotheticalPortfolioQOLAnalysis"]