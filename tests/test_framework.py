#!/usr/bin/env python
"""
Test script to validate the QOL Framework functionality
"""

import sys
import os
# Add the parent directory to path to find src module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.qol_framework import HypotheticalPortfolioQOLAnalysis
import numpy as np

def test_qol_framework():
    """Basic validation tests for the QOL framework"""
    print("🧪 Testing QOL Framework Components...")
    
    # Initialize analysis
    analysis = HypotheticalPortfolioQOLAnalysis()
    
    # Test 1: QOL function (internal function)
    print("  ✓ Testing Quality of Life function...")
    qol_65 = analysis.qol_function(65)
    qol_85 = analysis.qol_function(85)
    assert qol_65 == 1.0, f"QOL at 65 should be 1.0, got {qol_65}"
    assert qol_85 < qol_65, f"QOL should decrease with age"
    print(f"    QOL at age 65: {qol_65:.3f}")
    print(f"    QOL at age 85: {qol_85:.3f}")
    
    # Test 2: Allocation function
    print("  ✓ Testing dynamic allocation...")
    alloc_65 = analysis.get_allocation(65)
    alloc_85 = analysis.get_allocation(85)
    assert alloc_65['equity'] > alloc_85['equity'], "Equity allocation should decrease with age"
    print(f"    Allocation at 65: {alloc_65['equity']:.0%} equity")
    print(f"    Allocation at 85: {alloc_85['equity']:.0%} equity")
    
    # Test 3: Withdrawal strategies
    print("  ✓ Testing withdrawal strategies...")
    qol_rates = analysis.hauenstein_qol_strategy()
    traditional_rates = analysis.traditional_4_percent_strategy()
    
    # Test QOL strategy has higher rates early
    assert qol_rates[65] > traditional_rates[65], "QOL should have higher early withdrawal rates"
    print(f"    QOL withdrawal rate at 65: {qol_rates[65]:.1%}")
    print(f"    Traditional withdrawal rate at 65: {traditional_rates[65]:.1%}")
    
    # Test 4: Basic framework validation
    print("  ✓ Testing framework initialization...")
    assert analysis.starting_portfolio > 0, "Starting portfolio should be positive"
    assert analysis.retirement_horizon > 0, "Retirement horizon should be positive"
    assert analysis.simulations > 0, "Simulations should be positive"
    
    print(f"    Starting portfolio: ${analysis.starting_portfolio:,}")
    print(f"    Retirement horizon: {analysis.retirement_horizon} years")
    print(f"    Monte Carlo simulations: {analysis.simulations:,}")
    
    print("\n🎉 All tests passed! QOL Framework is working correctly.")
    # Proper pytest assertion instead of return

if __name__ == "__main__":
    test_qol_framework()