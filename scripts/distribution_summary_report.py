"""
PORTFOLIO DISTRIBUTION SUMMARY REPORT

This report synthesizes the key findings from the portfolio value distribution
analysis at the 10 and 20-year decision points for the Aggressive Glide Path strategy.
"""

import os
from pathlib import Path

# Find project root directory
script_dir = Path(__file__).parent
project_root = script_dir.parent

def create_distribution_summary():
    """Create a comprehensive summary of distribution findings"""
    
    summary = []
    summary.append("=" * 80)
    summary.append("📊 PORTFOLIO VALUE DISTRIBUTION ANALYSIS SUMMARY")
    summary.append("=" * 80)
    summary.append("")
    
    summary.append("🎯 EXECUTIVE SUMMARY")
    summary.append("-" * 50)
    summary.append("Analysis of 10,000 simulations examining portfolio value distributions")
    summary.append("at key decision points (Years 10 and 20) for the Aggressive Glide Path")
    summary.append("strategy compared to the Trinity Study baseline.")
    summary.append("")
    
    summary.append("📈 KEY FINDINGS")
    summary.append("-" * 30)
    summary.append("")
    
    summary.append("🎂 YEAR 10 (AGE 75) - FIRST REALLOCATION DECISION")
    summary.append("   Decision Context: Reduce allocation from 100% to 70% stocks")
    summary.append("")
    summary.append("   ALL SCENARIOS:")
    summary.append("   • Aggressive Glide median: $913,768")
    summary.append("   • Trinity Study median: $977,419") 
    summary.append("   • Advantage: -6.5% (Trinity leads by $63,651)")
    summary.append("")
    summary.append("   SUCCESSFUL SCENARIOS ONLY:")
    summary.append("   • Aggressive Glide median: $1,614,119")
    summary.append("   • Trinity Study median: $1,372,836")
    summary.append("   • Advantage: +17.6% (Aggressive leads by $241,283)")
    summary.append("")
    summary.append("   💡 INSIGHT: When Aggressive Glide succeeds, it builds substantial")
    summary.append("       wealth advantage by Year 10 through aggressive early allocation.")
    summary.append("")
    
    summary.append("🎂 YEAR 20 (AGE 85) - SECOND REALLOCATION DECISION")
    summary.append("   Decision Context: Reduce allocation from 70% to 40% stocks")
    summary.append("")
    summary.append("   ALL SCENARIOS:")
    summary.append("   • Aggressive Glide median: $427,461")
    summary.append("   • Trinity Study median: $989,143")
    summary.append("   • Advantage: -56.8% (Trinity leads by $561,682)")
    summary.append("")
    summary.append("   SUCCESSFUL SCENARIOS ONLY:")
    summary.append("   • Aggressive Glide median: $1,830,808")
    summary.append("   • Trinity Study median: $1,541,151")
    summary.append("   • Advantage: +18.8% (Aggressive leads by $289,656)")
    summary.append("")
    summary.append("   💡 INSIGHT: Higher QOL withdrawals reduce overall portfolio values,")
    summary.append("       but successful scenarios maintain strong wealth advantage.")
    summary.append("")
    
    summary.append("🏁 FINAL OUTCOME (AGE 94)")
    summary.append("")
    summary.append("   SUCCESS RATES:")
    summary.append("   • Aggressive Glide Path: 45.8%")
    summary.append("   • Trinity Study: 52.9%")
    summary.append("   • Success rate penalty: -7.1%")
    summary.append("")
    summary.append("   SUCCESSFUL SCENARIOS FINAL VALUES:")
    summary.append("   • Aggressive Glide median: $1,793,258")
    summary.append("   • Trinity Study median: $1,397,318")
    summary.append("   • Advantage: +28.3% (Aggressive leads by $395,940)")
    summary.append("")
    
    summary.append("🎉 ENJOYMENT VALUE ANALYSIS")
    summary.append("-" * 40)
    summary.append("   Total Enjoyment Value (Successful Scenarios):")
    summary.append("   • Aggressive Glide Path: $2,469,991")
    summary.append("   • Trinity Study equivalent: $2,229,563")
    summary.append("   • Enjoyment advantage: +10.8%")
    summary.append("")
    
    summary.append("🔍 STRATEGIC IMPLICATIONS")
    summary.append("-" * 40)
    summary.append("")
    summary.append("1. TRADE-OFF STRUCTURE:")
    summary.append("   • Lower success rate (-7.1%) for higher enjoyment (+10.8%)")
    summary.append("   • Cost per enjoyment dollar: $0.97 (excellent value)")
    summary.append("")
    summary.append("2. DECISION POINT RATIONALE:")
    summary.append("   • Year 10: Reduce risk as early wealth-building phase ends")
    summary.append("   • Year 20: Prioritize preservation as enjoyment value drops")
    summary.append("")
    summary.append("3. SUCCESS PROFILE:")
    summary.append("   • When successful, provides 17-28% higher final wealth")
    summary.append("   • Builds substantial early advantage through aggressive allocation")
    summary.append("   • Higher variability creates both bigger wins and losses")
    summary.append("")
    
    summary.append("📊 DISTRIBUTION CHARACTERISTICS")
    summary.append("-" * 40)
    summary.append("")
    summary.append("YEAR 10 PATTERNS:")
    summary.append("• Aggressive Glide: Higher volatility, wider distribution")
    summary.append("• Trinity Study: More consistent outcomes, lower variance")
    summary.append("• Failure rate impact: 4.6% vs 0.2% at Year 10")
    summary.append("")
    summary.append("YEAR 20 PATTERNS:")
    summary.append("• Aggressive Glide: Bimodal distribution (success vs struggle)")
    summary.append("• Trinity Study: More normal distribution shape")
    summary.append("• Failure rate impact: 35.1% vs 19.1% at Year 20")
    summary.append("")
    
    summary.append("💡 DECISION FRAMEWORK")
    summary.append("-" * 30)
    summary.append("")
    summary.append("CHOOSE AGGRESSIVE GLIDE PATH IF:")
    summary.append("• Value early retirement enjoyment highly")
    summary.append("• Comfortable with 7% higher failure risk")
    summary.append("• Willing to accept higher portfolio volatility")
    summary.append("• Believe in long-term equity market performance")
    summary.append("")
    summary.append("CHOOSE TRINITY STUDY IF:")
    summary.append("• Prioritize portfolio survival certainty")
    summary.append("• Prefer consistent, predictable outcomes")
    summary.append("• Risk-averse personality")
    summary.append("• Value capital preservation over enjoyment premium")
    summary.append("")
    
    summary.append("🎯 OPTIMAL USE CASE")
    summary.append("-" * 30)
    summary.append("The Aggressive Glide Path is optimal for retirees who:")
    summary.append("1. Have additional income sources or safety nets")
    summary.append("2. Place high value on early retirement experiences")
    summary.append("3. Are comfortable with dynamic allocation decisions")
    summary.append("4. Want to maximize enjoyment-adjusted retirement value")
    summary.append("")
    summary.append("At $0.97 per enjoyment dollar, it represents the most cost-effective")
    summary.append("QOL strategy identified, making it worthwhile for those who value")
    summary.append("enhanced early retirement experiences.")
    summary.append("")
    summary.append("=" * 80)
    
    return "\n".join(summary)

def main():
    """Generate and save the distribution summary report"""
    
    print("📋 GENERATING PORTFOLIO DISTRIBUTION SUMMARY REPORT")
    print("=" * 60)
    
    # Create the summary
    report = create_distribution_summary()
    
    # Display the report
    print(report)
    
    # Save the report
    output_dir = project_root / 'output'
    os.makedirs(output_dir, exist_ok=True)
    
    with open(f'{output_dir}/portfolio_distribution_summary.txt', 'w') as f:
        f.write(report)
    
    print(f"\n✅ Summary report saved: {output_dir}/portfolio_distribution_summary.txt")

if __name__ == "__main__":
    import os
    main()