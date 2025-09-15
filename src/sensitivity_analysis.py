"""
QOL Sensitivity Analysis System

This module provides comprehensive sensitivity analysis capabilities for the QOL framework,
including parameter sweeps, optimization recommendations, and advanced visualizations.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns
from typing import Dict, List, Tuple, Optional, Any, Callable
from itertools import product
import warnings
warnings.filterwarnings('ignore')

from .enhanced_qol_framework import EnhancedQOLAnalysis
from .depletion_analysis import PortfolioDepletionAnalysis


class QOLSensitivityAnalysis:
    """
    Comprehensive sensitivity analysis for QOL framework parameters.
    
    This class provides:
    - Multi-parameter sensitivity sweeps
    - Heatmap visualizations 
    - 3D surface plots
    - Optimization recommendations
    - Risk surface analysis
    - Parameter interaction effects
    """
    
    def __init__(self, base_parameters: Optional[Dict[str, Any]] = None):
        """
        Initialize sensitivity analysis with base parameters.
        
        Args:
            base_parameters: Dictionary of baseline parameter values
        """
        # Default base parameters
        self.base_parameters = base_parameters or {
            'starting_value': 1000000,
            'starting_age': 65,
            'horizon_years': 30,
            'n_simulations': 500,  # Reduced for faster sensitivity analysis
            'return_volatility': 0.15,
            'qol_variability': True,
            'inflation_variability': True,
            'withdrawal_strategy': 'hauenstein'
        }
        
        # Results storage
        self.sensitivity_results = {}
        self.parameter_ranges = {}
        
    def define_parameter_ranges(self, parameter_ranges: Dict[str, List]) -> None:
        """
        Define ranges for sensitivity analysis parameters.
        
        Args:
            parameter_ranges: Dictionary mapping parameter names to lists of values to test
        """
        self.parameter_ranges = parameter_ranges
        print(f"Defined sensitivity ranges for {len(parameter_ranges)} parameters:")
        for param, values in parameter_ranges.items():
            print(f"  • {param}: {len(values)} values from {min(values)} to {max(values)}")
    
    def run_single_parameter_sweep(self, 
                                  parameter_name: str,
                                  parameter_values: List[float],
                                  metric: str = 'depletion_rate',
                                  verbose: bool = True) -> Dict[str, Any]:
        """
        Run sensitivity analysis for a single parameter.
        
        Args:
            parameter_name: Name of parameter to vary
            parameter_values: List of values to test
            metric: Metric to optimize ('depletion_rate', 'final_value_mean', etc.)
            verbose: Whether to print progress
            
        Returns:
            Dictionary with sweep results
        """
        if verbose:
            print(f"\nRunning single parameter sweep for '{parameter_name}'...")
            print(f"Testing {len(parameter_values)} values: {parameter_values}")
        
        results = {
            'parameter_name': parameter_name,
            'parameter_values': parameter_values,
            'metric': metric,
            'metric_values': [],
            'full_results': [],
            'depletion_rates': [],
            'final_values': [],
            'survival_rates': []
        }
        
        for i, param_value in enumerate(parameter_values):
            if verbose:
                print(f"  Testing {parameter_name}={param_value} ({i+1}/{len(parameter_values)})...")
            
            # Create modified parameters
            test_params = self.base_parameters.copy()
            test_params[parameter_name] = param_value
            
            # Run analysis
            analyzer = EnhancedQOLAnalysis(
                starting_value=test_params['starting_value'],
                starting_age=test_params['starting_age'], 
                horizon_years=test_params['horizon_years'],
                n_simulations=test_params['n_simulations']
            )
            
            # Run simulation
            enhanced_results = analyzer.run_enhanced_simulation(
                withdrawal_strategy=test_params['withdrawal_strategy'],
                qol_variability=test_params['qol_variability'],
                return_volatility=test_params['return_volatility'],
                inflation_variability=test_params['inflation_variability'],
                verbose=False
            )
            
            # Get risk metrics
            risk_metrics = analyzer.depletion_analysis.get_risk_metrics()
            
            # Store results
            results['depletion_rates'].append(risk_metrics['depletion_rate'])
            results['final_values'].append(enhanced_results['portfolio_analysis']['final_value_mean'])
            results['survival_rates'].append(risk_metrics['survival_rate'])
            results['full_results'].append({
                'parameter_value': param_value,
                'enhanced_results': enhanced_results,
                'risk_metrics': risk_metrics
            })
            
            # Store primary metric
            if metric == 'depletion_rate':
                results['metric_values'].append(risk_metrics['depletion_rate'])
            elif metric == 'final_value_mean':
                results['metric_values'].append(enhanced_results['portfolio_analysis']['final_value_mean'])
            elif metric == 'survival_rate':
                results['metric_values'].append(risk_metrics['survival_rate'])
            else:
                results['metric_values'].append(0)  # Default
        
        if verbose:
            best_idx = self._find_optimal_index(results['metric_values'], metric)
            best_value = parameter_values[best_idx]
            best_metric = results['metric_values'][best_idx]
            print(f"✅ Optimal {parameter_name}: {best_value} (metric: {best_metric:.3f})")
        
        return results
    
    def run_two_parameter_sweep(self,
                               param1_name: str, param1_values: List[float],
                               param2_name: str, param2_values: List[float],
                               metric: str = 'depletion_rate',
                               verbose: bool = True) -> Dict[str, Any]:
        """
        Run sensitivity analysis for two parameters (creates heatmap).
        
        Args:
            param1_name: First parameter name
            param1_values: Values for first parameter
            param2_name: Second parameter name
            param2_values: Values for second parameter
            metric: Metric to analyze
            verbose: Whether to print progress
            
        Returns:
            Dictionary with 2D sweep results
        """
        if verbose:
            print(f"\nRunning 2-parameter sweep: {param1_name} vs {param2_name}")
            print(f"Grid size: {len(param1_values)} x {len(param2_values)} = {len(param1_values) * len(param2_values)} simulations")
        
        # Initialize results matrix
        metric_matrix = np.zeros((len(param2_values), len(param1_values)))
        depletion_matrix = np.zeros((len(param2_values), len(param1_values)))
        final_value_matrix = np.zeros((len(param2_values), len(param1_values)))
        
        total_combinations = len(param1_values) * len(param2_values)
        current_combination = 0
        
        # Run parameter combinations
        for i, param1_val in enumerate(param1_values):
            for j, param2_val in enumerate(param2_values):
                current_combination += 1
                if verbose and current_combination % max(1, total_combinations // 10) == 0:
                    pct_complete = 100 * current_combination / total_combinations
                    print(f"  Progress: {pct_complete:.1f}% ({current_combination}/{total_combinations})")
                
                # Create test parameters
                test_params = self.base_parameters.copy()
                test_params[param1_name] = param1_val
                test_params[param2_name] = param2_val
                
                # Run analysis
                analyzer = EnhancedQOLAnalysis(
                    starting_value=test_params['starting_value'],
                    starting_age=test_params['starting_age'],
                    horizon_years=test_params['horizon_years'],
                    n_simulations=test_params['n_simulations']
                )
                
                enhanced_results = analyzer.run_enhanced_simulation(
                    withdrawal_strategy=test_params['withdrawal_strategy'],
                    qol_variability=test_params['qol_variability'],
                    return_volatility=test_params['return_volatility'],
                    inflation_variability=test_params['inflation_variability'],
                    verbose=False
                )
                
                risk_metrics = analyzer.depletion_analysis.get_risk_metrics()
                
                # Store metrics
                depletion_matrix[j, i] = risk_metrics['depletion_rate']
                final_value_matrix[j, i] = enhanced_results['portfolio_analysis']['final_value_mean']
                
                if metric == 'depletion_rate':
                    metric_matrix[j, i] = risk_metrics['depletion_rate']
                elif metric == 'final_value_mean':
                    metric_matrix[j, i] = enhanced_results['portfolio_analysis']['final_value_mean']
                elif metric == 'survival_rate':
                    metric_matrix[j, i] = risk_metrics['survival_rate']
        
        # Find optimal combination
        optimal_idx = self._find_optimal_2d_index(metric_matrix, metric)
        optimal_param1 = param1_values[optimal_idx[1]]
        optimal_param2 = param2_values[optimal_idx[0]]
        optimal_metric = metric_matrix[optimal_idx]
        
        results = {
            'param1_name': param1_name,
            'param1_values': param1_values,
            'param2_name': param2_name,
            'param2_values': param2_values,
            'metric': metric,
            'metric_matrix': metric_matrix,
            'depletion_matrix': depletion_matrix,
            'final_value_matrix': final_value_matrix,
            'optimal_combination': {
                param1_name: optimal_param1,
                param2_name: optimal_param2,
                'metric_value': optimal_metric
            }
        }
        
        if verbose:
            print(f"✅ Optimal combination: {param1_name}={optimal_param1}, {param2_name}={optimal_param2}")
            print(f"   Metric value: {optimal_metric:.3f}")
        
        return results
    
    def run_comprehensive_sweep(self,
                              parameter_ranges: Optional[Dict[str, List]] = None,
                              max_combinations: int = 1000,
                              verbose: bool = True) -> Dict[str, Any]:
        """
        Run comprehensive multi-parameter sensitivity analysis.
        
        Args:
            parameter_ranges: Dictionary of parameter ranges to test
            max_combinations: Maximum number of combinations to test
            verbose: Whether to print progress
            
        Returns:
            Dictionary with comprehensive results
        """
        if parameter_ranges is None:
            parameter_ranges = self.parameter_ranges
        
        if not parameter_ranges:
            raise ValueError("No parameter ranges defined. Use define_parameter_ranges() first.")
        
        if verbose:
            total_combinations = np.prod([len(values) for values in parameter_ranges.values()])
            print(f"\nComprehensive sensitivity analysis:")
            print(f"Parameters: {list(parameter_ranges.keys())}")
            print(f"Total combinations: {total_combinations:,}")
            if total_combinations > max_combinations:
                print(f"Limiting to {max_combinations:,} combinations for performance")
        
        # Generate parameter combinations
        param_names = list(parameter_ranges.keys())
        param_value_lists = list(parameter_ranges.values())
        
        # Create all combinations
        all_combinations = list(product(*param_value_lists))
        
        # Limit combinations if too many
        if len(all_combinations) > max_combinations:
            # Sample random combinations
            np.random.shuffle(all_combinations)
            selected_combinations = all_combinations[:max_combinations]
        else:
            selected_combinations = all_combinations
        
        if verbose:
            print(f"Testing {len(selected_combinations):,} parameter combinations...")
        
        # Run analysis for each combination
        results = {
            'parameter_names': param_names,
            'combinations': [],
            'depletion_rates': [],
            'final_values': [],
            'survival_rates': [],
            'risk_metrics': []
        }
        
        for i, combination in enumerate(selected_combinations):
            if verbose and (i + 1) % max(1, len(selected_combinations) // 20) == 0:
                pct_complete = 100 * (i + 1) / len(selected_combinations)
                print(f"  Progress: {pct_complete:.1f}% ({i+1}/{len(selected_combinations)})")
            
            # Create test parameters
            test_params = self.base_parameters.copy()
            param_dict = dict(zip(param_names, combination))
            test_params.update(param_dict)
            
            # Run analysis
            analyzer = EnhancedQOLAnalysis(
                starting_value=test_params.get('starting_value', self.base_parameters['starting_value']),
                starting_age=test_params.get('starting_age', self.base_parameters['starting_age']),
                horizon_years=test_params.get('horizon_years', self.base_parameters['horizon_years']),
                n_simulations=test_params.get('n_simulations', self.base_parameters['n_simulations'])
            )
            
            enhanced_results = analyzer.run_enhanced_simulation(
                withdrawal_strategy=test_params.get('withdrawal_strategy', 'hauenstein'),
                qol_variability=test_params.get('qol_variability', True),
                return_volatility=test_params.get('return_volatility', 0.15),
                inflation_variability=test_params.get('inflation_variability', True),
                verbose=False
            )
            
            risk_metrics = analyzer.depletion_analysis.get_risk_metrics()
            
            # Store results
            results['combinations'].append(param_dict)
            results['depletion_rates'].append(risk_metrics['depletion_rate'])
            results['final_values'].append(enhanced_results['portfolio_analysis']['final_value_mean'])
            results['survival_rates'].append(risk_metrics['survival_rate'])
            results['risk_metrics'].append(risk_metrics)
        
        # Find optimal combinations
        results['optimal_for_depletion'] = self._find_optimal_combination(
            results, 'depletion_rates', 'minimize'
        )
        results['optimal_for_final_value'] = self._find_optimal_combination(
            results, 'final_values', 'maximize'
        )
        results['optimal_for_survival'] = self._find_optimal_combination(
            results, 'survival_rates', 'maximize'
        )
        
        if verbose:
            print(f"✅ Comprehensive analysis complete!")
            print("Optimal combinations:")
            for objective, optimal in [
                ('Minimize Depletion', results['optimal_for_depletion']),
                ('Maximize Final Value', results['optimal_for_final_value']),
                ('Maximize Survival', results['optimal_for_survival'])
            ]:
                print(f"  {objective}: {optimal['parameters']} → {optimal['metric_value']:.3f}")
        
        return results
    
    def _find_optimal_index(self, values: List[float], metric: str) -> int:
        """Find index of optimal value based on metric type."""
        if metric in ['depletion_rate']:
            return np.argmin(values)  # Minimize depletion rate
        else:
            return np.argmax(values)  # Maximize other metrics
    
    def _find_optimal_2d_index(self, matrix: np.ndarray, metric: str) -> Tuple[int, int]:
        """Find 2D index of optimal value based on metric type."""
        if metric in ['depletion_rate']:
            return np.unravel_index(np.argmin(matrix), matrix.shape)
        else:
            return np.unravel_index(np.argmax(matrix), matrix.shape)
    
    def _find_optimal_combination(self, results: Dict, metric_key: str, objective: str) -> Dict:
        """Find optimal parameter combination for given objective."""
        values = results[metric_key]
        if objective == 'minimize':
            optimal_idx = np.argmin(values)
        else:
            optimal_idx = np.argmax(values)
        
        return {
            'parameters': results['combinations'][optimal_idx],
            'metric_value': values[optimal_idx],
            'index': optimal_idx
        }
    
    def plot_single_parameter_sensitivity(self,
                                        sweep_results: Dict[str, Any],
                                        save_path: Optional[str] = None,
                                        figsize: Tuple[int, int] = (12, 8)) -> plt.Figure:
        """Plot single parameter sensitivity results."""
        fig, axes = plt.subplots(2, 2, figsize=figsize)
        
        param_name = sweep_results['parameter_name']
        param_values = sweep_results['parameter_values']
        
        # 1. Primary metric
        ax1 = axes[0, 0]
        ax1.plot(param_values, sweep_results['metric_values'], 'bo-', linewidth=2, markersize=6)
        ax1.set_title(f'{sweep_results["metric"].title()} Sensitivity')
        ax1.set_xlabel(param_name)
        ax1.set_ylabel(sweep_results["metric"].replace('_', ' ').title())
        ax1.grid(True, alpha=0.3)
        
        # 2. Depletion rate
        ax2 = axes[0, 1]
        ax2.plot(param_values, sweep_results['depletion_rates'], 'ro-', linewidth=2, markersize=6)
        ax2.set_title('Depletion Rate Sensitivity')
        ax2.set_xlabel(param_name)
        ax2.set_ylabel('Depletion Rate')
        ax2.grid(True, alpha=0.3)
        
        # 3. Final values
        ax3 = axes[1, 0]
        ax3.plot(param_values, sweep_results['final_values'], 'go-', linewidth=2, markersize=6)
        ax3.set_title('Final Portfolio Value Sensitivity')
        ax3.set_xlabel(param_name)
        ax3.set_ylabel('Final Value ($)')
        ax3.grid(True, alpha=0.3)
        
        # 4. Survival rate
        ax4 = axes[1, 1]
        ax4.plot(param_values, sweep_results['survival_rates'], 'mo-', linewidth=2, markersize=6)
        ax4.set_title('Survival Rate Sensitivity')
        ax4.set_xlabel(param_name)
        ax4.set_ylabel('Survival Rate')
        ax4.grid(True, alpha=0.3)
        
        plt.suptitle(f'Parameter Sensitivity Analysis: {param_name}', fontsize=14)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def plot_two_parameter_heatmap(self,
                                  sweep_results: Dict[str, Any],
                                  save_path: Optional[str] = None,
                                  figsize: Tuple[int, int] = (15, 5)) -> plt.Figure:
        """Plot 2-parameter sensitivity heatmaps."""
        fig, axes = plt.subplots(1, 3, figsize=figsize)
        
        param1_name = sweep_results['param1_name']
        param2_name = sweep_results['param2_name']
        param1_values = sweep_results['param1_values']
        param2_values = sweep_results['param2_values']
        
        # 1. Depletion rate heatmap
        ax1 = axes[0]
        sns.heatmap(sweep_results['depletion_matrix'], 
                   xticklabels=[f'{v:.2f}' for v in param1_values],
                   yticklabels=[f'{v:.2f}' for v in param2_values],
                   annot=True, fmt='.3f', cmap='RdYlBu_r', ax=ax1)
        ax1.set_title('Depletion Rate')
        ax1.set_xlabel(param1_name)
        ax1.set_ylabel(param2_name)
        
        # 2. Final value heatmap
        ax2 = axes[1]
        sns.heatmap(sweep_results['final_value_matrix'], 
                   xticklabels=[f'{v:.2f}' for v in param1_values],
                   yticklabels=[f'{v:.2f}' for v in param2_values],
                   annot=True, fmt='.0f', cmap='YlOrRd', ax=ax2)
        ax2.set_title('Final Portfolio Value')
        ax2.set_xlabel(param1_name)
        ax2.set_ylabel(param2_name)
        
        # 3. Primary metric heatmap
        ax3 = axes[2]
        cmap = 'RdYlBu_r' if sweep_results['metric'] == 'depletion_rate' else 'YlOrRd'
        sns.heatmap(sweep_results['metric_matrix'],
                   xticklabels=[f'{v:.2f}' for v in param1_values],
                   yticklabels=[f'{v:.2f}' for v in param2_values],
                   annot=True, fmt='.3f', cmap=cmap, ax=ax3)
        ax3.set_title(f'{sweep_results["metric"].title()}')
        ax3.set_xlabel(param1_name)
        ax3.set_ylabel(param2_name)
        
        plt.suptitle(f'2-Parameter Sensitivity: {param1_name} vs {param2_name}', fontsize=14)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def generate_sensitivity_report(self, results: Dict[str, Any]) -> str:
        """Generate comprehensive sensitivity analysis report."""
        report = "QOL FRAMEWORK SENSITIVITY ANALYSIS REPORT\n"
        report += "=" * 50 + "\n\n"
        
        # Analysis overview
        if 'parameter_names' in results:  # Comprehensive analysis
            report += "COMPREHENSIVE SENSITIVITY ANALYSIS\n"
            report += f"Parameters analyzed: {', '.join(results['parameter_names'])}\n"
            report += f"Combinations tested: {len(results['combinations']):,}\n\n"
            
            # Optimal combinations
            report += "OPTIMAL PARAMETER COMBINATIONS:\n\n"
            
            objectives = [
                ('Minimize Depletion Risk', results['optimal_for_depletion']),
                ('Maximize Final Portfolio Value', results['optimal_for_final_value']),  
                ('Maximize Survival Rate', results['optimal_for_survival'])
            ]
            
            for objective_name, optimal in objectives:
                report += f"{objective_name}:\n"
                for param, value in optimal['parameters'].items():
                    report += f"  • {param}: {value}\n"
                report += f"  Result: {optimal['metric_value']:.3f}\n\n"
            
            # Statistical summary
            report += "SENSITIVITY STATISTICS:\n"
            depletion_stats = self._calculate_stats(results['depletion_rates'])
            final_value_stats = self._calculate_stats(results['final_values'])
            
            report += f"Depletion Rate Range: {depletion_stats['min']:.3f} - {depletion_stats['max']:.3f}\n"
            report += f"Depletion Rate Std Dev: {depletion_stats['std']:.3f}\n"
            report += f"Final Value Range: ${final_value_stats['min']:,.0f} - ${final_value_stats['max']:,.0f}\n"
            report += f"Final Value Std Dev: ${final_value_stats['std']:,.0f}\n\n"
            
        else:  # Single or two-parameter analysis
            if 'param1_name' in results:  # Two parameter
                report += f"TWO-PARAMETER SENSITIVITY ANALYSIS\n"
                report += f"Parameters: {results['param1_name']} vs {results['param2_name']}\n"
                report += f"Grid size: {len(results['param1_values'])} x {len(results['param2_values'])}\n\n"
                
                optimal = results['optimal_combination']
                report += "OPTIMAL COMBINATION:\n"
                report += f"• {results['param1_name']}: {optimal[results['param1_name']]}\n"
                report += f"• {results['param2_name']}: {optimal[results['param2_name']]}\n"
                report += f"• {results['metric']}: {optimal['metric_value']:.3f}\n\n"
                
            else:  # Single parameter
                report += f"SINGLE PARAMETER SENSITIVITY ANALYSIS\n"
                report += f"Parameter: {results['parameter_name']}\n"
                report += f"Values tested: {len(results['parameter_values'])}\n\n"
                
                optimal_idx = self._find_optimal_index(results['metric_values'], results['metric'])
                optimal_value = results['parameter_values'][optimal_idx]
                optimal_metric = results['metric_values'][optimal_idx]
                
                report += "OPTIMAL VALUE:\n"
                report += f"• {results['parameter_name']}: {optimal_value}\n"
                report += f"• {results['metric']}: {optimal_metric:.3f}\n\n"
        
        # Recommendations
        report += "RECOMMENDATIONS:\n"
        report += self._generate_recommendations(results)
        
        return report
    
    def _calculate_stats(self, values: List[float]) -> Dict[str, float]:
        """Calculate basic statistics for a list of values."""
        return {
            'min': np.min(values),
            'max': np.max(values),
            'mean': np.mean(values),
            'median': np.median(values),
            'std': np.std(values)
        }
    
    def _generate_recommendations(self, results: Dict[str, Any]) -> str:
        """Generate parameter optimization recommendations."""
        recommendations = ""
        
        if 'parameter_names' in results:  # Comprehensive analysis
            # Find most sensitive parameters
            depletion_range = np.max(results['depletion_rates']) - np.min(results['depletion_rates'])
            final_value_range = np.max(results['final_values']) - np.min(results['final_values'])
            
            recommendations += f"• Parameter sensitivity analysis shows {depletion_range:.3f} range in depletion rates\n"
            recommendations += f"• Final portfolio values vary by ${final_value_range:,.0f}\n"
            
            # Optimal parameters
            optimal_depletion = results['optimal_for_depletion']['parameters']
            recommendations += "• For minimum risk, prioritize parameters:\n"
            for param, value in optimal_depletion.items():
                recommendations += f"  - {param}: {value}\n"
                
        else:
            recommendations += "• Single/two-parameter analysis completed\n"
            recommendations += "• Use optimal values identified for best results\n"
            
        recommendations += "• Consider running comprehensive analysis for full parameter optimization\n"
        
        return recommendations