#!/usr/bin/env python3
"""
Data Export Script for QOL Strategy Analysis

Exports detailed simulation data to CSV tables for analysis.
"""

import sys
import os
import pandas as pd
import numpy as np
from pathlib import Path

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from enhanced_qol_framework import EnhancedQOLFramework

def export_strategy_data(strategy_name, qol_rates, starting_age=70, years=29, simulations=1000):
    """Export detailed data for a specific strategy."""
    
    print(f"\n🔄 Generating data for {strategy_name}...")
    
    # Create framework
    framework = EnhancedQOLFramework(
        starting_value=1000000,
        starting_age=starting_age,
        horizon_years=years,
        n_simulations=simulations,
        qol_phase1_rate=qol_rates[0],
        qol_phase2_rate=qol_rates[1],
        qol_phase3_rate=qol_rates[2]
    )
    
    # Run simulation
    framework.run_enhanced_simulation(verbose=False)
    
    # Extract data
    portfolio_paths = np.array(framework.simulation_results['portfolio_paths'])
    withdrawal_paths = np.array(framework.simulation_results['withdrawal_paths'])
    age_paths = np.array(framework.simulation_results['age_paths'])
    return_paths = np.array(framework.simulation_results['return_paths'])
    
    # Create summary statistics by year
    years_list = []
    ages_list = []
    portfolio_mean = []
    portfolio_median = []
    portfolio_5th = []
    portfolio_95th = []
    withdrawal_mean = []
    withdrawal_median = []
    return_mean = []
    
    for year in range(years + 1):  # +1 because portfolio includes initial value
        age = starting_age + year
        years_list.append(year)
        ages_list.append(age)
        
        # Portfolio statistics
        year_portfolios = portfolio_paths[:, year]
        portfolio_mean.append(np.mean(year_portfolios))
        portfolio_median.append(np.median(year_portfolios))
        portfolio_5th.append(np.percentile(year_portfolios, 5))
        portfolio_95th.append(np.percentile(year_portfolios, 95))
        
        # Withdrawal statistics (only for years 1-29, not year 0)
        if year < years:
            year_withdrawals = withdrawal_paths[:, year]
            withdrawal_mean.append(np.mean(year_withdrawals))
            withdrawal_median.append(np.median(year_withdrawals))
            
            # Return statistics
            year_returns = return_paths[:, year]
            return_mean.append(np.mean(year_returns))
        else:
            withdrawal_mean.append(0)  # No withdrawal in final year
            withdrawal_median.append(0)
            return_mean.append(0)
    
    # Create summary DataFrame
    summary_df = pd.DataFrame({
        'Year': years_list,
        'Age': ages_list,
        'Portfolio_Mean': portfolio_mean,
        'Portfolio_Median': portfolio_median,
        'Portfolio_5th_Percentile': portfolio_5th,
        'Portfolio_95th_Percentile': portfolio_95th,
        'Withdrawal_Mean': withdrawal_mean,
        'Withdrawal_Median': withdrawal_median,
        'Return_Mean': return_mean
    })
    
    # Round to reasonable precision
    for col in ['Portfolio_Mean', 'Portfolio_Median', 'Portfolio_5th_Percentile', 'Portfolio_95th_Percentile']:
        summary_df[col] = summary_df[col].round(0)
    
    for col in ['Withdrawal_Mean', 'Withdrawal_Median']:
        summary_df[col] = summary_df[col].round(0)
    
    summary_df['Return_Mean'] = summary_df['Return_Mean'].round(4)
    
    # Create detailed paths DataFrame (first 10 simulations for examination)
    detailed_data = []
    for sim in range(min(10, simulations)):
        for year in range(years + 1):
            age = starting_age + year
            portfolio_value = portfolio_paths[sim, year]
            withdrawal_amount = withdrawal_paths[sim, year-1] if year > 0 else 0
            annual_return = return_paths[sim, year-1] if year > 0 else 0
            
            # Determine QOL phase
            if age < 75:
                phase = "Phase_1_Peak"
                phase_rate = qol_rates[0]
            elif age < 85:
                phase = "Phase_2_Comfort"
                phase_rate = qol_rates[1]
            else:
                phase = "Phase_3_Care"
                phase_rate = qol_rates[2]
            
            detailed_data.append({
                'Simulation': sim + 1,
                'Year': year,
                'Age': age,
                'Portfolio_Value': round(portfolio_value, 0),
                'Withdrawal_Amount': round(withdrawal_amount, 0),
                'Annual_Return': round(annual_return, 4),
                'QOL_Phase': phase,
                'Phase_Rate': phase_rate
            })
    
    detailed_df = pd.DataFrame(detailed_data)
    
    return summary_df, detailed_df

def main():
    """Export data for all strategies."""
    
    print("📊 QOL Strategy Data Export")
    print("=" * 50)
    
    # Create output directory
    output_dir = Path("output/data")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Define strategies
    strategies = {
        'Traditional_4pct': [0.04, 0.04, 0.04],
        'QOL_Standard': [0.054, 0.045, 0.035],
        'QOL_Enhanced': [0.07, 0.055, 0.04]
    }
    
    # Export data for each strategy
    all_summaries = {}
    
    for strategy_name, rates in strategies.items():
        summary_df, detailed_df = export_strategy_data(strategy_name, rates)
        
        # Save individual strategy files
        summary_path = output_dir / f"{strategy_name}_summary_stats.csv"
        detailed_path = output_dir / f"{strategy_name}_detailed_paths.csv"
        
        summary_df.to_csv(summary_path, index=False)
        detailed_df.to_csv(detailed_path, index=False)
        
        print(f"✅ {strategy_name} data exported:")
        print(f"   Summary: {summary_path}")
        print(f"   Detailed: {detailed_path}")
        
        # Store summary for comparison table
        all_summaries[strategy_name] = summary_df
    
    # Create comparison table
    print(f"\n📋 Creating strategy comparison table...")
    
    comparison_data = []
    for year in range(30):  # 0-29 years
        age = 70 + year
        row = {'Year': year, 'Age': age}
        
        for strategy_name, summary_df in all_summaries.items():
            if year < len(summary_df):
                row[f'{strategy_name}_Portfolio'] = summary_df.iloc[year]['Portfolio_Mean']
                row[f'{strategy_name}_Withdrawal'] = summary_df.iloc[year]['Withdrawal_Mean']
        
        comparison_data.append(row)
    
    comparison_df = pd.DataFrame(comparison_data)
    comparison_path = output_dir / "strategy_comparison_table.csv"
    comparison_df.to_csv(comparison_path, index=False)
    
    print(f"✅ Comparison table: {comparison_path}")
    
    # Show sample of comparison data
    print(f"\n📋 Sample Comparison Data (First 10 Years):")
    print(comparison_df.head(10).to_string(index=False))
    
    print(f"\n🎉 Data export completed!")
    print(f"📁 All files saved to: {output_dir}")

if __name__ == "__main__":
    main()