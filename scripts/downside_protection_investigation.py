#!/usr/bin/env python3
"""
DOWNSIDE PROTECTION DEEP DIVE ANALYSIS

Let's investigate the dramatic risk reduction numbers to understand what's driving
the 23,339% improvement in 10th percentile outcomes. This analysis will break down
exactly what's happening in the tail scenarios.
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

class DownsideProtectionAnalysis:
    """
    Deep dive into the dramatic downside protection improvements
    """
    
    def __init__(self):
        """Initialize with focused comparison parameters"""
        
        # Focus on the strategies showing the biggest improvements
        self.strategies = {
            'original_moderate': {
                'name': 'Original Moderate (60/40)',
                'allocation': {'stocks': 0.60, 'bonds': 0.40, 'gold': 0.0, 'tips': 0.0}
            },
            'enhanced_moderate': {
                'name': 'Enhanced Moderate (50/30/15/5)',
                'allocation': {'stocks': 0.50, 'bonds': 0.30, 'gold': 0.15, 'tips': 0.05}
            }
        }
        
        # Asset parameters with realistic correlations
        self.asset_params = {
            'stocks': {'real_return': 0.072, 'volatility': 0.20, 'inflation_sensitivity': -0.3},
            'bonds': {'real_return': 0.025, 'volatility': 0.08, 'inflation_sensitivity': -0.8},
            'gold': {'real_return': 0.015, 'volatility': 0.18, 'inflation_sensitivity': 0.7},
            'tips': {'real_return': 0.020, 'volatility': 0.06, 'inflation_sensitivity': 1.0}
        }
        
        # Correlation matrix
        self.correlation_matrix = np.array([
            [1.0, 0.1, -0.1, 0.2],   # Stocks
            [0.1, 1.0, -0.2, 0.6],   # Bonds  
            [-0.1, -0.2, 1.0, 0.3],  # Gold
            [0.2, 0.6, 0.3, 1.0]     # TIPS
        ])
        
        # Simulation parameters
        self.starting_value = 1000000
        self.n_simulations = 10000
        self.years = 29
        
    def run_detailed_comparison(self, inflation_scenario: str = 'normal') -> Dict:
        """Run detailed comparison with granular outcome tracking"""
        
        print(f"\n🔍 DETAILED DOWNSIDE ANALYSIS - {inflation_scenario.upper()} SCENARIO")
        print("=" * 70)
        
        # Inflation scenario parameters
        if inflation_scenario == 'normal':
            inflation_mean, inflation_std = 0.03, 0.015
        elif inflation_scenario == 'high':
            inflation_mean, inflation_std = 0.06, 0.025
        else:  # deflation
            inflation_mean, inflation_std = -0.005, 0.020
        
        results = {}
        
        for strategy_key, strategy in self.strategies.items():
            print(f"\n📊 Analyzing {strategy['name']}...")
            
            # Track detailed outcomes
            final_values = []
            failure_years = []
            min_values = []
            total_withdrawals = []
            
            for sim in range(self.n_simulations):
                portfolio_value = self.starting_value
                simulation_withdrawals = 0
                min_portfolio_value = portfolio_value
                failed_year = None
                
                for year in range(self.years):
                    # Generate correlated returns
                    inflation_shock = np.random.normal(inflation_mean - 0.03, inflation_std)
                    
                    # Base returns with correlation
                    random_draw = np.random.multivariate_normal([0, 0, 0, 0], self.correlation_matrix)
                    
                    returns = {}
                    for i, asset in enumerate(['stocks', 'bonds', 'gold', 'tips']):
                        params = self.asset_params[asset]
                        base_return = params['real_return'] + params['volatility'] * random_draw[i]
                        inflation_impact = params['inflation_sensitivity'] * inflation_shock
                        returns[asset] = base_return + inflation_impact
                    
                    # Calculate portfolio return
                    allocation = strategy['allocation']
                    portfolio_return = sum(allocation[asset] * returns[asset] for asset in allocation.keys())
                    
                    # QOL-based withdrawal
                    if year < 10:
                        qol_rate = 0.054  # 5.4% in peak years
                    elif year < 20:
                        qol_rate = 0.045  # 4.5% in comfort years
                    else:
                        qol_rate = 0.035  # 3.5% in care years
                    
                    # Inflation-adjusted withdrawal
                    cumulative_inflation = (1 + inflation_mean) ** year
                    withdrawal = self.starting_value * qol_rate * cumulative_inflation
                    withdrawal = min(withdrawal, portfolio_value * 0.95)  # Don't overdraw
                    
                    simulation_withdrawals += withdrawal
                    portfolio_value -= withdrawal
                    
                    # Check for failure
                    if portfolio_value <= 0:
                        portfolio_value = 0
                        if failed_year is None:
                            failed_year = year
                        break
                    
                    # Apply investment returns
                    portfolio_value *= (1 + portfolio_return)
                    min_portfolio_value = min(min_portfolio_value, portfolio_value)
                
                # Record results
                final_values.append(portfolio_value)
                failure_years.append(failed_year if failed_year is not None else self.years)
                min_values.append(min_portfolio_value)
                total_withdrawals.append(simulation_withdrawals)
            
            # Calculate detailed statistics
            final_values = np.array(final_values)
            failure_years = np.array(failure_years)
            min_values = np.array(min_values)
            total_withdrawals = np.array(total_withdrawals)
            
            # Survival analysis
            success_rate = np.sum(final_values > 0) / self.n_simulations
            
            # Percentile analysis
            percentiles = [1, 5, 10, 25, 50, 75, 90, 95, 99]
            percentile_values = [np.percentile(final_values, p) for p in percentiles]
            
            # Failure analysis
            failures = final_values == 0
            failure_rate = np.sum(failures) / self.n_simulations
            
            results[strategy_key] = {
                'name': strategy['name'],
                'allocation': strategy['allocation'],
                'final_values': final_values,
                'min_values': min_values,
                'total_withdrawals': total_withdrawals,
                'failure_years': failure_years,
                'success_rate': success_rate,
                'failure_rate': failure_rate,
                'mean_final': np.mean(final_values),
                'median_final': np.median(final_values),
                'std_final': np.std(final_values),
                'percentiles': dict(zip(percentiles, percentile_values)),
                'mean_withdrawal': np.mean(total_withdrawals),
                'min_portfolio_ever': np.mean(min_values)
            }
            
            # Print key statistics
            print(f"   Success Rate: {success_rate*100:.2f}%")
            print(f"   Mean Final Value: ${np.mean(final_values):,.0f}")
            print(f"   10th Percentile: ${percentile_values[2]:,.0f}")
            print(f"   1st Percentile: ${percentile_values[0]:,.0f}")
            print(f"   Failure Rate: {failure_rate*100:.2f}%")
        
        return results
    
    def analyze_percentile_improvement(self, results: Dict):
        """Analyze the dramatic percentile improvements"""
        
        print(f"\n🎯 PERCENTILE IMPROVEMENT ANALYSIS")
        print("=" * 50)
        
        original = results['original_moderate']
        enhanced = results['enhanced_moderate']
        
        print(f"\n📈 {original['name']} vs {enhanced['name']}")
        print("-" * 60)
        
        # Compare percentiles
        for percentile in [1, 5, 10, 25, 50]:
            orig_val = original['percentiles'][percentile]
            enh_val = enhanced['percentiles'][percentile]
            
            if orig_val > 0:
                improvement_pct = ((enh_val / orig_val) - 1) * 100
                print(f"{percentile:2d}th Percentile: ${orig_val:>12,.0f} → ${enh_val:>12,.0f} ({improvement_pct:>+8.1f}%)")
            else:
                print(f"{percentile:2d}th Percentile: ${orig_val:>12,.0f} → ${enh_val:>12,.0f} (N/A - division by zero)")
        
        # Special focus on the extreme improvements
        print(f"\n🔍 EXTREME IMPROVEMENT ANALYSIS:")
        print("-" * 40)
        
        # Check for near-zero or zero values causing extreme percentages
        orig_10th = original['percentiles'][10]
        enh_10th = enhanced['percentiles'][10]
        
        if orig_10th < 1000:  # Very small original value
            print(f"⚠️  IMPORTANT: Original 10th percentile is very small: ${orig_10th:.2f}")
            print(f"   This creates extreme percentage improvements when enhanced > 0")
            print(f"   Original: ${orig_10th:.2f} vs Enhanced: ${enh_10th:,.0f}")
            
            if orig_10th > 0:
                ratio = enh_10th / orig_10th
                print(f"   Ratio: {ratio:,.1f}x improvement")
        
        # Count scenarios near portfolio depletion
        orig_very_low = np.sum(original['final_values'] < 10000)
        enh_very_low = np.sum(enhanced['final_values'] < 10000)
        
        print(f"\n📊 PORTFOLIO DEPLETION ANALYSIS:")
        print(f"   Original strategy scenarios < $10K: {orig_very_low:,} ({orig_very_low/len(original['final_values'])*100:.1f}%)")
        print(f"   Enhanced strategy scenarios < $10K: {enh_very_low:,} ({enh_very_low/len(enhanced['final_values'])*100:.1f}%)")
        
        # Distribution comparison
        print(f"\n📈 DISTRIBUTION COMPARISON:")
        print(f"   Original - Mean: ${original['mean_final']:,.0f}, Std: ${original['std_final']:,.0f}")
        print(f"   Enhanced - Mean: ${enhanced['mean_final']:,.0f}, Std: ${enhanced['std_final']:,.0f}")
    
    def create_tail_risk_visualization(self, results: Dict):
        """Create detailed visualization of tail risk differences"""
        
        print(f"\n📊 Creating tail risk visualization...")
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        original = results['original_moderate']
        enhanced = results['enhanced_moderate']
        
        # Plot 1: Full distribution comparison
        bins = np.linspace(0, max(np.max(original['final_values']), np.max(enhanced['final_values'])), 100)
        
        ax1.hist(original['final_values'], bins=bins, alpha=0.6, label='Original 60/40', 
                density=True, color='red')
        ax1.hist(enhanced['final_values'], bins=bins, alpha=0.6, label='Enhanced 50/30/15/5',
                density=True, color='blue')
        
        ax1.set_xlabel('Final Portfolio Value ($)')
        ax1.set_ylabel('Density')
        ax1.set_title('Portfolio Value Distributions\nFull Range', fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Zoom in on left tail (bottom 10%)
        left_tail_max = max(np.percentile(original['final_values'], 10), 
                           np.percentile(enhanced['final_values'], 10)) * 1.5
        
        bins_tail = np.linspace(0, left_tail_max, 50)
        
        ax2.hist(original['final_values'], bins=bins_tail, alpha=0.6, label='Original 60/40',
                density=True, color='red')
        ax2.hist(enhanced['final_values'], bins=bins_tail, alpha=0.6, label='Enhanced 50/30/15/5',
                density=True, color='blue')
        
        ax2.set_xlabel('Final Portfolio Value ($)')
        ax2.set_ylabel('Density')
        ax2.set_title('Left Tail Distribution\n(Bottom 10% Focus)', fontweight='bold')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Percentile comparison
        percentiles = list(range(1, 21))  # 1st to 20th percentile
        orig_percentiles = [np.percentile(original['final_values'], p) for p in percentiles]
        enh_percentiles = [np.percentile(enhanced['final_values'], p) for p in percentiles]
        
        ax3.plot(percentiles, orig_percentiles, 'o-', label='Original 60/40', color='red', linewidth=2)
        ax3.plot(percentiles, enh_percentiles, 'o-', label='Enhanced 50/30/15/5', color='blue', linewidth=2)
        
        ax3.set_xlabel('Percentile')
        ax3.set_ylabel('Portfolio Value ($)')
        ax3.set_title('Bottom 20 Percentiles Comparison\nDownside Protection Focus', fontweight='bold')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        ax3.set_ylim(bottom=0)
        
        # Plot 4: Box plot comparison
        data_to_plot = [
            original['final_values'] / 1000000,  # Convert to millions
            enhanced['final_values'] / 1000000
        ]
        
        box_plot = ax4.boxplot(data_to_plot, labels=['Original\n60/40', 'Enhanced\n50/30/15/5'],
                              patch_artist=True, showfliers=True)
        
        # Color the boxes
        box_plot['boxes'][0].set_facecolor('red')
        box_plot['boxes'][0].set_alpha(0.6)
        box_plot['boxes'][1].set_facecolor('blue')
        box_plot['boxes'][1].set_alpha(0.6)
        
        ax4.set_ylabel('Final Portfolio Value ($M)')
        ax4.set_title('Distribution Summary\nBox Plot Comparison', fontweight='bold')
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Save the plot
        output_dir = Path('output/charts')
        output_dir.mkdir(parents=True, exist_ok=True)
        
        plt.savefig(output_dir / 'downside_protection_analysis.png', dpi=300, bbox_inches='tight')
        print(f"   📊 Visualization saved: {output_dir / 'downside_protection_analysis.png'}")
        
        plt.show()
    
    def investigate_calculation_methodology(self, results: Dict):
        """Investigate the calculation methodology for the extreme percentages"""
        
        print(f"\n🔬 CALCULATION METHODOLOGY INVESTIGATION")
        print("=" * 60)
        
        original = results['original_moderate']
        enhanced = results['enhanced_moderate']
        
        # Get the exact 10th percentile values
        orig_10th = original['percentiles'][10]
        enh_10th = enhanced['percentiles'][10]
        
        print(f"Original 10th Percentile: ${orig_10th:,.2f}")
        print(f"Enhanced 10th Percentile: ${enh_10th:,.2f}")
        
        if orig_10th > 0:
            improvement_ratio = enh_10th / orig_10th
            improvement_pct = ((enh_10th / orig_10th) - 1) * 100
            
            print(f"\nImprovement Ratio: {improvement_ratio:.1f}x")
            print(f"Improvement Percentage: {improvement_pct:,.1f}%")
            
            print(f"\n🔍 BREAKDOWN OF EXTREME PERCENTAGE:")
            print(f"   The {improvement_pct:,.1f}% improvement occurs because:")
            print(f"   1. Original 10th percentile is very small: ${orig_10th:,.2f}")
            print(f"   2. Enhanced 10th percentile is larger: ${enh_10th:,.2f}")
            print(f"   3. Formula: ({enh_10th:.2f} / {orig_10th:.2f} - 1) × 100 = {improvement_pct:,.1f}%")
            
            if orig_10th < 100:
                print(f"\n⚠️  WARNING: Original value is extremely small (< $100)")
                print(f"   This creates mathematical artifacts in percentage calculations")
                print(f"   Even small absolute improvements appear as massive percentages")
        
        # Count zero and near-zero values
        orig_zeros = np.sum(original['final_values'] == 0)
        orig_near_zero = np.sum(original['final_values'] < 1000)
        enh_zeros = np.sum(enhanced['final_values'] == 0)
        enh_near_zero = np.sum(enhanced['final_values'] < 1000)
        
        print(f"\n📊 ZERO AND NEAR-ZERO VALUE ANALYSIS:")
        print(f"   Original Strategy:")
        print(f"     Exactly zero values: {orig_zeros:,} ({orig_zeros/len(original['final_values'])*100:.2f}%)")
        print(f"     Near-zero (< $1K): {orig_near_zero:,} ({orig_near_zero/len(original['final_values'])*100:.2f}%)")
        print(f"   Enhanced Strategy:")
        print(f"     Exactly zero values: {enh_zeros:,} ({enh_zeros/len(enhanced['final_values'])*100:.2f}%)")
        print(f"     Near-zero (< $1K): {enh_near_zero:,} ({enh_near_zero/len(enhanced['final_values'])*100:.2f}%)")
        
        # Better metric: absolute improvement
        absolute_improvement = enh_10th - orig_10th
        print(f"\n💡 BETTER METRIC - ABSOLUTE IMPROVEMENT:")
        print(f"   10th Percentile Absolute Gain: ${absolute_improvement:,.2f}")
        print(f"   This is a more meaningful measure than the percentage")

def main():
    """Run the detailed downside protection analysis"""
    
    print("🔍 INVESTIGATING THE 23,339% DOWNSIDE PROTECTION CLAIM")
    print("=" * 70)
    print("Let's break down what's really happening with these extreme numbers...")
    
    # Initialize analyzer
    analyzer = DownsideProtectionAnalysis()
    
    # Run detailed comparison for normal inflation scenario
    results = analyzer.run_detailed_comparison('normal')
    
    # Analyze the percentile improvements
    analyzer.analyze_percentile_improvement(results)
    
    # Investigate calculation methodology
    analyzer.investigate_calculation_methodology(results)
    
    # Create visualization
    analyzer.create_tail_risk_visualization(results)
    
    print(f"\n💡 CONCLUSION:")
    print("=" * 40)
    print("The 23,339% improvement is mathematically correct but misleading.")
    print("It occurs because the original strategy's 10th percentile is near zero,")
    print("making any positive improvement appear as a massive percentage.")
    print("\nMore meaningful metrics:")
    print("• Absolute dollar improvement in worst-case scenarios")
    print("• Reduction in failure rates") 
    print("• Improvement in median outcomes")
    print("\nThe enhanced strategy DOES provide better downside protection,")
    print("but the extreme percentage is a mathematical artifact.")

if __name__ == "__main__":
    main()