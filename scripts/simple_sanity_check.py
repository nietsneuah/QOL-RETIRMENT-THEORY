#!/usr/bin/env python3
"""
Simple Sanity Check for QOL Framework

Tests basic math with simplified assumptions:
- 0% volatility
- 0% inflation  
- 7% CAGR
- Fixed withdrawal rates (no QOL adjustments)
"""

import sys
import os
import pandas as pd
import numpy as np

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from enhanced_qol_framework import EnhancedQOLFramework

def run_simple_sanity_check():
    """Run sanity check with simple fixed withdrawal rates."""
    
    print("🧪 Simple QOL Framework Sanity Check")
    print("=" * 50)
    print("Parameters:")
    print("- 0% volatility (no randomness)")
    print("- 0% inflation")
    print("- 7% CAGR (fixed returns)")
    print("- Fixed withdrawal rates (no phases)")
    print()
    
    # Test parameters
    starting_value = 1000000
    starting_age = 70
    years = 10  # Shorter test
    simulations = 1  # Just one since no randomness
    
    # Test different fixed withdrawal rates
    withdrawal_rates = [0.04, 0.05, 0.06, 0.07]
    
    results = {}
    
    for rate in withdrawal_rates:
        print(f"🔄 Testing {rate:.1%} fixed withdrawal rate")
        
        # Create framework with this rate for all phases
        framework = EnhancedQOLFramework(
            starting_value=starting_value,
            starting_age=starting_age,
            horizon_years=years,
            n_simulations=simulations,
            qol_phase1_rate=rate,  # All phases use same rate
            qol_phase2_rate=rate,
            qol_phase3_rate=rate
        )
        
        # Run with sanity check parameters
        framework.run_enhanced_simulation(
            withdrawal_strategy='custom',  # Use our custom rates
            return_volatility=0.0,  # 0% volatility
            inflation_variability=False,  # No inflation variability
            base_real_return=0.07,  # 7% return (nominal = real since 0% inflation)
            base_inflation=0.0,  # 0% inflation
            qol_variability=False,  # No QOL variability
            verbose=False
        )
        
        # Get paths
        portfolio_path = framework.simulation_results['portfolio_paths'][0]
        withdrawal_path = framework.simulation_results['withdrawal_paths'][0]
        
        results[f'{rate:.1%}'] = {
            'rate': rate,
            'portfolio_path': portfolio_path,
            'withdrawal_path': withdrawal_path,
            'final_value': portfolio_path[-1]
        }
        
        print(f"   Final portfolio value: ${portfolio_path[-1]:,.0f}")
        print(f"   Year 1 withdrawal: ${withdrawal_path[0]:,.0f}")
    
    # Manual calculations for verification
    print(f"\n📋 Manual Calculation Verification:")
    print(f"Starting portfolio: ${starting_value:,}")
    print(f"Annual return: 7.0% (fixed)")
    print()
    
    for rate in withdrawal_rates:
        print(f"--- {rate:.1%} Withdrawal Rate ---")
        manual_portfolio = starting_value
        
        for year in range(3):  # Show first 3 years
            withdrawal = manual_portfolio * rate
            manual_portfolio = manual_portfolio * 1.07 - withdrawal
            
            print(f"  Year {year + 1}: Withdraw ${withdrawal:,.0f}, Portfolio becomes ${manual_portfolio:,.0f}")
        
        # Compare with simulation
        sim_result = results[f'{rate:.1%}']
        sim_portfolio_year3 = sim_result['portfolio_path'][3]
        sim_withdrawal_year1 = sim_result['withdrawal_path'][0]
        expected_withdrawal_year1 = starting_value * rate
        
        print(f"  Simulation Year 3 portfolio: ${sim_portfolio_year3:,.0f}")
        print(f"  Simulation Year 1 withdrawal: ${sim_withdrawal_year1:,.0f}")
        print(f"  Expected Year 1 withdrawal: ${expected_withdrawal_year1:,.0f}")
        print(f"  Portfolio match: {'✅' if abs(manual_portfolio - sim_portfolio_year3) < 1 else '❌'}")
        print(f"  Withdrawal match: {'✅' if abs(sim_withdrawal_year1 - expected_withdrawal_year1) < 1 else '❌'}")
        print()
    
    # Create comparison table
    print(f"📊 Year-by-Year Comparison:")
    
    data = []
    for year in range(years + 1):
        age = starting_age + year
        row = {'Year': year, 'Age': age}
        
        for rate_str, result in results.items():
            portfolio_value = result['portfolio_path'][year]
            if year > 0:
                withdrawal = result['withdrawal_path'][year-1]
            else:
                withdrawal = 0
            
            row[f'{rate_str}_Portfolio'] = portfolio_value
            row[f'{rate_str}_Withdrawal'] = withdrawal
        
        data.append(row)
    
    df = pd.DataFrame(data)
    
    # Format for display
    print(df.to_string(index=False, formatters={
        col: '{:,.0f}'.format for col in df.columns if 'Portfolio' in col or 'Withdrawal' in col
    }))
    
    # Export to CSV
    output_path = "output/data/simple_sanity_check_results.csv"
    df.to_csv(output_path, index=False)
    print(f"\n💾 Results saved to: {output_path}")
    
    return results

if __name__ == "__main__":
    run_simple_sanity_check()