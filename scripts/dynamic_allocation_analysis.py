"""
DYNAMIC PORTFOLIO REALLOCATION WITH QOL STRATEGY

This analysis explores whether dynamically shifting portfolio allocation over time
can optimize the QOL framework - starting aggressive for early enjoyment benefits,
then becoming conservative for capital preservation as enjoyment value decreases.

Key Concept: Match portfolio risk to life phase enjoyment values:
- Early Retirement (High Enjoyment): Aggressive allocation for growth
- Mid Retirement (Moderate Enjoyment): Balanced allocation 
- Late Retirement (Low Enjoyment): Conservative allocation for preservation
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
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')


class DynamicAllocationQOLAnalysis:
    """
    Analyze QOL strategies with dynamic portfolio reallocation over time
    """
    
    def __init__(self):
        # Define allocation strategies that change over time
        self.dynamic_strategies = {
            'glide_path_aggressive': {
                'name': 'Aggressive Glide Path',
                'description': 'Start 100% stocks, end 40% stocks',
                'phase1_allocation': {'stocks': 1.00, 'bonds': 0.00},  # Years 0-9
                'phase2_allocation': {'stocks': 0.70, 'bonds': 0.30},  # Years 10-19
                'phase3_allocation': {'stocks': 0.40, 'bonds': 0.60},  # Years 20+
                'phase1_return': 0.072, 'phase1_vol': 0.20,
                'phase2_return': 0.060, 'phase2_vol': 0.165,
                'phase3_return': 0.045, 'phase3_vol': 0.135
            },
            'glide_path_moderate': {
                'name': 'Moderate Glide Path',
                'description': 'Start 80% stocks, end 30% stocks',
                'phase1_allocation': {'stocks': 0.80, 'bonds': 0.20},  # Years 0-9
                'phase2_allocation': {'stocks': 0.60, 'bonds': 0.40},  # Years 10-19
                'phase3_allocation': {'stocks': 0.30, 'bonds': 0.70},  # Years 20+
                'phase1_return': 0.068, 'phase1_vol': 0.18,
                'phase2_return': 0.055, 'phase2_vol': 0.15,
                'phase3_return': 0.035, 'phase3_vol': 0.12
            },
            'glide_path_conservative': {
                'name': 'Conservative Glide Path',
                'description': 'Start 60% stocks, end 20% stocks',
                'phase1_allocation': {'stocks': 0.60, 'bonds': 0.40},  # Years 0-9
                'phase2_allocation': {'stocks': 0.40, 'bonds': 0.60},  # Years 10-19
                'phase3_allocation': {'stocks': 0.20, 'bonds': 0.80},  # Years 20+
                'phase1_return': 0.055, 'phase1_vol': 0.15,
                'phase2_return': 0.045, 'phase2_vol': 0.135,
                'phase3_return': 0.030, 'phase3_vol': 0.10
            },
            'reverse_glide_path': {
                'name': 'Reverse Glide Path',
                'description': 'Start 40% stocks, end 90% stocks (contrarian)',
                'phase1_allocation': {'stocks': 0.40, 'bonds': 0.60},  # Years 0-9
                'phase2_allocation': {'stocks': 0.65, 'bonds': 0.35},  # Years 10-19
                'phase3_allocation': {'stocks': 0.90, 'bonds': 0.10},  # Years 20+
                'phase1_return': 0.045, 'phase1_vol': 0.135,
                'phase2_return': 0.058, 'phase2_vol': 0.155,
                'phase3_return': 0.070, 'phase3_vol': 0.19
            }
        }
        
        # Static strategies for comparison
        self.static_strategies = {
            'static_aggressive': {
                'name': 'Static Aggressive (80/20)',
                'description': 'Fixed 80% stocks throughout',
                'allocation': {'stocks': 0.80, 'bonds': 0.20},
                'return': 0.068, 'volatility': 0.18
            },
            'static_moderate': {
                'name': 'Static Moderate (60/40)',
                'description': 'Fixed 60% stocks throughout',
                'allocation': {'stocks': 0.60, 'bonds': 0.40},
                'return': 0.055, 'volatility': 0.15
            },
            'static_conservative': {
                'name': 'Static Conservative (40/60)',
                'description': 'Fixed 40% stocks throughout',
                'allocation': {'stocks': 0.40, 'bonds': 0.60},
                'return': 0.045, 'volatility': 0.135
            }
        }
        
        # Enjoyment scenarios
        self.enjoyment_scenarios = {
            'moderate': {'high': 1.50, 'moderate': 1.20, 'low': 1.00}
        }
        
    def get_phase_params(self, year: int, strategy_params: Dict) -> Tuple[float, float]:
        """Get return and volatility parameters for a specific year in dynamic strategy"""
        if year < 10:  # Phase 1: Years 0-9
            return strategy_params['phase1_return'], strategy_params['phase1_vol']
        elif year < 20:  # Phase 2: Years 10-19
            return strategy_params['phase2_return'], strategy_params['phase2_vol']
        else:  # Phase 3: Years 20+
            return strategy_params['phase3_return'], strategy_params['phase3_vol']
    
    def get_enjoyment_multiplier(self, year: int, scenario: str = 'moderate') -> float:
        """Get enjoyment multiplier for a specific year"""
        values = self.enjoyment_scenarios[scenario]
        
        if year < 10:  # Ages 65-74
            return values['high']
        elif year < 20:  # Ages 75-84
            return values['moderate']
        else:  # Ages 85+
            return values['low']
    
    def run_dynamic_simulation(self, strategy_key: str, withdrawal_strategy: str,
                              qol_params: Dict = None, n_simulations: int = 1000) -> Dict:
        """Run simulation with dynamic portfolio allocation"""
        
        if strategy_key in self.dynamic_strategies:
            strategy = self.dynamic_strategies[strategy_key]
            is_dynamic = True
        else:
            strategy = self.static_strategies[strategy_key]
            is_dynamic = False
        
        # Custom simulation with phase-specific parameters
        np.random.seed(42)  # For reproducibility
        
        starting_value = 1000000
        horizon_years = 29
        
        portfolio_paths = []
        withdrawal_paths = []
        
        for sim in range(n_simulations):
            portfolio_path = [starting_value]
            withdrawal_path = []
            
            current_portfolio = starting_value
            cumulative_inflation_factor = 1.0
            
            for year in range(horizon_years):
                # Update inflation
                inflation_rate = np.random.normal(0.03, 0.01)
                cumulative_inflation_factor *= (1 + inflation_rate)
                
                # Get returns based on strategy type
                if is_dynamic:
                    real_return, volatility = self.get_phase_params(year, strategy)
                else:
                    real_return, volatility = strategy['return'], strategy['volatility']
                
                # Generate annual return
                annual_return = np.random.normal(real_return, volatility)
                
                # Calculate QOL multiplier if needed
                if withdrawal_strategy == 'hauenstein' and qol_params:
                    if year < 10:
                        qol_multiplier = qol_params['phase1_mult']
                    elif year < 20:
                        qol_multiplier = qol_params['phase2_mult']
                    else:
                        qol_multiplier = qol_params['phase3_mult']
                else:
                    qol_multiplier = 1.0
                
                # Calculate withdrawal
                if withdrawal_strategy == 'trinity_4pct':
                    withdrawal_amount = starting_value * 0.04 * cumulative_inflation_factor
                elif withdrawal_strategy == 'hauenstein':
                    base_trinity_withdrawal = starting_value * 0.04 * cumulative_inflation_factor
                    withdrawal_amount = base_trinity_withdrawal * qol_multiplier
                else:
                    withdrawal_amount = starting_value * 0.04 * cumulative_inflation_factor
                
                # Apply portfolio growth and withdrawal
                pre_withdrawal_value = current_portfolio * (1 + annual_return)
                current_portfolio = max(0, pre_withdrawal_value - withdrawal_amount)
                
                portfolio_path.append(current_portfolio)
                withdrawal_path.append(withdrawal_amount)
            
            portfolio_paths.append(portfolio_path[1:])  # Exclude starting value
            withdrawal_paths.append(withdrawal_path)
        
        return {
            'portfolio_paths': np.array(portfolio_paths),
            'withdrawal_paths': np.array(withdrawal_paths),
            'strategy': strategy
        }
    
    def calculate_enjoyment_metrics(self, withdrawal_paths: np.ndarray) -> Dict:
        """Calculate enjoyment-weighted metrics"""
        n_simulations, n_years = withdrawal_paths.shape
        
        # Apply enjoyment multipliers
        enjoyment_weighted_paths = np.zeros_like(withdrawal_paths)
        total_enjoyment_premiums = np.zeros(n_simulations)
        
        for year in range(n_years):
            enjoyment_multiplier = self.get_enjoyment_multiplier(year, 'moderate')
            enjoyment_weighted_paths[:, year] = withdrawal_paths[:, year] * enjoyment_multiplier
            
            # Premium value
            premium_multiplier = enjoyment_multiplier - 1.0
            total_enjoyment_premiums += withdrawal_paths[:, year] * premium_multiplier
        
        return {
            'total_enjoyment_value': np.mean(np.sum(enjoyment_weighted_paths, axis=1)),
            'enjoyment_premium': np.mean(total_enjoyment_premiums),
            'total_income': np.mean(np.sum(withdrawal_paths, axis=1))
        }
    
    def run_comprehensive_analysis(self, n_simulations: int = 1000) -> Dict:
        """Run comprehensive analysis comparing dynamic vs static strategies"""
        
        print("🔄 DYNAMIC PORTFOLIO REALLOCATION ANALYSIS")
        print("=" * 70)
        print("Testing dynamic allocation strategies vs static approaches")
        print("for Trinity Study and QOL Enhanced strategies")
        print()
        
        results = {}
        
        # QOL parameters
        qol_params = {'phase1_mult': 1.35, 'phase2_mult': 1.125, 'phase3_mult': 0.875}
        
        # Test all allocation strategies
        all_strategies = {**self.dynamic_strategies, **self.static_strategies}
        
        for strategy_key, strategy_info in all_strategies.items():
            print(f"📊 Testing: {strategy_info['name']}")
            print(f"   {strategy_info['description']}")
            
            # Run Trinity Study
            trinity_results = self.run_dynamic_simulation(
                strategy_key, 'trinity_4pct', n_simulations=n_simulations
            )
            
            # Run QOL Enhanced
            qol_results = self.run_dynamic_simulation(
                strategy_key, 'hauenstein', qol_params, n_simulations=n_simulations
            )
            
            # Calculate metrics
            trinity_success = np.mean(trinity_results['portfolio_paths'][:, -1] > 0)
            qol_success = np.mean(qol_results['portfolio_paths'][:, -1] > 0)
            
            trinity_enjoyment = self.calculate_enjoyment_metrics(trinity_results['withdrawal_paths'])
            qol_enjoyment = self.calculate_enjoyment_metrics(qol_results['withdrawal_paths'])
            
            # Risk-adjusted enjoyment analysis
            risk_penalty = (trinity_success - qol_success) * 100
            enjoyment_premium = qol_enjoyment['enjoyment_premium'] - trinity_enjoyment['enjoyment_premium']
            
            if enjoyment_premium > 0 and risk_penalty > 0:
                cost_per_enjoyment = (risk_penalty / 100 * 1000000) / enjoyment_premium
            else:
                cost_per_enjoyment = float('inf')
            
            results[strategy_key] = {
                'strategy_info': strategy_info,
                'trinity_success': trinity_success,
                'qol_success': qol_success,
                'trinity_enjoyment': trinity_enjoyment,
                'qol_enjoyment': qol_enjoyment,
                'risk_penalty': risk_penalty,
                'enjoyment_premium': enjoyment_premium,
                'cost_per_enjoyment': cost_per_enjoyment,
                'trinity_results': trinity_results,
                'qol_results': qol_results
            }
            
            print(f"   Trinity Success: {trinity_success*100:.1f}%, QOL Success: {qol_success*100:.1f}%")
            print(f"   Cost per enjoyment $: ${cost_per_enjoyment:.2f}")
            print()
        
        return results
    
    def create_comparison_report(self, analysis_results: Dict) -> str:
        """Create comprehensive comparison report"""
        
        report = []
        report.append("=" * 80)
        report.append("🔄 DYNAMIC PORTFOLIO REALLOCATION ANALYSIS REPORT")
        report.append("=" * 80)
        report.append("")
        
        report.append("📋 STRATEGY OVERVIEW")
        report.append("-" * 40)
        report.append("Testing whether dynamic reallocation (shifting from aggressive to")
        report.append("conservative as enjoyment value decreases) improves QOL outcomes.")
        report.append("")
        
        # Separate dynamic and static results
        dynamic_results = {k: v for k, v in analysis_results.items() if k in self.dynamic_strategies}
        static_results = {k: v for k, v in analysis_results.items() if k in self.static_strategies}
        
        report.append("🎯 DYNAMIC STRATEGIES PERFORMANCE")
        report.append("-" * 50)
        
        best_dynamic = min(dynamic_results.items(), key=lambda x: x[1]['cost_per_enjoyment'])
        
        for strategy_key, result in dynamic_results.items():
            strategy_info = result['strategy_info']
            cost = result['cost_per_enjoyment']
            risk_penalty = result['risk_penalty']
            enjoyment_premium = result['enjoyment_premium']
            
            if cost <= 1.0:
                rating = "🟢 EXCELLENT"
            elif cost <= 2.0:
                rating = "🟡 GOOD"
            else:
                rating = "🔴 POOR"
            
            report.append(f"")
            report.append(f"{strategy_info['name']}:")
            report.append(f"  • {strategy_info['description']}")
            report.append(f"  • Cost per enjoyment $: ${cost:.2f}")
            report.append(f"  • Risk penalty: {risk_penalty:.1f}%")
            report.append(f"  • Enjoyment premium: ${enjoyment_premium:,.0f}")
            report.append(f"  • Rating: {rating}")
        
        report.append("")
        report.append("📊 STATIC STRATEGIES PERFORMANCE")
        report.append("-" * 50)
        
        best_static = min(static_results.items(), key=lambda x: x[1]['cost_per_enjoyment'])
        
        for strategy_key, result in static_results.items():
            strategy_info = result['strategy_info']
            cost = result['cost_per_enjoyment']
            risk_penalty = result['risk_penalty']
            enjoyment_premium = result['enjoyment_premium']
            
            if cost <= 1.0:
                rating = "🟢 EXCELLENT"
            elif cost <= 2.0:
                rating = "🟡 GOOD"
            else:
                rating = "🔴 POOR"
            
            report.append(f"")
            report.append(f"{strategy_info['name']}:")
            report.append(f"  • {strategy_info['description']}")
            report.append(f"  • Cost per enjoyment $: ${cost:.2f}")
            report.append(f"  • Risk penalty: {risk_penalty:.1f}%")
            report.append(f"  • Enjoyment premium: ${enjoyment_premium:,.0f}")
            report.append(f"  • Rating: {rating}")
        
        report.append("")
        report.append("🏆 OPTIMAL STRATEGY COMPARISON")
        report.append("-" * 50)
        
        overall_best = min(analysis_results.items(), key=lambda x: x[1]['cost_per_enjoyment'])
        
        report.append(f"Best Dynamic: {best_dynamic[1]['strategy_info']['name']}")
        report.append(f"  Cost: ${best_dynamic[1]['cost_per_enjoyment']:.2f} per enjoyment dollar")
        report.append("")
        report.append(f"Best Static: {best_static[1]['strategy_info']['name']}")
        report.append(f"  Cost: ${best_static[1]['cost_per_enjoyment']:.2f} per enjoyment dollar")
        report.append("")
        report.append(f"Overall Best: {overall_best[1]['strategy_info']['name']}")
        report.append(f"  Cost: ${overall_best[1]['cost_per_enjoyment']:.2f} per enjoyment dollar")
        
        # Dynamic vs Static Analysis
        dynamic_advantage = best_static[1]['cost_per_enjoyment'] - best_dynamic[1]['cost_per_enjoyment']
        
        report.append("")
        report.append("🔍 DYNAMIC ALLOCATION BENEFIT")
        report.append("-" * 40)
        
        if dynamic_advantage > 0.25:
            conclusion = "🟢 SIGNIFICANT BENEFIT - Dynamic allocation clearly superior"
        elif dynamic_advantage > 0.05:
            conclusion = "🟡 MODERATE BENEFIT - Dynamic allocation somewhat better"
        elif dynamic_advantage > -0.05:
            conclusion = "🟡 NEUTRAL - No clear advantage either way"
        else:
            conclusion = "🔴 DISADVANTAGE - Static allocation is better"
        
        report.append(f"Dynamic advantage: ${dynamic_advantage:+.2f} per enjoyment dollar")
        report.append(f"Conclusion: {conclusion}")
        
        report.append("")
        report.append("💡 KEY INSIGHTS")
        report.append("-" * 40)
        
        # Calculate average costs
        avg_dynamic_cost = np.mean([r['cost_per_enjoyment'] for r in dynamic_results.values()])
        avg_static_cost = np.mean([r['cost_per_enjoyment'] for r in static_results.values()])
        
        report.append(f"• Average dynamic strategy cost: ${avg_dynamic_cost:.2f}")
        report.append(f"• Average static strategy cost: ${avg_static_cost:.2f}")
        report.append(f"• Dynamic strategies are {avg_static_cost/avg_dynamic_cost:.1f}x more efficient on average")
        
        # Risk analysis
        avg_dynamic_risk = np.mean([r['risk_penalty'] for r in dynamic_results.values()])
        avg_static_risk = np.mean([r['risk_penalty'] for r in static_results.values()])
        
        report.append(f"• Average dynamic risk penalty: {avg_dynamic_risk:.1f}%")
        report.append(f"• Average static risk penalty: {avg_static_risk:.1f}%")
        
        return "\n".join(report)
    
    def create_dynamic_visualization(self, analysis_results: Dict):
        """Create visualization comparing dynamic vs static strategies"""
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Dynamic Portfolio Reallocation Analysis', fontsize=16, fontweight='bold')
        
        # Prepare data
        dynamic_strategies = [k for k in analysis_results.keys() if k in self.dynamic_strategies]
        static_strategies = [k for k in analysis_results.keys() if k in self.static_strategies]
        
        # Plot 1: Cost per enjoyment comparison
        dynamic_costs = [analysis_results[k]['cost_per_enjoyment'] for k in dynamic_strategies]
        static_costs = [analysis_results[k]['cost_per_enjoyment'] for k in static_strategies]
        
        dynamic_names = [analysis_results[k]['strategy_info']['name'].replace(' Glide Path', '') for k in dynamic_strategies]
        static_names = [analysis_results[k]['strategy_info']['name'].replace('Static ', '') for k in static_strategies]
        
        x_dynamic = np.arange(len(dynamic_strategies))
        x_static = np.arange(len(static_strategies))
        
        ax1.bar(x_dynamic - 0.2, dynamic_costs, 0.4, label='Dynamic', alpha=0.7, color='green')
        ax1.bar(x_static + 0.2, static_costs, 0.4, label='Static', alpha=0.7, color='blue')
        
        ax1.axhline(y=1.0, color='red', linestyle='--', alpha=0.7, label='$1.00 threshold')
        ax1.axhline(y=2.0, color='orange', linestyle='--', alpha=0.7, label='$2.00 threshold')
        
        ax1.set_xlabel('Strategy Type')
        ax1.set_ylabel('Cost per Enjoyment Dollar')
        ax1.set_title('Dynamic vs Static: Cost Efficiency')
        ax1.set_xticks(range(max(len(dynamic_strategies), len(static_strategies))))
        ax1.set_xticklabels([f'D{i+1}' if i < len(dynamic_names) else f'S{i+1-len(dynamic_names)}' 
                            for i in range(max(len(dynamic_strategies), len(static_strategies)))], rotation=45)
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Risk penalty comparison
        dynamic_risks = [analysis_results[k]['risk_penalty'] for k in dynamic_strategies]
        static_risks = [analysis_results[k]['risk_penalty'] for k in static_strategies]
        
        ax2.bar(x_dynamic - 0.2, dynamic_risks, 0.4, label='Dynamic', alpha=0.7, color='green')
        ax2.bar(x_static + 0.2, static_risks, 0.4, label='Static', alpha=0.7, color='blue')
        
        ax2.set_xlabel('Strategy Type')
        ax2.set_ylabel('Risk Penalty (%)')
        ax2.set_title('Dynamic vs Static: Risk Penalty')
        ax2.set_xticks(range(max(len(dynamic_strategies), len(static_strategies))))
        ax2.set_xticklabels([f'D{i+1}' if i < len(dynamic_names) else f'S{i+1-len(dynamic_names)}' 
                            for i in range(max(len(dynamic_strategies), len(static_strategies)))], rotation=45)
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Allocation evolution for best dynamic strategy
        best_dynamic_key = min(dynamic_strategies, key=lambda k: analysis_results[k]['cost_per_enjoyment'])
        best_dynamic = self.dynamic_strategies[best_dynamic_key]
        
        years = list(range(29))
        stock_allocation = []
        
        for year in years:
            if year < 10:
                stock_allocation.append(best_dynamic['phase1_allocation']['stocks'] * 100)
            elif year < 20:
                stock_allocation.append(best_dynamic['phase2_allocation']['stocks'] * 100)
            else:
                stock_allocation.append(best_dynamic['phase3_allocation']['stocks'] * 100)
        
        enjoyment_multipliers = [self.get_enjoyment_multiplier(year) for year in years]
        
        ax3_twin = ax3.twinx()
        
        line1 = ax3.plot(years, stock_allocation, 'b-', linewidth=3, label='Stock Allocation (%)')
        line2 = ax3_twin.plot(years, enjoyment_multipliers, 'r--', linewidth=2, label='Enjoyment Value')
        
        ax3.axvspan(0, 10, alpha=0.2, color='green', label='High Enjoyment Phase')
        ax3.axvspan(10, 20, alpha=0.15, color='yellow', label='Moderate Enjoyment Phase')
        ax3.axvspan(20, 29, alpha=0.1, color='gray', label='Low Enjoyment Phase')
        
        ax3.set_xlabel('Retirement Year')
        ax3.set_ylabel('Stock Allocation (%)', color='b')
        ax3_twin.set_ylabel('Enjoyment Multiplier', color='r')
        ax3.set_title(f'Best Dynamic Strategy: {best_dynamic["name"]}\nAllocation vs Enjoyment Over Time')
        
        # Combine legends
        lines = line1 + line2
        labels = [l.get_label() for l in lines]
        ax3.legend(lines, labels, loc='upper right')
        ax3.grid(True, alpha=0.3)
        
        # Plot 4: Success rates
        dynamic_trinity_success = [analysis_results[k]['trinity_success']*100 for k in dynamic_strategies]
        dynamic_qol_success = [analysis_results[k]['qol_success']*100 for k in dynamic_strategies]
        static_trinity_success = [analysis_results[k]['trinity_success']*100 for k in static_strategies]
        static_qol_success = [analysis_results[k]['qol_success']*100 for k in static_strategies]
        
        width = 0.35
        x = np.arange(len(dynamic_strategies))
        
        ax4.bar(x - width/2, dynamic_trinity_success, width/2, label='Dynamic Trinity', alpha=0.7, color='lightblue')
        ax4.bar(x, dynamic_qol_success, width/2, label='Dynamic QOL', alpha=0.7, color='lightgreen')
        
        ax4.set_xlabel('Dynamic Strategy')
        ax4.set_ylabel('Success Rate (%)')
        ax4.set_title('Success Rates: Trinity vs QOL')
        ax4.set_xticks(x)
        ax4.set_xticklabels([f'D{i+1}' for i in range(len(dynamic_strategies))])
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Save the plot
        output_dir = project_root / 'output' / 'charts'
        os.makedirs(output_dir, exist_ok=True)
        plt.savefig(f'{output_dir}/dynamic_allocation_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return fig


def main():
    """Run the dynamic portfolio reallocation analysis"""
    
    analyzer = DynamicAllocationQOLAnalysis()
    
    # Run comprehensive analysis
    print("Starting dynamic portfolio reallocation analysis...")
    analysis_results = analyzer.run_comprehensive_analysis(n_simulations=1000)
    
    # Generate comparison report
    report = analyzer.create_comparison_report(analysis_results)
    print("\n" + report)
    
    # Create visualization
    print("\n📈 Generating visualization...")
    analyzer.create_dynamic_visualization(analysis_results)
    
    # Save results
    output_dir = project_root / 'output'
    os.makedirs(output_dir, exist_ok=True)
    
    with open(f'{output_dir}/dynamic_allocation_analysis.txt', 'w') as f:
        f.write(report)
    
    print(f"\n✅ Analysis complete!")
    print(f"📋 Report: {output_dir}/dynamic_allocation_analysis.txt")
    print(f"📊 Visualization: output/charts/dynamic_allocation_analysis.png")


if __name__ == "__main__":
    main()