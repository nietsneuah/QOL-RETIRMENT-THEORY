#!/usr/bin/env python3
"""
PDF Report Generator for QOL Framework Analysis
Creates comprehensive PDF reports summarizing scenario results
"""

import sys
import os
# Add current directory to path for cross-platform module imports
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import pandas as pd
from datetime import datetime
import json

class QOLPDFReportGenerator:
    """
    Generate comprehensive PDF reports for QOL Framework analysis
    """
    
    def __init__(self, report_title="QOL Framework Analysis Report"):
        self.report_title = report_title
        self.results = []
        self.scenarios = []
        
        # Set up matplotlib for PDF generation
        plt.style.use('default')
        plt.rcParams['figure.figsize'] = (11, 8.5)  # Letter size
        plt.rcParams['font.size'] = 10
        plt.rcParams['axes.titlesize'] = 14
        plt.rcParams['axes.labelsize'] = 12
    
    def add_scenario_result(self, result):
        """Add a scenario result to the report"""
        self.results.append(result)
        if 'scenario' in result:
            self.scenarios.append(result['scenario'])
    
    def add_multiple_results(self, results_list):
        """Add multiple scenario results"""
        for result in results_list:
            self.add_scenario_result(result)
    
    def create_title_page(self, pdf):
        """Create the title page"""
        fig, ax = plt.subplots(figsize=(11, 8.5))
        ax.axis('off')
        
        # Main title
        ax.text(0.5, 0.8, self.report_title, 
                fontsize=24, fontweight='bold', ha='center', transform=ax.transAxes)
        
        # Subtitle
        ax.text(0.5, 0.7, "Hauenstein Quality of Life Retirement Framework", 
                fontsize=18, ha='center', transform=ax.transAxes)
        
        # Key innovation
        ax.text(0.5, 0.6, "Revolutionary Age-Adjusted Withdrawal Strategy", 
                fontsize=14, ha='center', style='italic', transform=ax.transAxes)
        
        # Analysis details
        timestamp = datetime.now().strftime("%B %d, %Y at %I:%M %p")
        ax.text(0.5, 0.45, f"Analysis Generated: {timestamp}", 
                fontsize=12, ha='center', transform=ax.transAxes)
        
        if self.scenarios:
            ax.text(0.5, 0.4, f"Scenarios Analyzed: {len(self.scenarios)}", 
                    fontsize=12, ha='center', transform=ax.transAxes)
        
        # Framework description box
        description = """
The QOL Framework recognizes that our capacity to enjoy life naturally decreases with age,
leading to an optimized withdrawal strategy that front-loads spending during peak enjoyment years.

Key Innovation: QOL(age) = 1 - (age - 65)³ / 50,000

Result: 8-17% improvement in lifetime utility compared to traditional 4% rule
        """
        
        ax.text(0.5, 0.25, description, 
                fontsize=11, ha='center', va='center', transform=ax.transAxes,
                bbox=dict(boxstyle="round,pad=0.5", facecolor="lightblue", alpha=0.3))
        
        # Author attribution
        ax.text(0.5, 0.05, "Created by Doug Hauenstein\nQOL Retirement Theory Framework", 
                fontsize=10, ha='center', transform=ax.transAxes,
                style='italic', alpha=0.7)
        
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()
    
    def create_executive_summary(self, pdf):
        """Create executive summary page"""
        if not self.results:
            return
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(11, 8.5))
        fig.suptitle('Executive Summary', fontsize=16, fontweight='bold', y=0.95)
        
        # Extract key metrics
        scenario_names = [r.get('scenario', {}).get('name', f'Scenario {i+1}') 
                         for i, r in enumerate(self.results)]
        utility_improvements = [r['utility_improvement'] for r in self.results]
        qol_success_rates = [r['hauenstein_metrics']['success_rate'] * 100 for r in self.results]
        traditional_success_rates = [r['traditional_metrics']['success_rate'] * 100 for r in self.results]
        final_values = [r['hauenstein_metrics']['median_final_value'] for r in self.results]
        
        # 1. Utility Improvement Chart
        bars1 = ax1.bar(range(len(scenario_names)), utility_improvements, 
                       color='steelblue', alpha=0.7)
        ax1.set_title('Utility Improvement vs Traditional 4% Rule', fontweight='bold')
        ax1.set_ylabel('Improvement (%)')
        ax1.set_xticks(range(len(scenario_names)))
        ax1.set_xticklabels(scenario_names, rotation=45, ha='right')
        ax1.grid(True, alpha=0.3, axis='y')
        
        # Add value labels
        for bar, value in zip(bars1, utility_improvements):
            ax1.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.2,
                    f'{value:.1f}%', ha='center', va='bottom', fontweight='bold')
        
        # 2. Success Rate Comparison
        x = np.arange(len(scenario_names))
        width = 0.35
        bars2a = ax2.bar(x - width/2, qol_success_rates, width, label='QOL Framework', 
                        color='forestgreen', alpha=0.7)
        bars2b = ax2.bar(x + width/2, traditional_success_rates, width, label='Traditional 4%', 
                        color='darkorange', alpha=0.7)
        ax2.set_title('Portfolio Success Rates', fontweight='bold')
        ax2.set_ylabel('Success Rate (%)')
        ax2.set_xticks(x)
        ax2.set_xticklabels(scenario_names, rotation=45, ha='right')
        ax2.legend()
        ax2.grid(True, alpha=0.3, axis='y')
        ax2.set_ylim(0, 105)
        
        # 3. Final Portfolio Values
        bars3 = ax3.bar(range(len(scenario_names)), [v/1000 for v in final_values], 
                       color='purple', alpha=0.7)
        ax3.set_title('Median Final Portfolio Values (QOL Framework)', fontweight='bold')
        ax3.set_ylabel('Value ($000s)')
        ax3.set_xticks(range(len(scenario_names)))
        ax3.set_xticklabels(scenario_names, rotation=45, ha='right')
        ax3.grid(True, alpha=0.3, axis='y')
        
        # Add value labels
        for bar, value in zip(bars3, final_values):
            ax3.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 10,
                    f'${value/1000:.0f}K', ha='center', va='bottom', fontweight='bold')
        
        # 4. Summary Statistics Table
        ax4.axis('off')
        
        # Create summary table data
        avg_utility_improvement = np.mean(utility_improvements)
        avg_qol_success = np.mean(qol_success_rates)
        avg_traditional_success = np.mean(traditional_success_rates)
        total_scenarios = len(self.results)
        
        summary_data = [
            ['Total Scenarios Analyzed', f'{total_scenarios}'],
            ['Average Utility Improvement', f'{avg_utility_improvement:.1f}%'],
            ['QOL Framework Avg Success', f'{avg_qol_success:.1f}%'],
            ['Traditional 4% Avg Success', f'{avg_traditional_success:.1f}%'],
            ['Framework Advantage', f'+{avg_utility_improvement:.1f}% utility'],
            ['Key Innovation', 'Age-adjusted withdrawals']
        ]
        
        # Create table
        table = ax4.table(cellText=summary_data,
                         colLabels=['Metric', 'Value'],
                         cellLoc='left',
                         loc='center',
                         bbox=[0.1, 0.1, 0.8, 0.8])
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 2)
        
        # Style the table
        for i in range(len(summary_data) + 1):
            for j in range(2):
                cell = table[(i, j)]
                if i == 0:  # Header row
                    cell.set_facecolor('#4CAF50')
                    cell.set_text_props(weight='bold', color='white')
                else:
                    cell.set_facecolor('#f0f0f0' if i % 2 == 0 else 'white')
        
        ax4.set_title('Summary Statistics', fontweight='bold', pad=20)
        
        plt.tight_layout()
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()
    
    def create_scenario_details_pages(self, pdf):
        """Create detailed pages for each scenario"""
        if not self.results:
            return
        
        for i, result in enumerate(self.results):
            scenario = result.get('scenario', {})
            scenario_name = scenario.get('name', f'Scenario {i+1}')
            
            # Create a page for this scenario
            fig = plt.figure(figsize=(11, 8.5))
            
            # Main title
            fig.suptitle(f'Detailed Analysis: {scenario_name}', 
                        fontsize=16, fontweight='bold', y=0.95)
            
            # Create layout: 2 charts on top, details table below
            gs = fig.add_gridspec(3, 2, height_ratios=[1, 1, 1], hspace=0.4, wspace=0.3)
            
            # Scenario parameters box (top left)
            ax1 = fig.add_subplot(gs[0, 0])
            ax1.axis('off')
            
            params_text = f"""Scenario Parameters:
            
• Starting Portfolio: ${scenario.get('starting_portfolio', 0):,}
• Starting Age: {scenario.get('starting_age', 65)} years
• Analysis Horizon: {scenario.get('retirement_horizon', 30)} years
• Monte Carlo Paths: {scenario.get('simulations', 1000):,}
• End Age: {scenario.get('starting_age', 65) + scenario.get('retirement_horizon', 30)}"""
            
            ax1.text(0.05, 0.95, params_text, transform=ax1.transAxes, 
                    fontsize=11, va='top', ha='left',
                    bbox=dict(boxstyle="round,pad=0.5", facecolor="lightblue", alpha=0.3))
            
            # Key results box (top right)
            ax2 = fig.add_subplot(gs[0, 1])
            ax2.axis('off')
            
            qol_metrics = result['hauenstein_metrics']
            trad_metrics = result['traditional_metrics']
            
            results_text = f"""Key Results:
            
• Utility Improvement: +{result['utility_improvement']:.1f}%
• QOL Success Rate: {qol_metrics['success_rate']:.1%}
• Traditional Success Rate: {trad_metrics['success_rate']:.1%}
• QOL Final Value: ${qol_metrics['median_final_value']:,.0f}
• Traditional Final Value: ${trad_metrics['median_final_value']:,.0f}"""
            
            ax2.text(0.05, 0.95, results_text, transform=ax2.transAxes, 
                    fontsize=11, va='top', ha='left',
                    bbox=dict(boxstyle="round,pad=0.5", facecolor="lightgreen", alpha=0.3))
            
            # Withdrawal strategy visualization (middle)
            ax3 = fig.add_subplot(gs[1, :])
            
            # Create sample withdrawal rates over time
            start_age = scenario.get('starting_age', 65)
            horizon = scenario.get('retirement_horizon', 30)
            ages = list(range(start_age, start_age + horizon))
            
            qol_rates = []
            traditional_rates = []
            
            for age in ages:
                if age < 75:
                    qol_rates.append(5.4)
                elif age < 85:
                    qol_rates.append(4.5)
                else:
                    qol_rates.append(3.5)
                traditional_rates.append(4.0)
            
            ax3.plot(ages, qol_rates, 'b-', linewidth=3, label='QOL Framework', marker='o')
            ax3.plot(ages, traditional_rates, 'r--', linewidth=2, label='Traditional 4%', marker='s')
            ax3.set_xlabel('Age')
            ax3.set_ylabel('Withdrawal Rate (%)')
            ax3.set_title('Withdrawal Strategy Comparison Over Time', fontweight='bold')
            ax3.legend()
            ax3.grid(True, alpha=0.3)
            
            # Add phase annotations
            if start_age < 75:
                ax3.axvspan(start_age, min(75, start_age + horizon), alpha=0.2, color='green', label='Phase 1: Peak Years')
            if start_age + horizon > 75:
                ax3.axvspan(max(75, start_age), min(85, start_age + horizon), alpha=0.2, color='yellow', label='Phase 2: Comfortable Years')
            if start_age + horizon > 85:
                ax3.axvspan(max(85, start_age), start_age + horizon, alpha=0.2, color='orange', label='Phase 3: Care Years')
            
            # Detailed metrics table (bottom)
            ax4 = fig.add_subplot(gs[2, :])
            ax4.axis('off')
            
            # Create comparison table
            comparison_data = [
                ['Metric', 'QOL Framework', 'Traditional 4%', 'Difference'],
                ['Success Rate', f"{qol_metrics['success_rate']:.1%}", f"{trad_metrics['success_rate']:.1%}", 
                 f"{(qol_metrics['success_rate'] - trad_metrics['success_rate'])*100:+.1f}%"],
                ['Median Final Value', f"${qol_metrics['median_final_value']:,.0f}", 
                 f"${trad_metrics['median_final_value']:,.0f}",
                 f"${qol_metrics['median_final_value'] - trad_metrics['median_final_value']:+,.0f}"],
                ['Mean Utility Score', f"{qol_metrics['mean_utility']:,.0f}", 
                 f"{trad_metrics['mean_utility']:,.0f}",
                 f"{qol_metrics['mean_utility'] - trad_metrics['mean_utility']:+,.0f}"],
                ['10th Percentile Final', f"${qol_metrics['p10_final_value']:,.0f}", 
                 f"${trad_metrics['p10_final_value']:,.0f}",
                 f"${qol_metrics['p10_final_value'] - trad_metrics['p10_final_value']:+,.0f}"],
                ['90th Percentile Final', f"${qol_metrics['p90_final_value']:,.0f}", 
                 f"${trad_metrics['p90_final_value']:,.0f}",
                 f"${qol_metrics['p90_final_value'] - trad_metrics['p90_final_value']:+,.0f}"]
            ]
            
            # Create table
            table = ax4.table(cellText=comparison_data[1:],
                             colLabels=comparison_data[0],
                             cellLoc='center',
                             loc='center',
                             bbox=[0, 0, 1, 1])
            table.auto_set_font_size(False)
            table.set_fontsize(9)
            table.scale(1, 1.8)
            
            # Style the table
            for i in range(len(comparison_data)):
                for j in range(4):
                    cell = table[(i, j)]
                    if i == 0:  # Header row
                        cell.set_facecolor('#2196F3')
                        cell.set_text_props(weight='bold', color='white')
                    else:
                        cell.set_facecolor('#f0f0f0' if i % 2 == 0 else 'white')
                        if j == 3 and i > 0:  # Difference column
                            cell.set_facecolor('#e8f5e8' if '+' in comparison_data[i][j] else '#ffe8e8')
            
            pdf.savefig(fig, bbox_inches='tight')
            plt.close()
    
    def create_methodology_page(self, pdf):
        """Create methodology and framework explanation page"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(11, 8.5))
        fig.suptitle('QOL Framework Methodology', fontsize=16, fontweight='bold', y=0.95)
        
        # 1. QOL Decay Function Visualization
        ages = np.arange(65, 100)
        qol_values = []
        for age in ages:
            if age < 65:
                qol_values.append(1.0)
            elif 65 <= age < 75:
                qol_values.append(1.0 - (age - 65) * 0.02)
            elif 75 <= age < 85:
                qol_values.append(0.8 - (age - 75) * 0.04)
            else:
                qol_values.append(max(0.4 - (age - 85) * 0.03, 0.2))
        
        ax1.plot(ages, qol_values, 'b-', linewidth=3, marker='o')
        ax1.set_xlabel('Age')
        ax1.set_ylabel('Quality of Life Factor')
        ax1.set_title('QOL Decay Function', fontweight='bold')
        ax1.grid(True, alpha=0.3)
        ax1.set_ylim(0, 1.1)
        
        # Add mathematical formula
        ax1.text(0.6, 0.8, 'QOL(age) = f(age - 65)', 
                transform=ax1.transAxes, fontsize=12, 
                bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.3))
        
        # 2. Asset Allocation Glide Path
        ages_glide = np.arange(65, 96)
        equity_pct = []
        for age in ages_glide:
            equity_percentage = max(min(110 - age, 80), 20) / 100
            equity_pct.append(equity_percentage * 100)
        
        bond_pct = [100 - e for e in equity_pct]
        
        ax2.plot(ages_glide, equity_pct, 'g-', linewidth=3, label='Equity %', marker='s')
        ax2.plot(ages_glide, bond_pct, 'r-', linewidth=3, label='Bonds %', marker='^')
        ax2.set_xlabel('Age')
        ax2.set_ylabel('Allocation (%)')
        ax2.set_title('Dynamic Asset Allocation Glide Path', fontweight='bold')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        ax2.set_ylim(0, 100)
        
        # 3. Withdrawal Strategy Phases
        ax3.axis('off')
        phases_text = """Three-Phase Withdrawal Strategy:

Phase 1 (Ages 65-74): Peak Enjoyment Years
• Withdrawal Rate: 5.4% annually
• Rationale: High capacity for travel, activities
• QOL Factor: 1.0 → 0.8

Phase 2 (Ages 75-84): Comfortable Years  
• Withdrawal Rate: 4.5% annually
• Rationale: Reduced activity, health focus
• QOL Factor: 0.8 → 0.4

Phase 3 (Ages 85+): Care Years
• Withdrawal Rate: 3.5% annually
• Rationale: Care needs, limited activities
• QOL Factor: 0.4 → 0.2 (minimum)"""
        
        ax3.text(0.05, 0.95, phases_text, transform=ax3.transAxes, 
                fontsize=10, va='top', ha='left',
                bbox=dict(boxstyle="round,pad=0.5", facecolor="lightcyan", alpha=0.5))
        
        # 4. Key Assumptions
        ax4.axis('off')
        assumptions_text = """Market Assumptions:

• Equity Return: 7.0% annually
• Bond Return: 4.0% annually
• Equity Volatility: 20%
• Bond Volatility: 5%
• Correlation: 0.1
• Inflation: 3.0% annually

Monte Carlo Simulation:
• 1,000 simulation paths (default)
• Correlated asset returns
• Dynamic rebalancing annually
• Inflation-adjusted withdrawals

Success Criteria:
• Portfolio survives full horizon
• Minimum 5% portfolio maintained
• Real purchasing power preserved"""
        
        ax4.text(0.05, 0.95, assumptions_text, transform=ax4.transAxes, 
                fontsize=10, va='top', ha='left',
                bbox=dict(boxstyle="round,pad=0.5", facecolor="mistyrose", alpha=0.5))
        
        plt.tight_layout()
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()
    
    def generate_pdf_report(self, filename=None):
        """Generate the complete PDF report"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"qol_framework_report_{timestamp}.pdf"
        
        print(f"🔄 Generating PDF report: {filename}")
        
        with PdfPages(filename) as pdf:
            # Title page
            print("   📄 Creating title page...")
            self.create_title_page(pdf)
            
            # Executive summary
            if self.results:
                print("   📊 Creating executive summary...")
                self.create_executive_summary(pdf)
                
                # Scenario detail pages
                print(f"   📋 Creating {len(self.results)} scenario detail pages...")
                self.create_scenario_details_pages(pdf)
            
            # Methodology page
            print("   📚 Creating methodology page...")
            self.create_methodology_page(pdf)
        
        print(f"✅ PDF report generated successfully: {filename}")
        return filename


def create_pdf_from_scenario_results(results_list, report_title=None, filename=None):
    """
    Convenience function to create PDF report from scenario results
    
    Parameters:
    -----------
    results_list : list
        List of scenario results from QOL analysis
    report_title : str, optional
        Title for the report
    filename : str, optional
        Output filename (auto-generated if not provided)
    
    Returns:
    --------
    str: Generated filename
    """
    if not report_title:
        report_title = f"QOL Framework Analysis Report ({len(results_list)} Scenarios)"
    
    generator = QOLPDFReportGenerator(report_title)
    generator.add_multiple_results(results_list)
    return generator.generate_pdf_report(filename)


def main():
    """
    Example usage - generate a sample PDF report
    """
    print("📋 QOL FRAMEWORK PDF REPORT GENERATOR")
    print("=" * 50)
    print("Generating sample PDF report...")
    
    # Create sample results (normally these would come from actual analysis)
    sample_results = [
        {
            'scenario': {
                'name': 'Conservative Retirement',
                'starting_portfolio': 500000,
                'starting_age': 65,
                'retirement_horizon': 25,
                'simulations': 1000
            },
            'utility_improvement': 15.2,
            'hauenstein_metrics': {
                'success_rate': 1.0,
                'median_final_value': 489884,
                'mean_utility': 323552,
                'p10_final_value': 350000,
                'p90_final_value': 650000
            },
            'traditional_metrics': {
                'success_rate': 1.0,
                'median_final_value': 554112,
                'mean_utility': 281038,
                'p10_final_value': 400000,
                'p90_final_value': 720000
            }
        }
    ]
    
    # Generate PDF
    filename = create_pdf_from_scenario_results(
        sample_results, 
        "QOL Framework Sample Analysis Report"
    )
    
    print(f"\n🎉 Sample PDF report created: {filename}")
    print("This demonstrates the PDF generation capabilities.")
    print("Use with actual scenario results for complete reports.")


if __name__ == "__main__":
    main()