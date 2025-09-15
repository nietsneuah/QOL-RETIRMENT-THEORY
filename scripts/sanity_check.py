#!/usr/bin/env python3
"""
Sanity Check Script for QOL Framework

Tests with simplified assumptions:
- 0% volatility
- 0% inflation  
- 7% CAGR
- QOL = 1.0 (no adjustments)
"""

import sys
import os
import pandas as pd
import numpy as np

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from enhanced_qol_framework import EnhancedQOLFramework

def run_sanity_check():
    """Run sanity check with simplified assumptions."""
    
    print("🧪 QOL Framework Sanity Check")
    print("=" * 50)
    print("Parameters:")
    print("- 0% volatility (no randomness)")
    print("- 0% inflation")
    print("- 7% CAGR (fixed returns)")
    print("- QOL = 1.0 (no adjustments)")
    print()
    
    # Test parameters
    starting_value = 1000000
    starting_age = 70
    years = 29
    simulations = 100  # Small number since there's no randomness
    
    # Test strategies with different withdrawal rates
    strategies = {
        'Fixed_4pct': [0.04, 0.04, 0.04],
        'Fixed_5pct': [0.05, 0.05, 0.05], 
        'Fixed_6pct': [0.06, 0.06, 0.06],
        'Fixed_7pct': [0.07, 0.07, 0.07],
        'Traditional_QOL': [0.054, 0.045, 0.035]
    }
    
    results = {}
    
    for strategy_name, rates in strategies.items():
        print(f"🔄 Testing {strategy_name} (Rates: {rates[0]:.1%}/{rates[1]:.1%}/{rates[2]:.1%})")
        
        # Create framework
        framework = EnhancedQOLFramework(
            starting_value=starting_value,
            starting_age=starting_age,
            horizon_years=years,
            n_simulations=simulations,
            qol_phase1_rate=rates[0],
            qol_phase2_rate=rates[1],
            qol_phase3_rate=rates[2]
        )
        
        # Run with sanity check parameters
        framework.run_enhanced_simulation(
            withdrawal_strategy='hauenstein',  # Use hauenstein to get our custom rates
            return_volatility=0.0,  # 0% volatility
            inflation_variability=False,  # No inflation variability
            base_real_return=0.07,  # 7% return (nominal = real since 0% inflation)
            base_inflation=0.0,  # 0% inflation
            qol_variability=False,  # No QOL variability (this will give us QOL = 1.0)
            verbose=False
        )
        
        # Get results
        analysis = framework.get_comprehensive_analysis()
        portfolio_analysis = analysis['enhanced_qol_results']['portfolio_analysis']
        
        # Store results
        results[strategy_name] = {
            'final_value_mean': portfolio_analysis['final_value_mean'],
            'rates': rates,
            'portfolio_paths': np.array(framework.simulation_results['portfolio_paths']),
            'withdrawal_paths': np.array(framework.simulation_results['withdrawal_paths'])
        }
        
        print(f"   Final portfolio value: ${portfolio_analysis['final_value_mean']:,.0f}")
    
    # Manual calculation verification
    print(f"\n📋 Manual Calculation Verification:")
    print(f"Starting portfolio: ${starting_value:,}")
    print(f"Annual return: 7.0% (fixed)")
    print()
    
    # Calculate manually for 4% withdrawal
    manual_portfolio = starting_value
    manual_withdrawals = []
    
    for year in range(5):  # Show first 5 years
        withdrawal = manual_portfolio * 0.04
        manual_withdrawals.append(withdrawal)
        manual_portfolio = manual_portfolio * 1.07 - withdrawal
        
        print(f"Year {year + 1}: Withdraw ${withdrawal:,.0f}, Portfolio becomes ${manual_portfolio:,.0f}")
    
    # Compare with simulation
    sim_4pct = results['Fixed_4pct']
    sim_portfolio_year5 = sim_4pct['portfolio_paths'][0, 5]  # First simulation, year 5
    
    print(f"\nComparison (Year 5):")
    print(f"Manual calculation: ${manual_portfolio:,.0f}")
    print(f"Simulation result:  ${sim_portfolio_year5:,.0f}")
    print(f"Difference: ${abs(manual_portfolio - sim_portfolio_year5):,.0f}")
    
    # Create detailed year-by-year table
    print(f"\n📊 Year-by-Year Comparison Table:")
    
    data = []
    for year in range(min(10, years + 1)):  # Show first 10 years
        age = starting_age + year
        row = {'Year': year, 'Age': age}
        
        for strategy_name, result in results.items():
            portfolio_value = result['portfolio_paths'][0, year]  # First simulation
            if year > 0:
                withdrawal = result['withdrawal_paths'][0, year-1]
            else:
                withdrawal = 0
            
            row[f'{strategy_name}_Portfolio'] = portfolio_value
            row[f'{strategy_name}_Withdrawal'] = withdrawal
        
        data.append(row)
    
    df = pd.DataFrame(data)
    
    # Format for display
    print(df.to_string(index=False, formatters={
        col: '{:,.0f}'.format for col in df.columns if 'Portfolio' in col or 'Withdrawal' in col
    }))
    
    # Export to CSV
    output_path = "output/data/sanity_check_results.csv"
    df.to_csv(output_path, index=False)
    print(f"\n💾 Results saved to: {output_path}")
    
    return results

if __name__ == "__main__":
    run_sanity_check()