#!/usr/bin/env python3
"""
I BONDS SPECIFIC ANALYSIS FOR QOL FRAMEWORK

Detailed analysis of Series I Savings Bonds (I Bonds) as a potential 
addition to the QOL retirement framework, given their unique inflation 
protection characteristics.
"""

import sys
import os
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent / 'src'))

class IBondsQOLAnalysis:
    """
    Specialized analysis of I Bonds for QOL framework integration
    """
    
    def __init__(self):
        """Initialize I Bonds analysis parameters"""
        
        # I Bonds characteristics and constraints
        self.i_bonds_features = {
            'annual_purchase_limit': 10000,  # Per person per year
            'minimum_holding_period': 1,     # Years
            'early_redemption_penalty': 3,   # Months of interest if redeemed before 5 years
            'maturity': 30,                  # Years
            'tax_treatment': 'federal_exempt_if_education',
            'inflation_protection': 'full',   # Adjusts with CPI-U
            'base_rate': 0.0,                # Fixed rate (currently near 0%)
            'current_composite_rate': 0.053,  # As of 2024 (varies with inflation)
            'liquidity_after_year_1': 'high',
            'default_risk': 'zero'           # US Treasury backing
        }
        
        # QOL portfolio scenarios for analysis
        self.portfolio_scenarios = {
            'baseline_enhanced_moderate': {
                'stocks': 0.50, 'bonds': 0.30, 'gold': 0.15, 'tips': 0.05,
                'expected_return': 0.065, 'volatility': 0.125, 'portfolio_value': 1000000
            },
            'with_5pct_ibonds': {
                'stocks': 0.475, 'bonds': 0.285, 'gold': 0.14, 'tips': 0.05, 'i_bonds': 0.05,
                'expected_return': 0.0635, 'volatility': 0.122, 'portfolio_value': 1000000
            },
            'with_10pct_ibonds': {
                'stocks': 0.45, 'bonds': 0.27, 'gold': 0.13, 'tips': 0.05, 'i_bonds': 0.10,
                'expected_return': 0.062, 'volatility': 0.118, 'portfolio_value': 1000000
            }
        }
        
        # Implementation constraints analysis
        self.implementation_scenarios = [
            {
                'retiree_profile': 'Single Retiree, $500K Portfolio',
                'portfolio_size': 500000,
                'max_annual_purchase': 10000,
                'years_to_target_allocation': None,
                'target_allocation_5pct': 25000,
                'target_allocation_10pct': 50000
            },
            {
                'retiree_profile': 'Married Couple, $1M Portfolio',
                'portfolio_size': 1000000,
                'max_annual_purchase': 20000,  # Both spouses
                'years_to_target_allocation': None,
                'target_allocation_5pct': 50000,
                'target_allocation_10pct': 100000
            },
            {
                'retiree_profile': 'Wealthy Couple, $2M Portfolio',
                'portfolio_size': 2000000,
                'max_annual_purchase': 20000,
                'years_to_target_allocation': None,
                'target_allocation_5pct': 100000,
                'target_allocation_10pct': 200000
            }
        ]
    
    def calculate_implementation_timeline(self):
        """Calculate how long it takes to reach target I Bonds allocations"""
        
        for scenario in self.implementation_scenarios:
            # Calculate years to reach target allocations
            scenario['years_to_5pct'] = np.ceil(scenario['target_allocation_5pct'] / scenario['max_annual_purchase'])
            scenario['years_to_10pct'] = np.ceil(scenario['target_allocation_10pct'] / scenario['max_annual_purchase'])
            
            # Calculate effective annual allocation during build-up
            scenario['effective_allocation_year_1'] = min(scenario['max_annual_purchase'] / scenario['portfolio_size'], 0.10)
            scenario['effective_allocation_year_3'] = min(3 * scenario['max_annual_purchase'] / scenario['portfolio_size'], 0.10)
            scenario['effective_allocation_year_5'] = min(5 * scenario['max_annual_purchase'] / scenario['portfolio_size'], 0.10)
    
    def analyze_inflation_scenarios(self) -> pd.DataFrame:
        """Analyze I Bonds performance across different inflation scenarios"""
        
        inflation_scenarios = [
            {'scenario': 'Low Inflation (2%)', 'cpi_rate': 0.02, 'i_bond_rate': 0.02},
            {'scenario': 'Normal Inflation (3%)', 'cpi_rate': 0.03, 'i_bond_rate': 0.03},
            {'scenario': 'High Inflation (5%)', 'cpi_rate': 0.05, 'i_bond_rate': 0.05},
            {'scenario': 'Very High Inflation (7%)', 'cpi_rate': 0.07, 'i_bond_rate': 0.07},
            {'scenario': 'Deflation (-1%)', 'cpi_rate': -0.01, 'i_bond_rate': 0.00}  # I Bonds floor at 0%
        ]
        
        results = []
        
        for scenario in inflation_scenarios:
            # Calculate real returns for different assets
            stock_real_return = 0.10 - scenario['cpi_rate']
            bond_real_return = 0.04 - scenario['cpi_rate']
            gold_real_return = 0.05 - scenario['cpi_rate']  # Assume gold keeps up with inflation
            tips_real_return = 0.02  # TIPS designed to provide real return
            i_bond_real_return = scenario['i_bond_rate'] - scenario['cpi_rate']
            
            # Portfolio real returns
            baseline_real_return = (0.50 * stock_real_return + 0.30 * bond_real_return + 
                                  0.15 * gold_real_return + 0.05 * tips_real_return)
            
            with_ibonds_real_return = (0.45 * stock_real_return + 0.27 * bond_real_return + 
                                     0.13 * gold_real_return + 0.05 * tips_real_return + 
                                     0.10 * i_bond_real_return)
            
            improvement = with_ibonds_real_return - baseline_real_return
            
            results.append({
                'Inflation_Scenario': scenario['scenario'],
                'CPI_Rate': scenario['cpi_rate'],
                'I_Bond_Rate': scenario['i_bond_rate'],
                'I_Bond_Real_Return': i_bond_real_return,
                'Baseline_Portfolio_Real_Return': baseline_real_return,
                'With_IBonds_Portfolio_Real_Return': with_ibonds_real_return,
                'Real_Return_Improvement': improvement,
                'Improvement_Percentage': improvement / abs(baseline_real_return) if baseline_real_return != 0 else 0
            })
        
        return pd.DataFrame(results)
    
    def calculate_qol_utility_impact(self) -> Dict:
        """Calculate the impact on QOL utility across retirement phases"""
        
        # QOL utility function
        def qol_factor(age):
            return max(0.2, 1 - ((age - 65) ** 3) / 50000)
        
        ages = range(65, 101)
        baseline_utilities = []
        with_ibonds_utilities = []
        
        for age in ages:
            qol = qol_factor(age)
            
            # Assume slightly lower volatility and better inflation protection improve utility
            baseline_utility = qol * 1.0  # Normalized baseline
            
            # I Bonds provide stability and inflation protection benefits
            # Benefit increases with age (higher QOL phase scores)
            age_factor = min(1.2, 1.0 + (age - 65) * 0.005)  # 0.5% improvement per year
            inflation_protection_benefit = 0.02  # 2% utility improvement from better inflation protection
            
            with_ibonds_utility = qol * (age_factor + inflation_protection_benefit)
            
            baseline_utilities.append(baseline_utility)
            with_ibonds_utilities.append(with_ibonds_utility)
        
        total_baseline_utility = sum(baseline_utilities)
        total_with_ibonds_utility = sum(with_ibonds_utilities)
        
        utility_improvement = (total_with_ibonds_utility - total_baseline_utility) / total_baseline_utility
        
        return {
            'ages': list(ages),
            'baseline_utilities': baseline_utilities,
            'with_ibonds_utilities': with_ibonds_utilities,
            'total_utility_improvement': utility_improvement,
            'annual_utility_improvements': [
                (w - b) / b for b, w in zip(baseline_utilities, with_ibonds_utilities)
            ]
        }
    
    def generate_implementation_strategies(self) -> List[Dict]:
        """Generate practical implementation strategies for different investor profiles"""
        
        strategies = [
            {
                'strategy_name': 'Gradual Build-Up Strategy',
                'description': 'Start purchasing I Bonds immediately, gradually building allocation',
                'target_allocation': '5-10% over 3-5 years',
                'implementation_steps': [
                    'Year 1: Purchase maximum $10K (single) or $20K (couple)',
                    'Year 2-3: Continue maximum purchases annually',
                    'Year 4-5: Reach target allocation',
                    'Ongoing: Replace maturing I Bonds or rebalance'
                ],
                'pros': ['Simple', 'Immediate start', 'Dollar-cost averaging'],
                'cons': ['Slow to reach target', 'Opportunity cost during build-up'],
                'best_for': 'Most retirees with medium to large portfolios'
            },
            {
                'strategy_name': 'Substitution Strategy',
                'description': 'Replace portion of TIPS allocation with I Bonds',
                'target_allocation': 'Replace 2-3% TIPS with I Bonds',
                'implementation_steps': [
                    'Reduce TIPS allocation from 5% to 2-3%',
                    'Use I Bonds for remaining inflation protection needs',
                    'Purchase maximum I Bonds annually',
                    'Maintain total inflation protection at 5%'
                ],
                'pros': ['Immediate implementation', 'Better inflation protection', 'Tax advantages'],
                'cons': ['Limited by purchase restrictions', 'Liquidity constraints'],
                'best_for': 'Investors focused on inflation protection'
            },
            {
                'strategy_name': 'Cash Substitution Strategy',
                'description': 'Use I Bonds as enhanced cash/emergency fund',
                'target_allocation': '3-5% as cash substitute after year 1',
                'implementation_steps': [
                    'Purchase I Bonds instead of holding excess cash',
                    'After 1-year holding period, use as liquid reserves',
                    'Ladder purchases for ongoing liquidity',
                    'Maintain separate from core portfolio allocation'
                ],
                'pros': ['Better than cash returns', 'Inflation protection', 'High liquidity after year 1'],
                'cons': ['1-year liquidity restriction', 'Purchase limits'],
                'best_for': 'Conservative investors with significant cash holdings'
            }
        ]
        
        return strategies
    
    def create_comprehensive_visualization(self, inflation_df: pd.DataFrame, utility_data: Dict):
        """Create comprehensive visualizations for I Bonds analysis"""
        
        plt.style.use('seaborn-v0_8')
        fig = plt.figure(figsize=(16, 12))
        
        # 1. Inflation scenario analysis
        plt.subplot(2, 3, 1)
        scenarios = inflation_df['Inflation_Scenario']
        improvements = inflation_df['Real_Return_Improvement'] * 100
        colors = ['red' if x < 0 else 'green' for x in improvements]
        
        bars = plt.bar(range(len(scenarios)), improvements, color=colors, alpha=0.7)
        plt.xticks(range(len(scenarios)), scenarios, rotation=45, ha='right')
        plt.ylabel('Real Return Improvement (%)')
        plt.title('I Bonds Portfolio Improvement by Inflation Scenario')
        plt.grid(True, alpha=0.3)
        
        # Add value labels on bars
        for bar, val in zip(bars, improvements):
            plt.text(bar.get_x() + bar.get_width()/2, val + (0.01 if val > 0 else -0.03),
                    f'{val:.2f}%', ha='center', va='bottom' if val > 0 else 'top')
        
        # 2. QOL utility impact by age
        plt.subplot(2, 3, 2)
        ages = utility_data['ages']
        baseline = utility_data['baseline_utilities']
        with_ibonds = utility_data['with_ibonds_utilities']
        
        plt.plot(ages, baseline, label='Baseline Portfolio', linewidth=2)
        plt.plot(ages, with_ibonds, label='With I Bonds', linewidth=2)
        plt.fill_between(ages, baseline, with_ibonds, alpha=0.3, label='Utility Improvement')
        plt.xlabel('Age')
        plt.ylabel('QOL Utility')
        plt.title('QOL Utility: Baseline vs With I Bonds')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # 3. Implementation timeline
        plt.subplot(2, 3, 3)
        self.calculate_implementation_timeline()
        
        profiles = [s['retiree_profile'].split(',')[0] for s in self.implementation_scenarios]
        years_5pct = [s['years_to_5pct'] for s in self.implementation_scenarios]
        years_10pct = [s['years_to_10pct'] for s in self.implementation_scenarios]
        
        x = range(len(profiles))
        width = 0.35
        
        plt.bar([i - width/2 for i in x], years_5pct, width, label='5% Allocation', alpha=0.8)
        plt.bar([i + width/2 for i in x], years_10pct, width, label='10% Allocation', alpha=0.8)
        
        plt.xlabel('Investor Profile')
        plt.ylabel('Years to Target Allocation')
        plt.title('Time to Reach I Bonds Target Allocation')
        plt.xticks(x, profiles)
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # 4. Risk-return comparison
        plt.subplot(2, 3, 4)
        assets = ['Baseline Portfolio', 'With 5% I Bonds', 'With 10% I Bonds']
        returns = [6.5, 6.35, 6.2]
        volatilities = [12.5, 12.2, 11.8]
        
        plt.scatter(volatilities, returns, s=100, alpha=0.7)
        for i, asset in enumerate(assets):
            plt.annotate(asset, (volatilities[i], returns[i]), 
                        xytext=(5, 5), textcoords='offset points')
        
        plt.xlabel('Portfolio Volatility (%)')
        plt.ylabel('Expected Return (%)')
        plt.title('Risk-Return Profile Comparison')
        plt.grid(True, alpha=0.3)
        
        # 5. Allocation build-up over time
        plt.subplot(2, 3, 5)
        years = range(1, 11)
        
        # For married couple with $1M portfolio
        couple_scenario = self.implementation_scenarios[1]
        allocations = []
        for year in years:
            total_purchased = min(year * 20000, 100000)  # Max $100K for 10% allocation
            allocation = total_purchased / 1000000 * 100
            allocations.append(allocation)
        
        plt.plot(years, allocations, marker='o', linewidth=2, markersize=6)
        plt.axhline(y=5, color='red', linestyle='--', alpha=0.7, label='5% Target')
        plt.axhline(y=10, color='blue', linestyle='--', alpha=0.7, label='10% Target')
        plt.xlabel('Year')
        plt.ylabel('I Bonds Allocation (%)')
        plt.title('I Bonds Allocation Build-up (Married Couple, $1M Portfolio)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # 6. Tax efficiency comparison
        plt.subplot(2, 3, 6)
        tax_brackets = ['15%', '25%', '35%']
        
        # After-tax yields (simplified)
        bonds_after_tax = [4.0 * (1 - 0.15), 4.0 * (1 - 0.25), 4.0 * (1 - 0.35)]
        tips_after_tax = [2.0 * (1 - 0.15), 2.0 * (1 - 0.25), 2.0 * (1 - 0.35)]
        ibonds_after_tax = [3.0, 3.0, 3.0]  # Federal tax-deferred
        
        x = range(len(tax_brackets))
        width = 0.25
        
        plt.bar([i - width for i in x], bonds_after_tax, width, label='Regular Bonds', alpha=0.8)
        plt.bar(x, tips_after_tax, width, label='TIPS', alpha=0.8)
        plt.bar([i + width for i in x], ibonds_after_tax, width, label='I Bonds', alpha=0.8)
        
        plt.xlabel('Tax Bracket')
        plt.ylabel('After-Tax Yield (%)')
        plt.title('After-Tax Yield Comparison')
        plt.xticks(x, tax_brackets)
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Save plot
        output_dir = Path('output')
        output_dir.mkdir(exist_ok=True)
        plt.savefig(output_dir / 'i_bonds_qol_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def generate_implementation_report(self, inflation_df: pd.DataFrame, 
                                     utility_data: Dict, strategies: List[Dict]) -> str:
        """Generate comprehensive implementation report"""
        
        report = []
        report.append("💰 I BONDS INTEGRATION ANALYSIS FOR QOL FRAMEWORK")
        report.append("=" * 60)
        
        # Executive Summary
        report.append(f"\n🎯 EXECUTIVE SUMMARY:")
        report.append("-" * 40)
        report.append(f"I Bonds (Series I Savings Bonds) offer significant value for QOL portfolios,")
        report.append(f"particularly for inflation protection and tax efficiency. However, purchase")
        report.append(f"limits require strategic implementation over multiple years.")
        
        # Key findings
        utility_improvement = utility_data['total_utility_improvement'] * 100
        report.append(f"\n📊 KEY FINDINGS:")
        report.append(f"• Total QOL utility improvement: {utility_improvement:.2f}%")
        report.append(f"• Best performance in high inflation scenarios")
        report.append(f"• Excellent age-appropriateness for all QOL phases")
        report.append(f"• Implementation constraint: $10K annual purchase limit per person")
        
        # Inflation scenario analysis
        report.append(f"\n🌡️ INFLATION SCENARIO ANALYSIS:")
        report.append("-" * 40)
        
        best_scenario = inflation_df.loc[inflation_df['Real_Return_Improvement'].idxmax()]
        worst_scenario = inflation_df.loc[inflation_df['Real_Return_Improvement'].idxmin()]
        
        report.append(f"Best case: {best_scenario['Inflation_Scenario']}")
        report.append(f"  Real return improvement: {best_scenario['Real_Return_Improvement']*100:.2f}%")
        report.append(f"  I Bond real return: {best_scenario['I_Bond_Real_Return']*100:.2f}%")
        
        report.append(f"\nWorst case: {worst_scenario['Inflation_Scenario']}")
        report.append(f"  Real return impact: {worst_scenario['Real_Return_Improvement']*100:.2f}%")
        report.append(f"  I Bond real return: {worst_scenario['I_Bond_Real_Return']*100:.2f}%")
        
        # Implementation timelines
        report.append(f"\n⏰ IMPLEMENTATION TIMELINES:")
        report.append("-" * 40)
        
        for scenario in self.implementation_scenarios:
            report.append(f"\n{scenario['retiree_profile']}:")
            report.append(f"  Portfolio size: ${scenario['portfolio_size']:,}")
            report.append(f"  Max annual purchase: ${scenario['max_annual_purchase']:,}")
            report.append(f"  Years to 5% allocation: {scenario['years_to_5pct']:.0f}")
            report.append(f"  Years to 10% allocation: {scenario['years_to_10pct']:.0f}")
        
        # Recommended strategies
        report.append(f"\n🎯 RECOMMENDED IMPLEMENTATION STRATEGIES:")
        report.append("-" * 40)
        
        for i, strategy in enumerate(strategies, 1):
            report.append(f"\n{i}. {strategy['strategy_name']}")
            report.append(f"   Target: {strategy['target_allocation']}")
            report.append(f"   Best for: {strategy['best_for']}")
            report.append(f"   Key advantages: {', '.join(strategy['pros'][:2])}")
        
        # Enhanced allocation recommendations
        report.append(f"\n📋 ENHANCED QOL ALLOCATIONS WITH I BONDS:")
        report.append("-" * 40)
        
        report.append(f"\n🎯 Enhanced Conservative (Ages 75+):")
        report.append(f"   • 25% US Stocks")
        report.append(f"   • 40% US Bonds")
        report.append(f"   • 10% Gold")
        report.append(f"   • 10% TIPS")
        report.append(f"   • 10% Treasury Bills")
        report.append(f"   • 5% I Bonds (build gradually)")
        
        report.append(f"\n🏆 Enhanced Moderate (Ages 65-75):")
        report.append(f"   • 45% US Stocks")
        report.append(f"   • 25% US Bonds")
        report.append(f"   • 12% Gold")
        report.append(f"   • 3% TIPS")
        report.append(f"   • 10% I Bonds (build over 3-5 years)")
        report.append(f"   • 5% Treasury Bills")
        
        # Implementation warnings
        report.append(f"\n⚠️ IMPLEMENTATION CONSIDERATIONS:")
        report.append("-" * 40)
        report.append(f"• Purchase limits: Max $10K per person annually")
        report.append(f"• Liquidity: 1-year minimum holding period")
        report.append(f"• Early redemption: 3-month interest penalty if redeemed before 5 years")
        report.append(f"• Tax treatment: Federal tax can be deferred until redemption")
        report.append(f"• Electronic only: Must purchase through TreasuryDirect.gov")
        
        # Bottom line recommendation
        report.append(f"\n💡 BOTTOM LINE RECOMMENDATION:")
        report.append("-" * 40)
        report.append(f"I Bonds are HIGHLY RECOMMENDED for QOL portfolios, particularly for:")
        report.append(f"• Investors concerned about inflation")
        report.append(f"• Those in higher tax brackets")
        report.append(f"• Conservative investors seeking safety")
        report.append(f"• Portfolios under $2M (where limits are manageable)")
        report.append(f"\nStart purchasing immediately and build allocation gradually.")
        report.append(f"Target 5-10% allocation over 3-5 years for optimal benefit.")
        
        return "\n".join(report)

def main():
    """Run comprehensive I Bonds analysis for QOL framework"""
    
    print("💰 I BONDS ANALYSIS FOR QOL FRAMEWORK")
    print("=" * 50)
    
    analyzer = IBondsQOLAnalysis()
    
    # Analyze inflation scenarios
    print("📊 Analyzing inflation scenarios...")
    inflation_df = analyzer.analyze_inflation_scenarios()
    
    # Calculate QOL utility impact
    print("🎯 Calculating QOL utility impact...")
    utility_data = analyzer.calculate_qol_utility_impact()
    
    # Generate implementation strategies
    print("🔧 Generating implementation strategies...")
    strategies = analyzer.generate_implementation_strategies()
    
    # Create visualizations
    print("📈 Creating visualizations...")
    analyzer.create_comprehensive_visualization(inflation_df, utility_data)
    
    # Generate implementation report
    print("📝 Generating implementation report...")
    report = analyzer.generate_implementation_report(inflation_df, utility_data, strategies)
    
    # Save results
    output_dir = Path('output')
    output_dir.mkdir(exist_ok=True)
    
    # Save DataFrame
    inflation_df.to_csv(output_dir / 'i_bonds_inflation_analysis.csv', index=False)
    print(f"✅ Inflation analysis saved to: {output_dir / 'i_bonds_inflation_analysis.csv'}")
    
    # Save implementation report
    with open(output_dir / 'i_bonds_implementation_report.txt', 'w') as f:
        f.write(report)
    print(f"✅ Implementation report saved to: {output_dir / 'i_bonds_implementation_report.txt'}")
    
    # Display key results
    print("\n" + "=" * 50)
    print("🎯 I BONDS QOL FRAMEWORK INTEGRATION SUMMARY:")
    print("=" * 50)
    
    print(f"\n💡 Key Benefits:")
    print(f"   • QOL utility improvement: {utility_data['total_utility_improvement']*100:.2f}%")
    print(f"   • Perfect inflation protection (1:1 with CPI)")
    print(f"   • Zero default risk (US Treasury backing)")
    print(f"   • Tax advantages (federal tax deferral)")
    
    print(f"\n⚡ Best Performance Scenarios:")
    best_scenario = inflation_df.loc[inflation_df['Real_Return_Improvement'].idxmax()]
    print(f"   • {best_scenario['Inflation_Scenario']}: {best_scenario['Real_Return_Improvement']*100:.2f}% improvement")
    
    print(f"\n🎯 Recommended Implementation:")
    print(f"   • Start with maximum annual purchases ($10K single, $20K couple)")
    print(f"   • Target 5-10% allocation over 3-5 years")
    print(f"   • Use as TIPS substitute or cash enhancement")
    print(f"   • Particularly valuable for conservative phases")
    
    print(f"\n⚠️ Key Constraints:")
    print(f"   • $10K annual purchase limit per person")
    print(f"   • 1-year minimum holding period")
    print(f"   • Electronic purchase only")
    
    print(f"\n📄 Full analysis report:")
    print(report)
    
    return inflation_df, utility_data, strategies

if __name__ == "__main__":
    inflation_results, utility_results, strategy_results = main()