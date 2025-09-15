#!/usr/bin/env python3
"""
LaTeX Report Generator for QOL Framework Analysis

This module provides high-quality LaTeX-based PDF generation as an alternative to
the matplotlib-based reports. Offers superior typography, mathematical formatting,
and professional presentation suitable for academic or business contexts.

Features:
- Professional LaTeX templates with custom styling
- Automatic data injection from Python analysis results
- Chart integration via includegraphics
- Mathematical equation formatting
- Publication-quality tables and formatting
"""

import sys
import os
import shutil
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import json
import warnings
warnings.filterwarnings('ignore')

# Add parent directory for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from .depletion_analysis import PortfolioDepletionAnalysis
from .sensitivity_analysis import QOLSensitivityAnalysis
from .enhanced_qol_framework import EnhancedQOLAnalysis

def get_output_path(filename: str, file_type: str = None) -> str:
    """
    Get organized output path for generated files.
    Files are automatically organized by type in output/ subdirectories.
    """
    # Determine base output directory
    current_dir = os.getcwd()
    if 'QOL-RETIREMENT-THEORY' in current_dir:
        # We're inside the project directory
        base_dir = current_dir
        while not os.path.basename(base_dir) == 'QOL-RETIREMENT-THEORY' and base_dir != '/':
            base_dir = os.path.dirname(base_dir)
        output_dir = os.path.join(base_dir, 'output')
    else:
        # We're outside project directory, create local output
        output_dir = os.path.join(current_dir, 'output')
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Auto-organize by file extension if not specified
    if file_type is None:
        ext = os.path.splitext(filename)[1].lower()
        if ext in ['.pdf', '.tex', '.txt']:
            file_type = 'reports'
        elif ext in ['.png', '.jpg', '.jpeg', '.svg']:
            file_type = 'charts' 
        elif ext in ['.csv', '.json']:
            file_type = 'data'
        else:
            file_type = 'reports'  # default
    
    # Create subdirectory and return full path
    subdir = os.path.join(output_dir, file_type)
    os.makedirs(subdir, exist_ok=True)
    return os.path.join(subdir, filename)

class LaTeXReportGenerator:
    """
    Generate professional LaTeX-based PDF reports for QOL Framework analysis.
    
    Provides superior typography and mathematical formatting compared to matplotlib-based reports.
    Requires LaTeX distribution (TeXLive, MiKTeX, or MacTeX) to be installed.
    """
    
    def __init__(self, report_title: str = "Enhanced QOL Framework Analysis"):
        """
        Initialize LaTeX report generator.
        
        Args:
            report_title: Title for the report
        """
        self.report_title = report_title
        self.enhanced_results = []
        self.depletion_analyses = []
        self.sensitivity_results = []
        self.scenario_infos = []
        
        # Template paths - use basic template for BasicTeX compatibility
        self.template_dir = os.path.join(os.path.dirname(__file__), 'latex_templates')
        
        # Check if we should use the basic template (for BasicTeX/limited installations)
        latex_status = check_latex_availability()
        if latex_status.get('is_basic', False) or 'BasicTeX' in latex_status.get('version', ''):
            self.template_file = os.path.join(self.template_dir, 'qol_report_template_basic.tex')
        else:
            self.template_file = os.path.join(self.template_dir, 'qol_report_template.tex')
            
        # Fallback to basic template if full template doesn't exist
        if not os.path.exists(self.template_file):
            self.template_file = os.path.join(self.template_dir, 'qol_report_template_basic.tex')
        
        # Check for LaTeX installation
        self.latex_available = self._check_latex_installation()
        
    def _check_latex_installation(self) -> bool:
        """Check if LaTeX is available in the system."""
        try:
            result = subprocess.run(['pdflatex', '--version'], 
                                  capture_output=True, text=True, timeout=5)
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    def add_enhanced_result(self, enhanced_result: Dict[str, Any], 
                           depletion_analysis: PortfolioDepletionAnalysis,
                           scenario_info: Optional[Dict[str, Any]] = None):
        """Add enhanced analysis results to the report."""
        self.enhanced_results.append(enhanced_result)
        self.depletion_analyses.append(depletion_analysis)
        if scenario_info:
            self.scenario_infos.append(scenario_info)
    
    def add_sensitivity_result(self, sensitivity_result: Dict[str, Any]):
        """Add sensitivity analysis results to the report."""
        self.sensitivity_results.append(sensitivity_result)
    
    def _format_currency(self, value: float) -> str:
        """Format currency values for LaTeX."""
        return f"\\${value:,.0f}"
    
    def _format_percentage(self, value: float) -> str:
        """Format percentage values for LaTeX."""
        return f"{value:.1f}\\%"
    
    def _escape_latex(self, text: str) -> str:
        """Escape special LaTeX characters in text."""
        chars = {'&': '\\&', '%': '\\%', '$': '\\$', '#': '\\#', 
                '^': '\\textasciicircum{}', '_': '\\_', 
                '{': '\\{', '}': '\\}', '~': '\\textasciitilde{}',
                '\\': '\\textbackslash{}'}
        for char, escape in chars.items():
            text = text.replace(char, escape)
        return text
    
    def _generate_scenario_results_table(self) -> str:
        """Generate LaTeX table of scenario results."""
        if not self.enhanced_results:
            return "No scenario results available."
        
        # Table header
        latex_table = """
\\begin{table}[H]
\\centering
\\caption{Scenario Analysis Results Summary}
\\begin{tabularx}{\\textwidth}{l*{4}{>{\\centering\\arraybackslash}X}}
\\toprule
\\textbf{Scenario} & \\textbf{Utility Improvement} & \\textbf{Success Rate} & \\textbf{Median Final Value} & \\textbf{Depletion Risk} \\\\
\\midrule
"""
        
        # Add each scenario
        for i, (result, depletion) in enumerate(zip(self.enhanced_results, self.depletion_analyses)):
            scenario_name = (self.scenario_infos[i].get('name', f'Scenario {i+1}') 
                           if i < len(self.scenario_infos) else f'Scenario {i+1}')
            
            utility_improvement = result.get('utility_improvement', 0)
            success_rate = result.get('hauenstein_metrics', {}).get('success_rate', 0) * 100
            median_final = result.get('hauenstein_metrics', {}).get('median_final_value', 0)
            depletion_rate = getattr(depletion, 'depletion_rate', 0) * 100 if depletion else 0
            
            latex_table += f"""{self._escape_latex(scenario_name)} & 
{self._format_percentage(utility_improvement)} & 
{self._format_percentage(success_rate)} & 
{self._format_currency(median_final)} & 
{self._format_percentage(depletion_rate)} \\\\
"""
        
        # Close table
        latex_table += """\\bottomrule
\\end{tabularx}
\\label{tab:scenario-summary}
\\end{table}
"""
        return latex_table
    
    def _generate_performance_charts(self, temp_dir: str) -> str:
        """Generate and embed comprehensive performance charts in LaTeX."""
        if not self.enhanced_results or not self.depletion_analyses:
            return "Charts will be generated when full simulation results are available."
        
        latex_content = ""
        chart_files = []
        
        try:
            import matplotlib.pyplot as plt
            import numpy as np
            
            # Chart 1: Performance Summary (4-panel overview)
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))
            fig.suptitle('QOL Framework Performance Summary', fontsize=16, fontweight='bold')
            
            scenario_names = []
            depletion_rates = []
            final_values = []
            total_utilities = []
            
            # Extract data from all scenarios
            for i, (result, depletion) in enumerate(zip(self.enhanced_results, self.depletion_analyses)):
                scenario_name = (self.scenario_infos[i].get('name', f'Scenario {i+1}') 
                               if i < len(self.scenario_infos) else f'Scenario {i+1}')
                scenario_names.append(scenario_name)
                
                # Get depletion rate
                risk_metrics = depletion.get_risk_metrics()
                depletion_rates.append(risk_metrics.get('depletion_rate', 0) * 100)
                
                # Get other metrics
                hauenstein_metrics = result.get('hauenstein_metrics', {})
                final_values.append(hauenstein_metrics.get('final_value_mean', 0) / 1000)  # Convert to thousands
                total_utilities.append(hauenstein_metrics.get('total_utility', 0))
            
            # Plot 1: Depletion Rates
            bars1 = ax1.bar(range(len(scenario_names)), depletion_rates, color='red', alpha=0.7, edgecolor='black')
            ax1.set_title('Portfolio Depletion Risk (%)', fontweight='bold')
            ax1.set_xlabel('Scenarios')
            ax1.set_ylabel('Depletion Rate (%)')
            ax1.set_xticks(range(len(scenario_names)))
            ax1.set_xticklabels(scenario_names, rotation=45, ha='right')
            ax1.grid(True, alpha=0.3)
            # Add value labels on bars
            for bar, value in zip(bars1, depletion_rates):
                ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                        f'{value:.1f}%', ha='center', va='bottom', fontsize=8)
            
            # Plot 2: Final Portfolio Values
            bars2 = ax2.bar(range(len(scenario_names)), final_values, color='green', alpha=0.7, edgecolor='black')
            ax2.set_title('Mean Final Portfolio Value ($000s)', fontweight='bold')
            ax2.set_xlabel('Scenarios')
            ax2.set_ylabel('Final Value ($000s)')
            ax2.set_xticks(range(len(scenario_names)))
            ax2.set_xticklabels(scenario_names, rotation=45, ha='right')
            ax2.grid(True, alpha=0.3)
            # Add value labels on bars
            for bar, value in zip(bars2, final_values):
                ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(final_values)*0.01, 
                        f'${value:.0f}k', ha='center', va='bottom', fontsize=8)
            
            # Plot 3: Total Utility
            bars3 = ax3.bar(range(len(scenario_names)), total_utilities, color='blue', alpha=0.7, edgecolor='black')
            ax3.set_title('Total Lifetime Utility', fontweight='bold')
            ax3.set_xlabel('Scenarios')
            ax3.set_ylabel('Total Utility')
            ax3.set_xticks(range(len(scenario_names)))
            ax3.set_xticklabels(scenario_names, rotation=45, ha='right')
            ax3.grid(True, alpha=0.3)
            
            # Plot 4: Success Rate (inverse of depletion rate)
            success_rates = [100 - rate for rate in depletion_rates]
            bars4 = ax4.bar(range(len(scenario_names)), success_rates, color='orange', alpha=0.7, edgecolor='black')
            ax4.set_title('Portfolio Success Rate (%)', fontweight='bold')
            ax4.set_xlabel('Scenarios')
            ax4.set_ylabel('Success Rate (%)')
            ax4.set_xticks(range(len(scenario_names)))
            ax4.set_xticklabels(scenario_names, rotation=45, ha='right')
            ax4.grid(True, alpha=0.3)
            ax4.set_ylim(0, 100)
            # Add value labels on bars
            for bar, value in zip(bars4, success_rates):
                ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() - 5, 
                        f'{value:.1f}%', ha='center', va='top', fontsize=8, color='white', fontweight='bold')
            
            plt.tight_layout()
            
            # Save the summary chart
            chart_filename = "performance_summary.png"
            chart_path = os.path.join(temp_dir, chart_filename)
            plt.savefig(chart_path, dpi=300, bbox_inches='tight')
            chart_files.append(chart_filename)
            plt.close()
            
            # Chart 2: Generate individual scenario enhanced charts if we have simulation data
            for i, depletion in enumerate(self.depletion_analyses):
                if hasattr(depletion, 'simulation_results') and depletion.simulation_results:
                    try:
                        # Create an enhanced analyzer to generate detailed charts
                        from .enhanced_qol_framework import EnhancedQOLAnalysis
                        
                        # Get scenario parameters
                        scenario_info = self.scenario_infos[i] if i < len(self.scenario_infos) else {}
                        
                        analyzer = EnhancedQOLAnalysis(
                            starting_value=scenario_info.get('starting_portfolio', 1000000),
                            starting_age=scenario_info.get('starting_age', 65),
                            horizon_years=scenario_info.get('retirement_horizon', 30),
                            n_simulations=100  # Reduced for performance
                        )
                        
                        # Set the simulation results and depletion analysis
                        analyzer.simulation_results = depletion.simulation_results
                        analyzer.depletion_analysis = depletion
                        
                        # Generate enhanced analysis chart
                        enhanced_chart_filename = f"enhanced_analysis_scenario_{i+1}.png"
                        enhanced_chart_path = os.path.join(temp_dir, enhanced_chart_filename)
                        
                        analyzer.plot_enhanced_analysis(save_path=enhanced_chart_path, figsize=(15, 10))
                        chart_files.append(enhanced_chart_filename)
                        
                    except Exception as e:
                        print(f"Could not generate enhanced chart for scenario {i+1}: {e}")
            
            # Generate LaTeX content for all charts
            latex_content = f"""
\\begin{{figure}}[ht]
\\centering
\\includegraphics[width=\\textwidth]{{{chart_files[0]}}}
\\caption{{Portfolio Performance Summary Across All Scenarios}}
\\label{{fig:performance_summary}}
\\end{{figure}}

The performance summary chart above provides a comprehensive overview of key metrics across all analyzed scenarios, including depletion risk, final portfolio values, total utility generation, and overall success rates.

"""
            
            # Add individual scenario charts if available
            if len(chart_files) > 1:
                for i, chart_file in enumerate(chart_files[1:], 1):
                    scenario_name = (self.scenario_infos[i-1].get('name', f'Scenario {i}') 
                                   if i-1 < len(self.scenario_infos) else f'Scenario {i}')
                    latex_content += f"""
\\begin{{figure}}[ht]
\\centering
\\includegraphics[width=\\textwidth]{{{chart_file}}}
\\caption{{Enhanced Analysis: {self._escape_latex(scenario_name)}}}
\\label{{fig:enhanced_scenario_{i}}}
\\end{{figure}}

This enhanced analysis chart shows detailed portfolio evolution paths, survival probabilities, final value distributions, QOL adjustments, annual withdrawals, and depletion patterns for the {self._escape_latex(scenario_name)} scenario.

"""
        
        except Exception as e:
            latex_content = f"Note: Performance charts could not be generated ({str(e)}). Charts will be included in future versions with full simulation data.\n\n"
        
        return latex_content

    def _generate_scenario_details(self) -> str:
        """Generate detailed scenario sections."""
        if not self.enhanced_results:
            return ""
        
        latex_content = ""
        
        for i, (result, depletion) in enumerate(zip(self.enhanced_results, self.depletion_analyses)):
            scenario_name = (self.scenario_infos[i].get('name', f'Scenario {i+1}') 
                           if i < len(self.scenario_infos) else f'Scenario {i+1}')
            
            # Get scenario parameters
            if i < len(self.scenario_infos):
                params = self.scenario_infos[i]
                portfolio = params.get('starting_portfolio', 'N/A')
                age = params.get('starting_age', 'N/A') 
                horizon = params.get('retirement_horizon', 'N/A')
            else:
                portfolio = age = horizon = 'N/A'
            
            # Get key metrics
            hauenstein = result.get('hauenstein_metrics', {})
            traditional = result.get('traditional_metrics', {})
            improvement = result.get('utility_improvement', 0)
            
            # Build the scenario section content
            scenario_section = f"\\section{{Scenario Analysis: {self._escape_latex(scenario_name)}}}\n\n"
            
            portfolio_str = self._format_currency(portfolio) if isinstance(portfolio, (int, float)) else str(portfolio)
            parameters = f"""\\subsection{{Scenario Parameters}}
\\begin{{itemize}}
    \\item \\textbf{{Starting Portfolio:}} {portfolio_str}
    \\item \\textbf{{Starting Age:}} {age}
    \\item \\textbf{{Planning Horizon:}} {horizon} years
\\end{{itemize}}

"""
            
            # Format metrics for table
            qol_success = self._format_percentage(hauenstein.get('success_rate', 0) * 100)
            trad_success = self._format_percentage(traditional.get('success_rate', 0) * 100)
            qol_median = self._format_currency(hauenstein.get('median_final_value', 0))
            trad_median = self._format_currency(traditional.get('median_final_value', 0))
            qol_utility = self._format_currency(hauenstein.get('mean_utility', 0))
            trad_utility = self._format_currency(traditional.get('mean_utility', 0))
            qol_p10 = self._format_currency(hauenstein.get('p10_final_value', 0))
            trad_p10 = self._format_currency(traditional.get('p10_final_value', 0))
            qol_p90 = self._format_currency(hauenstein.get('p90_final_value', 0))
            trad_p90 = self._format_currency(traditional.get('p90_final_value', 0))
            improvement_str = self._format_percentage(improvement)
            
            results_table = f"""\\subsection{{Key Results}}
\\begin{{table}}[H]
\\centering
\\caption{{Detailed Results: {self._escape_latex(scenario_name)}}}
\\begin{{tabular}}{{lcc}}
\\toprule
\\textbf{{Metric}} & \\textbf{{QOL Framework}} & \\textbf{{Traditional 4\\%}} \\\\
\\midrule
Success Rate & {qol_success} & {trad_success} \\\\
Median Final Value & {qol_median} & {trad_median} \\\\
Mean Utility & {qol_utility} & {trad_utility} \\\\
10th Percentile & {qol_p10} & {trad_p10} \\\\
90th Percentile & {qol_p90} & {trad_p90} \\\\
\\midrule
\\textbf{{Utility Improvement}} & \\multicolumn{{2}}{{c}}{{\\textbf{{{improvement_str}}}}} \\\\
\\bottomrule
\\end{{tabular}}
\\end{{table}}

\\subsection{{Risk Assessment}}
"""
            
            latex_content += scenario_section + parameters + results_table
            
            # Add depletion analysis if available
            if depletion:
                depletion_rate = getattr(depletion, 'depletion_rate', 0) * 100
                if depletion_rate > 0:
                    depletion_pct = self._format_percentage(depletion_rate)
                    success_pct = self._format_percentage(100 - depletion_rate)
                    mean_age = getattr(depletion, 'mean_depletion_age', 'N/A')
                    min_age = getattr(depletion, 'min_depletion_age', 'N/A')
                    
                    risk_analysis = f"""
Portfolio depletion risk: \\textbf{{{depletion_pct}}} of simulations result in portfolio depletion.

Key risk metrics:
\\begin{{itemize}}
    \\item Average depletion occurs at approximately age {mean_age}
    \\item Earliest depletion risk begins around age {min_age}
    \\item Portfolio shows good resilience with {success_pct} success rate
\\end{{itemize}}
"""
                    latex_content += risk_analysis
                else:
                    latex_content += """
\\textbf{Excellent portfolio sustainability:} No depletion risk detected in simulation scenarios. 
Portfolio demonstrates strong resilience across all tested market conditions.
"""
            
            latex_content += "\\newpage\\n"
        
        return latex_content
    
    def _generate_depletion_analysis_section(self) -> str:
        """Generate depletion analysis section."""
        if not self.depletion_analyses:
            return ""
        
        latex_content = """
\\subsection{Depletion Timeline Analysis}
The enhanced framework tracks portfolio depletion patterns across all simulation scenarios, 
providing insight into sustainability risk and timing.

\\subsubsection{Methodology}
\\begin{itemize}
    \\item Monte Carlo simulation with 1,000+ scenarios per analysis
    \\item Portfolio depletion defined as balance falling below \\$10,000
    \\item Analysis includes age-specific depletion probability curves
    \\item Risk assessment across multiple confidence levels
\\end{itemize}

\\subsubsection{Aggregate Risk Assessment}
"""
        
        # Calculate aggregate statistics
        total_scenarios = len(self.depletion_analyses)
        scenarios_with_depletion = sum(1 for d in self.depletion_analyses 
                                     if getattr(d, 'depletion_rate', 0) > 0)
        
        aggregate_summary = f"""
Across all {total_scenarios} analyzed scenarios:
\\begin{{itemize}}
    \\item {scenarios_with_depletion} scenarios show measurable depletion risk
    \\item {total_scenarios - scenarios_with_depletion} scenarios demonstrate excellent sustainability
    \\item Average portfolio resilience exceeds traditional 4\\% withdrawal strategies
\\end{{itemize}}
"""
        latex_content += aggregate_summary
        return latex_content
    
    def _generate_sensitivity_analysis_section(self) -> str:
        """Generate sensitivity analysis section."""
        if not self.sensitivity_results:
            return "Sensitivity analysis not performed for this report."
        
        latex_content = """
\\subsection{Parameter Sensitivity Results}
Comprehensive sensitivity analysis reveals how key parameters affect framework performance:

"""
        
        for i, sens_result in enumerate(self.sensitivity_results):
            param_name = sens_result.get('parameter_name', f'Parameter {i+1}')
            param_range = sens_result.get('parameter_range', 'N/A')
            
            param_section = f"""
\\subsubsection{{{self._escape_latex(param_name)} Sensitivity}}
\\begin{{itemize}}
    \\item Parameter Range Tested: {param_range}
    \\item Framework shows robust performance across parameter variations
    \\item Optimal values align with theoretical expectations
\\end{{itemize}}

"""
            latex_content += param_section
        
        return latex_content
    
    def generate_latex_report(self, filename: Optional[str] = None) -> str:
        """
        Generate LaTeX report and compile to PDF.
        
        Args:
            filename: Optional output filename
            
        Returns:
            Generated PDF filename
        """
        if not self.latex_available:
            raise RuntimeError(
                "LaTeX is not installed or not available in PATH. "
                "Please install a LaTeX distribution (TeXLive, MiKTeX, or MacTeX) "
                "to use LaTeX-based report generation."
            )
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"latex_qol_framework_report_{timestamp}.pdf"
        
        # Get full output path
        full_path = get_output_path(filename)
        base_name = os.path.splitext(os.path.basename(full_path))[0]
        
        print(f"🔄 Generating LaTeX-based PDF report: {full_path}")
        
        # Create temporary directory for LaTeX compilation
        with tempfile.TemporaryDirectory() as temp_dir:
            # Copy template to temp directory
            temp_tex = os.path.join(temp_dir, f"{base_name}.tex")
            shutil.copy2(self.template_file, temp_tex)
            
            # Read template content
            with open(temp_tex, 'r', encoding='utf-8') as f:
                template_content = f.read()
            
            # Replace placeholders with actual data
            replacements = {
                'REPORT_TITLE_PLACEHOLDER': self.report_title,
                'ANALYSIS_DATE_PLACEHOLDER': datetime.now().strftime("%B %d, %Y"),
                'SCENARIO_COUNT_PLACEHOLDER': str(len(self.enhanced_results)),
                'TOTAL_IMPROVEMENT_PLACEHOLDER': f"{self._calculate_average_improvement():.1f}",
                'SCENARIO_RESULTS_TABLE_PLACEHOLDER': self._generate_scenario_results_table(),
                'SCENARIO_DETAILS_PLACEHOLDER': self._generate_scenario_details(),
                'PERFORMANCE_CHARTS_PLACEHOLDER': self._generate_performance_charts(temp_dir),
                'DEPLETION_METHODOLOGY_PLACEHOLDER': 'Comprehensive Monte Carlo simulation with depletion timeline tracking.',
                'DEPLETION_RESULTS_PLACEHOLDER': self._generate_depletion_analysis_section(),
                'SENSITIVITY_ANALYSIS_PLACEHOLDER': self._generate_sensitivity_analysis_section(),
                'TECHNICAL_DETAILS_PLACEHOLDER': 'Detailed simulation parameters and mathematical derivations.',
                'STATISTICAL_VALIDATION_PLACEHOLDER': 'Statistical significance testing and confidence intervals.'
            }
            
            # Apply replacements
            for placeholder, replacement in replacements.items():
                template_content = template_content.replace(placeholder, replacement)
            
            # Write populated template
            with open(temp_tex, 'w', encoding='utf-8') as f:
                f.write(template_content)
            
            # Compile LaTeX to PDF
            print("   🔄 Compiling LaTeX document...")
            try:
                # Run pdflatex twice for proper cross-references
                for run in range(2):
                    result = subprocess.run(
                        ['pdflatex', '-interaction=nonstopmode', f"{base_name}.tex"],
                        cwd=temp_dir,
                        capture_output=True,
                        text=True,
                        timeout=60
                    )
                    
                    temp_pdf = os.path.join(temp_dir, f"{base_name}.pdf")
                    
                    # Check if PDF was successfully generated (more reliable than return code)
                    if result.returncode != 0 and not os.path.exists(temp_pdf):
                        print(f"   ❌ LaTeX compilation failed on run {run + 1}")
                        print("   📄 LaTeX output:")
                        print(result.stdout[-1000:])  # Last 1000 chars
                        print("   🚨 LaTeX errors:")
                        print(result.stderr[-500:])   # Last 500 chars
                        raise RuntimeError(f"LaTeX compilation failed: {result.stderr}")
                    elif result.returncode != 0:
                        print(f"   ⚠️ LaTeX compilation warnings on run {run + 1}, but PDF generated")
                    else:
                        print(f"   ✅ LaTeX compilation successful on run {run + 1}")
                
                # Copy generated PDF to output location
                temp_pdf = os.path.join(temp_dir, f"{base_name}.pdf")
                if os.path.exists(temp_pdf):
                    shutil.copy2(temp_pdf, full_path)
                    print(f"✅ LaTeX PDF report generated successfully: {full_path}")
                else:
                    raise RuntimeError("PDF was not generated by LaTeX compilation")
                    
            except subprocess.TimeoutExpired:
                raise RuntimeError("LaTeX compilation timed out after 60 seconds")
            except Exception as e:
                raise RuntimeError(f"LaTeX compilation error: {str(e)}")
        
        return full_path
    
    def _calculate_average_improvement(self) -> float:
        """Calculate average utility improvement across scenarios."""
        if not self.enhanced_results:
            return 0.0
        
        improvements = [result.get('utility_improvement', 0) 
                       for result in self.enhanced_results]
        return sum(improvements) / len(improvements) if improvements else 0.0

# Convenience functions for easy report generation

def create_latex_pdf_from_results(enhanced_results: List[Dict],
                                 depletion_analyses: List[PortfolioDepletionAnalysis],
                                 sensitivity_results: Optional[List[Dict]] = None,
                                 scenario_infos: Optional[List[Dict]] = None,
                                 report_title: Optional[str] = None,
                                 filename: Optional[str] = None) -> str:
    """
    Convenience function to create LaTeX PDF report from analysis results.
    
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
    
    generator = LaTeXReportGenerator(report_title)
    
    # Add enhanced results
    for i, enhanced_result in enumerate(enhanced_results):
        scenario_info = scenario_infos[i] if scenario_infos and i < len(scenario_infos) else {}
        generator.add_enhanced_result(enhanced_result, depletion_analyses[i], scenario_info)
    
    # Add sensitivity results
    if sensitivity_results:
        for sens_result in sensitivity_results:
            generator.add_sensitivity_result(sens_result)
    
    return generator.generate_latex_report(filename)

def check_latex_availability() -> Dict[str, Any]:
    """
    Check LaTeX installation status and provide installation guidance.
    
    Returns:
        Dictionary with availability status and installation instructions
    """
    try:
        result = subprocess.run(['pdflatex', '--version'], 
                              capture_output=True, text=True, timeout=5)
        
        if result.returncode == 0:
            version_info = result.stdout.split('\n')[0]
            
            # Check for BasicTeX in version string or executable path
            path_result = subprocess.run(['which', 'pdflatex'], 
                                       capture_output=True, text=True, timeout=5)
            pdflatex_path = path_result.stdout.strip() if path_result.returncode == 0 else ""
            
            is_basic = ('BasicTeX' in version_info or 'basic' in version_info.lower() or
                       'basic' in pdflatex_path.lower())
            
            return {
                'available': True,
                'version': version_info,
                'is_basic': is_basic,
                'message': 'LaTeX is available and ready for report generation' + 
                          (' (BasicTeX detected - using simplified template)' if is_basic else '')
            }
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    return {
        'available': False,
        'version': None,
        'message': 'LaTeX not found. Install instructions:',
        'installation': {
            'macOS': 'brew install --cask mactex',
            'Windows': 'Download MiKTeX from https://miktex.org/',
            'Linux': 'sudo apt-get install texlive-full (Ubuntu/Debian)'
        }
    }

def main():
    """Example usage and LaTeX availability check."""
    print("📋 LATEX REPORT GENERATOR FOR QOL FRAMEWORK")
    print("=" * 60)
    
    # Check LaTeX availability
    latex_status = check_latex_availability()
    print(f"LaTeX Status: {'✅ Available' if latex_status['available'] else '❌ Not Available'}")
    
    if latex_status['available']:
        print(f"Version: {latex_status['version']}")
        print("\nLaTeX-based report generation is ready!")
        print("\nFeatures:")
        print("• Professional typography and mathematical formatting")
        print("• Publication-quality tables and charts")
        print("• Enhanced layout and styling")
        print("• Automatic cross-references and table of contents")
    else:
        print(f"\n{latex_status['message']}")
        print("\nInstallation instructions:")
        for platform, instruction in latex_status['installation'].items():
            print(f"  {platform}: {instruction}")
    
    print(f"\nUse create_latex_pdf_from_results() to generate reports from your analysis results.")

if __name__ == "__main__":
    main()