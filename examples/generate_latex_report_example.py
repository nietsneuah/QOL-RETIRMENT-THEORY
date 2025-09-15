#!/usr/bin/env python3
"""
LaTeX Report Generation Example for QOL Framework

This example demonstrates how to generate high-quality LaTeX-based PDF reports
as an alternative to the standard matplotlib-based reports. LaTeX provides
superior typography, mathematical formatting, and professional presentation.

Requirements:
- LaTeX distribution (MacTeX, MiKTeX, or TeXLive) must be installed
- All standard QOL Framework dependencies
"""

import sys
import os
# Add parent directory to path for cross-platform module imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.enhanced_qol_framework import EnhancedQOLAnalysis
from src.depletion_analysis import PortfolioDepletionAnalysis
from src.sensitivity_analysis import QOLSensitivityAnalysis
from src.latex_report_generator import (
    check_latex_availability, 
    create_latex_pdf_from_results,
    LaTeXReportGenerator
)
import argparse

def run_sample_analysis():
    """Run a sample analysis to demonstrate LaTeX report generation."""
    
    print("🔄 Running sample QOL Framework analysis...")
    
    # Create sample scenario
    scenario_params = {
        'name': 'LaTeX Demo Scenario',
        'starting_portfolio': 750000,
        'starting_age': 65,
        'retirement_horizon': 30,
        'simulations': 1000,
        'description': 'Sample scenario for LaTeX report demonstration'
    }
    
    # Run enhanced analysis
    qol = EnhancedQOLAnalysis(
        starting_value=scenario_params['starting_portfolio'],
        starting_age=scenario_params['starting_age'],
        horizon_years=scenario_params['retirement_horizon'],
        n_simulations=scenario_params['simulations']
    )
    results = qol.run_enhanced_simulation(verbose=False)
    
    # Use the automatically created depletion analysis
    depletion = qol.depletion_analysis
    
    # Run sensitivity analysis (simplified)
    base_params = {
        'starting_value': scenario_params['starting_portfolio'],
        'starting_age': scenario_params['starting_age'],
        'horizon_years': scenario_params['retirement_horizon'],
        'n_simulations': 500,  # Fewer simulations for speed
        'withdrawal_strategy': 'hauenstein',
        'qol_variability': True,
        'return_volatility': 0.15,
        'inflation_variability': True
    }
    sensitivity = QOLSensitivityAnalysis(base_parameters=base_params)
    sens_results = sensitivity.run_single_parameter_sweep(
        parameter_name='starting_value',
        parameter_values=[500000, 750000, 1000000],
        verbose=False
    )
    
    return {
        'enhanced_results': [results],
        'depletion_analyses': [depletion],
        'sensitivity_results': [sens_results] if sens_results else [],
        'scenario_infos': [scenario_params]
    }

def main():
    """Main function to demonstrate LaTeX report generation."""
    
    parser = argparse.ArgumentParser(
        description="Generate LaTeX-based PDF report for QOL Framework analysis"
    )
    parser.add_argument('--check-latex', action='store_true',
                       help='Check LaTeX installation status')
    parser.add_argument('--install-guide', action='store_true',
                       help='Show LaTeX installation instructions')
    parser.add_argument('--generate-sample', action='store_true',
                       help='Generate sample LaTeX report (requires LaTeX)')
    
    args = parser.parse_args()
    
    print("📋 LATEX REPORT GENERATION EXAMPLE")
    print("=" * 60)
    
    # Check LaTeX availability
    latex_status = check_latex_availability()
    
    if args.check_latex:
        print(f"LaTeX Status: {'✅ Available' if latex_status['available'] else '❌ Not Available'}")
        if latex_status['available']:
            print(f"Version: {latex_status['version']}")
        else:
            print("LaTeX is not installed.")
        return
    
    if args.install_guide:
        print("LaTeX Installation Instructions:")
        print("-" * 40)
        for platform, instruction in latex_status['installation'].items():
            print(f"{platform}: {instruction}")
        print("\nAfter installation, restart your terminal and try again.")
        return
    
    if args.generate_sample:
        if not latex_status['available']:
            print("❌ LaTeX is not available. Please install LaTeX first.")
            print("Use --install-guide for installation instructions.")
            return
        
        try:
            print("🔄 Generating sample analysis data...")
            analysis_data = run_sample_analysis()
            
            print("📋 Generating LaTeX-based PDF report...")
            pdf_filename = create_latex_pdf_from_results(
                enhanced_results=analysis_data['enhanced_results'],
                depletion_analyses=analysis_data['depletion_analyses'],
                sensitivity_results=analysis_data['sensitivity_results'],
                scenario_infos=analysis_data['scenario_infos'],
                report_title="LaTeX Demo Report - Enhanced QOL Framework",
                filename="latex_demo_report.pdf"
            )
            
            print(f"✅ LaTeX PDF report generated successfully!")
            print(f"📄 Report saved: {pdf_filename}")
            print("\n🎉 LaTeX Report Features:")
            print("• Professional typography and layout")
            print("• Mathematical equations with proper formatting")
            print("• High-quality tables with enhanced styling")
            print("• Automatic table of contents and cross-references")
            print("• Publication-ready presentation")
            
        except Exception as e:
            print(f"❌ Error generating LaTeX report: {str(e)}")
            return
    
    # Default: show help and status
    if not any([args.check_latex, args.install_guide, args.generate_sample]):
        print("LaTeX Report Generation for QOL Framework")
        print("\nThis example demonstrates professional LaTeX-based PDF generation")
        print("as an alternative to matplotlib-based reports.\n")
        
        print(f"Current LaTeX Status: {'✅ Available' if latex_status['available'] else '❌ Not Available'}")
        
        if latex_status['available']:
            print(f"Version: {latex_status['version']}")
            print("\nUse --generate-sample to create a demo LaTeX report")
        else:
            print("Use --install-guide for installation instructions")
            print("Use --check-latex to verify installation status")
        
        print("\nOptions:")
        print("  --check-latex      Check LaTeX installation status")  
        print("  --install-guide    Show LaTeX installation instructions")
        print("  --generate-sample  Generate sample LaTeX report")
        
        print(f"\n💡 LaTeX Benefits:")
        print("• Superior typography compared to matplotlib reports")
        print("• Professional mathematical equation formatting") 
        print("• Enhanced table layouts and styling")
        print("• Publication-quality output suitable for business/academic use")
        print("• Automatic cross-references and table of contents")

if __name__ == "__main__":
    main()