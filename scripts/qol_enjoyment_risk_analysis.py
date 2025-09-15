"""
QOL ENJOYMENT-RISK TRADE-OFF ANALYSIS

This analysis examines the fundamental question: Is the early-retirement enjoyment
from QOL strategies worth the increased portfolio depletion risk?

We'll quantify the trade-off in multiple dimensions to help retirees make
informed decisions based on their personal risk tolerance and enjoyment preferences.
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


class QOLEnjoymentRiskAnalysis:
    """
    Analyze the enjoyment-risk trade-off inherent in QOL strategies
    """
    
    def __init__(self):
        # Use the best-case scenario from our aggressive portfolio analysis
        self.portfolio_params = {
            'real_return': 0.072,  # 7.2% real return (100% stocks)
            'volatility': 0.20,    # 20% volatility
            'description': '100% Stock Portfolio (Best Case for QOL)'
        }
        
        self.results = {}
        
    def calculate_enjoyment_metrics(self, strategy_results: Dict) -> Dict:
        """
        Calculate metrics related to early retirement enjoyment
        """
        portfolio_paths = strategy_results['portfolio_paths']
        withdrawal_paths = strategy_results['withdrawal_paths']
        
        # Time-weighted enjoyment analysis
        # Assumption: Early retirement years (65-75) have higher enjoyment value
        # due to better health, energy, and opportunities for active pursuits
        
        enjoyment_weights = np.array([
            # Years 0-9 (ages 65-74): High enjoyment period
            1.5, 1.5, 1.4, 1.4, 1.3, 1.3, 1.2, 1.2, 1.1, 1.1,
            # Years 10-19 (ages 75-84): Moderate enjoyment period  
            1.0, 1.0, 0.9, 0.9, 0.8, 0.8, 0.7, 0.7, 0.6, 0.6,
            # Years 20-28 (ages 85-93): Lower enjoyment period
            0.5, 0.5, 0.4, 0.4, 0.3, 0.3, 0.2, 0.2, 0.1
        ])
        
        # Calculate enjoyment-weighted income
        years = min(withdrawal_paths.shape[1], len(enjoyment_weights))
        weighted_withdrawals = withdrawal_paths[:, :years] * enjoyment_weights[:years]
        total_weighted_enjoyment = np.mean(np.sum(weighted_withdrawals, axis=1))
        
        # Calculate early-years income concentration
        early_years_income = np.mean(np.sum(withdrawal_paths[:, :10], axis=1))  # First 10 years
        total_income = np.mean(np.sum(withdrawal_paths, axis=1))
        early_concentration_ratio = early_years_income / total_income
        
        # Calculate "active retirement" benefit (years 0-14)
        active_years_income = np.mean(np.sum(withdrawal_paths[:, :15], axis=1))
        active_concentration_ratio = active_years_income / total_income
        
        return {
            'total_weighted_enjoyment': total_weighted_enjoyment,
            'early_concentration_ratio': early_concentration_ratio,
            'active_concentration_ratio': active_concentration_ratio,
            'early_years_income': early_years_income,
            'active_years_income': active_years_income,
            'total_income': total_income
        }
    
    def calculate_risk_adjusted_enjoyment(self, trinity_results: Dict, qol_results: Dict) -> Dict:
        """
        Calculate risk-adjusted enjoyment metrics comparing QOL to Trinity
        """
        trinity_enjoyment = self.calculate_enjoyment_metrics(trinity_results)
        qol_enjoyment = self.calculate_enjoyment_metrics(qol_results)
        
        # Calculate enjoyment premium
        enjoyment_premium = (qol_enjoyment['total_weighted_enjoyment'] / 
                           trinity_enjoyment['total_weighted_enjoyment'] - 1) * 100
        
        # Calculate risk penalty  
        risk_penalty = (trinity_results['success_rate'] - qol_results['success_rate']) * 100
        
        # Risk-adjusted enjoyment ratio
        if risk_penalty > 0:
            risk_adjusted_enjoyment = enjoyment_premium / risk_penalty
        else:
            risk_adjusted_enjoyment = float('inf')
        
        # Early years advantage
        early_advantage = ((qol_enjoyment['early_concentration_ratio'] / 
                           trinity_enjoyment['early_concentration_ratio']) - 1) * 100
        
        return {
            'enjoyment_premium_pct': enjoyment_premium,
            'risk_penalty_pct': risk_penalty,
            'risk_adjusted_enjoyment': risk_adjusted_enjoyment,
            'early_years_advantage_pct': early_advantage,
            'qol_early_concentration': qol_enjoyment['early_concentration_ratio'],
            'trinity_early_concentration': trinity_enjoyment['early_concentration_ratio'],
            'qol_active_income': qol_enjoyment['active_years_income'],
            'trinity_active_income': trinity_enjoyment['active_years_income']
        }
    
    def run_enjoyment_analysis(self) -> Dict:
        """Run comprehensive enjoyment-risk analysis"""
        
        print("🎯 QOL ENJOYMENT-RISK TRADE-OFF ANALYSIS")
        print("=" * 60)
        print(f"Portfolio: {self.portfolio_params['description']}")
        print(f"Real Return: {self.portfolio_params['real_return']*100:.1f}%")
        print(f"Volatility: {self.portfolio_params['volatility']*100:.1f}%")
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
            
            final_values = portfolio_paths[:, -1]
            success_rate = np.mean(final_values > 0)
            
            strategy_results[strategy_name] = {
                'success_rate': success_rate,
                'portfolio_paths': portfolio_paths,
                'withdrawal_paths': withdrawal_paths,
                'avg_final_value': np.mean(final_values),
                'total_withdrawals': np.mean(np.sum(withdrawal_paths, axis=1))
            }
        
        # Calculate enjoyment-risk trade-offs
        trade_off_analysis = self.calculate_risk_adjusted_enjoyment(
            strategy_results['Trinity Study'], 
            strategy_results['QOL Enhanced']
        )
        
        return {
            'strategy_results': strategy_results,
            'trade_off_analysis': trade_off_analysis,
            'portfolio_params': self.portfolio_params
        }
    
    def create_decision_framework(self, analysis_results: Dict) -> str:
        """
        Create a decision framework to help retirees evaluate the trade-off
        """
        trade_off = analysis_results['trade_off_analysis']
        trinity_results = analysis_results['strategy_results']['Trinity Study']
        qol_results = analysis_results['strategy_results']['QOL Enhanced']
        
        framework = []
        framework.append("=" * 80)
        framework.append("🎯 QOL DECISION FRAMEWORK: IS THE ENJOYMENT WORTH THE RISK?")
        framework.append("=" * 80)
        framework.append("")
        
        framework.append("📊 THE TRADE-OFF QUANTIFIED")
        framework.append("-" * 40)
        framework.append(f"• QOL provides {trade_off['enjoyment_premium_pct']:.1f}% more enjoyment-weighted income")
        framework.append(f"• QOL increases portfolio failure risk by {trade_off['risk_penalty_pct']:.1f}%")
        framework.append(f"• Risk-adjusted enjoyment ratio: {trade_off['risk_adjusted_enjoyment']:.2f}")
        framework.append("")
        
        framework.append("🏃 EARLY RETIREMENT ADVANTAGE")
        framework.append("-" * 40)
        framework.append(f"• QOL concentrates {trade_off['qol_early_concentration']*100:.1f}% of income in first 10 years")
        framework.append(f"• Trinity concentrates {trade_off['trinity_early_concentration']*100:.1f}% of income in first 10 years")
        framework.append(f"• QOL early-years advantage: {trade_off['early_years_advantage_pct']:.1f}%")
        framework.append("")
        
        framework.append("💰 ACTIVE RETIREMENT INCOME (Ages 65-79)")
        framework.append("-" * 40)
        framework.append(f"• QOL active retirement income: ${trade_off['qol_active_income']:,.0f}")
        framework.append(f"• Trinity active retirement income: ${trade_off['trinity_active_income']:,.0f}")
        framework.append(f"• QOL advantage: ${trade_off['qol_active_income'] - trade_off['trinity_active_income']:,.0f}")
        framework.append("")
        
        framework.append("⚖️ RISK COMPARISON")
        framework.append("-" * 40)
        framework.append(f"• Trinity Study success rate: {trinity_results['success_rate']*100:.1f}%")
        framework.append(f"• QOL Enhanced success rate: {qol_results['success_rate']*100:.1f}%") 
        framework.append(f"• Additional failure risk: {trade_off['risk_penalty_pct']:.1f} percentage points")
        framework.append("")
        
        # Decision guidance based on trade-off ratio
        framework.append("🎯 DECISION GUIDANCE")
        framework.append("-" * 40)
        
        if trade_off['risk_adjusted_enjoyment'] >= 1.0:
            recommendation = "🟢 QOL MAY BE WORTH CONSIDERING"
            explanation = "The enjoyment premium exceeds the risk penalty."
        elif trade_off['risk_adjusted_enjoyment'] >= 0.5:
            recommendation = "🟡 QOL IS A PERSONAL CHOICE"
            explanation = "Moderate enjoyment benefit with moderate additional risk."
        else:
            recommendation = "🔴 QOL DIFFICULT TO JUSTIFY"
            explanation = "Low enjoyment benefit relative to significant additional risk."
        
        framework.append(f"{recommendation}")
        framework.append(f"• {explanation}")
        framework.append(f"• Enjoyment-to-risk ratio: {trade_off['risk_adjusted_enjoyment']:.2f}")
        framework.append("")
        
        framework.append("👤 PERSONAL FACTORS TO CONSIDER")
        framework.append("-" * 40)
        framework.append("Consider QOL if you:")
        framework.append("• Highly value early retirement experiences (travel, adventure, family time)")
        framework.append("• Have concerns about health limiting later enjoyment")
        framework.append("• Prefer front-loaded spending over wealth preservation")
        framework.append("• Can accept higher portfolio depletion risk")
        framework.append("• Have other income sources or safety nets")
        framework.append("")
        framework.append("Prefer Trinity if you:")
        framework.append("• Prioritize portfolio preservation and legacy")
        framework.append("• Want lower risk of running out of money")
        framework.append("• Value consistent income throughout retirement")
        framework.append("• Worry about longevity risk (living beyond age 94)")
        framework.append("• Prefer to leave inheritance for heirs")
        framework.append("")
        
        framework.append("🔢 BREAK-EVEN ANALYSIS")
        framework.append("-" * 40)
        early_extra = trade_off['qol_active_income'] - trade_off['trinity_active_income']
        risk_cost = trade_off['risk_penalty_pct'] / 100 * 1000000  # Risk cost in portfolio value terms
        
        framework.append(f"• Extra early income from QOL: ${early_extra:,.0f}")
        framework.append(f"• Implied risk cost: ${risk_cost:,.0f} in portfolio value")
        framework.append(f"• Cost per dollar of early income: ${risk_cost/early_extra:.2f}")
        framework.append("")
        framework.append("The question: Is it worth paying ${:.2f} in portfolio risk".format(risk_cost/early_extra))
        framework.append("for each additional dollar of early retirement income?")
        
        return "\n".join(framework)
    
    def create_visualization(self, analysis_results: Dict):
        """Create comprehensive visualization of the enjoyment-risk trade-off"""
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('QOL Enjoyment-Risk Trade-off Analysis', fontsize=16, fontweight='bold')
        
        trinity_results = analysis_results['strategy_results']['Trinity Study']
        qol_results = analysis_results['strategy_results']['QOL Enhanced']
        trade_off = analysis_results['trade_off_analysis']
        
        # Plot 1: Annual Income Comparison by Year
        years = range(29)
        trinity_annual = np.mean(trinity_results['withdrawal_paths'], axis=0)
        qol_annual = np.mean(qol_results['withdrawal_paths'], axis=0)
        
        ax1.plot(years, trinity_annual/1000, label='Trinity Study', linewidth=2, color='blue')
        ax1.plot(years, qol_annual/1000, label='QOL Enhanced', linewidth=2, color='red')
        ax1.fill_between(years[:10], 0, max(qol_annual/1000), alpha=0.2, color='lightgreen', 
                        label='High Enjoyment Period')
        ax1.set_xlabel('Retirement Year')
        ax1.set_ylabel('Annual Income ($000s)')
        ax1.set_title('Annual Income: QOL Front-Loading vs Trinity Consistency')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Cumulative Income Race
        trinity_cumulative = np.cumsum(trinity_annual)
        qol_cumulative = np.cumsum(qol_annual)
        
        ax2.plot(years, trinity_cumulative/1000, label='Trinity Study', linewidth=2, color='blue')
        ax2.plot(years, qol_cumulative/1000, label='QOL Enhanced', linewidth=2, color='red')
        ax2.axvline(x=10, color='gray', linestyle='--', alpha=0.7, label='End of High Enjoyment')
        ax2.set_xlabel('Retirement Year')
        ax2.set_ylabel('Cumulative Income ($000s)')
        ax2.set_title('Cumulative Income: When Does QOL Advantage Peak?')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Portfolio Survival Curves
        trinity_survival = []
        qol_survival = []
        
        for year in range(29):
            trinity_survival.append(np.mean(trinity_results['portfolio_paths'][:, year] > 0) * 100)
            qol_survival.append(np.mean(qol_results['portfolio_paths'][:, year] > 0) * 100)
        
        ax3.plot(years, trinity_survival, label='Trinity Study', linewidth=2, color='blue')
        ax3.plot(years, qol_survival, label='QOL Enhanced', linewidth=2, color='red')
        ax3.axhline(y=50, color='gray', linestyle='--', alpha=0.7, label='50% Survival Threshold')
        ax3.set_xlabel('Retirement Year')
        ax3.set_ylabel('Portfolio Survival Rate (%)')
        ax3.set_title('Portfolio Survival: The Cost of Front-Loading')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # Plot 4: Risk-Return Trade-off Summary
        strategies = ['Trinity\nStudy', 'QOL\nEnhanced']
        success_rates = [trinity_results['success_rate']*100, qol_results['success_rate']*100]
        enjoyment_scores = [100, 100 + trade_off['enjoyment_premium_pct']]  # Relative to Trinity = 100
        
        x = np.arange(len(strategies))
        width = 0.35
        
        bars1 = ax4.bar(x - width/2, success_rates, width, label='Success Rate (%)', alpha=0.7, color='lightblue')
        bars2 = ax4.bar(x + width/2, enjoyment_scores, width, label='Enjoyment Score', alpha=0.7, color='lightcoral')
        
        ax4.set_xlabel('Strategy')
        ax4.set_ylabel('Percentage')
        ax4.set_title(f'Trade-off Summary\nRisk-Adjusted Enjoyment: {trade_off["risk_adjusted_enjoyment"]:.2f}')
        ax4.set_xticks(x)
        ax4.set_xticklabels(strategies)
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        # Add value labels on bars
        for bar in bars1:
            height = bar.get_height()
            ax4.annotate(f'{height:.1f}%', xy=(bar.get_x() + bar.get_width()/2, height),
                        xytext=(0, 3), textcoords="offset points", ha='center', va='bottom')
        
        for bar in bars2:
            height = bar.get_height()
            ax4.annotate(f'{height:.1f}', xy=(bar.get_x() + bar.get_width()/2, height),
                        xytext=(0, 3), textcoords="offset points", ha='center', va='bottom')
        
        plt.tight_layout()
        
        # Save the plot
        output_dir = project_root / 'output' / 'charts'
        os.makedirs(output_dir, exist_ok=True)
        plt.savefig(f'{output_dir}/qol_enjoyment_risk_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return fig


def main():
    """Run the QOL enjoyment-risk analysis"""
    
    analyzer = QOLEnjoymentRiskAnalysis()
    
    # Run the analysis
    results = analyzer.run_enjoyment_analysis()
    
    # Generate decision framework
    decision_framework = analyzer.create_decision_framework(results)
    print("\n" + decision_framework)
    
    # Create visualization
    print("\n📈 Generating visualization...")
    analyzer.create_visualization(results)
    
    # Save results
    output_dir = project_root / 'output'
    os.makedirs(output_dir, exist_ok=True)
    
    with open(f'{output_dir}/qol_enjoyment_risk_analysis.txt', 'w') as f:
        f.write(decision_framework)
        
        # Add detailed data appendix
        f.write("\n\n" + "="*80)
        f.write("\nDETAILED ANALYSIS DATA")
        f.write("\n" + "="*80)
        
        trade_off = results['trade_off_analysis']
        f.write(f"\nEnjoyment Premium: {trade_off['enjoyment_premium_pct']:.2f}%")
        f.write(f"\nRisk Penalty: {trade_off['risk_penalty_pct']:.2f}%")
        f.write(f"\nRisk-Adjusted Enjoyment: {trade_off['risk_adjusted_enjoyment']:.3f}")
        f.write(f"\nEarly Years Advantage: {trade_off['early_years_advantage_pct']:.2f}%")
        
        trinity = results['strategy_results']['Trinity Study']
        qol = results['strategy_results']['QOL Enhanced']
        f.write(f"\n\nTrinity Success Rate: {trinity['success_rate']*100:.1f}%")
        f.write(f"\nQOL Success Rate: {qol['success_rate']*100:.1f}%")
        f.write(f"\nTrinity Total Income: ${trinity['total_withdrawals']:,.0f}")
        f.write(f"\nQOL Total Income: ${qol['total_withdrawals']:,.0f}")
    
    print(f"\n✅ Analysis complete!")
    print(f"📋 Decision Framework: {output_dir}/qol_enjoyment_risk_analysis.txt")
    print(f"📊 Visualization: output/charts/qol_enjoyment_risk_analysis.png")


if __name__ == "__main__":
    main()