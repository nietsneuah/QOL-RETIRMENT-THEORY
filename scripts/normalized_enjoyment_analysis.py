"""
QOL NORMALIZED ENJOYMENT VALUE ANALYSIS

This analysis assigns specific dollar values to the "enjoyment premium" of early
retirement years and normalizes all values to Year 1 purchasing power for
direct comparison.

Key Concept: We'll quantify how much extra you'd be willing to pay for income
received during high-enjoyment years vs. low-enjoyment years.
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
from enhanced_qol_framework import EnhancedQOLAnalysis
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')


class NormalizedEnjoymentAnalysis:
    """
    Analyze QOL strategies using normalized enjoyment values
    """
    
    def __init__(self):
        # Use aggressive portfolio (best case for QOL)
        self.portfolio_params = {
            'real_return': 0.072,  # 7.2% real return (100% stocks)
            'volatility': 0.20,    # 20% volatility
            'description': '100% Stock Portfolio'
        }
        
        # Enjoyment value multipliers - how much more valuable is income in each phase?
        # These represent how much extra you'd pay to receive $1 in Year X vs Year 20
        self.enjoyment_values = {
            'high_enjoyment': 1.50,    # Ages 65-74: 50% premium for active, healthy years
            'moderate_enjoyment': 1.20, # Ages 75-84: 20% premium for semi-active years  
            'low_enjoyment': 1.00,     # Ages 85+: Base value (no premium)
            'description': 'Enjoyment Value: High=1.5x, Moderate=1.2x, Low=1.0x'
        }
        
        # Alternative scenarios for sensitivity analysis
        self.enjoyment_scenarios = {
            'conservative': {'high': 1.25, 'moderate': 1.10, 'low': 1.00},
            'moderate': {'high': 1.50, 'moderate': 1.20, 'low': 1.00},
            'aggressive': {'high': 2.00, 'moderate': 1.40, 'low': 1.00}
        }
        
    def get_enjoyment_multiplier(self, year: int, scenario: str = 'moderate') -> float:
        """Get enjoyment multiplier for a specific year"""
        values = self.enjoyment_scenarios[scenario]
        
        if year < 10:  # Ages 65-74
            return values['high']
        elif year < 20:  # Ages 75-84
            return values['moderate']
        else:  # Ages 85+
            return values['low']
    
    def calculate_normalized_enjoyment_value(self, withdrawal_paths: np.ndarray, 
                                           scenario: str = 'moderate') -> Dict:
        """
        Calculate the total enjoyment value normalized to Year 1 dollars
        """
        n_simulations, n_years = withdrawal_paths.shape
        
        # Apply enjoyment multipliers to each year's withdrawals
        enjoyment_weighted_paths = np.zeros_like(withdrawal_paths)
        total_enjoyment_premiums = np.zeros(n_simulations)
        
        for year in range(n_years):
            enjoyment_multiplier = self.get_enjoyment_multiplier(year, scenario)
            
            # Enjoyment-weighted value (what the income is "worth" in enjoyment terms)
            enjoyment_weighted_paths[:, year] = withdrawal_paths[:, year] * enjoyment_multiplier
            
            # Premium value (extra value above base income)
            premium_multiplier = enjoyment_multiplier - 1.0
            total_enjoyment_premiums += withdrawal_paths[:, year] * premium_multiplier
        
        # Calculate metrics
        total_raw_income = np.sum(withdrawal_paths, axis=1)
        total_enjoyment_value = np.sum(enjoyment_weighted_paths, axis=1)
        
        return {
            'avg_raw_income': np.mean(total_raw_income),
            'avg_enjoyment_value': np.mean(total_enjoyment_value),
            'avg_enjoyment_premium': np.mean(total_enjoyment_premiums),
            'enjoyment_premium_pct': (np.mean(total_enjoyment_value) / np.mean(total_raw_income) - 1) * 100,
            'enjoyment_weighted_paths': enjoyment_weighted_paths,
            'total_enjoyment_premiums': total_enjoyment_premiums
        }
    
    def run_normalized_analysis(self) -> Dict:
        """Run complete normalized enjoyment analysis"""
        
        print("💰 NORMALIZED ENJOYMENT VALUE ANALYSIS")
        print("=" * 60)
        print(f"Portfolio: {self.portfolio_params['description']}")
        print(f"Enjoyment Values: High=1.5x, Moderate=1.2x, Low=1.0x")
        print("(Normalized to Year 1 purchasing power)")
        print()
        
        # Run simulations for both strategies
        strategies = {
            'Trinity Study': ('trinity_4pct', {}),
            'QOL Enhanced': ('hauenstein', {'phase1': 1.35, 'phase2': 1.125, 'phase3': 0.875})
        }
        
        strategy_results = {}
        
        for strategy_name, (strategy_key, qol_params) in strategies.items():
            print(f"🔍 Analyzing {strategy_name}...")
            
            analyzer = EnhancedQOLAnalysis(
                starting_value=1000000,
                starting_age=65,
                horizon_years=29,
                n_simulations=1000
            )
            
            # Configure QOL rates if needed
            if qol_params:
                analyzer.qol_phase1_rate = qol_params['phase1'] * 0.04
                analyzer.qol_phase2_rate = qol_params['phase2'] * 0.04  
                analyzer.qol_phase3_rate = qol_params['phase3'] * 0.04
            
            # Run simulation
            analyzer.run_enhanced_simulation(
                withdrawal_strategy=strategy_key,
                return_volatility=self.portfolio_params['volatility'],
                base_real_return=self.portfolio_params['real_return'],
                base_inflation=0.03,
                qol_variability=False,
                verbose=False
            )
            
            # Extract results
            portfolio_paths = np.array(analyzer.simulation_results['portfolio_paths'])
            withdrawal_paths = np.array(analyzer.simulation_results['withdrawal_paths'])
            
            # Calculate basic metrics
            final_values = portfolio_paths[:, -1]
            success_rate = np.mean(final_values > 0)
            total_income = np.mean(np.sum(withdrawal_paths, axis=1))
            
            # Calculate normalized enjoyment values for different scenarios
            enjoyment_results = {}
            for scenario_name in self.enjoyment_scenarios.keys():
                enjoyment_results[scenario_name] = self.calculate_normalized_enjoyment_value(
                    withdrawal_paths, scenario_name
                )
            
            strategy_results[strategy_name] = {
                'success_rate': success_rate,
                'portfolio_paths': portfolio_paths,
                'withdrawal_paths': withdrawal_paths,
                'total_income': total_income,
                'avg_final_value': np.mean(final_values),
                'enjoyment_results': enjoyment_results
            }
        
        return {
            'strategy_results': strategy_results,
            'portfolio_params': self.portfolio_params,
            'enjoyment_scenarios': self.enjoyment_scenarios
        }
    
    def create_value_comparison_report(self, analysis_results: Dict) -> str:
        """Create comprehensive value comparison report"""
        
        trinity_results = analysis_results['strategy_results']['Trinity Study']
        qol_results = analysis_results['strategy_results']['QOL Enhanced']
        
        report = []
        report.append("=" * 80)
        report.append("💰 NORMALIZED ENJOYMENT VALUE ANALYSIS REPORT")
        report.append("=" * 80)
        report.append("")
        
        report.append("📋 EXECUTIVE SUMMARY")
        report.append("-" * 40)
        report.append("This analysis assigns dollar values to the 'enjoyment premium' of")
        report.append("early retirement years and normalizes all comparisons to Year 1")
        report.append("purchasing power for direct financial comparison.")
        report.append("")
        
        report.append("🎯 ENJOYMENT VALUE ASSUMPTIONS")
        report.append("-" * 40)
        report.append("Income received during different life phases has different value:")
        report.append("• High Enjoyment (Ages 65-74): 1.5x value (active, healthy years)")
        report.append("• Moderate Enjoyment (Ages 75-84): 1.2x value (semi-active years)")
        report.append("• Low Enjoyment (Ages 85+): 1.0x value (baseline)")
        report.append("")
        report.append("Question: Would you pay $1,500 to receive income in your first")
        report.append("retirement year vs. $1,000 to receive it at age 85?")
        report.append("")
        
        # Analyze all scenarios
        for scenario_name, scenario_values in analysis_results['enjoyment_scenarios'].items():
            report.append(f"📊 {scenario_name.upper()} ENJOYMENT SCENARIO")
            report.append("-" * 40)
            report.append(f"Values: High={scenario_values['high']:.1f}x, Moderate={scenario_values['moderate']:.1f}x, Low={scenario_values['low']:.1f}x")
            report.append("")
            
            trinity_enjoyment = trinity_results['enjoyment_results'][scenario_name]
            qol_enjoyment = qol_results['enjoyment_results'][scenario_name]
            
            # Calculate comparative metrics
            trinity_raw = trinity_enjoyment['avg_raw_income']
            trinity_value = trinity_enjoyment['avg_enjoyment_value']
            trinity_premium = trinity_enjoyment['avg_enjoyment_premium']
            
            qol_raw = qol_enjoyment['avg_raw_income']
            qol_value = qol_enjoyment['avg_enjoyment_value']
            qol_premium = qol_enjoyment['avg_enjoyment_premium']
            
            # Risk metrics
            trinity_success = trinity_results['success_rate']
            qol_success = qol_results['success_rate']
            risk_penalty = (trinity_success - qol_success) * 100
            
            # Value comparisons
            raw_income_diff = qol_raw - trinity_raw
            enjoyment_value_diff = qol_value - trinity_value
            enjoyment_premium_diff = qol_premium - trinity_premium
            
            report.append("Raw Income Comparison:")
            report.append(f"  • Trinity Study: ${trinity_raw:,.0f}")
            report.append(f"  • QOL Enhanced: ${qol_raw:,.0f}")
            report.append(f"  • QOL Advantage: ${raw_income_diff:+,.0f} ({raw_income_diff/trinity_raw*100:+.1f}%)")
            report.append("")
            
            report.append("Enjoyment-Weighted Value Comparison:")
            report.append(f"  • Trinity Study: ${trinity_value:,.0f}")
            report.append(f"  • QOL Enhanced: ${qol_value:,.0f}")
            report.append(f"  • QOL Advantage: ${enjoyment_value_diff:+,.0f} ({enjoyment_value_diff/trinity_value*100:+.1f}%)")
            report.append("")
            
            report.append("Enjoyment Premium Analysis:")
            report.append(f"  • Trinity Premium: ${trinity_premium:,.0f}")
            report.append(f"  • QOL Premium: ${qol_premium:,.0f}")
            report.append(f"  • Extra Enjoyment Value: ${enjoyment_premium_diff:+,.0f}")
            report.append("")
            
            # Risk-adjusted value
            if risk_penalty > 0:
                risk_adjusted_value = enjoyment_value_diff / (risk_penalty/100 * 1000000)
                enjoyment_cost_per_risk = (risk_penalty/100 * 1000000) / enjoyment_premium_diff if enjoyment_premium_diff > 0 else float('inf')
                
                report.append("Risk-Adjusted Analysis:")
                report.append(f"  • Additional Risk: {risk_penalty:.1f} percentage points")
                report.append(f"  • Risk Cost: ${risk_penalty/100 * 1000000:,.0f} in portfolio value")
                report.append(f"  • Risk-Adjusted Value: ${risk_adjusted_value:.2f} per risk dollar")
                report.append(f"  • Cost per Enjoyment Dollar: ${enjoyment_cost_per_risk:.2f} in risk")
                report.append("")
                
                # Decision guidance
                if enjoyment_cost_per_risk <= 1.0:
                    recommendation = "🟢 EXCELLENT VALUE - Less than $1 risk per $1 enjoyment"
                elif enjoyment_cost_per_risk <= 2.0:
                    recommendation = "🟡 GOOD VALUE - Reasonable risk-enjoyment trade-off"
                elif enjoyment_cost_per_risk <= 5.0:
                    recommendation = "🟡 MODERATE VALUE - Consider personal preferences"
                else:
                    recommendation = "🔴 POOR VALUE - High risk for modest enjoyment gain"
                
                report.append(f"Value Assessment: {recommendation}")
                report.append("")
        
        # Overall recommendation
        report.append("🎯 OVERALL RECOMMENDATION")
        report.append("-" * 40)
        
        # Use moderate scenario for overall assessment
        moderate_trinity = trinity_results['enjoyment_results']['moderate']
        moderate_qol = qol_results['enjoyment_results']['moderate']
        
        enjoyment_diff = moderate_qol['avg_enjoyment_premium'] - moderate_trinity['avg_enjoyment_premium']
        risk_cost = risk_penalty/100 * 1000000
        cost_per_enjoyment = risk_cost / enjoyment_diff if enjoyment_diff > 0 else float('inf')
        
        report.append(f"Based on moderate enjoyment values (1.5x/1.2x/1.0x):")
        report.append(f"• QOL provides ${enjoyment_diff:,.0f} extra enjoyment value")
        report.append(f"• QOL costs ${risk_cost:,.0f} in additional portfolio risk")
        report.append(f"• Cost: ${cost_per_enjoyment:.2f} risk per $1 enjoyment benefit")
        report.append("")
        
        if cost_per_enjoyment <= 1.0:
            final_rec = "🟢 QOL RECOMMENDED - Excellent enjoyment value for the risk"
        elif cost_per_enjoyment <= 2.0:
            final_rec = "🟡 QOL VIABLE - Good value if you prioritize early retirement enjoyment"
        else:
            final_rec = "🔴 QOL QUESTIONABLE - High cost for enjoyment benefits"
        
        report.append(f"FINAL RECOMMENDATION: {final_rec}")
        report.append("")
        
        report.append("🤔 PERSONAL DECISION FACTORS")
        report.append("-" * 40)
        report.append("The key question: How much extra would you personally pay to")
        report.append("receive retirement income during your healthy, active years")
        report.append("versus your later, potentially less active years?")
        report.append("")
        report.append("If your personal enjoyment values are:")
        report.append("• Conservative (1.25x/1.1x/1.0x): QOL may not be worth it")
        report.append("• Moderate (1.5x/1.2x/1.0x): QOL is a reasonable choice")
        report.append("• Aggressive (2.0x/1.4x/1.0x): QOL is strongly recommended")
        
        return "\n".join(report)
    
    def create_normalized_visualization(self, analysis_results: Dict):
        """Create visualization showing normalized enjoyment values"""
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Normalized Enjoyment Value Analysis', fontsize=16, fontweight='bold')
        
        trinity_results = analysis_results['strategy_results']['Trinity Study']
        qol_results = analysis_results['strategy_results']['QOL Enhanced']
        
        # Plot 1: Enjoyment Values by Year
        years = range(29)
        enjoyment_multipliers = [self.get_enjoyment_multiplier(year, 'moderate') for year in years]
        
        trinity_annual = np.mean(trinity_results['withdrawal_paths'], axis=0)
        qol_annual = np.mean(qol_results['withdrawal_paths'], axis=0)
        
        trinity_enjoyment_value = trinity_annual * np.array(enjoyment_multipliers)
        qol_enjoyment_value = qol_annual * np.array(enjoyment_multipliers)
        
        ax1.plot(years, trinity_annual/1000, label='Trinity Raw Income', linewidth=2, color='blue', linestyle='--')
        ax1.plot(years, trinity_enjoyment_value/1000, label='Trinity Enjoyment Value', linewidth=2, color='blue')
        ax1.plot(years, qol_annual/1000, label='QOL Raw Income', linewidth=2, color='red', linestyle='--')
        ax1.plot(years, qol_enjoyment_value/1000, label='QOL Enjoyment Value', linewidth=2, color='red')
        
        # Shade enjoyment periods
        ax1.axvspan(0, 10, alpha=0.2, color='green', label='High Enjoyment (1.5x)')
        ax1.axvspan(10, 20, alpha=0.15, color='yellow', label='Moderate Enjoyment (1.2x)')
        ax1.axvspan(20, 29, alpha=0.1, color='gray', label='Low Enjoyment (1.0x)')
        
        ax1.set_xlabel('Retirement Year')
        ax1.set_ylabel('Annual Value ($000s)')
        ax1.set_title('Raw Income vs Enjoyment-Weighted Value')
        ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Cumulative Enjoyment Value
        trinity_cumulative_value = np.cumsum(trinity_enjoyment_value)
        qol_cumulative_value = np.cumsum(qol_enjoyment_value)
        
        ax2.plot(years, trinity_cumulative_value/1000, label='Trinity Study', linewidth=2, color='blue')
        ax2.plot(years, qol_cumulative_value/1000, label='QOL Enhanced', linewidth=2, color='red')
        ax2.axvline(x=10, color='gray', linestyle='--', alpha=0.7, label='End High Enjoyment')
        ax2.axvline(x=20, color='gray', linestyle=':', alpha=0.7, label='End Moderate Enjoyment')
        
        ax2.set_xlabel('Retirement Year')
        ax2.set_ylabel('Cumulative Enjoyment Value ($000s)')
        ax2.set_title('Cumulative Enjoyment Value Comparison')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Scenario Sensitivity Analysis
        scenarios = list(analysis_results['enjoyment_scenarios'].keys())
        trinity_values = []
        qol_values = []
        qol_premiums = []
        
        for scenario in scenarios:
            trinity_values.append(trinity_results['enjoyment_results'][scenario]['avg_enjoyment_value'])
            qol_values.append(qol_results['enjoyment_results'][scenario]['avg_enjoyment_value'])
            qol_premiums.append(qol_results['enjoyment_results'][scenario]['avg_enjoyment_premium'] - 
                              trinity_results['enjoyment_results'][scenario]['avg_enjoyment_premium'])
        
        x = np.arange(len(scenarios))
        width = 0.35
        
        ax3.bar(x - width/2, np.array(trinity_values)/1000, width, label='Trinity Enjoyment Value', 
                alpha=0.7, color='blue')
        ax3.bar(x + width/2, np.array(qol_values)/1000, width, label='QOL Enjoyment Value', 
                alpha=0.7, color='red')
        
        ax3.set_xlabel('Enjoyment Scenario')
        ax3.set_ylabel('Total Enjoyment Value ($000s)')
        ax3.set_title('Enjoyment Value by Scenario')
        ax3.set_xticks(x)
        ax3.set_xticklabels([s.title() for s in scenarios])
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # Plot 4: Cost-Benefit Analysis
        risk_cost = (trinity_results['success_rate'] - qol_results['success_rate']) * 1000000
        cost_per_dollar = [risk_cost / premium if premium > 0 else 0 for premium in qol_premiums]
        
        colors = ['green' if x <= 1.0 else 'yellow' if x <= 2.0 else 'red' for x in cost_per_dollar]
        
        bars = ax4.bar(scenarios, cost_per_dollar, color=colors, alpha=0.7)
        ax4.axhline(y=1.0, color='black', linestyle='--', alpha=0.7, label='$1 Risk per $1 Enjoyment')
        ax4.axhline(y=2.0, color='orange', linestyle='--', alpha=0.7, label='$2 Risk per $1 Enjoyment')
        
        ax4.set_xlabel('Enjoyment Scenario')
        ax4.set_ylabel('Risk Cost per $ Enjoyment Benefit')
        ax4.set_title('Cost-Benefit Analysis by Scenario')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        # Add value labels
        for bar, value in zip(bars, cost_per_dollar):
            ax4.annotate(f'${value:.2f}', xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                        xytext=(0, 3), textcoords="offset points", ha='center', va='bottom')
        
        plt.tight_layout()
        
        # Save the plot
        output_dir = project_root / 'output' / 'charts'
        os.makedirs(output_dir, exist_ok=True)
        plt.savefig(f'{output_dir}/normalized_enjoyment_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return fig


def main():
    """Run the normalized enjoyment value analysis"""
    
    analyzer = NormalizedEnjoymentAnalysis()
    
    # Run the analysis
    print("Starting normalized enjoyment value analysis...")
    results = analyzer.run_normalized_analysis()
    
    # Generate comprehensive report
    report = analyzer.create_value_comparison_report(results)
    print("\n" + report)
    
    # Create visualization
    print("\n📈 Generating visualization...")
    analyzer.create_normalized_visualization(results)
    
    # Save results
    output_dir = project_root / 'output'
    os.makedirs(output_dir, exist_ok=True)
    
    with open(f'{output_dir}/normalized_enjoyment_analysis.txt', 'w') as f:
        f.write(report)
    
    print(f"\n✅ Analysis complete!")
    print(f"📋 Report: {output_dir}/normalized_enjoyment_analysis.txt")
    print(f"📊 Visualization: output/charts/normalized_enjoyment_analysis.png")


if __name__ == "__main__":
    main()