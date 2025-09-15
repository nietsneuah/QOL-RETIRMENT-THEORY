#!/usr/bin/env python3
"""
Comprehensive QOL Framework Analysis Report - Corrected Implementation

This script generates a complete analysis report comparing the corrected QOL Framework
against the Trinity Study baseline, with proper inflation adjustments and Trinity-based
withdrawal calculations.
"""

import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import seaborn as sns

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from enhanced_qol_framework import EnhancedQOLFramework

# Set style for professional charts
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def generate_comprehensive_report():
    """Generate comprehensive QOL Framework analysis report."""
    
    print("📊 Generating Comprehensive QOL Framework Analysis Report")
    print("=" * 65)
    print("✅ Using corrected Trinity Study foundation")
    print("✅ Proper inflation adjustments")
    print("✅ Real purchasing power analysis")
    print()
    
    # Report parameters
    starting_value = 1000000
    starting_age = 70
    years = 29
    simulations = 1000
    
    # Market parameters (realistic)
    base_real_return = 0.015  # 1.5% real return
    base_inflation = 0.03     # 3% inflation
    return_volatility = 0.15  # 15% volatility
    
    # Strategy configurations
    strategies = {
        'Trinity_4pct': {
            'strategy': 'trinity_4pct',
            'description': 'Trinity Study (4% Rule)',
            'detail': 'Fixed $40,000 real purchasing power annually',
            'color': '#2E86AB',
            'line_style': '-'
        },
        'QOL_Standard': {
            'strategy': 'hauenstein',
            'phase1_rate': 0.054,
            'phase2_rate': 0.045,
            'phase3_rate': 0.035,
            'description': 'QOL Standard Strategy',
            'detail': '135%/112.5%/87.5% of Trinity withdrawals by phase',
            'color': '#A23B72',
            'line_style': '--'
        },
        'QOL_Enhanced': {
            'strategy': 'hauenstein',
            'phase1_rate': 0.070,
            'phase2_rate': 0.055,
            'phase3_rate': 0.040,
            'description': 'QOL Enhanced Strategy',
            'detail': '175%/137.5%/100% of Trinity withdrawals by phase',
            'color': '#F18F01',
            'line_style': '-.'
        }
    }
    
    results = {}
    all_data = []
    
    print("🔄 Running Monte Carlo simulations...")
    
    # Run simulations for each strategy
    for name, config in strategies.items():
        print(f"\n📈 Analyzing {name}: {config['description']}")
        
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
                n_simulations=simulations
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
        
        # Store results
        results[name] = {
            'config': config,
            'framework': framework,
            'portfolio_paths': np.array(framework.simulation_results['portfolio_paths']),
            'withdrawal_paths': np.array(framework.simulation_results['withdrawal_paths']),
            'inflation_paths': np.array(framework.simulation_results['inflation_paths'])
        }
        
        # Calculate real values and summary statistics
        portfolio_paths = results[name]['portfolio_paths']
        withdrawal_paths = results[name]['withdrawal_paths']
        inflation_paths = results[name]['inflation_paths']
        
        # Convert to real dollars
        real_portfolio_paths = np.zeros_like(portfolio_paths)
        real_withdrawal_paths = np.zeros_like(withdrawal_paths)
        
        for sim in range(simulations):
            cumulative_inflation = 1.0
            real_portfolio_paths[sim, 0] = portfolio_paths[sim, 0]
            
            for year in range(years):
                if year > 0:
                    cumulative_inflation *= (1 + inflation_paths[sim, year-1])
                
                # Convert to real dollars
                if year + 1 < portfolio_paths.shape[1]:
                    real_portfolio_paths[sim, year + 1] = portfolio_paths[sim, year + 1] / cumulative_inflation
                
                if year < withdrawal_paths.shape[1]:
                    real_withdrawal_paths[sim, year] = withdrawal_paths[sim, year] / cumulative_inflation
        
        results[name]['real_portfolio_paths'] = real_portfolio_paths
        results[name]['real_withdrawal_paths'] = real_withdrawal_paths
        
        # Calculate key metrics
        final_real_values = real_portfolio_paths[:, -1]
        total_real_withdrawals = np.sum(real_withdrawal_paths, axis=1)
        
        metrics = {
            'final_value_mean': np.mean(final_real_values),
            'final_value_median': np.median(final_real_values),
            'final_value_10th': np.percentile(final_real_values, 10),
            'final_value_90th': np.percentile(final_real_values, 90),
            'total_withdrawals_mean': np.mean(total_real_withdrawals),
            'total_withdrawals_median': np.median(total_real_withdrawals),
            'depletion_rate': np.mean(final_real_values <= 1000),
            'success_rate': np.mean(final_real_values > 100000)
        }
        
        results[name]['metrics'] = metrics
        
        print(f"   Final value (real, mean): ${metrics['final_value_mean']:,.0f}")
        print(f"   Total withdrawals (real, mean): ${metrics['total_withdrawals_mean']:,.0f}")
        print(f"   Depletion rate: {metrics['depletion_rate']:.1%}")
        print(f"   Success rate (>$100K): {metrics['success_rate']:.1%}")
        
        # Prepare detailed year-by-year data
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
                'Portfolio_Mean': np.mean(portfolio_values),
                'Portfolio_Median': np.median(portfolio_values),
                'Portfolio_10th': np.percentile(portfolio_values, 10),
                'Portfolio_90th': np.percentile(portfolio_values, 90),
                'Withdrawal_Mean': np.mean(withdrawal_values),
                'Withdrawal_Median': np.median(withdrawal_values),
                'Survival_Rate': np.mean(portfolio_values > 1000)
            }
            all_data.append(year_data)
    
    # Create comprehensive dataframe
    df = pd.DataFrame(all_data)
    
    # Save detailed data
    output_path = "output/data/comprehensive_qol_analysis.csv"
    df.to_csv(output_path, index=False)
    print(f"\n💾 Detailed analysis data saved to: {output_path}")
    
    # Generate comprehensive visualizations
    create_comprehensive_charts(df, results)
    
    # Generate summary report
    generate_summary_report(results)
    
    # Generate detailed comparison tables
    generate_comparison_tables(results)
    
    print(f"\n✅ Comprehensive QOL Framework Analysis Complete!")
    print(f"📊 Charts saved to: output/charts/")
    print(f"📋 Reports saved to: output/reports/")
    
    return df, results

def create_comprehensive_charts(df, results):
    """Create comprehensive visualization suite."""
    
    print(f"\n📊 Creating comprehensive chart suite...")
    
    # Create figure with multiple subplots
    fig = plt.figure(figsize=(20, 16))
    
    # Chart 1: Portfolio Evolution Over Time
    ax1 = plt.subplot(3, 3, 1)
    for strategy in df['Strategy'].unique():
        strategy_data = df[df['Strategy'] == strategy]
        config = results[strategy]['config']
        
        ax1.plot(strategy_data['Age'], strategy_data['Portfolio_Mean'], 
                label=config['description'], color=config['color'], 
                linewidth=2.5, linestyle=config['line_style'])
        ax1.fill_between(strategy_data['Age'], 
                        strategy_data['Portfolio_10th'], 
                        strategy_data['Portfolio_90th'], 
                        alpha=0.2, color=config['color'])
    
    ax1.set_title('Real Portfolio Values Over Time\n(Year 1 Purchasing Power)', fontweight='bold')
    ax1.set_xlabel('Age')
    ax1.set_ylabel('Real Portfolio Value ($)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))
    
    # Chart 2: Annual Withdrawal Patterns
    ax2 = plt.subplot(3, 3, 2)
    for strategy in df['Strategy'].unique():
        strategy_data = df[df['Strategy'] == strategy]
        config = results[strategy]['config']
        
        ax2.plot(strategy_data['Age'], strategy_data['Withdrawal_Mean'], 
                label=config['description'], color=config['color'], 
                linewidth=2.5, linestyle=config['line_style'])
    
    ax2.set_title('Annual Real Withdrawals\n(Constant Year 1 Purchasing Power)', fontweight='bold')
    ax2.set_xlabel('Age')
    ax2.set_ylabel('Real Annual Withdrawal ($)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))
    
    # Chart 3: Survival Probability
    ax3 = plt.subplot(3, 3, 3)
    for strategy in df['Strategy'].unique():
        strategy_data = df[df['Strategy'] == strategy]
        config = results[strategy]['config']
        
        ax3.plot(strategy_data['Age'], strategy_data['Survival_Rate'], 
                label=config['description'], color=config['color'], 
                linewidth=2.5, linestyle=config['line_style'])
    
    ax3.set_title('Portfolio Survival Probability', fontweight='bold')
    ax3.set_xlabel('Age')
    ax3.set_ylabel('Survival Probability')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    ax3.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:.0%}'))
    
    # Chart 4: Final Value Distributions
    ax4 = plt.subplot(3, 3, 4)
    final_data = df[df['Year'] == df['Year'].max()]
    strategies_list = final_data['Strategy'].tolist()
    final_means = final_data['Portfolio_Mean'].tolist()
    final_medians = final_data['Portfolio_Median'].tolist()
    
    x = np.arange(len(strategies_list))
    width = 0.35
    
    colors = [results[s]['config']['color'] for s in strategies_list]
    bars1 = ax4.bar(x - width/2, final_means, width, label='Mean', alpha=0.8, color=colors)
    bars2 = ax4.bar(x + width/2, final_medians, width, label='Median', alpha=0.6, color=colors)
    
    ax4.set_title('Final Real Portfolio Values\n(Year 1 Purchasing Power)', fontweight='bold')
    ax4.set_xlabel('Strategy')
    ax4.set_ylabel('Final Value ($)')
    ax4.set_xticks(x)
    ax4.set_xticklabels([s.replace('_', ' ') for s in strategies_list], rotation=45)
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    ax4.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))
    
    # Add value labels on bars
    for bar in bars1:
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height,
                f'${height/1000:.0f}K', ha='center', va='bottom', fontsize=9)
    
    # Chart 5: Total Income Comparison
    ax5 = plt.subplot(3, 3, 5)
    total_incomes = [results[s]['metrics']['total_withdrawals_mean'] for s in strategies_list]
    
    bars = ax5.bar(strategies_list, total_incomes, color=colors, alpha=0.8)
    ax5.set_title('Total Real Lifetime Income\n(29-Year Period)', fontweight='bold')
    ax5.set_xlabel('Strategy')
    ax5.set_ylabel('Total Real Income ($)')
    ax5.set_xticklabels([s.replace('_', ' ') for s in strategies_list], rotation=45)
    ax5.grid(True, alpha=0.3)
    ax5.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        ax5.text(bar.get_x() + bar.get_width()/2., height,
                f'${height/1000:.0f}K', ha='center', va='bottom', fontsize=9)
    
    # Chart 6: Risk Metrics Comparison
    ax6 = plt.subplot(3, 3, 6)
    depletion_rates = [results[s]['metrics']['depletion_rate'] for s in strategies_list]
    
    bars = ax6.bar(strategies_list, depletion_rates, color=colors, alpha=0.8)
    ax6.set_title('Portfolio Depletion Risk\n(Probability of Running Out)', fontweight='bold')
    ax6.set_xlabel('Strategy')
    ax6.set_ylabel('Depletion Rate')
    ax6.set_xticklabels([s.replace('_', ' ') for s in strategies_list], rotation=45)
    ax6.grid(True, alpha=0.3)
    ax6.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:.0%}'))
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        ax6.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1%}', ha='center', va='bottom', fontsize=9)
    
    # Chart 7: QOL Withdrawal Pattern Detail
    ax7 = plt.subplot(3, 3, 7)
    
    # Show Trinity baseline and QOL multipliers
    ages = np.arange(70, 99)
    trinity_base = 40000 * np.ones(len(ages))  # Constant $40K real
    
    ax7.axhline(y=40000, color=results['Trinity_4pct']['config']['color'], 
               linestyle='-', linewidth=2, label='Trinity Baseline ($40K real)')
    
    # QOL Standard pattern
    qol_standard_pattern = []
    for age in ages:
        year = age - 70
        if year < 10:
            multiplier = 0.054 / 0.04  # 1.35x
        elif year < 20:
            multiplier = 0.045 / 0.04  # 1.125x
        else:
            multiplier = 0.035 / 0.04  # 0.875x
        qol_standard_pattern.append(40000 * multiplier)
    
    ax7.plot(ages, qol_standard_pattern, color=results['QOL_Standard']['config']['color'],
            linestyle='--', linewidth=2, label='QOL Standard Pattern')
    
    # QOL Enhanced pattern  
    qol_enhanced_pattern = []
    for age in ages:
        year = age - 70
        if year < 10:
            multiplier = 0.070 / 0.04  # 1.75x
        elif year < 20:
            multiplier = 0.055 / 0.04  # 1.375x
        else:
            multiplier = 0.040 / 0.04  # 1.0x
        qol_enhanced_pattern.append(40000 * multiplier)
    
    ax7.plot(ages, qol_enhanced_pattern, color=results['QOL_Enhanced']['config']['color'],
            linestyle='-.', linewidth=2, label='QOL Enhanced Pattern')
    
    ax7.set_title('QOL Withdrawal Patterns\n(Trinity Baseline × QOL Multipliers)', fontweight='bold')
    ax7.set_xlabel('Age')
    ax7.set_ylabel('Target Real Withdrawal ($)')
    ax7.legend()
    ax7.grid(True, alpha=0.3)
    ax7.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))
    
    # Chart 8: Cumulative Income Over Time
    ax8 = plt.subplot(3, 3, 8)
    for strategy in df['Strategy'].unique():
        strategy_data = df[df['Strategy'] == strategy]
        config = results[strategy]['config']
        
        # Calculate cumulative withdrawals
        cumulative_withdrawals = strategy_data['Withdrawal_Mean'].cumsum()
        
        ax8.plot(strategy_data['Age'][1:], cumulative_withdrawals[1:], 
                label=config['description'], color=config['color'], 
                linewidth=2.5, linestyle=config['line_style'])
    
    ax8.set_title('Cumulative Real Income Over Time', fontweight='bold')
    ax8.set_xlabel('Age')
    ax8.set_ylabel('Cumulative Real Income ($)')
    ax8.legend()
    ax8.grid(True, alpha=0.3)
    ax8.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))
    
    # Chart 9: Risk-Return Scatter
    ax9 = plt.subplot(3, 3, 9)
    
    total_incomes = [results[s]['metrics']['total_withdrawals_mean'] for s in strategies_list]
    depletion_rates = [results[s]['metrics']['depletion_rate'] for s in strategies_list]
    colors_list = [results[s]['config']['color'] for s in strategies_list]
    
    scatter = ax9.scatter(depletion_rates, total_incomes, c=colors_list, s=200, alpha=0.8)
    
    # Add strategy labels
    for i, strategy in enumerate(strategies_list):
        ax9.annotate(strategy.replace('_', ' '), 
                    (depletion_rates[i], total_incomes[i]),
                    xytext=(10, 10), textcoords='offset points',
                    fontsize=9, ha='left')
    
    ax9.set_title('Risk vs. Return Trade-off\n(Income vs. Depletion Risk)', fontweight='bold')
    ax9.set_xlabel('Depletion Rate')
    ax9.set_ylabel('Total Real Income ($)')
    ax9.grid(True, alpha=0.3)
    ax9.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:.0%}'))
    ax9.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))
    
    plt.tight_layout()
    plt.savefig("output/charts/comprehensive_qol_analysis.png", dpi=300, bbox_inches='tight')
    print(f"   📊 Main analysis chart saved")
    plt.close()

def generate_summary_report(results):
    """Generate executive summary report."""
    
    print(f"\n📋 Generating executive summary report...")
    
    report_date = datetime.now().strftime("%B %d, %Y")
    
    summary_text = f"""
# QOL Framework Analysis Report - Corrected Implementation
**Generated on {report_date}**

## Executive Summary

This analysis compares the corrected Quality of Life (QOL) retirement withdrawal framework against the traditional Trinity Study 4% rule. The QOL framework has been corrected to use Trinity Study as its foundation, applying QOL multipliers to redistribute withdrawals across retirement phases.

## Key Findings

### Strategy Performance Summary (Real Year 1 Dollars)

| Strategy | Total Real Income | Final Portfolio Value | Depletion Rate | Success Rate |
|----------|-------------------|----------------------|----------------|--------------|"""
    
    for name, result in results.items():
        metrics = result['metrics']
        description = result['config']['description']
        summary_text += f"""
| {description} | ${metrics['total_withdrawals_mean']:,.0f} | ${metrics['final_value_mean']:,.0f} | {metrics['depletion_rate']:.1%} | {metrics['success_rate']:.1%} |"""
    
    summary_text += f"""

### Corrected Implementation Details

**Trinity Study Foundation**: All QOL strategies now correctly use Trinity Study's 4% of initial portfolio (inflation-adjusted) as the base withdrawal amount.

**QOL Multipliers**: 
- **QOL Standard**: 135%/112.5%/87.5% of Trinity withdrawals across three phases
- **QOL Enhanced**: 175%/137.5%/100% of Trinity withdrawals across three phases

**Phase Definitions**:
- Phase 1 (Ages 70-79): Peak enjoyment years - higher withdrawals
- Phase 2 (Ages 80-89): Comfortable years - moderate withdrawals  
- Phase 3 (Ages 90-99): Care years - lower withdrawals

### Risk-Return Analysis

The corrected analysis reveals the true trade-offs:

1. **Higher Income, Higher Risk**: QOL strategies provide more total lifetime income but with significantly higher portfolio depletion rates
2. **Front-Loading Trade-off**: Early retirement years receive higher withdrawals at the cost of portfolio longevity
3. **Trinity Study Conservatism**: The traditional 4% rule shows its conservative nature with better portfolio preservation

### Methodology Corrections Applied

1. **Trinity Study Inflation Fix**: Corrected inflation timing so Year 1 withdrawal is exactly $40,000 real
2. **QOL Framework Rebase**: Changed from percentage-of-current-balance to Trinity-Study-with-multipliers approach
3. **Consistent Comparison**: Both strategies now use identical inflation-adjusted foundation for meaningful comparison

### Investment Assumptions

- **Starting Portfolio**: $1,000,000
- **Real Returns**: 1.5% annually (conservative assumption)
- **Inflation**: 3.0% annually with variability
- **Return Volatility**: 15% (realistic market conditions)
- **Simulation Count**: 1,000 Monte Carlo paths
- **Time Horizon**: 29 years (ages 70-99)

### Implications for Retirement Planning

The corrected QOL framework represents a **risk preference trade-off** rather than a superior strategy:

- **Choose QOL** if you prioritize early retirement enjoyment and are comfortable with higher depletion risk
- **Choose Trinity Study** if you prioritize portfolio preservation and steady, predictable withdrawals

Both strategies are now mathematically sound and provide meaningful comparison for retirement planning decisions.

---
*This analysis uses Monte Carlo simulation with realistic market assumptions. Past performance does not guarantee future results. Consult with financial professionals for personalized retirement planning advice.*
"""
    
    # Save summary report
    with open("output/reports/qol_framework_summary_report.md", "w") as f:
        f.write(summary_text)
    
    print(f"   📋 Executive summary saved")

def generate_comparison_tables(results):
    """Generate detailed comparison tables."""
    
    print(f"\n📊 Generating detailed comparison tables...")
    
    # Strategy comparison table
    comparison_data = []
    for name, result in results.items():
        metrics = result['metrics']
        config = result['config']
        
        if 'phase1_rate' in config:
            phase_details = f"P1: {config['phase1_rate']:.1%}, P2: {config['phase2_rate']:.1%}, P3: {config['phase3_rate']:.1%}"
            multipliers = f"{config['phase1_rate']/0.04:.2f}x / {config['phase2_rate']/0.04:.2f}x / {config['phase3_rate']/0.04:.2f}x"
        else:
            phase_details = "Fixed 4% of initial portfolio"
            multipliers = "1.00x / 1.00x / 1.00x"
        
        comparison_data.append({
            'Strategy': config['description'],
            'Implementation': 'Trinity Base + QOL Multipliers' if name != 'Trinity_4pct' else 'Fixed Real Withdrawal',
            'Phase_Rates': phase_details,
            'Trinity_Multipliers': multipliers,
            'Total_Real_Income': f"${metrics['total_withdrawals_mean']:,.0f}",
            'Final_Value_Mean': f"${metrics['final_value_mean']:,.0f}",
            'Final_Value_Median': f"${metrics['final_value_median']:,.0f}",
            'Depletion_Rate': f"{metrics['depletion_rate']:.1%}",
            'Success_Rate_100K': f"{metrics['success_rate']:.1%}"
        })
    
    comparison_df = pd.DataFrame(comparison_data)
    comparison_df.to_csv("output/data/strategy_comparison_table.csv", index=False)
    
    # Risk analysis table
    risk_data = []
    trinity_income = results['Trinity_4pct']['metrics']['total_withdrawals_mean']
    trinity_depletion = results['Trinity_4pct']['metrics']['depletion_rate']
    
    for name, result in results.items():
        metrics = result['metrics']
        config = result['config']
        
        income_vs_trinity = metrics['total_withdrawals_mean'] / trinity_income
        depletion_vs_trinity = metrics['depletion_rate'] - trinity_depletion
        
        risk_data.append({
            'Strategy': config['description'],
            'Total_Income_vs_Trinity': f"{income_vs_trinity:.2f}x",
            'Income_Premium': f"${metrics['total_withdrawals_mean'] - trinity_income:,.0f}",
            'Depletion_vs_Trinity': f"{depletion_vs_trinity:+.1%}",
            'Risk_Adjusted_Return': f"{income_vs_trinity / (1 + metrics['depletion_rate']):.2f}",
            'Sharpe_Analog': f"{(income_vs_trinity - 1) / (metrics['depletion_rate'] + 0.01):.2f}"
        })
    
    risk_df = pd.DataFrame(risk_data)
    risk_df.to_csv("output/data/risk_analysis_table.csv", index=False)
    
    print(f"   📊 Comparison tables saved")

if __name__ == "__main__":
    # Ensure output directories exist
    os.makedirs("output/charts", exist_ok=True)
    os.makedirs("output/data", exist_ok=True)
    os.makedirs("output/reports", exist_ok=True)
    
    # Generate comprehensive report
    df, results = generate_comprehensive_report()