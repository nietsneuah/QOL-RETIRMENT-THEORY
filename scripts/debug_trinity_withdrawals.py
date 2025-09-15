#!/usr/bin/env python3
"""
Debug Trinity Study withdrawal calculation to understand the real vs nominal issue.
"""

import sys
import os
import pandas as pd
import numpy as np

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from enhanced_qol_framework import EnhancedQOLFramework

def debug_trinity_withdrawals():
    """Debug what Trinity Study actually produces."""
    
    print("🔍 Trinity Study Withdrawal Debug")
    print("=" * 50)
    
    # Simple parameters for debugging
    starting_value = 1000000
    starting_age = 70
    years = 5  # Just 5 years for debugging
    simulations = 3  # Just 3 simulations
    
    # Market parameters
    base_real_return = 0.015
    base_inflation = 0.03
    return_volatility = 0.0  # No volatility for debugging
    
    framework = EnhancedQOLFramework(
        starting_value=starting_value,
        starting_age=starting_age,
        horizon_years=years,
        n_simulations=simulations
    )
    
    # Run Trinity Study simulation
    framework.run_enhanced_simulation(
        withdrawal_strategy='trinity_4pct',
        return_volatility=return_volatility,
        inflation_variability=False,  # Fixed inflation for debugging
        base_real_return=base_real_return,
        base_inflation=base_inflation,
        qol_variability=False,
        verbose=True
    )
    
    # Get results
    withdrawal_paths = np.array(framework.simulation_results['withdrawal_paths'])
    inflation_paths = np.array(framework.simulation_results['inflation_paths'])
    
    print(f"\nStarting portfolio: ${starting_value:,}")
    print(f"Base withdrawal (4%): ${starting_value * 0.04:,}")
    print(f"Fixed inflation rate: {base_inflation:.1%}")
    print()
    
    # Analyze first simulation in detail
    sim = 0
    print(f"Simulation {sim + 1} Analysis:")
    print("-" * 30)
    
    cumulative_inflation = 1.0
    base_withdrawal = starting_value * 0.04
    
    for year in range(years):
        if year > 0:
            cumulative_inflation *= (1 + base_inflation)
        
        expected_nominal = base_withdrawal * cumulative_inflation
        actual_withdrawal = withdrawal_paths[sim, year]
        
        # Calculate what the real value should be
        real_value = actual_withdrawal / cumulative_inflation
        
        print(f"Year {year + 1}:")
        print(f"  Cumulative inflation factor: {cumulative_inflation:.4f}")
        print(f"  Expected nominal withdrawal: ${expected_nominal:,.0f}")
        print(f"  Actual withdrawal from sim: ${actual_withdrawal:,.0f}")
        print(f"  Real purchasing power: ${real_value:,.0f}")
        print(f"  Match expected? {abs(expected_nominal - actual_withdrawal) < 1:.0f}")
        print()
    
    print("🔍 Summary:")
    print("- Trinity Study withdrawals ARE inflation-adjusted nominal amounts")
    print("- To get constant real purchasing power, divide by cumulative inflation")
    print("- The withdrawals should increase each year with inflation")
    print("- When deflated back, they should all equal $40,000 real")

if __name__ == "__main__":
    debug_trinity_withdrawals()