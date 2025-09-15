"""
CONDITIONAL SUCCESS ANALYSIS

This analysis examines portfolio distributions specifically for successful scenarios
to understand when the Aggressive Glide Path strategy outperforms and the magnitude
of benefits in those successful cases.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from pathlib import Path

# Find project root directory
script_dir = Path(__file__).parent
project_root = script_dir.parent

class ConditionalSuccessAnalysis:
    """
    Analyze portfolio distributions conditional on success
    """
    
    def __init__(self):
        self.strategy = {
            'phase1': {'expected_return': 0.072, 'volatility': 0.20, 'qol_multiplier': 1.35},
            'phase2': {'expected_return': 0.060, 'volatility': 0.165, 'qol_multiplier': 1.125},
            'phase3': {'expected_return': 0.045, 'volatility': 0.135, 'qol_multiplier': 0.875}
        }
        
        self.trinity_strategy = {
            'expected_return': 0.055, 'volatility': 0.15, 'qol_multiplier': 1.0
        }
    
    def run_conditional_analysis(self, n_simulations=10000):
        """Run analysis focusing on successful scenarios"""
        
        print("🎯 CONDITIONAL SUCCESS ANALYSIS")
        print("=" * 60)
        print("Examining portfolio distributions for successful scenarios only")
        print()
        
        np.random.seed(42)
        starting_portfolio = 1000000
        
        # Storage for successful scenarios only
        successful_scenarios = {
            'aggressive_glide': {
                'year_10': [], 'year_20': [], 'final': [],
                'total_withdrawals': [], 'total_enjoyment': []
            },
            'trinity': {
                'year_10': [], 'year_20': [], 'final': [],
                'total_withdrawals': []
            }
        }
        
        for sim in range(n_simulations):
            # Aggressive Glide Path simulation
            ag_results = self.simulate_aggressive_glide(starting_portfolio)
            
            # Trinity Study simulation  
            trinity_results = self.simulate_trinity(starting_portfolio)
            
            # Store only successful scenarios
            if ag_results['final_value'] > 0:
                successful_scenarios['aggressive_glide']['year_10'].append(ag_results['year_10_value'])
                successful_scenarios['aggressive_glide']['year_20'].append(ag_results['year_20_value'])
                successful_scenarios['aggressive_glide']['final'].append(ag_results['final_value'])
                successful_scenarios['aggressive_glide']['total_withdrawals'].append(ag_results['total_withdrawals'])
                successful_scenarios['aggressive_glide']['total_enjoyment'].append(ag_results['total_enjoyment'])
            
            if trinity_results['final_value'] > 0:
                successful_scenarios['trinity']['year_10'].append(trinity_results['year_10_value'])
                successful_scenarios['trinity']['year_20'].append(trinity_results['year_20_value'])
                successful_scenarios['trinity']['final'].append(trinity_results['final_value'])
                successful_scenarios['trinity']['total_withdrawals'].append(trinity_results['total_withdrawals'])
        
        return successful_scenarios
    
    def simulate_aggressive_glide(self, starting_portfolio):
        """Simulate Aggressive Glide Path strategy"""
        
        portfolio_value = starting_portfolio
        cumulative_inflation = 1.0
        total_withdrawals = 0
        total_enjoyment = 0
        year_10_value = 0
        year_20_value = 0
        
        for year in range(29):
            # Determine phase
            if year < 10:
                phase_params = self.strategy['phase1']
                enjoyment_weight = 1.5  # High enjoyment period
            elif year < 20:
                phase_params = self.strategy['phase2']
                enjoyment_weight = 1.2  # Moderate enjoyment period
            else:
                phase_params = self.strategy['phase3']
                enjoyment_weight = 1.0  # Low enjoyment period
            
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
            
            # Track metrics
            total_withdrawals += qol_withdrawal
            total_enjoyment += qol_withdrawal * enjoyment_weight
            
            if year == 9:
                year_10_value = portfolio_value
            elif year == 19:
                year_20_value = portfolio_value
        
        return {
            'final_value': portfolio_value,
            'year_10_value': year_10_value,
            'year_20_value': year_20_value,
            'total_withdrawals': total_withdrawals,
            'total_enjoyment': total_enjoyment
        }
    
    def simulate_trinity(self, starting_portfolio):
        """Simulate Trinity Study strategy"""
        
        portfolio_value = starting_portfolio
        cumulative_inflation = 1.0
        total_withdrawals = 0
        year_10_value = 0
        year_20_value = 0
        
        for year in range(29):
            # Inflation
            inflation_rate = np.random.normal(0.03, 0.01)
            cumulative_inflation *= (1 + inflation_rate)
            
            # Portfolio return
            annual_return = np.random.normal(
                self.trinity_strategy['expected_return'],
                self.trinity_strategy['volatility']
            )
            
            # Trinity withdrawal
            trinity_withdrawal = starting_portfolio * 0.04 * cumulative_inflation
            
            # Apply growth and withdrawal
            pre_withdrawal_value = portfolio_value * (1 + annual_return)
            portfolio_value = max(0, pre_withdrawal_value - trinity_withdrawal)
            
            total_withdrawals += trinity_withdrawal
            
            if year == 9:
                year_10_value = portfolio_value
            elif year == 19:
                year_20_value = portfolio_value
        
        return {
            'final_value': portfolio_value,
            'year_10_value': year_10_value,
            'year_20_value': year_20_value,
            'total_withdrawals': total_withdrawals
        }
    
    def analyze_successful_scenarios(self, successful_scenarios):
        """Analyze the successful scenarios"""
        
        print("📊 SUCCESSFUL SCENARIOS ANALYSIS")
        print("=" * 50)
        print()
        
        ag_success_count = len(successful_scenarios['aggressive_glide']['final'])
        trinity_success_count = len(successful_scenarios['trinity']['final'])
        
        print(f"Successful Simulations:")
        print(f"  • Aggressive Glide Path: {ag_success_count:,} ({ag_success_count/100:.1f}%)")
        print(f"  • Trinity Study: {trinity_success_count:,} ({trinity_success_count/100:.1f}%)")
        print()
        
        # Convert to numpy arrays
        ag_year_10 = np.array(successful_scenarios['aggressive_glide']['year_10'])
        ag_year_20 = np.array(successful_scenarios['aggressive_glide']['year_20'])
        ag_final = np.array(successful_scenarios['aggressive_glide']['final'])
        ag_enjoyment = np.array(successful_scenarios['aggressive_glide']['total_enjoyment'])
        
        trinity_year_10 = np.array(successful_scenarios['trinity']['year_10'])
        trinity_year_20 = np.array(successful_scenarios['trinity']['year_20'])
        trinity_final = np.array(successful_scenarios['trinity']['final'])
        
        # Year 10 Analysis (Successful scenarios only)
        print("🎂 YEAR 10 (AGE 75) - SUCCESSFUL SCENARIOS ONLY")
        print("-" * 60)
        
        print("Aggressive Glide Path (Successful scenarios):")
        self.print_success_stats(ag_year_10)
        
        print("Trinity Study (Successful scenarios):")
        self.print_success_stats(trinity_year_10)
        
        # Calculate advantage in successful scenarios
        ag_10_med_success = np.median(ag_year_10)
        trinity_10_med_success = np.median(trinity_year_10)
        advantage_10_success = (ag_10_med_success / trinity_10_med_success - 1) * 100
        
        print(f"💡 Year 10 Advantage (Successful scenarios): {advantage_10_success:+.1f}%")
        print(f"   Median difference: ${ag_10_med_success - trinity_10_med_success:,.0f}")
        print()
        
        # Year 20 Analysis (Successful scenarios only)
        print("🎂 YEAR 20 (AGE 85) - SUCCESSFUL SCENARIOS ONLY")
        print("-" * 60)
        
        print("Aggressive Glide Path (Successful scenarios):")
        self.print_success_stats(ag_year_20)
        
        print("Trinity Study (Successful scenarios):")
        self.print_success_stats(trinity_year_20)
        
        ag_20_med_success = np.median(ag_year_20)
        trinity_20_med_success = np.median(trinity_year_20)
        advantage_20_success = (ag_20_med_success / trinity_20_med_success - 1) * 100
        
        print(f"💡 Year 20 Advantage (Successful scenarios): {advantage_20_success:+.1f}%")
        print(f"   Median difference: ${ag_20_med_success - trinity_20_med_success:,.0f}")
        print()
        
        # Final Analysis (Successful scenarios only)
        print("🏁 FINAL OUTCOME - SUCCESSFUL SCENARIOS ONLY")
        print("-" * 50)
        
        print("Aggressive Glide Path (Successful scenarios):")
        self.print_success_stats(ag_final)
        
        print("Trinity Study (Successful scenarios):")
        self.print_success_stats(trinity_final)
        
        ag_final_med_success = np.median(ag_final)
        trinity_final_med_success = np.median(trinity_final)
        advantage_final_success = (ag_final_med_success / trinity_final_med_success - 1) * 100
        
        print(f"💡 Final Advantage (Successful scenarios): {advantage_final_success:+.1f}%")
        print(f"   Median difference: ${ag_final_med_success - trinity_final_med_success:,.0f}")
        print()
        
        # Enjoyment Analysis
        print("🎉 ENJOYMENT VALUE ANALYSIS")
        print("-" * 40)
        
        ag_enjoyment_med = np.median(ag_enjoyment)
        
        # Calculate equivalent Trinity enjoyment (using 1.2x average weight)
        trinity_withdrawals = np.array(successful_scenarios['trinity']['total_withdrawals'][:len(ag_enjoyment)])
        trinity_equivalent_enjoyment = trinity_withdrawals * 1.2
        trinity_enjoyment_med = np.median(trinity_equivalent_enjoyment)
        
        enjoyment_advantage = (ag_enjoyment_med / trinity_enjoyment_med - 1) * 100
        
        print(f"Median total enjoyment value:")
        print(f"  • Aggressive Glide Path: ${ag_enjoyment_med:,.0f}")
        print(f"  • Trinity Study (equivalent): ${trinity_enjoyment_med:,.0f}")
        print(f"  • Enjoyment advantage: {enjoyment_advantage:+.1f}%")
        print()
        
        return {
            'success_rates': {'aggressive': ag_success_count/100, 'trinity': trinity_success_count/100},
            'advantages': {
                'year_10': advantage_10_success,
                'year_20': advantage_20_success,
                'final': advantage_final_success,
                'enjoyment': enjoyment_advantage
            }
        }
    
    def print_success_stats(self, values):
        """Print statistics for successful scenarios"""
        print(f"  • Count: {len(values):,}")
        print(f"  • Median: ${np.median(values):,.0f}")
        print(f"  • Mean: ${np.mean(values):,.0f}")
        print(f"  • 25th percentile: ${np.percentile(values, 25):,.0f}")
        print(f"  • 75th percentile: ${np.percentile(values, 75):,.0f}")
        print()
    
    def create_success_visualization(self, successful_scenarios):
        """Create visualization for successful scenarios"""
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Portfolio Distributions: Successful Scenarios Only', fontsize=16, fontweight='bold')
        
        # Convert to millions for better readability
        ag_year_10 = np.array(successful_scenarios['aggressive_glide']['year_10']) / 1000000
        ag_year_20 = np.array(successful_scenarios['aggressive_glide']['year_20']) / 1000000
        trinity_year_10 = np.array(successful_scenarios['trinity']['year_10']) / 1000000
        trinity_year_20 = np.array(successful_scenarios['trinity']['year_20']) / 1000000
        
        # Year 10 comparison
        ax1.hist(ag_year_10, bins=50, alpha=0.7, label='Aggressive Glide', color='green', density=True)
        ax1.hist(trinity_year_10, bins=50, alpha=0.7, label='Trinity Study', color='blue', density=True)
        ax1.set_xlabel('Portfolio Value ($M)')
        ax1.set_ylabel('Density')
        ax1.set_title('Year 10 (Age 75) - Successful Scenarios')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Year 20 comparison
        ax2.hist(ag_year_20, bins=50, alpha=0.7, label='Aggressive Glide', color='green', density=True)
        ax2.hist(trinity_year_20, bins=50, alpha=0.7, label='Trinity Study', color='blue', density=True)
        ax2.set_xlabel('Portfolio Value ($M)')
        ax2.set_ylabel('Density')
        ax2.set_title('Year 20 (Age 85) - Successful Scenarios')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Box plot comparison - Year 10
        box_data_10 = [ag_year_10, trinity_year_10]
        bp1 = ax3.boxplot(box_data_10, labels=['Aggressive\nGlide', 'Trinity\nStudy'], patch_artist=True)
        bp1['boxes'][0].set_facecolor('lightgreen')
        bp1['boxes'][1].set_facecolor('lightblue')
        ax3.set_ylabel('Portfolio Value ($M)')
        ax3.set_title('Year 10 Distribution Comparison')
        ax3.grid(True, alpha=0.3)
        
        # Box plot comparison - Year 20
        box_data_20 = [ag_year_20, trinity_year_20]
        bp2 = ax4.boxplot(box_data_20, labels=['Aggressive\nGlide', 'Trinity\nStudy'], patch_artist=True)
        bp2['boxes'][0].set_facecolor('lightgreen')
        bp2['boxes'][1].set_facecolor('lightblue')
        ax4.set_ylabel('Portfolio Value ($M)')
        ax4.set_title('Year 20 Distribution Comparison')
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Save the plot
        output_dir = project_root / 'output' / 'charts'
        os.makedirs(output_dir, exist_ok=True)
        plt.savefig(f'{output_dir}/successful_scenarios_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return fig
    
    def run_complete_analysis(self, n_simulations=10000):
        """Run the complete conditional success analysis"""
        
        print("🎯 CONDITIONAL SUCCESS ANALYSIS")
        print("=" * 70)
        print("Focusing on successful scenarios to understand when")
        print("Aggressive Glide Path provides superior outcomes")
        print()
        
        # Run conditional analysis
        successful_scenarios = self.run_conditional_analysis(n_simulations)
        
        # Analyze successful scenarios
        summary_stats = self.analyze_successful_scenarios(successful_scenarios)
        
        # Create visualization
        print("📊 Generating successful scenarios visualization...")
        self.create_success_visualization(successful_scenarios)
        
        print("✅ Conditional analysis complete!")
        print("📊 Visualization saved: output/charts/successful_scenarios_analysis.png")
        
        return successful_scenarios, summary_stats


def main():
    """Run the conditional success analysis"""
    analyzer = ConditionalSuccessAnalysis()
    analyzer.run_complete_analysis(n_simulations=10000)


if __name__ == "__main__":
    main()