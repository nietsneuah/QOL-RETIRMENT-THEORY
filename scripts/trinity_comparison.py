#!/usr/bin/env python3
"""
Trinity Study vs Current Approach Comparison

Compares:
1. Trinity Study: Fixed $40K/year adjusted for inflation
2. Current: 4% of current portfolio value each year
3. Zero inflation for pure comparison
"""

import sys
import os
import pandas as pd
import numpy as np

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from enhanced_qol_framework import EnhancedQOLFramework

def run_trinity_comparison():
    """Compare Trinity Study vs current withdrawal approaches."""
    
    print("🧪 Trinity Study vs Current Approach Comparison")
    print("=" * 60)
    print("Parameters:")
    print("- 0% volatility (deterministic)")
    print("- 0% inflation (pure comparison)")
    print("- 7% CAGR")
    print("- Trinity: Fixed $40K/year (no inflation adjustment needed)")
    print("- Current: 4% of current portfolio each year")
    print()
    
    # Test parameters
    starting_value = 1000000
    starting_age = 70
    years = 29
    simulations = 1
    
    strategies = {
        'Trinity_4pct': 'trinity_4pct',
        'Dynamic_4pct': 'dynamic_4pct'
    }
    
    results = {}
    
    for name, strategy in strategies.items():
        print(f"🔄 Running {name} strategy")
        
        # Create framework (rates don't matter for these strategies)
        framework = EnhancedQOLFramework(
            starting_value=starting_value,
            starting_age=starting_age,
            horizon_years=years,
            n_simulations=simulations,
            qol_phase1_rate=0.04,  # Not used for these strategies
            qol_phase2_rate=0.04,
            qol_phase3_rate=0.04
        )
        
        # Run simulation
        framework.run_enhanced_simulation(
            withdrawal_strategy=strategy,
            return_volatility=0.0,  # 0% volatility
            inflation_variability=False,  # No inflation variability
            base_real_return=0.07,  # 7% return
            base_inflation=0.0,  # 0% inflation
            qol_variability=False,  # No QOL variability
            verbose=False
        )
        
        # Get paths
        portfolio_path = framework.simulation_results['portfolio_paths'][0]
        withdrawal_path = framework.simulation_results['withdrawal_paths'][0]
        
        results[name] = {
            'strategy': strategy,
            'portfolio_path': portfolio_path,
            'withdrawal_path': withdrawal_path,
            'final_value': portfolio_path[-1],
            'total_withdrawn': sum(withdrawal_path)
        }
        
        print(f"   Final portfolio: ${portfolio_path[-1]:,.0f}")
        print(f"   Total withdrawn: ${sum(withdrawal_path):,.0f}")
    
    # Manual verification for Trinity Study
    print(f"\n📋 Manual Trinity Study Verification:")
    manual_portfolio = starting_value
    annual_withdrawal = starting_value * 0.04  # Fixed $40,000
    
    print(f"Fixed annual withdrawal: ${annual_withdrawal:,.0f}")
    
    for year in range(5):
        # Trinity: withdraw fixed amount, then apply returns
        manual_portfolio = (manual_portfolio - annual_withdrawal) * 1.07
        sim_portfolio = results['Trinity_4pct']['portfolio_path'][year + 1]
        sim_withdrawal = results['Trinity_4pct']['withdrawal_path'][year]
        
        print(f"Year {year + 1}:")
        print(f"  Manual: Portfolio ${manual_portfolio:,.0f}")
        print(f"  Simulation: Portfolio ${sim_portfolio:,.0f}, Withdrawal ${sim_withdrawal:,.0f}")
        print(f"  Match: {'✅' if abs(manual_portfolio - sim_portfolio) < 1 else '❌'}")
    
    # Create comparison dataframe
    data = []
    
    for year in range(years + 1):
        age = starting_age + year
        row = {'Year': year, 'Age': age}
        
        for name, result in results.items():
            portfolio_value = result['portfolio_path'][year]
            if year > 0:
                withdrawal = result['withdrawal_path'][year-1]
                total_withdrawn = sum(result['withdrawal_path'][:year])
            else:
                withdrawal = 0
                total_withdrawn = 0
            
            row[f'{name}_Portfolio'] = portfolio_value
            row[f'{name}_Withdrawal'] = withdrawal
            row[f'{name}_Total_Withdrawn'] = total_withdrawn
        
        data.append(row)
    
    df = pd.DataFrame(data)
    
    # Calculate key differences
    trinity_final = results['Trinity_4pct']['final_value']
    dynamic_final = results['Dynamic_4pct']['final_value']
    trinity_total = results['Trinity_4pct']['total_withdrawn']
    dynamic_total = results['Dynamic_4pct']['total_withdrawn']
    
    print(f"\n📊 Final Comparison (Year {years}):")
    print(f"Trinity Study 4%:")
    print(f"  Final portfolio: ${trinity_final:,.0f}")
    print(f"  Total withdrawn: ${trinity_total:,.0f}")
    print(f"  Average annual withdrawal: ${trinity_total/years:,.0f}")
    
    print(f"\nDynamic 4% (current):")
    print(f"  Final portfolio: ${dynamic_final:,.0f}")
    print(f"  Total withdrawn: ${dynamic_total:,.0f}")
    print(f"  Average annual withdrawal: ${dynamic_total/years:,.0f}")
    
    print(f"\nDifferences:")
    print(f"  Portfolio difference: ${trinity_final - dynamic_final:,.0f}")
    print(f"  Withdrawal difference: ${trinity_total - dynamic_total:,.0f}")
    
    # Show withdrawal patterns
    print(f"\n💰 Withdrawal Patterns:")
    print(f"Trinity Study - Fixed $40K per year")
    print(f"Dynamic 4% - Decreasing amounts:")
    for year in [1, 5, 10, 15, 20, 25, 29]:
        if year <= len(results['Dynamic_4pct']['withdrawal_path']):
            dynamic_withdrawal = results['Dynamic_4pct']['withdrawal_path'][year-1]
            print(f"  Year {year:2d}: ${dynamic_withdrawal:,.0f}")
    
    # Export to CSV
    output_path = "output/data/trinity_vs_dynamic_comparison.csv"
    df.to_csv(output_path, index=False)
    print(f"\n💾 Detailed comparison saved to: {output_path}")
    
    # Display first 10 years
    print(f"\n📋 First 10 Years Comparison:")
    display_cols = ['Year', 'Age', 'Trinity_4pct_Portfolio', 'Trinity_4pct_Withdrawal', 
                    'Dynamic_4pct_Portfolio', 'Dynamic_4pct_Withdrawal']
    print(df[display_cols].head(10).to_string(index=False, formatters={
        col: '${:,.0f}'.format for col in display_cols if 'Portfolio' in col or 'Withdrawal' in col
    }))
    
    return df

if __name__ == "__main__":
    run_trinity_comparison()