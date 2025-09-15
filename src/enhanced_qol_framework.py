"""
Enhanced QOL Framework with Depletion Analysis Integration

This module extends the original QOL framework with comprehensive depletion analysis,
detailed simulation tracking, and enhanced risk assessment capabilities.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple, Optional, Any
import warnings
warnings.filterwarnings('ignore')

# Import the original framework and depletion analysis
from qol_framework import HypotheticalPortfolioQOLAnalysis
from depletion_analysis import PortfolioDepletionAnalysis


class EnhancedQOLAnalysis:
    """
    Enhanced QOL analysis with integrated depletion tracking and comprehensive risk assessment.
    
    This class extends the original QOL framework by:
    - Tracking detailed simulation paths with age-by-age portfolio evolution
    - Integrating comprehensive depletion analysis
    - Providing enhanced risk metrics and survival analysis  
    - Supporting parameter variability and sensitivity analysis
    """
    
    def __init__(self, 
                 starting_value: float = 1000000,
                 starting_age: int = 65,
                 horizon_years: int = 30,
                 n_simulations: int = 1000,
                 qol_phase1_rate: float = 0.054,
                 qol_phase2_rate: float = 0.045,
                 qol_phase3_rate: float = 0.035):
        """
        Initialize enhanced QOL analysis.
        
        Args:
            starting_value: Initial portfolio value
            starting_age: Starting age (retirement age)
            horizon_years: Number of years to simulate
            n_simulations: Number of Monte Carlo simulation paths
            qol_phase1_rate: Withdrawal rate for Phase 1 (years 0-9)
            qol_phase2_rate: Withdrawal rate for Phase 2 (years 10-19)
            qol_phase3_rate: Withdrawal rate for Phase 3 (years 20+)
        """
        self.starting_value = starting_value
        self.starting_age = starting_age
        self.horizon_years = horizon_years
        self.n_simulations = n_simulations
        
        # QOL withdrawal rate parameters
        self.qol_phase1_rate = qol_phase1_rate
        self.qol_phase2_rate = qol_phase2_rate
        self.qol_phase3_rate = qol_phase3_rate
        
        # Initialize original framework
        self.qol_framework = HypotheticalPortfolioQOLAnalysis()
        
        # Results storage
        self.simulation_results = {}
        self.depletion_analysis = None
        self.enhanced_results = {}
        
    def run_enhanced_simulation(self, 
                              withdrawal_strategy: str = 'hauenstein',
                              qol_variability: bool = True,
                              return_volatility: float = 0.15,
                              inflation_variability: bool = True,
                              base_real_return: float = None,
                              base_inflation: float = None,
                              verbose: bool = True) -> Dict[str, Any]:
        """
        Run enhanced Monte Carlo simulation with detailed tracking.
        
        Args:
            withdrawal_strategy: Strategy to use ('hauenstein', 'fixed_4pct', etc.)
            qol_variability: Whether to add variability to QOL adjustments
            return_volatility: Annual return volatility 
            inflation_variability: Whether to vary inflation rates
            base_real_return: Override default real return (for testing)
            base_inflation: Override default inflation (for testing)
            verbose: Whether to print progress updates
            
        Returns:
            Dictionary with comprehensive simulation results
        """
        if verbose:
            print(f"Running enhanced simulation with {self.n_simulations:,} paths...")
            
        # Storage for detailed results
        detailed_paths = {
            'portfolio_paths': [],      # Portfolio value each year for each simulation
            'qol_paths': [],           # QOL value each year for each simulation  
            'withdrawal_paths': [],     # Withdrawal amounts each year
            'age_paths': [],           # Ages corresponding to each year
            'allocation_paths': [],     # Asset allocation each year
            'return_paths': [],        # Annual returns for each simulation
            'inflation_paths': []      # Inflation rates for each simulation
        }
        
        # Run individual simulations
        for sim_idx in range(self.n_simulations):
            if verbose and (sim_idx + 1) % 200 == 0:
                print(f"  Completed {sim_idx + 1:,} of {self.n_simulations:,} simulations...")
                
            # Run single simulation path
            path_results = self._run_single_enhanced_path(
                sim_idx, withdrawal_strategy, qol_variability, 
                return_volatility, inflation_variability,
                base_real_return, base_inflation
            )
            
            # Store detailed path data
            detailed_paths['portfolio_paths'].append(path_results['portfolio_path'])
            detailed_paths['qol_paths'].append(path_results['qol_path'])
            detailed_paths['withdrawal_paths'].append(path_results['withdrawal_path'])
            detailed_paths['age_paths'].append(path_results['age_path'])
            detailed_paths['allocation_paths'].append(path_results['allocation_path'])
            detailed_paths['return_paths'].append(path_results['return_path'])
            detailed_paths['inflation_paths'].append(path_results['inflation_path'])
        
        # Store results
        self.simulation_results = detailed_paths
        
        # Create comprehensive results dictionary
        self.enhanced_results = self._compile_enhanced_results()
        
        # Initialize depletion analysis
        self.depletion_analysis = PortfolioDepletionAnalysis(
            self.simulation_results, 
            retirement_age=self.starting_age
        )
        
        if verbose:
            print(f"✅ Enhanced simulation complete!")
            print(f"   Depletion rate: {self.depletion_analysis.get_risk_metrics()['depletion_rate']:.1%}")
        
        return self.enhanced_results
    
    def _run_single_enhanced_path(self, 
                                 sim_idx: int,
                                 withdrawal_strategy: str,
                                 qol_variability: bool,
                                 return_volatility: float,
                                 inflation_variability: bool,
                                 base_real_return: float = None,
                                 base_inflation: float = None) -> Dict[str, List]:
        """Run a single simulation path with detailed tracking."""
        
        # Initialize path storage
        portfolio_path = [self.starting_value]
        qol_path = []
        withdrawal_path = []
        age_path = list(range(self.starting_age, self.starting_age + self.horizon_years))
        allocation_path = []
        return_path = []
        inflation_path = []
        
        # Set random seed for reproducible results within simulation
        np.random.seed(42 + sim_idx)
        
        # Initialize variables
        current_portfolio = self.starting_value
        current_age = self.starting_age
        cumulative_inflation_factor = 1.0  # Track cumulative inflation for Trinity Study
        
        # Generate inflation and return scenarios
        if base_inflation is None:
            base_inflation = 0.025  # 2.5% base inflation
        
        # Use realistic market assumptions (unless overridden for testing)
        if base_real_return is None:
            # Nominal returns: Stocks ~7%, Bonds ~4%
            # Real returns after inflation: Stocks ~4.5%, Bonds ~1.5%
            # For blended portfolio (declining equity allocation), expect ~1-3% real returns
            base_real_return = 0.015  # 1.5% average real return (more conservative/realistic)
        
        for year in range(self.horizon_years):
            current_age = self.starting_age + year
            
            # Generate market conditions
            if inflation_variability:
                annual_inflation = np.random.normal(base_inflation, 0.01)
            else:
                annual_inflation = base_inflation
                
            annual_return = np.random.normal(base_real_return, return_volatility)
            
            # Get dynamic asset allocation (from original framework)
            allocation = self.qol_framework.get_allocation(current_age)
            
            # Calculate QOL adjustment with optional variability
            if withdrawal_strategy == 'hauenstein':
                qol_adjustment = self.qol_framework.qol_function(year)
                if qol_variability:
                    # Add 10% variability to QOL adjustment
                    variability = np.random.normal(1.0, 0.1)
                    qol_adjustment *= max(0.5, min(1.5, variability))  # Clamp between 50%-150%
            else:
                qol_adjustment = 1.0  # No QOL adjustment for other strategies
            
            # Calculate withdrawal based on strategy
            if withdrawal_strategy == 'hauenstein':
                # QOL Framework: Trinity Study base with QOL multipliers
                # Start with Trinity's 4% of initial value, inflation-adjusted
                base_trinity_withdrawal = self.starting_value * 0.04 * cumulative_inflation_factor
                qol_multiplier = self._get_qol_multiplier(year)
                withdrawal_amount = base_trinity_withdrawal * qol_multiplier * qol_adjustment
                # Update cumulative inflation factor AFTER withdrawal calculation
                cumulative_inflation_factor *= (1 + annual_inflation)
            elif withdrawal_strategy == 'custom':
                # QOL Framework: Trinity Study base with QOL multipliers (same as hauenstein)
                base_trinity_withdrawal = self.starting_value * 0.04 * cumulative_inflation_factor
                qol_multiplier = self._get_qol_multiplier(year)
                withdrawal_amount = base_trinity_withdrawal * qol_multiplier * qol_adjustment
                # Update cumulative inflation factor AFTER withdrawal calculation
                cumulative_inflation_factor *= (1 + annual_inflation)
            elif withdrawal_strategy == 'trinity_4pct':
                # Trinity Study: Fixed 4% of initial value, adjusted for cumulative inflation
                base_withdrawal = self.starting_value * 0.04
                withdrawal_amount = base_withdrawal * cumulative_inflation_factor
                # Update cumulative inflation factor AFTER withdrawal calculation
                cumulative_inflation_factor *= (1 + annual_inflation)
            elif withdrawal_strategy == 'fixed_4pct':
                withdrawal_amount = self.starting_value * 0.04  # Fixed 4% of initial (no inflation adjustment)
            elif withdrawal_strategy == 'dynamic_4pct':
                withdrawal_amount = current_portfolio * 0.04   # 4% of current portfolio
            else:
                withdrawal_amount = current_portfolio * 0.04   # Default to 4%
            
            # Apply market returns
            pre_withdrawal_value = current_portfolio * (1 + annual_return)
            
            # Subtract withdrawal
            post_withdrawal_value = max(0, pre_withdrawal_value - withdrawal_amount)
            
            # Store path data
            portfolio_path.append(post_withdrawal_value)
            qol_path.append(qol_adjustment)
            withdrawal_path.append(withdrawal_amount)
            allocation_path.append(allocation)
            return_path.append(annual_return)
            inflation_path.append(annual_inflation)
            
            # Update for next year
            current_portfolio = post_withdrawal_value
            
            # If portfolio is depleted, set remaining values to zero
            if current_portfolio <= 0:
                remaining_years = self.horizon_years - year - 1
                portfolio_path.extend([0] * remaining_years)
                qol_path.extend([0] * remaining_years)
                withdrawal_path.extend([0] * remaining_years)
                allocation_path.extend([allocation] * remaining_years)
                return_path.extend([0] * remaining_years)
                inflation_path.extend([annual_inflation] * remaining_years)
                break
        
        return {
            'portfolio_path': portfolio_path,
            'qol_path': qol_path,
            'withdrawal_path': withdrawal_path,
            'age_path': age_path,
            'allocation_path': allocation_path,
            'return_path': return_path,
            'inflation_path': inflation_path
        }
    
    def _get_qol_multiplier(self, year: int) -> float:
        """
        Get QOL multiplier for Trinity Study base withdrawal.
        
        These multipliers are designed to redistribute Trinity Study's total expected
        income across years based on QOL preferences:
        - Phase 1 (Years 0-9): Higher withdrawal (overweight early high-QOL years)
        - Phase 2 (Years 10-19): Moderate withdrawal 
        - Phase 3 (Years 20+): Lower withdrawal (underweight low-QOL years)
        
        The multipliers are calculated to maintain approximately the same total
        expected income as Trinity Study over the full retirement horizon.
        """
        if year < 10:
            # Phase 1: Convert 5.4% rate to Trinity multiplier
            # 5.4% vs 4.0% base = 1.35x multiplier
            return self.qol_phase1_rate / 0.04
        elif year < 20:
            # Phase 2: Convert 4.5% rate to Trinity multiplier  
            # 4.5% vs 4.0% base = 1.125x multiplier
            return self.qol_phase2_rate / 0.04
        else:
            # Phase 3: Convert 3.5% rate to Trinity multiplier
            # 3.5% vs 4.0% base = 0.875x multiplier
            return self.qol_phase3_rate / 0.04
    
    def _compile_enhanced_results(self) -> Dict[str, Any]:
        """Compile comprehensive simulation results."""
        portfolio_paths = np.array(self.simulation_results['portfolio_paths'])
        qol_paths = np.array(self.simulation_results['qol_paths'])
        withdrawal_paths = np.array(self.simulation_results['withdrawal_paths'])
        
        # Final values analysis
        final_values = portfolio_paths[:, -1]
        
        # Calculate success rates for different scenarios
        success_rates = {
            'never_depleted': np.mean(final_values > 0),
            'value_at_90': np.mean(portfolio_paths[:, min(25, portfolio_paths.shape[1]-1)] > 0) if portfolio_paths.shape[1] > 25 else 0,
            'value_at_85': np.mean(portfolio_paths[:, min(20, portfolio_paths.shape[1]-1)] > 0) if portfolio_paths.shape[1] > 20 else 0,
            'value_at_80': np.mean(portfolio_paths[:, min(15, portfolio_paths.shape[1]-1)] > 0) if portfolio_paths.shape[1] > 15 else 0,
        }
        
        # Withdrawal sustainability analysis
        total_withdrawals = np.sum(withdrawal_paths, axis=1)
        
        # Comprehensive statistics
        enhanced_results = {
            'simulation_metadata': {
                'n_simulations': self.n_simulations,
                'starting_value': self.starting_value,
                'starting_age': self.starting_age,
                'horizon_years': self.horizon_years,
                'simulation_type': 'enhanced_qol'
            },
            'portfolio_analysis': {
                'final_value_mean': np.mean(final_values),
                'final_value_median': np.median(final_values),
                'final_value_std': np.std(final_values),
                'final_value_percentiles': {
                    '5th': np.percentile(final_values, 5),
                    '25th': np.percentile(final_values, 25),
                    '75th': np.percentile(final_values, 75),
                    '95th': np.percentile(final_values, 95)
                }
            },
            'success_rates': success_rates,
            'withdrawal_analysis': {
                'total_withdrawals_mean': np.mean(total_withdrawals),
                'total_withdrawals_median': np.median(total_withdrawals),
                'average_annual_withdrawal': np.mean(withdrawal_paths),
                'withdrawal_variability': np.std(withdrawal_paths)
            },
            'qol_analysis': {
                'average_qol_adjustment': np.mean(qol_paths),
                'qol_variability': np.std(qol_paths),
                'max_qol_adjustment': np.max(qol_paths),
                'min_qol_adjustment': np.min(qol_paths)
            },
            'simulation_paths': {
                'portfolio_paths': self.simulation_results['portfolio_paths'],
                'qol_paths': self.simulation_results['qol_paths'],
                'withdrawal_paths': self.simulation_results['withdrawal_paths'],
                'age_paths': self.simulation_results['age_paths'][0]  # Same for all simulations
            }
        }
        
        return enhanced_results
    
    def get_comprehensive_analysis(self) -> Dict[str, Any]:
        """
        Get comprehensive analysis including depletion analysis.
        
        Returns:
            Dictionary with all analysis results
        """
        if not self.simulation_results:
            raise ValueError("No simulation results available. Run enhanced simulation first.")
            
        if self.depletion_analysis is None:
            self.depletion_analysis = PortfolioDepletionAnalysis(
                self.simulation_results,
                retirement_age=self.starting_age
            )
        
        return {
            'enhanced_qol_results': self.enhanced_results,
            'depletion_analysis': self.depletion_analysis.to_dict(),
            'combined_summary': self._generate_combined_summary()
        }
    
    def _generate_combined_summary(self) -> str:
        """Generate combined summary of QOL and depletion analysis."""
        if not self.depletion_analysis:
            return "No depletion analysis available."
            
        risk_metrics = self.depletion_analysis.get_risk_metrics()
        enhanced_results = self.enhanced_results
        
        summary = "ENHANCED QOL FRAMEWORK - COMPREHENSIVE ANALYSIS\n"
        summary += "=" * 60 + "\n\n"
        
        # Portfolio Analysis
        summary += "PORTFOLIO PERFORMANCE:\n"
        summary += f"• Starting Value: ${self.starting_value:,.0f}\n"
        summary += f"• Final Value (Mean): ${enhanced_results['portfolio_analysis']['final_value_mean']:,.0f}\n"
        summary += f"• Final Value (Median): ${enhanced_results['portfolio_analysis']['final_value_median']:,.0f}\n"
        summary += f"• Success Rate (Never Depleted): {enhanced_results['success_rates']['never_depleted']:.1%}\n\n"
        
        # Depletion Risk Analysis  
        summary += "DEPLETION RISK ASSESSMENT:\n"
        summary += f"• Overall Depletion Risk: {risk_metrics['depletion_rate']:.1%}\n"
        summary += f"• Survival Rate: {risk_metrics['survival_rate']:.1%}\n"
        if risk_metrics['depleted_simulations'] > 0:
            summary += f"• Mean Depletion Age: {risk_metrics['mean_depletion_age']:.1f}\n"
            summary += f"• 5% Worst Case: Age {risk_metrics['var_95_age']:.0f}\n"
        summary += "\n"
        
        # QOL Analysis
        summary += "QOL FRAMEWORK ANALYSIS:\n"
        summary += f"• Average QOL Adjustment: {enhanced_results['qol_analysis']['average_qol_adjustment']:.3f}\n"
        summary += f"• QOL Variability (Std Dev): {enhanced_results['qol_analysis']['qol_variability']:.3f}\n"
        summary += f"• Total Withdrawals (Mean): ${enhanced_results['withdrawal_analysis']['total_withdrawals_mean']:,.0f}\n\n"
        
        # Longevity Analysis
        summary += "LONGEVITY ANALYSIS:\n"
        summary += f"• Survival to Age 80: {risk_metrics['survival_at_80']:.1%}\n"
        summary += f"• Survival to Age 90: {risk_metrics['survival_at_90']:.1%}\n"
        summary += f"• Survival to Age 100: {risk_metrics['survival_at_100']:.1%}\n\n"
        
        # Recommendations
        summary += "FRAMEWORK RECOMMENDATIONS:\n"
        if risk_metrics['depletion_rate'] > 0.15:
            summary += "• HIGH RISK: Consider reducing QOL adjustments or withdrawal rates\n"
        elif risk_metrics['depletion_rate'] > 0.1:
            summary += "• MODERATE RISK: Monitor closely and consider strategy adjustments\n" 
        else:
            summary += "• LOW RISK: Framework parameters appear sustainable\n"
            
        if enhanced_results['qol_analysis']['qol_variability'] > 0.2:
            summary += "• High QOL variability detected - consider constraints\n"
            
        return summary
    
    def plot_enhanced_analysis(self, save_path: Optional[str] = None, figsize: Tuple[int, int] = (15, 10)) -> plt.Figure:
        """
        Create comprehensive visualization of enhanced analysis results.
        
        Args:
            save_path: Optional path to save the plot
            figsize: Figure size tuple
            
        Returns:
            Matplotlib figure object
        """
        if not self.simulation_results:
            raise ValueError("No simulation results available. Run enhanced simulation first.")
            
        fig, axes = plt.subplots(2, 3, figsize=figsize)
        
        portfolio_paths = np.array(self.simulation_results['portfolio_paths'])
        ages = self.simulation_results['age_paths'][0]
        
        # Ensure arrays have matching dimensions
        min_length = min(len(ages), portfolio_paths.shape[1])
        ages = ages[:min_length]
        portfolio_paths = portfolio_paths[:, :min_length]
        
        # 1. Portfolio evolution paths
        ax1 = axes[0, 0]
        for i in range(min(50, len(portfolio_paths))):  # Show first 50 paths
            ax1.plot(ages, portfolio_paths[i], alpha=0.1, color='blue')
        
        # Add percentile bands
        p10 = np.percentile(portfolio_paths, 10, axis=0)
        p50 = np.percentile(portfolio_paths, 50, axis=0)  
        p90 = np.percentile(portfolio_paths, 90, axis=0)
        
        ax1.plot(ages, p10, 'r--', linewidth=2, label='10th percentile')
        ax1.plot(ages, p50, 'g-', linewidth=2, label='Median')
        ax1.plot(ages, p90, 'b--', linewidth=2, label='90th percentile')
        
        ax1.set_title('Portfolio Evolution Paths')
        ax1.set_xlabel('Age')
        ax1.set_ylabel('Portfolio Value ($)')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. Survival curve
        ax2 = axes[0, 1]
        if self.depletion_analysis:
            self.depletion_analysis.plot_survival_curve(save_path=None, figsize=(6, 4))
            # Copy the survival curve plot
            survival_ages = self.depletion_analysis.survival_data['ages']
            survival_probs = self.depletion_analysis.survival_data['survival_probabilities']
            ax2.plot(survival_ages, survival_probs, 'b-', linewidth=2)
            ax2.set_title('Portfolio Survival Probability')
            ax2.set_xlabel('Age')
            ax2.set_ylabel('Survival Probability')
            ax2.grid(True, alpha=0.3)
        
        # 3. Final value distribution
        ax3 = axes[0, 2]
        final_values = portfolio_paths[:, -1]
        ax3.hist(final_values, bins=50, alpha=0.7, color='green', edgecolor='black')
        ax3.axvline(np.mean(final_values), color='red', linestyle='--', linewidth=2, label=f'Mean: ${np.mean(final_values):,.0f}')
        ax3.set_title('Final Portfolio Value Distribution')
        ax3.set_xlabel('Final Value ($)')
        ax3.set_ylabel('Number of Simulations')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # 4. QOL adjustments
        ax4 = axes[1, 0]
        qol_paths = np.array(self.simulation_results['qol_paths'])
        # Ensure QOL paths match the age dimension
        qol_paths = qol_paths[:, :min_length]
        qol_mean = np.mean(qol_paths, axis=0)
        years = np.arange(len(qol_mean))
        ax4.plot(years, qol_mean, 'purple', linewidth=2)
        ax4.fill_between(years, 
                        np.percentile(qol_paths, 25, axis=0),
                        np.percentile(qol_paths, 75, axis=0),
                        alpha=0.3, color='purple')
        ax4.set_title('QOL Adjustments Over Time')
        ax4.set_xlabel('Years from Retirement')
        ax4.set_ylabel('QOL Adjustment Factor')
        ax4.grid(True, alpha=0.3)
        
        # 5. Annual withdrawals
        ax5 = axes[1, 1]
        withdrawal_paths = np.array(self.simulation_results['withdrawal_paths'])
        # Ensure withdrawal paths match the age dimension
        withdrawal_paths = withdrawal_paths[:, :min_length]
        withdrawal_mean = np.mean(withdrawal_paths, axis=0)
        ax5.plot(years, withdrawal_mean, 'orange', linewidth=2)
        ax5.fill_between(years,
                        np.percentile(withdrawal_paths, 25, axis=0),
                        np.percentile(withdrawal_paths, 75, axis=0),
                        alpha=0.3, color='orange')
        ax5.set_title('Annual Withdrawals Over Time')
        ax5.set_xlabel('Years from Retirement')
        ax5.set_ylabel('Annual Withdrawal ($)')
        ax5.grid(True, alpha=0.3)
        
        # 6. Depletion histogram
        ax6 = axes[1, 2]
        if self.depletion_analysis:
            depletion_ages = self.depletion_analysis.depletion_data['depletion_ages']
            finite_ages = depletion_ages[np.isfinite(depletion_ages)]
            
            if len(finite_ages) > 0:
                ax6.hist(finite_ages, bins=20, alpha=0.7, color='red', edgecolor='black')
                ax6.axvline(np.mean(finite_ages), color='blue', linestyle='--', linewidth=2, 
                           label=f'Mean: {np.mean(finite_ages):.1f}')
                ax6.set_title('Depletion Age Distribution')
                ax6.set_xlabel('Age at Depletion')
                ax6.set_ylabel('Number of Simulations')
                ax6.legend()
            else:
                ax6.text(0.5, 0.5, 'No Depletions\nOccurred', ha='center', va='center', 
                        transform=ax6.transAxes, fontsize=12)
                ax6.set_title('Depletion Analysis')
        
        ax6.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def compare_strategies(self, strategies: List[str], **simulation_kwargs) -> Dict[str, Any]:
        """
        Compare multiple withdrawal strategies using enhanced analysis.
        
        Args:
            strategies: List of strategy names to compare
            **simulation_kwargs: Additional simulation parameters
            
        Returns:
            Dictionary with comparison results
        """
        comparison_results = {}
        
        for strategy in strategies:
            print(f"\nRunning enhanced simulation for strategy: {strategy}")
            
            # Run simulation for this strategy
            results = self.run_enhanced_simulation(
                withdrawal_strategy=strategy,
                verbose=False,
                **simulation_kwargs
            )
            
            # Store results
            comparison_results[strategy] = {
                'enhanced_results': results,
                'depletion_analysis': self.depletion_analysis.to_dict(),
                'risk_summary': {
                    'depletion_rate': self.depletion_analysis.get_risk_metrics()['depletion_rate'],
                    'final_value_mean': results['portfolio_analysis']['final_value_mean'],
                    'success_rate': results['success_rates']['never_depleted'],
                    'survival_at_90': self.depletion_analysis.get_risk_metrics()['survival_at_90']
                }
            }
        
        return comparison_results


# Alias for backwards compatibility
EnhancedQOLFramework = EnhancedQOLAnalysis