#!/usr/bin/env python3
"""
Four-Asset QOL Framework Prototype
Extending the current framework to include Gold and TIPS

Asset Classes:
1. US Stocks (VTI) - Growth engine
2. US Bonds (TFLO) - Stability  
3. TIPS (TIP) - Inflation protection
4. Gold (GLD) - Crisis hedge and inflation hedge

This prototype demonstrates how Gold and TIPS integration might affect
QOL retirement strategies and cost-per-enjoyment-dollar calculations.
"""

import sys
import os
import pandas as pd
import numpy as np
from pathlib import Path

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

class FourAssetQOLFramework:
    """
    Enhanced QOL Framework with Gold and TIPS integration
    """
    
    def __init__(self, starting_value=1000000, starting_age=65, horizon_years=30, n_simulations=1000):
        self.starting_value = starting_value
        self.starting_age = starting_age
        self.horizon_years = horizon_years
        self.n_simulations = n_simulations
        
        # Enhanced asset class definitions
        self.asset_classes = {
            'stocks': {
                'real_return': 0.072,    # 7.2% real
                'volatility': 0.20,      # 20% volatility
                'description': 'US Total Stock Market (VTI)'
            },
            'bonds': {
                'real_return': 0.020,    # 2.0% real
                'volatility': 0.06,      # 6% volatility  
                'description': 'US Treasury Bonds (TFLO)'
            },
            'tips': {
                'real_return': 0.010,    # 1.0% real (guaranteed)
                'volatility': 0.05,      # 5% volatility
                'description': 'Treasury Inflation-Protected Securities (TIP)'
            },
            'gold': {
                'real_return': 0.015,    # 1.5% real long-term
                'volatility': 0.18,      # 18% volatility
                'description': 'Gold ETF (GLD)'
            }
        }
        
        # Correlation matrix (Stocks, Bonds, TIPS, Gold)
        self.correlation_matrix = np.array([
            [1.00,  0.10, -0.10,  0.30],  # Stocks
            [0.10,  1.00,  0.80, -0.20],  # Bonds  
            [-0.10, 0.80,  1.00,  0.10],  # TIPS
            [0.30, -0.20,  0.10,  1.00]   # Gold
        ])
        
        # QOL phases and multipliers
        self.qol_phases = {
            'phase1': {'ages': (65, 74), 'multiplier': 1.35},  # High enjoyment
            'phase2': {'ages': (75, 84), 'multiplier': 1.125}, # Moderate enjoyment  
            'phase3': {'ages': (85, 99), 'multiplier': 0.875}  # Lower enjoyment
        }
        
        # Define allocation strategies
        self.allocation_strategies = {
            'two_asset_aggressive': {
                'name': 'Two-Asset Aggressive Glide Path',
                'phase1': {'stocks': 1.00, 'bonds': 0.00, 'tips': 0.00, 'gold': 0.00},
                'phase2': {'stocks': 0.70, 'bonds': 0.30, 'tips': 0.00, 'gold': 0.00},
                'phase3': {'stocks': 0.40, 'bonds': 0.60, 'tips': 0.00, 'gold': 0.00},
            },
            'four_asset_aggressive': {
                'name': 'Four-Asset Aggressive with TIPS/Gold',
                'phase1': {'stocks': 0.80, 'bonds': 0.10, 'tips': 0.05, 'gold': 0.05},
                'phase2': {'stocks': 0.60, 'bonds': 0.20, 'tips': 0.15, 'gold': 0.05},
                'phase3': {'stocks': 0.40, 'bonds': 0.30, 'tips': 0.25, 'gold': 0.05},
            },
            'four_asset_balanced': {
                'name': 'Four-Asset Balanced with Enhanced TIPS',
                'phase1': {'stocks': 0.60, 'bonds': 0.20, 'tips': 0.15, 'gold': 0.05},
                'phase2': {'stocks': 0.45, 'bonds': 0.25, 'tips': 0.25, 'gold': 0.05},
                'phase3': {'stocks': 0.30, 'bonds': 0.35, 'tips': 0.30, 'gold': 0.05},
            },
            'inflation_protected': {
                'name': 'Inflation-Protected Strategy (High TIPS/Gold)',
                'phase1': {'stocks': 0.50, 'bonds': 0.15, 'tips': 0.25, 'gold': 0.10},
                'phase2': {'stocks': 0.35, 'bonds': 0.20, 'tips': 0.35, 'gold': 0.10},
                'phase3': {'stocks': 0.25, 'bonds': 0.25, 'tips': 0.40, 'gold': 0.10},
            }
        }
    
    def get_allocation_for_age(self, age, strategy_name):
        """Get asset allocation for given age and strategy"""
        strategy = self.allocation_strategies[strategy_name]
        
        # Determine phase
        if age <= 74:
            return strategy['phase1']
        elif age <= 84:
            return strategy['phase2']
        else:
            return strategy['phase3']
    
    def generate_correlated_returns(self, years):
        """Generate correlated returns for all four asset classes"""
        
        # Create arrays for each asset class
        returns = {}
        
        for sim in range(self.n_simulations):
            # Generate correlated random returns using Cholesky decomposition
            L = np.linalg.cholesky(self.correlation_matrix)
            
            sim_returns = {}
            for asset in self.asset_classes:
                sim_returns[asset] = []
            
            for year in range(years):
                # Generate independent random normals
                independent_randoms = np.random.normal(0, 1, 4)
                
                # Apply correlation structure
                correlated_randoms = L @ independent_randoms
                
                # Convert to asset returns
                for i, asset in enumerate(['stocks', 'bonds', 'tips', 'gold']):
                    asset_info = self.asset_classes[asset]
                    annual_return = (asset_info['real_return'] + 
                                   asset_info['volatility'] * correlated_randoms[i])
                    sim_returns[asset].append(annual_return)
            
            # Store simulation results
            for asset in self.asset_classes:
                if asset not in returns:
                    returns[asset] = []
                returns[asset].append(sim_returns[asset])
        
        return returns
    
    def run_strategy_simulation(self, strategy_name, withdrawal_approach='qol'):
        """Run Monte Carlo simulation for a given allocation strategy"""
        
        print(f"\n🔄 Simulating: {self.allocation_strategies[strategy_name]['name']}")
        
        # Generate returns for all asset classes
        returns = self.generate_correlated_returns(self.horizon_years)
        
        # Storage for simulation results
        portfolio_paths = []
        withdrawal_paths = []
        enjoyment_values = []
        
        for sim in range(self.n_simulations):
            portfolio_value = self.starting_value
            sim_withdrawals = []
            sim_enjoyment = 0
            sim_portfolio = [portfolio_value]
            
            for year in range(self.horizon_years):
                age = self.starting_age + year
                
                # Get current allocation
                allocation = self.get_allocation_for_age(age, strategy_name)
                
                # Calculate withdrawal based on approach
                if withdrawal_approach == 'qol':
                    # QOL approach with phase-based multipliers
                    qol_mult = self.get_qol_multiplier(age)
                    trinity_base = 40000 * (1.03 ** year)  # Inflation-adjusted Trinity base
                    withdrawal = trinity_base * qol_mult
                else:
                    # Trinity Study approach (fixed real amount)
                    withdrawal = 40000 * (1.03 ** year)  # Fixed real purchasing power
                
                # Apply withdrawal
                portfolio_value -= withdrawal
                sim_withdrawals.append(withdrawal)
                
                # Calculate enjoyment value for QOL
                qol_mult = self.get_qol_multiplier(age)
                enjoyment = withdrawal * qol_mult
                sim_enjoyment += enjoyment / (1.03 ** year)  # Present value
                
                # Calculate portfolio return
                portfolio_return = 0
                for asset, weight in allocation.items():
                    asset_return = returns[asset][sim][year]
                    portfolio_return += weight * asset_return
                
                # Apply return to portfolio
                portfolio_value *= (1 + portfolio_return)
                sim_portfolio.append(portfolio_value)
            
            portfolio_paths.append(sim_portfolio)
            withdrawal_paths.append(sim_withdrawals)
            enjoyment_values.append(sim_enjoyment)
        
        return {
            'portfolio_paths': np.array(portfolio_paths),
            'withdrawal_paths': np.array(withdrawal_paths),
            'enjoyment_values': np.array(enjoyment_values),
            'final_values': [path[-1] for path in portfolio_paths],
            'depletion_rate': np.mean([1 if any(v <= 0 for v in path) else 0 for path in portfolio_paths])
        }
    
    def get_qol_multiplier(self, age):
        """Get QOL multiplier for given age"""
        for phase, info in self.qol_phases.items():
            if info['ages'][0] <= age <= info['ages'][1]:
                return info['multiplier']
        return self.qol_phases['phase3']['multiplier']  # Default to phase 3
    
    def calculate_cost_per_enjoyment_dollar(self, results):
        """Calculate cost per enjoyment dollar for the strategy"""
        
        # Total cost = starting portfolio value
        total_cost = self.starting_value
        
        # Total enjoyment = sum of present value of enjoyment across all simulations
        mean_enjoyment = np.mean(results['enjoyment_values'])
        
        # Cost per enjoyment dollar
        cost_per_enjoyment = total_cost / mean_enjoyment if mean_enjoyment > 0 else float('inf')
        
        return cost_per_enjoyment, mean_enjoyment
    
    def compare_strategies(self):
        """Compare all allocation strategies"""
        
        print("🚀 FOUR-ASSET QOL FRAMEWORK ANALYSIS")
        print("=" * 60)
        print(f"Parameters:")
        print(f"  Starting Portfolio: ${self.starting_value:,}")
        print(f"  Age Range: {self.starting_age}-{self.starting_age + self.horizon_years - 1}")
        print(f"  Simulations: {self.n_simulations:,}")
        print(f"  Asset Classes: Stocks, Bonds, TIPS, Gold")
        
        results = {}
        
        # Test all strategies
        for strategy_name in self.allocation_strategies:
            strategy_results = self.run_strategy_simulation(strategy_name, 'qol')
            
            # Calculate metrics
            cost_per_enjoyment, mean_enjoyment = self.calculate_cost_per_enjoyment_dollar(strategy_results)
            
            final_values = strategy_results['final_values']
            depletion_rate = strategy_results['depletion_rate']
            success_rate = 1 - depletion_rate
            
            results[strategy_name] = {
                'name': self.allocation_strategies[strategy_name]['name'],
                'cost_per_enjoyment': cost_per_enjoyment,
                'mean_enjoyment': mean_enjoyment,
                'success_rate': success_rate,
                'depletion_rate': depletion_rate,
                'median_final_value': np.median(final_values),
                'mean_final_value': np.mean(final_values),
                'final_value_std': np.std(final_values)
            }
        
        return results
    
    def create_comparison_report(self, results):
        """Create detailed comparison report"""
        
        print("\n📊 STRATEGY COMPARISON RESULTS")
        print("=" * 80)
        
        # Sort by cost per enjoyment dollar
        sorted_strategies = sorted(results.items(), key=lambda x: x[1]['cost_per_enjoyment'])
        
        print(f"{'Strategy':<35} {'Cost/Enjoy':<12} {'Success Rate':<12} {'Final Value':<15}")
        print("-" * 80)
        
        for strategy_name, metrics in sorted_strategies:
            name = metrics['name'][:34]  # Truncate if too long
            cost = f"${metrics['cost_per_enjoyment']:.2f}"
            success = f"{metrics['success_rate']:.1%}"
            final_val = f"${metrics['median_final_value']:,.0f}"
            
            print(f"{name:<35} {cost:<12} {success:<12} {final_val:<15}")
        
        print("\n🏆 KEY FINDINGS:")
        best_strategy = sorted_strategies[0]
        best_name = best_strategy[1]['name']
        best_cost = best_strategy[1]['cost_per_enjoyment']
        
        print(f"  Best Strategy: {best_name}")
        print(f"  Cost per Enjoyment Dollar: ${best_cost:.2f}")
        
        # Compare with two-asset baseline
        two_asset = results.get('two_asset_aggressive')
        four_asset = results.get('four_asset_aggressive')
        
        if two_asset and four_asset:
            cost_improvement = two_asset['cost_per_enjoyment'] - four_asset['cost_per_enjoyment']
            success_change = four_asset['success_rate'] - two_asset['success_rate']
            
            print(f"\n🔄 TWO-ASSET vs FOUR-ASSET AGGRESSIVE COMPARISON:")
            print(f"  Cost Improvement: ${cost_improvement:.2f} per enjoyment dollar")
            print(f"  Success Rate Change: {success_change:+.1%}")
            
            if cost_improvement > 0:
                print(f"  ✅ Four-asset strategy provides better value")
            else:
                print(f"  ❌ Two-asset strategy provides better value")
        
        return sorted_strategies

def main():
    """Run the four-asset QOL framework analysis"""
    
    # Initialize framework
    framework = FourAssetQOLFramework(
        starting_value=1000000,
        starting_age=65,
        horizon_years=30,
        n_simulations=1000
    )
    
    # Run comparison
    results = framework.compare_strategies()
    
    # Generate report
    sorted_results = framework.create_comparison_report(results)
    
    # Save detailed results
    output_dir = Path("output/data")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Convert to DataFrame for CSV export
    df_data = []
    for strategy_name, metrics in results.items():
        df_data.append({
            'strategy': strategy_name,
            'name': metrics['name'],
            'cost_per_enjoyment_dollar': metrics['cost_per_enjoyment'],
            'success_rate': metrics['success_rate'],
            'median_final_value': metrics['median_final_value'],
            'mean_final_value': metrics['mean_final_value'],
            'mean_enjoyment': metrics['mean_enjoyment']
        })
    
    df = pd.DataFrame(df_data)
    output_file = output_dir / "four_asset_qol_comparison.csv"
    df.to_csv(output_file, index=False)
    
    print(f"\n💾 Detailed results saved to: {output_file}")
    
    return results

if __name__ == "__main__":
    results = main()