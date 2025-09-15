#!/usr/bin/env python3
"""
Realistic Simulation with Inflation

Parameters:
- $1M starting portfolio
- Age 70-95 (25 years)
- 3% inflation
- 5% CAGR (nominal returns)
- Compare Trinity Study vs QOL strategies
"""

import sys
import os
import pandas as pd
import numpy as np

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from enhanced_qol_framework import EnhancedQOLFramework

def run_realistic_simulation():
    """Run simulation with realistic inflation and returns."""
    
    print("🧪 Realistic Simulation with Inflation")
    print("=" * 50)
    print("Parameters:")
    print("- Starting portfolio: $1,000,000")
    print("- Age: 70-95 (25 years)")
    print("- Inflation: 3% annual")
    print("- CAGR: 5% nominal returns")
    print("- Real returns: ~2% (5% nominal - 3% inflation)")
    print("- 1000 Monte Carlo simulations")
    print()
    
    # Test parameters
    starting_value = 1000000
    starting_age = 70
    years = 25  # Age 70-95
    simulations = 1000
    
    # With 3% inflation and 5% nominal returns, real return ≈ 2%
    nominal_return = 0.05  # 5% CAGR
    inflation_rate = 0.03  # 3% inflation
    real_return = nominal_return - inflation_rate  # ≈2% real return
    
    print(f"💡 Real return calculation: {nominal_return:.1%} nominal - {inflation_rate:.1%} inflation = {real_return:.1%} real")
    print()
    
    strategies = {
        'Trinity_4pct': {
            'strategy': 'trinity_4pct',
            'description': 'Fixed $40K/year, inflation-adjusted'
        },
        'QOL_Standard': {
            'strategy': 'hauenstein',
            'phase1_rate': 0.054,  # 5.4% ages 70-74
            'phase2_rate': 0.045,  # 4.5% ages 75-84  
            'phase3_rate': 0.035,  # 3.5% ages 85+
            'description': 'QOL phases: 5.4%/4.5%/3.5%'
        },
        'QOL_Enhanced': {
            'strategy': 'hauenstein',
            'phase1_rate': 0.070,  # 7.0% ages 70-74
            'phase2_rate': 0.055,  # 5.5% ages 75-84
            'phase3_rate': 0.040,  # 4.0% ages 85+
            'description': 'QOL phases: 7.0%/5.5%/4.0%'
        }
    }
    
    results = {}
    
    for name, config in strategies.items():
        print(f"🔄 Running {name}: {config['description']}")
        
        # Create framework
        if 'phase1_rate' in config:
            framework = EnhancedQOLFramework(
                starting_value=starting_value,
                starting_age=starting_age,
                horizon_years=years,
                n_simulations=simulations,
                qol_phase1_rate=config['phase1_rate'],
                qol_phase2_rate=config['phase2_rate'],
                qol_phase3_rate=config['phase3_rate']
            )
        else:
            # Trinity study - rates don't matter
            framework = EnhancedQOLFramework(
                starting_value=starting_value,
                starting_age=starting_age,
                horizon_years=years,
                n_simulations=simulations,
                qol_phase1_rate=0.04,
                qol_phase2_rate=0.04,
                qol_phase3_rate=0.04
            )
        
        # Run simulation with inflation and volatility
        framework.run_enhanced_simulation(
            withdrawal_strategy=config['strategy'],
            return_volatility=0.15,  # 15% volatility (realistic)
            inflation_variability=True,  # Inflation variability
            base_real_return=real_return,  # 2% real return
            base_inflation=inflation_rate,  # 3% base inflation
            qol_variability=False,  # No QOL variability for cleaner comparison
            verbose=True
        )
        
        # Get results
        analysis = framework.get_comprehensive_analysis()
        portfolio_results = analysis['enhanced_qol_results']['portfolio_analysis']
        
        results[name] = {
            'config': config,
            'analysis': analysis,
            'portfolio_results': portfolio_results,
            'framework': framework
        }
        
        # Print key results
        success_rates = analysis['enhanced_qol_results']['success_rates']
        print(f"   Value at 80: {success_rates['value_at_80']:.1%}")
        print(f"   Final value (mean): ${portfolio_results['final_value_mean']:,.0f}")
        print(f"   Final value (median): ${portfolio_results['final_value_median']:,.0f}")
        print(f"   5th percentile: ${portfolio_results['final_value_percentiles']['5th']:,.0f}")
        print(f"   95th percentile: ${portfolio_results['final_value_percentiles']['95th']:,.0f}")
        print()
    
    # Create summary comparison
    print("📊 Strategy Comparison Summary:")
    print("=" * 80)
    print(f"{'Strategy':<15} {'Value at 80':<12} {'Final Mean':<15} {'Final Median':<15} {'5th %ile':<12}")
    print("-" * 80)
    
    for name, result in results.items():
        portfolio_results = result['portfolio_results']
        success_rates = result['analysis']['enhanced_qol_results']['success_rates']
        value_at_80 = success_rates['value_at_80']
        final_mean = portfolio_results['final_value_mean']
        final_median = portfolio_results['final_value_median'] 
        pct_5th = portfolio_results['final_value_percentiles']['5th']
        
        print(f"{name:<15} {value_at_80:>10.1%} ${final_mean:>12,.0f} ${final_median:>13,.0f} ${pct_5th:>9,.0f}")
    
    # Create detailed year-by-year analysis
    print(f"\n📋 Creating detailed year-by-year analysis...")
    
    data = []
    for year in range(years + 1):
        age = starting_age + year
        row = {'Year': year, 'Age': age}
        
        for name, result in results.items():
            portfolio_paths = np.array(result['framework'].simulation_results['portfolio_paths'])
            withdrawal_paths = np.array(result['framework'].simulation_results['withdrawal_paths'])
            
            # Calculate statistics for this year
            if year < len(portfolio_paths[0]):
                portfolio_values = portfolio_paths[:, year]
                row[f'{name}_Portfolio_Mean'] = np.mean(portfolio_values)
                row[f'{name}_Portfolio_Median'] = np.median(portfolio_values)
                row[f'{name}_Portfolio_10th'] = np.percentile(portfolio_values, 10)
                row[f'{name}_Portfolio_90th'] = np.percentile(portfolio_values, 90)
            
            if year > 0 and year <= len(withdrawal_paths[0]):
                withdrawal_values = withdrawal_paths[:, year-1]
                row[f'{name}_Withdrawal_Mean'] = np.mean(withdrawal_values)
                row[f'{name}_Withdrawal_Median'] = np.median(withdrawal_values)
        
        data.append(row)
    
    df = pd.DataFrame(data)
    
    # Export detailed results
    output_path = "output/data/realistic_inflation_simulation.csv"
    df.to_csv(output_path, index=False)
    print(f"💾 Detailed results saved to: {output_path}")
    
    # Show key years
    print(f"\n🎯 Key Milestones:")
    key_years = [0, 5, 10, 15, 20, 25]
    for year in key_years:
        if year <= years:
            row = df[df['Year'] == year].iloc[0]
            print(f"\nYear {year:2d} (Age {row['Age']:2.0f}):")
            for name in results.keys():
                portfolio_col = f'{name}_Portfolio_Mean'
                if portfolio_col in row:
                    print(f"  {name:<15}: ${row[portfolio_col]:8,.0f}")
    
    # Calculate purchasing power impact
    print(f"\n💰 Inflation Impact Analysis:")
    initial_withdrawal = 40000  # $40K initial
    for year in [5, 10, 15, 20, 25]:
        inflation_factor = (1 + inflation_rate) ** year
        inflated_amount = initial_withdrawal * inflation_factor
        print(f"Year {year:2d}: ${initial_withdrawal:,} in Year 0 = ${inflated_amount:,.0f} needed (purchasing power)")
    
    # Open the results file
    print(f"\n🔍 Opening detailed results...")
    
    return df, results

if __name__ == "__main__":
    run_realistic_simulation()