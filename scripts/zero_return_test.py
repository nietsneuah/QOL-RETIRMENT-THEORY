#!/usr/bin/env python3
"""
Zero Return Sanity Check for QOL Framework

Tests with no returns to see pure withdrawal depletion:
- 0% volatility
- 0% inflation  
- 0% CAGR (no returns)
- 4% withdrawal rate only
"""

import sys
import os
import pandas as pd
import numpy as np

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from enhanced_qol_framework import EnhancedQOLFramework

def run_zero_return_test():
    """Run test with 0% returns to see pure withdrawal effects."""
    
    print("🧪 Zero Return Test - Pure Withdrawal Depletion")
    print("=" * 55)
    print("Parameters:")
    print("- 0% volatility (no randomness)")
    print("- 0% inflation")
    print("- 0% CAGR (NO RETURNS)")
    print("- 4% withdrawal rate")
    print("- Testing withdrawal timing")
    print()
    
    # Test parameters
    starting_value = 1000000
    starting_age = 70
    years = 29  # Full retirement horizon
    simulations = 1  # Just one since no randomness
    withdrawal_rate = 0.04  # 4% only
    
    print(f"🔄 Testing 4% withdrawal with 0% returns")
    
    # Create framework
    framework = EnhancedQOLFramework(
        starting_value=starting_value,
        starting_age=starting_age,
        horizon_years=years,
        n_simulations=simulations,
        qol_phase1_rate=withdrawal_rate,  # All phases same rate
        qol_phase2_rate=withdrawal_rate,
        qol_phase3_rate=withdrawal_rate
    )
    
    # Run with zero return parameters
    framework.run_enhanced_simulation(
        withdrawal_strategy='custom',  
        return_volatility=0.0,  # 0% volatility
        inflation_variability=False,  # No inflation variability
        base_real_return=0.0,  # 0% return *** KEY CHANGE ***
        base_inflation=0.0,  # 0% inflation
        qol_variability=False,  # No QOL variability
        verbose=False
    )
    
    # Get paths
    portfolio_path = framework.simulation_results['portfolio_paths'][0]
    withdrawal_path = framework.simulation_results['withdrawal_paths'][0]
    
    print(f"Starting portfolio: ${starting_value:,}")
    print(f"Final portfolio (Year {years}): ${portfolio_path[-1]:,.0f}")
    print(f"Portfolio depletion: ${starting_value - portfolio_path[-1]:,.0f}")
    print()
    
    # Manual calculation verification
    print("📋 Manual Calculation Check:")
    manual_portfolio = starting_value
    total_withdrawn = 0
    
    for year in range(5):  # Show first 5 years
        # Current method: Apply returns first, then withdraw
        manual_portfolio_after_return = manual_portfolio * 1.0  # 0% return
        withdrawal = manual_portfolio * withdrawal_rate  # Based on beginning value
        manual_portfolio = manual_portfolio_after_return - withdrawal
        total_withdrawn += withdrawal
        
        sim_portfolio = portfolio_path[year + 1]
        sim_withdrawal = withdrawal_path[year]
        
        print(f"Year {year + 1}:")
        print(f"  Manual: Portfolio ${manual_portfolio:,.0f}, Withdrawal ${withdrawal:,.0f}")
        print(f"  Simulation: Portfolio ${sim_portfolio:,.0f}, Withdrawal ${sim_withdrawal:,.0f}")
        print(f"  Match: {'✅' if abs(manual_portfolio - sim_portfolio) < 1 else '❌'}")
    
    print(f"\nTotal withdrawn after 5 years: ${total_withdrawn:,.0f}")
    
    # Create detailed dataframe
    data = []
    cumulative_withdrawn = 0
    
    for year in range(years + 1):
        age = starting_age + year
        portfolio_value = portfolio_path[year]
        
        if year > 0:
            withdrawal = withdrawal_path[year-1]
            cumulative_withdrawn += withdrawal
            withdrawal_pct = (withdrawal / starting_value) * 100
        else:
            withdrawal = 0
            withdrawal_pct = 0
        
        remaining_pct = (portfolio_value / starting_value) * 100
        years_left_at_current_rate = portfolio_value / (starting_value * withdrawal_rate) if withdrawal_rate > 0 else float('inf')
        
        data.append({
            'Year': year,
            'Age': age,
            'Portfolio_Value': portfolio_value,
            'Portfolio_Remaining_Pct': remaining_pct,
            'Annual_Withdrawal': withdrawal,
            'Withdrawal_Pct_of_Original': withdrawal_pct,
            'Cumulative_Withdrawn': cumulative_withdrawn,
            'Cumulative_Withdrawn_Pct': (cumulative_withdrawn / starting_value) * 100,
            'Years_Left_at_Current_Rate': min(years_left_at_current_rate, 99) if years_left_at_current_rate != float('inf') else 99
        })
    
    df = pd.DataFrame(data)
    
    # Display summary
    print(f"\n📊 Portfolio Depletion Analysis:")
    print(f"Years until depletion at 4% rate: {25:.1f} years") # 1/0.04 = 25 years exactly
    print(f"Age when depleted: {starting_age + 25}")
    print(f"Portfolio at Year 25: ${df[df['Year'] == 25]['Portfolio_Value'].iloc[0]:,.0f}")
    
    # Show key milestones
    print(f"\n🎯 Key Milestones:")
    milestones = [5, 10, 15, 20, 25]
    for milestone in milestones:
        if milestone <= years:
            row = df[df['Year'] == milestone].iloc[0]
            print(f"Year {milestone:2d} (Age {row['Age']:2.0f}): ${row['Portfolio_Value']:8,.0f} ({row['Portfolio_Remaining_Pct']:5.1f}% remaining)")
    
    # Export to CSV
    output_path = "output/data/zero_return_withdrawal_analysis.csv"
    df.to_csv(output_path, index=False)
    print(f"\n💾 Complete dataframe saved to: {output_path}")
    
    # Also create a formatted version for easy reading
    formatted_output_path = "output/data/zero_return_analysis_formatted.csv"
    
    # Format currency columns
    df_formatted = df.copy()
    df_formatted['Portfolio_Value'] = df_formatted['Portfolio_Value'].apply(lambda x: f"${x:,.0f}")
    df_formatted['Annual_Withdrawal'] = df_formatted['Annual_Withdrawal'].apply(lambda x: f"${x:,.0f}")
    df_formatted['Cumulative_Withdrawn'] = df_formatted['Cumulative_Withdrawn'].apply(lambda x: f"${x:,.0f}")
    df_formatted['Portfolio_Remaining_Pct'] = df_formatted['Portfolio_Remaining_Pct'].apply(lambda x: f"{x:.1f}%")
    df_formatted['Withdrawal_Pct_of_Original'] = df_formatted['Withdrawal_Pct_of_Original'].apply(lambda x: f"{x:.1f}%")
    df_formatted['Cumulative_Withdrawn_Pct'] = df_formatted['Cumulative_Withdrawn_Pct'].apply(lambda x: f"{x:.1f}%")
    df_formatted['Years_Left_at_Current_Rate'] = df_formatted['Years_Left_at_Current_Rate'].apply(lambda x: f"{x:.1f}")
    
    df_formatted.to_csv(formatted_output_path, index=False)
    print(f"💾 Formatted version saved to: {formatted_output_path}")
    
    # Display first 10 rows
    print(f"\n📋 First 10 Years of Data:")
    display_cols = ['Year', 'Age', 'Portfolio_Value', 'Portfolio_Remaining_Pct', 'Annual_Withdrawal', 'Cumulative_Withdrawn_Pct']
    print(df[display_cols].head(10).to_string(index=False, formatters={
        'Portfolio_Value': '${:,.0f}'.format,
        'Annual_Withdrawal': '${:,.0f}'.format,
        'Portfolio_Remaining_Pct': '{:.1f}%'.format,
        'Cumulative_Withdrawn_Pct': '{:.1f}%'.format
    }))
    
    return df

if __name__ == "__main__":
    run_zero_return_test()