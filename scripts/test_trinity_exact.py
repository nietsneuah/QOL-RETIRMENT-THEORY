#!/usr/bin/env python3
"""
Check if Trinity Study should always produce exactly $40K real withdrawals.
"""

import sys
import os
import pandas as pd
import numpy as np

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from enhanced_qol_framework import EnhancedQOLFramework

def test_trinity_exact():
    """Test if Trinity produces exactly $40K real."""
    
    print("🎯 Testing Trinity Study Exact Real Withdrawals")
    print("=" * 55)
    
    # Fixed parameters - no randomness
    starting_value = 1000000
    years = 10
    simulations = 1000
    
    framework = EnhancedQOLFramework(
        starting_value=starting_value,
        starting_age=70,
        horizon_years=years,
        n_simulations=simulations
    )
    
    # Run with inflation variability TRUE (realistic)
    print("\n📊 Test 1: With Inflation Variability (Realistic)")
    framework.run_enhanced_simulation(
        withdrawal_strategy='trinity_4pct',
        return_volatility=0.15,
        inflation_variability=True,  # Random inflation
        base_real_return=0.015,
        base_inflation=0.03,
        qol_variability=False,
        verbose=False
    )
    
    withdrawal_paths = np.array(framework.simulation_results['withdrawal_paths'])
    inflation_paths = np.array(framework.simulation_results['inflation_paths'])
    
    # Calculate real withdrawals for all simulations
    real_withdrawals_year1 = []
    real_withdrawals_year5 = []
    real_withdrawals_year10 = []
    
    for sim in range(min(100, simulations)):  # Check first 100 sims
        cumulative_inflation = 1.0
        
        # Year 1 real withdrawal
        real_year1 = withdrawal_paths[sim, 0] / cumulative_inflation
        real_withdrawals_year1.append(real_year1)
        
        # Year 5 real withdrawal
        for year in range(4):  # Years 0-3 (to get to year 5)
            cumulative_inflation *= (1 + inflation_paths[sim, year])
        real_year5 = withdrawal_paths[sim, 4] / cumulative_inflation
        real_withdrawals_year5.append(real_year5)
        
        # Year 10 real withdrawal
        cumulative_inflation = 1.0
        for year in range(9):  # Years 0-8 (to get to year 10)
            cumulative_inflation *= (1 + inflation_paths[sim, year])
        real_year10 = withdrawal_paths[sim, 9] / cumulative_inflation
        real_withdrawals_year10.append(real_year10)
    
    print(f"Year 1 real withdrawals:")
    print(f"  Mean: ${np.mean(real_withdrawals_year1):,.0f}")
    print(f"  Std:  ${np.std(real_withdrawals_year1):,.0f}")
    print(f"  Range: ${np.min(real_withdrawals_year1):,.0f} - ${np.max(real_withdrawals_year1):,.0f}")
    
    print(f"\nYear 5 real withdrawals:")
    print(f"  Mean: ${np.mean(real_withdrawals_year5):,.0f}")
    print(f"  Std:  ${np.std(real_withdrawals_year5):,.0f}")
    print(f"  Range: ${np.min(real_withdrawals_year5):,.0f} - ${np.max(real_withdrawals_year5):,.0f}")
    
    print(f"\nYear 10 real withdrawals:")
    print(f"  Mean: ${np.mean(real_withdrawals_year10):,.0f}")
    print(f"  Std:  ${np.std(real_withdrawals_year10):,.0f}")
    print(f"  Range: ${np.min(real_withdrawals_year10):,.0f} - ${np.max(real_withdrawals_year10):,.0f}")
    
    # Run with inflation variability FALSE (exact)
    print(f"\n📊 Test 2: WITHOUT Inflation Variability (Exact)")
    framework2 = EnhancedQOLFramework(
        starting_value=starting_value,
        starting_age=70,
        horizon_years=years,
        n_simulations=3  # Just a few for exact test
    )
    
    framework2.run_enhanced_simulation(
        withdrawal_strategy='trinity_4pct',
        return_volatility=0.0,  # No return variance
        inflation_variability=False,  # Fixed inflation
        base_real_return=0.015,
        base_inflation=0.03,
        qol_variability=False,
        verbose=False
    )
    
    withdrawal_paths2 = np.array(framework2.simulation_results['withdrawal_paths'])
    inflation_paths2 = np.array(framework2.simulation_results['inflation_paths'])
    
    print(f"Fixed inflation rate: {framework2.simulation_results['inflation_paths'][0][0]:.3f}")
    
    sim = 0
    cumulative_inflation = 1.0
    print(f"\nExact calculation for Simulation 1:")
    for year in range(5):
        if year > 0:
            cumulative_inflation *= (1 + framework2.simulation_results['inflation_paths'][sim][year-1])
        
        nominal_withdrawal = withdrawal_paths2[sim, year]
        real_withdrawal = nominal_withdrawal / cumulative_inflation
        
        print(f"Year {year+1}: Nominal=${nominal_withdrawal:,.0f}, Real=${real_withdrawal:,.0f}")
    
    print(f"\n🎯 CONCLUSION:")
    if np.std(real_withdrawals_year1) < 100:  # Very small variance
        print("✅ Trinity Study produces nearly constant real withdrawals")
        print("   Small variations due to inflation randomness in Year 1")
    else:
        print("❌ Trinity Study has significant real withdrawal variation")
        print("   This suggests a calculation error")

if __name__ == "__main__":
    test_trinity_exact()