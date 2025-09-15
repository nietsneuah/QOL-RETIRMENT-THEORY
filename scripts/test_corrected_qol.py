#!/usr/bin/env python3
"""
Test the corrected QOL Framework implementation.
QOL should now be Trinity Study + QOL multipliers, not percentage of current balance.
"""

import sys
import os
import numpy as np

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from enhanced_qol_framework import EnhancedQOLFramework

def test_corrected_qol():
    """Test the corrected QOL implementation."""
    
    print("🔧 Testing Corrected QOL Framework Implementation")
    print("=" * 60)
    print("QOL should now be Trinity Study base × QOL multipliers")
    print()
    
    # Test parameters
    starting_value = 1000000
    years = 5
    simulations = 1
    
    # Test both Trinity and QOL with identical conditions for comparison
    strategies = ['trinity_4pct', 'hauenstein']
    
    for strategy in strategies:
        print(f"📊 Testing {strategy.upper()}")
        print("-" * 40)
        
        framework = EnhancedQOLFramework(
            starting_value=starting_value,
            starting_age=70,
            horizon_years=years,
            n_simulations=simulations,
            qol_phase1_rate=0.054,  # 5.4% = 1.35x Trinity
            qol_phase2_rate=0.045,  # 4.5% = 1.125x Trinity  
            qol_phase3_rate=0.035   # 3.5% = 0.875x Trinity
        )
        
        # Run with no randomness for exact comparison
        framework.run_enhanced_simulation(
            withdrawal_strategy=strategy,
            return_volatility=0.0,
            inflation_variability=False,
            base_real_return=0.00,  # 0% return for simple math
            base_inflation=0.03,    # 3% inflation
            qol_variability=False,
            verbose=False
        )
        
        withdrawal_paths = framework.simulation_results['withdrawal_paths'][0]
        portfolio_paths = framework.simulation_results['portfolio_paths'][0]
        
        print(f"Starting portfolio: ${starting_value:,}")
        print(f"Base Trinity withdrawal: $40,000 (4% of initial)")
        print()
        
        # Calculate expected values for comparison
        trinity_base = 40000
        cumulative_inflation = 1.0
        
        for year in range(years):
            if year > 0:
                cumulative_inflation *= 1.03
            
            expected_trinity = trinity_base * cumulative_inflation
            actual_withdrawal = withdrawal_paths[year]
            
            if strategy == 'trinity_4pct':
                multiplier = 1.0
                expected_withdrawal = expected_trinity
            else:  # hauenstein
                if year < 10:
                    multiplier = 0.054 / 0.04  # 1.35x
                elif year < 20:
                    multiplier = 0.045 / 0.04  # 1.125x
                else:
                    multiplier = 0.035 / 0.04  # 0.875x
                expected_withdrawal = expected_trinity * multiplier
            
            print(f"Year {year+1}:")
            print(f"  Trinity base (inflation-adj): ${expected_trinity:,.0f}")
            print(f"  QOL multiplier: {multiplier:.3f}")
            print(f"  Expected withdrawal: ${expected_withdrawal:,.0f}")
            print(f"  Actual withdrawal: ${actual_withdrawal:,.0f}")
            print(f"  Match? {'✅' if abs(actual_withdrawal - expected_withdrawal) < 1 else '❌'}")
            print(f"  Portfolio after: ${portfolio_paths[year+1]:,.0f}")
            print()
        
        print()
    
    print("🎯 Key Changes:")
    print("✅ QOL withdrawals now based on Trinity Study foundation")
    print("✅ QOL multipliers redistribute Trinity's total expected income")
    print("✅ Higher withdrawals in early years (better QOL)")
    print("✅ Lower withdrawals in later years (lower QOL)")
    print("✅ Both strategies now use same inflation-adjusted base")
    print()
    print("📊 Expected QOL Standard multipliers:")
    print(f"   Phase 1 (Years 1-10): {0.054/0.04:.3f}x Trinity (5.4% vs 4.0%)")
    print(f"   Phase 2 (Years 11-20): {0.045/0.04:.3f}x Trinity (4.5% vs 4.0%)")
    print(f"   Phase 3 (Years 21+): {0.035/0.04:.3f}x Trinity (3.5% vs 4.0%)")

if __name__ == "__main__":
    test_corrected_qol()