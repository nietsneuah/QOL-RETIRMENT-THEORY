#!/usr/bin/env python3
"""
Generate PDF report for a single custom scenario
"""

import sys
import os
# Add parent directory to path for cross-platform module imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.custom_scenario import run_custom_analysis
from src.pdf_report_generator import create_pdf_from_scenario_results
import argparse

def main():
    """
    Generate PDF report for single scenario with command line parameters
    """
    parser = argparse.ArgumentParser(
        description="Generate PDF report for single QOL Framework scenario"
    )
    
    parser.add_argument('--portfolio', type=float, required=True,
                       help='Starting portfolio value (e.g., 750000)')
    parser.add_argument('--age', type=int, required=True,
                       help='Starting retirement age (e.g., 65)')
    parser.add_argument('--horizon', type=int, required=True,
                       help='Analysis horizon in years (e.g., 30)')
    parser.add_argument('--simulations', type=int, default=1000,
                       help='Number of Monte Carlo simulations (default: 1000)')
    parser.add_argument('--name', type=str, default=None,
                       help='Scenario name (default: auto-generated)')
    parser.add_argument('--output', type=str, default=None,
                       help='Output PDF filename (default: auto-generated)')
    
    args = parser.parse_args()
    
    print("🎯 QOL FRAMEWORK SINGLE SCENARIO PDF GENERATOR")
    print("=" * 60)
    print(f"💰 Portfolio: ${args.portfolio:,}")
    print(f"🎂 Age: {args.age}")
    print(f"📅 Horizon: {args.horizon} years")
    print(f"🎲 Simulations: {args.simulations:,}")
    print()
    
    # Generate scenario name if not provided
    if not args.name:
        args.name = f"Custom_${args.portfolio/1000:.0f}K_Age{args.age}_Horizon{args.horizon}"
    
    # Run the analysis
    print("🔄 Running QOL Framework analysis...")
    results = run_custom_analysis(
        starting_portfolio=args.portfolio,
        starting_age=args.age,
        retirement_horizon=args.horizon,
        simulations=args.simulations
    )
    
    # Add scenario metadata
    results['scenario'] = {
        'name': args.name,
        'starting_portfolio': args.portfolio,
        'starting_age': args.age,
        'retirement_horizon': args.horizon,
        'simulations': args.simulations,
        'description': f'Custom analysis: ${args.portfolio:,} portfolio, age {args.age}, {args.horizon} year horizon'
    }
    
    # Generate PDF report
    print("\n📋 Generating PDF report...")
    pdf_filename = create_pdf_from_scenario_results(
        [results],  # Single scenario in list
        f"QOL Framework Analysis: {args.name}",
        args.output
    )
    
    print(f"\n🎉 Analysis complete!")
    print(f"📋 PDF report generated: {pdf_filename}")
    
    return pdf_filename

if __name__ == "__main__":
    main()