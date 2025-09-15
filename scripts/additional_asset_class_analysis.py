#!/usr/bin/env python3
"""
ADDITIONAL ASSET CLASS UTILITY ANALYSIS FOR QOL FRAMEWORK

Analyzes potential additional asset classes and instruments that could enhance
the Quality of Life retirement framework beyond stocks, bonds, gold, and TIPS.
"""

import sys
import os
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent / 'src'))

class AdditionalAssetAnalysis:
    """
    Analysis of additional asset classes for QOL framework enhancement
    """
    
    def __init__(self):
        """Initialize analysis parameters"""
        
        # Historical return/risk estimates (annual)
        self.asset_characteristics = {
            # Current QOL assets
            'US_Stocks': {
                'return': 0.10, 'volatility': 0.20, 'inflation_beta': 0.3,
                'liquidity': 1.0, 'complexity': 0.1, 'tax_efficiency': 0.7,
                'correlation_stocks': 1.0, 'correlation_bonds': -0.2,
                'crisis_performance': -0.4, 'age_suitability': 0.8
            },
            'US_Bonds': {
                'return': 0.04, 'volatility': 0.06, 'inflation_beta': -0.5,
                'liquidity': 0.9, 'complexity': 0.1, 'tax_efficiency': 0.5,
                'correlation_stocks': -0.2, 'correlation_bonds': 1.0,
                'crisis_performance': 0.1, 'age_suitability': 0.9
            },
            'Gold': {
                'return': 0.05, 'volatility': 0.20, 'inflation_beta': 0.8,
                'liquidity': 0.8, 'complexity': 0.2, 'tax_efficiency': 0.3,
                'correlation_stocks': 0.1, 'correlation_bonds': -0.1,
                'crisis_performance': 0.2, 'age_suitability': 0.6
            },
            'TIPS': {
                'return': 0.02, 'volatility': 0.08, 'inflation_beta': 1.0,
                'liquidity': 0.8, 'complexity': 0.3, 'tax_efficiency': 0.6,
                'correlation_stocks': 0.0, 'correlation_bonds': 0.4,
                'crisis_performance': 0.05, 'age_suitability': 0.8
            },
            
            # Potential additional assets
            'REITs': {
                'return': 0.08, 'volatility': 0.25, 'inflation_beta': 0.6,
                'liquidity': 0.9, 'complexity': 0.2, 'tax_efficiency': 0.4,
                'correlation_stocks': 0.7, 'correlation_bonds': 0.1,
                'crisis_performance': -0.3, 'age_suitability': 0.7,
                'income_generation': 0.9, 'real_asset': 1.0
            },
            'International_Stocks': {
                'return': 0.09, 'volatility': 0.22, 'inflation_beta': 0.4,
                'liquidity': 0.9, 'complexity': 0.3, 'tax_efficiency': 0.6,
                'correlation_stocks': 0.8, 'correlation_bonds': -0.1,
                'crisis_performance': -0.35, 'age_suitability': 0.7,
                'diversification': 0.8, 'currency_hedge': 0.3
            },
            'Emerging_Markets': {
                'return': 0.11, 'volatility': 0.28, 'inflation_beta': 0.5,
                'liquidity': 0.7, 'complexity': 0.4, 'tax_efficiency': 0.5,
                'correlation_stocks': 0.7, 'correlation_bonds': 0.0,
                'crisis_performance': -0.5, 'age_suitability': 0.4,
                'diversification': 0.9, 'growth_potential': 0.9
            },
            'Commodities': {
                'return': 0.06, 'volatility': 0.25, 'inflation_beta': 0.9,
                'liquidity': 0.6, 'complexity': 0.6, 'tax_efficiency': 0.3,
                'correlation_stocks': 0.3, 'correlation_bonds': -0.2,
                'crisis_performance': 0.1, 'age_suitability': 0.5,
                'inflation_hedge': 1.0, 'diversification': 0.8
            },
            'I_Bonds': {
                'return': 0.03, 'volatility': 0.02, 'inflation_beta': 1.0,
                'liquidity': 0.3, 'complexity': 0.4, 'tax_efficiency': 0.9,
                'correlation_stocks': 0.0, 'correlation_bonds': 0.2,
                'crisis_performance': 0.0, 'age_suitability': 0.9,
                'inflation_protection': 1.0, 'safety': 1.0
            },
            'Treasury_Bills': {
                'return': 0.025, 'volatility': 0.005, 'inflation_beta': 0.8,
                'liquidity': 1.0, 'complexity': 0.1, 'tax_efficiency': 0.7,
                'correlation_stocks': 0.0, 'correlation_bonds': 0.3,
                'crisis_performance': 0.0, 'age_suitability': 1.0,
                'safety': 1.0, 'liquidity_premium': 1.0
            },
            'High_Yield_Bonds': {
                'return': 0.06, 'volatility': 0.12, 'inflation_beta': 0.2,
                'liquidity': 0.7, 'complexity': 0.3, 'tax_efficiency': 0.4,
                'correlation_stocks': 0.5, 'correlation_bonds': 0.6,
                'crisis_performance': -0.2, 'age_suitability': 0.6,
                'income_generation': 0.9, 'yield_pickup': 0.8
            },
            'Bank_Loans': {
                'return': 0.055, 'volatility': 0.08, 'inflation_beta': 0.7,
                'liquidity': 0.4, 'complexity': 0.5, 'tax_efficiency': 0.4,
                'correlation_stocks': 0.3, 'correlation_bonds': 0.4,
                'crisis_performance': -0.1, 'age_suitability': 0.7,
                'floating_rate': 1.0, 'income_generation': 0.8
            },
            'Preferred_Stocks': {
                'return': 0.065, 'volatility': 0.15, 'inflation_beta': 0.1,
                'liquidity': 0.6, 'complexity': 0.4, 'tax_efficiency': 0.7,
                'correlation_stocks': 0.6, 'correlation_bonds': 0.5,
                'crisis_performance': -0.25, 'age_suitability': 0.7,
                'income_generation': 0.9, 'dividend_priority': 0.8
            },
            'Dividend_Stocks': {
                'return': 0.095, 'volatility': 0.16, 'inflation_beta': 0.4,
                'liquidity': 0.9, 'complexity': 0.2, 'tax_efficiency': 0.8,
                'correlation_stocks': 0.9, 'correlation_bonds': 0.0,
                'crisis_performance': -0.25, 'age_suitability': 0.8,
                'income_generation': 0.9, 'dividend_growth': 0.7
            },
            'Value_Stocks': {
                'return': 0.105, 'volatility': 0.18, 'inflation_beta': 0.5,
                'liquidity': 0.9, 'complexity': 0.2, 'tax_efficiency': 0.7,
                'correlation_stocks': 0.85, 'correlation_bonds': -0.1,
                'crisis_performance': -0.3, 'age_suitability': 0.7,
                'factor_premium': 0.8, 'contrarian_nature': 0.8
            },
            'Small_Cap_Stocks': {
                'return': 0.115, 'volatility': 0.24, 'inflation_beta': 0.4,
                'liquidity': 0.8, 'complexity': 0.3, 'tax_efficiency': 0.7,
                'correlation_stocks': 0.8, 'correlation_bonds': -0.1,
                'crisis_performance': -0.45, 'age_suitability': 0.5,
                'factor_premium': 0.8, 'growth_potential': 0.9
            }
        }
        
        # QOL-specific criteria weights
        self.qol_weights = {
            'utility_enhancement': 0.25,    # How much it improves QOL utility
            'age_appropriateness': 0.20,    # Suitability for older investors
            'implementation_ease': 0.15,    # Simplicity for retirees
            'income_generation': 0.15,      # Provides regular income
            'inflation_protection': 0.10,   # Protects against inflation
            'crisis_resilience': 0.10,      # Performance during downturns
            'diversification': 0.05         # Correlation benefits
        }
        
        # Enhanced QOL phases
        self.qol_phases = {
            'Phase_1_65_75': {
                'withdrawal_rate': 0.054,
                'risk_tolerance': 0.7,
                'income_need': 0.6,
                'complexity_tolerance': 0.7,
                'liquidity_need': 0.6
            },
            'Phase_2_75_85': {
                'withdrawal_rate': 0.045,
                'risk_tolerance': 0.5,
                'income_need': 0.8,
                'complexity_tolerance': 0.5,
                'liquidity_need': 0.7
            },
            'Phase_3_85_plus': {
                'withdrawal_rate': 0.035,
                'risk_tolerance': 0.3,
                'income_need': 0.9,
                'complexity_tolerance': 0.3,
                'liquidity_need': 0.9
            }
        }
    
    def calculate_qol_utility_score(self, asset: str) -> float:
        """Calculate QOL-specific utility score for an asset"""
        
        char = self.asset_characteristics[asset]
        
        # Utility enhancement (risk-adjusted return + special features)
        risk_adj_return = char['return'] / char['volatility']
        utility_enhancement = risk_adj_return * 0.6
        
        # Add special features
        if 'income_generation' in char:
            utility_enhancement += char['income_generation'] * 0.2
        if 'inflation_hedge' in char:
            utility_enhancement += char['inflation_hedge'] * 0.1
        if 'safety' in char:
            utility_enhancement += char['safety'] * 0.1
            
        utility_enhancement = min(1.0, utility_enhancement)
        
        # Age appropriateness
        age_score = char['age_suitability']
        
        # Implementation ease (inverse of complexity, plus liquidity)
        implementation_score = (1 - char['complexity']) * 0.6 + char['liquidity'] * 0.4
        
        # Income generation
        income_score = char.get('income_generation', 0.3)
        
        # Inflation protection
        inflation_score = max(0, char['inflation_beta']) * 0.6 + char.get('inflation_protection', 0.0) * 0.4
        inflation_score = min(1.0, inflation_score)
        
        # Crisis resilience (positive crisis performance + low correlation with stocks)
        crisis_score = max(0, char['crisis_performance'] + 0.5) + (1 - abs(char['correlation_stocks'])) * 0.3
        crisis_score = min(1.0, crisis_score)
        
        # Diversification (inverse correlation with existing assets)
        diversification_score = char.get('diversification', 0.5)
        
        # Calculate weighted score
        total_score = (
            utility_enhancement * self.qol_weights['utility_enhancement'] +
            age_score * self.qol_weights['age_appropriateness'] +
            implementation_score * self.qol_weights['implementation_ease'] +
            income_score * self.qol_weights['income_generation'] +
            inflation_score * self.qol_weights['inflation_protection'] +
            crisis_score * self.qol_weights['crisis_resilience'] +
            diversification_score * self.qol_weights['diversification']
        )
        
        return total_score
    
    def analyze_phase_suitability(self, asset: str) -> Dict[str, float]:
        """Analyze asset suitability for each QOL phase"""
        
        char = self.asset_characteristics[asset]
        phase_scores = {}
        
        for phase_name, phase_char in self.qol_phases.items():
            # Risk alignment
            risk_alignment = 1 - abs(char['volatility'] / 0.25 - phase_char['risk_tolerance'])
            risk_alignment = max(0, risk_alignment)
            
            # Income generation alignment
            income_alignment = char.get('income_generation', 0.3) * phase_char['income_need']
            
            # Complexity alignment
            complexity_alignment = (1 - char['complexity']) * phase_char['complexity_tolerance']
            
            # Liquidity alignment
            liquidity_alignment = char['liquidity'] * phase_char['liquidity_need']
            
            # Overall phase score
            phase_score = (
                risk_alignment * 0.4 +
                income_alignment * 0.25 +
                complexity_alignment * 0.2 +
                liquidity_alignment * 0.15
            )
            
            phase_scores[phase_name] = phase_score
        
        return phase_scores
    
    def simulate_portfolio_enhancement(self, additional_asset: str, allocation: float = 0.1) -> Dict:
        """Simulate adding an asset to the Enhanced Moderate portfolio"""
        
        # Base Enhanced Moderate: 50% stocks, 30% bonds, 15% gold, 5% TIPS
        base_allocation = {
            'US_Stocks': 0.50,
            'US_Bonds': 0.30,
            'Gold': 0.15,
            'TIPS': 0.05
        }
        
        # Create enhanced allocation by reducing proportionally
        reduction_factor = 1 - allocation
        enhanced_allocation = {k: v * reduction_factor for k, v in base_allocation.items()}
        enhanced_allocation[additional_asset] = allocation
        
        # Calculate portfolio metrics
        portfolio_return = sum(
            enhanced_allocation[asset] * self.asset_characteristics[asset]['return']
            for asset in enhanced_allocation
        )
        
        # Simplified portfolio volatility (assuming correlations)
        portfolio_variance = 0
        for asset1, weight1 in enhanced_allocation.items():
            for asset2, weight2 in enhanced_allocation.items():
                if asset1 == asset2:
                    variance = self.asset_characteristics[asset1]['volatility'] ** 2
                    portfolio_variance += weight1 * weight2 * variance
                else:
                    # Use simplified correlation estimates
                    corr = 0.3 if asset1 != asset2 else 1.0  # Simplified
                    vol1 = self.asset_characteristics[asset1]['volatility']
                    vol2 = self.asset_characteristics[asset2]['volatility']
                    portfolio_variance += weight1 * weight2 * corr * vol1 * vol2
        
        portfolio_volatility = np.sqrt(portfolio_variance)
        
        # Calculate utility metrics
        sharpe_ratio = (portfolio_return - 0.02) / portfolio_volatility  # Assuming 2% risk-free rate
        
        # Inflation protection score
        inflation_protection = sum(
            enhanced_allocation[asset] * max(0, self.asset_characteristics[asset]['inflation_beta'])
            for asset in enhanced_allocation
        )
        
        # Income generation score
        income_generation = sum(
            enhanced_allocation[asset] * self.asset_characteristics[asset].get('income_generation', 0.3)
            for asset in enhanced_allocation
        )
        
        return {
            'allocation': enhanced_allocation,
            'expected_return': portfolio_return,
            'volatility': portfolio_volatility,
            'sharpe_ratio': sharpe_ratio,
            'inflation_protection': inflation_protection,
            'income_generation': income_generation
        }
    
    def generate_comprehensive_analysis(self) -> pd.DataFrame:
        """Generate comprehensive analysis of all potential assets"""
        
        results = []
        
        for asset in self.asset_characteristics:
            if asset in ['US_Stocks', 'US_Bonds', 'Gold', 'TIPS']:
                continue  # Skip existing QOL assets
            
            # Calculate QOL utility score
            qol_score = self.calculate_qol_utility_score(asset)
            
            # Analyze phase suitability
            phase_scores = self.analyze_phase_suitability(asset)
            
            # Simulate portfolio enhancement
            portfolio_sim = self.simulate_portfolio_enhancement(asset)
            
            char = self.asset_characteristics[asset]
            
            results.append({
                'Asset': asset,
                'QOL_Utility_Score': qol_score,
                'Expected_Return': char['return'],
                'Volatility': char['volatility'],
                'Sharpe_Ratio': (char['return'] - 0.02) / char['volatility'],
                'Inflation_Beta': char['inflation_beta'],
                'Age_Suitability': char['age_suitability'],
                'Liquidity': char['liquidity'],
                'Complexity': char['complexity'],
                'Tax_Efficiency': char['tax_efficiency'],
                'Phase_1_Score': phase_scores['Phase_1_65_75'],
                'Phase_2_Score': phase_scores['Phase_2_75_85'],
                'Phase_3_Score': phase_scores['Phase_3_85_plus'],
                'Portfolio_Return_Enhancement': portfolio_sim['expected_return'] - 0.065,  # vs base
                'Portfolio_Sharpe_Enhancement': portfolio_sim['sharpe_ratio'] - 0.32,  # vs base
                'Income_Generation': char.get('income_generation', 0.3),
                'Crisis_Performance': char['crisis_performance'],
                'Implementation_Difficulty': char['complexity'] + (1 - char['liquidity']),
                'Overall_Recommendation': 'TBD'
            })
        
        df = pd.DataFrame(results)
        
        # Add recommendations based on scores
        def get_recommendation(row):
            if row['QOL_Utility_Score'] >= 0.7 and row['Implementation_Difficulty'] <= 0.6:
                return 'Highly Recommended'
            elif row['QOL_Utility_Score'] >= 0.6 and row['Implementation_Difficulty'] <= 0.7:
                return 'Recommended'
            elif row['QOL_Utility_Score'] >= 0.5:
                return 'Consider'
            else:
                return 'Not Recommended'
        
        df['Overall_Recommendation'] = df.apply(get_recommendation, axis=1)
        
        return df.sort_values('QOL_Utility_Score', ascending=False)
    
    def create_visualizations(self, df: pd.DataFrame):
        """Create comprehensive visualizations"""
        
        plt.style.use('seaborn-v0_8')
        fig = plt.figure(figsize=(20, 16))
        
        # 1. QOL Utility Score vs Implementation Difficulty
        plt.subplot(3, 3, 1)
        scatter = plt.scatter(df['Implementation_Difficulty'], df['QOL_Utility_Score'], 
                            c=df['Age_Suitability'], s=100, alpha=0.7, cmap='viridis')
        plt.xlabel('Implementation Difficulty')
        plt.ylabel('QOL Utility Score')
        plt.title('QOL Utility vs Implementation Difficulty')
        plt.colorbar(scatter, label='Age Suitability')
        
        # Add asset labels
        for i, row in df.iterrows():
            plt.annotate(row['Asset'].replace('_', ' '), 
                        (row['Implementation_Difficulty'], row['QOL_Utility_Score']),
                        xytext=(5, 5), textcoords='offset points', fontsize=8)
        
        # 2. Risk-Return Profile
        plt.subplot(3, 3, 2)
        colors = {'Highly Recommended': 'green', 'Recommended': 'blue', 
                 'Consider': 'orange', 'Not Recommended': 'red'}
        for rec, group in df.groupby('Overall_Recommendation'):
            plt.scatter(group['Volatility'], group['Expected_Return'], 
                       label=rec, color=colors[rec], s=80, alpha=0.7)
        plt.xlabel('Volatility')
        plt.ylabel('Expected Return')
        plt.title('Risk-Return Profile by Recommendation')
        plt.legend()
        
        # 3. Phase Suitability Heatmap
        plt.subplot(3, 3, 3)
        phase_data = df[['Asset', 'Phase_1_Score', 'Phase_2_Score', 'Phase_3_Score']].set_index('Asset')
        sns.heatmap(phase_data, annot=True, cmap='RdYlGn', cbar_kws={'label': 'Phase Suitability'})
        plt.title('Suitability by QOL Phase')
        plt.ylabel('Asset Classes')
        
        # 4. Income Generation vs Age Suitability
        plt.subplot(3, 3, 4)
        plt.scatter(df['Income_Generation'], df['Age_Suitability'], 
                   c=df['QOL_Utility_Score'], s=100, alpha=0.7, cmap='plasma')
        plt.xlabel('Income Generation Score')
        plt.ylabel('Age Suitability Score')
        plt.title('Income Generation vs Age Suitability')
        plt.colorbar(label='QOL Utility Score')
        
        # 5. Inflation Protection vs Crisis Performance
        plt.subplot(3, 3, 5)
        plt.scatter(df['Inflation_Beta'], df['Crisis_Performance'], 
                   c=df['QOL_Utility_Score'], s=100, alpha=0.7, cmap='coolwarm')
        plt.xlabel('Inflation Beta')
        plt.ylabel('Crisis Performance')
        plt.title('Inflation Protection vs Crisis Resilience')
        plt.colorbar(label='QOL Utility Score')
        
        # 6. Top Assets by QOL Utility Score
        plt.subplot(3, 3, 6)
        top_assets = df.head(8)
        plt.barh(top_assets['Asset'], top_assets['QOL_Utility_Score'])
        plt.xlabel('QOL Utility Score')
        plt.title('Top 8 Assets by QOL Utility')
        plt.gca().invert_yaxis()
        
        # 7. Portfolio Enhancement Potential
        plt.subplot(3, 3, 7)
        plt.scatter(df['Portfolio_Return_Enhancement'], df['Portfolio_Sharpe_Enhancement'],
                   c=df['QOL_Utility_Score'], s=100, alpha=0.7, cmap='viridis')
        plt.xlabel('Portfolio Return Enhancement')
        plt.ylabel('Portfolio Sharpe Enhancement')
        plt.title('Portfolio Enhancement Potential')
        plt.colorbar(label='QOL Utility Score')
        
        # 8. Asset Characteristics Radar Chart (Top 4 assets)
        plt.subplot(3, 3, 8)
        top_4 = df.head(4)
        characteristics = ['Expected_Return', 'Age_Suitability', 'Liquidity', 
                          'Income_Generation', 'Inflation_Beta']
        
        angles = np.linspace(0, 2 * np.pi, len(characteristics), endpoint=False)
        angles = np.concatenate((angles, [angles[0]]))
        
        ax = plt.subplot(3, 3, 8, projection='polar')
        for i, (_, asset) in enumerate(top_4.iterrows()):
            values = [asset[char] for char in characteristics]
            values += [values[0]]
            ax.plot(angles, values, 'o-', linewidth=2, label=asset['Asset'])
        
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(characteristics)
        ax.set_title('Top 4 Assets - Characteristic Profile')
        plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
        
        # 9. Recommendation Distribution
        plt.subplot(3, 3, 9)
        rec_counts = df['Overall_Recommendation'].value_counts()
        plt.pie(rec_counts.values, labels=rec_counts.index, autopct='%1.1f%%')
        plt.title('Distribution of Recommendations')
        
        plt.tight_layout()
        
        # Save plot
        output_dir = Path('output')
        output_dir.mkdir(exist_ok=True)
        plt.savefig(output_dir / 'additional_asset_class_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def generate_detailed_recommendations(self, df: pd.DataFrame) -> str:
        """Generate detailed recommendations report"""
        
        report = []
        report.append("🎯 ADDITIONAL ASSET CLASS RECOMMENDATIONS FOR QOL FRAMEWORK")
        report.append("=" * 70)
        
        # Top recommendations
        highly_recommended = df[df['Overall_Recommendation'] == 'Highly Recommended']
        recommended = df[df['Overall_Recommendation'] == 'Recommended']
        
        report.append(f"\n🌟 HIGHLY RECOMMENDED ADDITIONS ({len(highly_recommended)} assets):")
        report.append("-" * 50)
        
        for _, asset in highly_recommended.iterrows():
            report.append(f"\n📈 {asset['Asset'].replace('_', ' ')}")
            report.append(f"   QOL Utility Score: {asset['QOL_Utility_Score']:.3f}")
            report.append(f"   Expected Return: {asset['Expected_Return']:.1%}")
            report.append(f"   Volatility: {asset['Volatility']:.1%}")
            report.append(f"   Age Suitability: {asset['Age_Suitability']:.1%}")
            report.append(f"   Income Generation: {asset['Income_Generation']:.1%}")
            report.append(f"   Implementation Difficulty: {asset['Implementation_Difficulty']:.2f}")
            
            # Phase recommendations
            best_phase = max(
                ['Phase_1_Score', 'Phase_2_Score', 'Phase_3_Score'],
                key=lambda x: asset[x]
            )
            phase_name = best_phase.replace('_Score', '').replace('_', ' ')
            report.append(f"   Best suited for: {phase_name} ({asset[best_phase]:.2f} score)")
        
        report.append(f"\n💡 RECOMMENDED ADDITIONS ({len(recommended)} assets):")
        report.append("-" * 50)
        
        for _, asset in recommended.iterrows():
            report.append(f"\n📊 {asset['Asset'].replace('_', ' ')}")
            report.append(f"   QOL Utility Score: {asset['QOL_Utility_Score']:.3f}")
            # Identify key strength
            if asset['Income_Generation'] >= 0.8:
                report.append(f"   Key Strength: High income generation")
            elif asset['Inflation_Beta'] >= 0.7:
                report.append(f"   Key Strength: Strong inflation protection")
            elif asset['Age_Suitability'] >= 0.8:
                report.append(f"   Key Strength: Age-appropriate characteristics")
            else:
                report.append(f"   Key Strength: Balanced characteristics")
        
        # Implementation guidance
        report.append(f"\n🔧 IMPLEMENTATION GUIDANCE:")
        report.append("-" * 50)
        
        if len(highly_recommended) > 0:
            top_asset = highly_recommended.iloc[0]
            report.append(f"\n🎯 Start with: {top_asset['Asset'].replace('_', ' ')}")
            report.append(f"   Suggested allocation: 5-15% of portfolio")
            report.append(f"   Implementation: Use low-cost index funds/ETFs")
            report.append(f"   Best timing: During regular rebalancing")
        
        # Enhanced allocation suggestions
        report.append(f"\n📋 ENHANCED QOL ALLOCATION SUGGESTIONS:")
        report.append("-" * 50)
        
        report.append("\n🏆 Enhanced Conservative (Ages 75+):")
        report.append("   • 25% US Stocks")
        report.append("   • 45% US Bonds")
        report.append("   • 10% Gold")
        report.append("   • 10% TIPS")
        if len(highly_recommended) > 0:
            top_asset = highly_recommended.iloc[0]['Asset'].replace('_', ' ')
            report.append(f"   • 10% {top_asset}")
        
        report.append("\n🎯 Enhanced Moderate (Ages 65-75):")
        report.append("   • 45% US Stocks")
        report.append("   • 25% US Bonds")
        report.append("   • 10% Gold")
        report.append("   • 5% TIPS")
        if len(highly_recommended) >= 2:
            asset1 = highly_recommended.iloc[0]['Asset'].replace('_', ' ')
            asset2 = highly_recommended.iloc[1]['Asset'].replace('_', ' ')
            report.append(f"   • 10% {asset1}")
            report.append(f"   • 5% {asset2}")
        
        # Warnings and considerations
        report.append(f"\n⚠️  IMPLEMENTATION WARNINGS:")
        report.append("-" * 50)
        
        complex_assets = df[df['Complexity'] >= 0.5]
        if len(complex_assets) > 0:
            report.append("\n🔴 Complex Assets (Consider Carefully):")
            for _, asset in complex_assets.iterrows():
                report.append(f"   • {asset['Asset'].replace('_', ' ')}: Complexity {asset['Complexity']:.1%}")
        
        low_liquidity = df[df['Liquidity'] <= 0.6]
        if len(low_liquidity) > 0:
            report.append("\n🟡 Lower Liquidity Assets:")
            for _, asset in low_liquidity.iterrows():
                report.append(f"   • {asset['Asset'].replace('_', ' ')}: Liquidity {asset['Liquidity']:.1%}")
        
        report.append(f"\n📊 QUANTITATIVE IMPACT ANALYSIS:")
        report.append("-" * 50)
        
        if len(highly_recommended) > 0:
            top_asset = highly_recommended.iloc[0]
            report.append(f"\nAdding 10% {top_asset['Asset'].replace('_', ' ')} to Enhanced Moderate:")
            report.append(f"   Portfolio return change: {top_asset['Portfolio_Return_Enhancement']:+.2%}")
            report.append(f"   Sharpe ratio change: {top_asset['Portfolio_Sharpe_Enhancement']:+.3f}")
            report.append(f"   Income generation improvement: Significant")
        
        return "\n".join(report)

def main():
    """Run comprehensive additional asset class analysis"""
    
    print("🔍 ANALYZING ADDITIONAL ASSET CLASSES FOR QOL FRAMEWORK")
    print("=" * 60)
    
    analyzer = AdditionalAssetAnalysis()
    
    # Generate comprehensive analysis
    print("📊 Generating comprehensive asset analysis...")
    df = analyzer.generate_comprehensive_analysis()
    
    # Create visualizations
    print("📈 Creating visualizations...")
    analyzer.create_visualizations(df)
    
    # Generate detailed recommendations
    print("📝 Generating detailed recommendations...")
    recommendations = analyzer.generate_detailed_recommendations(df)
    
    # Save results
    output_dir = Path('output')
    output_dir.mkdir(exist_ok=True)
    
    # Save DataFrame
    df.to_csv(output_dir / 'additional_asset_analysis.csv', index=False)
    print(f"✅ Analysis saved to: {output_dir / 'additional_asset_analysis.csv'}")
    
    # Save recommendations
    with open(output_dir / 'additional_asset_recommendations.txt', 'w') as f:
        f.write(recommendations)
    print(f"✅ Recommendations saved to: {output_dir / 'additional_asset_recommendations.txt'}")
    
    # Display top results
    print("\n" + "=" * 60)
    print("TOP 5 ASSET RECOMMENDATIONS BY QOL UTILITY SCORE:")
    print("=" * 60)
    
    top_5 = df.head(5)
    for i, (_, asset) in enumerate(top_5.iterrows(), 1):
        print(f"\n{i}. {asset['Asset'].replace('_', ' ')}")
        print(f"   QOL Utility Score: {asset['QOL_Utility_Score']:.3f}")
        print(f"   Recommendation: {asset['Overall_Recommendation']}")
        print(f"   Key Metrics: {asset['Expected_Return']:.1%} return, {asset['Volatility']:.1%} volatility")
        best_phase = max(['Phase_1_Score', 'Phase_2_Score', 'Phase_3_Score'],
                        key=lambda x: asset[x])
        phase_name = best_phase.replace('_Score', '').replace('_', ' ')
        print(f"   Best for: {phase_name}")
    
    print(f"\n📄 Full recommendations report:")
    print(recommendations)
    
    return df

if __name__ == "__main__":
    results_df = main()