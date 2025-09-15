"""
PORTFOLIO VALUE DISTRIBUTION ANALYSIS

This analysis examines the distribution of portfolio values at key transition points
(10 and 20 years) for the Aggressive Glide Path strategy, showing the range of
outcomes and decision-making context at each reallocation point.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Find project root directory
script_dir = Path(__file__).parent
project_root = script_dir.parent

class PortfolioDistributionAnalysis:
    """
    Analyze portfolio value distributions at key decision points
    """
    
    def __init__(self):
        # Aggressive Glide Path strategy parameters
        self.strategy = {
            'phase1': {  # Years 0-9 (Ages 65-74)
                'allocation': {'stocks': 1.00, 'bonds': 0.00},
                'expected_return': 0.072,
                'volatility': 0.20,
                'qol_multiplier': 1.35
            },
            'phase2': {  # Years 10-19 (Ages 75-84)
                'allocation': {'stocks': 0.70, 'bonds': 0.30},
                'expected_return': 0.060,
                'volatility': 0.165,
                'qol_multiplier': 1.125
            },
            'phase3': {  # Years 20+ (Ages 85+)
                'allocation': {'stocks': 0.40, 'bonds': 0.60},
                'expected_return': 0.045,
                'volatility': 0.135,
                'qol_multiplier': 0.875
            }
        }
        
        # Trinity Study comparison
        self.trinity_strategy = {
            'allocation': {'stocks': 0.60, 'bonds': 0.40},
            'expected_return': 0.055,
            'volatility': 0.15,
            'qol_multiplier': 1.0
        }
    
    def run_distribution_simulation(self, n_simulations=10000):
        """Run simulation focusing on portfolio distributions at key points"""
        
        print("🔄 PORTFOLIO DISTRIBUTION SIMULATION")
        print("=" * 60)
        print(f"Running {n_simulations:,} simulations for detailed distribution analysis")
        print()
        
        np.random.seed(42)  # For reproducibility
        
        starting_portfolio = 1000000
        
        # Storage for results
        results = {
            'aggressive_glide': {
                'year_10_values': [],
                'year_20_values': [],
                'final_values': [],
                'year_10_withdrawals': [],
                'year_20_withdrawals': [],
                'success_at_10': [],
                'success_at_20': []
            },
            'trinity_comparison': {
                'year_10_values': [],
                'year_20_values': [],
                'final_values': []
            }
        }
        
        for sim in range(n_simulations):
            # Aggressive Glide Path simulation
            portfolio_value = starting_portfolio
            cumulative_inflation = 1.0
            
            for year in range(29):
                # Determine phase
                if year < 10:
                    phase_params = self.strategy['phase1']
                elif year < 20:
                    phase_params = self.strategy['phase2']
                else:
                    phase_params = self.strategy['phase3']
                
                # Inflation
                inflation_rate = np.random.normal(0.03, 0.01)
                cumulative_inflation *= (1 + inflation_rate)
                
                # Portfolio return
                annual_return = np.random.normal(
                    phase_params['expected_return'],
                    phase_params['volatility']
                )
                
                # QOL withdrawal
                base_withdrawal = starting_portfolio * 0.04 * cumulative_inflation
                qol_withdrawal = base_withdrawal * phase_params['qol_multiplier']
                
                # Apply growth and withdrawal
                pre_withdrawal_value = portfolio_value * (1 + annual_return)
                portfolio_value = max(0, pre_withdrawal_value - qol_withdrawal)
                
                # Record key transition points
                if year == 9:  # End of year 10 (before transition to 70% stocks)
                    results['aggressive_glide']['year_10_values'].append(portfolio_value)
                    results['aggressive_glide']['year_10_withdrawals'].append(qol_withdrawal)
                    results['aggressive_glide']['success_at_10'].append(portfolio_value > 0)
                elif year == 19:  # End of year 20 (before transition to 40% stocks)
                    results['aggressive_glide']['year_20_values'].append(portfolio_value)
                    results['aggressive_glide']['year_20_withdrawals'].append(qol_withdrawal)
                    results['aggressive_glide']['success_at_20'].append(portfolio_value > 0)
            
            results['aggressive_glide']['final_values'].append(portfolio_value)
            
            # Trinity Study comparison simulation
            portfolio_value_trinity = starting_portfolio
            cumulative_inflation_trinity = 1.0
            
            for year in range(29):
                # Inflation
                inflation_rate = np.random.normal(0.03, 0.01)
                cumulative_inflation_trinity *= (1 + inflation_rate)
                
                # Portfolio return (fixed 60/40)
                annual_return = np.random.normal(
                    self.trinity_strategy['expected_return'],
                    self.trinity_strategy['volatility']
                )
                
                # Trinity withdrawal (4% rule)
                trinity_withdrawal = starting_portfolio * 0.04 * cumulative_inflation_trinity
                
                # Apply growth and withdrawal
                pre_withdrawal_value = portfolio_value_trinity * (1 + annual_return)
                portfolio_value_trinity = max(0, pre_withdrawal_value - trinity_withdrawal)
                
                # Record key points
                if year == 9:
                    results['trinity_comparison']['year_10_values'].append(portfolio_value_trinity)
                elif year == 19:
                    results['trinity_comparison']['year_20_values'].append(portfolio_value_trinity)
            
            results['trinity_comparison']['final_values'].append(portfolio_value_trinity)
        
        return results
    
    def analyze_distributions(self, results):
        """Analyze the portfolio value distributions"""
        
        print("📊 DISTRIBUTION ANALYSIS RESULTS")
        print("=" * 50)
        print()
        
        # Convert to numpy arrays for easier analysis
        ag_10 = np.array(results['aggressive_glide']['year_10_values'])
        ag_20 = np.array(results['aggressive_glide']['year_20_values'])
        ag_final = np.array(results['aggressive_glide']['final_values'])
        
        trinity_10 = np.array(results['trinity_comparison']['year_10_values'])
        trinity_20 = np.array(results['trinity_comparison']['year_20_values'])
        trinity_final = np.array(results['trinity_comparison']['final_values'])
        
        # Year 10 Analysis (Age 75 - First Transition Point)
        print("🎂 YEAR 10 (AGE 75) - FIRST REALLOCATION DECISION")
        print("-" * 60)
        print("Decision: Reduce from 100% to 70% stocks")
        print()
        
        self.print_distribution_stats("Aggressive Glide Path", ag_10)
        self.print_distribution_stats("Trinity Study (60/40)", trinity_10)
        
        # Calculate advantage
        ag_10_median = np.median(ag_10)
        trinity_10_median = np.median(trinity_10)
        advantage_10 = (ag_10_median / trinity_10_median - 1) * 100
        
        print(f"💡 Aggressive Glide Advantage at Year 10: {advantage_10:+.1f}%")
        print(f"   Portfolio boost from aggressive early allocation: ${ag_10_median - trinity_10_median:,.0f}")
        print()
        
        # Year 20 Analysis (Age 85 - Second Transition Point)
        print("🎂 YEAR 20 (AGE 85) - SECOND REALLOCATION DECISION")
        print("-" * 60)
        print("Decision: Reduce from 70% to 40% stocks")
        print()
        
        self.print_distribution_stats("Aggressive Glide Path", ag_20)
        self.print_distribution_stats("Trinity Study (60/40)", trinity_20)
        
        # Calculate advantage
        ag_20_median = np.median(ag_20)
        trinity_20_median = np.median(trinity_20)
        advantage_20 = (ag_20_median / trinity_20_median - 1) * 100
        
        print(f"💡 Aggressive Glide Advantage at Year 20: {advantage_20:+.1f}%")
        print(f"   Remaining advantage after higher withdrawals: ${ag_20_median - trinity_20_median:,.0f}")
        print()
        
        # Final Analysis
        print("🏁 FINAL OUTCOME (AGE 94)")
        print("-" * 40)
        
        self.print_distribution_stats("Aggressive Glide Path", ag_final)
        self.print_distribution_stats("Trinity Study (60/40)", trinity_final)
        
        # Success rates
        ag_success = np.mean(ag_final > 0) * 100
        trinity_success = np.mean(trinity_final > 0) * 100
        
        print(f"💡 Success Rates:")
        print(f"   Aggressive Glide Path: {ag_success:.1f}%")
        print(f"   Trinity Study: {trinity_success:.1f}%")
        print(f"   Success rate difference: {ag_success - trinity_success:+.1f}%")
        print()
        
        return {
            'year_10': {'aggressive': ag_10, 'trinity': trinity_10},
            'year_20': {'aggressive': ag_20, 'trinity': trinity_20},
            'final': {'aggressive': ag_final, 'trinity': trinity_final}
        }
    
    def print_distribution_stats(self, strategy_name, values):
        """Print detailed distribution statistics"""
        
        # Remove zeros for meaningful percentile calculations
        non_zero_values = values[values > 0]
        failure_rate = (len(values) - len(non_zero_values)) / len(values) * 100
        
        if len(non_zero_values) > 0:
            print(f"{strategy_name}:")
            print(f"  • Median: ${np.median(non_zero_values):,.0f}")
            print(f"  • Mean: ${np.mean(non_zero_values):,.0f}")
            print(f"  • 10th percentile: ${np.percentile(non_zero_values, 10):,.0f}")
            print(f"  • 25th percentile: ${np.percentile(non_zero_values, 25):,.0f}")
            print(f"  • 75th percentile: ${np.percentile(non_zero_values, 75):,.0f}")
            print(f"  • 90th percentile: ${np.percentile(non_zero_values, 90):,.0f}")
            print(f"  • Standard deviation: ${np.std(non_zero_values):,.0f}")
            if failure_rate > 0:
                print(f"  • Failure rate: {failure_rate:.1f}%")
        else:
            print(f"{strategy_name}: All simulations failed")
        print()
    
    def create_distribution_visualization(self, distributions):
        """Create comprehensive distribution visualization"""
        
        fig = plt.figure(figsize=(20, 16))
        
        # Create a complex subplot layout
        gs = fig.add_gridspec(4, 3, height_ratios=[1, 1, 1, 0.8], hspace=0.3, wspace=0.3)
        
        # Year 10 distributions
        ax1 = fig.add_subplot(gs[0, 0])
        ax2 = fig.add_subplot(gs[0, 1])
        ax3 = fig.add_subplot(gs[0, 2])
        
        # Year 20 distributions
        ax4 = fig.add_subplot(gs[1, 0])
        ax5 = fig.add_subplot(gs[1, 1])
        ax6 = fig.add_subplot(gs[1, 2])
        
        # Final distributions
        ax7 = fig.add_subplot(gs[2, 0])
        ax8 = fig.add_subplot(gs[2, 1])
        ax9 = fig.add_subplot(gs[2, 2])
        
        # Summary comparison
        ax10 = fig.add_subplot(gs[3, :])
        
        fig.suptitle('Portfolio Value Distributions at Key Decision Points', fontsize=16, fontweight='bold')
        
        # Year 10 Analysis
        self.plot_distribution_comparison(ax1, distributions['year_10'], "Year 10 (Age 75)", "histogram")
        self.plot_distribution_comparison(ax2, distributions['year_10'], "Year 10 (Age 75)", "box")
        self.plot_percentile_comparison(ax3, distributions['year_10'], "Year 10 Percentiles")
        
        # Year 20 Analysis
        self.plot_distribution_comparison(ax4, distributions['year_20'], "Year 20 (Age 85)", "histogram")
        self.plot_distribution_comparison(ax5, distributions['year_20'], "Year 20 (Age 85)", "box")
        self.plot_percentile_comparison(ax6, distributions['year_20'], "Year 20 Percentiles")
        
        # Final Analysis
        self.plot_distribution_comparison(ax7, distributions['final'], "Final (Age 94)", "histogram")
        self.plot_distribution_comparison(ax8, distributions['final'], "Final (Age 94)", "box")
        self.plot_percentile_comparison(ax9, distributions['final'], "Final Percentiles")
        
        # Summary timeline
        self.plot_median_timeline(ax10, distributions)
        
        # Save the plot
        output_dir = project_root / 'output' / 'charts'
        os.makedirs(output_dir, exist_ok=True)
        plt.savefig(f'{output_dir}/portfolio_distributions_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return fig
    
    def plot_distribution_comparison(self, ax, data, title, plot_type):
        """Plot distribution comparison between strategies"""
        
        ag_data = data['aggressive'][data['aggressive'] > 0] / 1000000  # Convert to millions
        trinity_data = data['trinity'][data['trinity'] > 0] / 1000000
        
        if plot_type == "histogram":
            ax.hist(ag_data, bins=50, alpha=0.7, label='Aggressive Glide', color='green', density=True)
            ax.hist(trinity_data, bins=50, alpha=0.7, label='Trinity Study', color='blue', density=True)
            ax.set_xlabel('Portfolio Value ($M)')
            ax.set_ylabel('Density')
        elif plot_type == "box":
            box_data = [ag_data, trinity_data]
            box_labels = ['Aggressive\nGlide', 'Trinity\nStudy']
            bp = ax.boxplot(box_data, labels=box_labels, patch_artist=True)
            bp['boxes'][0].set_facecolor('lightgreen')
            bp['boxes'][1].set_facecolor('lightblue')
            ax.set_ylabel('Portfolio Value ($M)')
        
        ax.set_title(title)
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    def plot_percentile_comparison(self, ax, data, title):
        """Plot percentile comparison"""
        
        percentiles = [5, 10, 25, 50, 75, 90, 95]
        
        ag_data = data['aggressive'][data['aggressive'] > 0]
        trinity_data = data['trinity'][data['trinity'] > 0]
        
        ag_percentiles = [np.percentile(ag_data, p) / 1000000 for p in percentiles]
        trinity_percentiles = [np.percentile(trinity_data, p) / 1000000 for p in percentiles]
        
        ax.plot(percentiles, ag_percentiles, 'o-', label='Aggressive Glide', color='green', linewidth=2)
        ax.plot(percentiles, trinity_percentiles, 's-', label='Trinity Study', color='blue', linewidth=2)
        
        ax.set_xlabel('Percentile')
        ax.set_ylabel('Portfolio Value ($M)')
        ax.set_title(title)
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    def plot_median_timeline(self, ax, distributions):
        """Plot median values over time"""
        
        time_points = ['Year 10\n(Age 75)', 'Year 20\n(Age 85)', 'Final\n(Age 94)']
        
        ag_medians = [
            np.median(distributions['year_10']['aggressive']) / 1000000,
            np.median(distributions['year_20']['aggressive']) / 1000000,
            np.median(distributions['final']['aggressive']) / 1000000
        ]
        
        trinity_medians = [
            np.median(distributions['year_10']['trinity']) / 1000000,
            np.median(distributions['year_20']['trinity']) / 1000000,
            np.median(distributions['final']['trinity']) / 1000000
        ]
        
        x = range(len(time_points))
        
        ax.plot(x, ag_medians, 'o-', label='Aggressive Glide Path', color='green', linewidth=3, markersize=8)
        ax.plot(x, trinity_medians, 's-', label='Trinity Study', color='blue', linewidth=3, markersize=8)
        
        # Add decision annotations
        ax.annotate('Decision: 100% → 70% stocks', xy=(0, ag_medians[0]), xytext=(0, ag_medians[0] + 0.3),
                   arrowprops=dict(arrowstyle='->', color='red'), color='red', fontweight='bold')
        ax.annotate('Decision: 70% → 40% stocks', xy=(1, ag_medians[1]), xytext=(1, ag_medians[1] + 0.2),
                   arrowprops=dict(arrowstyle='->', color='red'), color='red', fontweight='bold')
        
        ax.set_xticks(x)
        ax.set_xticklabels(time_points)
        ax.set_ylabel('Median Portfolio Value ($M)')
        ax.set_title('Median Portfolio Evolution with Decision Points')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    def run_complete_analysis(self, n_simulations=10000):
        """Run the complete portfolio distribution analysis"""
        
        print("📈 PORTFOLIO VALUE DISTRIBUTION ANALYSIS")
        print("=" * 70)
        print("Examining portfolio distributions at key reallocation decision points")
        print("for the optimal Aggressive Glide Path strategy")
        print()
        
        # Run simulation
        results = self.run_distribution_simulation(n_simulations)
        
        # Analyze distributions
        distributions = self.analyze_distributions(results)
        
        # Create visualization
        print("📊 Generating distribution visualization...")
        self.create_distribution_visualization(distributions)
        
        print("✅ Analysis complete!")
        print("📊 Visualization saved: output/charts/portfolio_distributions_analysis.png")
        
        return results, distributions


def main():
    """Run the portfolio distribution analysis"""
    analyzer = PortfolioDistributionAnalysis()
    analyzer.run_complete_analysis(n_simulations=10000)


if __name__ == "__main__":
    main()