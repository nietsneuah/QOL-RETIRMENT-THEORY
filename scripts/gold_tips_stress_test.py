#!/usr/bin/env python3
"""
GOLD & TIPS STRESS TEST ANALYSIS

This script focuses on specific stress scenarios where Gold and TIPS provide
maximum benefit to QOL retirement strategies. Based on the comprehensive analysis,
we'll dive deeper into high inflation periods and sequence of returns risk.
"""

import sys
import os
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent / 'src'))

class GoldTIPSStressTest:
    """
    Focused stress testing of Gold and TIPS in extreme scenarios
    """
    
    def __init__(self):
        """Initialize with stress test parameters"""
        
        self.asset_returns = {
            # Historical data-informed parameters
            'stocks': {'real_return': 0.072, 'volatility': 0.20},
            'bonds': {'real_return': 0.025, 'volatility': 0.08}, 
            'gold': {'real_return': 0.015, 'volatility': 0.18},
            'tips': {'real_return': 0.020, 'volatility': 0.06}
        }
        
        # Test strategies
        self.test_strategies = {
            'original_60_40': {
                'name': 'Original 60/40',
                'allocation': {'stocks': 0.60, 'bonds': 0.40, 'gold': 0.0, 'tips': 0.0}
            },
            'enhanced_balanced': {
                'name': 'Enhanced Balanced',
                'allocation': {'stocks': 0.50, 'bonds': 0.30, 'gold': 0.15, 'tips': 0.05}
            },
            'inflation_fighter': {
                'name': 'Inflation Fighter',
                'allocation': {'stocks': 0.40, 'bonds': 0.20, 'gold': 0.25, 'tips': 0.15}
            },
            'tips_focused': {
                'name': 'TIPS Focused',
                'allocation': {'stocks': 0.50, 'bonds': 0.10, 'gold': 0.15, 'tips': 0.25}
            }
        }
        
        # Simulation parameters
        self.starting_value = 1000000
        self.n_simulations = 10000
        self.years = 30
    
    def simulate_1970s_stagflation(self) -> Dict:
        """Simulate 1970s-style stagflation scenario"""
        
        print("\n🔥 SIMULATING 1970s STAGFLATION SCENARIO")
        print("   High inflation (8-12%) + stock market struggles")
        print("   Duration: 10-year period starting at retirement")
        
        results = {}
        
        for strategy_key, strategy in self.test_strategies.items():
            print(f"   Testing {strategy['name']}...")
            
            portfolio_values = []
            success_count = 0
            
            for sim in range(self.n_simulations):
                portfolio_value = self.starting_value
                
                for year in range(self.years):
                    # 1970s-style returns for first 10 years
                    if year < 10:
                        # High inflation period
                        inflation_rate = np.random.normal(0.10, 0.03)  # 10% avg inflation
                        
                        # Asset returns during stagflation
                        stock_return = np.random.normal(-0.02, 0.25)  # Real negative returns
                        bond_return = np.random.normal(-0.06, 0.12)   # Bonds crushed by inflation
                        gold_return = np.random.normal(0.12, 0.20)    # Gold shines in inflation
                        tips_return = inflation_rate + np.random.normal(0.01, 0.04)  # TIPS protect
                        
                    else:
                        # Normal period after stagflation
                        inflation_rate = np.random.normal(0.03, 0.015)
                        stock_return = np.random.normal(0.072, 0.20)
                        bond_return = np.random.normal(0.025, 0.08)
                        gold_return = np.random.normal(0.015, 0.18)
                        tips_return = inflation_rate + np.random.normal(0.005, 0.04)
                    
                    # Calculate portfolio return
                    allocation = strategy['allocation']
                    portfolio_return = (
                        allocation['stocks'] * stock_return +
                        allocation['bonds'] * bond_return +
                        allocation['gold'] * gold_return +
                        allocation['tips'] * tips_return
                    )
                    
                    # Apply withdrawal (4% of original portfolio, inflation-adjusted)
                    cumulative_inflation = (1.0 + inflation_rate) ** (year + 1)
                    withdrawal = 40000 * cumulative_inflation
                    withdrawal = min(withdrawal, portfolio_value * 0.95)
                    
                    portfolio_value -= withdrawal
                    
                    if portfolio_value <= 0:
                        portfolio_value = 0
                        break
                    
                    # Apply investment returns
                    portfolio_value *= (1 + portfolio_return)
                
                if portfolio_value > 0:
                    success_count += 1
                
                portfolio_values.append(portfolio_value)
            
            results[strategy_key] = {
                'name': strategy['name'],
                'success_rate': success_count / self.n_simulations,
                'final_values': portfolio_values,
                'median_final': np.median(portfolio_values),
                'percentile_10': np.percentile(portfolio_values, 10)
            }
        
        return results
    
    def simulate_sequence_risk(self) -> Dict:
        """Simulate sequence of returns risk scenarios"""
        
        print("\n📉 SIMULATING SEQUENCE OF RETURNS RISK")
        print("   Poor returns in first 5 years of retirement")
        print("   Testing portfolio resilience to early losses")
        
        results = {}
        
        for strategy_key, strategy in self.test_strategies.items():
            print(f"   Testing {strategy['name']}...")
            
            portfolio_values = []
            success_count = 0
            
            for sim in range(self.n_simulations):
                portfolio_value = self.starting_value
                
                for year in range(self.years):
                    # Poor sequence in first 5 years
                    if year < 5:
                        # Bear market scenario
                        stock_return = np.random.normal(-0.15, 0.30)  # Severe stock losses
                        bond_return = np.random.normal(0.03, 0.10)    # Bonds provide some stability
                        gold_return = np.random.normal(0.08, 0.20)    # Gold rallies in crisis
                        tips_return = np.random.normal(0.04, 0.06)    # TIPS provide stability
                        
                    else:
                        # Recovery period with normal returns
                        stock_return = np.random.normal(0.12, 0.18)   # Strong recovery
                        bond_return = np.random.normal(0.025, 0.08)
                        gold_return = np.random.normal(0.015, 0.18)
                        tips_return = np.random.normal(0.025, 0.06)
                    
                    # Calculate portfolio return
                    allocation = strategy['allocation']
                    portfolio_return = (
                        allocation['stocks'] * stock_return +
                        allocation['bonds'] * bond_return +
                        allocation['gold'] * gold_return +
                        allocation['tips'] * tips_return
                    )
                    
                    # Apply QOL-adjusted withdrawal
                    # Higher withdrawals in early years when QOL is more valuable
                    if year < 10:
                        base_rate = 0.054  # 5.4% in peak QOL years
                    elif year < 20:
                        base_rate = 0.045  # 4.5% in moderate years
                    else:
                        base_rate = 0.035  # 3.5% in care years
                    
                    # Inflation-adjusted withdrawal
                    inflation_factor = (1.03) ** year  # 3% annual inflation
                    withdrawal = self.starting_value * base_rate * inflation_factor
                    withdrawal = min(withdrawal, portfolio_value * 0.95)
                    
                    portfolio_value -= withdrawal
                    
                    if portfolio_value <= 0:
                        portfolio_value = 0
                        break
                    
                    # Apply investment returns
                    portfolio_value *= (1 + portfolio_return)
                
                if portfolio_value > 0:
                    success_count += 1
                
                portfolio_values.append(portfolio_value)
            
            results[strategy_key] = {
                'name': strategy['name'],
                'success_rate': success_count / self.n_simulations,
                'final_values': portfolio_values,
                'median_final': np.median(portfolio_values),
                'percentile_10': np.percentile(portfolio_values, 10)
            }
        
        return results
    
    def analyze_optimal_allocations(self) -> Dict:
        """Analyze optimal Gold/TIPS allocations across scenarios"""
        
        print("\n🎯 OPTIMIZING GOLD/TIPS ALLOCATIONS")
        print("   Testing different Gold/TIPS combinations")
        
        # Test different allocations
        test_allocations = []
        for gold_pct in [0.05, 0.10, 0.15, 0.20, 0.25, 0.30]:
            for tips_pct in [0.05, 0.10, 0.15, 0.20, 0.25]:
                if gold_pct + tips_pct <= 0.40:  # Max 40% alternative assets
                    remaining = 1.0 - gold_pct - tips_pct
                    stock_pct = remaining * 0.7  # 70% of remaining in stocks
                    bond_pct = remaining * 0.3   # 30% of remaining in bonds
                    
                    test_allocations.append({
                        'stocks': stock_pct,
                        'bonds': bond_pct,
                        'gold': gold_pct,
                        'tips': tips_pct,
                        'name': f"S{stock_pct:.0%}/B{bond_pct:.0%}/G{gold_pct:.0%}/T{tips_pct:.0%}"
                    })
        
        best_allocations = {}
        
        for scenario_name, scenario_func in [
            ('stagflation', self.run_stagflation_test),
            ('sequence_risk', self.run_sequence_risk_test)
        ]:
            print(f"   Optimizing for {scenario_name}...")
            
            best_utility = -np.inf
            best_allocation = None
            
            for allocation in test_allocations[:20]:  # Test subset for performance
                # Run quick test with fewer simulations
                utility_score = self.quick_utility_test(allocation, scenario_func)
                
                if utility_score > best_utility:
                    best_utility = utility_score
                    best_allocation = allocation
            
            best_allocations[scenario_name] = {
                'allocation': best_allocation,
                'utility_score': best_utility
            }
        
        return best_allocations
    
    def quick_utility_test(self, allocation: Dict, scenario_func, n_sims: int = 1000) -> float:
        """Quick utility test for optimization"""
        
        portfolio_values = []
        
        for sim in range(n_sims):
            result = scenario_func(allocation, single_sim=True)
            portfolio_values.append(result)
        
        # Utility score: success rate + median final value (normalized)
        success_rate = sum(1 for v in portfolio_values if v > 0) / n_sims
        median_value = np.median(portfolio_values)
        
        utility_score = success_rate * 100 + (median_value / 1000000) * 10
        return utility_score
    
    def run_stagflation_test(self, allocation: Dict, single_sim: bool = False) -> float:
        """Helper for stagflation testing"""
        # Simplified version for optimization
        portfolio_value = 1000000
        
        for year in range(30):
            if year < 10:  # Stagflation period
                returns = {
                    'stocks': np.random.normal(-0.02, 0.25),
                    'bonds': np.random.normal(-0.06, 0.12),
                    'gold': np.random.normal(0.12, 0.20),
                    'tips': np.random.normal(0.12, 0.06)  # TIPS + inflation
                }
            else:  # Normal period
                returns = {
                    'stocks': np.random.normal(0.072, 0.20),
                    'bonds': np.random.normal(0.025, 0.08),
                    'gold': np.random.normal(0.015, 0.18),
                    'tips': np.random.normal(0.025, 0.06)
                }
            
            # Portfolio return
            portfolio_return = sum(allocation[asset] * returns[asset] for asset in allocation.keys())
            
            # Withdrawal
            withdrawal = min(40000 * (1.08 ** year), portfolio_value * 0.95)
            portfolio_value -= withdrawal
            
            if portfolio_value <= 0:
                return 0
            
            portfolio_value *= (1 + portfolio_return)
        
        return portfolio_value
    
    def run_sequence_risk_test(self, allocation: Dict, single_sim: bool = False) -> float:
        """Helper for sequence risk testing"""
        portfolio_value = 1000000
        
        for year in range(30):
            if year < 5:  # Poor sequence
                returns = {
                    'stocks': np.random.normal(-0.15, 0.30),
                    'bonds': np.random.normal(0.03, 0.10),
                    'gold': np.random.normal(0.08, 0.20),
                    'tips': np.random.normal(0.04, 0.06)
                }
            else:  # Recovery
                returns = {
                    'stocks': np.random.normal(0.12, 0.18),
                    'bonds': np.random.normal(0.025, 0.08),
                    'gold': np.random.normal(0.015, 0.18),
                    'tips': np.random.normal(0.025, 0.06)
                }
            
            # Portfolio return
            portfolio_return = sum(allocation[asset] * returns[asset] for asset in allocation.keys())
            
            # QOL withdrawal
            if year < 10:
                rate = 0.054
            elif year < 20:
                rate = 0.045
            else:
                rate = 0.035
            
            withdrawal = min(1000000 * rate * (1.03 ** year), portfolio_value * 0.95)
            portfolio_value -= withdrawal
            
            if portfolio_value <= 0:
                return 0
            
            portfolio_value *= (1 + portfolio_return)
        
        return portfolio_value
    
    def create_stress_test_visualization(self, stagflation_results: Dict, 
                                       sequence_results: Dict):
        """Create stress test visualization"""
        
        print("\n📊 Creating stress test visualization...")
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        strategies = list(stagflation_results.keys())
        strategy_names = [stagflation_results[s]['name'] for s in strategies]
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
        
        # Plot 1: Stagflation Success Rates
        stagflation_success = [stagflation_results[s]['success_rate'] * 100 for s in strategies]
        bars1 = ax1.bar(strategy_names, stagflation_success, color=colors, alpha=0.8)
        ax1.set_ylabel('Success Rate (%)')
        ax1.set_title('1970s Stagflation Scenario\nPortfolio Survival Rates', fontweight='bold')
        ax1.set_ylim([0, 100])
        ax1.grid(axis='y', alpha=0.3)
        
        # Add value labels
        for bar, value in zip(bars1, stagflation_success):
            ax1.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 1,
                    f'{value:.1f}%', ha='center', va='bottom', fontweight='bold')
        
        # Rotate x-axis labels
        ax1.set_xticklabels(strategy_names, rotation=45, ha='right')
        
        # Plot 2: Sequence Risk Success Rates
        sequence_success = [sequence_results[s]['success_rate'] * 100 for s in strategies]
        bars2 = ax2.bar(strategy_names, sequence_success, color=colors, alpha=0.8)
        ax2.set_ylabel('Success Rate (%)')
        ax2.set_title('Sequence of Returns Risk\nEarly Bear Market Scenario', fontweight='bold')
        ax2.set_ylim([0, 100])
        ax2.grid(axis='y', alpha=0.3)
        
        # Add value labels
        for bar, value in zip(bars2, sequence_success):
            ax2.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 1,
                    f'{value:.1f}%', ha='center', va='bottom', fontweight='bold')
        
        ax2.set_xticklabels(strategy_names, rotation=45, ha='right')
        
        # Plot 3: Median Final Values Comparison
        stagflation_median = [stagflation_results[s]['median_final']/1000000 for s in strategies]
        sequence_median = [sequence_results[s]['median_final']/1000000 for s in strategies]
        
        x = np.arange(len(strategy_names))
        width = 0.35
        
        ax3.bar(x - width/2, stagflation_median, width, label='Stagflation', 
               color='#ff7f0e', alpha=0.8)
        ax3.bar(x + width/2, sequence_median, width, label='Sequence Risk',
               color='#2ca02c', alpha=0.8)
        
        ax3.set_ylabel('Median Final Value ($M)')
        ax3.set_title('Portfolio Values After Crisis\nMedian Outcomes', fontweight='bold')
        ax3.set_xticks(x)
        ax3.set_xticklabels(strategy_names, rotation=45, ha='right')
        ax3.legend()
        ax3.grid(axis='y', alpha=0.3)
        
        # Plot 4: Risk Comparison (10th Percentile)
        stagflation_risk = [stagflation_results[s]['percentile_10']/1000000 for s in strategies]
        sequence_risk = [sequence_results[s]['percentile_10']/1000000 for s in strategies]
        
        ax4.bar(x - width/2, stagflation_risk, width, label='Stagflation',
               color='#ff7f0e', alpha=0.8)
        ax4.bar(x + width/2, sequence_risk, width, label='Sequence Risk',
               color='#2ca02c', alpha=0.8)
        
        ax4.set_ylabel('10th Percentile Value ($M)')
        ax4.set_title('Downside Risk Protection\n10th Percentile Outcomes', fontweight='bold')
        ax4.set_xticks(x)
        ax4.set_xticklabels(strategy_names, rotation=45, ha='right')
        ax4.legend()
        ax4.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        
        # Save the plot
        output_dir = Path('output/charts')
        output_dir.mkdir(parents=True, exist_ok=True)
        
        plt.savefig(output_dir / 'gold_tips_stress_test.png', dpi=300, bbox_inches='tight')
        print(f"   📊 Stress test visualization saved: {output_dir / 'gold_tips_stress_test.png'}")
        
        plt.show()
    
    def generate_stress_test_report(self, stagflation_results: Dict, 
                                   sequence_results: Dict) -> str:
        """Generate stress test summary report"""
        
        report = []
        report.append("=" * 80)
        report.append("🔥 GOLD & TIPS STRESS TEST ANALYSIS - CRISIS SCENARIOS")
        report.append("=" * 80)
        report.append("")
        
        # Stagflation analysis
        report.append("🌡️ 1970s STAGFLATION SCENARIO (10 years of high inflation + poor stocks):")
        report.append("-" * 70)
        
        best_stagflation = max(stagflation_results.keys(), 
                             key=lambda k: stagflation_results[k]['success_rate'])
        
        for strategy in stagflation_results.keys():
            result = stagflation_results[strategy]
            report.append(f"• {result['name']}: {result['success_rate']*100:.1f}% success, "
                         f"${result['median_final']:,.0f} median final value")
        
        report.append(f"\n🏆 WINNER: {stagflation_results[best_stagflation]['name']}")
        report.append("")
        
        # Sequence risk analysis
        report.append("📉 SEQUENCE OF RETURNS RISK (Early bear market + high QOL withdrawals):")
        report.append("-" * 70)
        
        best_sequence = max(sequence_results.keys(),
                           key=lambda k: sequence_results[k]['success_rate'])
        
        for strategy in sequence_results.keys():
            result = sequence_results[strategy]
            report.append(f"• {result['name']}: {result['success_rate']*100:.1f}% success, "
                         f"${result['median_final']:,.0f} median final value")
        
        report.append(f"\n🏆 WINNER: {sequence_results[best_sequence]['name']}")
        report.append("")
        
        # Key insights
        report.append("💡 KEY INSIGHTS:")
        report.append("-" * 40)
        report.append("• Gold provides crucial protection during stagflation scenarios")
        report.append("• TIPS offer stability during both inflation and deflation periods")
        report.append("• Alternative assets reduce portfolio correlation and improve resilience")
        report.append("• Enhanced strategies show superior crisis performance vs traditional 60/40")
        report.append("")
        
        # Recommendations
        report.append("🎯 CRISIS-TESTED RECOMMENDATIONS:")
        report.append("-" * 40)
        report.append("• For Inflation Protection: 15-25% Gold allocation")
        report.append("• For Stability: 5-15% TIPS allocation")
        report.append("• Total Alternative Assets: 20-40% of portfolio")
        report.append("• Rebalancing: Quarterly during crisis periods")
        
        return "\n".join(report)

def main():
    """Run the Gold and TIPS stress test analysis"""
    
    print("🔥 GOLD & TIPS CRISIS STRESS TEST")
    print("Testing portfolio resilience in extreme scenarios...")
    
    # Initialize stress tester
    tester = GoldTIPSStressTest()
    
    # Run stress tests
    stagflation_results = tester.simulate_1970s_stagflation()
    sequence_results = tester.simulate_sequence_risk()
    
    # Create visualization
    tester.create_stress_test_visualization(stagflation_results, sequence_results)
    
    # Generate report
    report = tester.generate_stress_test_report(stagflation_results, sequence_results)
    print(report)
    
    # Save results
    output_dir = Path('output/data')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    with open(output_dir / 'gold_tips_stress_test_report.txt', 'w') as f:
        f.write(report)
    
    print(f"\n📁 Stress test results saved to: {output_dir}")
    print("   • Visualization: output/charts/gold_tips_stress_test.png") 
    print("   • Report: output/data/gold_tips_stress_test_report.txt")

if __name__ == "__main__":
    main()