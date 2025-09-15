#!/usr/bin/env python3
"""
Strategy Comparison Script for QOL Retirement Theory

Compares Traditional 4%, QOL Standard, and QOL Enhanced withdrawal strategies
with comprehensive analysis and professional reporting.

Author: QOL Retirement Theory Research Team
Date: September 14, 2025
"""

import sys
import os
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from pathlib import Path

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from enhanced_qol_framework import EnhancedQOLFramework
from reportlab_generator import QOLReportLabGenerator as ReportLabGenerator

# Set matplotlib style for professional charts
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class StrategyComparison:
    """Comprehensive comparison of retirement withdrawal strategies."""
    
    def __init__(self, initial_portfolio=1000000, retirement_age=70, simulation_years=35):
        """Initialize comparison with standardized parameters."""
        self.initial_portfolio = initial_portfolio
        self.retirement_age = retirement_age
        self.simulation_years = simulation_years
        self.num_simulations = 1000
        
        # Strategy definitions
        self.strategies = {
            'traditional_4pct': {
                'name': 'Traditional 4%',
                'description': 'Fixed 4% withdrawal rate (industry standard)',
                'qol_phase1_rate': 0.04,
                'qol_phase2_rate': 0.04,
                'qol_phase3_rate': 0.04,
                'color': '#2E86AB'
            },
            'qol_standard': {
                'name': 'QOL Standard',
                'description': 'Hauenstein QOL strategy (5.4%/4.5%/3.5%)',
                'qol_phase1_rate': 0.054,
                'qol_phase2_rate': 0.045,
                'qol_phase3_rate': 0.035,
                'color': '#A23B72'
            },
            'qol_enhanced': {
                'name': 'QOL Enhanced',
                'description': 'Higher quality-of-life approach (7%/5.5%/4%)',
                'qol_phase1_rate': 0.07,
                'qol_phase2_rate': 0.055,
                'qol_phase3_rate': 0.04,
                'color': '#F18F01'
            }
        }
        
        self.results = {}
        self.charts_dir = Path("output/charts")
        self.reports_dir = Path("output/reports")
        
        # Create output directories
        self.charts_dir.mkdir(parents=True, exist_ok=True)
        self.reports_dir.mkdir(parents=True, exist_ok=True)
    
    def run_strategy_simulation(self, strategy_key):
        """Run simulation for a specific strategy."""
        strategy = self.strategies[strategy_key]
        
        print(f"\n🔄 Running {strategy['name']} simulation...")
        
        # Create framework instance with strategy parameters
        framework = EnhancedQOLFramework(
            starting_value=self.initial_portfolio,
            starting_age=self.retirement_age,
            horizon_years=self.simulation_years,
            n_simulations=self.num_simulations,
            qol_phase1_rate=strategy['qol_phase1_rate'],
            qol_phase2_rate=strategy['qol_phase2_rate'],
            qol_phase3_rate=strategy['qol_phase3_rate']
        )
        
        # Run enhanced analysis
        framework.run_enhanced_simulation()
        results = framework.get_comprehensive_analysis()
        
        # Store results with strategy metadata
        self.results[strategy_key] = {
            'strategy_info': strategy,
            'framework_results': results,
            'framework': framework
        }
        
        # Extract key metrics for easy access
        enhanced_qol_results = results['enhanced_qol_results']
        depletion_analysis = results['depletion_analysis']
        
        portfolio_analysis = enhanced_qol_results['portfolio_analysis']
        risk_metrics = depletion_analysis['risk_metrics']
        
        strategy_summary = {
            'name': strategy['name'],
            'description': strategy['description'],
            'withdrawal_rates': f"{strategy['qol_phase1_rate']:.1%}/{strategy['qol_phase2_rate']:.1%}/{strategy['qol_phase3_rate']:.1%}",
            'avg_final_value': portfolio_analysis['final_value_mean'],
            'median_final_value': portfolio_analysis['final_value_median'],
            'min_final_value': portfolio_analysis['final_value_percentiles']['5th'],
            'max_final_value': portfolio_analysis['final_value_percentiles']['95th'],
            'depletion_rate': risk_metrics['depletion_rate'],
            'avg_withdrawal_year1': strategy['qol_phase1_rate'] * self.initial_portfolio,
            'total_withdrawals_avg': enhanced_qol_results.get('withdrawal_analysis', {}).get('total_withdrawals_mean', 0),
            'survival_rate': 1.0 - risk_metrics['depletion_rate']
        }
        
        self.results[strategy_key]['summary'] = strategy_summary
        
        print(f"✅ {strategy['name']} completed:")
        print(f"   Average Final Value: ${strategy_summary['avg_final_value']:,.0f}")
        print(f"   First Year Withdrawal: ${strategy_summary['avg_withdrawal_year1']:,.0f}")
        print(f"   Portfolio Survival Rate: {strategy_summary['survival_rate']:.1%}")
        
        return results
    
    def run_all_strategies(self):
        """Run simulations for all strategies."""
        print("🚀 Starting comprehensive strategy comparison...")
        print(f"📊 Parameters: ${self.initial_portfolio:,} portfolio, retire at {self.retirement_age}, {self.simulation_years} years")
        
        for strategy_key in self.strategies.keys():
            self.run_strategy_simulation(strategy_key)
        
        print(f"\n✅ All strategy simulations completed!")
    
    def create_comparison_charts(self):
        """Generate comprehensive comparison charts."""
        print("\n📈 Creating comparison charts...")
        
        # Set up the plotting style
        plt.rcParams.update({
            'font.size': 10,
            'axes.titlesize': 12,
            'axes.labelsize': 10,
            'xtick.labelsize': 9,
            'ytick.labelsize': 9,
            'legend.fontsize': 9
        })
        
        # Create a comprehensive comparison figure
        fig = plt.figure(figsize=(16, 12))
        
        # Chart 1: Portfolio Value Over Time (Average Paths)
        ax1 = plt.subplot(2, 3, 1)
        years = range(self.simulation_years + 1)
        
        for strategy_key, result in self.results.items():
            strategy = result['strategy_info']
            framework = result['framework']
            
            # Get average portfolio values over time
            portfolio_paths = np.array(framework.simulation_results['portfolio_paths'])
            avg_portfolios = np.mean(portfolio_paths, axis=0)
            
            plt.plot(years, avg_portfolios / 1000000, 
                    label=strategy['name'], 
                    color=strategy['color'], 
                    linewidth=2.5)
        
        plt.title('Portfolio Value Over Time\n(Average of 1,000 Simulations)', fontweight='bold')
        plt.xlabel('Years into Retirement')
        plt.ylabel('Portfolio Value ($ Millions)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Chart 2: Annual Withdrawal Amounts
        ax2 = plt.subplot(2, 3, 2)
        
        for strategy_key, result in self.results.items():
            strategy = result['strategy_info']
            framework = result['framework']
            
            # Get average withdrawal amounts over time
            withdrawal_paths = np.array(framework.simulation_results['withdrawal_paths'])
            avg_withdrawals = np.mean(withdrawal_paths, axis=0)
            
            plt.plot(years[:-1], avg_withdrawals / 1000, 
                    label=strategy['name'], 
                    color=strategy['color'], 
                    linewidth=2.5)
        
        plt.title('Annual Withdrawal Amounts\n(Average of 1,000 Simulations)', fontweight='bold')
        plt.xlabel('Years into Retirement')
        plt.ylabel('Annual Withdrawal ($000s)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Chart 3: Final Portfolio Value Distribution
        ax3 = plt.subplot(2, 3, 3)
        
        final_values_data = []
        strategy_names = []
        colors = []
        
        for strategy_key, result in self.results.items():
            strategy = result['strategy_info']
            framework = result['framework']
            
            final_values = np.array(framework.simulation_results['portfolio_paths'])[:, -1] / 1000000
            final_values_data.append(final_values)
            strategy_names.append(strategy['name'])
            colors.append(strategy['color'])
        
        box_plot = plt.boxplot(final_values_data, labels=strategy_names, patch_artist=True)
        for patch, color in zip(box_plot['boxes'], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
        
        plt.title('Final Portfolio Value Distribution\n(After 35 Years)', fontweight='bold')
        plt.ylabel('Final Portfolio Value ($ Millions)')
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        
        # Chart 4: Key Metrics Comparison (Bar Chart)
        ax4 = plt.subplot(2, 3, 4)
        
        strategies_list = list(self.results.keys())
        avg_final_values = [self.results[s]['summary']['avg_final_value'] / 1000000 for s in strategies_list]
        strategy_colors = [self.strategies[s]['color'] for s in strategies_list]
        strategy_labels = [self.strategies[s]['name'] for s in strategies_list]
        
        bars = plt.bar(strategy_labels, avg_final_values, color=strategy_colors, alpha=0.8)
        plt.title('Average Final Portfolio Value\n($ Millions)', fontweight='bold')
        plt.ylabel('Portfolio Value ($ Millions)')
        plt.xticks(rotation=45)
        
        # Add value labels on bars
        for bar, value in zip(bars, avg_final_values):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
                    f'${value:.1f}M', ha='center', va='bottom', fontweight='bold')
        
        plt.grid(True, alpha=0.3)
        
        # Chart 5: First Year Withdrawal Comparison
        ax5 = plt.subplot(2, 3, 5)
        
        first_year_withdrawals = [self.results[s]['summary']['avg_withdrawal_year1'] / 1000 for s in strategies_list]
        
        bars = plt.bar(strategy_labels, first_year_withdrawals, color=strategy_colors, alpha=0.8)
        plt.title('First Year Withdrawal Amount\n($000s)', fontweight='bold')
        plt.ylabel('Annual Withdrawal ($000s)')
        plt.xticks(rotation=45)
        
        # Add value labels on bars
        for bar, value in zip(bars, first_year_withdrawals):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                    f'${value:.0f}K', ha='center', va='bottom', fontweight='bold')
        
        plt.grid(True, alpha=0.3)
        
        # Chart 6: Portfolio Survival Rates
        ax6 = plt.subplot(2, 3, 6)
        
        survival_rates = [self.results[s]['summary']['survival_rate'] * 100 for s in strategies_list]
        
        bars = plt.bar(strategy_labels, survival_rates, color=strategy_colors, alpha=0.8)
        plt.title('Portfolio Survival Rate\n(% of Simulations)', fontweight='bold')
        plt.ylabel('Survival Rate (%)')
        plt.ylim(95, 101)  # Focus on the high range since all should be near 100%
        plt.xticks(rotation=45)
        
        # Add value labels on bars
        for bar, value in zip(bars, survival_rates):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                    f'{value:.1f}%', ha='center', va='bottom', fontweight='bold')
        
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Save the comprehensive chart
        chart_path = self.charts_dir / "strategy_comparison_comprehensive.png"
        plt.savefig(chart_path, dpi=300, bbox_inches='tight')
        print(f"💾 Saved comprehensive comparison chart: {chart_path}")
        
        # Create a summary table chart
        self.create_summary_table_chart()
        
        plt.show()
        
        return chart_path
    
    def create_summary_table_chart(self):
        """Create a professional summary table as a chart."""
        fig, ax = plt.subplots(figsize=(14, 8))
        ax.axis('tight')
        ax.axis('off')
        
        # Prepare data for table
        table_data = []
        headers = ['Strategy', 'Withdrawal Rates', 'First Year ($)', 'Avg Final Value', 'Min Final Value', 'Survival Rate']
        
        for strategy_key in self.results.keys():
            summary = self.results[strategy_key]['summary']
            
            row = [
                summary['name'],
                summary['withdrawal_rates'],
                f"${summary['avg_withdrawal_year1']:,.0f}",
                f"${summary['avg_final_value']:,.0f}",
                f"${summary['min_final_value']:,.0f}",
                f"{summary['survival_rate']:.1%}"
            ]
            table_data.append(row)
        
        # Create table
        table = ax.table(cellText=table_data, colLabels=headers, 
                        cellLoc='center', loc='center')
        
        # Style the table
        table.auto_set_font_size(False)
        table.set_fontsize(11)
        table.scale(1.2, 2)
        
        # Color headers
        for i in range(len(headers)):
            table[(0, i)].set_facecolor('#4CAF50')
            table[(0, i)].set_text_props(weight='bold', color='white')
        
        # Color strategy rows
        colors = ['#E3F2FD', '#F3E5F5', '#FFF3E0']
        for i, color in enumerate(colors):
            for j in range(len(headers)):
                table[(i+1, j)].set_facecolor(color)
        
        plt.title('Strategy Comparison Summary\nStandardized $1M Portfolio, Retire at 70, 35-Year Horizon', 
                 fontsize=14, fontweight='bold', pad=20)
        
        # Save summary table
        summary_path = self.charts_dir / "strategy_comparison_summary_table.png"
        plt.savefig(summary_path, dpi=300, bbox_inches='tight')
        print(f"💾 Saved summary table: {summary_path}")
        
        plt.show()
        
        return summary_path
    
    def generate_comparison_report(self):
        """Generate comprehensive PDF report with all strategies."""
        print("\n📋 Generating comprehensive comparison report...")
        
        # Prepare consolidated data for ReportLab
        report_data = {
            'scenario_info': {
                'scenario_name': 'QOL Strategy Comparison Analysis',
                'portfolio_value': self.initial_portfolio,
                'retirement_age': self.retirement_age,
                'simulation_years': self.simulation_years,
                'num_simulations': self.num_simulations,
                'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            },
            'strategies': {}
        }
        
        # Add each strategy's results
        for strategy_key, result in self.results.items():
            strategy_info = result['strategy_info']
            framework_results = result['framework_results']
            summary = result['summary']
            
            report_data['strategies'][strategy_key] = {
                'name': strategy_info['name'],
                'description': strategy_info['description'],
                'withdrawal_rates': f"{strategy_info['qol_phase1_rate']:.1%}/{strategy_info['qol_phase2_rate']:.1%}/{strategy_info['qol_phase3_rate']:.1%}",
                'portfolio_analysis': framework_results['enhanced_qol_results']['portfolio_analysis'],
                'risk_metrics': framework_results['depletion_analysis']['risk_metrics'],
                'summary_metrics': summary
            }
        
        # Generate comparison report
        generator = ReportLabGenerator()
        report_path = generator.create_strategy_comparison_report(report_data)
        
        print(f"✅ Comparison report generated: {report_path}")
        return report_path

def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(description='Compare retirement withdrawal strategies')
    parser.add_argument('--portfolio', type=float, default=1000000,
                       help='Initial portfolio value (default: $1,000,000)')
    parser.add_argument('--age', type=int, default=70,
                       help='Retirement age (default: 70)')
    parser.add_argument('--years', type=int, default=35,
                       help='Simulation years (default: 35)')
    parser.add_argument('--no-charts', action='store_true',
                       help='Skip chart generation')
    parser.add_argument('--no-report', action='store_true',
                       help='Skip PDF report generation')
    
    args = parser.parse_args()
    
    print("🏁 QOL Retirement Strategy Comparison")
    print("=" * 50)
    
    # Create comparison instance
    comparison = StrategyComparison(
        initial_portfolio=args.portfolio,
        retirement_age=args.age,
        simulation_years=args.years
    )
    
    # Run all strategy simulations
    comparison.run_all_strategies()
    
    # Generate charts
    if not args.no_charts:
        comparison.create_comparison_charts()
    
    # Generate report
    if not args.no_report:
        comparison.generate_comparison_report()
    
    print("\n🎉 Strategy comparison completed successfully!")
    print(f"\n📁 Results saved to:")
    print(f"   Charts: {comparison.charts_dir}")
    print(f"   Reports: {comparison.reports_dir}")

if __name__ == "__main__":
    main()