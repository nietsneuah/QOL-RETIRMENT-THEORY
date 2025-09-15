"""
Portfolio Depletion Analysis Module

This module provides comprehensive analysis of portfolio depletion timelines,
including percentile analysis, survival curves, and risk metrics for retirement planning.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

class PortfolioDepletionAnalysis:
    """
    Comprehensive analysis of portfolio depletion patterns and timelines.
    
    This class analyzes simulation results to provide detailed insights into:
    - Portfolio depletion timelines across percentiles
    - Survival probability curves
    - Risk metrics and statistics
    - Age-specific depletion probabilities
    """
    
    def __init__(self, simulation_results: Dict, retirement_age: int = 65):
        """
        Initialize depletion analysis with simulation results.
        
        Args:
            simulation_results: Dictionary containing simulation data with portfolio values
            retirement_age: Age at retirement start (default 65)
        """
        self.simulation_results = simulation_results
        self.retirement_age = retirement_age
        self.depletion_data = {}
        self.survival_data = {}
        self._analyze_depletion()
    
    def _analyze_depletion(self):
        """Perform comprehensive depletion analysis on simulation results."""
        portfolio_paths = self.simulation_results.get('portfolio_paths', [])
        qol_paths = self.simulation_results.get('qol_paths', [])
        
        if not portfolio_paths:
            raise ValueError("No portfolio paths found in simulation results")
        
        n_simulations = len(portfolio_paths)
        n_years = len(portfolio_paths[0])
        
        # Track depletion for each simulation
        depletion_years = []  # Years until depletion (np.inf if never depleted)
        depletion_ages = []   # Age at depletion (np.inf if never depleted)
        
        for sim_idx, portfolio_path in enumerate(portfolio_paths):
            # Find first year where portfolio hits zero or negative
            depletion_year = None
            for year_idx, value in enumerate(portfolio_path):
                if value <= 0:
                    depletion_year = year_idx
                    break
            
            if depletion_year is not None:
                depletion_years.append(depletion_year)
                depletion_ages.append(self.retirement_age + depletion_year)
            else:
                depletion_years.append(np.inf)
                depletion_ages.append(np.inf)
        
        # Store core depletion data
        self.depletion_data = {
            'depletion_years': np.array(depletion_years),
            'depletion_ages': np.array(depletion_ages),
            'n_simulations': n_simulations,
            'n_years': n_years,
            'portfolio_paths': portfolio_paths,
            'qol_paths': qol_paths
        }
        
        # Calculate survival probabilities for each year
        self._calculate_survival_probabilities()
    
    def _calculate_survival_probabilities(self):
        """Calculate year-by-year survival probabilities."""
        n_years = self.depletion_data['n_years']
        n_simulations = self.depletion_data['n_simulations']
        depletion_years = self.depletion_data['depletion_years']
        
        survival_probs = []
        survival_ages = []
        
        for year in range(n_years):
            # Count simulations that survive past this year
            survivors = np.sum(depletion_years > year)
            prob = survivors / n_simulations
            survival_probs.append(prob)
            survival_ages.append(self.retirement_age + year)
        
        self.survival_data = {
            'years': np.arange(n_years),
            'ages': np.array(survival_ages),
            'survival_probabilities': np.array(survival_probs)
        }
    
    def get_depletion_percentiles(self, percentiles: List[float] = [10, 25, 50, 75, 90]) -> Dict:
        """
        Calculate depletion timeline percentiles.
        
        Args:
            percentiles: List of percentiles to calculate (0-100)
            
        Returns:
            Dictionary with percentile analysis results
        """
        depletion_years = self.depletion_data['depletion_years']
        
        # Filter out infinite values (never depleted) for percentile calculation
        finite_depletions = depletion_years[np.isfinite(depletion_years)]
        
        if len(finite_depletions) == 0:
            # No depletions occurred
            return {
                'percentiles': percentiles,
                'depletion_years': [np.inf] * len(percentiles),
                'depletion_ages': [np.inf] * len(percentiles),
                'depletion_rate': 0.0,
                'never_depleted_rate': 1.0,
                'summary': "Portfolio never depletes in any simulation"
            }
        
        # Calculate percentiles for simulations that do deplete
        percentile_years = np.percentile(finite_depletions, percentiles)
        percentile_ages = percentile_years + self.retirement_age
        
        depletion_rate = len(finite_depletions) / len(depletion_years)
        never_depleted_rate = 1.0 - depletion_rate
        
        return {
            'percentiles': percentiles,
            'depletion_years': percentile_years,
            'depletion_ages': percentile_ages,
            'depletion_rate': depletion_rate,
            'never_depleted_rate': never_depleted_rate,
            'total_simulations': len(depletion_years),
            'depleted_simulations': len(finite_depletions),
            'summary': f"{depletion_rate:.1%} of simulations experience depletion"
        }
    
    def get_survival_at_age(self, target_ages: List[int]) -> Dict:
        """
        Get survival probability at specific ages.
        
        Args:
            target_ages: List of ages to analyze
            
        Returns:
            Dictionary with survival probabilities at each age
        """
        survival_ages = self.survival_data['ages']
        survival_probs = self.survival_data['survival_probabilities']
        
        results = {}
        for age in target_ages:
            if age < self.retirement_age:
                results[age] = 1.0  # Before retirement
            elif age >= survival_ages[-1]:
                results[age] = survival_probs[-1]  # Beyond simulation
            else:
                # Interpolate or find closest age
                age_idx = np.argmin(np.abs(survival_ages - age))
                results[age] = survival_probs[age_idx]
        
        return results
    
    def get_risk_metrics(self) -> Dict:
        """
        Calculate comprehensive risk metrics.
        
        Returns:
            Dictionary with various risk measures
        """
        depletion_years = self.depletion_data['depletion_years']
        finite_depletions = depletion_years[np.isfinite(depletion_years)]
        
        # Basic statistics
        total_sims = len(depletion_years)
        depleted_sims = len(finite_depletions)
        depletion_rate = depleted_sims / total_sims
        
        # Time-based metrics
        if depleted_sims > 0:
            mean_depletion_year = np.mean(finite_depletions)
            median_depletion_year = np.median(finite_depletions)
            std_depletion_year = np.std(finite_depletions)
            earliest_depletion = np.min(finite_depletions)
            
            # Risk measures
            var_95 = np.percentile(finite_depletions, 5)  # 5% worst case
            var_99 = np.percentile(finite_depletions, 1)  # 1% worst case
        else:
            mean_depletion_year = np.inf
            median_depletion_year = np.inf
            std_depletion_year = 0
            earliest_depletion = np.inf
            var_95 = np.inf
            var_99 = np.inf
        
        # Survival milestones
        survival_80 = self.get_survival_at_age([80])[80]
        survival_90 = self.get_survival_at_age([90])[90]
        survival_100 = self.get_survival_at_age([100])[100]
        
        return {
            'depletion_rate': depletion_rate,
            'survival_rate': 1 - depletion_rate,
            'mean_depletion_year': mean_depletion_year,
            'mean_depletion_age': mean_depletion_year + self.retirement_age if np.isfinite(mean_depletion_year) else np.inf,
            'median_depletion_year': median_depletion_year,
            'median_depletion_age': median_depletion_year + self.retirement_age if np.isfinite(median_depletion_year) else np.inf,
            'depletion_std': std_depletion_year,
            'earliest_depletion_year': earliest_depletion,
            'earliest_depletion_age': earliest_depletion + self.retirement_age if np.isfinite(earliest_depletion) else np.inf,
            'var_95_years': var_95,  # 5% worst case depletion year
            'var_95_age': var_95 + self.retirement_age if np.isfinite(var_95) else np.inf,
            'var_99_years': var_99,  # 1% worst case depletion year
            'var_99_age': var_99 + self.retirement_age if np.isfinite(var_99) else np.inf,
            'survival_at_80': survival_80,
            'survival_at_90': survival_90,
            'survival_at_100': survival_100,
            'total_simulations': total_sims,
            'depleted_simulations': depleted_sims
        }
    
    def plot_survival_curve(self, save_path: Optional[str] = None, figsize: Tuple[int, int] = (10, 6)) -> plt.Figure:
        """
        Plot portfolio survival probability curve.
        
        Args:
            save_path: Optional path to save the plot
            figsize: Figure size tuple
            
        Returns:
            Matplotlib figure object
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        ages = self.survival_data['ages']
        survival_probs = self.survival_data['survival_probabilities']
        
        # Main survival curve
        ax.plot(ages, survival_probs, linewidth=2, color='blue', label='Survival Probability')
        
        # Add key milestone lines
        milestones = [80, 90, 100]
        colors = ['green', 'orange', 'red']
        
        for milestone, color in zip(milestones, colors):
            if milestone <= ages[-1]:
                survival_at_milestone = self.get_survival_at_age([milestone])[milestone]
                ax.axhline(y=survival_at_milestone, color=color, linestyle='--', alpha=0.7,
                          label=f'Age {milestone}: {survival_at_milestone:.1%}')
                ax.axvline(x=milestone, color=color, linestyle='--', alpha=0.7)
        
        ax.set_xlabel('Age')
        ax.set_ylabel('Portfolio Survival Probability')
        ax.set_title('Portfolio Survival Curve\n(Probability of Portfolio Lasting to Each Age)')
        ax.grid(True, alpha=0.3)
        ax.legend()
        ax.set_ylim(0, 1)
        
        # Format y-axis as percentages
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: '{:.0%}'.format(y)))
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def plot_depletion_histogram(self, save_path: Optional[str] = None, figsize: Tuple[int, int] = (10, 6)) -> plt.Figure:
        """
        Plot histogram of depletion ages.
        
        Args:
            save_path: Optional path to save the plot
            figsize: Figure size tuple
            
        Returns:
            Matplotlib figure object
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        depletion_ages = self.depletion_data['depletion_ages']
        finite_ages = depletion_ages[np.isfinite(depletion_ages)]
        
        if len(finite_ages) == 0:
            ax.text(0.5, 0.5, 'No Portfolio Depletions Occurred\nPortfolio survives in all simulations', 
                   ha='center', va='center', transform=ax.transAxes, fontsize=14)
            ax.set_title('Portfolio Depletion Analysis')
        else:
            # Plot histogram
            bins = max(10, len(finite_ages) // 50)  # Adaptive bin count
            ax.hist(finite_ages, bins=bins, alpha=0.7, color='red', edgecolor='black')
            
            # Add statistics
            mean_age = np.mean(finite_ages)
            median_age = np.median(finite_ages)
            
            ax.axvline(mean_age, color='blue', linestyle='--', linewidth=2, label=f'Mean: {mean_age:.1f}')
            ax.axvline(median_age, color='green', linestyle='--', linewidth=2, label=f'Median: {median_age:.1f}')
            
            ax.set_xlabel('Age at Portfolio Depletion')
            ax.set_ylabel('Number of Simulations')
            ax.set_title(f'Portfolio Depletion Age Distribution\n({len(finite_ages):,} of {len(depletion_ages):,} simulations deplete)')
            ax.legend()
            ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def generate_summary_report(self) -> str:
        """
        Generate comprehensive text summary of depletion analysis.
        
        Returns:
            Formatted summary report string
        """
        risk_metrics = self.get_risk_metrics()
        percentiles = self.get_depletion_percentiles()
        
        report = "PORTFOLIO DEPLETION ANALYSIS SUMMARY\n"
        report += "=" * 50 + "\n\n"
        
        # Overall risk assessment
        report += "RISK ASSESSMENT:\n"
        report += f"• Depletion Risk: {risk_metrics['depletion_rate']:.1%}\n"
        report += f"• Survival Rate: {risk_metrics['survival_rate']:.1%}\n"
        report += f"• Total Simulations: {risk_metrics['total_simulations']:,}\n\n"
        
        if risk_metrics['depleted_simulations'] > 0:
            # Depletion timing
            report += "DEPLETION TIMING (for simulations that deplete):\n"
            report += f"• Earliest Depletion: Age {risk_metrics['earliest_depletion_age']:.0f}\n"
            report += f"• Median Depletion: Age {risk_metrics['median_depletion_age']:.1f}\n"
            report += f"• Mean Depletion: Age {risk_metrics['mean_depletion_age']:.1f}\n\n"
            
            # Risk metrics
            report += "RISK METRICS:\n"
            if np.isfinite(risk_metrics['var_95_age']):
                report += f"• 5% Worst Case: Portfolio depletes by age {risk_metrics['var_95_age']:.0f}\n"
            if np.isfinite(risk_metrics['var_99_age']):
                report += f"• 1% Worst Case: Portfolio depletes by age {risk_metrics['var_99_age']:.0f}\n"
            report += "\n"
            
            # Percentile analysis
            report += "DEPLETION PERCENTILES:\n"
            for i, pct in enumerate(percentiles['percentiles']):
                age = percentiles['depletion_ages'][i]
                if np.isfinite(age):
                    report += f"• {pct}th percentile: Age {age:.1f}\n"
            report += "\n"
        
        # Survival milestones
        report += "SURVIVAL AT KEY AGES:\n"
        report += f"• Age 80: {risk_metrics['survival_at_80']:.1%}\n"
        report += f"• Age 90: {risk_metrics['survival_at_90']:.1%}\n"
        report += f"• Age 100: {risk_metrics['survival_at_100']:.1%}\n\n"
        
        # Recommendations
        report += "RECOMMENDATIONS:\n"
        if risk_metrics['depletion_rate'] > 0.1:  # More than 10% depletion risk
            report += "• HIGH RISK: Consider reducing withdrawal rates or increasing savings\n"
            if np.isfinite(risk_metrics['var_95_age']) and risk_metrics['var_95_age'] < 85:
                report += "• 5% chance of depletion before age 85 - consider risk mitigation\n"
        elif risk_metrics['depletion_rate'] > 0.05:  # 5-10% risk
            report += "• MODERATE RISK: Monitor portfolio performance and consider adjustments\n"
        else:
            report += "• LOW RISK: Portfolio shows strong sustainability\n"
        
        if risk_metrics['survival_at_90'] < 0.9:
            report += "• Consider longevity risk - less than 90% chance of lasting to age 90\n"
        
        return report
    
    def to_dict(self) -> Dict:
        """
        Export all analysis results to a dictionary.
        
        Returns:
            Comprehensive dictionary with all analysis results
        """
        return {
            'risk_metrics': self.get_risk_metrics(),
            'percentile_analysis': self.get_depletion_percentiles(),
            'survival_milestones': self.get_survival_at_age([70, 75, 80, 85, 90, 95, 100]),
            'survival_data': {
                'ages': self.survival_data['ages'].tolist(),
                'survival_probabilities': self.survival_data['survival_probabilities'].tolist()
            },
            'summary_report': self.generate_summary_report(),
            'depletion_statistics': {
                'total_simulations': self.depletion_data['n_simulations'],
                'years_analyzed': self.depletion_data['n_years'],
                'retirement_age': self.retirement_age
            }
        }