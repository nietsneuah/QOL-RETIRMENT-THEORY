#!/usr/bin/env python3
"""
Trinity Study Verification Test

Verify that Trinity 4% rule produces:
1. Fixed real purchasing power (inflation-adjusted withdrawals)
2. Portfolio fluctuates based on market performance
3. Withdrawal amount independent of portfolio value
"""

import sys
import os
import pandas as pd
import numpy as np

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from enhanced_qol_framework import EnhancedQOLFramework

def verify_trinity_implementation():
    """Verify Trinity Study implementation with simple scenario."""
    
    print("🔍 Trinity Study Implementation Verification")
    print("=" * 55)
    print("Test Scenario:")
    print("- $1M initial portfolio")
    print("- 3% fixed inflation")
    print("- 5% fixed returns (2% real)")
    print("- Trinity 4% rule")
    print("- Expected: $40K Year 1, then inflation-adjusted")
    print()
    
    # Test parameters
    starting_value = 1000000
    starting_age = 70
    years = 10  # First 10 years for clarity
    simulations = 1
    
    # Create framework
    framework = EnhancedQOLFramework(
        starting_value=starting_value,
        starting_age=starting_age,
        horizon_years=years,
        n_simulations=simulations,
        qol_phase1_rate=0.04,  # Not used for Trinity
        qol_phase2_rate=0.04,
        qol_phase3_rate=0.04
    )
    
    # Run Trinity simulation
    framework.run_enhanced_simulation(
        withdrawal_strategy='trinity_4pct',
        return_volatility=0.0,  # No volatility for clean test
        inflation_variability=False,  # Fixed inflation
        base_real_return=0.02,  # 2% real return (5% nominal - 3% inflation)
        base_inflation=0.03,  # 3% inflation
        qol_variability=False,
        verbose=False
    )
    
    # Get results
    portfolio_path = framework.simulation_results['portfolio_paths'][0]
    withdrawal_path = framework.simulation_results['withdrawal_paths'][0]
    
    print("📊 Trinity Study Results:")
    print(f"{'Year':<4} {'Age':<3} {'Portfolio':<12} {'Withdrawal':<12} {'Real Value':<12}")
    print("-" * 55)
    
    # Calculate expected values manually
    manual_portfolio = starting_value
    base_withdrawal = starting_value * 0.04  # $40,000
    
    data = []
    
    for year in range(years + 1):
        age = starting_age + year
        
        if year == 0:
            portfolio_value = starting_value
            withdrawal = 0
            real_value = 40000  # Base real value
        else:
            # Expected withdrawal (inflation-adjusted)
            expected_withdrawal = base_withdrawal * (1.03 ** year)
            
            # Manual portfolio calculation
            # Last year: portfolio grew 5%, then withdrew inflation-adjusted amount
            if year == 1:
                manual_portfolio = starting_value * 1.05 - expected_withdrawal
            else:
                manual_portfolio = manual_portfolio * 1.05 - expected_withdrawal
            
            # Simulation results
            portfolio_value = portfolio_path[year]
            withdrawal = withdrawal_path[year-1]
            
            # Real purchasing power (deflated back to Year 1 dollars)
            real_value = withdrawal / (1.03 ** (year-1))
        
        print(f"{year:<4} {age:<3} ${portfolio_value:<11,.0f} ${withdrawal:<11,.0f} ${real_value:<11,.0f}")
        
        # Store for analysis
        data.append({
            'Year': year,
            'Age': age,
            'Portfolio': portfolio_value,
            'Withdrawal': withdrawal,
            'Real_Value': real_value,
            'Expected_Portfolio': manual_portfolio if year > 0 else starting_value,
            'Inflation_Factor': 1.03 ** year
        })
    
    # Create dataframe for analysis
    df = pd.DataFrame(data)
    
    # Verify consistency
    print(f"\n🔍 Verification Checks:")
    
    # Check 1: Real purchasing power should be constant
    real_values = df[df['Year'] > 0]['Real_Value'].values
    real_variation = np.std(real_values)
    print(f"Real purchasing power variation: ${real_variation:.2f}")
    print(f"Real purchasing power constant: {'✅' if real_variation < 1 else '❌'}")
    
    # Check 2: Withdrawals should increase with inflation
    if len(withdrawal_path) >= 2:
        withdrawal_growth = withdrawal_path[1] / withdrawal_path[0] - 1
        print(f"Year 1-2 withdrawal growth: {withdrawal_growth:.1%} (expected: 3.0%)")
        print(f"Inflation adjustment correct: {'✅' if abs(withdrawal_growth - 0.03) < 0.001 else '❌'}")
    
    # Check 3: Portfolio math
    expected_year_2 = (starting_value * 1.05) - (base_withdrawal * 1.03)
    actual_year_2 = portfolio_path[2] if len(portfolio_path) > 2 else 0
    print(f"Year 2 portfolio - Expected: ${expected_year_2:,.0f}, Actual: ${actual_year_2:,.0f}")
    print(f"Portfolio math correct: {'✅' if abs(expected_year_2 - actual_year_2) < 10 else '❌'}")
    
    # Show the key insight
    print(f"\n💡 Key Trinity Study Characteristics:")
    print(f"1. Withdrawal amounts INCREASE with inflation each year")
    print(f"2. Portfolio value FLUCTUATES based on market performance")
    print(f"3. Bad markets + fixed withdrawals = portfolio depletion risk")
    print(f"4. Good markets + fixed withdrawals = portfolio growth")
    
    # Export results
    output_path = "output/data/trinity_verification.csv"
    df.to_csv(output_path, index=False)
    print(f"\n💾 Detailed verification saved to: {output_path}")
    
    return df

if __name__ == "__main__":
    verify_trinity_implementation()