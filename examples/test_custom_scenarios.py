#!/usr/bin/env python3
"""
Test the custom scenario functionality
"""
import sys
import os
# Add parent directory to path for cross-platform module imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.custom_scenario import run_custom_analysis
from src.pdf_report_generator import create_pdf_from_scenario_results

def test_scenarios():
    """Test different scenarios with various parameters"""
    
    scenarios = [
        {
            'name': 'Conservative Scenario',
            'portfolio': 500000,
            'age': 65,
            'horizon': 25,
            'simulations': 100  # Small for testing
        },
        {
            'name': 'Aggressive Scenario', 
            'portfolio': 1000000,
            'age': 60,
            'horizon': 35,
            'simulations': 100
        },
        {
            'name': 'Late Retirement',
            'portfolio': 600000,
            'age': 70,
            'horizon': 20,
            'simulations': 100
        }
    ]
    
    print("🧪 TESTING CUSTOM SCENARIO FUNCTIONALITY")
    print("=" * 60)
    
    all_results = []
    
    for scenario in scenarios:
        print(f"\n🔄 Testing: {scenario['name']}")
        print("-" * 30)
        
        try:
            results = run_custom_analysis(
                starting_portfolio=scenario['portfolio'],
                starting_age=scenario['age'], 
                retirement_horizon=scenario['horizon'],
                simulations=scenario['simulations']
            )
            
            # Store for comparison
            results['scenario_name'] = scenario['name']
            all_results.append(results)
            
            print("✅ Test passed!")
            
        except Exception as e:
            print(f"❌ Test failed: {e}")
    
    # Summary comparison
    if all_results:
        print("\n📊 SCENARIO COMPARISON")
        print("=" * 70)
        print(f"{'Scenario':<20} {'Utility Improvement':<18} {'QOL Success':<12} {'Final Value'}")
        print("-" * 70)
        
        for result in all_results:
            name = result['scenario_name'][:19]
            utility_imp = f"{result['utility_improvement']:.1f}%"
            success = f"{result['hauenstein_metrics']['success_rate']:.1%}"
            final_val = f"${result['hauenstein_metrics']['median_final_value']:,.0f}"
            
            print(f"{name:<20} {utility_imp:<18} {success:<12} {final_val}")
    
    # Generate PDF report
    print(f"\n📋 Generating consolidated PDF report...")
    pdf_filename = create_pdf_from_scenario_results(
        all_results,
        "QOL Framework Test Scenarios Analysis"
    )
    print(f"✅ PDF report generated: {pdf_filename}")
    
    print(f"\n🎉 All {len(all_results)} scenarios completed successfully!")
    return all_results

if __name__ == "__main__":
    test_scenarios()