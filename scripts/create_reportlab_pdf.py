#!/usr/bin/env python3
"""
Generate professional PDF report using ReportLab for QOL Framework analysis.
This creates a comprehensive, publication-ready PDF report.
"""

import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

# ReportLab imports
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

from enhanced_qol_framework import EnhancedQOLFramework

def create_professional_pdf_report():
    """Create a comprehensive PDF report using ReportLab."""
    
    print("📄 Creating Professional PDF Report with ReportLab")
    print("=" * 55)
    
    # Report filename
    report_filename = "output/reports/QOL_Framework_Analysis_Report.pdf"
    
    # Create the PDF document
    doc = SimpleDocTemplate(
        report_filename,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18
    )
    
    # Container for the 'Flowable' objects
    story = []
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=colors.darkblue
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=20,
        alignment=TA_CENTER,
        textColor=colors.darkred
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=12,
        textColor=colors.darkblue
    )
    
    # Title page
    story.append(Spacer(1, 2*inch))
    story.append(Paragraph("Quality of Life Retirement Framework", title_style))
    story.append(Paragraph("Comprehensive Analysis Report", subtitle_style))
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph("Corrected Implementation with Trinity Study Foundation", styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # Report details
    report_date = datetime.now().strftime("%B %d, %Y")
    story.append(Paragraph(f"<b>Generated:</b> {report_date}", styles['Normal']))
    story.append(Paragraph("<b>Analysis Type:</b> Monte Carlo Simulation (1,000 paths)", styles['Normal']))
    story.append(Paragraph("<b>Time Horizon:</b> 29 years (Ages 70-99)", styles['Normal']))
    story.append(Paragraph("<b>Market Assumptions:</b> 1.5% real returns, 3% inflation, 15% volatility", styles['Normal']))
    
    story.append(PageBreak())
    
    # Run the analysis to get fresh data
    print("🔄 Running analysis for PDF report...")
    results = run_analysis_for_report()
    
    # Executive Summary
    story.append(Paragraph("Executive Summary", heading_style))
    story.append(Paragraph(
        "This analysis compares the corrected Quality of Life (QOL) retirement withdrawal framework "
        "against the traditional Trinity Study 4% rule. Critical methodological corrections have been "
        "applied to ensure meaningful comparison between strategies.",
        styles['Normal']
    ))
    story.append(Spacer(1, 0.2*inch))
    
    # Key corrections
    story.append(Paragraph("Key Corrections Applied:", styles['Heading3']))
    corrections_text = """
    1. <b>Trinity Study Inflation Fix:</b> Corrected inflation timing so Year 1 withdrawal is exactly $40,000 real purchasing power<br/>
    2. <b>QOL Framework Rebase:</b> Changed from percentage-of-current-balance to Trinity-Study-with-multipliers approach<br/>
    3. <b>Consistent Foundation:</b> Both strategies now use identical inflation-adjusted base for meaningful comparison
    """
    story.append(Paragraph(corrections_text, styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # Strategy Performance Table
    story.append(Paragraph("Strategy Performance Summary", heading_style))
    
    # Create performance table data
    table_data = [
        ['Strategy', 'Total Real Income', 'Final Portfolio Value', 'Depletion Rate', 'Success Rate'],
        ['Trinity Study', f"${results['Trinity_4pct']['total_income']:,.0f}", 
         f"${results['Trinity_4pct']['final_value']:,.0f}", 
         f"{results['Trinity_4pct']['depletion_rate']:.1%}",
         f"{results['Trinity_4pct']['success_rate']:.1%}"],
        ['QOL Standard', f"${results['QOL_Standard']['total_income']:,.0f}", 
         f"${results['QOL_Standard']['final_value']:,.0f}", 
         f"{results['QOL_Standard']['depletion_rate']:.1%}",
         f"{results['QOL_Standard']['success_rate']:.1%}"],
        ['QOL Enhanced', f"${results['QOL_Enhanced']['total_income']:,.0f}", 
         f"${results['QOL_Enhanced']['final_value']:,.0f}", 
         f"{results['QOL_Enhanced']['depletion_rate']:.1%}",
         f"{results['QOL_Enhanced']['success_rate']:.1%}"]
    ]
    
    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(table)
    story.append(Spacer(1, 0.3*inch))
    
    # Key Findings
    story.append(Paragraph("Key Findings", heading_style))
    
    trinity_income = results['Trinity_4pct']['total_income']
    qol_std_income = results['QOL_Standard']['total_income']
    qol_enh_income = results['QOL_Enhanced']['total_income']
    
    findings_text = f"""
    <b>1. Income vs Risk Trade-off:</b> QOL Enhanced provides {((qol_enh_income/trinity_income)-1)*100:.1f}% more total income 
    but with {results['QOL_Enhanced']['depletion_rate'] - results['Trinity_4pct']['depletion_rate']:.1%} higher depletion risk.<br/><br/>
    
    <b>2. Trinity Study Conservatism:</b> The traditional 4% rule demonstrates superior portfolio preservation 
    with {results['Trinity_4pct']['depletion_rate']:.1%} depletion rate compared to {results['QOL_Enhanced']['depletion_rate']:.1%} for QOL Enhanced.<br/><br/>
    
    <b>3. Front-Loading Effect:</b> QOL strategies provide 35-75% higher withdrawals in early retirement years 
    (ages 70-79) when quality of life is typically highest.<br/><br/>
    
    <b>4. Strategic Choice:</b> The corrected analysis reveals QOL framework as a risk preference trade-off 
    rather than superior performance.
    """
    
    story.append(Paragraph(findings_text, styles['Normal']))
    story.append(PageBreak())
    
    # Methodology Section
    story.append(Paragraph("Methodology", heading_style))
    
    methodology_text = """
    <b>Corrected QOL Framework Implementation:</b><br/>
    The QOL framework now correctly implements Trinity Study as its foundation with quality-of-life multipliers:<br/><br/>
    
    QOL Withdrawal = Trinity Base × QOL Multiplier<br/>
    Trinity Base = $40,000 × Cumulative Inflation Factor<br/><br/>
    
    <b>QOL Multipliers by Phase:</b><br/>
    • Phase 1 (Ages 70-79): 1.35x Trinity (Peak enjoyment years)<br/>
    • Phase 2 (Ages 80-89): 1.125x Trinity (Comfortable years)<br/>
    • Phase 3 (Ages 90-99): 0.875x Trinity (Care years)<br/><br/>
    
    <b>Investment Assumptions:</b><br/>
    • Starting Portfolio: $1,000,000<br/>
    • Real Returns: 1.5% annually (conservative assumption)<br/>
    • Inflation: 3.0% annually with variability<br/>
    • Return Volatility: 15% (realistic market conditions)<br/>
    • Simulation Count: 1,000 Monte Carlo paths<br/>
    • Time Horizon: 29 years (ages 70-99)
    """
    
    story.append(Paragraph(methodology_text, styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # Risk Analysis Table
    story.append(Paragraph("Risk Analysis Comparison", heading_style))
    
    # Create risk analysis table
    risk_data = [
        ['Strategy', 'Income vs Trinity', 'Income Premium', 'Depletion Premium', 'Risk-Adjusted Return'],
        ['Trinity Study', '1.00x', '$0', '+0.0%', f"{1/(1+results['Trinity_4pct']['depletion_rate']):.2f}"],
        ['QOL Standard', f"{qol_std_income/trinity_income:.2f}x", 
         f"${qol_std_income - trinity_income:,.0f}", 
         f"{results['QOL_Standard']['depletion_rate'] - results['Trinity_4pct']['depletion_rate']:+.1%}",
         f"{(qol_std_income/trinity_income)/(1+results['QOL_Standard']['depletion_rate']):.2f}"],
        ['QOL Enhanced', f"{qol_enh_income/trinity_income:.2f}x", 
         f"${qol_enh_income - trinity_income:,.0f}", 
         f"{results['QOL_Enhanced']['depletion_rate'] - results['Trinity_4pct']['depletion_rate']:+.1%}",
         f"{(qol_enh_income/trinity_income)/(1+results['QOL_Enhanced']['depletion_rate']):.2f}"]
    ]
    
    risk_table = Table(risk_data)
    risk_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkred),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(risk_table)
    story.append(PageBreak())
    
    # Add visualizations
    story.append(Paragraph("Analysis Visualizations", heading_style))
    
    # Create and add charts
    chart_paths = create_report_charts(results)
    
    for chart_path, caption in chart_paths:
        if os.path.exists(chart_path):
            img = Image(chart_path, width=6*inch, height=4*inch)
            story.append(img)
            story.append(Paragraph(caption, styles['Normal']))
            story.append(Spacer(1, 0.2*inch))
    
    # Decision Framework
    story.append(PageBreak())
    story.append(Paragraph("Decision Framework", heading_style))
    
    decision_text = """
    <b>Choose Trinity Study If:</b><br/>
    • Portfolio preservation is the primary concern<br/>
    • Steady, predictable withdrawals are preferred<br/>
    • Lower risk tolerance for portfolio depletion<br/>
    • Legacy/inheritance planning is important<br/><br/>
    
    <b>Choose QOL Framework If:</b><br/>
    • Early retirement enjoyment is prioritized<br/>
    • Comfortable with higher portfolio depletion risk<br/>
    • Prefer front-loaded consumption during healthy years<br/>
    • Less concerned about late-life portfolio preservation<br/><br/>
    
    <b>Conclusion:</b><br/>
    The corrected QOL framework analysis demonstrates that quality of life considerations can be 
    meaningfully incorporated into retirement withdrawal strategies. However, these benefits come 
    with measurable trade-offs in portfolio longevity and depletion risk. The choice between 
    Trinity Study and QOL frameworks ultimately depends on individual risk tolerance, lifestyle 
    preferences, and retirement objectives.
    """
    
    story.append(Paragraph(decision_text, styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # Disclaimers
    story.append(Paragraph("Limitations and Disclaimers", heading_style))
    disclaimer_text = """
    • Analysis uses Monte Carlo simulation with realistic but hypothetical market assumptions<br/>
    • Past performance does not guarantee future results<br/>
    • Individual circumstances may significantly affect optimal strategy choice<br/>
    • Professional financial advice recommended for personalized retirement planning<br/>
    • Healthcare costs and long-term care needs not explicitly modeled
    """
    story.append(Paragraph(disclaimer_text, styles['Normal']))
    
    # Build PDF
    print("📄 Building PDF document...")
    doc.build(story)
    
    print(f"✅ Professional PDF report created: {report_filename}")
    print(f"📊 Report includes comprehensive analysis, tables, and visualizations")
    
    return report_filename

def run_analysis_for_report():
    """Run analysis to get fresh data for the report."""
    
    # Analysis parameters
    starting_value = 1000000
    starting_age = 70
    years = 29
    simulations = 1000
    
    # Market parameters
    base_real_return = 0.015
    base_inflation = 0.03
    return_volatility = 0.15
    
    strategies = {
        'Trinity_4pct': {'strategy': 'trinity_4pct'},
        'QOL_Standard': {
            'strategy': 'hauenstein',
            'phase1_rate': 0.054,
            'phase2_rate': 0.045,
            'phase3_rate': 0.035
        },
        'QOL_Enhanced': {
            'strategy': 'hauenstein',
            'phase1_rate': 0.070,
            'phase2_rate': 0.055,
            'phase3_rate': 0.040
        }
    }
    
    results = {}
    
    for name, config in strategies.items():
        # Create framework
        if 'phase1_rate' in config:
            framework = EnhancedQOLFramework(
                starting_value=starting_value,
                starting_age=starting_age,
                horizon_years=years,
                n_simulations=simulations,
                qol_phase1_rate=config['phase1_rate'],
                qol_phase2_rate=config['phase2_rate'],
                qol_phase3_rate=config['phase3_rate']
            )
        else:
            framework = EnhancedQOLFramework(
                starting_value=starting_value,
                starting_age=starting_age,
                horizon_years=years,
                n_simulations=simulations
            )
        
        # Run simulation
        framework.run_enhanced_simulation(
            withdrawal_strategy=config['strategy'],
            return_volatility=return_volatility,
            inflation_variability=True,
            base_real_return=base_real_return,
            base_inflation=base_inflation,
            qol_variability=False,
            verbose=False
        )
        
        # Calculate real values
        portfolio_paths = np.array(framework.simulation_results['portfolio_paths'])
        withdrawal_paths = np.array(framework.simulation_results['withdrawal_paths'])
        inflation_paths = np.array(framework.simulation_results['inflation_paths'])
        
        # Convert to real dollars
        real_final_values = []
        real_total_withdrawals = []
        
        for sim in range(simulations):
            cumulative_inflation = 1.0
            total_real_withdrawal = 0
            
            for year in range(years):
                if year > 0:
                    cumulative_inflation *= (1 + inflation_paths[sim, year-1])
                
                if year < withdrawal_paths.shape[1]:
                    real_withdrawal = withdrawal_paths[sim, year] / cumulative_inflation
                    total_real_withdrawal += real_withdrawal
            
            # Final portfolio value in real terms
            final_cumulative_inflation = 1.0
            for year in range(years):
                final_cumulative_inflation *= (1 + inflation_paths[sim, year])
            
            real_final_value = portfolio_paths[sim, -1] / final_cumulative_inflation
            
            real_final_values.append(real_final_value)
            real_total_withdrawals.append(total_real_withdrawal)
        
        # Store results
        results[name] = {
            'total_income': np.mean(real_total_withdrawals),
            'final_value': np.mean(real_final_values),
            'depletion_rate': np.mean(np.array(real_final_values) <= 1000),
            'success_rate': np.mean(np.array(real_final_values) > 100000),
            'framework': framework
        }
    
    return results

def create_report_charts(results):
    """Create charts for the PDF report."""
    
    chart_paths = []
    
    # Chart 1: Strategy Performance Comparison
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    strategies = list(results.keys())
    total_incomes = [results[s]['total_income'] for s in strategies]
    depletion_rates = [results[s]['depletion_rate'] for s in strategies]
    
    # Total income chart
    bars1 = ax1.bar(strategies, total_incomes, color=['#2E86AB', '#A23B72', '#F18F01'], alpha=0.8)
    ax1.set_title('Total Real Lifetime Income', fontweight='bold')
    ax1.set_ylabel('Total Income ($)')
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))
    
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'${height/1000:.0f}K', ha='center', va='bottom')
    
    # Depletion rate chart
    bars2 = ax2.bar(strategies, depletion_rates, color=['#2E86AB', '#A23B72', '#F18F01'], alpha=0.8)
    ax2.set_title('Portfolio Depletion Risk', fontweight='bold')
    ax2.set_ylabel('Depletion Rate')
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:.0%}'))
    
    for bar in bars2:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1%}', ha='center', va='bottom')
    
    plt.tight_layout()
    chart1_path = "output/charts/report_strategy_comparison.png"
    plt.savefig(chart1_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    chart_paths.append((chart1_path, "Figure 1: Strategy Performance Comparison - Total income vs depletion risk"))
    
    # Chart 2: Risk-Return Scatter
    fig, ax = plt.subplots(1, 1, figsize=(8, 6))
    
    colors_list = ['#2E86AB', '#A23B72', '#F18F01']
    trinity_income = results['Trinity_4pct']['total_income']
    
    for i, strategy in enumerate(strategies):
        income_ratio = results[strategy]['total_income'] / trinity_income
        depletion_rate = results[strategy]['depletion_rate']
        
        ax.scatter(depletion_rate, income_ratio, s=200, c=colors_list[i], alpha=0.8, label=strategy.replace('_', ' '))
        ax.annotate(strategy.replace('_', ' '), 
                   (depletion_rate, income_ratio),
                   xytext=(10, 10), textcoords='offset points')
    
    ax.set_title('Risk vs Return Trade-off', fontweight='bold')
    ax.set_xlabel('Depletion Rate')
    ax.set_ylabel('Income Ratio vs Trinity Study')
    ax.grid(True, alpha=0.3)
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:.0%}'))
    ax.legend()
    
    chart2_path = "output/charts/report_risk_return.png"
    plt.savefig(chart2_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    chart_paths.append((chart2_path, "Figure 2: Risk vs Return Trade-off - Income benefits vs depletion risk"))
    
    return chart_paths

if __name__ == "__main__":
    # Ensure output directories exist
    os.makedirs("output/reports", exist_ok=True)
    os.makedirs("output/charts", exist_ok=True)
    
    # Create professional PDF report
    report_path = create_professional_pdf_report()
    
    print(f"\n📄 Professional PDF Report Complete!")
    print(f"📁 Location: {report_path}")
    print(f"🎯 This is the definitive QOL Framework analysis report")