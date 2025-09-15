"""
Aggressive Portfolio Analysis for QOL Framework

This script analyzes how different portfolio allocations affect the viability
of QOL strategies compared to the Trinity Study approach.

Historical Real Returns (1926-2023):
- Conservative (30/70 Stocks/Bonds): ~3.5% real, 12% volatility  
- Moderate (60/40 Stocks/Bonds): ~5.5% real, 15% volatility
- Aggressive (80/20 Stocks/Bonds): ~6.8% real, 18% volatility
- Very Aggressive (100% Stocks): ~7.2% real, 20% volatility

Current framework uses: 1.5% real, 15% volatility (too conservative)
"""

import sys
import os
from pathlib import Path
import numpy as np

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


class PortfolioAllocationAnalysis:
    """
    Analyze QOL strategies across different portfolio allocations
    """
    
    def __init__(self):
        self.portfolio_allocations = {
            'conservative': {
                'name': 'Conservative (30/70)',
                'real_return': 0.035,  # 3.5% real return
                'volatility': 0.12,    # 12% volatility
                'description': '30% stocks, 70% bonds'
            },
            'moderate': {
                'name': 'Moderate (60/40)', 
                'real_return': 0.055,  # 5.5% real return
                'volatility': 0.15,    # 15% volatility
                'description': '60% stocks, 40% bonds'
            },
            'aggressive': {
                'name': 'Aggressive (80/20)',
                'real_return': 0.068,  # 6.8% real return
                'volatility': 0.18,    # 18% volatility  
                'description': '80% stocks, 20% bonds'
            },
            'very_aggressive': {
                'name': 'Very Aggressive (100/0)',
                'real_return': 0.072,  # 7.2% real return
                'volatility': 0.20,    # 20% volatility
                'description': '100% stocks'
            }
        }
        
        self.current_framework = {
            'name': 'Current Framework',
            'real_return': 0.015,  # 1.5% real return (too conservative)
            'volatility': 0.15,    # 15% volatility
            'description': 'Current conservative parameters'
        }
        
        self.results = {}
        
    def run_portfolio_analysis(self, allocation_key: str, n_simulations: int = 1000) -> Dict:
        """Run QOL analysis for a specific portfolio allocation"""
        
        allocation = self.portfolio_allocations[allocation_key]
        
        print(f"\n🔍 Analyzing {allocation['name']}")
        print(f"   Real Return: {allocation['real_return']*100:.1f}%")
        print(f"   Volatility: {allocation['volatility']*100:.1f}%")
        print(f"   {allocation['description']}")
        
        # Initialize enhanced QOL analysis
        analyzer = EnhancedQOLAnalysis(
            starting_value=1000000,
            starting_age=65, 
            horizon_years=29,  # Match our previous analysis
            n_simulations=n_simulations
        )
        
        # Run simulation for each strategy we want to compare
        strategies = {
            'Trinity Study': ('trinity_4pct', {}),
            'QOL Conservative': ('hauenstein', {'phase1': 1.20, 'phase2': 1.05, 'phase3': 0.95}),  # Less aggressive QOL
            'QOL Moderate': ('hauenstein', {'phase1': 1.275, 'phase2': 1.1, 'phase3': 0.91}),     # Medium QOL
            'QOL Enhanced': ('hauenstein', {'phase1': 1.35, 'phase2': 1.125, 'phase3': 0.875})   # Standard QOL
        }
        
        strategy_results = {}
        
        for strategy_name, (strategy_key, qol_params) in strategies.items():
            
            # Configure QOL rates if this is a QOL strategy
            if qol_params:
                analyzer.qol_phase1_rate = qol_params['phase1'] * 0.04  # Convert multiplier to rate
                analyzer.qol_phase2_rate = qol_params['phase2'] * 0.04
                analyzer.qol_phase3_rate = qol_params['phase3'] * 0.04
            
            # Run simulation
            analyzer.run_enhanced_simulation(
                withdrawal_strategy=strategy_key,
                return_volatility=allocation['volatility'],
                base_real_return=allocation['real_return'],
                base_inflation=0.03,
                qol_variability=False,
                verbose=False
            )
            
            # Extract results
            portfolio_paths = np.array(analyzer.simulation_results['portfolio_paths'])
            withdrawal_paths = np.array(analyzer.simulation_results['withdrawal_paths'])
            
            # Calculate success rate (portfolio survives)
            final_values = portfolio_paths[:, -1]
            success_rate = np.mean(final_values > 0)
            
            # Calculate total withdrawals and average final value
            total_withdrawals = np.mean(np.sum(withdrawal_paths, axis=1))
            avg_final_value = np.mean(final_values)
            
            strategy_results[strategy_name] = {
                'success_rate': success_rate,
                'total_withdrawals': total_withdrawals,
                'avg_final_value': avg_final_value,
                'portfolio_paths': portfolio_paths,
                'withdrawal_paths': withdrawal_paths
            }
        
        return {'strategy_results': strategy_results}
    
    def compare_allocations(self, n_simulations: int = 1000) -> pd.DataFrame:
        """Compare all allocations and create summary table"""
        
        print("=" * 80)
        print("🚀 AGGRESSIVE PORTFOLIO ALLOCATION ANALYSIS")
        print("=" * 80)
        
        comparison_data = []
        
        # Run analysis for each allocation
        for allocation_key in self.portfolio_allocations.keys():
            results = self.run_portfolio_analysis(allocation_key, n_simulations)
            self.results[allocation_key] = results
            
            allocation = self.portfolio_allocations[allocation_key]
            
            # Extract key metrics for each strategy
            for strategy_name, strategy_results in results['strategy_results'].items():
                comparison_data.append({
                    'Portfolio': allocation['name'],
                    'Real_Return': f"{allocation['real_return']*100:.1f}%",
                    'Volatility': f"{allocation['volatility']*100:.1f}%", 
                    'Strategy': strategy_name,
                    'Success_Rate': f"{strategy_results['success_rate']*100:.1f}%",
                    'Avg_Final_Value': f"${strategy_results['avg_final_value']:,.0f}",
                    'Total_Withdrawals': f"${strategy_results['total_withdrawals']:,.0f}",
                    'Depletion_Risk': f"{(1-strategy_results['success_rate'])*100:.1f}%",
                    'Sharpe_Approx': strategy_results['total_withdrawals'] / (1000000 * (1-strategy_results['success_rate']) + 0.01)  # Risk-adjusted return proxy
                })
        
        return pd.DataFrame(comparison_data)
    
    def analyze_qol_viability(self) -> Dict:
        """
        Analyze when QOL strategies become attractive vs Trinity Study
        """
        print("\n" + "=" * 60)
        print("📊 QOL STRATEGY VIABILITY ANALYSIS")
        print("=" * 60)
        
        viability_analysis = {}
        
        for allocation_key, results in self.results.items():
            allocation = self.portfolio_allocations[allocation_key]
            trinity_results = results['strategy_results']['Trinity Study']
            qol_enhanced_results = results['strategy_results']['QOL Enhanced'] 
            
            # Calculate key metrics
            trinity_income = trinity_results['total_withdrawals']
            qol_income = qol_enhanced_results['total_withdrawals']
            
            trinity_success = trinity_results['success_rate']
            qol_success = qol_enhanced_results['success_rate']
            
            income_advantage = (qol_income / trinity_income - 1) * 100
            risk_penalty = (trinity_success - qol_success) * 100
            
            # Risk-adjusted income (income per unit of additional risk)
            if risk_penalty > 0:
                risk_adjusted_advantage = income_advantage / risk_penalty
            else:
                risk_adjusted_advantage = float('inf')  # QOL has better success rate
                
            viability_analysis[allocation_key] = {
                'allocation': allocation['name'],
                'real_return': allocation['real_return'],
                'volatility': allocation['volatility'],
                'income_advantage_pct': income_advantage,
                'risk_penalty_pct': risk_penalty,
                'risk_adjusted_advantage': risk_adjusted_advantage,
                'trinity_success': trinity_success,
                'qol_success': qol_success,
                'recommendation': self._get_recommendation(income_advantage, risk_penalty, risk_adjusted_advantage)
            }
            
        return viability_analysis
    
    def _get_recommendation(self, income_adv: float, risk_penalty: float, risk_adj_adv: float) -> str:
        """Generate recommendation based on metrics"""
        
        if risk_penalty <= 0:
            return "🟢 QOL STRONGLY RECOMMENDED - Higher income with equal/better safety"
        elif risk_adj_adv >= 2.0:
            return "🟢 QOL RECOMMENDED - Excellent risk-adjusted returns"  
        elif risk_adj_adv >= 1.0:
            return "🟡 QOL VIABLE - Good risk-adjusted returns"
        elif risk_adj_adv >= 0.5:
            return "🟡 QOL MARGINAL - Modest risk-adjusted benefit"
        else:
            return "🔴 QOL NOT RECOMMENDED - Poor risk-adjusted returns"
    
    def create_visualization(self):
        """Create comprehensive visualization of results"""
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Portfolio Allocation Impact on QOL Strategy Viability', fontsize=16, fontweight='bold')
        
        # Prepare data for plotting
        allocations = list(self.portfolio_allocations.keys())
        returns = [self.portfolio_allocations[k]['real_return']*100 for k in allocations]
        volatilities = [self.portfolio_allocations[k]['volatility']*100 for k in allocations]
        
        trinity_incomes = []
        qol_incomes = []
        trinity_success = []
        qol_success = []
        
        for allocation_key in allocations:
            results = self.results[allocation_key]['strategy_results']
            trinity_incomes.append(results['Trinity Study']['total_withdrawals'] / 1000)  # Convert to thousands
            qol_incomes.append(results['QOL Enhanced']['total_withdrawals'] / 1000)
            trinity_success.append(results['Trinity Study']['success_rate'] * 100)
            qol_success.append(results['QOL Enhanced']['success_rate'] * 100)
        
        # Plot 1: Income Comparison
        x = np.arange(len(allocations))
        width = 0.35
        
        ax1.bar(x - width/2, trinity_incomes, width, label='Trinity Study', alpha=0.7, color='blue')
        ax1.bar(x + width/2, qol_incomes, width, label='QOL Enhanced', alpha=0.7, color='red')
        ax1.set_xlabel('Portfolio Allocation')
        ax1.set_ylabel('Total Income ($000s)')
        ax1.set_title('Total Retirement Income by Strategy')
        ax1.set_xticks(x)
        ax1.set_xticklabels([self.portfolio_allocations[k]['name'].split('(')[0].strip() for k in allocations], rotation=45)
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Success Rate Comparison  
        ax2.bar(x - width/2, trinity_success, width, label='Trinity Study', alpha=0.7, color='blue')
        ax2.bar(x + width/2, qol_success, width, label='QOL Enhanced', alpha=0.7, color='red')
        ax2.set_xlabel('Portfolio Allocation')
        ax2.set_ylabel('Success Rate (%)')
        ax2.set_title('Portfolio Preservation Success Rate')
        ax2.set_xticks(x)
        ax2.set_xticklabels([self.portfolio_allocations[k]['name'].split('(')[0].strip() for k in allocations], rotation=45)
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Risk vs Return Scatter
        for i, allocation_key in enumerate(allocations):
            allocation = self.portfolio_allocations[allocation_key]
            ax3.scatter(volatilities[i], returns[i], s=150, alpha=0.7, 
                       label=allocation['name'].split('(')[0].strip())
        
        ax3.set_xlabel('Volatility (%)')
        ax3.set_ylabel('Expected Real Return (%)')
        ax3.set_title('Portfolio Risk-Return Profile')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # Plot 4: QOL Income Advantage vs Risk Penalty
        viability = self.analyze_qol_viability()
        income_advantages = [viability[k]['income_advantage_pct'] for k in allocations]
        risk_penalties = [viability[k]['risk_penalty_pct'] for k in allocations]
        colors = ['red' if x < 0 else 'green' for x in income_advantages]
        
        ax4.scatter(risk_penalties, income_advantages, s=150, c=colors, alpha=0.7)
        
        for i, allocation_key in enumerate(allocations):
            ax4.annotate(self.portfolio_allocations[allocation_key]['name'].split('(')[0].strip(), 
                        (risk_penalties[i], income_advantages[i]), 
                        xytext=(5, 5), textcoords='offset points', fontsize=9)
        
        ax4.axhline(y=0, color='black', linestyle='--', alpha=0.5)
        ax4.axvline(x=0, color='black', linestyle='--', alpha=0.5)
        ax4.set_xlabel('Risk Penalty (% lower success rate)')
        ax4.set_ylabel('Income Advantage (% higher income)')
        ax4.set_title('QOL Enhanced vs Trinity Study Trade-off')
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Save the plot
        output_dir = project_root / 'output' / 'charts'
        os.makedirs(output_dir, exist_ok=True)
        plt.savefig(f'{output_dir}/aggressive_portfolio_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return fig
    
    def generate_report(self) -> str:
        """Generate comprehensive text report"""
        
        viability = self.analyze_qol_viability()
        
        report = []
        report.append("=" * 80)
        report.append("🚀 AGGRESSIVE PORTFOLIO ANALYSIS REPORT")
        report.append("=" * 80)
        report.append("")
        
        report.append("📋 EXECUTIVE SUMMARY")
        report.append("-" * 40)
        report.append("Analysis of QOL strategy viability across different portfolio allocations:")
        report.append(f"• Conservative (30/70): 3.5% real return, 12% volatility")
        report.append(f"• Moderate (60/40): 5.5% real return, 15% volatility") 
        report.append(f"• Aggressive (80/20): 6.8% real return, 18% volatility")
        report.append(f"• Very Aggressive (100/0): 7.2% real return, 20% volatility")
        report.append("")
        
        report.append("🎯 KEY FINDINGS")
        report.append("-" * 40)
        
        for allocation_key in self.portfolio_allocations.keys():
            analysis = viability[allocation_key]
            report.append(f"")
            report.append(f"{analysis['allocation']}:")
            report.append(f"  • QOL income advantage: {analysis['income_advantage_pct']:+.1f}%")
            report.append(f"  • Risk penalty: {analysis['risk_penalty_pct']:+.1f}%")
            report.append(f"  • Risk-adjusted advantage: {analysis['risk_adjusted_advantage']:.2f}")
            report.append(f"  • {analysis['recommendation']}")
        
        # Find the best allocation for QOL
        best_allocation = max(viability.keys(), 
                            key=lambda k: viability[k]['risk_adjusted_advantage'])
        best_analysis = viability[best_allocation]
        
        report.append("")
        report.append("🏆 OPTIMAL ALLOCATION FOR QOL")
        report.append("-" * 40)
        report.append(f"Best allocation: {best_analysis['allocation']}")
        report.append(f"Risk-adjusted advantage: {best_analysis['risk_adjusted_advantage']:.2f}")
        report.append(f"{best_analysis['recommendation']}")
        
        return "\n".join(report)


def main():
    """Run the aggressive portfolio analysis"""
    
    # Create analyzer
    analyzer = PortfolioAllocationAnalysis()
    
    # Run comprehensive comparison
    print("🚀 Starting Aggressive Portfolio Allocation Analysis...")
    comparison_df = analyzer.compare_allocations(n_simulations=1000)
    
    # Display results table
    print("\n📊 STRATEGY COMPARISON ACROSS ALLOCATIONS")
    print("=" * 120)
    print(comparison_df.to_string(index=False))
    
    # Analyze QOL viability
    viability_analysis = analyzer.analyze_qol_viability()
    
    # Generate and display report
    report = analyzer.generate_report()
    print("\n" + report)
    
    # Create visualization
    print("\n📈 Generating visualization...")
    analyzer.create_visualization()
    
    # Save detailed results
    output_dir = project_root / 'output'
    os.makedirs(output_dir, exist_ok=True)
    
    # Save comparison table
    comparison_df.to_csv(f'{output_dir}/aggressive_portfolio_comparison.csv', index=False)
    
    # Save detailed report
    with open(f'{output_dir}/aggressive_portfolio_report.txt', 'w') as f:
        f.write(report)
        f.write("\n\n" + "="*80)
        f.write("\nDETAILED COMPARISON TABLE\n")
        f.write("="*80 + "\n")
        f.write(comparison_df.to_string(index=False))
    
    print(f"\n✅ Analysis complete! Results saved to {output_dir}/")
    print(f"📊 Chart: output/charts/aggressive_portfolio_analysis.png")
    print(f"📋 Report: output/aggressive_portfolio_report.txt")
    print(f"📊 Data: output/aggressive_portfolio_comparison.csv")


if __name__ == "__main__":
    main()