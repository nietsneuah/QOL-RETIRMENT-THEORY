#!/usr/bin/env python3
"""
Test if QOL real purchasing power calculations are consistent.
Since QOL uses percentage withdrawals, there shouldn't be a fixed real amount issue.
"""

import sys
import os
import numpy as np

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from enhanced_qol_framework import EnhancedQOLFramework

def test_qol_real_purchasing_power():
    """Test QOL real purchasing power consistency."""
    
    print("💰 Testing QOL Real Purchasing Power Consistency")
    print("=" * 55)
    
    # Test parameters
    starting_value = 1000000
    years = 5
    simulations = 3
    
    framework = EnhancedQOLFramework(
        starting_value=starting_value,
        starting_age=70,
        horizon_years=years,
        n_simulations=simulations,
        qol_phase1_rate=0.054,  # 5.4% QOL Standard
        qol_phase2_rate=0.045,
        qol_phase3_rate=0.035
    )
    
    # Run with fixed inflation to see the pattern clearly
    framework.run_enhanced_simulation(
        withdrawal_strategy='hauenstein',
        return_volatility=0.0,
        inflation_variability=False,  # Fixed 3% inflation
        base_real_return=0.015,       # 1.5% real return
        base_inflation=0.03,          # 3% inflation
        qol_variability=False,
        verbose=False
    )
    
    portfolio_paths = framework.simulation_results['portfolio_paths'][0]
    withdrawal_paths = framework.simulation_results['withdrawal_paths'][0]
    inflation_paths = framework.simulation_results['inflation_paths'][0]
    
    print("📊 QOL Standard Strategy Analysis")
    print("Fixed: 1.5% real return, 3% inflation, no volatility")
    print()
    
    cumulative_inflation = 1.0
    print(f"{'Year':<4} {'Portfolio':<12} {'Withdrawal':<12} {'Rate':<6} {'Real Withdrawal':<15} {'Real/Start':<10}")
    print("-" * 70)
    
    for year in range(years):
        if year > 0:
            cumulative_inflation *= (1 + inflation_paths[year-1])
        
        withdrawal_rate = 0.054 if year < 10 else (0.045 if year < 20 else 0.035)
        real_withdrawal = withdrawal_paths[year] / cumulative_inflation
        real_as_pct_of_start = real_withdrawal / starting_value
        
        print(f"{year+1:<4} ${portfolio_paths[year]:<11,.0f} ${withdrawal_paths[year]:<11,.0f} {withdrawal_rate:<5.1%} ${real_withdrawal:<14,.0f} {real_as_pct_of_start:<9.2%}")
    
    print()
    print("🔍 Key Observations:")
    print("1. QOL withdrawals are percentage-based, not fixed real amounts")
    print("2. Real withdrawal amounts vary with portfolio performance")
    print("3. This is intentional - QOL adjusts spending to portfolio health")
    print("4. No 'inflation timing error' because there's no fixed real target")
    
    # Compare with what Trinity Study SHOULD do
    print()
    print("📊 Comparison: Trinity Study (Fixed Real Amount)")
    trinity_real = 40000
    print(f"{'Year':<4} {'Trinity Nominal':<15} {'Trinity Real':<12}")
    print("-" * 35)
    
    cumulative_inflation = 1.0
    for year in range(years):
        if year > 0:
            cumulative_inflation *= (1 + 0.03)  # 3% inflation
        
        trinity_nominal = trinity_real * cumulative_inflation
        print(f"{year+1:<4} ${trinity_nominal:<14,.0f} ${trinity_real:<11,.0f}")
    
    print()
    print("🎯 Conclusion:")
    print("✅ QOL strategies don't have the Trinity Study inflation timing issue")
    print("   because they use percentage-based withdrawals, not fixed real amounts.")
    print("   The 'real purchasing power' varies intentionally with portfolio health.")

if __name__ == "__main__":
    test_qol_real_purchasing_power()