#!/usr/bin/env python3
"""
Fresh Comprehensive Strategy Comparison

Compares three withdrawal strategies:
1. Trinity Study 4% (traditional approach)
2. QOL Standard (5.4%/4.5%/3.5%)
3. QOL Enhanced (7.0%/5.5%/4.0%)

With realistic market conditions and full analysis.
"""

import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from enhanced_qol_framework import EnhancedQOLFramework

def run_comprehensive_comparison():
    """Run comprehensive strategy comparison with full analysis."""
    
    print("🚀 Fresh Comprehensive Strategy Comparison")
    print("=" * 60)
    print("Parameters:")
    print("- Starting portfolio: $1,000,000")
    print("- Age: 70-99 (29 years)")
    print("- Inflation: 3% base (with variability)")
    print("- Real returns: 1.5% base (with 15% volatility)")
    print("- Monte Carlo: 1,000 simulations")
    print("- Trinity Study: Fixed $40K/year, inflation-adjusted")
    print("- QOL Standard: 5.4%/4.5%/3.5% phases")
    print("- QOL Enhanced: 7.0%/5.5%/4.0% phases")
    print()
    
    # Simulation parameters
    starting_value = 1000000
    starting_age = 70
    years = 29  # Age 70-99
    simulations = 1000
    
    # Market parameters (realistic)
    base_real_return = 0.015  # 1.5% real return
    base_inflation = 0.03     # 3% inflation
    return_volatility = 0.15  # 15% volatility
    
    strategies = {
        'Trinity_4pct': {
            'strategy': 'trinity_4pct',
            'description': 'Trinity Study: Fixed $40K/year, inflation-adjusted',
            'color': '#1f77b4'  # Blue
        },
        'QOL_Standard': {
            'strategy': 'hauenstein',
            'phase1_rate': 0.054,  # 5.4% ages 70-74
            'phase2_rate': 0.045,  # 4.5% ages 75-84  
            'phase3_rate': 0.035,  # 3.5% ages 85+
            'description': 'QOL Standard: 5.4%/4.5%/3.5% phases',
            'color': '#ff7f0e'  # Orange
        },
        'QOL_Enhanced': {
            'strategy': 'hauenstein',
            'phase1_rate': 0.070,  # 7.0% ages 70-74
            'phase2_rate': 0.055,  # 5.5% ages 75-84
            'phase3_rate': 0.040,  # 4.0% ages 85+
            'description': 'QOL Enhanced: 7.0%/5.5%/4.0% phases',
            'color': '#2ca02c'  # Green
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
            # Trinity study
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
            qol_variability=False,  # Keep QOL constant for cleaner comparison
            verbose=True
        )
        
        # Get comprehensive analysis
        analysis = framework.get_comprehensive_analysis()
        portfolio_results = analysis['enhanced_qol_results']['portfolio_analysis']
        success_rates = analysis['enhanced_qol_results']['success_rates']
        withdrawal_analysis = analysis['enhanced_qol_results']['withdrawal_analysis']
        
        # Store results
        results[name] = {
            'config': config,
            'analysis': analysis,
            'portfolio_results': portfolio_results,
            'success_rates': success_rates,
            'withdrawal_analysis': withdrawal_analysis,
            'framework': framework
        }
        
        # Calculate additional metrics
        portfolio_paths = np.array(framework.simulation_results['portfolio_paths'])
        withdrawal_paths = np.array(framework.simulation_results['withdrawal_paths'])
        
        # Depletion analysis
        final_values = portfolio_paths[:, -1]
        depleted_count = np.sum(final_values <= 1000)  # Consider depleted if < $1K
        depletion_rate = depleted_count / simulations
        
        # Print key results
        print(f"   Final value (mean): ${portfolio_results['final_value_mean']:,.0f}")
        print(f"   Final value (median): ${portfolio_results['final_value_median']:,.0f}")
        print(f"   Depletion rate: {depletion_rate:.1%}")
        print(f"   Value at age 80: {success_rates['value_at_80']:.1%}")
        print(f"   5th percentile: ${portfolio_results['final_value_percentiles']['5th']:,.0f}")
        print(f"   95th percentile: ${portfolio_results['final_value_percentiles']['95th']:,.0f}")
        print(f"   Total withdrawals (mean): ${withdrawal_analysis['total_withdrawals_mean']:,.0f}")
        
        # Store summary data
        results[name]['summary'] = {
            'depletion_rate': depletion_rate,
            'depleted_count': depleted_count
        }
        
        # Prepare data for year-by-year analysis
        for year in range(years + 1):
            age = starting_age + year
            portfolio_values = portfolio_paths[:, year]
            
            if year > 0 and year <= len(withdrawal_paths[0]):
                withdrawal_values = withdrawal_paths[:, year-1]
            else:
                withdrawal_values = np.zeros(simulations)
            
            year_data = {
                'Strategy': name,
                'Year': year,
                'Age': age,
                'Portfolio_Mean': np.mean(portfolio_values),
                'Portfolio_Median': np.median(portfolio_values),
                'Portfolio_10th': np.percentile(portfolio_values, 10),
                'Portfolio_90th': np.percentile(portfolio_values, 90),
                'Portfolio_5th': np.percentile(portfolio_values, 5),
                'Portfolio_95th': np.percentile(portfolio_values, 95),
                'Withdrawal_Mean': np.mean(withdrawal_values),
                'Withdrawal_Median': np.median(withdrawal_values),
                'Survival_Rate': np.mean(portfolio_values > 1000)  # % with >$1K
            }
            all_data.append(year_data)
    
    # Create comprehensive dataframe
    df = pd.DataFrame(all_data)
    
    # Export detailed results
    output_path = "output/data/comprehensive_strategy_comparison.csv"
    df.to_csv(output_path, index=False)
    print(f"\n💾 Detailed year-by-year results saved to: {output_path}")
    
    # Create summary comparison table
    print(f"\n📊 Strategy Comparison Summary:")
    print("=" * 100)
    print(f"{'Strategy':<15} {'Final Mean':<12} {'Final Median':<13} {'Depletion':<10} {'Age 80':<8} {'Total Income':<12}")
    print("-" * 100)
    
    for name, result in results.items():
        portfolio_results = result['portfolio_results']
        success_rates = result['success_rates']
        withdrawal_analysis = result['withdrawal_analysis']
        depletion_rate = result['summary']['depletion_rate']
        
        print(f"{name:<15} ${portfolio_results['final_value_mean']:>9,.0f} "
              f"${portfolio_results['final_value_median']:>10,.0f} "
              f"{depletion_rate:>8.1%} "
              f"{success_rates['value_at_80']:>6.1%} "
              f"${withdrawal_analysis['total_withdrawals_mean']:>9,.0f}")
    
    # Create visualization
    create_comparison_charts(df, results, output_path="output/charts/strategy_comparison.png")
    
    # Create summary statistics
    create_summary_report(results, df, output_path="output/reports/strategy_comparison_summary.txt")
    
    print(f"\n🎯 Key Findings:")
    
    # Find best performers
    best_survival = max(results.items(), key=lambda x: x[1]['success_rates']['value_at_80'])
    lowest_depletion = min(results.items(), key=lambda x: x[1]['summary']['depletion_rate'])
    highest_income = max(results.items(), key=lambda x: x[1]['withdrawal_analysis']['total_withdrawals_mean'])
    
    print(f"📈 Best survival to age 80: {best_survival[0]} ({best_survival[1]['success_rates']['value_at_80']:.1%})")
    print(f"🛡️  Lowest depletion rate: {lowest_depletion[0]} ({lowest_depletion[1]['summary']['depletion_rate']:.1%})")
    print(f"💰 Highest total income: {highest_income[0]} (${highest_income[1]['withdrawal_analysis']['total_withdrawals_mean']:,.0f})")
    
    return df, results

def create_comparison_charts(df, results, output_path):
    """Create comprehensive comparison charts."""
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('QOL Retirement Strategy Comparison', fontsize=16, fontweight='bold')
    
    strategies = df['Strategy'].unique()
    
    # Chart 1: Portfolio Values Over Time
    for strategy in strategies:
        strategy_data = df[df['Strategy'] == strategy]
        color = results[strategy]['config']['color']
        
        ax1.plot(strategy_data['Age'], strategy_data['Portfolio_Mean'], 
                label=f'{strategy} (Mean)', color=color, linewidth=2)
        ax1.fill_between(strategy_data['Age'], 
                        strategy_data['Portfolio_10th'], 
                        strategy_data['Portfolio_90th'], 
                        alpha=0.2, color=color)
    
    ax1.set_title('Portfolio Values Over Time\n(Mean with 10th-90th percentile bands)')
    ax1.set_xlabel('Age')
    ax1.set_ylabel('Portfolio Value ($)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))
    
    # Chart 2: Withdrawal Amounts Over Time
    for strategy in strategies:
        strategy_data = df[df['Strategy'] == strategy]
        color = results[strategy]['config']['color']
        
        ax2.plot(strategy_data['Age'], strategy_data['Withdrawal_Mean'], 
                label=strategy, color=color, linewidth=2)
    
    ax2.set_title('Average Annual Withdrawals')
    ax2.set_xlabel('Age')
    ax2.set_ylabel('Annual Withdrawal ($)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))
    
    # Chart 3: Survival Rates Over Time
    for strategy in strategies:
        strategy_data = df[df['Strategy'] == strategy]
        color = results[strategy]['config']['color']
        
        ax3.plot(strategy_data['Age'], strategy_data['Survival_Rate'] * 100, 
                label=strategy, color=color, linewidth=2)
    
    ax3.set_title('Portfolio Survival Rate\n(% with portfolio > $1,000)')
    ax3.set_xlabel('Age')
    ax3.set_ylabel('Survival Rate (%)')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    ax3.set_ylim(0, 105)
    
    # Chart 4: Final Value Distribution
    final_data = df[df['Year'] == df['Year'].max()]
    strategies_list = final_data['Strategy'].tolist()
    final_means = final_data['Portfolio_Mean'].tolist()
    final_medians = final_data['Portfolio_Median'].tolist()
    
    x = np.arange(len(strategies_list))
    width = 0.35
    
    bars1 = ax4.bar(x - width/2, final_means, width, label='Mean', alpha=0.8)
    bars2 = ax4.bar(x + width/2, final_medians, width, label='Median', alpha=0.8)
    
    ax4.set_title('Final Portfolio Values (Age 99)')
    ax4.set_xlabel('Strategy')
    ax4.set_ylabel('Final Value ($)')
    ax4.set_xticks(x)
    ax4.set_xticklabels(strategies_list, rotation=45)
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    ax4.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))
    
    # Add value labels on bars
    for bar in bars1:
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height,
                f'${height/1000:.0f}K', ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"📊 Charts saved to: {output_path}")
    plt.close()

def create_summary_report(results, df, output_path):
    """Create text summary report."""
    
    with open(output_path, 'w') as f:
        f.write("QOL RETIREMENT STRATEGY COMPARISON REPORT\n")
        f.write("=" * 50 + "\n\n")
        
        f.write("SIMULATION PARAMETERS:\n")
        f.write("- Starting Portfolio: $1,000,000\n")
        f.write("- Age Range: 70-99 (29 years)\n")
        f.write("- Real Returns: 1.5% base with 15% volatility\n")
        f.write("- Inflation: 3% base with variability\n")
        f.write("- Monte Carlo Simulations: 1,000\n\n")
        
        f.write("STRATEGY RESULTS:\n")
        f.write("-" * 30 + "\n")
        
        for name, result in results.items():
            portfolio_results = result['portfolio_results']
            success_rates = result['success_rates']
            withdrawal_analysis = result['withdrawal_analysis']
            depletion_rate = result['summary']['depletion_rate']
            
            f.write(f"\n{name}:\n")
            f.write(f"  Description: {result['config']['description']}\n")
            f.write(f"  Final Value (Mean): ${portfolio_results['final_value_mean']:,.0f}\n")
            f.write(f"  Final Value (Median): ${portfolio_results['final_value_median']:,.0f}\n")
            f.write(f"  Depletion Rate: {depletion_rate:.1%}\n")
            f.write(f"  Survival to Age 80: {success_rates['value_at_80']:.1%}\n")
            f.write(f"  Total Lifetime Income: ${withdrawal_analysis['total_withdrawals_mean']:,.0f}\n")
            f.write(f"  5th Percentile Final: ${portfolio_results['final_value_percentiles']['5th']:,.0f}\n")
            f.write(f"  95th Percentile Final: ${portfolio_results['final_value_percentiles']['95th']:,.0f}\n")
        
        # Add key insights
        f.write(f"\nKEY INSIGHTS:\n")
        f.write("-" * 15 + "\n")
        
        # Compare strategies
        trinity_depletion = results['Trinity_4pct']['summary']['depletion_rate']
        qol_std_depletion = results['QOL_Standard']['summary']['depletion_rate']
        qol_enh_depletion = results['QOL_Enhanced']['summary']['depletion_rate']
        
        f.write(f"- Trinity Study shows {trinity_depletion:.1%} depletion rate\n")
        f.write(f"- QOL Standard shows {qol_std_depletion:.1%} depletion rate\n")
        f.write(f"- QOL Enhanced shows {qol_enh_depletion:.1%} depletion rate\n")
        
        if qol_std_depletion < trinity_depletion:
            improvement = trinity_depletion - qol_std_depletion
            f.write(f"- QOL Standard reduces depletion risk by {improvement:.1%} vs Trinity Study\n")
        
        # Income comparison
        trinity_income = results['Trinity_4pct']['withdrawal_analysis']['total_withdrawals_mean']
        qol_std_income = results['QOL_Standard']['withdrawal_analysis']['total_withdrawals_mean']
        qol_enh_income = results['QOL_Enhanced']['withdrawal_analysis']['total_withdrawals_mean']
        
        if qol_enh_income > trinity_income:
            income_boost = (qol_enh_income - trinity_income) / trinity_income * 100
            f.write(f"- QOL Enhanced provides {income_boost:.1f}% more lifetime income than Trinity Study\n")
    
    print(f"📄 Summary report saved to: {output_path}")

if __name__ == "__main__":
    df, results = run_comprehensive_comparison()