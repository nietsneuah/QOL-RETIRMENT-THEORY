"""
Enhanced PDF Report Generator with Depletion and Sensitivity Analysis

This module extends the original PDF generator to include comprehensive depletion analysis,
sensitivity analysis results, and enhanced risk visualizations.
"""

import sys
import os
# Add parent directory to path for cross-platform module imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns
import numpy as np
import pandas as pd
from datetime import datetime
import json
from typing import Dict, List, Any, Optional
import warnings
warnings.filterwarnings('ignore')

from .depletion_analysis import PortfolioDepletionAnalysis
from .sensitivity_analysis import QOLSensitivityAnalysis

def get_output_path(filename: str, file_type: str = None) -> str:
    """
    Get the full path for output files in the appropriate output subdirectory.
    Cross-platform compatible with proper path normalization.
    
    Args:
        filename: The filename to create in the output directory
        file_type: Optional file type to determine subdirectory ('reports', 'data', 'charts')
                  If not provided, will be inferred from file extension
        
    Returns:
        Full normalized path to the file in the appropriate output subdirectory
    """
    # Get the repository root directory (parent of src directory)
    # Use abspath and normpath for cross-platform compatibility
    src_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(src_dir)
    output_base = os.path.join(repo_root, 'output')
    
    # Determine subdirectory based on file type or extension
    if file_type:
        subdir = file_type
    else:
        ext = filename.lower().split('.')[-1] if '.' in filename else ''
        if ext == 'pdf':
            subdir = 'reports'
        elif ext in ['csv', 'json']:
            subdir = 'data'
        elif ext in ['png', 'jpg', 'jpeg', 'svg']:
            subdir = 'charts'
        else:
            subdir = 'reports'  # default
    
    output_dir = os.path.join(output_base, subdir)
    
    # Create output directory if it doesn't exist (cross-platform)
    os.makedirs(output_dir, exist_ok=True)
    
    # Return normalized path for cross-platform compatibility
    return os.path.normpath(os.path.join(output_dir, filename))


class EnhancedPDFReportGenerator:
    """
    Enhanced PDF report generator with comprehensive risk analysis capabilities.
    
    Features:
    - Depletion analysis charts and tables
    - Sensitivity analysis visualizations
    - Enhanced risk metrics
    - Comprehensive scenario comparisons
    - Professional formatting and layout
    """
    
    def __init__(self, report_title: str = "Enhanced QOL Framework Analysis"):
        """
        Initialize enhanced PDF report generator.
        
        Args:
            report_title: Title for the report
        """
        self.report_title = report_title
        self.enhanced_results = []
        self.depletion_analyses = []
        self.sensitivity_results = []
        
        # Set up matplotlib for professional PDF generation
        plt.style.use('default')
        plt.rcParams['figure.figsize'] = (11, 8.5)  # Letter size
        plt.rcParams['font.size'] = 10
        plt.rcParams['axes.titlesize'] = 14
        plt.rcParams['axes.labelsize'] = 12
        plt.rcParams['legend.fontsize'] = 10
        
        # Professional color scheme
        self.colors = {
            'primary': '#2E86C1',      # Blue
            'secondary': '#28B463',    # Green
            'danger': '#E74C3C',       # Red
            'warning': '#F39C12',      # Orange
            'info': '#8E44AD',         # Purple
            'light': '#BDC3C7',       # Light gray
            'dark': '#2C3E50'          # Dark blue-gray
        }
    
    def add_enhanced_result(self, enhanced_result: Dict[str, Any], 
                           depletion_analysis: PortfolioDepletionAnalysis,
                           scenario_info: Optional[Dict[str, Any]] = None):
        """
        Add enhanced analysis results to the report.
        
        Args:
            enhanced_result: Results from EnhancedQOLAnalysis
            depletion_analysis: PortfolioDepletionAnalysis instance
            scenario_info: Optional scenario metadata
        """
        self.enhanced_results.append({
            'enhanced_result': enhanced_result,
            'scenario_info': scenario_info or {},
            'timestamp': datetime.now().isoformat()
        })
        self.depletion_analyses.append(depletion_analysis)
    
    def add_sensitivity_result(self, sensitivity_result: Dict[str, Any]):
        """Add sensitivity analysis results to the report."""
        self.sensitivity_results.append(sensitivity_result)
    
    def create_enhanced_title_page(self, pdf: PdfPages):
        """Create enhanced title page with new framework features."""
        fig, ax = plt.subplots(figsize=(11, 8.5))
        ax.axis('off')
        
        # Main title with enhanced features
        ax.text(0.5, 0.85, self.report_title, 
                fontsize=26, fontweight='bold', ha='center', 
                transform=ax.transAxes, color=self.colors['dark'])
        
        # Subtitle
        ax.text(0.5, 0.75, "Enhanced QOL Framework with Comprehensive Risk Analysis", 
                fontsize=18, ha='center', transform=ax.transAxes,
                color=self.colors['primary'])
        
        # New features highlight
        ax.text(0.5, 0.68, "🔥 NEW: Depletion Timeline Analysis • Parameter Sensitivity • Risk Optimization", 
                fontsize=14, ha='center', style='italic', 
                transform=ax.transAxes, color=self.colors['warning'])
        
        # Analysis details
        timestamp = datetime.now().strftime("%B %d, %Y at %I:%M %p")
        ax.text(0.5, 0.6, f"Analysis Generated: {timestamp}", 
                fontsize=12, ha='center', transform=ax.transAxes)
        
        if self.enhanced_results:
            ax.text(0.5, 0.55, f"Enhanced Scenarios Analyzed: {len(self.enhanced_results)}", 
                    fontsize=12, ha='center', transform=ax.transAxes)
            
        if self.sensitivity_results:
            ax.text(0.5, 0.5, f"Sensitivity Analyses: {len(self.sensitivity_results)}", 
                    fontsize=12, ha='center', transform=ax.transAxes)
        
        # Enhanced framework description
        description = """
The Enhanced QOL Framework combines age-adjusted withdrawal strategies with comprehensive
risk analysis including portfolio depletion timelines and parameter optimization.

Key Innovations:
• Portfolio Depletion Timeline Analysis with survival curves and percentile risk metrics
• Multi-parameter Sensitivity Analysis for optimization recommendations  
• Enhanced Monte Carlo simulation with detailed age-by-age tracking
• Dynamic Asset Allocation with QOL variability modeling

Result: Superior risk assessment and parameter optimization for retirement planning
        """
        
        ax.text(0.5, 0.32, description, 
                fontsize=11, ha='center', va='center', transform=ax.transAxes,
                bbox=dict(boxstyle="round,pad=0.6", facecolor=self.colors['info'], 
                         alpha=0.1, edgecolor=self.colors['info'], linewidth=2))
        
        # Feature highlights
        features = [
            "✓ Depletion Risk Analysis",
            "✓ Survival Probability Curves", 
            "✓ Parameter Sensitivity Optimization",
            "✓ Enhanced Monte Carlo Tracking"
        ]
        
        for i, feature in enumerate(features):
            ax.text(0.25 + (i % 2) * 0.5, 0.15 - (i // 2) * 0.03, feature,
                   fontsize=11, ha='center' if i % 2 == 0 else 'center',
                   transform=ax.transAxes, color=self.colors['secondary'],
                   weight='bold')
        
        # Author attribution with enhanced framework credit
        ax.text(0.5, 0.02, "Created by Doug Hauenstein\nEnhanced QOL Retirement Framework with Advanced Risk Analytics", 
                fontsize=10, ha='center', transform=ax.transAxes,
                style='italic', alpha=0.7)
        
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()
    
    def create_enhanced_executive_summary(self, pdf: PdfPages):
        """Create enhanced executive summary with depletion and risk metrics."""
        if not self.enhanced_results:
            return
        
        fig = plt.figure(figsize=(11, 8.5))
        fig.suptitle('Enhanced Executive Summary', fontsize=16, fontweight='bold', y=0.95)
        
        gs = fig.add_gridspec(3, 3, height_ratios=[1, 1, 1], hspace=0.4, wspace=0.3)
        
        # Extract enhanced metrics
        scenario_names = []
        depletion_rates = []
        survival_at_90 = []
        final_values = []
        success_rates = []
        
        for i, result_data in enumerate(self.enhanced_results):
            enhanced_result = result_data['enhanced_result']
            depletion_analysis = self.depletion_analyses[i]
            
            scenario_names.append(result_data['scenario_info'].get('name', f'Scenario {i+1}'))
            
            risk_metrics = depletion_analysis.get_risk_metrics()
            depletion_rates.append(risk_metrics['depletion_rate'] * 100)
            survival_at_90.append(risk_metrics['survival_at_90'] * 100)
            final_values.append(enhanced_result['portfolio_analysis']['final_value_mean'])
            success_rates.append(enhanced_result['success_rates']['never_depleted'] * 100)
        
        # 1. Depletion Risk Overview
        ax1 = fig.add_subplot(gs[0, 0])
        bars1 = ax1.bar(range(len(scenario_names)), depletion_rates,
                       color=self.colors['danger'], alpha=0.7)
        ax1.set_title('Portfolio Depletion Risk', fontweight='bold')
        ax1.set_ylabel('Depletion Risk (%)')
        ax1.set_xticks(range(len(scenario_names)))
        ax1.set_xticklabels(scenario_names, rotation=45, ha='right')
        ax1.grid(True, alpha=0.3, axis='y')
        
        # Add risk level annotations
        for bar, value in zip(bars1, depletion_rates):
            color = 'red' if value > 15 else 'orange' if value > 5 else 'green'
            ax1.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.5,
                    f'{value:.1f}%', ha='center', va='bottom', 
                    fontweight='bold', color=color)
        
        # 2. Survival at Age 90
        ax2 = fig.add_subplot(gs[0, 1])
        bars2 = ax2.bar(range(len(scenario_names)), survival_at_90,
                       color=self.colors['secondary'], alpha=0.7)
        ax2.set_title('Survival Probability at Age 90', fontweight='bold')
        ax2.set_ylabel('Survival Rate (%)')
        ax2.set_xticks(range(len(scenario_names)))
        ax2.set_xticklabels(scenario_names, rotation=45, ha='right')
        ax2.grid(True, alpha=0.3, axis='y')
        ax2.set_ylim(0, 105)
        
        # Add value labels
        for bar, value in zip(bars2, survival_at_90):
            ax2.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 1,
                    f'{value:.1f}%', ha='center', va='bottom', fontweight='bold')
        
        # 3. Final Portfolio Values
        ax3 = fig.add_subplot(gs[0, 2])
        bars3 = ax3.bar(range(len(scenario_names)), [v/1000 for v in final_values],
                       color=self.colors['primary'], alpha=0.7)
        ax3.set_title('Final Portfolio Values', fontweight='bold')
        ax3.set_ylabel('Value ($000s)')
        ax3.set_xticks(range(len(scenario_names)))
        ax3.set_xticklabels(scenario_names, rotation=45, ha='right')
        ax3.grid(True, alpha=0.3, axis='y')
        
        # Add value labels
        for bar, value in zip(bars3, final_values):
            ax3.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 20,
                    f'${value/1000:.0f}K', ha='center', va='bottom', fontweight='bold')
        
        # 4. Risk Assessment Matrix
        ax4 = fig.add_subplot(gs[1, :])
        
        # Create risk matrix visualization
        risk_data = []
        for i in range(len(scenario_names)):
            risk_score = depletion_rates[i] * 0.4 + (100 - survival_at_90[i]) * 0.6
            risk_data.append(risk_score)
        
        # Create risk level categories
        risk_levels = []
        risk_colors = []
        for risk_score in risk_data:
            if risk_score < 5:
                risk_levels.append('LOW')
                risk_colors.append('green')
            elif risk_score < 15:
                risk_levels.append('MODERATE')
                risk_colors.append('orange')
            else:
                risk_levels.append('HIGH')
                risk_colors.append('red')
        
        bars4 = ax4.bar(range(len(scenario_names)), risk_data, color=risk_colors, alpha=0.7)
        ax4.set_title('Comprehensive Risk Assessment Score', fontweight='bold')
        ax4.set_ylabel('Risk Score')
        ax4.set_xlabel('Scenarios')
        ax4.set_xticks(range(len(scenario_names)))
        ax4.set_xticklabels(scenario_names)
        ax4.grid(True, alpha=0.3, axis='y')
        
        # Add risk level labels
        for bar, level, score in zip(bars4, risk_levels, risk_data):
            ax4.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.5,
                    f'{level}\n({score:.1f})', ha='center', va='bottom', fontweight='bold')
        
        # 5. Summary Statistics Table
        ax5 = fig.add_subplot(gs[2, :])
        ax5.axis('off')
        
        # Create comprehensive summary table
        avg_depletion = np.mean(depletion_rates)
        avg_survival_90 = np.mean(survival_at_90)
        avg_final_value = np.mean(final_values)
        min_depletion = min(depletion_rates)
        max_depletion = max(depletion_rates)
        
        summary_data = [
            ['Enhanced Framework Metrics', 'Value', 'Assessment'],
            ['Average Depletion Risk', f'{avg_depletion:.1f}%', 
             'Low' if avg_depletion < 5 else 'Moderate' if avg_depletion < 15 else 'High'],
            ['Average Survival at 90', f'{avg_survival_90:.1f}%',
             'Excellent' if avg_survival_90 > 90 else 'Good' if avg_survival_90 > 80 else 'Poor'],
            ['Average Final Portfolio', f'${avg_final_value:,.0f}',
             'Strong' if avg_final_value > 500000 else 'Adequate'],
            ['Depletion Risk Range', f'{min_depletion:.1f}% - {max_depletion:.1f}%',
             'Consistent' if max_depletion - min_depletion < 10 else 'Variable'],
            ['Total Scenarios Analyzed', f'{len(self.enhanced_results)}',
             'Comprehensive' if len(self.enhanced_results) > 3 else 'Limited'],
            ['Enhanced Features', 'Depletion + Sensitivity Analysis', 'Advanced Risk Assessment']
        ]
        
        # Create and style table
        table = ax5.table(cellText=summary_data[1:],
                         colLabels=summary_data[0],
                         cellLoc='center',
                         loc='center',
                         bbox=[0, 0, 1, 1])
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 1.8)
        
        # Color-code table
        for i in range(len(summary_data)):
            for j in range(3):
                cell = table[(i, j)]
                if i == 0:  # Header
                    cell.set_facecolor(self.colors['dark'])
                    cell.set_text_props(weight='bold', color='white')
                else:
                    # Color-code assessment column based on values
                    if j == 2:  # Assessment column
                        assessment = summary_data[i][j]
                        if assessment in ['Low', 'Excellent', 'Strong', 'Consistent', 'Comprehensive']:
                            cell.set_facecolor('#d4edda')  # Light green
                        elif assessment in ['Moderate', 'Good', 'Adequate', 'Variable']:
                            cell.set_facecolor('#fff3cd')  # Light yellow
                        elif assessment in ['High', 'Poor']:
                            cell.set_facecolor('#f8d7da')  # Light red
                        else:
                            cell.set_facecolor('#e2e3e5')  # Light gray
                    else:
                        cell.set_facecolor('#f8f9fa' if i % 2 == 0 else 'white')
        
        plt.tight_layout()
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()
    
    def create_depletion_analysis_pages(self, pdf: PdfPages):
        """Create dedicated pages for depletion analysis results."""
        if not self.depletion_analyses:
            return
        
        for i, depletion_analysis in enumerate(self.depletion_analyses):
            scenario_info = self.enhanced_results[i]['scenario_info']
            scenario_name = scenario_info.get('name', f'Scenario {i+1}')
            
            # Create depletion analysis page
            fig = plt.figure(figsize=(11, 8.5))
            fig.suptitle(f'Depletion Risk Analysis: {scenario_name}', 
                        fontsize=16, fontweight='bold', y=0.95)
            
            gs = fig.add_gridspec(3, 2, height_ratios=[1, 1, 1], hspace=0.4, wspace=0.3)
            
            # 1. Survival Curve
            ax1 = fig.add_subplot(gs[0, :])
            survival_data = depletion_analysis.survival_data
            ages = survival_data['ages']
            survival_probs = survival_data['survival_probabilities']
            
            ax1.plot(ages, survival_probs, linewidth=3, color=self.colors['primary'], 
                    label='Portfolio Survival Probability')
            
            # Add milestone markers
            milestones = [80, 90, 100]
            colors = [self.colors['secondary'], self.colors['warning'], self.colors['danger']]
            
            for milestone, color in zip(milestones, colors):
                if milestone <= ages[-1]:
                    survival_at_milestone = depletion_analysis.get_survival_at_age([milestone])[milestone]
                    ax1.axhline(y=survival_at_milestone, color=color, linestyle='--', alpha=0.7,
                              linewidth=2, label=f'Age {milestone}: {survival_at_milestone:.1%}')
                    ax1.axvline(x=milestone, color=color, linestyle='--', alpha=0.7, linewidth=2)
            
            ax1.set_xlabel('Age')
            ax1.set_ylabel('Survival Probability')
            ax1.set_title('Portfolio Survival Curve Over Time', fontweight='bold')
            ax1.legend()
            ax1.grid(True, alpha=0.3)
            ax1.set_ylim(0, 1)
            
            # Format y-axis as percentages
            ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: '{:.0%}'.format(y)))
            
            # 2. Depletion Histogram
            ax2 = fig.add_subplot(gs[1, 0])
            depletion_ages = depletion_analysis.depletion_data['depletion_ages']
            finite_ages = depletion_ages[np.isfinite(depletion_ages)]
            
            if len(finite_ages) > 0:
                ax2.hist(finite_ages, bins=15, alpha=0.7, color=self.colors['danger'], 
                        edgecolor='black')
                mean_age = np.mean(finite_ages)
                median_age = np.median(finite_ages)
                
                ax2.axvline(mean_age, color='blue', linestyle='--', linewidth=2, 
                           label=f'Mean: {mean_age:.1f}')
                ax2.axvline(median_age, color='green', linestyle='--', linewidth=2, 
                           label=f'Median: {median_age:.1f}')
                ax2.set_title('Depletion Age Distribution')
                ax2.legend()
            else:
                ax2.text(0.5, 0.5, 'No Portfolio\nDepletions Occurred', ha='center', va='center',
                        transform=ax2.transAxes, fontsize=14, weight='bold',
                        bbox=dict(boxstyle="round,pad=0.3", facecolor=self.colors['secondary'], alpha=0.3))
                ax2.set_title('Depletion Analysis')
            
            ax2.set_xlabel('Age at Depletion')
            ax2.set_ylabel('Number of Simulations')
            ax2.grid(True, alpha=0.3)
            
            # 3. Risk Metrics Table
            ax3 = fig.add_subplot(gs[1, 1])
            ax3.axis('off')
            
            risk_metrics = depletion_analysis.get_risk_metrics()
            percentiles = depletion_analysis.get_depletion_percentiles()
            
            # Create risk metrics display
            metrics_text = f"""Key Risk Metrics:

Depletion Risk: {risk_metrics['depletion_rate']:.1%}
Survival Rate: {risk_metrics['survival_rate']:.1%}

Longevity Analysis:
• Age 80 Survival: {risk_metrics['survival_at_80']:.1%}
• Age 90 Survival: {risk_metrics['survival_at_90']:.1%}
• Age 100 Survival: {risk_metrics['survival_at_100']:.1%}

Depletion Timeline:
• Earliest: Age {risk_metrics['earliest_depletion_age']:.0f}
• Median: Age {risk_metrics['median_depletion_age']:.1f}
• 5% Worst Case: Age {risk_metrics['var_95_age']:.0f}"""
            
            if np.isfinite(risk_metrics['earliest_depletion_age']):
                color = self.colors['danger'] if risk_metrics['depletion_rate'] > 0.15 else self.colors['warning'] if risk_metrics['depletion_rate'] > 0.05 else self.colors['secondary']
            else:
                metrics_text = "Risk Assessment:\n\nNo Depletion Risk Detected\n\nPortfolio survives in 100%\nof simulation scenarios\n\nExcellent sustainability\nfor chosen parameters"
                color = self.colors['secondary']
            
            ax3.text(0.05, 0.95, metrics_text, transform=ax3.transAxes,
                    fontsize=11, va='top', ha='left', weight='bold',
                    bbox=dict(boxstyle="round,pad=0.5", facecolor=color, alpha=0.2))
            
            # 4. Percentile Analysis
            ax4 = fig.add_subplot(gs[2, :])
            
            if len(finite_ages) > 0:
                percentile_ages = percentiles['depletion_ages']
                percentile_labels = [f'{p}th' for p in percentiles['percentiles']]
                
                bars = ax4.bar(range(len(percentile_labels)), percentile_ages, 
                              color=self.colors['warning'], alpha=0.7)
                ax4.set_title('Depletion Age Percentiles (For Simulations That Deplete)', fontweight='bold')
                ax4.set_ylabel('Age at Depletion')
                ax4.set_xlabel('Percentile')
                ax4.set_xticks(range(len(percentile_labels)))
                ax4.set_xticklabels(percentile_labels)
                ax4.grid(True, alpha=0.3, axis='y')
                
                # Add value labels
                for bar, age in zip(bars, percentile_ages):
                    ax4.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.5,
                            f'{age:.1f}', ha='center', va='bottom', fontweight='bold')
            else:
                ax4.text(0.5, 0.5, 'Portfolio Never Depletes\nNo Percentile Analysis Available', 
                        ha='center', va='center', transform=ax4.transAxes, fontsize=14,
                        bbox=dict(boxstyle="round,pad=0.5", facecolor=self.colors['secondary'], alpha=0.3))
                ax4.set_title('Depletion Percentile Analysis')
            
            pdf.savefig(fig, bbox_inches='tight')
            plt.close()
    
    def create_sensitivity_analysis_pages(self, pdf: PdfPages):
        """Create pages for sensitivity analysis results."""
        if not self.sensitivity_results:
            return
        
        for i, sens_result in enumerate(self.sensitivity_results):
            # Create sensitivity analysis page
            fig = plt.figure(figsize=(11, 8.5))
            fig.suptitle(f'Sensitivity Analysis Results {i+1}', 
                        fontsize=16, fontweight='bold', y=0.95)
            
            # Determine sensitivity result type and create appropriate visualization
            if 'param1_name' in sens_result:  # Two-parameter analysis
                self._create_two_param_sensitivity_page(fig, sens_result)
            elif 'parameter_names' in sens_result:  # Comprehensive analysis
                self._create_comprehensive_sensitivity_page(fig, sens_result)
            else:  # Single parameter analysis
                self._create_single_param_sensitivity_page(fig, sens_result)
            
            pdf.savefig(fig, bbox_inches='tight')
            plt.close()
    
    def _create_single_param_sensitivity_page(self, fig: plt.Figure, sens_result: Dict):
        """Create single parameter sensitivity visualization."""
        gs = fig.add_gridspec(2, 2, hspace=0.4, wspace=0.3)
        
        param_name = sens_result['parameter_name']
        param_values = sens_result['parameter_values']
        
        # Plot sensitivity curves
        axes = [fig.add_subplot(gs[0, 0]), fig.add_subplot(gs[0, 1]),
                fig.add_subplot(gs[1, 0]), fig.add_subplot(gs[1, 1])]
        
        metrics = [
            ('metric_values', sens_result['metric'].title(), self.colors['primary']),
            ('depletion_rates', 'Depletion Rate (%)', self.colors['danger']),
            ('final_values', 'Final Value ($)', self.colors['secondary']),
            ('survival_rates', 'Survival Rate (%)', self.colors['info'])
        ]
        
        for ax, (metric_key, title, color) in zip(axes, metrics):
            values = sens_result[metric_key]
            if metric_key in ['depletion_rates', 'survival_rates']:
                values = [v * 100 if v <= 1 else v for v in values]  # Convert to percentages
                
            ax.plot(param_values, values, 'o-', linewidth=2, markersize=6, color=color)
            ax.set_title(f'{title} Sensitivity', fontweight='bold')
            ax.set_xlabel(param_name)
            ax.set_ylabel(title)
            ax.grid(True, alpha=0.3)
            
            # Highlight optimal point
            if metric_key == 'depletion_rates':
                optimal_idx = np.argmin(values)
            else:
                optimal_idx = np.argmax(values)
            ax.scatter(param_values[optimal_idx], values[optimal_idx], 
                      color='red', s=100, zorder=5, marker='*')
    
    def _create_two_param_sensitivity_page(self, fig: plt.Figure, sens_result: Dict):
        """Create two-parameter sensitivity heatmap."""
        gs = fig.add_gridspec(2, 2, hspace=0.4, wspace=0.3)
        
        param1_name = sens_result['param1_name']
        param2_name = sens_result['param2_name']
        param1_values = sens_result['param1_values']
        param2_values = sens_result['param2_values']
        
        # Create heatmaps
        matrices = [
            (sens_result['depletion_matrix'], 'Depletion Rate', 'RdYlBu_r'),
            (sens_result['final_value_matrix'] / 1000, 'Final Value ($000s)', 'YlOrRd'),
            (sens_result['metric_matrix'], sens_result['metric'].title(), 'viridis'),
        ]
        
        axes = [fig.add_subplot(gs[0, 0]), fig.add_subplot(gs[0, 1]), fig.add_subplot(gs[1, :])]
        
        for ax, (matrix, title, cmap) in zip(axes[:3], matrices):
            im = ax.imshow(matrix, cmap=cmap, aspect='auto')
            ax.set_title(title, fontweight='bold')
            ax.set_xlabel(param1_name)
            ax.set_ylabel(param2_name)
            
            # Set tick labels
            ax.set_xticks(range(len(param1_values)))
            ax.set_xticklabels([f'{v:.2f}' for v in param1_values])
            ax.set_yticks(range(len(param2_values)))
            ax.set_yticklabels([f'{v:.2f}' for v in param2_values])
            
            # Add colorbar
            plt.colorbar(im, ax=ax, shrink=0.8)
        
        # Add optimal combination summary
        if len(axes) > 2:
            ax = axes[2]
            ax.axis('off')
            
            optimal = sens_result['optimal_combination']
            summary_text = f"""Optimal Parameter Combination:

{param1_name}: {optimal[param1_name]}
{param2_name}: {optimal[param2_name]}

Optimal {sens_result['metric']}: {optimal['metric_value']:.3f}

This combination provides the best performance
for the selected optimization metric."""
            
            ax.text(0.5, 0.5, summary_text, transform=ax.transAxes, ha='center', va='center',
                   fontsize=14, weight='bold',
                   bbox=dict(boxstyle="round,pad=0.5", facecolor=self.colors['secondary'], alpha=0.2))
    
    def _create_comprehensive_sensitivity_page(self, fig: plt.Figure, sens_result: Dict):
        """Create comprehensive sensitivity analysis visualization."""
        gs = fig.add_gridspec(3, 2, hspace=0.5, wspace=0.3)
        
        # Summary statistics
        ax1 = fig.add_subplot(gs[0, :])
        ax1.axis('off')
        
        param_names = sens_result['parameter_names']
        n_combinations = len(sens_result['combinations'])
        
        # Display optimal combinations
        optimal_depletion = sens_result['optimal_for_depletion']
        optimal_final = sens_result['optimal_for_final_value']
        
        summary_text = f"""Comprehensive Sensitivity Analysis Summary

Parameters Analyzed: {', '.join(param_names)}
Total Combinations Tested: {n_combinations:,}

OPTIMAL FOR MINIMUM DEPLETION RISK:
{self._format_parameter_dict(optimal_depletion['parameters'])}
Result: {optimal_depletion['metric_value']:.1%} depletion risk

OPTIMAL FOR MAXIMUM FINAL VALUE:
{self._format_parameter_dict(optimal_final['parameters'])}
Result: ${optimal_final['metric_value']:,.0f} final value"""
        
        ax1.text(0.05, 0.95, summary_text, transform=ax1.transAxes, va='top', ha='left',
                fontsize=11, weight='bold',
                bbox=dict(boxstyle="round,pad=0.5", facecolor=self.colors['info'], alpha=0.2))
        
        # Distribution plots
        depletion_rates = [r * 100 for r in sens_result['depletion_rates']]
        final_values = [v / 1000 for v in sens_result['final_values']]
        
        ax2 = fig.add_subplot(gs[1, 0])
        ax2.hist(depletion_rates, bins=20, alpha=0.7, color=self.colors['danger'])
        ax2.set_title('Depletion Rate Distribution', fontweight='bold')
        ax2.set_xlabel('Depletion Rate (%)')
        ax2.set_ylabel('Frequency')
        ax2.grid(True, alpha=0.3)
        
        ax3 = fig.add_subplot(gs[1, 1])
        ax3.hist(final_values, bins=20, alpha=0.7, color=self.colors['secondary'])
        ax3.set_title('Final Value Distribution', fontweight='bold')
        ax3.set_xlabel('Final Value ($000s)')
        ax3.set_ylabel('Frequency')
        ax3.grid(True, alpha=0.3)
        
        # Scatter plot showing relationship
        ax4 = fig.add_subplot(gs[2, :])
        scatter = ax4.scatter(depletion_rates, final_values, alpha=0.6, s=30, 
                             c=range(len(depletion_rates)), cmap='viridis')
        ax4.set_xlabel('Depletion Rate (%)')
        ax4.set_ylabel('Final Portfolio Value ($000s)')
        ax4.set_title('Risk vs Return Relationship Across Parameter Combinations', fontweight='bold')
        ax4.grid(True, alpha=0.3)
        
        # Add optimal points
        opt_depl_idx = optimal_depletion['index']
        opt_final_idx = optimal_final['index']
        
        ax4.scatter(depletion_rates[opt_depl_idx], final_values[opt_depl_idx],
                   color='red', s=100, marker='*', label='Min Depletion Risk')
        ax4.scatter(depletion_rates[opt_final_idx], final_values[opt_final_idx],
                   color='gold', s=100, marker='*', label='Max Final Value')
        ax4.legend()
    
    def _format_parameter_dict(self, params: Dict) -> str:
        """Format parameter dictionary for display."""
        lines = []
        for key, value in params.items():
            lines.append(f"• {key}: {value}")
        return '\n'.join(lines)
    
    def generate_enhanced_pdf_report(self, filename: Optional[str] = None) -> str:
        """
        Generate the complete enhanced PDF report.
        
        Args:
            filename: Optional output filename
            
        Returns:
            Generated filename
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"enhanced_qol_framework_report_{timestamp}.pdf"
        
        # Ensure file is saved to output directory
        full_path = get_output_path(filename)
        
        print(f"🔄 Generating enhanced PDF report: {full_path}")
        
        with PdfPages(full_path) as pdf:
            # Enhanced title page
            print("   📄 Creating enhanced title page...")
            self.create_enhanced_title_page(pdf)
            
            # Enhanced executive summary
            if self.enhanced_results:
                print("   📊 Creating enhanced executive summary...")
                self.create_enhanced_executive_summary(pdf)
                
                # Depletion analysis pages
                print(f"   📋 Creating {len(self.depletion_analyses)} depletion analysis pages...")
                self.create_depletion_analysis_pages(pdf)
            
            # Sensitivity analysis pages
            if self.sensitivity_results:
                print(f"   🎯 Creating {len(self.sensitivity_results)} sensitivity analysis pages...")
                self.create_sensitivity_analysis_pages(pdf)
            
            # Add methodology page (from base class concept)
            print("   📚 Creating enhanced methodology page...")
            self._create_enhanced_methodology_page(pdf)
        
        print(f"✅ Enhanced PDF report generated successfully: {full_path}")
        return full_path
    
    def _create_enhanced_methodology_page(self, pdf: PdfPages):
        """Create enhanced methodology page explaining new features."""
        fig = plt.figure(figsize=(11, 8.5))
        fig.suptitle('Enhanced QOL Framework Methodology', fontsize=16, fontweight='bold', y=0.95)
        
        gs = fig.add_gridspec(3, 2, hspace=0.5, wspace=0.3)
        
        # Enhanced framework overview
        ax1 = fig.add_subplot(gs[0, :])
        ax1.axis('off')
        
        methodology_text = """Enhanced QOL Framework Methodology & New Features

The Enhanced QOL Framework extends the original age-adjusted withdrawal strategy with comprehensive
risk analysis and parameter optimization capabilities:

🔥 NEW FEATURES:
• Portfolio Depletion Timeline Analysis: Track exact age and year of portfolio exhaustion across percentiles
• Survival Probability Curves: Calculate probability of portfolio lasting to any specific age
• Parameter Sensitivity Analysis: Optimize withdrawal rates, starting values, and horizon lengths
• Enhanced Monte Carlo: Detailed age-by-age tracking with QOL variability and dynamic allocation
• Risk Assessment Matrix: Comprehensive scoring combining depletion risk with longevity analysis"""
        
        ax1.text(0.05, 0.95, methodology_text, transform=ax1.transAxes, va='top', ha='left',
                fontsize=11, weight='bold',
                bbox=dict(boxstyle="round,pad=0.5", facecolor=self.colors['primary'], alpha=0.1))
        
        # Depletion analysis explanation
        ax2 = fig.add_subplot(gs[1, 0])
        ax2.axis('off')
        
        depletion_text = """DEPLETION ANALYSIS:

Key Metrics:
• Depletion Rate: % of simulations where 
  portfolio reaches zero
• Survival Curves: Probability of portfolio 
  lasting to each age
• Risk Percentiles: 5th, 25th, 50th, 75th, 
  90th percentile depletion ages
• Longevity Markers: Specific survival 
  probabilities at ages 80, 90, 100

Uses:
• Assess true portfolio longevity risk
• Plan for different life expectancies  
• Compare scenarios objectively
• Set appropriate withdrawal rates"""
        
        ax2.text(0.05, 0.95, depletion_text, transform=ax2.transAxes, va='top', ha='left',
                fontsize=10,
                bbox=dict(boxstyle="round,pad=0.4", facecolor=self.colors['danger'], alpha=0.1))
        
        # Sensitivity analysis explanation
        ax3 = fig.add_subplot(gs[1, 1])
        ax3.axis('off')
        
        sensitivity_text = """SENSITIVITY ANALYSIS:

Parameter Optimization:
• Single Parameter: Test one variable 
  across range of values
• Two Parameter: Create heatmaps showing 
  interaction effects  
• Comprehensive: Test all parameter 
  combinations for global optimization

Key Parameters:
• Starting Portfolio Value
• Withdrawal Strategy Rates
• Return Volatility Assumptions
• QOL Variability Settings
• Analysis Horizon Length

Output:
• Optimal parameter combinations
• Risk sensitivity rankings
• Performance trade-offs"""
        
        ax3.text(0.05, 0.95, sensitivity_text, transform=ax3.transAxes, va='top', ha='left',
                fontsize=10,
                bbox=dict(boxstyle="round,pad=0.4", facecolor=self.colors['warning'], alpha=0.1))
        
        # Technical specifications
        ax4 = fig.add_subplot(gs[2, :])
        ax4.axis('off')
        
        technical_text = """TECHNICAL ENHANCEMENTS:

Enhanced Monte Carlo Simulation:
• Age-by-age portfolio tracking with detailed path storage
• Dynamic asset allocation glide path based on age
• QOL variability modeling with configurable standard deviations  
• Inflation and return volatility with correlation modeling
• Support for multiple withdrawal strategies (Hauenstein, Fixed 4%, Dynamic)

Advanced Analytics:
• Statistical risk metrics: VaR (Value at Risk), survival analysis, percentile distributions
• Comprehensive reporting: PDF generation with charts, tables, and executive summaries
• Parameter optimization: Grid search, gradient-based optimization, and recommendation engine
• Extensible framework: Modular design supporting additional strategies and risk measures

Validation & Quality Assurance:
• Monte Carlo convergence testing • Statistical significance validation • Stress testing under extreme scenarios"""
        
        ax4.text(0.05, 0.95, technical_text, transform=ax4.transAxes, va='top', ha='left',
                fontsize=10,
                bbox=dict(boxstyle="round,pad=0.4", facecolor=self.colors['secondary'], alpha=0.1))
        
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()


# Convenience functions for easy report generation

def create_enhanced_pdf_from_results(enhanced_results: List[Dict],
                                   depletion_analyses: List[PortfolioDepletionAnalysis],
                                   sensitivity_results: Optional[List[Dict]] = None,
                                   scenario_infos: Optional[List[Dict]] = None,
                                   report_title: Optional[str] = None,
                                   filename: Optional[str] = None) -> str:
    """
    Convenience function to create enhanced PDF report from analysis results.
    
    Args:
        enhanced_results: List of enhanced QOL analysis results
        depletion_analyses: List of depletion analysis instances
        sensitivity_results: Optional list of sensitivity analysis results
        scenario_infos: Optional list of scenario metadata
        report_title: Optional report title
        filename: Optional output filename
        
    Returns:
        Generated filename
    """
    if not report_title:
        report_title = f"Enhanced QOL Framework Analysis ({len(enhanced_results)} Scenarios)"
    
    generator = EnhancedPDFReportGenerator(report_title)
    
    # Add enhanced results
    for i, enhanced_result in enumerate(enhanced_results):
        scenario_info = scenario_infos[i] if scenario_infos and i < len(scenario_infos) else {}
        generator.add_enhanced_result(enhanced_result, depletion_analyses[i], scenario_info)
    
    # Add sensitivity results
    if sensitivity_results:
        for sens_result in sensitivity_results:
            generator.add_sensitivity_result(sens_result)
    
    return generator.generate_enhanced_pdf_report(filename)


def main():
    """Example usage of enhanced PDF generator."""
    print("📋 ENHANCED QOL FRAMEWORK PDF REPORT GENERATOR")
    print("=" * 60)
    print("This module provides comprehensive PDF reporting with:")
    print("• Depletion timeline analysis")
    print("• Sensitivity analysis visualizations") 
    print("• Enhanced risk assessment")
    print("• Professional formatting")
    print("\nUse create_enhanced_pdf_from_results() to generate reports from your analysis results.")


if __name__ == "__main__":
    main()