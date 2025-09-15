"""
Example script demonstrating the QOL Framework analysis
"""
import sys
import os
# Add parent directory to path for cross-platform module imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.qol_framework import HypotheticalPortfolioQOLAnalysis

def main():
    """Run the complete QOL framework analysis"""
    print("🔬 Initializing Hauenstein QOL Framework Analysis...")
    print("=" * 60)
    
    # Initialize the analysis
    analysis = HypotheticalPortfolioQOLAnalysis()
    
    print("📊 Running Monte Carlo simulations...")
    print("   - Hypothetical portfolio: $750,000")
    print("   - Retirement age: 65")
    print("   - Analysis horizon: 35 years")
    print("   - Simulations: 1,000 paths")
    print()
    
    # Run the complete analysis using the correct method
    results = analysis.compare_strategies()
    
    print("🎯 Analysis Complete!")
    print("=" * 60)
    print(f"Traditional 4% Rule Utility: {results['traditional_metrics']['mean_utility']:.2f}")
    print(f"QOL Framework Utility: {results['hauenstein_metrics']['mean_utility']:.2f}")
    print(f"Utility Improvement: {results['utility_improvement']:.1f}%")
    print()
    print(f"Traditional Portfolio Survival: {results['traditional_metrics']['success_rate']:.0%}")
    print(f"QOL Framework Portfolio Survival: {results['hauenstein_metrics']['success_rate']:.0%}")
    print()
    print("📁 Results saved to 'results/' directory")
    print("📈 Charts generated showing portfolio performance and utility comparison")
    print()
    print("🚀 Key Innovation: This framework challenges the $30+ trillion retirement industry")
    print("   by incorporating the reality that quality of life decreases with age.")

if __name__ == "__main__":
    main()