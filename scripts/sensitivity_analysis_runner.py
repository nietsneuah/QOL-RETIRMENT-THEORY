#!/usr/bin/env python3
"""
QOL Framework Sensitivity Analysis Runner

This script provides easy-to-use interfaces for running comprehensive sensitivity analysis
on the QOL framework parameters with predefined scenarios and custom parameter ranges.
"""

import sys
import os
# Add parent directory to path for cross-platform module imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import argparse
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
import numpy as np

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


class SensitivityAnalysisRunner:
    """
    Main runner for QOL framework sensitivity analysis with predefined scenarios.
    """
    
    def __init__(self):
        """Initialize sensitivity analysis runner with predefined scenarios."""
        self.predefined_scenarios = {
            'conservative_retirement': {
                'name': 'Conservative Retirement',
                'description': 'Lower risk scenario with moderate portfolio size',
                'base_parameters': {
                    'starting_value': 750000,
                    'starting_age': 65,
                    'horizon_years': 30,
                    'n_simulations': 500,
                    'return_volatility': 0.12,
                    'qol_variability': True,
                    'inflation_variability': True,
                    'withdrawal_strategy': 'hauenstein'
                }
            },
            'aggressive_retirement': {
                'name': 'Aggressive Retirement',
                'description': 'Higher risk scenario with larger portfolio and longer horizon',
                'base_parameters': {
                    'starting_value': 1500000,
                    'starting_age': 60,
                    'horizon_years': 35,
                    'n_simulations': 500,
                    'return_volatility': 0.18,
                    'qol_variability': True,
                    'inflation_variability': True,
                    'withdrawal_strategy': 'hauenstein'
                }
            },
            'moderate_retirement': {
                'name': 'Moderate Retirement',
                'description': 'Balanced scenario for typical retirement planning',
                'base_parameters': {
                    'starting_value': 1000000,
                    'starting_age': 65,
                    'horizon_years': 30,
                    'n_simulations': 500,
                    'return_volatility': 0.15,
                    'qol_variability': True,
                    'inflation_variability': True,
                    'withdrawal_strategy': 'hauenstein'
                }
            },
            'lean_fire': {
                'name': 'Lean FIRE',
                'description': 'Early retirement with smaller portfolio',
                'base_parameters': {
                    'starting_value': 500000,
                    'starting_age': 55,
                    'horizon_years': 40,
                    'n_simulations': 500,
                    'return_volatility': 0.15,
                    'qol_variability': True,
                    'inflation_variability': True,
                    'withdrawal_strategy': 'hauenstein'
                }
            },
            'fat_fire': {
                'name': 'Fat FIRE',
                'description': 'High-value retirement with substantial portfolio',
                'base_parameters': {
                    'starting_value': 2500000,
                    'starting_age': 55,
                    'horizon_years': 40,
                    'n_simulations': 500,
                    'return_volatility': 0.16,
                    'qol_variability': True,
                    'inflation_variability': True,
                    'withdrawal_strategy': 'hauenstein'
                }
            }
        }
        
        self.predefined_parameter_ranges = {
            'starting_value_sensitivity': {
                'starting_value': [500000, 750000, 1000000, 1250000, 1500000, 2000000]
            },
            'volatility_sensitivity': {
                'return_volatility': [0.10, 0.12, 0.15, 0.18, 0.20, 0.25]
            },
            'horizon_sensitivity': {
                'horizon_years': [20, 25, 30, 35, 40]
            },
            'age_sensitivity': {
                'starting_age': [55, 60, 65, 70]
            },
            'comprehensive_optimization': {
                'starting_value': [750000, 1000000, 1500000],
                'return_volatility': [0.12, 0.15, 0.18],
                'horizon_years': [25, 30, 35],
                'starting_age': [60, 65, 70]
            }
        }
    
    def list_scenarios(self):
        """List all available predefined scenarios."""
        print("📋 AVAILABLE PREDEFINED SCENARIOS:")
        print("=" * 50)
        
        for key, scenario in self.predefined_scenarios.items():
            print(f"\n{key.upper()}:")
            print(f"  Name: {scenario['name']}")
            print(f"  Description: {scenario['description']}")
            params = scenario['base_parameters']
            print(f"  Starting Value: ${params['starting_value']:,}")
            print(f"  Starting Age: {params['starting_age']}")
            print(f"  Horizon: {params['horizon_years']} years")
            print(f"  Volatility: {params['return_volatility']:.1%}")
    
    def list_parameter_ranges(self):
        """List all available predefined parameter ranges."""
        print("📋 AVAILABLE PARAMETER RANGE SETS:")
        print("=" * 50)
        
        for key, ranges in self.predefined_parameter_ranges.items():
            print(f"\n{key.upper()}:")
            for param, values in ranges.items():
                print(f"  {param}: {values}")
    
    def run_single_parameter_sensitivity(self, 
                                       scenario_key: str,
                                       parameter_name: str, 
                                       parameter_values: List[float],
                                       metric: str = 'depletion_rate',
                                       generate_pdf: bool = True,
                                       verbose: bool = True) -> Dict[str, Any]:
        """
        Run single parameter sensitivity analysis.
        
        Args:
            scenario_key: Key of predefined scenario to use as base
            parameter_name: Name of parameter to vary
            parameter_values: List of values to test
            metric: Primary metric to optimize
            generate_pdf: Whether to generate PDF report
            verbose: Whether to print detailed progress
            
        Returns:
            Dictionary with sensitivity analysis results
        """
        if scenario_key not in self.predefined_scenarios:
            raise ValueError(f"Scenario '{scenario_key}' not found. Available: {list(self.predefined_scenarios.keys())}")
        
        scenario = self.predefined_scenarios[scenario_key]
        base_params = scenario['base_parameters'].copy()
        
        if verbose:
            print(f"🎯 SINGLE PARAMETER SENSITIVITY ANALYSIS")
            print(f"Scenario: {scenario['name']}")
            print(f"Parameter: {parameter_name}")
            print(f"Values: {parameter_values}")
            print(f"Metric: {metric}")
        
        # Initialize sensitivity analyzer
        sensitivity_analyzer = QOLSensitivityAnalysis(base_params)
        
        # Run single parameter sweep
        results = sensitivity_analyzer.run_single_parameter_sweep(
            parameter_name=parameter_name,
            parameter_values=parameter_values,
            metric=metric,
            verbose=verbose
        )
        
        # Add scenario metadata
        results['scenario_info'] = scenario
        results['analysis_timestamp'] = datetime.now().isoformat()
        
        if generate_pdf:
            # Generate PDF report
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            pdf_filename = f"sensitivity_analysis_{scenario_key}_{parameter_name}_{timestamp}.pdf"
            pdf_path = get_output_path(pdf_filename)
            
            print(f"📄 Generating PDF report: {pdf_path}")
            
            # Create visualization
            fig = sensitivity_analyzer.plot_single_parameter_sensitivity(results)
            plot_filename = f"sensitivity_plot_{scenario_key}_{parameter_name}_{timestamp}.png"
            plot_path = get_output_path(plot_filename)
            fig.savefig(plot_path, dpi=300, bbox_inches='tight')
            
            # Generate text report
            report_text = sensitivity_analyzer.generate_sensitivity_report(results)
            report_filename = f"sensitivity_report_{scenario_key}_{parameter_name}_{timestamp}.txt"
            report_path = get_output_path(report_filename)
            with open(report_path, 'w') as f:
                f.write(report_text)
            
            print(f"✅ Reports generated:")
            print(f"  • Plot: {plot_path}")
            print(f"  • Report: {report_path}")
        
        return results
    
    def run_two_parameter_sensitivity(self,
                                    scenario_key: str,
                                    param1_name: str, param1_values: List[float],
                                    param2_name: str, param2_values: List[float],
                                    metric: str = 'depletion_rate',
                                    generate_pdf: bool = True,
                                    verbose: bool = True) -> Dict[str, Any]:
        """
        Run two-parameter sensitivity analysis.
        
        Args:
            scenario_key: Key of predefined scenario to use as base
            param1_name: First parameter name
            param1_values: Values for first parameter
            param2_name: Second parameter name
            param2_values: Values for second parameter  
            metric: Primary metric to optimize
            generate_pdf: Whether to generate PDF report
            verbose: Whether to print detailed progress
            
        Returns:
            Dictionary with 2D sensitivity analysis results
        """
        if scenario_key not in self.predefined_scenarios:
            raise ValueError(f"Scenario '{scenario_key}' not found")
        
        scenario = self.predefined_scenarios[scenario_key]
        base_params = scenario['base_parameters'].copy()
        
        if verbose:
            print(f"🎯 TWO-PARAMETER SENSITIVITY ANALYSIS")
            print(f"Scenario: {scenario['name']}")
            print(f"Parameters: {param1_name} vs {param2_name}")
            print(f"Grid: {len(param1_values)} x {len(param2_values)}")
            print(f"Metric: {metric}")
        
        # Initialize sensitivity analyzer
        sensitivity_analyzer = QOLSensitivityAnalysis(base_params)
        
        # Run two parameter sweep
        results = sensitivity_analyzer.run_two_parameter_sweep(
            param1_name=param1_name, param1_values=param1_values,
            param2_name=param2_name, param2_values=param2_values,
            metric=metric,
            verbose=verbose
        )
        
        # Add scenario metadata
        results['scenario_info'] = scenario
        results['analysis_timestamp'] = datetime.now().isoformat()
        
        if generate_pdf:
            # Generate visualizations
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Create heatmap visualization
            fig = sensitivity_analyzer.plot_two_parameter_heatmap(results)
            plot_filename = f"sensitivity_heatmap_{scenario_key}_{param1_name}_{param2_name}_{timestamp}.png"
            plot_path = get_output_path(plot_filename)
            fig.savefig(plot_path, dpi=300, bbox_inches='tight')
            
            # Generate text report
            report_text = sensitivity_analyzer.generate_sensitivity_report(results)
            report_filename = f"sensitivity_report_{scenario_key}_{param1_name}_{param2_name}_{timestamp}.txt"
            report_path = get_output_path(report_filename)
            with open(report_path, 'w') as f:
                f.write(report_text)
            
            print(f"✅ Reports generated:")
            print(f"  • Heatmap: {plot_path}")
            print(f"  • Report: {report_path}")
        
        return results
    
    def run_comprehensive_sensitivity(self,
                                    scenario_key: str,
                                    parameter_range_key: Optional[str] = None,
                                    custom_ranges: Optional[Dict[str, List]] = None,
                                    max_combinations: int = 500,
                                    generate_pdf: bool = True,
                                    verbose: bool = True) -> Dict[str, Any]:
        """
        Run comprehensive multi-parameter sensitivity analysis.
        
        Args:
            scenario_key: Key of predefined scenario to use as base
            parameter_range_key: Key of predefined parameter ranges
            custom_ranges: Custom parameter ranges (overrides parameter_range_key)
            max_combinations: Maximum combinations to test
            generate_pdf: Whether to generate PDF report
            verbose: Whether to print detailed progress
            
        Returns:
            Dictionary with comprehensive sensitivity results
        """
        if scenario_key not in self.predefined_scenarios:
            raise ValueError(f"Scenario '{scenario_key}' not found")
        
        scenario = self.predefined_scenarios[scenario_key]
        base_params = scenario['base_parameters'].copy()
        
        # Determine parameter ranges
        if custom_ranges:
            parameter_ranges = custom_ranges
        elif parameter_range_key:
            if parameter_range_key not in self.predefined_parameter_ranges:
                raise ValueError(f"Parameter range '{parameter_range_key}' not found")
            parameter_ranges = self.predefined_parameter_ranges[parameter_range_key]
        else:
            parameter_ranges = self.predefined_parameter_ranges['comprehensive_optimization']
        
        if verbose:
            print(f"🎯 COMPREHENSIVE SENSITIVITY ANALYSIS")
            print(f"Scenario: {scenario['name']}")
            print(f"Parameter ranges: {list(parameter_ranges.keys())}")
            print(f"Max combinations: {max_combinations:,}")
        
        # Initialize sensitivity analyzer
        sensitivity_analyzer = QOLSensitivityAnalysis(base_params)
        
        # Define parameter ranges and run comprehensive analysis
        sensitivity_analyzer.define_parameter_ranges(parameter_ranges)
        results = sensitivity_analyzer.run_comprehensive_sweep(
            max_combinations=max_combinations,
            verbose=verbose
        )
        
        # Add scenario metadata
        results['scenario_info'] = scenario
        results['analysis_timestamp'] = datetime.now().isoformat()
        results['parameter_ranges_used'] = parameter_ranges
        
        if generate_pdf:
            # Generate comprehensive report
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Generate text report
            report_text = sensitivity_analyzer.generate_sensitivity_report(results)
            report_filename = f"comprehensive_sensitivity_{scenario_key}_{timestamp}.txt"
            report_path = get_output_path(report_filename)
            with open(report_path, 'w') as f:
                f.write(report_text)
            
            # Save results as JSON
            results_filename = f"comprehensive_sensitivity_{scenario_key}_{timestamp}.json"
            results_path = get_output_path(results_filename)
            # Convert numpy arrays to lists for JSON serialization
            json_results = self._prepare_results_for_json(results)
            with open(results_path, 'w') as f:
                json.dump(json_results, f, indent=2)
            
            print(f"✅ Reports generated:")
            print(f"  • Report: {report_path}")
            print(f"  • Results: {results_path}")
        
        return results
    
    def run_predefined_analysis_suite(self,
                                    suite_name: str = 'standard',
                                    generate_combined_pdf: bool = True,
                                    verbose: bool = True) -> Dict[str, Any]:
        """
        Run a predefined suite of sensitivity analyses.
        
        Args:
            suite_name: Name of analysis suite ('standard', 'comprehensive', 'quick')
            generate_combined_pdf: Whether to generate combined PDF report
            verbose: Whether to print detailed progress
            
        Returns:
            Dictionary with all analysis results
        """
        if verbose:
            print(f"🚀 PREDEFINED ANALYSIS SUITE: {suite_name.upper()}")
            print("=" * 60)
        
        suite_results = {
            'suite_name': suite_name,
            'timestamp': datetime.now().isoformat(),
            'analyses': {}
        }
        
        if suite_name == 'quick':
            # Quick analysis for testing
            scenarios_to_test = ['moderate_retirement']
            analyses = [
                ('starting_value', [750000, 1000000, 1250000]),
                ('return_volatility', [0.12, 0.15, 0.18])
            ]
            
        elif suite_name == 'comprehensive':
            # Comprehensive analysis
            scenarios_to_test = ['conservative_retirement', 'moderate_retirement', 'aggressive_retirement']
            analyses = [
                ('starting_value', [500000, 750000, 1000000, 1250000, 1500000]),
                ('return_volatility', [0.10, 0.12, 0.15, 0.18, 0.20]),
                ('horizon_years', [20, 25, 30, 35, 40]),
                ('starting_age', [55, 60, 65, 70])
            ]
            
        else:  # standard
            # Standard analysis
            scenarios_to_test = ['conservative_retirement', 'moderate_retirement']
            analyses = [
                ('starting_value', [750000, 1000000, 1250000, 1500000]),
                ('return_volatility', [0.12, 0.15, 0.18]),
                ('horizon_years', [25, 30, 35])
            ]
        
        # Run analyses for each scenario
        for scenario_key in scenarios_to_test:
            if verbose:
                print(f"\n📊 Analyzing scenario: {self.predefined_scenarios[scenario_key]['name']}")
            
            suite_results['analyses'][scenario_key] = {}
            
            # Single parameter analyses
            for param_name, param_values in analyses:
                if verbose:
                    print(f"  🔍 Parameter: {param_name}")
                
                try:
                    results = self.run_single_parameter_sensitivity(
                        scenario_key=scenario_key,
                        parameter_name=param_name,
                        parameter_values=param_values,
                        generate_pdf=False,
                        verbose=False
                    )
                    suite_results['analyses'][scenario_key][param_name] = results
                    
                except Exception as e:
                    if verbose:
                        print(f"    ❌ Error analyzing {param_name}: {e}")
                    suite_results['analyses'][scenario_key][param_name] = {'error': str(e)}
            
            # Comprehensive analysis
            if suite_name in ['comprehensive', 'standard']:
                if verbose:
                    print(f"  🎯 Running comprehensive analysis...")
                
                try:
                    comp_results = self.run_comprehensive_sensitivity(
                        scenario_key=scenario_key,
                        parameter_range_key='comprehensive_optimization',
                        max_combinations=250 if suite_name == 'standard' else 500,
                        generate_pdf=False,
                        verbose=False
                    )
                    suite_results['analyses'][scenario_key]['comprehensive'] = comp_results
                    
                except Exception as e:
                    if verbose:
                        print(f"    ❌ Error in comprehensive analysis: {e}")
                    suite_results['analyses'][scenario_key]['comprehensive'] = {'error': str(e)}
        
        if generate_combined_pdf:
            # Generate combined PDF report with all results
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            pdf_filename = f"sensitivity_suite_{suite_name}_{timestamp}.pdf"
            pdf_path = get_output_path(pdf_filename)
            
            if verbose:
                print(f"\n📄 Generating combined PDF report: {pdf_path}")
            
            try:
                self._generate_suite_pdf_report(suite_results, pdf_path)
                print(f"✅ Combined PDF report generated: {pdf_path}")
            except Exception as e:
                print(f"❌ Error generating PDF: {e}")
        
        # Save complete results
        results_filename = f"sensitivity_suite_{suite_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        results_path = get_output_path(results_filename)
        json_results = self._prepare_results_for_json(suite_results)
        with open(results_path, 'w') as f:
            json.dump(json_results, f, indent=2)
        
        if verbose:
            print(f"\n✅ Analysis suite complete!")
            print(f"Results saved: {results_path}")
        
        return suite_results
    
    def _prepare_results_for_json(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare results for JSON serialization by converting numpy arrays to lists."""
        def convert_numpy(obj):
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
        
        return convert_numpy(results)
    
    def _generate_suite_pdf_report(self, suite_results: Dict[str, Any], filename: str):
        """Generate comprehensive PDF report for analysis suite."""
        # This would integrate with the enhanced PDF generator
        # For now, create a simple text summary
        summary_filename = filename.replace('.pdf', '_summary.txt')
        
        with open(summary_filename, 'w') as f:
            f.write("SENSITIVITY ANALYSIS SUITE SUMMARY\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Suite: {suite_results['suite_name']}\n")
            f.write(f"Timestamp: {suite_results['timestamp']}\n\n")
            
            for scenario_key, scenario_results in suite_results['analyses'].items():
                f.write(f"SCENARIO: {scenario_key.upper()}\n")
                f.write("-" * 30 + "\n")
                
                for analysis_type, results in scenario_results.items():
                    if 'error' in results:
                        f.write(f"{analysis_type}: ERROR - {results['error']}\n")
                    else:
                        f.write(f"{analysis_type}: SUCCESS\n")
                
                f.write("\n")
        
        print(f"Summary report saved: {summary_filename}")


def main():
    """Main CLI interface for sensitivity analysis runner."""
    parser = argparse.ArgumentParser(description="QOL Framework Sensitivity Analysis Runner")
    
    parser.add_argument('--list-scenarios', action='store_true',
                      help='List available predefined scenarios')
    parser.add_argument('--list-ranges', action='store_true',
                      help='List available parameter range sets')
    
    # Single parameter analysis
    parser.add_argument('--single', action='store_true',
                      help='Run single parameter sensitivity analysis')
    parser.add_argument('--scenario', type=str,
                      help='Scenario key to use as base')
    parser.add_argument('--parameter', type=str,
                      help='Parameter name to vary')
    parser.add_argument('--values', type=str,
                      help='Comma-separated list of parameter values')
    parser.add_argument('--metric', type=str, default='depletion_rate',
                      help='Metric to optimize (default: depletion_rate)')
    
    # Two parameter analysis
    parser.add_argument('--two-param', action='store_true',
                      help='Run two-parameter sensitivity analysis')
    parser.add_argument('--param1', type=str, help='First parameter name')
    parser.add_argument('--values1', type=str, help='Values for first parameter')
    parser.add_argument('--param2', type=str, help='Second parameter name')
    parser.add_argument('--values2', type=str, help='Values for second parameter')
    
    # Comprehensive analysis
    parser.add_argument('--comprehensive', action='store_true',
                      help='Run comprehensive sensitivity analysis')
    parser.add_argument('--ranges', type=str,
                      help='Parameter range set key (or JSON file)')
    parser.add_argument('--max-combinations', type=int, default=500,
                      help='Maximum combinations to test')
    
    # Analysis suite
    parser.add_argument('--suite', type=str, choices=['quick', 'standard', 'comprehensive'],
                      help='Run predefined analysis suite')
    
    # General options
    parser.add_argument('--no-pdf', action='store_true',
                      help='Skip PDF generation')
    parser.add_argument('--quiet', action='store_true',
                      help='Reduce output verbosity')
    
    args = parser.parse_args()
    
    # Initialize runner
    runner = SensitivityAnalysisRunner()
    
    # Handle list commands
    if args.list_scenarios:
        runner.list_scenarios()
        return
    
    if args.list_ranges:
        runner.list_parameter_ranges()
        return
    
    verbose = not args.quiet
    generate_pdf = not args.no_pdf
    
    try:
        # Single parameter analysis
        if args.single:
            if not all([args.scenario, args.parameter, args.values]):
                print("❌ Single parameter analysis requires --scenario, --parameter, and --values")
                return
            
            values = [float(x.strip()) for x in args.values.split(',')]
            runner.run_single_parameter_sensitivity(
                scenario_key=args.scenario,
                parameter_name=args.parameter,
                parameter_values=values,
                metric=args.metric,
                generate_pdf=generate_pdf,
                verbose=verbose
            )
        
        # Two parameter analysis
        elif args.two_param:
            if not all([args.scenario, args.param1, args.values1, args.param2, args.values2]):
                print("❌ Two parameter analysis requires --scenario, --param1, --values1, --param2, --values2")
                return
            
            values1 = [float(x.strip()) for x in args.values1.split(',')]
            values2 = [float(x.strip()) for x in args.values2.split(',')]
            
            runner.run_two_parameter_sensitivity(
                scenario_key=args.scenario,
                param1_name=args.param1,
                param1_values=values1,
                param2_name=args.param2,
                param2_values=values2,
                metric=args.metric,
                generate_pdf=generate_pdf,
                verbose=verbose
            )
        
        # Comprehensive analysis
        elif args.comprehensive:
            if not args.scenario:
                print("❌ Comprehensive analysis requires --scenario")
                return
            
            runner.run_comprehensive_sensitivity(
                scenario_key=args.scenario,
                parameter_range_key=args.ranges,
                max_combinations=args.max_combinations,
                generate_pdf=generate_pdf,
                verbose=verbose
            )
        
        # Analysis suite
        elif args.suite:
            runner.run_predefined_analysis_suite(
                suite_name=args.suite,
                generate_combined_pdf=generate_pdf,
                verbose=verbose
            )
        
        else:
            print("🎯 QOL FRAMEWORK SENSITIVITY ANALYSIS RUNNER")
            print("=" * 50)
            print("Please specify an analysis type:")
            print("  --single: Single parameter sensitivity")
            print("  --two-param: Two parameter sensitivity")
            print("  --comprehensive: Comprehensive optimization")
            print("  --suite: Predefined analysis suite")
            print("\nUse --help for detailed options.")
            print("Use --list-scenarios to see available scenarios.")
            print("Use --list-ranges to see parameter range sets.")
    
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        if verbose:
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()