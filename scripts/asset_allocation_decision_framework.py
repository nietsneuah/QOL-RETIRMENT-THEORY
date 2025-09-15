#!/usr/bin/env python3
"""
ASSET ALLOCATION DECISION FRAMEWORK

A comprehensive guide for making informed decisions about portfolio structure
in QOL retirement frameworks. This analysis considers utility optimization,
risk tolerance, economic scenarios, and practical implementation factors.
"""

import sys
import os
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import warnings
warnings.filterwarnings('ignore')

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent / 'src'))

@dataclass
class InvestorProfile:
    """Investor characteristics that drive allocation decisions"""
    age: int
    risk_tolerance: str  # 'conservative', 'moderate', 'aggressive'
    health_status: str   # 'excellent', 'good', 'fair', 'poor'
    spouse_status: str   # 'married', 'single', 'widowed'
    legacy_importance: str  # 'high', 'medium', 'low'
    inflation_concern: str  # 'high', 'medium', 'low'
    market_experience: str  # 'experienced', 'moderate', 'novice'
    portfolio_size: int
    other_income: int    # Pensions, Social Security, etc.
    spending_flexibility: str  # 'high', 'medium', 'low'

class AssetAllocationDecisionFramework:
    """
    Comprehensive framework for making asset allocation decisions
    """
    
    def __init__(self):
        """Initialize the decision framework"""
        
        # Define asset characteristics
        self.asset_characteristics = {
            'stocks': {
                'expected_real_return': 0.072,
                'volatility': 0.20,
                'inflation_protection': 'medium',
                'liquidity': 'high',
                'correlation_inflation': -0.3,
                'crisis_performance': 'poor_short_term',
                'tax_efficiency': 'medium',
                'complexity': 'low'
            },
            'bonds': {
                'expected_real_return': 0.025,
                'volatility': 0.08,
                'inflation_protection': 'poor',
                'liquidity': 'high',
                'correlation_inflation': -0.8,
                'crisis_performance': 'stable',
                'tax_efficiency': 'low',
                'complexity': 'low'
            },
            'gold': {
                'expected_real_return': 0.015,
                'volatility': 0.18,
                'inflation_protection': 'excellent',
                'liquidity': 'medium',
                'correlation_inflation': 0.7,
                'crisis_performance': 'excellent',
                'tax_efficiency': 'poor',
                'complexity': 'medium'
            },
            'tips': {
                'expected_real_return': 0.020,
                'volatility': 0.06,
                'inflation_protection': 'perfect',
                'liquidity': 'high',
                'correlation_inflation': 1.0,
                'crisis_performance': 'stable',
                'tax_efficiency': 'low',
                'complexity': 'medium'
            },
            'reits': {
                'expected_real_return': 0.055,
                'volatility': 0.25,
                'inflation_protection': 'good',
                'liquidity': 'medium',
                'correlation_inflation': 0.4,
                'crisis_performance': 'volatile',
                'tax_efficiency': 'low',
                'complexity': 'medium'
            },
            'commodities': {
                'expected_real_return': 0.025,
                'volatility': 0.22,
                'inflation_protection': 'excellent',
                'liquidity': 'medium',
                'correlation_inflation': 0.8,
                'crisis_performance': 'volatile',
                'tax_efficiency': 'medium',
                'complexity': 'high'
            }
        }
        
        # Define portfolio templates
        self.portfolio_templates = {
            'ultra_conservative': {
                'name': 'Ultra Conservative',
                'description': 'Maximum stability, minimal growth',
                'allocation': {'stocks': 0.20, 'bonds': 0.70, 'tips': 0.10},
                'target_demographics': ['age_80_plus', 'poor_health', 'low_risk_tolerance']
            },
            'conservative': {
                'name': 'Conservative',
                'description': 'Stability focused with modest growth',
                'allocation': {'stocks': 0.30, 'bonds': 0.60, 'gold': 0.05, 'tips': 0.05},
                'target_demographics': ['age_75_plus', 'low_risk_tolerance', 'high_inflation_concern']
            },
            'moderate': {
                'name': 'Moderate',
                'description': 'Balanced growth and stability',
                'allocation': {'stocks': 0.50, 'bonds': 0.35, 'gold': 0.10, 'tips': 0.05},
                'target_demographics': ['age_65_75', 'moderate_risk_tolerance', 'good_health']
            },
            'growth_oriented': {
                'name': 'Growth Oriented',
                'description': 'Growth focus with diversification',
                'allocation': {'stocks': 0.70, 'bonds': 0.15, 'gold': 0.10, 'tips': 0.05},
                'target_demographics': ['age_65_70', 'high_risk_tolerance', 'excellent_health']
            },
            'inflation_defensive': {
                'name': 'Inflation Defensive',
                'description': 'Maximum inflation protection',
                'allocation': {'stocks': 0.40, 'bonds': 0.20, 'gold': 0.25, 'tips': 0.15},
                'target_demographics': ['high_inflation_concern', 'long_retirement_horizon']
            },
            'legacy_focused': {
                'name': 'Legacy Focused',
                'description': 'Wealth preservation and growth for heirs',
                'allocation': {'stocks': 0.60, 'bonds': 0.25, 'gold': 0.10, 'tips': 0.05},
                'target_demographics': ['high_legacy_importance', 'large_portfolio', 'other_income']
            }
        }
        
        # Decision factors and weights
        self.decision_factors = {
            'risk_tolerance': {
                'conservative': {'stocks': -0.3, 'bonds': +0.3, 'gold': +0.1, 'tips': +0.1},
                'moderate': {'stocks': 0.0, 'bonds': 0.0, 'gold': 0.0, 'tips': 0.0},
                'aggressive': {'stocks': +0.3, 'bonds': -0.2, 'gold': -0.05, 'tips': -0.05}
            },
            'age_adjustment': {
                'young_retiree': {'stocks': +0.2, 'bonds': -0.1, 'gold': -0.05, 'tips': -0.05},
                'mid_retiree': {'stocks': 0.0, 'bonds': 0.0, 'gold': 0.0, 'tips': 0.0},
                'old_retiree': {'stocks': -0.2, 'bonds': +0.1, 'gold': +0.05, 'tips': +0.05}
            },
            'inflation_concern': {
                'high': {'stocks': -0.1, 'bonds': -0.2, 'gold': +0.2, 'tips': +0.1},
                'medium': {'stocks': 0.0, 'bonds': 0.0, 'gold': 0.0, 'tips': 0.0},
                'low': {'stocks': +0.1, 'bonds': +0.1, 'gold': -0.1, 'tips': -0.1}
            },
            'health_status': {
                'excellent': {'stocks': +0.1, 'bonds': -0.05, 'gold': -0.025, 'tips': -0.025},
                'good': {'stocks': 0.0, 'bonds': 0.0, 'gold': 0.0, 'tips': 0.0},
                'fair': {'stocks': -0.05, 'bonds': +0.025, 'gold': +0.0125, 'tips': +0.0125},
                'poor': {'stocks': -0.1, 'bonds': +0.05, 'gold': +0.025, 'tips': +0.025}
            }
        }
    
    def analyze_investor_profile(self, profile: InvestorProfile) -> Dict:
        """Analyze investor profile and recommend allocation"""
        
        print(f"\n👤 INVESTOR PROFILE ANALYSIS")
        print("=" * 50)
        print(f"Age: {profile.age}")
        print(f"Risk Tolerance: {profile.risk_tolerance}")
        print(f"Health Status: {profile.health_status}")
        print(f"Inflation Concern: {profile.inflation_concern}")
        print(f"Portfolio Size: ${profile.portfolio_size:,}")
        print(f"Other Income: ${profile.other_income:,}")
        
        # Start with moderate baseline
        base_allocation = self.portfolio_templates['moderate']['allocation'].copy()
        
        # Apply adjustments based on profile
        adjustments = {}
        for asset in base_allocation.keys():
            adjustments[asset] = 0
        
        # Risk tolerance adjustment
        risk_adj = self.decision_factors['risk_tolerance'][profile.risk_tolerance]
        for asset, adj in risk_adj.items():
            if asset in adjustments:
                adjustments[asset] += adj
        
        # Age adjustment
        if profile.age < 70:
            age_category = 'young_retiree'
        elif profile.age < 80:
            age_category = 'mid_retiree'
        else:
            age_category = 'old_retiree'
        
        age_adj = self.decision_factors['age_adjustment'][age_category]
        for asset, adj in age_adj.items():
            if asset in adjustments:
                adjustments[asset] += adj
        
        # Inflation concern adjustment
        inflation_adj = self.decision_factors['inflation_concern'][profile.inflation_concern]
        for asset, adj in inflation_adj.items():
            if asset in adjustments:
                adjustments[asset] += adj
        
        # Health status adjustment
        health_adj = self.decision_factors['health_status'][profile.health_status]
        for asset, adj in health_adj.items():
            if asset in adjustments:
                adjustments[asset] += adj
        
        # Apply adjustments and normalize
        recommended_allocation = {}
        for asset, base_weight in base_allocation.items():
            adjusted_weight = base_weight + adjustments[asset]
            recommended_allocation[asset] = max(0.05, adjusted_weight)  # Minimum 5% per asset
        
        # Normalize to 100%
        total_weight = sum(recommended_allocation.values())
        for asset in recommended_allocation:
            recommended_allocation[asset] /= total_weight
        
        return {
            'base_allocation': base_allocation,
            'adjustments': adjustments,
            'recommended_allocation': recommended_allocation,
            'age_category': age_category
        }
    
    def evaluate_allocation_scenarios(self, allocations: List[Dict], 
                                    economic_scenarios: List[str] = None) -> Dict:
        """Evaluate multiple allocations across different scenarios"""
        
        if economic_scenarios is None:
            economic_scenarios = ['normal', 'high_inflation', 'deflation', 'recession']
        
        print(f"\n📊 ALLOCATION SCENARIO ANALYSIS")
        print("=" * 50)
        
        results = {}
        
        for i, allocation in enumerate(allocations):
            allocation_name = f"Allocation_{i+1}"
            results[allocation_name] = {}
            
            for scenario in economic_scenarios:
                scenario_result = self.simulate_allocation_performance(allocation, scenario)
                results[allocation_name][scenario] = scenario_result
        
        return results
    
    def simulate_allocation_performance(self, allocation: Dict, scenario: str,
                                     n_simulations: int = 1000) -> Dict:
        """Simulate allocation performance in specific economic scenario"""
        
        # Define scenario parameters
        scenario_params = {
            'normal': {'inflation_mean': 0.03, 'inflation_std': 0.015, 'crisis_prob': 0.1},
            'high_inflation': {'inflation_mean': 0.07, 'inflation_std': 0.025, 'crisis_prob': 0.3},
            'deflation': {'inflation_mean': -0.01, 'inflation_std': 0.020, 'crisis_prob': 0.2},
            'recession': {'inflation_mean': 0.02, 'inflation_std': 0.015, 'crisis_prob': 0.4}
        }
        
        params = scenario_params[scenario]
        
        # Run simulations
        final_values = []
        total_utilities = []
        
        for sim in range(n_simulations):
            portfolio_value = 1000000  # $1M starting portfolio
            total_utility = 0
            
            for year in range(30):
                # Generate scenario-specific returns
                inflation = np.random.normal(params['inflation_mean'], params['inflation_std'])
                
                # Crisis check
                is_crisis = np.random.random() < params['crisis_prob'] / 10  # Per year probability
                
                # Asset returns
                returns = {}
                for asset in allocation.keys():
                    base_return = self.asset_characteristics[asset]['expected_real_return']
                    volatility = self.asset_characteristics[asset]['volatility']
                    inflation_sensitivity = self.asset_characteristics[asset]['correlation_inflation']
                    
                    # Adjust for inflation
                    inflation_impact = inflation_sensitivity * (inflation - 0.03)
                    
                    # Crisis impact
                    crisis_impact = 0
                    if is_crisis:
                        if asset == 'stocks':
                            crisis_impact = np.random.normal(-0.20, 0.10)
                        elif asset == 'gold':
                            crisis_impact = np.random.normal(0.10, 0.05)
                        elif asset == 'tips':
                            crisis_impact = np.random.normal(0.05, 0.02)
                    
                    asset_return = (base_return + np.random.normal(0, volatility) + 
                                  inflation_impact + crisis_impact)
                    returns[asset] = asset_return
                
                # Calculate portfolio return
                portfolio_return = sum(allocation[asset] * returns[asset] 
                                     for asset in allocation.keys())
                
                # QOL withdrawal
                if year < 10:
                    withdrawal_rate = 0.054
                elif year < 20:
                    withdrawal_rate = 0.045
                else:
                    withdrawal_rate = 0.035
                
                # Inflation-adjusted withdrawal
                real_withdrawal = 1000000 * withdrawal_rate * ((1 + inflation) ** year)
                withdrawal = min(real_withdrawal, portfolio_value * 0.95)
                
                # Calculate utility (withdrawal adjusted for QOL phase)
                if year < 10:
                    qol_multiplier = 1.35
                elif year < 20:
                    qol_multiplier = 1.125
                else:
                    qol_multiplier = 0.875
                
                utility = withdrawal * qol_multiplier
                total_utility += utility
                
                # Apply withdrawal and returns
                portfolio_value -= withdrawal
                if portfolio_value <= 0:
                    break
                
                portfolio_value *= (1 + portfolio_return)
            
            final_values.append(portfolio_value)
            total_utilities.append(total_utility)
        
        return {
            'final_values': final_values,
            'total_utilities': total_utilities,
            'success_rate': sum(1 for v in final_values if v > 0) / n_simulations,
            'median_final': np.median(final_values),
            'mean_utility': np.mean(total_utilities),
            'percentile_10': np.percentile(final_values, 10),
            'percentile_90': np.percentile(final_values, 90)
        }
    
    def create_decision_tree(self) -> str:
        """Create a decision tree for allocation choices"""
        
        decision_tree = """
        
        🌳 ASSET ALLOCATION DECISION TREE
        ═══════════════════════════════════════════════════════════════════════
        
        START: What's your primary concern?
        
        ┌─ 🛡️  WEALTH PRESERVATION (Age 75+, Poor Health)
        │   ├─ High Inflation Concern?
        │   │   ├─ YES → Ultra Conservative + TIPS (20/60/5/15)
        │   │   └─ NO → Ultra Conservative (20/70/10/0)
        │   └─ Low Risk Tolerance → Conservative (30/60/5/5)
        │
        ├─ ⚖️  BALANCED APPROACH (Age 65-75, Good Health)
        │   ├─ Market Experience?
        │   │   ├─ EXPERIENCED → Moderate (50/35/10/5)
        │   │   └─ NOVICE → Conservative+ (40/45/10/5)
        │   ├─ High Inflation Concern?
        │   │   ├─ YES → Inflation Defensive (40/20/25/15)
        │   │   └─ NO → Standard Moderate (50/35/10/5)
        │   └─ Large Portfolio (>$2M)?
        │       ├─ YES + Legacy Important → Legacy Focused (60/25/10/5)
        │       └─ NO → Standard Moderate (50/35/10/5)
        │
        ├─ 📈 GROWTH ORIENTED (Age 65-70, Excellent Health)
        │   ├─ Risk Tolerance?
        │   │   ├─ HIGH → Growth Oriented (70/15/10/5)
        │   │   └─ MODERATE → Moderate+ (60/25/10/5)
        │   ├─ Other Guaranteed Income?
        │   │   ├─ SUBSTANTIAL → Can take more risk (75/15/5/5)
        │   │   └─ LIMITED → Moderate approach (60/25/10/5)
        │   └─ Market Volatility Tolerance?
        │       ├─ HIGH → Growth Oriented (70/15/10/5)
        │       └─ MEDIUM → Balanced Growth (60/25/10/5)
        │
        └─ 🔥 INFLATION PROTECTION FOCUS
            ├─ Primary Concern = Purchasing Power?
            │   ├─ YES → Inflation Defensive (40/20/25/15)
            │   └─ PARTIAL → TIPS Heavy (50/10/15/25)
            ├─ International Exposure Desired?
            │   ├─ YES → Add Int'l Stocks (45/20/20/15)
            │   └─ NO → Domestic Focus (40/20/25/15)
            └─ Complexity Tolerance?
                ├─ HIGH → Add Commodities (35/15/25/15/10)
                └─ LOW → Keep Simple (40/20/25/15)
        
        ═══════════════════════════════════════════════════════════════════════
        
        🎯 QUICK REFERENCE GUIDE:
        
        Age-Based Starting Points:
        • 65-70: Start with 60-70% stocks
        • 70-75: Start with 50-60% stocks  
        • 75-80: Start with 30-50% stocks
        • 80+: Start with 20-30% stocks
        
        Then Adjust for:
        ✓ Risk Tolerance: ±20% stocks
        ✓ Health Status: ±10% stocks
        ✓ Inflation Concern: +10-25% Gold/TIPS
        ✓ Legacy Goals: +10% stocks, -5% bonds
        ✓ Market Experience: ±5% complexity assets
        
        Asset Allocation Ranges:
        • Stocks: 20-75% (growth engine)
        • Bonds: 10-70% (stability, rates)
        • Gold: 0-25% (inflation hedge, crisis)
        • TIPS: 0-25% (inflation protection)
        • Total Alt Assets: 10-40% max
        
        ═══════════════════════════════════════════════════════════════════════
        """
        
        return decision_tree
    
    def generate_allocation_recommendation(self, profile: InvestorProfile) -> Dict:
        """Generate comprehensive allocation recommendation"""
        
        print(f"\n🎯 COMPREHENSIVE ALLOCATION RECOMMENDATION")
        print("=" * 60)
        
        # Analyze profile
        analysis = self.analyze_investor_profile(profile)
        recommended_allocation = analysis['recommended_allocation']
        
        # Find best matching template
        best_template = self.find_best_template_match(profile)
        
        # Generate reasoning
        reasoning = self.generate_allocation_reasoning(profile, analysis)
        
        # Risk analysis
        risk_analysis = self.assess_allocation_risks(recommended_allocation)
        
        # Implementation guidance
        implementation = self.generate_implementation_guidance(recommended_allocation, profile)
        
        return {
            'recommended_allocation': recommended_allocation,
            'best_template': best_template,
            'reasoning': reasoning,
            'risk_analysis': risk_analysis,
            'implementation': implementation,
            'profile_analysis': analysis
        }
    
    def find_best_template_match(self, profile: InvestorProfile) -> str:
        """Find the best matching portfolio template"""
        
        # Score each template based on profile fit
        template_scores = {}
        
        for template_name, template in self.portfolio_templates.items():
            score = 0
            demographics = template['target_demographics']
            
            # Age scoring
            if profile.age >= 80 and 'age_80_plus' in demographics:
                score += 3
            elif profile.age >= 75 and 'age_75_plus' in demographics:
                score += 2
            elif 65 <= profile.age <= 75 and 'age_65_75' in demographics:
                score += 2
            elif 65 <= profile.age <= 70 and 'age_65_70' in demographics:
                score += 2
            
            # Risk tolerance scoring
            if f"{profile.risk_tolerance}_risk_tolerance" in demographics:
                score += 3
            
            # Health scoring
            if f"{profile.health_status}_health" in demographics:
                score += 2
            
            # Other factors
            if profile.inflation_concern == 'high' and 'high_inflation_concern' in demographics:
                score += 2
            if profile.legacy_importance == 'high' and 'high_legacy_importance' in demographics:
                score += 2
            if profile.portfolio_size > 2000000 and 'large_portfolio' in demographics:
                score += 1
            if profile.other_income > 50000 and 'other_income' in demographics:
                score += 1
            
            template_scores[template_name] = score
        
        best_template = max(template_scores.keys(), key=lambda k: template_scores[k])
        return best_template
    
    def generate_allocation_reasoning(self, profile: InvestorProfile, analysis: Dict) -> List[str]:
        """Generate reasoning for allocation decisions"""
        
        reasoning = []
        allocation = analysis['recommended_allocation']
        
        # Stock allocation reasoning
        stock_pct = allocation.get('stocks', 0) * 100
        if stock_pct >= 60:
            reasoning.append(f"High stock allocation ({stock_pct:.0f}%) due to young retirement age ({profile.age}) and {profile.risk_tolerance} risk tolerance")
        elif stock_pct <= 30:
            reasoning.append(f"Conservative stock allocation ({stock_pct:.0f}%) appropriate for age {profile.age} and {profile.health_status} health status")
        else:
            reasoning.append(f"Moderate stock allocation ({stock_pct:.0f}%) balances growth needs with age-appropriate risk reduction")
        
        # Bond allocation reasoning
        bond_pct = allocation.get('bonds', 0) * 100
        if bond_pct >= 50:
            reasoning.append(f"High bond allocation ({bond_pct:.0f}%) provides stability and income for {profile.risk_tolerance} investor")
        
        # Gold allocation reasoning
        gold_pct = allocation.get('gold', 0) * 100
        if gold_pct >= 15:
            reasoning.append(f"Meaningful gold allocation ({gold_pct:.0f}%) addresses {profile.inflation_concern} inflation concerns")
        elif gold_pct >= 10:
            reasoning.append(f"Moderate gold allocation ({gold_pct:.0f}%) provides portfolio diversification and crisis protection")
        
        # TIPS allocation reasoning
        tips_pct = allocation.get('tips', 0) * 100
        if tips_pct >= 10:
            reasoning.append(f"TIPS allocation ({tips_pct:.0f}%) provides direct inflation protection given {profile.inflation_concern} inflation concern")
        
        # Portfolio size considerations
        if profile.portfolio_size > 2000000:
            reasoning.append("Large portfolio size allows for more sophisticated diversification strategies")
        elif profile.portfolio_size < 500000:
            reasoning.append("Smaller portfolio size suggests focus on simplicity and low-cost broad diversification")
        
        # Other income impact
        if profile.other_income > profile.portfolio_size * 0.04:
            reasoning.append("Substantial other income allows for more aggressive portfolio allocation")
        
        return reasoning
    
    def assess_allocation_risks(self, allocation: Dict) -> Dict:
        """Assess risks of the recommended allocation"""
        
        risks = {
            'inflation_risk': 'medium',
            'sequence_risk': 'medium', 
            'longevity_risk': 'medium',
            'complexity_risk': 'low'
        }
        
        # Inflation risk assessment
        inflation_protected = allocation.get('gold', 0) + allocation.get('tips', 0)
        if inflation_protected < 0.10:
            risks['inflation_risk'] = 'high'
        elif inflation_protected > 0.25:
            risks['inflation_risk'] = 'low'
        
        # Sequence of returns risk
        stock_allocation = allocation.get('stocks', 0)
        if stock_allocation > 0.70:
            risks['sequence_risk'] = 'high'
        elif stock_allocation < 0.30:
            risks['sequence_risk'] = 'low'
        
        # Longevity risk (running out of money)
        growth_assets = allocation.get('stocks', 0)
        if growth_assets < 0.30:
            risks['longevity_risk'] = 'high'
        elif growth_assets > 0.60:
            risks['longevity_risk'] = 'low'
        
        # Complexity risk
        num_asset_classes = sum(1 for weight in allocation.values() if weight > 0.05)
        if num_asset_classes > 4:
            risks['complexity_risk'] = 'medium'
        elif num_asset_classes > 5:
            risks['complexity_risk'] = 'high'
        
        return risks
    
    def generate_implementation_guidance(self, allocation: Dict, profile: InvestorProfile) -> Dict:
        """Generate practical implementation guidance"""
        
        guidance = {
            'rebalancing_frequency': 'quarterly',
            'fund_suggestions': {},
            'tax_considerations': [],
            'monitoring_metrics': [],
            'adjustment_triggers': []
        }
        
        # Rebalancing frequency based on complexity
        num_assets = len([a for a in allocation.values() if a > 0.05])
        if num_assets <= 3:
            guidance['rebalancing_frequency'] = 'semi-annually'
        elif num_assets >= 5:
            guidance['rebalancing_frequency'] = 'monthly'
        
        # Fund suggestions (simplified)
        if allocation.get('stocks', 0) > 0:
            guidance['fund_suggestions']['stocks'] = 'Low-cost total stock market index fund'
        if allocation.get('bonds', 0) > 0:
            guidance['fund_suggestions']['bonds'] = 'Intermediate-term treasury or aggregate bond fund'
        if allocation.get('gold', 0) > 0:
            guidance['fund_suggestions']['gold'] = 'Gold ETF (GLD) or precious metals fund'
        if allocation.get('tips', 0) > 0:
            guidance['fund_suggestions']['tips'] = 'TIPS fund or I-bonds for smaller allocations'
        
        # Tax considerations
        if profile.portfolio_size > 1000000:
            guidance['tax_considerations'].append('Consider tax-loss harvesting opportunities')
            guidance['tax_considerations'].append('Hold gold in tax-advantaged accounts due to poor tax treatment')
        
        # Monitoring metrics
        guidance['monitoring_metrics'] = [
            'Portfolio value vs. spending needs',
            'Inflation rate vs. TIPS/Gold performance',
            'Stock/bond correlation during stress periods',
            'Withdrawal sustainability ratios'
        ]
        
        # Adjustment triggers
        guidance['adjustment_triggers'] = [
            'Major health status changes',
            'Significant market regime shifts (>20% asset class moves)',
            'Inflation exceeding 5% for 2+ consecutive years',
            'Portfolio value changes >25% from plan assumptions'
        ]
        
        return guidance

def create_example_scenarios():
    """Create example investor scenarios for demonstration"""
    
    scenarios = [
        InvestorProfile(
            age=67,
            risk_tolerance='moderate',
            health_status='good',
            spouse_status='married',
            legacy_importance='medium',
            inflation_concern='high',
            market_experience='experienced',
            portfolio_size=1200000,
            other_income=40000,
            spending_flexibility='medium'
        ),
        InvestorProfile(
            age=72,
            risk_tolerance='conservative',
            health_status='fair',
            spouse_status='widowed',
            legacy_importance='high',
            inflation_concern='medium',
            market_experience='moderate',
            portfolio_size=800000,
            other_income=60000,
            spending_flexibility='low'
        ),
        InvestorProfile(
            age=65,
            risk_tolerance='aggressive',
            health_status='excellent',
            spouse_status='married',
            legacy_importance='low',
            inflation_concern='low',
            market_experience='experienced',
            portfolio_size=2500000,
            other_income=80000,
            spending_flexibility='high'
        )
    ]
    
    return scenarios

def main():
    """Demonstrate the asset allocation decision framework"""
    
    print("🎯 ASSET ALLOCATION DECISION FRAMEWORK")
    print("=" * 70)
    print("A comprehensive approach to portfolio construction for QOL retirement strategies")
    
    # Initialize framework
    framework = AssetAllocationDecisionFramework()
    
    # Show decision tree
    decision_tree = framework.create_decision_tree()
    print(decision_tree)
    
    # Demonstrate with example scenarios
    scenarios = create_example_scenarios()
    
    for i, profile in enumerate(scenarios, 1):
        print(f"\n{'='*70}")
        print(f"EXAMPLE SCENARIO {i}")
        print(f"{'='*70}")
        
        recommendation = framework.generate_allocation_recommendation(profile)
        
        # Display recommendation
        allocation = recommendation['recommended_allocation']
        print(f"\n🎯 RECOMMENDED ALLOCATION:")
        print("-" * 40)
        for asset, weight in allocation.items():
            print(f"{asset.capitalize():10}: {weight*100:5.1f}%")
        
        print(f"\n💡 REASONING:")
        print("-" * 20)
        for reason in recommendation['reasoning']:
            print(f"• {reason}")
        
        print(f"\n⚠️  RISK ASSESSMENT:")
        print("-" * 20)
        risks = recommendation['risk_analysis']
        for risk_type, level in risks.items():
            print(f"• {risk_type.replace('_', ' ').title()}: {level.upper()}")
        
        print(f"\n🔧 IMPLEMENTATION:")
        print("-" * 20)
        impl = recommendation['implementation']
        print(f"• Rebalancing: {impl['rebalancing_frequency'].title()}")
        print(f"• Monitoring: {len(impl['monitoring_metrics'])} key metrics")
        print(f"• Adjustment triggers: {len(impl['adjustment_triggers'])} defined")

if __name__ == "__main__":
    main()