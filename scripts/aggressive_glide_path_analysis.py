"""
DETAILED ANALYSIS: AGGRESSIVE GLIDE PATH STRATEGY

This analysis provides a detailed breakdown of the optimal dynamic allocation strategy:
starting aggressive (100% stocks) during high enjoyment years, then gradually 
becoming conservative (40% stocks) as enjoyment value decreases.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from pathlib import Path

# Find project root directory
script_dir = Path(__file__).parent
project_root = script_dir.parent

class AggressiveGlidePathAnalysis:
    """
    Deep dive into the optimal dynamic allocation strategy
    """
    
    def __init__(self):
        # Aggressive Glide Path parameters
        self.strategy = {
            'phase1': {  # Years 0-9 (Ages 65-74)
                'allocation': {'stocks': 1.00, 'bonds': 0.00},
                'expected_return': 0.072,
                'volatility': 0.20,
                'enjoyment_multiplier': 1.35,
                'description': 'High Enjoyment Phase - Maximum Growth'
            },
            'phase2': {  # Years 10-19 (Ages 75-84)
                'allocation': {'stocks': 0.70, 'bonds': 0.30},
                'expected_return': 0.060,
                'volatility': 0.165,
                'enjoyment_multiplier': 1.125,
                'description': 'Moderate Enjoyment Phase - Balanced Growth'
            },
            'phase3': {  # Years 20+ (Ages 85+)
                'allocation': {'stocks': 0.40, 'bonds': 0.60},
                'expected_return': 0.045,
                'volatility': 0.135,
                'enjoyment_multiplier': 0.875,
                'description': 'Low Enjoyment Phase - Capital Preservation'
            }
        }
    
    def analyze_phase_rationale(self):
        """Analyze the rationale behind each phase"""
        
        print("🎯 AGGRESSIVE GLIDE PATH STRATEGY RATIONALE")
        print("=" * 60)
        print()
        
        for phase_name, phase_data in self.strategy.items():
            print(f"📊 {phase_name.upper()}")
            print(f"   {phase_data['description']}")
            print(f"   • Stock allocation: {phase_data['allocation']['stocks']*100:.0f}%")
            print(f"   • Expected return: {phase_data['expected_return']*100:.1f}%")
            print(f"   • Volatility: {phase_data['volatility']*100:.1f}%")
            print(f"   • Enjoyment multiplier: {phase_data['enjoyment_multiplier']:.3f}x")
            print(f"   • Risk-adjusted return: {phase_data['expected_return']/phase_data['volatility']:.2f}")
            print()
        
        # Calculate phase values
        enjoyment_values = [p['enjoyment_multiplier'] for p in self.strategy.values()]
        risk_levels = [p['volatility'] for p in self.strategy.values()]
        returns = [p['expected_return'] for p in self.strategy.values()]
        
        print("💡 KEY INSIGHTS:")
        print(f"   • Enjoyment decreases {(enjoyment_values[0]/enjoyment_values[-1]):.1f}x over time")
        print(f"   • Risk decreases {(risk_levels[0]/risk_levels[-1]):.1f}x over time")
        print(f"   • Expected returns decrease {(returns[0]/returns[-1]):.1f}x over time")
        print(f"   • Strategy matches risk appetite to enjoyment value")
        print()
    
    def simulate_lifecycle_decisions(self, n_simulations=1000):
        """Simulate key decision points throughout retirement"""
        
        print("🔄 LIFECYCLE DECISION SIMULATION")
        print("=" * 50)
        print()
        
        np.random.seed(42)
        starting_portfolio = 1000000
        
        # Track key metrics at transition points
        transition_metrics = {
            'year_10_wealth': [],
            'year_20_wealth': [],
            'final_wealth': [],
            'cumulative_enjoyment': [],
            'phase1_total_income': [],
            'phase2_total_income': [],
            'phase3_total_income': []
        }
        
        for sim in range(n_simulations):
            portfolio_value = starting_portfolio
            cumulative_inflation = 1.0
            total_enjoyment = 0
            phase_incomes = {'phase1': 0, 'phase2': 0, 'phase3': 0}
            
            for year in range(29):
                # Determine phase
                if year < 10:
                    phase = 'phase1'
                elif year < 20:
                    phase = 'phase2'
                else:
                    phase = 'phase3'
                
                phase_data = self.strategy[phase]
                
                # Inflation
                inflation = np.random.normal(0.03, 0.01)
                cumulative_inflation *= (1 + inflation)
                
                # Portfolio return
                annual_return = np.random.normal(
                    phase_data['expected_return'], 
                    phase_data['volatility']
                )
                
                # QOL withdrawal
                base_withdrawal = starting_portfolio * 0.04 * cumulative_inflation
                qol_withdrawal = base_withdrawal * phase_data['enjoyment_multiplier']
                
                # Apply growth and withdrawal
                portfolio_value = portfolio_value * (1 + annual_return) - qol_withdrawal
                portfolio_value = max(0, portfolio_value)
                
                # Track metrics
                enjoyment_value = qol_withdrawal * {
                    'phase1': 1.5, 'phase2': 1.2, 'phase3': 1.0
                }[phase]
                total_enjoyment += enjoyment_value
                phase_incomes[phase] += qol_withdrawal
                
                # Record transition points
                if year == 9:  # End of phase 1
                    transition_metrics['year_10_wealth'].append(portfolio_value)
                elif year == 19:  # End of phase 2
                    transition_metrics['year_20_wealth'].append(portfolio_value)
            
            # Final metrics
            transition_metrics['final_wealth'].append(portfolio_value)
            transition_metrics['cumulative_enjoyment'].append(total_enjoyment)
            transition_metrics['phase1_total_income'].append(phase_incomes['phase1'])
            transition_metrics['phase2_total_income'].append(phase_incomes['phase2'])
            transition_metrics['phase3_total_income'].append(phase_incomes['phase3'])
        
        return transition_metrics
    
    def analyze_transition_points(self, metrics):
        """Analyze key transition points in the strategy"""
        
        print("📈 TRANSITION POINT ANALYSIS")
        print("=" * 40)
        print()
        
        # Calculate statistics
        year_10_median = np.median(metrics['year_10_wealth'])
        year_20_median = np.median(metrics['year_20_wealth'])
        final_median = np.median(metrics['final_wealth'])
        
        success_rate = np.mean(np.array(metrics['final_wealth']) > 0) * 100
        
        print(f"🎂 YEAR 10 TRANSITION (Age 75):")
        print(f"   • Median portfolio value: ${year_10_median:,.0f}")
        print(f"   • Decision: Reduce stocks from 100% to 70%")
        print(f"   • Rationale: Enjoyment value drops from 1.35x to 1.125x")
        print()
        
        print(f"🎂 YEAR 20 TRANSITION (Age 85):")
        print(f"   • Median portfolio value: ${year_20_median:,.0f}")
        print(f"   • Decision: Reduce stocks from 70% to 40%")
        print(f"   • Rationale: Enjoyment value drops from 1.125x to 0.875x")
        print()
        
        print(f"🏁 FINAL OUTCOME (Age 94):")
        print(f"   • Median portfolio value: ${final_median:,.0f}")
        print(f"   • Success rate: {success_rate:.1f}%")
        print()
        
        # Phase income analysis
        phase1_avg = np.mean(metrics['phase1_total_income'])
        phase2_avg = np.mean(metrics['phase2_total_income'])
        phase3_avg = np.mean(metrics['phase3_total_income'])
        
        print(f"💰 INCOME DISTRIBUTION BY PHASE:")
        print(f"   • Phase 1 (High Enjoyment): ${phase1_avg:,.0f} total")
        print(f"   • Phase 2 (Moderate Enjoyment): ${phase2_avg:,.0f} total")
        print(f"   • Phase 3 (Low Enjoyment): ${phase3_avg:,.0f} total")
        print()
        
        # Enjoyment analysis
        avg_enjoyment = np.mean(metrics['cumulative_enjoyment'])
        print(f"🎉 TOTAL ENJOYMENT VALUE: ${avg_enjoyment:,.0f}")
        print()
    
    def create_strategy_roadmap(self):
        """Create a visual roadmap of the strategy"""
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Aggressive Glide Path Strategy Roadmap', fontsize=16, fontweight='bold')
        
        years = list(range(29))
        ages = [65 + year for year in years]
        
        # Plot 1: Stock allocation over time
        stock_allocation = []
        for year in years:
            if year < 10:
                stock_allocation.append(100)
            elif year < 20:
                stock_allocation.append(70)
            else:
                stock_allocation.append(40)
        
        ax1.plot(ages, stock_allocation, 'b-', linewidth=3, marker='o', markersize=4)
        ax1.axvspan(65, 75, alpha=0.2, color='green', label='Phase 1: Max Growth')
        ax1.axvspan(75, 85, alpha=0.15, color='yellow', label='Phase 2: Balanced')
        ax1.axvspan(85, 94, alpha=0.1, color='gray', label='Phase 3: Preservation')
        
        ax1.set_xlabel('Age')
        ax1.set_ylabel('Stock Allocation (%)')
        ax1.set_title('Portfolio Allocation Evolution')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Enjoyment multipliers over time
        enjoyment_mult = []
        for year in years:
            if year < 10:
                enjoyment_mult.append(1.35)
            elif year < 20:
                enjoyment_mult.append(1.125)
            else:
                enjoyment_mult.append(0.875)
        
        ax2.plot(ages, enjoyment_mult, 'r-', linewidth=3, marker='s', markersize=4)
        ax2.axhline(y=1.0, color='gray', linestyle='--', alpha=0.7, label='Trinity baseline')
        ax2.axvspan(65, 75, alpha=0.2, color='green')
        ax2.axvspan(75, 85, alpha=0.15, color='yellow')
        ax2.axvspan(85, 94, alpha=0.1, color='gray')
        
        ax2.set_xlabel('Age')
        ax2.set_ylabel('QOL Multiplier')
        ax2.set_title('Quality of Life Enhancement')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Expected returns and volatility
        expected_returns = []
        volatilities = []
        for year in years:
            if year < 10:
                expected_returns.append(7.2)
                volatilities.append(20.0)
            elif year < 20:
                expected_returns.append(6.0)
                volatilities.append(16.5)
            else:
                expected_returns.append(4.5)
                volatilities.append(13.5)
        
        ax3_twin = ax3.twinx()
        line1 = ax3.plot(ages, expected_returns, 'g-', linewidth=2, label='Expected Return (%)')
        line2 = ax3_twin.plot(ages, volatilities, 'orange', linestyle='--', linewidth=2, label='Volatility (%)')
        
        ax3.axvspan(65, 75, alpha=0.2, color='green')
        ax3.axvspan(75, 85, alpha=0.15, color='yellow')
        ax3.axvspan(85, 94, alpha=0.1, color='gray')
        
        ax3.set_xlabel('Age')
        ax3.set_ylabel('Expected Return (%)', color='g')
        ax3_twin.set_ylabel('Volatility (%)', color='orange')
        ax3.set_title('Risk-Return Profile Evolution')
        
        lines = line1 + line2
        labels = [l.get_label() for l in lines]
        ax3.legend(lines, labels, loc='upper right')
        ax3.grid(True, alpha=0.3)
        
        # Plot 4: Strategy rationale summary
        ax4.axis('off')
        
        rationale_text = """
STRATEGY RATIONALE:

Phase 1 (Ages 65-74): MAXIMUM GROWTH
• 100% stocks for highest returns
• 35% QOL enhancement captures peak enjoyment
• High risk tolerance when time horizon longest

Phase 2 (Ages 75-84): BALANCED APPROACH  
• 70% stocks balances growth and stability
• 12.5% QOL enhancement for moderate enjoyment
• Reduced risk as health becomes concern

Phase 3 (Ages 85+): CAPITAL PRESERVATION
• 40% stocks prioritizes stability
• -12.5% QOL reduction preserves capital
• Low risk when portfolio must last longest

KEY INSIGHT: Match portfolio risk to enjoyment value
"""
        
        ax4.text(0.05, 0.95, rationale_text, transform=ax4.transAxes, fontsize=11,
                verticalalignment='top', fontfamily='monospace',
                bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
        
        plt.tight_layout()
        
        # Save the plot
        output_dir = project_root / 'output' / 'charts'
        os.makedirs(output_dir, exist_ok=True)
        plt.savefig(f'{output_dir}/aggressive_glide_path_roadmap.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return fig
    
    def run_complete_analysis(self):
        """Run the complete analysis"""
        
        print("🚀 AGGRESSIVE GLIDE PATH STRATEGY ANALYSIS")
        print("=" * 60)
        print("Optimal dynamic allocation strategy for QOL retirement")
        print()
        
        # Phase rationale
        self.analyze_phase_rationale()
        
        # Lifecycle simulation
        print("Running lifecycle simulation...")
        metrics = self.simulate_lifecycle_decisions(n_simulations=1000)
        
        # Transition analysis
        self.analyze_transition_points(metrics)
        
        # Create roadmap
        print("📊 Generating strategy roadmap...")
        self.create_strategy_roadmap()
        
        print("✅ Analysis complete!")
        print("📊 Roadmap saved: output/charts/aggressive_glide_path_roadmap.png")


def main():
    """Run the aggressive glide path analysis"""
    analyzer = AggressiveGlidePathAnalysis()
    analyzer.run_complete_analysis()


if __name__ == "__main__":
    main()