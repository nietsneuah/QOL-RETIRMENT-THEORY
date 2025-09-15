#!/usr/bin/env python3
"""
Real Dollar Comparison - Normalized to Year 1 Purchasing Power

Shows all withdrawal amounts in constant Year 1 dollars to enable
true economic comparison between strategies.
"""

import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from enhanced_qol_framework import EnhancedQOLFramework

def run_real_dollar_comparison():
    """Run comparison showing all values in real Year 1 dollars."""
    
    print("💰 Real Dollar Comparison - Year 1 Purchasing Power")
    print("=" * 60)
    print("All amounts shown in constant Year 1 dollars")
    print("Parameters:")
    print("- Starting portfolio: $1,000,000 (Year 1 dollars)")
    print("- Age: 70-99 (29 years)")
    print("- Inflation: 3% base (with variability)")
    print("- Real returns: 1.5% base (with 15% volatility)")
    print("- Monte Carlo: 1,000 simulations")
    print()
    
    # Simulation parameters
    starting_value = 1000000
    starting_age = 70
    years = 29
    simulations = 1000
    
    # Market parameters
    base_real_return = 0.015  # 1.5% real return
    base_inflation = 0.03     # 3% inflation
    return_volatility = 0.15  # 15% volatility
    
    strategies = {
        'Trinity_4pct': {
            'strategy': 'trinity_4pct',
            'description': 'Trinity Study: Fixed $40K real/year',
            'color': '#1f77b4'
        },
        'QOL_Standard': {
            'strategy': 'hauenstein',
            'phase1_rate': 0.054,
            'phase2_rate': 0.045,
            'phase3_rate': 0.035,
            'description': 'QOL Standard: 5.4%/4.5%/3.5% phases',
            'color': '#ff7f0e'
        },
        'QOL_Enhanced': {
            'strategy': 'hauenstein',
            'phase1_rate': 0.070,
            'phase2_rate': 0.055,
            'phase3_rate': 0.040,
            'description': 'QOL Enhanced: 7.0%/5.5%/4.0% phases',
            'color': '#2ca02c'
        }
    }
    
    results = {}
    all_data = []
    
    print("🔄 Running simulations...")
    
    for name, config in strategies.items():
        print(f"\n📊 Running {name}: {config['description']}")
        
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
            framework = EnhancedQOLFramework(
                starting_value=starting_value,
                starting_age=starting_age,
                horizon_years=years,
                n_simulations=simulations,
                qol_phase1_rate=0.04,
                qol_phase2_rate=0.04,
                qol_phase3_rate=0.04
            )
        
        # Run simulation
        framework.run_enhanced_simulation(
            withdrawal_strategy=config['strategy'],
            return_volatility=return_volatility,
            inflation_variability=True,
            base_real_return=base_real_return,
            base_inflation=base_inflation,
            qol_variability=False,
            verbose=False
        )
        
        # Get raw results
        portfolio_paths = np.array(framework.simulation_results['portfolio_paths'])
        withdrawal_paths = np.array(framework.simulation_results['withdrawal_paths'])
        inflation_paths = np.array(framework.simulation_results['inflation_paths'])
        
        # Calculate real values (deflated to Year 1 purchasing power)
        real_portfolio_paths = np.zeros_like(portfolio_paths)
        real_withdrawal_paths = np.zeros_like(withdrawal_paths)
        
        for sim in range(simulations):
            cumulative_inflation = 1.0
            
            # Year 0 (starting values)
            real_portfolio_paths[sim, 0] = portfolio_paths[sim, 0]  # Year 1 dollars
            
            for year in range(years):
                if year > 0:
                    cumulative_inflation *= (1 + inflation_paths[sim, year-1])
                
                # Convert to real Year 1 dollars
                if year + 1 < portfolio_paths.shape[1]:
                    real_portfolio_paths[sim, year + 1] = portfolio_paths[sim, year + 1] / cumulative_inflation
                
                if year < withdrawal_paths.shape[1]:
                    real_withdrawal_paths[sim, year] = withdrawal_paths[sim, year] / cumulative_inflation
        
        # Store results
        results[name] = {
            'config': config,
            'real_portfolio_paths': real_portfolio_paths,
            'real_withdrawal_paths': real_withdrawal_paths,
            'framework': framework
        }
        
        # Calculate summary statistics in real terms
        final_real_values = real_portfolio_paths[:, -1]
        total_real_withdrawals = np.sum(real_withdrawal_paths, axis=1)
        
        print(f"   Final value (real, mean): ${np.mean(final_real_values):,.0f}")
        print(f"   Final value (real, median): ${np.median(final_real_values):,.0f}")
        print(f"   Total real withdrawals (mean): ${np.mean(total_real_withdrawals):,.0f}")
        print(f"   Depletion rate: {np.mean(final_real_values <= 1000):.1%}")
        
        # Prepare year-by-year data
        for year in range(years + 1):
            age = starting_age + year
            
            if year < real_portfolio_paths.shape[1]:
                portfolio_values = real_portfolio_paths[:, year]
            else:
                portfolio_values = np.zeros(simulations)
            
            if year > 0 and year <= real_withdrawal_paths.shape[1]:
                withdrawal_values = real_withdrawal_paths[:, year-1]
            else:
                withdrawal_values = np.zeros(simulations)
            
            year_data = {
                'Strategy': name,
                'Year': year,
                'Age': age,
                'Real_Portfolio_Mean': np.mean(portfolio_values),
                'Real_Portfolio_Median': np.median(portfolio_values),
                'Real_Portfolio_10th': np.percentile(portfolio_values, 10),
                'Real_Portfolio_90th': np.percentile(portfolio_values, 90),
                'Real_Withdrawal_Mean': np.mean(withdrawal_values),
                'Real_Withdrawal_Median': np.median(withdrawal_values),
                'Survival_Rate': np.mean(portfolio_values > 1000)
            }
            all_data.append(year_data)
    
    # Create comprehensive dataframe
    df = pd.DataFrame(all_data)
    
    # Export results
    output_path = "output/data/real_dollar_comparison.csv"
    df.to_csv(output_path, index=False)
    print(f"\n💾 Real dollar analysis saved to: {output_path}")
    
    # Create comparison summary
    print(f"\n📊 Real Dollar Strategy Summary (Year 1 Purchasing Power):")
    print("=" * 80)
    print(f"{'Strategy':<15} {'Real Final Mean':<15} {'Real Total Income':<17} {'Depletion Rate':<13}")
    print("-" * 80)
    
    for name, result in results.items():
        final_real = np.mean(result['real_portfolio_paths'][:, -1])
        total_real = np.mean(np.sum(result['real_withdrawal_paths'], axis=1))
        depletion = np.mean(result['real_portfolio_paths'][:, -1] <= 1000)
        
        print(f"{name:<15} ${final_real:>12,.0f} ${total_real:>14,.0f} {depletion:>11.1%}")
    
    # Create real dollar charts
    create_real_dollar_charts(df, results)
    
    # Show key insights
    print(f"\n💡 Key Insights (Real Year 1 Dollars):")
    
    trinity_real_final = np.mean(results['Trinity_4pct']['real_portfolio_paths'][:, -1])
    qol_std_real_final = np.mean(results['QOL_Standard']['real_portfolio_paths'][:, -1])
    qol_enh_real_final = np.mean(results['QOL_Enhanced']['real_portfolio_paths'][:, -1])
    
    trinity_real_income = np.mean(np.sum(results['Trinity_4pct']['real_withdrawal_paths'], axis=1))
    qol_std_real_income = np.mean(np.sum(results['QOL_Standard']['real_withdrawal_paths'], axis=1))
    qol_enh_real_income = np.mean(np.sum(results['QOL_Enhanced']['real_withdrawal_paths'], axis=1))
    
    print(f"1. Trinity Study provides constant $40K/year real purchasing power")
    print(f"2. QOL Enhanced provides {qol_enh_real_income/trinity_real_income:.1f}x total real income vs Trinity")
    print(f"3. QOL Standard leaves {qol_std_real_final/trinity_real_final:.1f}x more real wealth vs Trinity")
    print(f"4. All values adjusted for inflation - true economic comparison")
    
    return df, results

def create_real_dollar_charts(df, results):
    """Create charts showing real dollar values."""
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Strategy Comparison - Real Year 1 Dollars', fontsize=16, fontweight='bold')
    
    strategies = df['Strategy'].unique()
    
    # Chart 1: Real Portfolio Values Over Time
    for strategy in strategies:
        strategy_data = df[df['Strategy'] == strategy]
        color = results[strategy]['config']['color']
        
        ax1.plot(strategy_data['Age'], strategy_data['Real_Portfolio_Mean'], 
                label=f'{strategy} (Mean)', color=color, linewidth=2)
        ax1.fill_between(strategy_data['Age'], 
                        strategy_data['Real_Portfolio_10th'], 
                        strategy_data['Real_Portfolio_90th'], 
                        alpha=0.2, color=color)
    
    ax1.set_title('Real Portfolio Values Over Time\n(Year 1 Purchasing Power)')
    ax1.set_xlabel('Age')
    ax1.set_ylabel('Real Portfolio Value (Year 1 $)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))
    
    # Chart 2: Real Withdrawal Amounts Over Time
    for strategy in strategies:
        strategy_data = df[df['Strategy'] == strategy]
        color = results[strategy]['config']['color']
        
        ax2.plot(strategy_data['Age'], strategy_data['Real_Withdrawal_Mean'], 
                label=strategy, color=color, linewidth=2)
    
    ax2.set_title('Real Annual Withdrawals\n(Constant Year 1 Purchasing Power)')
    ax2.set_xlabel('Age')
    ax2.set_ylabel('Real Annual Withdrawal (Year 1 $)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))
    
    # Chart 3: Trinity Study - Nominal vs Real
    trinity_data = df[df['Strategy'] == 'Trinity_4pct']
    ax3.axhline(y=40000, color='blue', linestyle='-', linewidth=2, label='Real Value (Constant $40K)')
    
    # Calculate nominal values for Trinity (for illustration)
    ages = trinity_data['Age'].values
    n_years = len(ages)
    cumulative_inflation = np.cumprod([1.0] + [1.03] * (n_years-1))  # Match data length
    nominal_values = 40000 * cumulative_inflation
    
    ax3.plot(ages, nominal_values, 'red', linestyle='--', linewidth=2, 
            label='Nominal Value (Inflated $)')
    
    ax3.set_title('Trinity Study: Real vs Nominal Withdrawals')
    ax3.set_xlabel('Age')
    ax3.set_ylabel('Withdrawal Amount ($)')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    ax3.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))
    
    # Chart 4: Real Final Value Comparison
    final_data = df[df['Year'] == df['Year'].max()]
    strategies_list = final_data['Strategy'].tolist()
    real_final_means = final_data['Real_Portfolio_Mean'].tolist()
    real_final_medians = final_data['Real_Portfolio_Median'].tolist()
    
    x = np.arange(len(strategies_list))
    width = 0.35
    
    colors = [results[s]['config']['color'] for s in strategies_list]
    bars1 = ax4.bar(x - width/2, real_final_means, width, label='Mean', alpha=0.8, color=colors)
    bars2 = ax4.bar(x + width/2, real_final_medians, width, label='Median', alpha=0.6, color=colors)
    
    ax4.set_title('Final Real Portfolio Values\n(Year 1 Purchasing Power)')
    ax4.set_xlabel('Strategy')
    ax4.set_ylabel('Real Final Value (Year 1 $)')
    ax4.set_xticks(x)
    ax4.set_xticklabels(strategies_list, rotation=45)
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    ax4.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))
    
    # Add value labels
    for bar in bars1:
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height,
                f'${height/1000:.0f}K', ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    plt.savefig("output/charts/real_dollar_comparison.png", dpi=300, bbox_inches='tight')
    print(f"📊 Real dollar charts saved to: output/charts/real_dollar_comparison.png")
    plt.close()

if __name__ == "__main__":
    df, results = run_real_dollar_comparison()