#!/usr/bin/env python3
"""
Enhanced Custom Scenario Analysis with Interactive Interface

This script provides an interactive interface for running custom QOL framework analysis
with full depletion analysis and sensitivity features.
"""

import sys
import os
# Add parent directory to path for cross-platform module imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import argparse
import json
from datetime import datetime
from typing import Dict, Any, Optional

from src.enhanced_qol_framework import EnhancedQOLAnalysis
from src.sensitivity_analysis import QOLSensitivityAnalysis
from src.enhanced_pdf_report import create_enhanced_pdf_from_results

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


class EnhancedCustomScenario:
    """
    Interactive custom scenario analysis with enhanced features.
    """
    
    def __init__(self):
        """Initialize custom scenario analyzer."""
        self.default_parameters = {
            'starting_value': 1000000,
            'starting_age': 65,
            'horizon_years': 30,
            'n_simulations': 1000,
            'return_volatility': 0.15,
            'qol_variability': True,
            'inflation_variability': True,
            'withdrawal_strategy': 'hauenstein'
        }
    
    def get_user_parameters(self) -> Dict[str, Any]:
        """Get scenario parameters from user input."""
        print("📋 ENHANCED CUSTOM SCENARIO BUILDER")
        print("=" * 50)
        print("Enter your retirement scenario parameters.")
        print("Press Enter to use default values shown in [brackets].")
        print()
        
        parameters = {}
        
        # Starting portfolio value
        default = self.default_parameters['starting_value']
        while True:
            try:
                value = input(f"Starting Portfolio Value [${default:,}]: ").strip()
                if not value:
                    parameters['starting_value'] = default
                    break
                else:
                    # Remove $ and commas if present
                    clean_value = value.replace('$', '').replace(',', '')
                    parameters['starting_value'] = float(clean_value)
                    break
            except ValueError:
                print("Please enter a valid number.")
        
        # Starting age
        default = self.default_parameters['starting_age']
        while True:
            try:
                value = input(f"Starting (Retirement) Age [{default}]: ").strip()
                if not value:
                    parameters['starting_age'] = default
                    break
                else:
                    age = int(value)
                    if 45 <= age <= 80:
                        parameters['starting_age'] = age
                        break
                    else:
                        print("Please enter an age between 45 and 80.")
            except ValueError:
                print("Please enter a valid integer.")
        
        # Horizon years
        default = self.default_parameters['horizon_years']
        while True:
            try:
                value = input(f"Analysis Horizon (years) [{default}]: ").strip()
                if not value:
                    parameters['horizon_years'] = default
                    break
                else:
                    years = int(value)
                    if 10 <= years <= 50:
                        parameters['horizon_years'] = years
                        break
                    else:
                        print("Please enter a horizon between 10 and 50 years.")
            except ValueError:
                print("Please enter a valid integer.")
        
        # Number of simulations
        default = self.default_parameters['n_simulations']
        while True:
            try:
                value = input(f"Monte Carlo Simulations [{default:,}]: ").strip()
                if not value:
                    parameters['n_simulations'] = default
                    break
                else:
                    sims = int(value)
                    if 100 <= sims <= 10000:
                        parameters['n_simulations'] = sims
                        break
                    else:
                        print("Please enter a number between 100 and 10,000.")
            except ValueError:
                print("Please enter a valid integer.")
        
        # Return volatility
        default = self.default_parameters['return_volatility']
        while True:
            try:
                value = input(f"Expected Return Volatility (0.10-0.30) [{default:.2f}]: ").strip()
                if not value:
                    parameters['return_volatility'] = default
                    break
                else:
                    vol = float(value)
                    if 0.05 <= vol <= 0.35:
                        parameters['return_volatility'] = vol
                        break
                    else:
                        print("Please enter a volatility between 0.05 and 0.35.")
            except ValueError:
                print("Please enter a valid number.")
        
        # Withdrawal strategy
        print("\nWithdrawal Strategies:")
        print("  1. hauenstein (QOL-adjusted, recommended)")
        print("  2. fixed_4pct (Traditional 4% rule)")
        print("  3. dynamic_4pct (4% of current portfolio)")
        
        while True:
            strategy_choice = input("Select withdrawal strategy [1]: ").strip()
            if not strategy_choice or strategy_choice == '1':
                parameters['withdrawal_strategy'] = 'hauenstein'
                break
            elif strategy_choice == '2':
                parameters['withdrawal_strategy'] = 'fixed_4pct'
                break
            elif strategy_choice == '3':
                parameters['withdrawal_strategy'] = 'dynamic_4pct'
                break
            else:
                print("Please enter 1, 2, or 3.")
        
        # QOL variability
        qol_var = input("Include QOL variability? [Y/n]: ").strip().lower()
        parameters['qol_variability'] = qol_var != 'n'
        
        # Inflation variability
        inf_var = input("Include inflation variability? [Y/n]: ").strip().lower()
        parameters['inflation_variability'] = inf_var != 'n'
        
        return parameters
    
    def display_scenario_summary(self, parameters: Dict[str, Any]):
        """Display summary of scenario parameters."""
        print("\n📊 SCENARIO SUMMARY:")
        print("=" * 30)
        print(f"Starting Portfolio: ${parameters['starting_value']:,}")
        print(f"Starting Age: {parameters['starting_age']}")
        print(f"End Age: {parameters['starting_age'] + parameters['horizon_years']}")
        print(f"Analysis Horizon: {parameters['horizon_years']} years")
        print(f"Monte Carlo Simulations: {parameters['n_simulations']:,}")
        print(f"Return Volatility: {parameters['return_volatility']:.1%}")
        print(f"Withdrawal Strategy: {parameters['withdrawal_strategy']}")
        print(f"QOL Variability: {'Yes' if parameters['qol_variability'] else 'No'}")
        print(f"Inflation Variability: {'Yes' if parameters['inflation_variability'] else 'No'}")
        print()
        
        # Confirm before running
        confirm = input("Proceed with analysis? [Y/n]: ").strip().lower()
        return confirm != 'n'
    
    def run_enhanced_analysis(self, parameters: Dict[str, Any], verbose: bool = True) -> Dict[str, Any]:
        """
        Run enhanced analysis with full depletion analysis.
        
        Args:
            parameters: Scenario parameters
            verbose: Whether to print detailed progress
            
        Returns:
            Comprehensive analysis results
        """
        if verbose:
            print("🚀 RUNNING ENHANCED QOL ANALYSIS")
            print("=" * 40)
        
        # Initialize enhanced analyzer
        analyzer = EnhancedQOLAnalysis(
            starting_value=parameters['starting_value'],
            starting_age=parameters['starting_age'],
            horizon_years=parameters['horizon_years'],
            n_simulations=parameters['n_simulations']
        )
        
        # Run enhanced simulation
        enhanced_results = analyzer.run_enhanced_simulation(
            withdrawal_strategy=parameters['withdrawal_strategy'],
            qol_variability=parameters['qol_variability'],
            return_volatility=parameters['return_volatility'],
            inflation_variability=parameters['inflation_variability'],
            verbose=verbose
        )
        
        # Get comprehensive analysis
        comprehensive_analysis = analyzer.get_comprehensive_analysis()
        
        # Compile complete results
        complete_results = {
            'scenario_parameters': parameters,
            'enhanced_results': enhanced_results,
            'depletion_analysis': comprehensive_analysis['depletion_analysis'],
            'combined_summary': comprehensive_analysis['combined_summary'],
            'analysis_timestamp': datetime.now().isoformat(),
            'analyzer_instance': analyzer,
            'depletion_analyzer': analyzer.depletion_analysis
        }
        
        return complete_results
    
    def display_results_summary(self, results: Dict[str, Any]):
        """Display key results summary."""
        enhanced_results = results['enhanced_results']
        risk_metrics = results['depletion_analysis']['risk_metrics']
        
        print("\n🎯 ENHANCED ANALYSIS RESULTS")
        print("=" * 40)
        
        print("\n📈 Portfolio Performance:")
        print(f"  Mean Final Value: ${enhanced_results['portfolio_analysis']['final_value_mean']:,.0f}")
        print(f"  Median Final Value: ${enhanced_results['portfolio_analysis']['final_value_median']:,.0f}")
        print(f"  Portfolio Success Rate: {enhanced_results['success_rates']['never_depleted']:.1%}")
        
        print("\n⚠️  Risk Assessment:")
        print(f"  Depletion Risk: {risk_metrics['depletion_rate']:.1%}")
        print(f"  Survival Rate: {risk_metrics['survival_rate']:.1%}")
        
        print("\n👥 Longevity Analysis:")
        print(f"  Survival to Age 80: {risk_metrics['survival_at_80']:.1%}")
        print(f"  Survival to Age 90: {risk_metrics['survival_at_90']:.1%}")
        print(f"  Survival to Age 100: {risk_metrics['survival_at_100']:.1%}")
        
        if risk_metrics['depletion_rate'] > 0:
            print("\n📅 Depletion Timeline (for portfolios that deplete):")
            print(f"  Earliest Depletion: Age {risk_metrics['earliest_depletion_age']:.0f}")
            print(f"  Median Depletion: Age {risk_metrics['median_depletion_age']:.1f}")
            print(f"  5% Worst Case: Age {risk_metrics['var_95_age']:.0f}")
        
        print("\n💰 QOL Framework Impact:")
        qol_analysis = enhanced_results['qol_analysis']
        print(f"  Average QOL Adjustment: {qol_analysis['average_qol_adjustment']:.3f}")
        print(f"  Total Withdrawals (Mean): ${enhanced_results['withdrawal_analysis']['total_withdrawals_mean']:,.0f}")
        
        # Risk assessment
        print(f"\n🚦 Overall Risk Level: ", end="")
        if risk_metrics['depletion_rate'] < 0.05:
            print("LOW RISK ✅")
        elif risk_metrics['depletion_rate'] < 0.15:
            print("MODERATE RISK ⚠️")
        else:
            print("HIGH RISK ❌")
    
    def run_parameter_sensitivity(self, base_parameters: Dict[str, Any], verbose: bool = True) -> Optional[Dict[str, Any]]:
        """
        Run parameter sensitivity analysis on the custom scenario.
        
        Args:
            base_parameters: Base scenario parameters
            verbose: Whether to print progress
            
        Returns:
            Sensitivity analysis results or None if user cancels
        """
        print("\n🔍 PARAMETER SENSITIVITY ANALYSIS")
        print("=" * 40)
        print("Analyze how sensitive your results are to parameter changes.")
        
        run_sensitivity = input("Run sensitivity analysis? [y/N]: ").strip().lower()
        if run_sensitivity != 'y':
            return None
        
        print("\nSelect parameter to analyze:")
        print("  1. Starting Portfolio Value (±20%)")
        print("  2. Return Volatility (±25%)")
        print("  3. Analysis Horizon (±5 years)")
        print("  4. Starting Age (±5 years)")
        
        param_choice = input("Select parameter [1]: ").strip()
        
        # Define sensitivity ranges
        sensitivity_configs = {
            '1': ('starting_value', [
                base_parameters['starting_value'] * 0.8,
                base_parameters['starting_value'] * 0.9,
                base_parameters['starting_value'],
                base_parameters['starting_value'] * 1.1,
                base_parameters['starting_value'] * 1.2
            ]),
            '2': ('return_volatility', [
                max(0.05, base_parameters['return_volatility'] * 0.75),
                base_parameters['return_volatility'] * 0.9,
                base_parameters['return_volatility'],
                base_parameters['return_volatility'] * 1.1,
                min(0.35, base_parameters['return_volatility'] * 1.25)
            ]),
            '3': ('horizon_years', [
                max(10, base_parameters['horizon_years'] - 5),
                base_parameters['horizon_years'] - 2,
                base_parameters['horizon_years'],
                base_parameters['horizon_years'] + 2,
                min(50, base_parameters['horizon_years'] + 5)
            ]),
            '4': ('starting_age', [
                max(45, base_parameters['starting_age'] - 5),
                base_parameters['starting_age'] - 2,
                base_parameters['starting_age'],
                base_parameters['starting_age'] + 2,
                min(80, base_parameters['starting_age'] + 5)
            ])
        }
        
        if param_choice not in sensitivity_configs:
            param_choice = '1'  # Default
        
        param_name, param_values = sensitivity_configs[param_choice]
        
        if verbose:
            print(f"\nRunning sensitivity analysis for {param_name}...")
            print(f"Testing values: {param_values}")
        
        # Initialize sensitivity analyzer
        sensitivity_analyzer = QOLSensitivityAnalysis(base_parameters)
        
        # Run single parameter sweep
        sensitivity_results = sensitivity_analyzer.run_single_parameter_sweep(
            parameter_name=param_name,
            parameter_values=param_values,
            metric='depletion_rate',
            verbose=verbose
        )
        
        if verbose:
            print("\n📊 SENSITIVITY RESULTS:")
            print("-" * 25)
            optimal_idx = sensitivity_analyzer._find_optimal_index(sensitivity_results['depletion_rates'], 'depletion_rate')
            optimal_value = param_values[optimal_idx]
            optimal_depletion = sensitivity_results['depletion_rates'][optimal_idx]
            
            print(f"Optimal {param_name}: {optimal_value}")
            print(f"Minimum depletion rate: {optimal_depletion:.1%}")
            
            # Show range of outcomes
            min_depletion = min(sensitivity_results['depletion_rates'])
            max_depletion = max(sensitivity_results['depletion_rates'])
            print(f"Depletion rate range: {min_depletion:.1%} - {max_depletion:.1%}")
        
        return sensitivity_results
    
    def generate_reports(self, 
                        results: Dict[str, Any], 
                        sensitivity_results: Optional[Dict[str, Any]] = None,
                        verbose: bool = True) -> Dict[str, str]:
        """
        Generate comprehensive reports from analysis results.
        
        Args:
            results: Main analysis results
            sensitivity_results: Optional sensitivity analysis results
            verbose: Whether to print progress
            
        Returns:
            Dictionary with generated filenames
        """
        if verbose:
            print("\n📄 GENERATING REPORTS")
            print("=" * 25)
        
        generated_files = {}
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Text summary report
        summary_filename = f"custom_scenario_summary_{timestamp}.txt"
        with open(summary_filename, 'w') as f:
            f.write("ENHANCED QOL FRAMEWORK - CUSTOM SCENARIO ANALYSIS\n")
            f.write("=" * 55 + "\n\n")
            
            # Scenario parameters
            f.write("SCENARIO PARAMETERS:\n")
            f.write("-" * 20 + "\n")
            params = results['scenario_parameters']
            for key, value in params.items():
                f.write(f"{key}: {value}\n")
            
            # Results summary
            f.write(f"\n{results['combined_summary']}")
            
            # Sensitivity analysis
            if sensitivity_results:
                f.write("\n\nSENSITIVITY ANALYSIS:\n")
                f.write("-" * 20 + "\n")
                f.write(f"Parameter: {sensitivity_results['parameter_name']}\n")
                f.write(f"Values tested: {sensitivity_results['parameter_values']}\n")
                f.write(f"Depletion rates: {[f'{r:.1%}' for r in sensitivity_results['depletion_rates']]}\n")
        
        generated_files['summary'] = summary_filename
        
        # JSON results
        json_filename = f"custom_scenario_results_{timestamp}.json"
        json_path = get_output_path(json_filename)
        json_results = {
            'scenario_parameters': results['scenario_parameters'],
            'enhanced_results': results['enhanced_results'],
            'depletion_analysis': results['depletion_analysis'],
            'analysis_timestamp': results['analysis_timestamp']
        }
        
        if sensitivity_results:
            # Clean sensitivity results for JSON
            clean_sens = {k: v for k, v in sensitivity_results.items() 
                         if k not in ['full_results']}  # Remove large nested objects
            json_results['sensitivity_analysis'] = clean_sens
        
        # Convert numpy arrays to lists
        def convert_numpy(obj):
            import numpy as np
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            elif isinstance(obj, np.integer):
                return int(obj)
            elif isinstance(obj, np.floating):
                return float(obj)
            elif isinstance(obj, dict):
                return {key: convert_numpy(value) for key, value in obj.items()}
            elif isinstance(obj, list):
                return [convert_numpy(item) for item in obj]
            else:
                return obj
        
        json_results = convert_numpy(json_results)
        
        with open(json_path, 'w') as f:
            json.dump(json_results, f, indent=2)
        
        generated_files['json'] = json_path
        
        # Enhanced PDF report
        try:
            pdf_filename = create_enhanced_pdf_from_results(
                enhanced_results=[results['enhanced_results']],
                depletion_analyses=[results['depletion_analyzer']],
                sensitivity_results=[sensitivity_results] if sensitivity_results else None,
                scenario_infos=[{'name': 'Custom Scenario', 'parameters': results['scenario_parameters']}],
                report_title="Custom Scenario Analysis Report",
                filename=get_output_path(f"custom_scenario_report_{timestamp}.pdf")
            )
            generated_files['pdf'] = pdf_filename
        except Exception as e:
            if verbose:
                print(f"  ❌ PDF generation failed: {e}")
        
        # Generate visualization plots
        try:
            analyzer = results['analyzer_instance']
            charts_path = get_output_path(f"custom_scenario_charts_{timestamp}.png")
            fig = analyzer.plot_enhanced_analysis(
                save_path=charts_path
            )
            generated_files['charts'] = charts_path
            
            if sensitivity_results:
                from src.sensitivity_analysis import QOLSensitivityAnalysis
                sens_analyzer = QOLSensitivityAnalysis(results['scenario_parameters'])
                sens_path = get_output_path(f"sensitivity_analysis_{timestamp}.png")
                sens_fig = sens_analyzer.plot_single_parameter_sensitivity(
                    sensitivity_results,
                    save_path=sens_path
                )
                generated_files['sensitivity_chart'] = sens_path
        except Exception as e:
            if verbose:
                print(f"  ❌ Chart generation failed: {e}")
        
        if verbose:
            print("✅ Reports generated:")
            for report_type, filename in generated_files.items():
                print(f"  • {report_type.title()}: {filename}")
        
        return generated_files
    
    def run_interactive_analysis(self) -> Dict[str, Any]:
        """
        Run complete interactive custom scenario analysis.
        
        Returns:
            Complete analysis results
        """
        print("🚀 ENHANCED QOL FRAMEWORK - CUSTOM SCENARIO ANALYSIS")
        print("=" * 60)
        print("Welcome to the enhanced interactive scenario analyzer!")
        print("This tool will help you analyze your retirement scenario with")
        print("comprehensive risk assessment and parameter optimization.\n")
        
        # Get parameters from user
        parameters = self.get_user_parameters()
        
        # Display summary and confirm
        if not self.display_scenario_summary(parameters):
            print("Analysis cancelled.")
            return {}
        
        # Run enhanced analysis
        results = self.run_enhanced_analysis(parameters)
        
        # Display results
        self.display_results_summary(results)
        
        # Optional sensitivity analysis
        sensitivity_results = self.run_parameter_sensitivity(parameters)
        
        # Generate reports
        print("\n" + "="*50)
        generate_reports = input("Generate detailed reports? [Y/n]: ").strip().lower()
        if generate_reports != 'n':
            self.generate_reports(results, sensitivity_results)
        
        print("\n✅ Enhanced custom scenario analysis complete!")
        print("Thank you for using the Enhanced QOL Framework!")
        
        return {
            'main_results': results,
            'sensitivity_results': sensitivity_results
        }


def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(description="Enhanced Custom Scenario Analysis")
    
    parser.add_argument('--interactive', action='store_true', default=True,
                      help='Run interactive mode (default)')
    parser.add_argument('--file', type=str,
                      help='Load parameters from JSON file')
    parser.add_argument('--no-sensitivity', action='store_true',
                      help='Skip sensitivity analysis')
    parser.add_argument('--no-reports', action='store_true',
                      help='Skip report generation')
    parser.add_argument('--quiet', action='store_true',
                      help='Reduce output verbosity')
    
    args = parser.parse_args()
    
    analyzer = EnhancedCustomScenario()
    verbose = not args.quiet
    
    try:
        if args.file:
            # Load from file
            if verbose:
                print(f"Loading parameters from {args.file}...")
            
            with open(args.file, 'r') as f:
                parameters = json.load(f)
            
            # Run analysis
            results = analyzer.run_enhanced_analysis(parameters, verbose=verbose)
            
            if not args.quiet:
                analyzer.display_results_summary(results)
            
            # Optional sensitivity analysis
            sensitivity_results = None
            if not args.no_sensitivity:
                sensitivity_results = analyzer.run_parameter_sensitivity(parameters, verbose=verbose)
            
            # Generate reports
            if not args.no_reports:
                analyzer.generate_reports(results, sensitivity_results, verbose=verbose)
        
        else:
            # Interactive mode
            analyzer.run_interactive_analysis()
    
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        if verbose:
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()