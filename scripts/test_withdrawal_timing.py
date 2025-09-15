#!/usr/bin/env python3
"""
Test withdrawal timing: Are returns applied before or after withdrawals?
This affects whether QOL strategies have the same timing error as Trinity Study.
"""

import sys
import os
import numpy as np

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from enhanced_qol_framework import EnhancedQOLFramework

def test_withdrawal_timing():
    """Test withdrawal timing and return application order."""
    
    print("⏰ Testing Withdrawal Timing and Return Application")
    print("=" * 60)
    
    # Simple test case
    starting_value = 1000000
    years = 3
    simulations = 1
    
    framework = EnhancedQOLFramework(
        starting_value=starting_value,
        starting_age=70,
        horizon_years=years,
        n_simulations=simulations,
        qol_phase1_rate=0.05,  # 5% withdrawal rate
        qol_phase2_rate=0.05,
        qol_phase3_rate=0.05
    )
    
    # Run with fixed parameters for predictable results
    framework.run_enhanced_simulation(
        withdrawal_strategy='hauenstein',
        return_volatility=0.0,  # No variance
        inflation_variability=False,
        base_real_return=0.10,  # 10% return for easy math
        base_inflation=0.00,    # No inflation for simplicity
        qol_variability=False,
        verbose=False
    )
    
    portfolio_paths = framework.simulation_results['portfolio_paths'][0]
    withdrawal_paths = framework.simulation_results['withdrawal_paths'][0]
    return_paths = framework.simulation_results['return_paths'][0]
    
    print("🔍 Manual Calculation vs Framework Results")
    print("Fixed parameters: 10% return, 5% withdrawal, no inflation")
    print()
    
    # Manual calculation - Method 1: Withdraw first, then apply returns
    print("📊 Method 1: Withdraw FIRST, then apply returns")
    manual_portfolio_1 = starting_value
    for year in range(years):
        withdrawal = manual_portfolio_1 * 0.05
        after_withdrawal = manual_portfolio_1 - withdrawal
        after_returns = after_withdrawal * 1.10
        
        print(f"Year {year+1}:")
        print(f"  Start: ${manual_portfolio_1:,.0f}")
        print(f"  Withdraw: ${withdrawal:,.0f}")
        print(f"  After withdrawal: ${after_withdrawal:,.0f}")
        print(f"  After 10% return: ${after_returns:,.0f}")
        
        manual_portfolio_1 = after_returns
    
    print()
    
    # Manual calculation - Method 2: Apply returns first, then withdraw
    print("📊 Method 2: Apply RETURNS first, then withdraw")
    manual_portfolio_2 = starting_value
    for year in range(years):
        after_returns = manual_portfolio_2 * 1.10
        withdrawal = manual_portfolio_2 * 0.05  # Withdrawal based on start-of-year value
        after_withdrawal = after_returns - withdrawal
        
        print(f"Year {year+1}:")
        print(f"  Start: ${manual_portfolio_2:,.0f}")
        print(f"  After 10% return: ${after_returns:,.0f}")
        print(f"  Withdraw: ${withdrawal:,.0f} (5% of start value)")
        print(f"  Final: ${after_withdrawal:,.0f}")
        
        manual_portfolio_2 = after_withdrawal
    
    print()
    
    # Framework results
    print("📊 Framework Results:")
    for year in range(years):
        print(f"Year {year+1}:")
        print(f"  Start: ${portfolio_paths[year]:,.0f}")
        print(f"  Withdrawal: ${withdrawal_paths[year]:,.0f}")
        print(f"  Return: {return_paths[year]:.1%}")
        print(f"  End: ${portfolio_paths[year+1]:,.0f}")
    
    print()
    print("🎯 Comparison:")
    print(f"Method 1 (withdraw first): Final = ${manual_portfolio_1:,.0f}")
    print(f"Method 2 (returns first):  Final = ${manual_portfolio_2:,.0f}")
    print(f"Framework result:           Final = ${portfolio_paths[-1]:,.0f}")
    
    if abs(portfolio_paths[-1] - manual_portfolio_1) < 1:
        print("✅ Framework uses Method 1: Withdraw first, then returns")
    elif abs(portfolio_paths[-1] - manual_portfolio_2) < 1:
        print("✅ Framework uses Method 2: Returns first, then withdraw")
    else:
        print("❓ Framework uses a different method")
    
    # Test if this affects real purchasing power calculations
    print()
    print("🔍 Impact on Real Purchasing Power:")
    print("QOL strategies withdraw based on current portfolio value.")
    print("Unlike Trinity Study, they don't have a fixed real amount.")
    print("So withdrawal timing affects the nominal amounts but not")
    print("the concept of 'real purchasing power' since withdrawals")
    print("automatically adjust to portfolio performance.")

if __name__ == "__main__":
    test_withdrawal_timing()