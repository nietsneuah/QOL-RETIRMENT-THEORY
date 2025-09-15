"""
MULTI-PORTFOLIO QOL SIMULATION ANALYSIS

This script runs QOL vs Trinity Study comparisons across multiple portfolio
risk strategies to understand how asset allocation affects the enjoyment-risk
trade-off and optimal strategy selection.

Portfolio Strategies Tested:
1. Conservative (30/70 stocks/bonds): 3.5% real return, 12% volatility
2. Moderate Conservative (50/50): 4.5% real return, 13.5% volatility  
3. Moderate (60/40): 5.5% real return, 15% volatility
4. Moderate Aggressive (70/30): 6.0% real return, 16.5% volatility
5. Aggressive (80/20): 6.8% real return, 18% volatility
6. Very Aggressive (90/10): 7.0% real return, 19% volatility
7. Ultra Aggressive (100/0): 7.2% real return, 20% volatility
"""

import sys
import os
from pathlib import Path

# Find project root directory (look for src directory)
script_dir = Path(__file__).parent
project_root = script_dir.parent
src_path = project_root / 'src'
sys.path.append(str(src_path))

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from enhanced_qol_framework import EnhancedQOLAnalysis
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')


class MultiPortfolioQOLAnalysis:
    """
    Comprehensive QOL analysis across multiple portfolio risk strategies
    """
    
    def __init__(self):
        # Define portfolio allocation strategies with realistic historical parameters
        self.portfolio_strategies = {
            'Conservative_30_70': {
                'name': 'Conservative (30/70)',
                'stocks': 30,
                'bonds': 70,
                'real_return': 0.035,  # 3.5%
                'volatility': 0.12,    # 12%
                'description': '30% stocks, 70% bonds - Capital preservation focus'
            },
            'Moderate_Conservative_50_50': {
                'name': 'Moderate Conservative (50/50)',
                'stocks': 50,
                'bonds': 50,
                'real_return': 0.045,  # 4.5%
                'volatility': 0.135,   # 13.5%
                'description': '50% stocks, 50% bonds - Balanced safety'
            },
            'Moderate_60_40': {
                'name': 'Moderate (60/40)',
                'stocks': 60,
                'bonds': 40,
                'real_return': 0.055,  # 5.5%
                'volatility': 0.15,    # 15%
                'description': '60% stocks, 40% bonds - Traditional balanced'
            },
            'Moderate_Aggressive_70_30': {
                'name': 'Moderate Aggressive (70/30)',
                'stocks': 70,
                'bonds': 30,
                'real_return': 0.060,  # 6.0%
                'volatility': 0.165,   # 16.5%
                'description': '70% stocks, 30% bonds - Growth focused'
            },
            'Aggressive_80_20': {
                'name': 'Aggressive (80/20)',
                'stocks': 80,
                'bonds': 20,
                'real_return': 0.068,  # 6.8%
                'volatility': 0.18,    # 18%
                'description': '80% stocks, 20% bonds - High growth'
            },
            'Very_Aggressive_90_10': {
                'name': 'Very Aggressive (90/10)',
                'stocks': 90,
                'bonds': 10,
                'real_return': 0.070,  # 7.0%
                'volatility': 0.19,    # 19%
                'description': '90% stocks, 10% bonds - Near equity'
            },
            'Ultra_Aggressive_100_0': {
                'name': 'Ultra Aggressive (100/0)',
                'stocks': 100,
                'bonds': 0,
                'real_return': 0.072,  # 7.2%
                'volatility': 0.20,    # 20%
                'description': '100% stocks - Maximum growth'
            }
        }
        
        # QOL strategy variants
        self.qol_strategies = {
            'QOL_Conservative': {
                'name': 'QOL Conservative',
                'phase1_mult': 1.20,   # 20% above Trinity in early years
                'phase2_mult': 1.05,   # 5% above Trinity in middle years
                'phase3_mult': 0.95,   # 5% below Trinity in late years
                'description': 'Modest front-loading'
            },
            'QOL_Moderate': {
                'name': 'QOL Moderate', 
                'phase1_mult': 1.275,  # 27.5% above Trinity
                'phase2_mult': 1.10,   # 10% above Trinity
                'phase3_mult': 0.91,   # 9% below Trinity
                'description': 'Moderate front-loading'
            },
            'QOL_Enhanced': {
                'name': 'QOL Enhanced',
                'phase1_mult': 1.35,   # 35% above Trinity (original)
                'phase2_mult': 1.125,  # 12.5% above Trinity
                'phase3_mult': 0.875,  # 12.5% below Trinity
                'description': 'Aggressive front-loading'
            }
        }
        
        # Enjoyment valuation scenarios
        self.enjoyment_scenarios = {
            'conservative': {'high': 1.25, 'moderate': 1.10, 'low': 1.00},
            'moderate': {'high': 1.50, 'moderate': 1.20, 'low': 1.00},
            'aggressive': {'high': 2.00, 'moderate': 1.40, 'low': 1.00}
        }
        
        self.results = {}
        
    def get_enjoyment_multiplier(self, year: int, scenario: str = 'moderate') -> float:
        """Get enjoyment multiplier for a specific year"""
        values = self.enjoyment_scenarios[scenario]
        
        if year < 10:  # Ages 65-74
            return values['high']
        elif year < 20:  # Ages 75-84
            return values['moderate']
        else:  # Ages 85+
            return values['low']
    
    def calculate_enjoyment_value(self, withdrawal_paths: np.ndarray, 
                                  scenario: str = 'moderate') -> Dict:
        """Calculate enjoyment-weighted value for withdrawal paths"""
        n_simulations, n_years = withdrawal_paths.shape
        
        # Apply enjoyment multipliers
        enjoyment_weighted_paths = np.zeros_like(withdrawal_paths)
        total_enjoyment_premiums = np.zeros(n_simulations)
        
        for year in range(n_years):
            enjoyment_multiplier = self.get_enjoyment_multiplier(year, scenario)
            enjoyment_weighted_paths[:, year] = withdrawal_paths[:, year] * enjoyment_multiplier
            
            # Premium value (extra value above base income)
            premium_multiplier = enjoyment_multiplier - 1.0
            total_enjoyment_premiums += withdrawal_paths[:, year] * premium_multiplier
        
        return {
            'total_enjoyment_value': np.mean(np.sum(enjoyment_weighted_paths, axis=1)),
            'enjoyment_premium': np.mean(total_enjoyment_premiums)
        }
    
    def run_strategy_simulation(self, portfolio_key: str, qol_key: str, 
                               n_simulations: int = 1000) -> Dict:
        """Run simulation for a specific portfolio and QOL strategy combination"""
        
        portfolio = self.portfolio_strategies[portfolio_key]
        qol_strategy = self.qol_strategies[qol_key]
        
        # Run Trinity Study simulation
        trinity_analyzer = EnhancedQOLAnalysis(
            starting_value=1000000,
            starting_age=65,
            horizon_years=29,
            n_simulations=n_simulations
        )
        
        trinity_analyzer.run_enhanced_simulation(
            withdrawal_strategy='trinity_4pct',
            return_volatility=portfolio['volatility'],
            base_real_return=portfolio['real_return'],
            base_inflation=0.03,
            qol_variability=False,
            verbose=False
        )
        
        trinity_portfolio_paths = np.array(trinity_analyzer.simulation_results['portfolio_paths'])
        trinity_withdrawal_paths = np.array(trinity_analyzer.simulation_results['withdrawal_paths'])
        
        # Run QOL simulation
        qol_analyzer = EnhancedQOLAnalysis(
            starting_value=1000000,
            starting_age=65,
            horizon_years=29,
            n_simulations=n_simulations
        )
        
        # Configure QOL rates
        qol_analyzer.qol_phase1_rate = qol_strategy['phase1_mult'] * 0.04
        qol_analyzer.qol_phase2_rate = qol_strategy['phase2_mult'] * 0.04
        qol_analyzer.qol_phase3_rate = qol_strategy['phase3_mult'] * 0.04
        
        qol_analyzer.run_enhanced_simulation(
            withdrawal_strategy='hauenstein',
            return_volatility=portfolio['volatility'],
            base_real_return=portfolio['real_return'],
            base_inflation=0.03,
            qol_variability=False,
            verbose=False
        )
        
        qol_portfolio_paths = np.array(qol_analyzer.simulation_results['portfolio_paths'])
        qol_withdrawal_paths = np.array(qol_analyzer.simulation_results['withdrawal_paths'])
        
        # Calculate basic metrics
        trinity_success = np.mean(trinity_portfolio_paths[:, -1] > 0)
        qol_success = np.mean(qol_portfolio_paths[:, -1] > 0)
        
        trinity_total_income = np.mean(np.sum(trinity_withdrawal_paths, axis=1))
        qol_total_income = np.mean(np.sum(qol_withdrawal_paths, axis=1))
        
        # Calculate enjoyment values for all scenarios
        trinity_enjoyment = {}
        qol_enjoyment = {}
        
        for enjoyment_scenario in self.enjoyment_scenarios.keys():
            trinity_enjoyment[enjoyment_scenario] = self.calculate_enjoyment_value(
                trinity_withdrawal_paths, enjoyment_scenario
            )
            qol_enjoyment[enjoyment_scenario] = self.calculate_enjoyment_value(
                qol_withdrawal_paths, enjoyment_scenario
            )
        
        return {
            'portfolio': portfolio,
            'qol_strategy': qol_strategy,
            'trinity_success_rate': trinity_success,
            'qol_success_rate': qol_success,
            'trinity_total_income': trinity_total_income,
            'qol_total_income': qol_total_income,
            'risk_penalty': (trinity_success - qol_success) * 100,
            'income_advantage': (qol_total_income / trinity_total_income - 1) * 100,
            'trinity_enjoyment': trinity_enjoyment,
            'qol_enjoyment': qol_enjoyment
        }
    
    def run_comprehensive_analysis(self, n_simulations: int = 1000) -> Dict:
        """Run comprehensive analysis across all portfolio and QOL strategy combinations"""
        
        print("🔬 MULTI-PORTFOLIO QOL SIMULATION ANALYSIS")
        print("=" * 70)
        print(f"Simulations per strategy: {n_simulations:,}")
        print(f"Portfolio strategies: {len(self.portfolio_strategies)}")
        print(f"QOL strategies: {len(self.qol_strategies)}")
        print(f"Total combinations: {len(self.portfolio_strategies) * len(self.qol_strategies)}")
        print()
        
        all_results = []
        
        for portfolio_key, portfolio in self.portfolio_strategies.items():
            print(f"📊 Portfolio: {portfolio['name']}")
            print(f"   {portfolio['real_return']*100:.1f}% real return, {portfolio['volatility']*100:.1f}% volatility")
            
            for qol_key, qol_strategy in self.qol_strategies.items():
                print(f"   🎯 {qol_strategy['name']}: ", end="")
                
                # Run simulation
                result = self.run_strategy_simulation(portfolio_key, qol_key, n_simulations)
                
                # Add identifiers
                result['portfolio_key'] = portfolio_key
                result['qol_key'] = qol_key
                
                all_results.append(result)
                
                # Quick summary
                risk_penalty = result['risk_penalty']
                income_adv = result['income_advantage']
                print(f"{income_adv:+.1f}% income, {risk_penalty:+.1f}% risk")
            
            print()
        
        return {
            'results': all_results,
            'portfolio_strategies': self.portfolio_strategies,
            'qol_strategies': self.qol_strategies,
            'enjoyment_scenarios': self.enjoyment_scenarios
        }
    
    def create_comprehensive_summary(self, analysis_results: Dict) -> str:
        """Create comprehensive summary across all scenarios"""
        
        results = analysis_results['results']
        
        summary = []
        summary.append("=" * 80)
        summary.append("🔬 MULTI-PORTFOLIO QOL SIMULATION SUMMARY")
        summary.append("=" * 80)
        summary.append("")
        
        # Create results DataFrame for easier analysis
        data = []
        for result in results:
            portfolio = result['portfolio']
            qol_strategy = result['qol_strategy']
            
            # Calculate enjoyment metrics for moderate scenario
            trinity_enjoyment = result['trinity_enjoyment']['moderate']
            qol_enjoyment = result['qol_enjoyment']['moderate']
            
            enjoyment_premium = qol_enjoyment['enjoyment_premium'] - trinity_enjoyment['enjoyment_premium']
            risk_cost = result['risk_penalty'] / 100 * 1000000
            
            cost_per_enjoyment = risk_cost / enjoyment_premium if enjoyment_premium > 0 else float('inf')
            
            data.append({
                'Portfolio': portfolio['name'],
                'Stock_Allocation': portfolio['stocks'],
                'Real_Return': portfolio['real_return'],
                'Volatility': portfolio['volatility'],
                'QOL_Strategy': qol_strategy['name'],
                'Phase1_Mult': qol_strategy['phase1_mult'],
                'Trinity_Success': result['trinity_success_rate'],
                'QOL_Success': result['qol_success_rate'],
                'Risk_Penalty': result['risk_penalty'],
                'Income_Advantage': result['income_advantage'],
                'Enjoyment_Premium': enjoyment_premium,
                'Risk_Cost': risk_cost,
                'Cost_Per_Enjoyment': cost_per_enjoyment
            })
        
        df = pd.DataFrame(data)
        
        # Find optimal combinations
        summary.append("🏆 OPTIMAL COMBINATIONS (Moderate Enjoyment Scenario)")
        summary.append("-" * 60)
        
        # Best QOL strategies by portfolio allocation
        for portfolio_name in df['Portfolio'].unique():
            portfolio_df = df[df['Portfolio'] == portfolio_name]
            best_qol = portfolio_df.loc[portfolio_df['Cost_Per_Enjoyment'].idxmin()]
            
            if best_qol['Cost_Per_Enjoyment'] <= 2.0:
                recommendation = "🟢 RECOMMENDED"
            elif best_qol['Cost_Per_Enjoyment'] <= 5.0:
                recommendation = "🟡 CONSIDER"
            else:
                recommendation = "🔴 NOT RECOMMENDED"
            
            summary.append(f"")
            summary.append(f"{portfolio_name}:")
            summary.append(f"  Best QOL: {best_qol['QOL_Strategy']}")
            summary.append(f"  Cost per enjoyment $: ${best_qol['Cost_Per_Enjoyment']:.2f}")
            summary.append(f"  Income advantage: {best_qol['Income_Advantage']:+.1f}%")
            summary.append(f"  Risk penalty: {best_qol['Risk_Penalty']:+.1f}%")
            summary.append(f"  {recommendation}")
        
        summary.append("")
        summary.append("🎯 KEY INSIGHTS")
        summary.append("-" * 40)
        
        # Overall patterns
        best_overall = df.loc[df['Cost_Per_Enjoyment'].idxmin()]
        worst_overall = df.loc[df['Cost_Per_Enjoyment'].idxmax()]
        
        summary.append(f"• Best overall combination: {best_overall['Portfolio']} + {best_overall['QOL_Strategy']}")
        summary.append(f"  Cost: ${best_overall['Cost_Per_Enjoyment']:.2f} per enjoyment dollar")
        summary.append("")
        summary.append(f"• Worst combination: {worst_overall['Portfolio']} + {worst_overall['QOL_Strategy']}")
        summary.append(f"  Cost: ${worst_overall['Cost_Per_Enjoyment']:.2f} per enjoyment dollar")
        summary.append("")
        
        # Analyze by stock allocation
        correlation_stocks_cost = df['Stock_Allocation'].corr(df['Cost_Per_Enjoyment'])
        
        summary.append(f"• Stock allocation effect on QOL viability:")
        summary.append(f"  Correlation with cost per enjoyment $: {correlation_stocks_cost:.3f}")
        if correlation_stocks_cost < -0.3:
            summary.append(f"  Higher stock allocation IMPROVES QOL viability")
        elif correlation_stocks_cost > 0.3:
            summary.append(f"  Higher stock allocation WORSENS QOL viability")
        else:
            summary.append(f"  Stock allocation has NEUTRAL effect on QOL viability")
        
        # Count viable strategies
        viable_count = len(df[df['Cost_Per_Enjoyment'] <= 2.0])
        total_count = len(df)
        
        summary.append("")
        summary.append(f"• Viable QOL combinations (≤$2.00 per enjoyment $): {viable_count}/{total_count}")
        summary.append(f"• QOL viability rate: {viable_count/total_count*100:.1f}%")
        
        return "\n".join(summary)
    
    def create_comprehensive_visualization(self, analysis_results: Dict):
        """Create comprehensive visualization dashboard"""
        
        results = analysis_results['results']
        
        # Prepare data
        data = []
        for result in results:
            portfolio = result['portfolio']
            qol_strategy = result['qol_strategy']
            
            trinity_enjoyment = result['trinity_enjoyment']['moderate']
            qol_enjoyment = result['qol_enjoyment']['moderate']
            
            enjoyment_premium = qol_enjoyment['enjoyment_premium'] - trinity_enjoyment['enjoyment_premium']
            risk_cost = result['risk_penalty'] / 100 * 1000000
            cost_per_enjoyment = risk_cost / enjoyment_premium if enjoyment_premium > 0 else float('inf')
            
            data.append({
                'Portfolio': portfolio['name'],
                'Stock_Pct': portfolio['stocks'],
                'Real_Return': portfolio['real_return'] * 100,
                'Volatility': portfolio['volatility'] * 100,
                'QOL_Strategy': qol_strategy['name'],
                'Phase1_Mult': qol_strategy['phase1_mult'],
                'Trinity_Success': result['trinity_success_rate'] * 100,
                'QOL_Success': result['qol_success_rate'] * 100,
                'Risk_Penalty': result['risk_penalty'],
                'Income_Advantage': result['income_advantage'],
                'Cost_Per_Enjoyment': min(cost_per_enjoyment, 10)  # Cap for visualization
            })
        
        df = pd.DataFrame(data)
        
        # Create dashboard
        fig = plt.figure(figsize=(20, 16))
        
        # Main heatmap: Cost per enjoyment dollar
        ax1 = plt.subplot(2, 3, 1)
        pivot_cost = df.pivot(index='QOL_Strategy', columns='Portfolio', values='Cost_Per_Enjoyment')
        sns.heatmap(pivot_cost, annot=True, fmt='.2f', cmap='RdYlGn_r', 
                    cbar_kws={'label': 'Cost per Enjoyment $'}, ax=ax1)
        ax1.set_title('Cost per Enjoyment Dollar\n(Lower is Better)', fontweight='bold')
        ax1.set_xlabel('')
        
        # Risk penalty heatmap
        ax2 = plt.subplot(2, 3, 2)
        pivot_risk = df.pivot(index='QOL_Strategy', columns='Portfolio', values='Risk_Penalty')
        sns.heatmap(pivot_risk, annot=True, fmt='.1f', cmap='Reds', 
                    cbar_kws={'label': 'Risk Penalty (%)'}, ax=ax2)
        ax2.set_title('Portfolio Failure Risk Penalty\n(Lower is Better)', fontweight='bold')
        ax2.set_xlabel('')
        
        # Income advantage heatmap
        ax3 = plt.subplot(2, 3, 3)
        pivot_income = df.pivot(index='QOL_Strategy', columns='Portfolio', values='Income_Advantage')
        sns.heatmap(pivot_income, annot=True, fmt='.1f', cmap='Blues', 
                    cbar_kws={'label': 'Income Advantage (%)'}, ax=ax3)
        ax3.set_title('Total Income Advantage\n(Higher is Better)', fontweight='bold')
        ax3.set_xlabel('')
        
        # Stock allocation effect
        ax4 = plt.subplot(2, 3, 4)
        for qol_strategy in df['QOL_Strategy'].unique():
            strategy_data = df[df['QOL_Strategy'] == qol_strategy]
            ax4.plot(strategy_data['Stock_Pct'], strategy_data['Cost_Per_Enjoyment'], 
                    marker='o', label=qol_strategy, linewidth=2)
        
        ax4.axhline(y=1.0, color='green', linestyle='--', alpha=0.7, label='$1.00 threshold')
        ax4.axhline(y=2.0, color='orange', linestyle='--', alpha=0.7, label='$2.00 threshold')
        ax4.set_xlabel('Stock Allocation (%)')
        ax4.set_ylabel('Cost per Enjoyment Dollar')
        ax4.set_title('Stock Allocation Effect on QOL Viability')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        # Success rate comparison
        ax5 = plt.subplot(2, 3, 5)
        
        # Group by portfolio for cleaner visualization
        portfolio_order = ['Conservative (30/70)', 'Moderate Conservative (50/50)', 'Moderate (60/40)', 
                          'Moderate Aggressive (70/30)', 'Aggressive (80/20)', 'Very Aggressive (90/10)', 
                          'Ultra Aggressive (100/0)']
        
        trinity_success_by_portfolio = []
        qol_enhanced_success_by_portfolio = []
        
        for portfolio in portfolio_order:
            trinity_val = df[(df['Portfolio'] == portfolio) & (df['QOL_Strategy'] == 'QOL Enhanced')]['Trinity_Success'].iloc[0]
            qol_val = df[(df['Portfolio'] == portfolio) & (df['QOL_Strategy'] == 'QOL Enhanced')]['QOL_Success'].iloc[0]
            trinity_success_by_portfolio.append(trinity_val)
            qol_enhanced_success_by_portfolio.append(qol_val)
        
        x = np.arange(len(portfolio_order))
        width = 0.35
        
        ax5.bar(x - width/2, trinity_success_by_portfolio, width, label='Trinity Study', alpha=0.7, color='blue')
        ax5.bar(x + width/2, qol_enhanced_success_by_portfolio, width, label='QOL Enhanced', alpha=0.7, color='red')
        
        ax5.set_xlabel('Portfolio Strategy')
        ax5.set_ylabel('Success Rate (%)')
        ax5.set_title('Portfolio Survival Rates')
        ax5.set_xticks(x)
        ax5.set_xticklabels([p.split('(')[0].strip() for p in portfolio_order], rotation=45)
        ax5.legend()
        ax5.grid(True, alpha=0.3)
        
        # Viability summary
        ax6 = plt.subplot(2, 3, 6)
        
        viability_counts = {
            'Excellent\n(≤$1.00)': len(df[df['Cost_Per_Enjoyment'] <= 1.0]),
            'Good\n(≤$2.00)': len(df[(df['Cost_Per_Enjoyment'] > 1.0) & (df['Cost_Per_Enjoyment'] <= 2.0)]),
            'Moderate\n(≤$5.00)': len(df[(df['Cost_Per_Enjoyment'] > 2.0) & (df['Cost_Per_Enjoyment'] <= 5.0)]),
            'Poor\n(>$5.00)': len(df[df['Cost_Per_Enjoyment'] > 5.0])
        }
        
        colors = ['green', 'lightgreen', 'yellow', 'red']
        wedges, texts, autotexts = ax6.pie(viability_counts.values(), labels=viability_counts.keys(), 
                                          autopct='%1.1f%%', colors=colors, startangle=90)
        ax6.set_title('QOL Strategy Viability Distribution\n(All Portfolio-Strategy Combinations)')
        
        plt.suptitle('Multi-Portfolio QOL Strategy Analysis Dashboard', fontsize=16, fontweight='bold')
        plt.tight_layout()
        
        # Save the plot
        output_dir = project_root / 'output' / 'charts'
        os.makedirs(output_dir, exist_ok=True)
        plt.savefig(f'{output_dir}/multi_portfolio_qol_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return fig


def main():
    """Run the comprehensive multi-portfolio QOL analysis"""
    
    analyzer = MultiPortfolioQOLAnalysis()
    
    # Run comprehensive analysis
    print("Starting multi-portfolio QOL simulation analysis...")
    analysis_results = analyzer.run_comprehensive_analysis(n_simulations=1000)
    
    # Generate summary report
    summary_report = analyzer.create_comprehensive_summary(analysis_results)
    print("\n" + summary_report)
    
    # Create visualization dashboard
    print("\n📈 Generating comprehensive visualization dashboard...")
    analyzer.create_comprehensive_visualization(analysis_results)
    
    # Save detailed results
    output_dir = project_root / 'output'
    os.makedirs(output_dir, exist_ok=True)
    
    # Save summary report
    with open(f'{output_dir}/multi_portfolio_qol_analysis.txt', 'w') as f:
        f.write(summary_report)
    
    # Save detailed data
    results_data = []
    for result in analysis_results['results']:
        portfolio = result['portfolio']
        qol_strategy = result['qol_strategy']
        
        trinity_enjoyment = result['trinity_enjoyment']['moderate']
        qol_enjoyment = result['qol_enjoyment']['moderate']
        
        enjoyment_premium = qol_enjoyment['enjoyment_premium'] - trinity_enjoyment['enjoyment_premium']
        risk_cost = result['risk_penalty'] / 100 * 1000000
        cost_per_enjoyment = risk_cost / enjoyment_premium if enjoyment_premium > 0 else float('inf')
        
        results_data.append({
            'Portfolio': portfolio['name'],
            'Stock_Allocation': portfolio['stocks'],
            'Bond_Allocation': portfolio['bonds'],
            'Real_Return_Pct': portfolio['real_return'] * 100,
            'Volatility_Pct': portfolio['volatility'] * 100,
            'QOL_Strategy': qol_strategy['name'],
            'Phase1_Multiplier': qol_strategy['phase1_mult'],
            'Phase2_Multiplier': qol_strategy['phase2_mult'],
            'Phase3_Multiplier': qol_strategy['phase3_mult'],
            'Trinity_Success_Rate_Pct': result['trinity_success_rate'] * 100,
            'QOL_Success_Rate_Pct': result['qol_success_rate'] * 100,
            'Risk_Penalty_Pct': result['risk_penalty'],
            'Income_Advantage_Pct': result['income_advantage'],
            'Trinity_Total_Income': result['trinity_total_income'],
            'QOL_Total_Income': result['qol_total_income'],
            'Enjoyment_Premium_Dollars': enjoyment_premium,
            'Risk_Cost_Dollars': risk_cost,
            'Cost_Per_Enjoyment_Dollar': cost_per_enjoyment
        })
    
    results_df = pd.DataFrame(results_data)
    results_df.to_csv(f'{output_dir}/multi_portfolio_qol_detailed_results.csv', index=False)
    
    print(f"\n✅ Analysis complete!")
    print(f"📋 Summary Report: {output_dir}/multi_portfolio_qol_analysis.txt")
    print(f"📊 Detailed Data: {output_dir}/multi_portfolio_qol_detailed_results.csv")
    print(f"📈 Dashboard: output/charts/multi_portfolio_qol_analysis.png")
    
    # Quick summary
    viable_count = len(results_df[results_df['Cost_Per_Enjoyment_Dollar'] <= 2.0])
    total_count = len(results_df)
    print(f"\n🎯 Quick Summary: {viable_count}/{total_count} combinations are viable (≤$2.00 per enjoyment dollar)")


if __name__ == "__main__":
    main()