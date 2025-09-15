#!/usr/bin/env python3
"""
GOLD AND TIPS INTEGRATION FOR QOL MODELING

This script analyzes the potential impact of adding Gold and TIPS (Treasury Inflation-Protected Securities)
to the existing QOL retirement framework. We'll examine how these alternative assets affect:

1. Portfolio resilience during inflationary periods
2. Risk-adjusted returns across different QOL phases  
3. Success rates for dynamic allocation strategies
4. Overall utility optimization in retirement

Key Research Questions:
- How do Gold and TIPS improve inflation protection during high QOL phases?
- What optimal allocations maximize utility while preserving portfolio survival?
- How do these assets perform in various economic scenarios?
"""

import sys
import os
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import warnings
warnings.filterwarnings('ignore')

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent / 'src'))

@dataclass
class AssetParameters:
    """Parameters for different asset classes"""
    name: str
    real_return: float
    volatility: float
    correlation_stocks: float
    correlation_bonds: float
    correlation_gold: float = 0.0
    correlation_tips: float = 0.0
    inflation_sensitivity: float = 0.0  # How asset responds to inflation shocks

class GoldTIPSQOLAnalysis:
    """
    Extended QOL Analysis incorporating Gold and TIPS
    """
    
    def __init__(self):
        """Initialize with enhanced 4-asset model"""
        
        # Original 2-asset parameters (baseline)
        self.original_assets = {
            'stocks': AssetParameters(
                name='Stocks',
                real_return=0.072,
                volatility=0.20,
                correlation_stocks=1.0,
                correlation_bonds=0.1,
                inflation_sensitivity=-0.3  # Stocks often struggle with inflation initially
            ),
            'bonds': AssetParameters(
                name='Bonds', 
                real_return=0.025,
                volatility=0.08,
                correlation_stocks=0.1,
                correlation_bonds=1.0,
                inflation_sensitivity=-0.8  # Bonds hurt most by inflation
            )
        }
        
        # Enhanced 4-asset parameters
        self.enhanced_assets = {
            'stocks': AssetParameters(
                name='Stocks',
                real_return=0.072,
                volatility=0.20,
                correlation_stocks=1.0,
                correlation_bonds=0.1,
                correlation_gold=-0.1,
                correlation_tips=0.2,
                inflation_sensitivity=-0.3
            ),
            'bonds': AssetParameters(
                name='Bonds',
                real_return=0.025,
                volatility=0.08,
                correlation_stocks=0.1,
                correlation_bonds=1.0,
                correlation_gold=-0.2,
                correlation_tips=0.6,
                inflation_sensitivity=-0.8
            ),
            'gold': AssetParameters(
                name='Gold',
                real_return=0.015,  # Low real return but inflation hedge
                volatility=0.18,
                correlation_stocks=-0.1,
                correlation_bonds=-0.2,
                correlation_gold=1.0,
                correlation_tips=0.3,
                inflation_sensitivity=0.7  # Strong inflation hedge
            ),
            'tips': AssetParameters(
                name='TIPS',
                real_return=0.020,  # Slightly below regular bonds
                volatility=0.06,
                correlation_stocks=0.2,
                correlation_bonds=0.6,
                correlation_gold=0.3,
                correlation_tips=1.0,
                inflation_sensitivity=1.0  # Perfect inflation protection by design
            )
        }
        
        # QOL phase parameters (from existing research)
        self.qol_phases = {
            'phase1': {'years': (0, 9), 'multiplier': 1.35, 'name': 'Peak Years (65-74)'},
            'phase2': {'years': (10, 19), 'multiplier': 1.125, 'name': 'Comfort Years (75-84)'},
            'phase3': {'years': (20, 29), 'multiplier': 0.875, 'name': 'Care Years (85+)'}
        }
        
        # Portfolio strategies to test
        self.portfolio_strategies = {
            # Original 2-asset strategies
            'original_conservative': {
                'name': 'Original Conservative (30/70)',
                'assets': {'stocks': 0.30, 'bonds': 0.70, 'gold': 0.0, 'tips': 0.0},
                'type': 'original'
            },
            'original_moderate': {
                'name': 'Original Moderate (60/40)', 
                'assets': {'stocks': 0.60, 'bonds': 0.40, 'gold': 0.0, 'tips': 0.0},
                'type': 'original'
            },
            'original_aggressive': {
                'name': 'Original Aggressive (80/20)',
                'assets': {'stocks': 0.80, 'bonds': 0.20, 'gold': 0.0, 'tips': 0.0},
                'type': 'original'
            },
            
            # Enhanced 4-asset strategies 
            'enhanced_conservative': {
                'name': 'Enhanced Conservative (25/60/10/5)',
                'assets': {'stocks': 0.25, 'bonds': 0.60, 'gold': 0.10, 'tips': 0.05},
                'type': 'enhanced'
            },
            'enhanced_moderate': {
                'name': 'Enhanced Moderate (50/30/15/5)',
                'assets': {'stocks': 0.50, 'bonds': 0.30, 'gold': 0.15, 'tips': 0.05},
                'type': 'enhanced'
            },
            'enhanced_aggressive': {
                'name': 'Enhanced Aggressive (70/15/10/5)',
                'assets': {'stocks': 0.70, 'bonds': 0.15, 'gold': 0.10, 'tips': 0.05},
                'type': 'enhanced'
            },
            
            # Inflation-focused strategies
            'inflation_defensive': {
                'name': 'Inflation Defensive (40/20/25/15)',
                'assets': {'stocks': 0.40, 'bonds': 0.20, 'gold': 0.25, 'tips': 0.15},
                'type': 'enhanced'
            },
            'tips_heavy': {
                'name': 'TIPS Heavy (50/10/15/25)',
                'assets': {'stocks': 0.50, 'bonds': 0.10, 'gold': 0.15, 'tips': 0.25},
                'type': 'enhanced'
            }
        }
        
        # Simulation parameters
        self.starting_value = 1000000
        self.horizon_years = 29
        self.n_simulations = 5000
        self.base_trinity_rate = 0.04
        
    def generate_correlated_returns(self, n_simulations: int, n_years: int, 
                                  inflation_scenario: str = 'normal') -> Dict[str, np.ndarray]:
        """Generate correlated returns for all asset classes with inflation scenarios"""
        
        # Define inflation scenarios
        inflation_scenarios = {
            'normal': {'mean': 0.03, 'std': 0.015},
            'high': {'mean': 0.06, 'std': 0.025},  # 1970s-style inflation
            'deflation': {'mean': -0.005, 'std': 0.020}  # Japan-style deflation
        }
        
        inflation_params = inflation_scenarios[inflation_scenario]
        
        # Generate inflation shocks
        inflation_shocks = np.random.normal(
            inflation_params['mean'] - 0.03,  # Deviation from normal 3%
            inflation_params['std'],
            (n_simulations, n_years)
        )
        
        returns = {}
        
        # Generate base returns using enhanced correlation matrix
        assets = list(self.enhanced_assets.keys())
        n_assets = len(assets)
        
        # Build correlation matrix
        correlation_matrix = np.eye(n_assets)
        for i, asset_i in enumerate(assets):
            for j, asset_j in enumerate(assets):
                if i != j:
                    # Get correlation from asset parameters
                    asset_params = self.enhanced_assets[asset_i]
                    if asset_j == 'stocks':
                        correlation_matrix[i, j] = asset_params.correlation_stocks
                    elif asset_j == 'bonds':
                        correlation_matrix[i, j] = asset_params.correlation_bonds
                    elif asset_j == 'gold':
                        correlation_matrix[i, j] = asset_params.correlation_gold
                    elif asset_j == 'tips':
                        correlation_matrix[i, j] = asset_params.correlation_tips
        
        # Generate correlated random variables
        for sim in range(n_simulations):
            # Generate correlated standard normal variables
            random_vars = np.random.multivariate_normal(
                mean=np.zeros(n_assets),
                cov=correlation_matrix,
                size=n_years
            )
            
            for i, asset in enumerate(assets):
                asset_params = self.enhanced_assets[asset]
                
                # Base return calculation
                base_returns = (asset_params.real_return + 
                               asset_params.volatility * random_vars[:, i])
                
                # Apply inflation sensitivity
                inflation_impact = (asset_params.inflation_sensitivity * 
                                  inflation_shocks[sim, :])
                
                final_returns = base_returns + inflation_impact
                
                if asset not in returns:
                    returns[asset] = np.zeros((n_simulations, n_years))
                
                returns[asset][sim, :] = final_returns
        
        return returns, inflation_shocks
    
    def calculate_portfolio_returns(self, returns: Dict[str, np.ndarray], 
                                  allocation: Dict[str, float]) -> np.ndarray:
        """Calculate portfolio returns given asset returns and allocation"""
        
        portfolio_returns = np.zeros_like(next(iter(returns.values())))
        
        for asset, weight in allocation.items():
            if weight > 0:
                portfolio_returns += weight * returns[asset]
        
        return portfolio_returns
    
    def run_qol_simulation(self, strategy_key: str, inflation_scenario: str = 'normal') -> Dict:
        """Run QOL simulation with given portfolio strategy and inflation scenario"""
        
        strategy = self.portfolio_strategies[strategy_key]
        
        print(f"   Running {strategy['name']} under {inflation_scenario} inflation...")
        
        # Generate returns
        returns, inflation_shocks = self.generate_correlated_returns(
            self.n_simulations, self.horizon_years, inflation_scenario
        )
        
        # Calculate portfolio returns
        portfolio_returns = self.calculate_portfolio_returns(returns, strategy['assets'])
        
        # Run simulations
        portfolio_paths = []
        withdrawal_paths = []
        utility_paths = []
        success_count = 0
        
        for sim in range(self.n_simulations):
            portfolio_value = self.starting_value
            annual_withdrawals = []
            annual_utilities = []
            portfolio_history = [portfolio_value]
            
            for year in range(self.horizon_years):
                # Determine QOL phase and multiplier
                if year <= self.qol_phases['phase1']['years'][1]:
                    qol_multiplier = self.qol_phases['phase1']['multiplier']
                elif year <= self.qol_phases['phase2']['years'][1]:
                    qol_multiplier = self.qol_phases['phase2']['multiplier']
                else:
                    qol_multiplier = self.qol_phases['phase3']['multiplier']
                
                # Calculate withdrawal (QOL-adjusted Trinity rate)
                # Use real purchasing power - inflate by cumulative inflation
                cumulative_inflation = np.prod(1 + inflation_shocks[sim, :year+1]) if year > 0 else 1
                base_withdrawal = self.starting_value * self.base_trinity_rate
                real_withdrawal = base_withdrawal * qol_multiplier * cumulative_inflation
                
                # Ensure we don't withdraw more than 95% of portfolio
                actual_withdrawal = min(real_withdrawal, portfolio_value * 0.95)
                annual_withdrawals.append(actual_withdrawal)
                
                # Calculate utility (withdrawal × QOL factor)
                # QOL factor decreases with age (from existing research)
                age = 65 + year
                if age < 75:
                    qol_factor = 1.0  # Peak years
                elif age < 85:
                    qol_factor = 0.7  # Moderate enjoyment
                else:
                    qol_factor = 0.4  # Care years
                
                utility = actual_withdrawal * qol_factor
                annual_utilities.append(utility)
                
                # Apply withdrawal
                portfolio_value -= actual_withdrawal
                
                # Check for depletion
                if portfolio_value <= 0:
                    portfolio_value = 0
                    portfolio_history.append(0)
                    break
                
                # Apply investment returns
                portfolio_value *= (1 + portfolio_returns[sim, year])
                portfolio_history.append(portfolio_value)
            
            # Record results
            if portfolio_value > 0:
                success_count += 1
            
            portfolio_paths.append(portfolio_history)
            withdrawal_paths.append(annual_withdrawals)
            utility_paths.append(annual_utilities)
        
        # Calculate summary statistics
        portfolio_paths_array = np.array([p[:self.horizon_years+1] for p in portfolio_paths])
        withdrawal_paths_array = np.array([w for w in withdrawal_paths])
        utility_paths_array = np.array([u for u in utility_paths])
        
        final_values = portfolio_paths_array[:, -1]
        total_withdrawals = np.sum(withdrawal_paths_array, axis=1)
        total_utilities = np.sum(utility_paths_array, axis=1)
        
        return {
            'strategy_name': strategy['name'],
            'strategy_key': strategy_key,
            'inflation_scenario': inflation_scenario,
            'success_rate': success_count / self.n_simulations,
            'portfolio_paths': portfolio_paths_array,
            'withdrawal_paths': withdrawal_paths_array,
            'utility_paths': utility_paths_array,
            'final_values': final_values,
            'total_withdrawals': total_withdrawals,
            'total_utilities': total_utilities,
            'avg_final_value': np.mean(final_values),
            'median_final_value': np.median(final_values),
            'avg_total_withdrawal': np.mean(total_withdrawals),
            'avg_total_utility': np.mean(total_utilities),
            'percentile_10_final': np.percentile(final_values, 10),
            'percentile_90_final': np.percentile(final_values, 90)
        }
    
    def run_comprehensive_analysis(self) -> Dict:
        """Run comprehensive analysis across all strategies and scenarios"""
        
        print("\n" + "=" * 80)
        print("🏆 GOLD & TIPS QOL ENHANCEMENT ANALYSIS")
        print("=" * 80)
        print("Analyzing impact of Gold and TIPS on QOL retirement strategies...")
        print(f"Simulations: {self.n_simulations:,} | Horizon: {self.horizon_years} years")
        
        results = {}
        inflation_scenarios = ['normal', 'high', 'deflation']
        
        for scenario in inflation_scenarios:
            print(f"\n🌡️  INFLATION SCENARIO: {scenario.upper()}")
            print("-" * 50)
            
            scenario_results = {}
            
            for strategy_key in self.portfolio_strategies.keys():
                result = self.run_qol_simulation(strategy_key, scenario)
                scenario_results[strategy_key] = result
            
            results[scenario] = scenario_results
        
        return results
    
    def analyze_enhancement_benefits(self, results: Dict) -> Dict:
        """Analyze specific benefits of Gold and TIPS integration"""
        
        print("\n" + "=" * 80)
        print("📊 ENHANCEMENT BENEFITS ANALYSIS")
        print("=" * 80)
        
        benefits_analysis = {}
        
        for scenario in results.keys():
            print(f"\n🎯 {scenario.upper()} INFLATION SCENARIO")
            print("-" * 40)
            
            scenario_results = results[scenario]
            scenario_benefits = {}
            
            # Compare original vs enhanced strategies
            strategy_pairs = [
                ('original_conservative', 'enhanced_conservative'),
                ('original_moderate', 'enhanced_moderate'), 
                ('original_aggressive', 'enhanced_aggressive')
            ]
            
            for original_key, enhanced_key in strategy_pairs:
                original = scenario_results[original_key]
                enhanced = scenario_results[enhanced_key]
                
                # Calculate improvements
                success_improvement = enhanced['success_rate'] - original['success_rate']
                utility_improvement = (enhanced['avg_total_utility'] / original['avg_total_utility'] - 1) * 100
                final_value_improvement = (enhanced['avg_final_value'] / original['avg_final_value'] - 1) * 100
                withdrawal_improvement = (enhanced['avg_total_withdrawal'] / original['avg_total_withdrawal'] - 1) * 100
                
                # Risk reduction (measured by 10th percentile improvement)
                risk_reduction = (enhanced['percentile_10_final'] / original['percentile_10_final'] - 1) * 100
                
                scenario_benefits[f"{original_key}_vs_{enhanced_key}"] = {
                    'original_strategy': original['strategy_name'],
                    'enhanced_strategy': enhanced['strategy_name'],
                    'success_rate_improvement': success_improvement * 100,  # percentage points
                    'utility_improvement_pct': utility_improvement,
                    'final_value_improvement_pct': final_value_improvement,
                    'withdrawal_improvement_pct': withdrawal_improvement,
                    'risk_reduction_pct': risk_reduction,
                    'original_success_rate': original['success_rate'] * 100,
                    'enhanced_success_rate': enhanced['success_rate'] * 100
                }
                
                print(f"\n📈 {original['strategy_name']} → {enhanced['strategy_name']}")
                print(f"   Success Rate: {original['success_rate']*100:.1f}% → {enhanced['success_rate']*100:.1f}% ({success_improvement*100:+.1f}pp)")
                print(f"   Total Utility: {utility_improvement:+.1f}%")
                print(f"   Final Value: {final_value_improvement:+.1f}%")
                print(f"   Risk (10th %ile): {risk_reduction:+.1f}%")
            
            benefits_analysis[scenario] = scenario_benefits
        
        return benefits_analysis
    
    def create_comprehensive_visualization(self, results: Dict, benefits: Dict):
        """Create comprehensive visualization of Gold/TIPS impact"""
        
        print("\n📊 Creating comprehensive visualization...")
        
        # Set up the plotting environment
        plt.style.use('seaborn-v0_8')
        fig = plt.figure(figsize=(20, 16))
        
        # Create a comprehensive layout
        gs = fig.add_gridspec(4, 3, height_ratios=[1, 1, 1, 1], hspace=0.3, wspace=0.3)
        
        scenarios = ['normal', 'high', 'deflation']
        colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#7209B7', '#1B998B', '#FF6B35', '#004E64']
        
        # Plot 1: Success Rates Across Scenarios
        ax1 = fig.add_subplot(gs[0, :])
        
        strategy_names = [results['normal'][k]['strategy_name'] for k in self.portfolio_strategies.keys()]
        x_pos = np.arange(len(strategy_names))
        
        for i, scenario in enumerate(scenarios):
            success_rates = [results[scenario][k]['success_rate'] * 100 for k in self.portfolio_strategies.keys()]
            ax1.bar(x_pos + i*0.25, success_rates, 0.25, 
                   label=f'{scenario.title()} Inflation', alpha=0.8, color=colors[i])
        
        ax1.set_xlabel('Portfolio Strategy')
        ax1.set_ylabel('Success Rate (%)')
        ax1.set_title('Portfolio Success Rates: Original vs Gold/TIPS Enhanced Strategies', fontweight='bold', fontsize=14)
        ax1.set_xticks(x_pos + 0.25)
        ax1.set_xticklabels(strategy_names, rotation=45, ha='right')
        ax1.legend()
        ax1.grid(axis='y', alpha=0.3)
        
        # Plot 2: Utility Improvements
        ax2 = fig.add_subplot(gs[1, 0])
        
        enhancements = ['conservative', 'moderate', 'aggressive']
        normal_scenario_benefits = benefits['normal']
        
        utility_improvements = []
        for enhancement in enhancements:
            key = f"original_{enhancement}_vs_enhanced_{enhancement}"
            if key in normal_scenario_benefits:
                utility_improvements.append(normal_scenario_benefits[key]['utility_improvement_pct'])
            else:
                utility_improvements.append(0)
        
        bars = ax2.bar(enhancements, utility_improvements, color=colors[0], alpha=0.7)
        ax2.set_ylabel('Utility Improvement (%)')
        ax2.set_title('Gold/TIPS Utility Enhancement\n(Normal Inflation)', fontweight='bold')
        ax2.grid(axis='y', alpha=0.3)
        
        # Add value labels
        for bar, value in zip(bars, utility_improvements):
            if value != 0:
                ax2.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.1,
                        f'{value:.1f}%', ha='center', va='bottom', fontweight='bold')
        
        # Plot 3: Risk Reduction (10th Percentile Improvement)
        ax3 = fig.add_subplot(gs[1, 1])
        
        risk_reductions = []
        for enhancement in enhancements:
            key = f"original_{enhancement}_vs_enhanced_{enhancement}"
            if key in normal_scenario_benefits:
                risk_reductions.append(normal_scenario_benefits[key]['risk_reduction_pct'])
            else:
                risk_reductions.append(0)
        
        bars = ax3.bar(enhancements, risk_reductions, color=colors[1], alpha=0.7)
        ax3.set_ylabel('Risk Reduction (%)')
        ax3.set_title('Downside Risk Improvement\n(10th Percentile)', fontweight='bold')
        ax3.grid(axis='y', alpha=0.3)
        
        # Add value labels
        for bar, value in zip(bars, risk_reductions):
            if value != 0:
                ax3.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.5,
                        f'{value:.1f}%', ha='center', va='bottom', fontweight='bold')
        
        # Plot 4: Inflation Scenario Comparison
        ax4 = fig.add_subplot(gs[1, 2])
        
        # Compare enhanced_moderate across inflation scenarios
        enhanced_moderate_success = [results[s]['enhanced_moderate']['success_rate'] * 100 for s in scenarios]
        original_moderate_success = [results[s]['original_moderate']['success_rate'] * 100 for s in scenarios]
        
        x_scenarios = np.arange(len(scenarios))
        width = 0.35
        
        ax4.bar(x_scenarios - width/2, original_moderate_success, width, 
               label='Original (60/40)', alpha=0.8, color=colors[3])
        ax4.bar(x_scenarios + width/2, enhanced_moderate_success, width,
               label='Enhanced + Gold/TIPS', alpha=0.8, color=colors[4])
        
        ax4.set_ylabel('Success Rate (%)')
        ax4.set_title('Inflation Resilience\n(Moderate Strategies)', fontweight='bold')
        ax4.set_xticks(x_scenarios)
        ax4.set_xticklabels([s.title() for s in scenarios])
        ax4.legend()
        ax4.grid(axis='y', alpha=0.3)
        
        # Plot 5-7: Asset Allocation Comparison
        allocation_strategies = ['enhanced_conservative', 'enhanced_moderate', 'enhanced_aggressive']
        allocation_titles = ['Conservative', 'Moderate', 'Aggressive']
        
        for i, (strategy_key, title) in enumerate(zip(allocation_strategies, allocation_titles)):
            ax = fig.add_subplot(gs[2, i])
            
            strategy = self.portfolio_strategies[strategy_key]
            allocations = strategy['assets']
            
            # Create pie chart
            assets = []
            weights = []
            colors_pie = []
            color_map = {'stocks': '#2E86AB', 'bonds': '#A23B72', 'gold': '#F18F01', 'tips': '#1B998B'}
            
            for asset, weight in allocations.items():
                if weight > 0:
                    assets.append(asset.upper())
                    weights.append(weight)
                    colors_pie.append(color_map[asset])
            
            ax.pie(weights, labels=assets, colors=colors_pie, autopct='%1.0f%%', startangle=90)
            ax.set_title(f'{title} Enhanced\nAllocation', fontweight='bold')
        
        # Plot 8: Efficiency Analysis (Utility per Unit Risk)
        ax8 = fig.add_subplot(gs[3, :2])
        
        # Calculate efficiency metrics for normal inflation scenario
        strategies_to_plot = ['original_moderate', 'enhanced_moderate', 'inflation_defensive', 'tips_heavy']
        strategy_labels = [results['normal'][s]['strategy_name'] for s in strategies_to_plot]
        
        utilities = [results['normal'][s]['avg_total_utility'] for s in strategies_to_plot]
        risks = [100 - results['normal'][s]['success_rate'] * 100 for s in strategies_to_plot]  # Risk as failure rate
        
        scatter = ax8.scatter(risks, utilities, s=200, alpha=0.7, c=colors[:len(strategies_to_plot)])
        
        for i, label in enumerate(strategy_labels):
            ax8.annotate(label.replace(' (', '\n('), (risks[i], utilities[i]), 
                        xytext=(10, 10), textcoords='offset points', fontsize=9)
        
        ax8.set_xlabel('Portfolio Risk (Failure Rate %)')
        ax8.set_ylabel('Average Total Utility')
        ax8.set_title('Risk-Utility Efficiency: Gold/TIPS Strategies', fontweight='bold')
        ax8.grid(True, alpha=0.3)
        
        # Plot 9: Summary Impact Table
        ax9 = fig.add_subplot(gs[3, 2])
        ax9.axis('off')
        
        # Create summary table data
        table_data = []
        table_data.append(['Metric', 'Conservative', 'Moderate', 'Aggressive'])
        
        metrics = ['Success Rate Δ', 'Utility Δ (%)', 'Risk Reduction (%)']
        
        for metric in metrics:
            row = [metric]
            for enhancement in enhancements:
                key = f"original_{enhancement}_vs_enhanced_{enhancement}"
                if key in normal_scenario_benefits:
                    if metric == 'Success Rate Δ':
                        value = f"{normal_scenario_benefits[key]['success_rate_improvement']:.1f}pp"
                    elif metric == 'Utility Δ (%)':
                        value = f"{normal_scenario_benefits[key]['utility_improvement_pct']:.1f}%"
                    else:  # Risk Reduction
                        value = f"{normal_scenario_benefits[key]['risk_reduction_pct']:.1f}%"
                else:
                    value = "N/A"
                row.append(value)
            table_data.append(row)
        
        # Create table
        table = ax9.table(cellText=table_data[1:], colLabels=table_data[0],
                         cellLoc='center', loc='center', bbox=[0, 0, 1, 1])
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 2)
        
        # Style the table
        for i in range(len(table_data)):
            for j in range(len(table_data[0])):
                cell = table[(i, j)]
                if i == 0:  # Header row
                    cell.set_facecolor('#4472C4')
                    cell.set_text_props(weight='bold', color='white')
                else:
                    if j == 0:  # First column
                        cell.set_facecolor('#D9E1F2')
                        cell.set_text_props(weight='bold')
                    else:
                        cell.set_facecolor('#F2F2F2')
        
        ax9.set_title('Enhancement Summary\n(Normal Inflation)', fontweight='bold', y=0.95)
        
        plt.suptitle('Gold & TIPS Integration: QOL Framework Enhancement Analysis', 
                    fontsize=16, fontweight='bold', y=0.98)
        
        # Save the plot
        output_dir = Path('output/charts')
        output_dir.mkdir(parents=True, exist_ok=True)
        
        plt.savefig(output_dir / 'gold_tips_qol_analysis.png', dpi=300, bbox_inches='tight')
        print(f"   📊 Visualization saved: {output_dir / 'gold_tips_qol_analysis.png'}")
        
        plt.show()
    
    def generate_summary_report(self, results: Dict, benefits: Dict) -> str:
        """Generate comprehensive summary report"""
        
        report = []
        report.append("=" * 80)
        report.append("🏆 GOLD & TIPS QOL ENHANCEMENT ANALYSIS - EXECUTIVE SUMMARY")
        report.append("=" * 80)
        report.append("")
        
        # Key findings
        report.append("🎯 KEY FINDINGS:")
        report.append("-" * 40)
        
        # Find best improvements
        normal_benefits = benefits['normal']
        best_utility_improvement = 0
        best_risk_reduction = 0
        best_success_improvement = 0
        
        for key, benefit in normal_benefits.items():
            if benefit['utility_improvement_pct'] > best_utility_improvement:
                best_utility_improvement = benefit['utility_improvement_pct']
            if benefit['risk_reduction_pct'] > best_risk_reduction:
                best_risk_reduction = benefit['risk_reduction_pct']
            if benefit['success_rate_improvement'] > best_success_improvement:
                best_success_improvement = benefit['success_rate_improvement']
        
        report.append(f"• Maximum Utility Improvement: {best_utility_improvement:.1f}%")
        report.append(f"• Maximum Risk Reduction: {best_risk_reduction:.1f}%") 
        report.append(f"• Maximum Success Rate Gain: {best_success_improvement:.1f} percentage points")
        report.append("")
        
        # Inflation resilience analysis
        report.append("🌡️  INFLATION RESILIENCE:")
        report.append("-" * 40)
        
        # Compare enhanced_moderate across scenarios
        for scenario in ['normal', 'high', 'deflation']:
            enhanced_success = results[scenario]['enhanced_moderate']['success_rate'] * 100
            original_success = results[scenario]['original_moderate']['success_rate'] * 100
            difference = enhanced_success - original_success
            
            report.append(f"• {scenario.title()} Inflation: Enhanced {enhanced_success:.1f}% vs Original {original_success:.1f}% ({difference:+.1f}pp)")
        
        report.append("")
        
        # Strategy recommendations
        report.append("💡 STRATEGIC RECOMMENDATIONS:")
        report.append("-" * 40)
        
        # Find best performing strategies for each scenario
        for scenario in results.keys():
            scenario_results = results[scenario]
            best_strategy = max(scenario_results.keys(), 
                              key=lambda k: scenario_results[k]['avg_total_utility'])
            best_utility = scenario_results[best_strategy]['avg_total_utility']
            best_success = scenario_results[best_strategy]['success_rate'] * 100
            
            report.append(f"• {scenario.title()} Inflation Environment:")
            report.append(f"  - Optimal Strategy: {scenario_results[best_strategy]['strategy_name']}")
            report.append(f"  - Success Rate: {best_success:.1f}%")
            report.append(f"  - Average Total Utility: {best_utility:,.0f}")
        
        report.append("")
        
        # Implementation guidance
        report.append("🔧 IMPLEMENTATION GUIDANCE:")
        report.append("-" * 40)
        report.append("• Conservative Retirees: Consider Enhanced Conservative (25/60/10/5)")
        report.append("• Moderate Risk Tolerance: Enhanced Moderate (50/30/15/5)")
        report.append("• High Inflation Concern: Inflation Defensive (40/20/25/15)")
        report.append("• Maximum TIPS Exposure: TIPS Heavy (50/10/15/25)")
        report.append("")
        
        report.append("📊 DETAILED ANALYSIS:")
        report.append("-" * 40)
        
        # Detailed comparison table
        report.append(f"{'Strategy':<30} {'Success Rate':<15} {'Avg Utility':<15} {'Final Value':<15}")
        report.append("-" * 75)
        
        normal_results = results['normal']
        for strategy_key in ['original_moderate', 'enhanced_moderate', 'inflation_defensive', 'tips_heavy']:
            if strategy_key in normal_results:
                result = normal_results[strategy_key]
                report.append(f"{result['strategy_name']:<30} {result['success_rate']*100:<14.1f}% "
                            f"{result['avg_total_utility']:<14,.0f} ${result['avg_final_value']:<14,.0f}")
        
        report.append("")
        report.append("=" * 80)
        
        return "\n".join(report)

def main():
    """Run the comprehensive Gold and TIPS QOL analysis"""
    
    # Initialize analysis
    analyzer = GoldTIPSQOLAnalysis()
    
    # Run comprehensive analysis
    results = analyzer.run_comprehensive_analysis()
    
    # Analyze enhancement benefits
    benefits = analyzer.analyze_enhancement_benefits(results)
    
    # Create visualization
    analyzer.create_comprehensive_visualization(results, benefits)
    
    # Generate summary report
    summary = analyzer.generate_summary_report(results, benefits)
    print(summary)
    
    # Save results
    output_dir = Path('output/data')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save summary report
    with open(output_dir / 'gold_tips_qol_summary.txt', 'w') as f:
        f.write(summary)
    
    print(f"\n📁 Results saved to: {output_dir}")
    print("   • Visualization: output/charts/gold_tips_qol_analysis.png")
    print("   • Summary Report: output/data/gold_tips_qol_summary.txt")

if __name__ == "__main__":
    main()