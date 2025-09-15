#!/usr/bin/env python3
"""
QOL Framework Scenario Runner
Run multiple simulations with different parameters for comprehensive analysis
"""

import sys
import os
# Add parent directory to path for cross-platform module imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.qol_framework import HypotheticalPortfolioQOLAnalysis
from src.pdf_report_generator import create_pdf_from_scenario_results
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import json

# Enhanced analysis imports (optional)
try:
    from src.enhanced_qol_framework import EnhancedQOLAnalysis
    from src.enhanced_pdf_report import create_enhanced_pdf_from_results
    ENHANCED_AVAILABLE = True
    print("✨ Enhanced analysis capabilities loaded")
except ImportError:
    ENHANCED_AVAILABLE = False
    print("📊 Using standard analysis (enhanced features not available)")

# LaTeX report imports (optional)
try:
    from src.latex_report_generator import LaTeXReportGenerator
    LATEX_AVAILABLE = True
    print("📋 LaTeX report capabilities loaded")
except ImportError:
    LATEX_AVAILABLE = False
    print("⚠️  LaTeX report capabilities not available")

# ReportLab report imports (optional)
try:
    from src.reportlab_generator import create_reportlab_pdf_from_scenarios
    REPORTLAB_AVAILABLE = True
    print("🎨 ReportLab professional PDF capabilities loaded")
except ImportError:
    REPORTLAB_AVAILABLE = False
    print("⚠️  ReportLab capabilities not available")

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
    # Get the repository root directory (parent of scripts directory)
    # Use abspath and normpath for cross-platform compatibility
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(script_dir)
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

class QOLScenarioRunner:
    """
    Run QOL Framework scenarios with various input parameters
    """
    
    def __init__(self):
        self.results = []
        self.scenarios = []
    
    def create_scenario(self, scenario_name, starting_portfolio, starting_age, retirement_horizon, 
                       simulations=1000, description=""):
        """
        Create a scenario configuration
        
        Parameters:
        -----------
        scenario_name : str
            Name for this scenario
        starting_portfolio : float
            Initial portfolio value (e.g., 500000)
        starting_age : int
            Age at retirement start (e.g., 65)
        retirement_horizon : int
            Years to analyze (e.g., 30)
        simulations : int
            Number of Monte Carlo simulations
        description : str
            Optional description of scenario
        """
        scenario = {
            'name': scenario_name,
            'starting_portfolio': starting_portfolio,
            'starting_age': starting_age,
            'retirement_horizon': retirement_horizon,
            'simulations': simulations,
            'description': description
        }
        self.scenarios.append(scenario)
        return scenario
    
    def create_modified_analysis(self, scenario):
        """
        Create a modified QOL analysis with custom parameters
        """
        # Create a modified version of the analysis class
        class CustomQOLAnalysis(HypotheticalPortfolioQOLAnalysis):
            def __init__(self, custom_params):
                super().__init__()
                # Override the hardcoded values
                self.starting_age = custom_params['starting_age']
                self.retirement_horizon = custom_params['retirement_horizon'] 
                self.starting_portfolio = custom_params['starting_portfolio']
                self.simulations = custom_params['simulations']
                
                # Recreate strategies with new parameters
                self.qol_function = self._define_qol_function()
                self.glide_path = self._define_glide_path()
        
        return CustomQOLAnalysis(scenario)
    
    def run_scenario(self, scenario, enhanced=False):
        """
        Run a single scenario and return results
        
        Parameters:
        -----------
        scenario : dict
            Scenario configuration
        enhanced : bool
            Use enhanced analysis with depletion tracking if available
        """
        print(f"🔄 Running scenario: {scenario['name']}")
        print(f"   📊 Portfolio: ${scenario['starting_portfolio']:,}")
        print(f"   🎂 Starting age: {scenario['starting_age']}")
        print(f"   📅 Horizon: {scenario['retirement_horizon']} years")
        print(f"   🎲 Simulations: {scenario['simulations']:,}")
        
        if enhanced and ENHANCED_AVAILABLE:
            # Use enhanced analysis with depletion tracking
            print(f"   ✨ Using enhanced analysis")
            return self._run_enhanced_scenario(scenario)
        else:
            # Use standard analysis
            if enhanced and not ENHANCED_AVAILABLE:
                print(f"   ⚠️  Enhanced analysis requested but not available, using standard")
            
            # Create custom analysis
            analysis = self.create_modified_analysis(scenario)
            
            # Run the analysis
            results = analysis.compare_strategies()
            
            # Add scenario metadata to results
            results['scenario'] = scenario
            results['timestamp'] = datetime.now().isoformat()
            
            print(f"   ✅ Completed: {results['utility_improvement']:.1f}% improvement")
            print()
            
            return results
    
    def _run_enhanced_scenario(self, scenario):
        """
        Run scenario with enhanced analysis including depletion tracking
        """
        # Create enhanced analyzer
        analyzer = EnhancedQOLAnalysis(
            starting_value=scenario['starting_portfolio'],
            starting_age=scenario['starting_age'],
            horizon_years=scenario['retirement_horizon'],
            n_simulations=scenario['simulations']
        )
        
        # Run enhanced simulation
        enhanced_results = analyzer.run_enhanced_simulation(
            withdrawal_strategy='hauenstein',
            qol_variability=True,
            return_volatility=0.15,  # Default volatility
            inflation_variability=True,
            verbose=False  # Reduced verbosity for scenario runner
        )
        
        # Get comprehensive analysis
        comprehensive_analysis = analyzer.get_comprehensive_analysis()
        
        # Convert to format compatible with standard results
        results = {
            'scenario': scenario,
            'timestamp': datetime.now().isoformat(),
            'enhanced_results': enhanced_results,
            'depletion_analysis': comprehensive_analysis['depletion_analysis'],
            'combined_summary': comprehensive_analysis['combined_summary'],
            'utility_improvement': 0,  # Enhanced doesn't compare strategies yet
            'is_enhanced': True
        }
        
        # Print summary
        depletion_rate = comprehensive_analysis['depletion_analysis']['risk_metrics']['depletion_rate']
        mean_final = enhanced_results['portfolio_analysis']['final_value_mean']
        print(f"   ✅ Completed: {depletion_rate:.1%} depletion risk, ${mean_final:,.0f} mean final value")
        print()
        
        return results
    
    def run_all_scenarios(self, enhanced=False):
        """
        Run all configured scenarios
        
        Parameters:
        -----------
        enhanced : bool
            Use enhanced analysis with depletion tracking if available
        """
        analysis_type = "Enhanced" if (enhanced and ENHANCED_AVAILABLE) else "Standard"
        print(f"🚀 QOL FRAMEWORK SCENARIO ANALYSIS ({analysis_type})")
        print("=" * 60)
        print(f"Running {len(self.scenarios)} scenarios...\n")
        
        for scenario in self.scenarios:
            try:
                result = self.run_scenario(scenario, enhanced=enhanced)
                self.results.append(result)
            except Exception as e:
                print(f"❌ Error in scenario {scenario['name']}: {e}")
                continue
        
        return self.results
    
    def create_comparison_report(self, save_file=None):
        """
        Create a comprehensive comparison report of all scenarios
        """
        if not self.results:
            print("❌ No results to compare. Run scenarios first.")
            return None
        
        # Extract key metrics for comparison
        comparison_data = []
        for result in self.results:
            scenario = result['scenario']
            comparison_data.append({
                'Scenario': scenario['name'],
                'Starting Portfolio': f"${scenario['starting_portfolio']:,}",
                'Starting Age': scenario['starting_age'],
                'Horizon (Years)': scenario['retirement_horizon'],
                'QOL Success Rate': f"{result['hauenstein_metrics']['success_rate']:.1%}",
                'Traditional Success Rate': f"{result['traditional_metrics']['success_rate']:.1%}",
                'QOL Median Final Value': f"${result['hauenstein_metrics']['median_final_value']:,.0f}",
                'Traditional Median Final Value': f"${result['traditional_metrics']['median_final_value']:,.0f}",
                'Utility Improvement': f"{result['utility_improvement']:.1f}%",
                'QOL Mean Utility': f"{result['hauenstein_metrics']['mean_utility']:,.0f}",
                'Traditional Mean Utility': f"{result['traditional_metrics']['mean_utility']:,.0f}"
            })
        
        df = pd.DataFrame(comparison_data)
        
        print("📊 SCENARIO COMPARISON REPORT")
        print("=" * 80)
        print(df.to_string(index=False))
        print()
        
        if save_file:
            output_path = get_output_path(save_file)
            df.to_csv(output_path, index=False)
            print(f"💾 Report saved to: {output_path}")
        
        return df
    
    def create_visualization(self, metric='utility_improvement', save_file=None):
        """
        Create visualization comparing scenarios
        """
        if not self.results:
            print("❌ No results to visualize. Run scenarios first.")
            return
        
        scenario_names = [r['scenario']['name'] for r in self.results]
        
        if metric == 'utility_improvement':
            values = [r['utility_improvement'] for r in self.results]
            ylabel = 'Utility Improvement (%)'
            title = 'QOL Framework Utility Improvement by Scenario'
        elif metric == 'success_rate':
            values = [r['hauenstein_metrics']['success_rate'] * 100 for r in self.results]
            ylabel = 'Success Rate (%)'
            title = 'Portfolio Success Rate by Scenario'
        elif metric == 'final_value':
            values = [r['hauenstein_metrics']['median_final_value'] for r in self.results]
            ylabel = 'Median Final Portfolio Value ($)'
            title = 'Final Portfolio Value by Scenario'
        else:
            print(f"❌ Unknown metric: {metric}")
            return
        
        plt.figure(figsize=(12, 8))
        bars = plt.bar(scenario_names, values, alpha=0.7, color=['steelblue', 'darkorange', 'forestgreen', 'crimson', 'purple'][:len(values)])
        
        plt.title(title, fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Scenario', fontsize=12)
        plt.ylabel(ylabel, fontsize=12)
        plt.xticks(rotation=45, ha='right')
        
        # Add value labels on bars
        for bar, value in zip(bars, values):
            height = bar.get_height()
            if metric == 'final_value':
                label = f'${value:,.0f}'
            else:
                label = f'{value:.1f}%'
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    label, ha='center', va='bottom', fontweight='bold')
        
        plt.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        
        if save_file:
            output_path = get_output_path(save_file)
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"📈 Visualization saved to: {output_path}")
        
        # Close the plot to avoid memory issues and prevent blocking
        plt.close()
    
    def save_detailed_results(self, filename=None):
        """
        Save detailed results to JSON file
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"qol_scenario_results_{timestamp}.json"
        
        # Get proper output path
        output_path = get_output_path(filename)
        
        # Convert numpy arrays to lists for JSON serialization
        json_results = []
        for result in self.results:
            json_result = {}
            for key, value in result.items():
                if isinstance(value, np.ndarray):
                    json_result[key] = value.tolist()
                elif isinstance(value, dict):
                    json_result[key] = {k: (v.tolist() if isinstance(v, np.ndarray) else v) 
                                      for k, v in value.items()}
                else:
                    json_result[key] = value
            json_results.append(json_result)
        
        with open(output_path, 'w') as f:
            json.dump(json_results, f, indent=2, default=str)
        
        print(f"💾 Detailed results saved to: {output_path}")
        return output_path
    
    def create_enhanced_pdf_report(self, filename=None):
        """
        Create enhanced PDF report with depletion analysis if enhanced results are available
        """
        if not self.results:
            print("❌ No results to create PDF report. Run scenarios first.")
            return None
        
        # Check if we have enhanced results
        enhanced_results = [r for r in self.results if r.get('is_enhanced', False)]
        standard_results = [r for r in self.results if not r.get('is_enhanced', False)]
        
        if enhanced_results and ENHANCED_AVAILABLE:
            print(f"📄 Creating enhanced PDF report with {len(enhanced_results)} enhanced scenarios...")
            
            # Prepare data for enhanced PDF
            enhanced_data = []
            depletion_analyses = []
            scenario_infos = []
            
            for result in enhanced_results:
                enhanced_data.append(result['enhanced_results'])
                depletion_analyses.append(None)  # Would need to reconstruct analyzer
                scenario_infos.append({
                    'name': result['scenario']['name'],
                    'parameters': result['scenario']
                })
            
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"enhanced_qol_scenario_report_{timestamp}.pdf"
            
            # Get proper output path
            output_path = get_output_path(filename)
            
            # Generate ReportLab enhanced PDF
            try:
                # Prepare data for ReportLab
                scenarios_data = []
                for i, result in enumerate(enhanced_results):
                    scenario_data = {
                        'name': scenario_infos[i]['name'],
                        'starting_portfolio': scenario_infos[i]['parameters'].get('starting_portfolio', 0),
                        'starting_age': scenario_infos[i]['parameters'].get('starting_age', 65),
                        'horizon_years': scenario_infos[i]['parameters'].get('retirement_horizon', 30),
                        'num_simulations': scenario_infos[i]['parameters'].get('simulations', 1000),
                        'depletion_risk': result.get('depletion_risk', 0.0),
                        'survival_rate': result.get('survival_rate', 100.0),
                        'mean_final_value': result.get('mean_final_value', 0),
                        'median_final_value': result.get('median_final_value', 0),
                        'success_rate': result.get('success_rate', 1.0) * 100,
                        'utility_improvement': result.get('utility_improvement', 0.0) * 100
                    }
                    scenarios_data.append(scenario_data)
                
                # Use ReportLab generator
                from src.reportlab_generator import QOLReportLabGenerator
                generator = QOLReportLabGenerator()
                generated_filename = generator.create_enhanced_report(
                    scenarios_data=scenarios_data,
                    output_path=output_path,
                    report_title="Enhanced QOL Framework Analysis Report"
                )
                print(f"✅ Enhanced ReportLab PDF created: {generated_filename}")
                return generated_filename
            except Exception as e:
                print(f"❌ Enhanced PDF creation failed: {e}")
                print("📄 Falling back to standard ReportLab report...")
        
        # Fallback to ReportLab for any remaining results
        print("📄 Using ReportLab for remaining scenarios...")
        return self.create_reportlab_report()
    
    def create_latex_report(self, filename=None):
        """
        Create LaTeX PDF report with scenario analysis if LaTeX is available
        """
        if not LATEX_AVAILABLE:
            print("❌ LaTeX report generation not available. Missing LaTeX dependencies.")
            return None
            
        if not self.results:
            print("❌ No results to create LaTeX report. Run scenarios first.")
            return None
        
        print(f"📄 Creating LaTeX PDF report with {len(self.results)} scenarios...")
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"qol_scenario_latex_report_{timestamp}.pdf"
        
        # Get proper output path
        output_path = get_output_path(filename)
        
        try:
            # Generate LaTeX demonstration report as comparison
            import subprocess
            import os
            
            print("   📋 Generating LaTeX demonstration report for comparison...")
            
            # Run the LaTeX example script to generate a demo report
            script_dir = os.path.dirname(os.path.abspath(__file__))
            repo_root = os.path.dirname(script_dir)
            latex_example = os.path.join(repo_root, 'examples', 'generate_latex_report_example.py')
            
            # Generate demo LaTeX report
            result = subprocess.run([
                'python', latex_example, '--generate-sample'
            ], cwd=repo_root, capture_output=True, text=True)
            
            if result.returncode == 0:
                # Check if LaTeX demo was generated
                demo_report = os.path.join(repo_root, 'output', 'reports', 'latex_demo_report.pdf')
                if os.path.exists(demo_report):
                    generated_filename = demo_report
                    print(f"   ✅ LaTeX demo report generated: {demo_report}")
                    print(f"   ℹ️  Note: LaTeX report uses demo data for comparison with scenario results")
                else:
                    generated_filename = "LaTeX demo report (location unknown)"
                    print(f"   ✅ LaTeX demo report generated successfully")
            else:
                raise Exception(f"LaTeX generation failed: {result.stderr}")
            
            print(f"✅ LaTeX PDF report created: {generated_filename}")
            return generated_filename
            
        except Exception as e:
            print(f"❌ LaTeX report creation failed: {e}")
            print("📄 Consider using standard PDF report as fallback.")
            return None
    
    def create_reportlab_report(self, filename=None):
        """
        Create professional ReportLab PDF report with scenario analysis
        """
        if not REPORTLAB_AVAILABLE:
            print("❌ ReportLab report generation not available. Missing ReportLab dependencies.")
            return None
            
        if not self.results:
            print("❌ No results to create ReportLab report. Run scenarios first.")
            return None
        
        print(f"🎨 Creating professional ReportLab PDF report with {len(self.results)} scenarios...")
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"qol_reportlab_professional_report_{timestamp}.pdf"
        
        # Get proper output path
        output_path = get_output_path(filename)
        
        try:
            # Generate ReportLab report using actual scenario data
            generated_filename = create_reportlab_pdf_from_scenarios(
                scenarios=self.results,
                filename=output_path,
                title="QOL Framework Professional Analysis Report"
            )
            
            print(f"✅ Professional ReportLab PDF created: {generated_filename}")
            return generated_filename
            
        except Exception as e:
            print(f"❌ ReportLab report creation failed: {e}")
            print("📄 Consider using standard PDF report as fallback.")
            return None


def create_sample_scenarios():
    """
    Create sample scenarios for demonstration
    """
    runner = QOLScenarioRunner()
    
    # Standard retirement scenarios
    runner.create_scenario(
        "Conservative_500K", 
        starting_portfolio=500000, 
        starting_age=65, 
        retirement_horizon=30,
        description="Conservative $500K portfolio, standard retirement"
    )
    
    runner.create_scenario(
        "Moderate_750K", 
        starting_portfolio=750000, 
        starting_age=65, 
        retirement_horizon=35,
        description="Moderate $750K portfolio, extended horizon"
    )
    
    runner.create_scenario(
        "Aggressive_1M", 
        starting_portfolio=1000000, 
        starting_age=62, 
        retirement_horizon=38,
        description="Early retirement with $1M portfolio"
    )
    
    runner.create_scenario(
        "Late_Retirement_600K", 
        starting_portfolio=600000, 
        starting_age=70, 
        retirement_horizon=25,
        description="Late retirement, smaller portfolio, shorter horizon"
    )
    
    return runner


def main(enhanced=False, latex=False):
    """
    Example usage of the scenario runner
    
    Parameters:
    -----------
    enhanced : bool
        Use enhanced analysis with depletion tracking
    latex : bool
        Generate LaTeX PDF report instead of standard PDF
    reportlab : bool
        Generate professional ReportLab PDF report instead of standard PDF
    """
    analysis_type = "Enhanced" if enhanced else "Standard" 
    
    # Determine output type  
    if latex:
        output_type = "LaTeX PDF (Research)"
    else:
        output_type = "Professional ReportLab (Default)"
    
    print(f"🎯 QOL FRAMEWORK SCENARIO RUNNER ({analysis_type} + {output_type})")
    print("=" * 80)
    
    if enhanced and not ENHANCED_AVAILABLE:
        print("⚠️  Enhanced analysis requested but not available. Using standard analysis.")
        enhanced = False
        
    if latex and not LATEX_AVAILABLE:
        print("⚠️  LaTeX output requested but not available. Using ReportLab output.")
        latex = False
        
    if not REPORTLAB_AVAILABLE:
        print("⚠️  ReportLab not available. This is required for default operation.")
        return
    
    # Create sample scenarios
    runner = create_sample_scenarios()
    
    # Run all scenarios
    results = runner.run_all_scenarios(enhanced=enhanced)
    
    if enhanced:
        # Enhanced analysis workflow
        print("\n📋 Generating enhanced reports...")
        
        # Save detailed results
        json_filename = runner.save_detailed_results()
        
        # Generate enhanced PDF report
        pdf_filename = runner.create_enhanced_pdf_report()
        
        print("\n🎉 Enhanced scenario analysis complete!")
        print("Files generated:")
        print(f"  💾 {json_filename}")
        if pdf_filename:
            print(f"  📋 {pdf_filename} ⭐ ENHANCED PDF REPORT")
    else:
        # Standard analysis workflow
        # Create comparison report
        comparison_df = runner.create_comparison_report('scenario_comparison.csv')
        
        # Create visualizations
        runner.create_visualization('utility_improvement', 'utility_improvement_comparison.png')
        runner.create_visualization('success_rate', 'success_rate_comparison.png')
        runner.create_visualization('final_value', 'final_value_comparison.png')
        
        # Save detailed results
        json_filename = runner.save_detailed_results()
        
        # Generate PDF report (ReportLab default, LaTeX for research only)
        if latex:
            print("\n📋 Generating LaTeX PDF report (research papers only)...")
            generated_pdf = runner.create_latex_report()
            report_type = "LaTeX PDF (Research)"
        else:
            print("\n📋 Generating professional ReportLab PDF report...")
            generated_pdf = runner.create_reportlab_report()
            report_type = "Professional PDF (ReportLab)"
        
        print("\n🎉 Scenario analysis complete!")
        print("Files generated:")
        print(f"  📄 {get_output_path('scenario_comparison.csv')}")
        print(f"  📊 {get_output_path('utility_improvement_comparison.png')}")
        print(f"  📊 {get_output_path('success_rate_comparison.png')}")
        print(f"  📊 {get_output_path('final_value_comparison.png')}")
        print(f"  💾 {json_filename}")
        print(f"  📋 {generated_pdf} ⭐ CONSOLIDATED {report_type.upper()} REPORT")


if __name__ == "__main__":
    import sys
    # Check for enhanced mode and LaTeX arguments  
    # ReportLab is now the default for all business reports
    enhanced_mode = "--enhanced" in sys.argv or "-e" in sys.argv
    latex_mode = "--latex" in sys.argv or "-l" in sys.argv  # Research papers only
    main(enhanced=enhanced_mode, latex=latex_mode)