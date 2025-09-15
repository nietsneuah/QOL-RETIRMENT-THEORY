#!/usr/bin/env python3
"""
Enhanced Scenario Runner with Depletion Analysis Integration

This script extends the original scenario runner to include comprehensive depletion analysis,
risk assessment, and enhanced reporting capabilities.
"""

import sys
import os
# Add parent directory to path for cross-platform module imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import argparse
import json
import csv
from datetime import datetime
from typing import Dict, List, Any, Optional
import numpy as np

from src.enhanced_qol_framework import EnhancedQOLAnalysis
from src.depletion_analysis import PortfolioDepletionAnalysis
from src.reportlab_generator import QOLReportLabGenerator


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


class EnhancedScenarioRunner:
    """
    Enhanced scenario runner with integrated depletion analysis and comprehensive reporting.
    """
    
    def __init__(self):
        """Initialize enhanced scenario runner with predefined scenarios."""
        self.predefined_scenarios = {
            'conservative_retirement': {
                'name': 'Conservative Retirement',
                'starting_portfolio': 750000,
                'starting_age': 65,
                'retirement_horizon': 30,
                'simulations': 1000,
                'return_volatility': 0.12,
                'withdrawal_strategy': 'hauenstein',
                'qol_variability': True,
                'inflation_variability': True
            },
            'moderate_retirement': {
                'name': 'Moderate Retirement',
                'starting_portfolio': 1000000,
                'starting_age': 65,
                'retirement_horizon': 30,
                'simulations': 1000,
                'return_volatility': 0.15,
                'withdrawal_strategy': 'hauenstein',
                'qol_variability': True,
                'inflation_variability': True
            },
            'aggressive_retirement': {
                'name': 'Aggressive Retirement',
                'starting_portfolio': 1500000,
                'starting_age': 60,
                'retirement_horizon': 35,
                'simulations': 1000,
                'return_volatility': 0.18,
                'withdrawal_strategy': 'hauenstein',
                'qol_variability': True,
                'inflation_variability': True
            },
            'lean_fire': {
                'name': 'Lean FIRE',
                'starting_portfolio': 500000,
                'starting_age': 55,
                'retirement_horizon': 40,
                'simulations': 1000,
                'return_volatility': 0.15,
                'withdrawal_strategy': 'hauenstein',
                'qol_variability': True,
                'inflation_variability': True
            },
            'fat_fire': {
                'name': 'Fat FIRE',
                'starting_portfolio': 2500000,
                'starting_age': 55,
                'retirement_horizon': 40,
                'simulations': 1000,
                'return_volatility': 0.16,
                'withdrawal_strategy': 'hauenstein',
                'qol_variability': True,
                'inflation_variability': True
            },
            'early_retirement_modest': {
                'name': 'Early Retirement (Modest)',
                'starting_portfolio': 800000,
                'starting_age': 60,
                'retirement_horizon': 35,
                'simulations': 1000,
                'return_volatility': 0.14,
                'withdrawal_strategy': 'hauenstein',
                'qol_variability': True,
                'inflation_variability': True
            },
            'traditional_retirement': {
                'name': 'Traditional Retirement',
                'starting_portfolio': 1200000,
                'starting_age': 67,
                'retirement_horizon': 28,
                'simulations': 1000,
                'return_volatility': 0.13,
                'withdrawal_strategy': 'hauenstein',
                'qol_variability': True,
                'inflation_variability': True
            },
            # High-risk scenarios designed to test depletion analysis
            'underfunded_retirement': {
                'name': 'Underfunded Retirement (High Risk)',
                'starting_portfolio': 300000,  # Low portfolio
                'starting_age': 62,
                'retirement_horizon': 33,      # Long horizon
                'simulations': 1000,
                'return_volatility': 0.20,     # High volatility
                'withdrawal_strategy': 'hauenstein',
                'qol_variability': True,
                'inflation_variability': True
            },
            'extreme_early_retirement': {
                'name': 'Extreme Early Retirement (High Risk)',
                'starting_portfolio': 400000,  # Modest portfolio
                'starting_age': 50,            # Very early retirement
                'retirement_horizon': 45,      # Very long horizon
                'simulations': 1000,
                'return_volatility': 0.22,     # Very high volatility
                'withdrawal_strategy': 'hauenstein',
                'qol_variability': True,
                'inflation_variability': True
            },
            'market_crash_scenario': {
                'name': 'Market Crash Scenario (Extreme Risk)',
                'starting_portfolio': 500000,  # Moderate portfolio
                'starting_age': 60,
                'retirement_horizon': 35,
                'simulations': 1000,
                'return_volatility': 0.25,     # Extreme volatility
                'withdrawal_strategy': 'hauenstein',
                'qol_variability': True,
                'inflation_variability': True
            },
            'traditional_4percent_risky': {
                'name': 'Traditional 4% Rule (High Depletion Risk)',
                'starting_portfolio': 400000,  # Small portfolio
                'starting_age': 55,            # Early retirement
                'retirement_horizon': 40,      # Long horizon
                'simulations': 1000,
                'return_volatility': 0.20,     # High volatility
                'withdrawal_strategy': 'traditional',  # Use 4% rule instead
                'qol_variability': True,
                'inflation_variability': True
            },
            'withdrawal_stress_test_5pct': {
                'name': 'Traditional 5% Withdrawal Rate Test',
                'starting_portfolio': 1000000,  # Standard portfolio
                'starting_age': 60,             # Reasonable retirement age
                'retirement_horizon': 30,       # Standard 30-year horizon
                'simulations': 1000,
                'return_volatility': 0.18,      # Realistic market volatility
                'withdrawal_strategy': 'traditional',  # Fixed % withdrawal
                'base_withdrawal_rate': 0.05,   # 5% instead of 4%
                'qol_variability': True,
                'inflation_variability': True
            },
            'withdrawal_stress_test_6pct': {
                'name': 'Traditional 6% Withdrawal Rate Test',
                'starting_portfolio': 1000000,  # Standard portfolio
                'starting_age': 60,             # Reasonable retirement age
                'retirement_horizon': 30,       # Standard 30-year horizon
                'simulations': 1000,
                'return_volatility': 0.18,      # Realistic market volatility
                'withdrawal_strategy': 'traditional',  # Fixed % withdrawal
                'base_withdrawal_rate': 0.06,   # 6% withdrawal rate
                'qol_variability': True,
                'inflation_variability': True
            },
            'bear_market_sequence': {
                'name': 'Early Bear Market Sequence Risk',
                'starting_portfolio': 1000000,  # Standard portfolio  
                'starting_age': 65,             # Standard retirement
                'retirement_horizon': 30,       # Standard horizon
                'simulations': 1000,
                'return_volatility': 0.22,      # Higher volatility (bear market)
                'withdrawal_strategy': 'traditional',  # Traditional 4% rule  
                'qol_variability': False,       # Remove QOL adjustments to focus on withdrawal
                'inflation_variability': True
            },
            'qol_value_demonstration': {
                'name': 'QOL Strategy vs Traditional Comparison',
                'starting_portfolio': 1000000,  # Standard $1M portfolio
                'starting_age': 70,             # Standardized retirement age
                'retirement_horizon': 35,       # Standardized 35-year horizon
                'simulations': 1000,
                'return_volatility': 0.15,      # Moderate volatility
                'withdrawal_strategy': 'hauenstein',  # QOL-driven approach
                'qol_variability': True,        # Include QOL adjustments
                'inflation_variability': True
            },
            'traditional_comparison': {
                'name': 'Traditional 4% Rule Baseline',
                'starting_portfolio': 1000000,  # Standard $1M portfolio
                'starting_age': 70,             # Standardized retirement age
                'retirement_horizon': 35,       # Standardized 35-year horizon
                'simulations': 1000,
                'return_volatility': 0.15,      # Same volatility
                'withdrawal_strategy': 'traditional',  # Traditional 4% rule
                'qol_variability': False,       # No QOL adjustments
                'inflation_variability': True
            },
            'qol_conservative': {
                'name': 'Conservative QOL (4.8%/4.2%/3.2%)',
                'starting_portfolio': 1000000,
                'starting_age': 70,
                'retirement_horizon': 35,
                'simulations': 1000,
                'return_volatility': 0.15,
                'withdrawal_strategy': 'hauenstein',
                'qol_phase1_rate': 0.048,       # 4.8% (vs 5.4% baseline)
                'qol_phase2_rate': 0.042,       # 4.2% (vs 4.5% baseline)
                'qol_phase3_rate': 0.032,       # 3.2% (vs 3.5% baseline)
                'qol_variability': True,
                'inflation_variability': True
            },
            'qol_aggressive': {
                'name': 'Aggressive QOL (6.0%/4.8%/3.6%)',
                'starting_portfolio': 1000000,
                'starting_age': 70,
                'retirement_horizon': 35,
                'simulations': 1000,
                'return_volatility': 0.15,
                'withdrawal_strategy': 'hauenstein',
                'qol_phase1_rate': 0.060,       # 6.0% - higher early spending
                'qol_phase2_rate': 0.048,       # 4.8% 
                'qol_phase3_rate': 0.036,       # 3.6%
                'qol_variability': True,
                'inflation_variability': True
            },
            'qol_extreme': {
                'name': 'Extreme QOL (7.0%/5.0%/4.0%) - Testing Limits',
                'starting_portfolio': 1000000,
                'starting_age': 70,
                'retirement_horizon': 35,
                'simulations': 1000,
                'return_volatility': 0.15,
                'withdrawal_strategy': 'hauenstein',
                'qol_phase1_rate': 0.070,       # 7.0% - very high early spending
                'qol_phase2_rate': 0.050,       # 5.0%
                'qol_phase3_rate': 0.040,       # 4.0%
                'qol_variability': True,
                'inflation_variability': True
            },
            'optimal_depletion_low_vol': {
                'name': 'Optimal Depletion Strategy (Low Volatility)',
                'starting_portfolio': 1000000,
                'starting_age': 70,
                'retirement_horizon': 35,
                'simulations': 1000,
                'return_volatility': 0.12,      # Low volatility
                'withdrawal_strategy': 'hauenstein',
                'qol_phase1_rate': 0.080,       # 8.0% - aggressive early spending
                'qol_phase2_rate': 0.060,       # 6.0%
                'qol_phase3_rate': 0.045,       # 4.5%
                'qol_variability': True,
                'inflation_variability': True
            },
            'optimal_depletion_med_vol': {
                'name': 'Optimal Depletion Strategy (Medium Volatility)',
                'starting_portfolio': 1000000,
                'starting_age': 70,
                'retirement_horizon': 35,
                'simulations': 1000,
                'return_volatility': 0.18,      # Medium volatility
                'withdrawal_strategy': 'hauenstein',
                'qol_phase1_rate': 0.080,       # 8.0% - same spending pattern
                'qol_phase2_rate': 0.060,       # 6.0%
                'qol_phase3_rate': 0.045,       # 4.5%
                'qol_variability': True,
                'inflation_variability': True
            },
            'optimal_depletion_high_vol': {
                'name': 'Optimal Depletion Strategy (High Volatility)',
                'starting_portfolio': 1000000,
                'starting_age': 70,
                'retirement_horizon': 35,
                'simulations': 1000,
                'return_volatility': 0.25,      # High volatility
                'withdrawal_strategy': 'hauenstein',
                'qol_phase1_rate': 0.080,       # 8.0% - testing risk tolerance
                'qol_phase2_rate': 0.060,       # 6.0%
                'qol_phase3_rate': 0.045,       # 4.5%
                'qol_variability': True,
                'inflation_variability': True
            },
            'maximum_spending_test': {
                'name': 'Maximum Spending Test (9%/7%/5%)',
                'starting_portfolio': 1000000,
                'starting_age': 70,
                'retirement_horizon': 35,
                'simulations': 1000,
                'return_volatility': 0.20,      # Realistic high volatility
                'withdrawal_strategy': 'hauenstein',
                'qol_phase1_rate': 0.090,       # 9.0% - maximum early spending
                'qol_phase2_rate': 0.070,       # 7.0%
                'qol_phase3_rate': 0.050,       # 5.0%
                'qol_variability': True,
                'inflation_variability': True
            }
        }
        
        self.results = []
    
    def list_scenarios(self):
        """List all available predefined scenarios."""
        print("📋 ENHANCED SCENARIO RUNNER - AVAILABLE SCENARIOS:")
        print("=" * 60)
        
        for key, scenario in self.predefined_scenarios.items():
            print(f"\n{key.upper()}:")
            print(f"  Name: {scenario['name']}")
            print(f"  Starting Portfolio: ${scenario['starting_portfolio']:,}")
            print(f"  Starting Age: {scenario['starting_age']}")
            print(f"  Horizon: {scenario['retirement_horizon']} years")
            print(f"  Simulations: {scenario['simulations']:,}")
            print(f"  Volatility: {scenario['return_volatility']:.1%}")
            print(f"  Strategy: {scenario['withdrawal_strategy']}")
    
    def run_single_scenario(self, 
                           scenario_key: Optional[str] = None,
                           custom_scenario: Optional[Dict] = None,
                           verbose: bool = True) -> Dict[str, Any]:
        """
        Run a single scenario with enhanced analysis.
        
        Args:
            scenario_key: Key of predefined scenario
            custom_scenario: Custom scenario parameters
            verbose: Whether to print detailed progress
            
        Returns:
            Dictionary with comprehensive results
        """
        # Determine scenario parameters
        if custom_scenario:
            scenario = custom_scenario
        elif scenario_key and scenario_key in self.predefined_scenarios:
            scenario = self.predefined_scenarios[scenario_key]
        else:
            raise ValueError(f"Must provide either scenario_key or custom_scenario")
        
        scenario_name = scenario.get('name', scenario_key or 'Custom Scenario')
        
        if verbose:
            print(f"🎯 RUNNING ENHANCED SCENARIO: {scenario_name}")
            print("=" * 50)
            print(f"Starting Portfolio: ${scenario['starting_portfolio']:,} (nominal)")
            print(f"Starting Age: {scenario['starting_age']}")
            print(f"Horizon: {scenario['retirement_horizon']} years")
            print(f"Simulations: {scenario['simulations']:,}")
            print(f"Volatility: {scenario.get('return_volatility', 0.15):.1%}")
            print(f"Strategy: {scenario.get('withdrawal_strategy', 'hauenstein')}")
            print("Note: All dollar amounts reported in nominal (non-inflation-adjusted) terms")
        
        # Initialize enhanced analyzer
        analyzer = EnhancedQOLAnalysis(
            starting_value=scenario['starting_portfolio'],
            starting_age=scenario['starting_age'],
            horizon_years=scenario['retirement_horizon'],
            n_simulations=scenario['simulations'],
            qol_phase1_rate=scenario.get('qol_phase1_rate', 0.054),
            qol_phase2_rate=scenario.get('qol_phase2_rate', 0.045),
            qol_phase3_rate=scenario.get('qol_phase3_rate', 0.035)
        )
        
        # Run enhanced simulation
        enhanced_results = analyzer.run_enhanced_simulation(
            withdrawal_strategy=scenario.get('withdrawal_strategy', 'hauenstein'),
            qol_variability=scenario.get('qol_variability', True),
            return_volatility=scenario.get('return_volatility', 0.15),
            inflation_variability=scenario.get('inflation_variability', True),
            verbose=verbose
        )
        
        # Get comprehensive analysis (includes depletion analysis)
        comprehensive_analysis = analyzer.get_comprehensive_analysis()
        
        # Compile results
        scenario_results = {
            'scenario_info': {
                'name': scenario_name,
                'key': scenario_key,
                'parameters': scenario,
                'timestamp': datetime.now().isoformat()
            },
            'enhanced_results': enhanced_results,
            'depletion_analysis': comprehensive_analysis['depletion_analysis'],
            'combined_summary': comprehensive_analysis['combined_summary'],
            'analyzer_instance': analyzer,  # Keep for plotting
            'depletion_analyzer': analyzer.depletion_analysis
        }
        
        if verbose:
            print("\n📊 SCENARIO RESULTS SUMMARY (All Values in Nominal Dollars):")
            print("-" * 30)
            
            # Key metrics
            risk_metrics = analyzer.depletion_analysis.get_risk_metrics()
            print(f"Depletion Risk: {risk_metrics['depletion_rate']:.1%}")
            print(f"Survival Rate: {risk_metrics['survival_rate']:.1%}")
            print(f"Mean Final Value: ${enhanced_results['portfolio_analysis']['final_value_mean']:,.0f} (nominal)")
            
            # Calculate and display early withdrawal amounts in nominal terms
            if scenario.get('qol_phase1_rate'):
                early_withdrawal = scenario['starting_portfolio'] * scenario.get('qol_phase1_rate', 0.054)
                print(f"Year 1 Withdrawal: ${early_withdrawal:,.0f} (nominal)")
            elif scenario.get('withdrawal_strategy') == 'traditional':
                early_withdrawal = scenario['starting_portfolio'] * 0.04
                print(f"Year 1 Withdrawal: ${early_withdrawal:,.0f} (nominal)")
                
            print(f"Survival at Age 90: {risk_metrics['survival_at_90']:.1%}")
            
            if risk_metrics['depletion_rate'] > 0:
                print(f"Median Depletion Age: {risk_metrics['median_depletion_age']:.1f}")
                print(f"5% Worst Case: Age {risk_metrics['var_95_age']:.0f}")
        
        self.results.append(scenario_results)
        return scenario_results
    
    def run_multiple_scenarios(self,
                             scenario_keys: List[str],
                             verbose: bool = True) -> List[Dict[str, Any]]:
        """
        Run multiple predefined scenarios.
        
        Args:
            scenario_keys: List of scenario keys to run
            verbose: Whether to print detailed progress
            
        Returns:
            List of scenario results
        """
        if verbose:
            print(f"🚀 RUNNING {len(scenario_keys)} ENHANCED SCENARIOS")
            print("=" * 60)
        
        scenario_results = []
        
        for i, scenario_key in enumerate(scenario_keys, 1):
            if verbose:
                print(f"\n[{i}/{len(scenario_keys)}] Starting scenario: {scenario_key}")
            
            try:
                result = self.run_single_scenario(
                    scenario_key=scenario_key,
                    verbose=verbose
                )
                scenario_results.append(result)
                
                if verbose:
                    print(f"✅ Scenario {scenario_key} completed successfully")
                    
            except Exception as e:
                if verbose:
                    print(f"❌ Scenario {scenario_key} failed: {e}")
                # Add error result
                error_result = {
                    'scenario_info': {
                        'name': scenario_key,
                        'key': scenario_key,
                        'error': str(e),
                        'timestamp': datetime.now().isoformat()
                    }
                }
                scenario_results.append(error_result)
        
        self.results.extend(scenario_results)
        return scenario_results
    
    def run_all_scenarios(self, verbose: bool = True) -> List[Dict[str, Any]]:
        """
        Run all predefined scenarios.
        
        Args:
            verbose: Whether to print detailed progress
            
        Returns:
            List of all scenario results
        """
        all_scenario_keys = list(self.predefined_scenarios.keys())
        return self.run_multiple_scenarios(all_scenario_keys, verbose)
    
    def generate_comparison_table(self, 
                                results: Optional[List[Dict]] = None,
                                save_csv: bool = True,
                                verbose: bool = True) -> str:
        """
        Generate comparison table of scenario results.
        
        Args:
            results: List of results to compare (uses self.results if None)
            save_csv: Whether to save as CSV file
            verbose: Whether to print the table
            
        Returns:
            Formatted table string
        """
        if results is None:
            results = self.results
        
        if not results:
            return "No results available for comparison."
        
        # Extract key metrics for comparison
        comparison_data = []
        headers = [
            'Scenario', 'Starting Portfolio', 'Starting Age', 'Horizon (Years)',
            'Depletion Risk (%)', 'Survival Rate (%)', 'Survival at 90 (%)',
            'Final Value Mean ($)', 'Final Value Median ($)',
            'Mean Depletion Age', '5% Worst Case Age'
        ]
        
        for result in results:
            if 'error' in result['scenario_info']:
                continue  # Skip error results
            
            scenario_info = result['scenario_info']
            enhanced_results = result['enhanced_results']
            risk_metrics = result['depletion_analysis']['risk_metrics']
            
            row = [
                scenario_info['name'],
                f"${scenario_info['parameters']['starting_portfolio']:,}",
                scenario_info['parameters']['starting_age'],
                scenario_info['parameters']['retirement_horizon'],
                f"{risk_metrics['depletion_rate']*100:.1f}%",
                f"{risk_metrics['survival_rate']*100:.1f}%",
                f"{risk_metrics['survival_at_90']*100:.1f}%",
                f"${enhanced_results['portfolio_analysis']['final_value_mean']:,.0f}",
                f"${enhanced_results['portfolio_analysis']['final_value_median']:,.0f}",
                f"{risk_metrics['mean_depletion_age']:.1f}" if np.isfinite(risk_metrics['mean_depletion_age']) else "N/A",
                f"{risk_metrics['var_95_age']:.0f}" if np.isfinite(risk_metrics['var_95_age']) else "N/A"
            ]
            comparison_data.append(row)
        
        # Create formatted table string
        if not comparison_data:
            return "No valid results for comparison."
        
        # Calculate column widths
        col_widths = []
        for i in range(len(headers)):
            max_width = max(len(headers[i]), max(len(str(row[i])) for row in comparison_data))
            col_widths.append(max_width + 2)
        
        # Build table
        table_lines = []
        
        # Header
        header_line = "|".join(headers[i].ljust(col_widths[i]) for i in range(len(headers)))
        table_lines.append(header_line)
        table_lines.append("-" * len(header_line))
        
        # Data rows
        for row in comparison_data:
            data_line = "|".join(str(row[i]).ljust(col_widths[i]) for i in range(len(row)))
            table_lines.append(data_line)
        
        table_string = "\n".join(table_lines)
        
        if verbose:
            print("\n📊 ENHANCED SCENARIO COMPARISON TABLE:")
            print("=" * 80)
            print(table_string)
        
        # Save as CSV
        if save_csv:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            csv_filename = get_output_path(f"enhanced_scenario_comparison_{timestamp}.csv")
            
            with open(csv_filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(headers)
                for row in comparison_data:
                    # Clean currency formatting for CSV
                    clean_row = []
                    for cell in row:
                        if isinstance(cell, str) and cell.startswith('$'):
                            clean_row.append(cell.replace('$', '').replace(',', ''))
                        elif isinstance(cell, str) and cell.endswith('%'):
                            clean_row.append(cell.replace('%', ''))
                        else:
                            clean_row.append(cell)
                    writer.writerow(clean_row)
            
            if verbose:
                print(f"📁 Comparison saved to: {csv_filename}")
        
        return table_string
    
    def generate_comprehensive_report(self,
                                    results: Optional[List[Dict]] = None,
                                    filename: Optional[str] = None,
                                    verbose: bool = True) -> str:
        """
        Generate comprehensive PDF report with all enhanced features.
        
        Args:
            results: List of results to include (uses self.results if None)
            filename: Optional output filename
            verbose: Whether to print progress
            
        Returns:
            Generated filename
        """
        if results is None:
            results = self.results
        
        if not results:
            raise ValueError("No results available for reporting")
        
        # Filter out error results
        valid_results = [r for r in results if 'error' not in r['scenario_info']]
        
        if not valid_results:
            raise ValueError("No valid results for reporting")
        
        if verbose:
            print(f"📄 Generating comprehensive PDF report for {len(valid_results)} scenarios...")
        
        # Prepare data for ReportLab PDF generator
        scenarios_data = []
        
        for result in valid_results:
            # Extract risk metrics from depletion analyzer
            risk_metrics = result['depletion_analyzer'].get_risk_metrics()
            # Extract portfolio analysis from enhanced results
            portfolio_analysis = result['enhanced_results']['portfolio_analysis']
            # Extract scenario parameters properly
            scenario_params = result['scenario_info']['parameters']
            
            scenario_data = {
                'name': result['scenario_info'].get('name', 'Unknown Scenario'),
                'starting_portfolio': scenario_params.get('starting_portfolio', 0),
                'starting_age': scenario_params.get('starting_age', 65),
                'horizon_years': scenario_params.get('retirement_horizon', 30),
                'num_simulations': scenario_params.get('simulations', 1000),
                'depletion_risk': risk_metrics.get('depletion_rate', 0.0) * 100,  # Convert to percentage
                'survival_rate': risk_metrics.get('survival_rate', 1.0) * 100,    # Convert to percentage
                'mean_final_value': portfolio_analysis.get('final_value_mean', 0),
                'median_final_value': portfolio_analysis.get('final_value_median', 0),
                'success_rate': result['enhanced_results'].get('success_rate', 1.0) * 100,
                'utility_improvement': result['enhanced_results'].get('utility_improvement', 0.0) * 100
            }
            scenarios_data.append(scenario_data)
        
        # Generate ReportLab PDF report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if filename is None:
            filename = get_output_path(f"enhanced_qol_reportlab_report_{timestamp}.pdf", "reports")
        
        generator = QOLReportLabGenerator()
        generated_filename = generator.create_enhanced_report(
            scenarios_data=scenarios_data,
            output_path=filename,
            report_title=f"Enhanced QOL Framework Analysis - {len(valid_results)} Scenarios"
        )
        
        if verbose:
            print(f"✅ Comprehensive PDF report generated: {generated_filename}")
        
        return generated_filename
    
    def save_results_json(self,
                         results: Optional[List[Dict]] = None,
                         filename: Optional[str] = None,
                         verbose: bool = True) -> str:
        """
        Save results to JSON file.
        
        Args:
            results: Results to save (uses self.results if None)
            filename: Optional output filename
            verbose: Whether to print progress
            
        Returns:
            Generated filename
        """
        if results is None:
            results = self.results
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"enhanced_scenario_results_{timestamp}.json"
        
        # Ensure file is saved to output directory
        full_path = get_output_path(filename)
        
        # Prepare results for JSON serialization
        json_results = []
        for result in results:
            # Remove non-serializable objects
            json_result = result.copy()
            json_result.pop('analyzer_instance', None)
            json_result.pop('depletion_analyzer', None)
            json_results.append(json_result)
        
        # Convert numpy arrays to lists
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
        
        json_results = convert_numpy(json_results)
        
        # Save to file
        with open(full_path, 'w') as f:
            json.dump(json_results, f, indent=2)
        
        if verbose:
            print(f"📁 Results saved to JSON: {full_path}")
        
        return full_path


def main():
    """Main CLI interface for enhanced scenario runner."""
    parser = argparse.ArgumentParser(description="Enhanced QOL Framework Scenario Runner with Professional ReportLab PDF Reports")
    
    # List available scenarios
    parser.add_argument('--list', action='store_true',
                      help='List available predefined scenarios')
    
    # Single scenario
    parser.add_argument('--scenario', type=str,
                      help='Run single predefined scenario')
    parser.add_argument('--custom', type=str,
                      help='JSON file with custom scenario parameters')
    
    # Multiple scenarios
    parser.add_argument('--scenarios', type=str,
                      help='Comma-separated list of scenario keys')
    parser.add_argument('--all', action='store_true',
                      help='Run all predefined scenarios')
    
    # Output options (ReportLab PDF is now default)
    parser.add_argument('--json', action='store_true',
                      help='Save results to JSON file')
    parser.add_argument('--csv', action='store_true', default=True,
                      help='Generate CSV comparison table (default: True)')
    parser.add_argument('--no-csv', action='store_true',
                      help='Skip CSV comparison table')
    
    # Control options
    parser.add_argument('--quiet', action='store_true',
                      help='Reduce output verbosity')
    parser.add_argument('--output-dir', type=str,
                      help='Output directory for generated files')
    
    args = parser.parse_args()
    
    # Change to output directory if specified
    if args.output_dir:
        os.makedirs(args.output_dir, exist_ok=True)
        os.chdir(args.output_dir)
    
    verbose = not args.quiet
    
    # Initialize runner
    runner = EnhancedScenarioRunner()
    
    try:
        # List scenarios
        if args.list:
            runner.list_scenarios()
            return
        
        results = []
        
        # Single scenario
        if args.scenario:
            if verbose:
                print("🎯 Running single scenario...")
            result = runner.run_single_scenario(scenario_key=args.scenario, verbose=verbose)
            results.append(result)
        
        # Custom scenario
        elif args.custom:
            if verbose:
                print("🎯 Running custom scenario...")
            with open(args.custom, 'r') as f:
                custom_scenario = json.load(f)
            result = runner.run_single_scenario(custom_scenario=custom_scenario, verbose=verbose)
            results.append(result)
        
        # Multiple scenarios
        elif args.scenarios:
            scenario_keys = [key.strip() for key in args.scenarios.split(',')]
            results = runner.run_multiple_scenarios(scenario_keys, verbose=verbose)
        
        # All scenarios
        elif args.all:
            results = runner.run_all_scenarios(verbose=verbose)
        
        else:
            print("🎯 ENHANCED QOL FRAMEWORK SCENARIO RUNNER")
            print("=" * 50)
            print("Please specify scenarios to run:")
            print("  --scenario: Run single predefined scenario")
            print("  --custom: Run custom scenario from JSON file")
            print("  --scenarios: Run multiple scenarios (comma-separated)")
            print("  --all: Run all predefined scenarios")
            print("\nUse --list to see available scenarios.")
            print("Use --help for detailed options.")
            return
        
        if not results:
            print("❌ No results to process")
            return
        
        # Generate outputs
        if verbose:
            print(f"\n📊 Processing {len(results)} scenario results...")
        
        # Comparison table (default)
        if not args.no_csv:
            runner.generate_comparison_table(results, save_csv=args.csv, verbose=verbose)
        
        # JSON output
        if args.json:
            runner.save_results_json(results, verbose=verbose)
        
        # ReportLab PDF report (default)
        runner.generate_comprehensive_report(results, verbose=verbose)
        
        if verbose:
            print(f"\n✅ Enhanced scenario analysis complete!")
            print(f"   Scenarios processed: {len([r for r in results if 'error' not in r['scenario_info']])}")
            print(f"   Errors encountered: {len([r for r in results if 'error' in r['scenario_info']])}")
    
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        if verbose:
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()