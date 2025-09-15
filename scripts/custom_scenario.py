#!/usr/bin/env python3
"""
Interactive QOL Framework Analysis
Run single custom scenarios with user-s    print(f"\n🚀 Key Innovation: This framework challenges the $30+ trillion retirement industry")
    print("   by incorporating the reality that quality of life decreases with age.")
    
    # Generate PDF report for the comparison
    print(f"\n📋 Generating consolidated PDF report...")
    pdf_filename = create_pdf_from_scenario_results(
        all_results,
        "QOL Framework Preset Scenarios Comparison"
    )
    print(f"✅ PDF report generated: {pdf_filename}")
    
    return all_resultsecified parameters
"""

import sys
import os
# Add parent directory to path for cross-platform module imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.qol_framework import HypotheticalPortfolioQOLAnalysis
from src.pdf_report_generator import create_pdf_from_scenario_results


class CustomQOLAnalysis(HypotheticalPortfolioQOLAnalysis):
    """
    Customizable version of the QOL Framework
    """
    
    def __init__(self, starting_portfolio, starting_age, retirement_horizon, simulations=1000):
        """
        Initialize with custom parameters
        
        Parameters:
        -----------
        starting_portfolio : float
            Initial portfolio value (e.g., 750000)
        starting_age : int
            Age at retirement start (e.g., 65)
        retirement_horizon : int
            Years to analyze (e.g., 35)
        simulations : int
            Number of Monte Carlo simulations (default: 1000)
        """
        # Call parent constructor first
        super().__init__()
        
        # Override with custom parameters
        self.starting_portfolio = starting_portfolio
        self.starting_age = starting_age
        self.retirement_horizon = retirement_horizon
        self.simulations = simulations
        
        # Recreate dependent objects with new parameters
        self.qol_function = self._define_qol_function()
        self.glide_path = self._define_glide_path()


def run_custom_analysis(starting_portfolio, starting_age, retirement_horizon, simulations=1000):
    """
    Run QOL analysis with custom parameters
    
    Parameters:
    -----------
    starting_portfolio : float
        Initial portfolio value
    starting_age : int  
        Age at retirement start
    retirement_horizon : int
        Years to analyze
    simulations : int
        Number of Monte Carlo simulations
        
    Returns:
    --------
    dict: Analysis results
    """
    
    print("🔬 CUSTOM QOL FRAMEWORK ANALYSIS")
    print("=" * 50)
    print(f"💰 Starting Portfolio: ${starting_portfolio:,}")
    print(f"🎂 Starting Age: {starting_age}")
    print(f"📅 Analysis Horizon: {retirement_horizon} years")
    print(f"🎲 Monte Carlo Simulations: {simulations:,}")
    print()
    
    # Create custom analysis
    analysis = CustomQOLAnalysis(
        starting_portfolio=starting_portfolio,
        starting_age=starting_age, 
        retirement_horizon=retirement_horizon,
        simulations=simulations
    )
    
    # Run the analysis
    print("🔄 Running simulations...")
    results = analysis.compare_strategies()
    
    # Display results
    print("\n🎯 ANALYSIS RESULTS")
    print("=" * 50)
    print(f"🏆 QOL Framework Results:")
    print(f"   Success Rate: {results['hauenstein_metrics']['success_rate']:.1%}")
    print(f"   Median Final Value: ${results['hauenstein_metrics']['median_final_value']:,.0f}")
    print(f"   Mean Utility Score: {results['hauenstein_metrics']['mean_utility']:,.0f}")
    print()
    print(f"📊 Traditional 4% Rule Results:")
    print(f"   Success Rate: {results['traditional_metrics']['success_rate']:.1%}")
    print(f"   Median Final Value: ${results['traditional_metrics']['median_final_value']:,.0f}")
    print(f"   Mean Utility Score: {results['traditional_metrics']['mean_utility']:,.0f}")
    print()
    print(f"🚀 QOL Framework Improvement: +{results['utility_improvement']:.1f}% utility enhancement")
    
    # Show withdrawal strategy for this scenario
    qol_rates = analysis.hauenstein_qol_strategy()
    print(f"\n📋 QOL Withdrawal Strategy (Age {starting_age}-{starting_age + retirement_horizon}):")
    
    # Show sample rates by phase
    phases = [
        (starting_age, min(starting_age + 10, starting_age + retirement_horizon)),
        (starting_age + 10, min(starting_age + 20, starting_age + retirement_horizon)),
        (starting_age + 20, starting_age + retirement_horizon)
    ]
    
    for i, (start_age, end_age) in enumerate(phases):
        if start_age >= starting_age + retirement_horizon:
            break
        sample_age = min(start_age + 5, end_age - 1, starting_age + retirement_horizon - 1)
        if sample_age in qol_rates:
            print(f"   Phase {i+1} (ages {start_age}-{end_age-1}): {qol_rates[sample_age]:.1%}")
    
    return results


def interactive_mode():
    """
    Interactive mode for entering custom parameters
    """
    print("🎯 QOL FRAMEWORK - INTERACTIVE MODE")
    print("=" * 50)
    print("Enter your retirement scenario parameters:")
    print()
    
    try:
        # Get user inputs
        portfolio = float(input("💰 Starting portfolio value ($): "))
        age = int(input("🎂 Starting retirement age: "))
        horizon = int(input("📅 Analysis horizon (years): "))
        
        # Optional simulation count
        sim_input = input("🎲 Number of simulations (press Enter for 1000): ").strip()
        simulations = int(sim_input) if sim_input else 1000
        
        print("\n" + "="*50)
        
        # Run analysis
        results = run_custom_analysis(portfolio, age, horizon, simulations)
        
        return results
        
    except ValueError as e:
        print(f"❌ Invalid input: {e}")
        return None
    except KeyboardInterrupt:
        print("\n❌ Analysis cancelled by user")
        return None


def preset_scenarios():
    """
    Run some preset scenarios for comparison
    """
    scenarios = [
        {
            'name': 'Conservative Early Retirement',
            'portfolio': 500000,
            'age': 62,
            'horizon': 33
        },
        {
            'name': 'Standard Retirement',
            'portfolio': 750000,
            'age': 65,
            'horizon': 30
        },
        {
            'name': 'Late High-Value Retirement',
            'portfolio': 1200000,
            'age': 70,
            'horizon': 25
        },
        {
            'name': 'Extended Horizon',
            'portfolio': 600000,
            'age': 60,
            'horizon': 40
        }
    ]
    
    print("🎯 PRESET SCENARIOS COMPARISON")
    print("=" * 60)
    
    all_results = []
    
    for scenario in scenarios:
        print(f"\n🔄 Running: {scenario['name']}")
        print("-" * 40)
        
        results = run_custom_analysis(
            scenario['portfolio'], 
            scenario['age'], 
            scenario['horizon'],
            simulations=500  # Fewer simulations for speed
        )
        
        results['scenario_name'] = scenario['name']
        all_results.append(results)
    
    # Summary comparison
    print("\n📊 SCENARIOS SUMMARY")
    print("=" * 60)
    print(f"{'Scenario':<25} {'Utility Imp.':<12} {'QOL Success':<12} {'Trad. Success':<12}")
    print("-" * 60)
    
    for result in all_results:
        name = result['scenario_name'][:24]
        utility_imp = f"{result['utility_improvement']:.1f}%"
        qol_success = f"{result['hauenstein_metrics']['success_rate']:.1%}"
        trad_success = f"{result['traditional_metrics']['success_rate']:.1%}"
        
        print(f"{name:<25} {utility_imp:<12} {qol_success:<12} {trad_success:<12}")
    
    return all_results


def main():
    """
    Main interface for custom scenario analysis
    """
    print("🎯 QOL FRAMEWORK CUSTOM SCENARIO RUNNER")
    print("=" * 60)
    print("Choose analysis mode:")
    print("1. Interactive mode (enter custom parameters)")
    print("2. Preset scenarios comparison") 
    print("3. Single custom scenario (command line)")
    print()
    
    try:
        choice = input("Enter choice (1-3): ").strip()
        
        if choice == '1':
            interactive_mode()
        elif choice == '2':
            preset_scenarios()
        elif choice == '3':
            # Example single scenario
            print("\nRunning example scenario...")
            run_custom_analysis(
                starting_portfolio=800000,
                starting_age=67,
                retirement_horizon=28,
                simulations=1000
            )
        else:
            print("❌ Invalid choice")
            
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")


if __name__ == "__main__":
    main()