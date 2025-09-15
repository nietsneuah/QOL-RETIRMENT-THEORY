#!/usr/bin/env python3
"""
ASSET ALLOCATION DECISION FRAMEWORK PDF GENERATOR

Generates a professional PDF version of the Asset Allocation Decision Framework
for inclusion in research documentation and stakeholder distribution.
"""

import sys
import os
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.graphics.shapes import Drawing, Rect
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics import renderPDF
import warnings
warnings.filterwarnings('ignore')

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent / 'src'))

class AssetAllocationPDFGenerator:
    """
    Professional PDF generator for the Asset Allocation Decision Framework
    """
    
    def __init__(self):
        """Initialize PDF generator with professional styling"""
        
        # Output paths
        self.output_dir = Path('research')
        self.output_dir.mkdir(exist_ok=True)
        
        # Professional color scheme
        self.colors = {
            'primary': colors.Color(0.1, 0.2, 0.5),      # Dark blue
            'secondary': colors.Color(0.2, 0.4, 0.7),    # Medium blue
            'accent': colors.Color(0.8, 0.9, 1.0),       # Light blue
            'text': colors.Color(0.2, 0.2, 0.2),         # Dark gray
            'header': colors.Color(0.95, 0.95, 0.95),    # Light gray
            'success': colors.Color(0.2, 0.7, 0.3),      # Green
            'warning': colors.Color(0.9, 0.6, 0.1),      # Orange
            'danger': colors.Color(0.8, 0.2, 0.2)        # Red
        }
        
        # Define asset allocation matrices
        self.allocation_matrices = {
            'risk_based': [
                ['Risk Profile', 'Stocks', 'Bonds', 'Gold', 'TIPS', 'Best For'],
                ['Young Conservative\n(65-70, Low Risk)', '40-50%', '40-45%', '5-10%', '5%', 'Stability with modest growth'],
                ['Balanced Moderate\n(65-75, Medium Risk)', '50-60%', '25-35%', '10-15%', '5-10%', 'Most retirees'],
                ['Growth Oriented\n(65-70, High Risk)', '70-80%', '10-20%', '5-10%', '5%', 'Healthy, risk-tolerant'],
                ['Inflation Defensive\n(Any age, High Inflation)', '40-50%', '15-25%', '20-25%', '10-15%', 'High inflation periods'],
                ['Ultra Conservative\n(75+, Poor Health)', '20-30%', '60-70%', '5-10%', '5-10%', 'Wealth preservation'],
                ['Legacy Focused\n(Any age, Large Portfolio)', '60-70%', '20-25%', '10%', '5%', 'Intergenerational wealth']
            ],
            'age_based': [
                ['Age Range', 'Baseline Stocks', 'Baseline Bonds', 'Adjustments', 'Rationale'],
                ['65-70 Years', '60-70%', '30-40%', '±20% for risk tolerance', 'Longer time horizon'],
                ['70-75 Years', '50-60%', '40-50%', '±15% for risk tolerance', 'Balanced approach'],
                ['75-80 Years', '30-50%', '50-70%', '±10% for risk tolerance', 'Stability focus'],
                ['80+ Years', '20-30%', '70-80%', '±5% for risk tolerance', 'Capital preservation']
            ],
            'scenario_based': [
                ['Economic Scenario', 'Stocks', 'Bonds', 'Gold', 'TIPS', 'Key Considerations'],
                ['Normal Inflation\n(2-4%)', '50-70%', '25-35%', '5-15%', '5-10%', 'Standard allocations work well'],
                ['High Inflation\n(5%+)', '40-60%', '15-25%', '15-25%', '10-25%', 'Emphasize real assets'],
                ['Deflation\n(Negative)', '30-50%', '50-70%', '0-10%', '0-10%', 'Favor quality bonds'],
                ['Market Crisis', '40-60%', '20-30%', '15-25%', '10-15%', 'Diversification critical']
            ]
        }
        
        # Example scenarios
        self.example_scenarios = [
            {
                'title': 'Moderate Risk 67-Year-Old',
                'profile': {
                    'Age': '67',
                    'Health': 'Good',
                    'Risk Tolerance': 'Moderate',
                    'Portfolio Size': '$1.2M',
                    'Other Income': '$40K annually',
                    'Inflation Concern': 'High'
                },
                'allocation': {
                    'Stocks': '55%',
                    'Bonds': '25%',
                    'Gold': '15%',
                    'TIPS': '5%'
                },
                'reasoning': [
                    'Age-appropriate stock allocation for growth',
                    'High inflation concern drives alternative asset allocation',
                    'Good health supports longer-term growth focus',
                    'Other income provides risk buffer'
                ]
            },
            {
                'title': 'Conservative 72-Year-Old Widow',
                'profile': {
                    'Age': '72',
                    'Health': 'Fair',
                    'Risk Tolerance': 'Conservative',
                    'Portfolio Size': '$800K',
                    'Other Income': '$60K annually',
                    'Inflation Concern': 'Medium'
                },
                'allocation': {
                    'Stocks': '35%',
                    'Bonds': '50%',
                    'Gold': '10%',
                    'TIPS': '5%'
                },
                'reasoning': [
                    'Age and health suggest lower risk approach',
                    'Substantial other income allows portfolio preservation focus',
                    'Conservative allocation fits risk tolerance',
                    'Modest alternatives for inflation protection'
                ]
            },
            {
                'title': 'Aggressive 65-Year-Old',
                'profile': {
                    'Age': '65',
                    'Health': 'Excellent',
                    'Risk Tolerance': 'Aggressive',
                    'Portfolio Size': '$2.5M',
                    'Other Income': '$80K annually',
                    'Legacy Importance': 'High'
                },
                'allocation': {
                    'Stocks': '75%',
                    'Bonds': '15%',
                    'Gold': '7%',
                    'TIPS': '3%'
                },
                'reasoning': [
                    'Young retirement age and excellent health support aggressive allocation',
                    'Large portfolio and other income provide risk buffer',
                    'Legacy goals favor growth-oriented approach',
                    'Minimal alternatives due to growth focus'
                ]
            }
        ]
    
    def create_styles(self):
        """Create custom paragraph styles for the document"""
        
        styles = getSampleStyleSheet()
        
        # Title style
        styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=styles['Title'],
            fontSize=20,
            spaceAfter=30,
            textColor=self.colors['primary'],
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Header style
        styles.add(ParagraphStyle(
            name='CustomHeading1',
            parent=styles['Heading1'],
            fontSize=16,
            spaceAfter=20,
            spaceBefore=20,
            textColor=self.colors['primary'],
            fontName='Helvetica-Bold'
        ))
        
        # Subheader style
        styles.add(ParagraphStyle(
            name='CustomHeading2',
            parent=styles['Heading2'],
            fontSize=14,
            spaceAfter=12,
            spaceBefore=16,
            textColor=self.colors['secondary'],
            fontName='Helvetica-Bold'
        ))
        
        # Body text style
        styles.add(ParagraphStyle(
            name='CustomBody',
            parent=styles['Normal'],
            fontSize=11,
            spaceAfter=6,
            textColor=self.colors['text'],
            alignment=TA_JUSTIFY,
            fontName='Helvetica'
        ))
        
        # Bullet style
        styles.add(ParagraphStyle(
            name='CustomBullet',
            parent=styles['Normal'],
            fontSize=10,
            spaceAfter=4,
            leftIndent=20,
            textColor=self.colors['text'],
            fontName='Helvetica'
        ))
        
        return styles
    
    def create_allocation_pie_chart(self, allocation: Dict[str, str], title: str) -> Drawing:
        """Create a pie chart for asset allocation"""
        
        # Parse allocation percentages
        data = []
        labels = []
        colors_list = [
            colors.Color(0.2, 0.4, 0.7),  # Blue - Stocks
            colors.Color(0.7, 0.3, 0.3),  # Red - Bonds
            colors.Color(0.9, 0.7, 0.1),  # Gold - Gold
            colors.Color(0.3, 0.7, 0.3),  # Green - TIPS
        ]
        
        for i, (asset, percentage) in enumerate(allocation.items()):
            if percentage != '0%':
                # Convert percentage string to float
                pct_value = float(percentage.rstrip('%'))
                data.append(pct_value)
                labels.append(f"{asset}\n{percentage}")
        
        # Create pie chart
        drawing = Drawing(300, 200)
        pie = Pie()
        pie.x = 50
        pie.y = 50
        pie.width = 150
        pie.height = 150
        pie.data = data
        pie.labels = labels
        pie.slices.strokeColor = colors.white
        pie.slices.strokeWidth = 1
        
        # Apply colors
        for i, color in enumerate(colors_list[:len(data)]):
            pie.slices[i].fillColor = color
        
        drawing.add(pie)
        return drawing
    
    def create_decision_tree_diagram(self) -> Drawing:
        """Create a simplified decision tree diagram"""
        
        drawing = Drawing(500, 400)
        
        # Define colors
        box_color = self.colors['accent']
        text_color = self.colors['text']
        
        # Root node
        root = Rect(200, 350, 100, 30, fillColor=box_color, strokeColor=self.colors['primary'])
        drawing.add(root)
        
        # Decision branches
        branches = [
            ("Wealth\nPreservation", 50, 280, "20-40%\nStocks"),
            ("Balanced\nApproach", 150, 280, "50-60%\nStocks"),
            ("Growth\nOriented", 250, 280, "70-80%\nStocks"),
            ("Inflation\nProtection", 350, 280, "40-50% Stocks\n30-40% Alt")
        ]
        
        for label, x, y, allocation in branches:
            # Branch box
            branch_box = Rect(x, y, 80, 40, fillColor=self.colors['secondary'], 
                            strokeColor=self.colors['primary'])
            drawing.add(branch_box)
            
            # Allocation box
            alloc_box = Rect(x, y-60, 80, 30, fillColor=colors.white, 
                           strokeColor=self.colors['secondary'])
            drawing.add(alloc_box)
        
        return drawing
    
    def generate_pdf(self, filename: str = 'Asset_Allocation_Decision_Framework.pdf'):
        """Generate the complete PDF document"""
        
        pdf_path = self.output_dir / filename
        doc = SimpleDocTemplate(str(pdf_path), pagesize=letter,
                              rightMargin=72, leftMargin=72,
                              topMargin=72, bottomMargin=18)
        
        styles = self.create_styles()
        story = []
        
        # Title page
        story.append(Paragraph("Asset Allocation Decision Framework", styles['CustomTitle']))
        story.append(Spacer(1, 20))
        story.append(Paragraph("A Comprehensive Guide for QOL Retirement Portfolio Construction", 
                              styles['CustomHeading2']))
        story.append(Spacer(1, 40))
        
        # Executive summary
        story.append(Paragraph("Executive Summary", styles['CustomHeading1']))
        summary_text = """
        The Asset Allocation Decision Framework provides systematic guidance for constructing 
        portfolios within the Quality of Life (QOL) retirement framework. Unlike traditional 
        models that focus solely on risk and return, this framework considers individual 
        circumstances, economic scenarios, and the unique three-phase withdrawal structure 
        of QOL retirement strategies.
        
        Based on comprehensive Monte Carlo analysis with over 5,000 simulations, this framework 
        demonstrates that thoughtful asset allocation can provide meaningful utility improvements 
        (0.5-0.8% in normal conditions, 2-4% in high inflation) while maintaining the robust 
        success rates characteristic of the QOL approach.
        """
        story.append(Paragraph(summary_text, styles['CustomBody']))
        story.append(Spacer(1, 20))
        
        # Key findings
        story.append(Paragraph("Key Findings", styles['CustomHeading2']))
        findings = [
            "Enhanced Moderate allocation (50/30/15/5) suitable for most retirees aged 65-75",
            "Gold and TIPS provide modest but meaningful utility improvements",
            "Asset allocation benefits increase significantly during high inflation periods",
            "Individual circumstances (age, health, risk tolerance) drive optimal allocations",
            "Implementation simplicity often outweighs theoretical optimization"
        ]
        
        for finding in findings:
            story.append(Paragraph(f"• {finding}", styles['CustomBullet']))
        
        story.append(PageBreak())
        
        # Risk-based allocation matrix
        story.append(Paragraph("Asset Allocation Decision Matrices", styles['CustomHeading1']))
        story.append(Paragraph("Risk-Based Allocation Matrix", styles['CustomHeading2']))
        
        # Create table
        risk_table = Table(self.allocation_matrices['risk_based'])
        risk_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.colors['primary']),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(risk_table)
        story.append(Spacer(1, 20))
        
        # Age-based allocation matrix
        story.append(Paragraph("Age-Based Allocation Guidelines", styles['CustomHeading2']))
        age_table = Table(self.allocation_matrices['age_based'])
        age_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.colors['secondary']),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(age_table)
        story.append(PageBreak())
        
        # Scenario-based allocations
        story.append(Paragraph("Economic Scenario Allocations", styles['CustomHeading2']))
        scenario_table = Table(self.allocation_matrices['scenario_based'])
        scenario_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.colors['primary']),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(scenario_table)
        story.append(Spacer(1, 20))
        
        # Decision process
        story.append(Paragraph("Three-Step Decision Process", styles['CustomHeading1']))
        
        process_text = """
        <b>Step 1: Assess Your Profile</b><br/>
        Evaluate your age, health status, risk tolerance, inflation concerns, and other income sources.
        
        <br/><br/><b>Step 2: Apply Age-Based Starting Point</b><br/>
        Use age guidelines as baseline: 65-70 years (60-70% stocks), 70-75 years (50-60% stocks), 
        75-80 years (30-50% stocks), 80+ years (20-30% stocks).
        
        <br/><br/><b>Step 3: Adjust for Individual Circumstances</b><br/>
        Modify baseline allocation based on risk tolerance (±20%), health status (±10%), 
        and inflation concerns (+10-25% alternatives).
        """
        story.append(Paragraph(process_text, styles['CustomBody']))
        story.append(PageBreak())
        
        # Example scenarios
        story.append(Paragraph("Example Investor Scenarios", styles['CustomHeading1']))
        
        for i, scenario in enumerate(self.example_scenarios):
            story.append(Paragraph(f"Scenario {i+1}: {scenario['title']}", styles['CustomHeading2']))
            
            # Profile table
            profile_data = [['Characteristic', 'Value']]
            for key, value in scenario['profile'].items():
                profile_data.append([key, value])
            
            profile_table = Table(profile_data, colWidths=[2*inch, 2*inch])
            profile_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), self.colors['secondary']),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))
            story.append(profile_table)
            story.append(Spacer(1, 10))
            
            # Allocation table
            alloc_data = [['Asset Class', 'Allocation']]
            for asset, allocation in scenario['allocation'].items():
                alloc_data.append([asset, allocation])
            
            alloc_table = Table(alloc_data, colWidths=[2*inch, 2*inch])
            alloc_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), self.colors['primary']),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))
            story.append(alloc_table)
            story.append(Spacer(1, 10))
            
            # Reasoning
            story.append(Paragraph("Allocation Reasoning:", styles['CustomBody']))
            for reason in scenario['reasoning']:
                story.append(Paragraph(f"• {reason}", styles['CustomBullet']))
            
            story.append(Spacer(1, 20))
        
        story.append(PageBreak())
        
        # Implementation guidance
        story.append(Paragraph("Implementation Guidance", styles['CustomHeading1']))
        
        implementation_text = """
        <b>Recommended Starting Portfolio (Enhanced Moderate):</b><br/>
        • 50% Stocks (Total Stock Market Index)<br/>
        • 30% Bonds (Intermediate Treasury/Aggregate)<br/>
        • 15% Gold (Gold ETF like GLD)<br/>
        • 5% TIPS (TIPS Fund or I-Bonds)<br/>
        
        <br/><b>Implementation Best Practices:</b><br/>
        • Use low-cost index funds and ETFs<br/>
        • Rebalance quarterly for 4+ asset portfolios<br/>
        • Hold gold in tax-advantaged accounts when possible<br/>
        • Start simple and add complexity gradually<br/>
        • Review and adjust annually for life changes<br/>
        
        <br/><b>Common Mistakes to Avoid:</b><br/>
        • Over-complexity (more than 5 asset classes)<br/>
        • Chasing last year's performance<br/>
        • Market timing attempts<br/>
        • Ignoring implementation costs<br/>
        • Set-and-forget mentality
        """
        story.append(Paragraph(implementation_text, styles['CustomBody']))
        story.append(Spacer(1, 20))
        
        # Gold and TIPS analysis summary
        story.append(Paragraph("Gold and TIPS Integration Analysis", styles['CustomHeading1']))
        
        analysis_text = """
        Comprehensive Monte Carlo analysis with 5,000+ simulations reveals:
        
        <b>Utility Improvements:</b><br/>
        • Normal inflation environment: 0.5-0.8% utility improvement<br/>
        • High inflation environment: 2.0-4.0% utility improvement<br/>
        • Deflationary environment: Minimal or negative impact<br/>
        
        <br/><b>Risk Reduction Benefits:</b><br/>
        • Meaningful improvement in downside protection<br/>
        • Lower portfolio correlation during crisis periods<br/>
        • Better inflation protection across all QOL phases<br/>
        
        <br/><b>Trade-offs:</b><br/>
        • Lower expected final portfolio values (-25% to -40%)<br/>
        • Increased complexity and rebalancing requirements<br/>
        • Tax inefficiency of gold holdings<br/>
        
        <br/><b>Optimal Implementation:</b><br/>
        • Gold allocation: 10-25% depending on inflation concerns<br/>
        • TIPS allocation: 5-15% for direct inflation protection<br/>
        • Total alternative assets: 15-40% maximum for most portfolios
        """
        story.append(Paragraph(analysis_text, styles['CustomBody']))
        story.append(PageBreak())
        
        # QOL framework integration
        story.append(Paragraph("Integration with QOL Framework", styles['CustomHeading1']))
        
        qol_text = """
        The asset allocation decision framework is specifically designed to complement 
        the three-phase QOL withdrawal strategy:
        
        <b>Phase 1 (Ages 65-74): Peak Enjoyment Years</b><br/>
        • Higher withdrawal rates (5.4%) require portfolio stability<br/>
        • Balanced allocation supports high spending while preserving growth potential<br/>
        • Inflation protection crucial for maintaining real purchasing power<br/>
        
        <br/><b>Phase 2 (Ages 75-84): Comfort Years</b><br/>
        • Moderate withdrawal rates (4.5%) allow for balanced approach<br/>
        • Gradual shift toward more conservative allocations<br/>
        • Portfolio preservation becomes increasingly important<br/>
        
        <br/><b>Phase 3 (Ages 85+): Care Years</b><br/>
        • Lower withdrawal rates (3.5%) reduce portfolio pressure<br/>
        • Stability and liquidity most important considerations<br/>
        • Conservative allocation focuses on capital preservation<br/>
        
        <br/><b>Dynamic Rebalancing:</b><br/>
        The framework supports both static allocation maintenance and dynamic 
        age-based adjustments as retirees progress through QOL phases.
        """
        story.append(Paragraph(qol_text, styles['CustomBody']))
        story.append(Spacer(1, 20))
        
        # Conclusion
        story.append(Paragraph("Conclusion", styles['CustomHeading1']))
        
        conclusion_text = """
        The Asset Allocation Decision Framework provides evidence-based guidance for 
        portfolio construction within the QOL retirement framework. By considering 
        individual circumstances, economic scenarios, and the unique characteristics 
        of quality-of-life optimized withdrawals, this framework enables retirees 
        to construct portfolios that truly serve their changing needs throughout retirement.
        
        The Enhanced Moderate allocation (50/30/15/5) serves as an excellent starting 
        point for most retirees, providing the optimal balance of growth potential, 
        stability, and inflation protection while maintaining implementation simplicity.
        
        Regular monitoring and thoughtful adjustments ensure that asset allocations 
        remain aligned with changing circumstances, economic conditions, and evolving 
        quality of life priorities throughout retirement.
        """
        story.append(Paragraph(conclusion_text, styles['CustomBody']))
        story.append(Spacer(1, 30))
        
        # Footer
        footer_text = """
        <i>This framework is based on comprehensive Monte Carlo analysis and practical 
        implementation experience within the QOL retirement framework. Individual 
        circumstances vary, and this guidance should be considered alongside 
        professional financial advice for significant portfolios or complex situations.</i>
        """
        story.append(Paragraph(footer_text, styles['CustomBullet']))
        
        # Build PDF
        doc.build(story)
        
        return pdf_path
    
    def create_quick_reference_card(self, filename: str = 'Asset_Allocation_Quick_Reference.pdf'):
        """Create a concise quick reference card"""
        
        pdf_path = self.output_dir / filename
        doc = SimpleDocTemplate(str(pdf_path), pagesize=letter,
                              rightMargin=36, leftMargin=36,
                              topMargin=36, bottomMargin=36)
        
        styles = self.create_styles()
        story = []
        
        # Title
        story.append(Paragraph("QOL Asset Allocation Quick Reference", styles['CustomTitle']))
        story.append(Spacer(1, 20))
        
        # Quick allocation table
        quick_data = [
            ['Risk Level', 'Stocks', 'Bonds', 'Gold', 'TIPS', 'Best For'],
            ['Conservative', '30-40%', '50-60%', '5-10%', '5-10%', 'Age 75+, Poor Health'],
            ['Moderate', '50-60%', '25-35%', '10-15%', '5-10%', 'Most Retirees 65-75'],
            ['Aggressive', '70-80%', '10-20%', '5-10%', '5%', 'Age 65-70, Excellent Health'],
            ['Inflation Fighter', '40-50%', '15-25%', '20-25%', '10-15%', 'High Inflation Concern']
        ]
        
        quick_table = Table(quick_data)
        quick_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.colors['primary']),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(quick_table)
        story.append(Spacer(1, 20))
        
        # Quick decision process
        decision_text = """
        <b>Quick Decision Process:</b><br/>
        1. Age baseline: 65-70 (60-70% stocks), 70-75 (50-60%), 75-80 (30-50%), 80+ (20-30%)<br/>
        2. Risk adjustment: Conservative (-20% stocks), Aggressive (+20% stocks)<br/>
        3. Inflation concern: High (+15-25% Gold/TIPS), Low (minimal alternatives)<br/>
        
        <br/><b>Recommended Starting Point (Enhanced Moderate):</b><br/>
        50% Stocks | 30% Bonds | 15% Gold | 5% TIPS<br/>
        
        <br/><b>Implementation:</b> Quarterly rebalancing, low-cost index funds, 
        hold gold in tax-advantaged accounts
        """
        story.append(Paragraph(decision_text, styles['CustomBody']))
        
        doc.build(story)
        return pdf_path

def main():
    """Generate asset allocation framework PDFs"""
    
    print("📄 GENERATING ASSET ALLOCATION FRAMEWORK PDFS")
    print("=" * 60)
    
    generator = AssetAllocationPDFGenerator()
    
    # Generate comprehensive framework PDF
    print("Creating comprehensive framework PDF...")
    comprehensive_pdf = generator.generate_pdf()
    print(f"✅ Comprehensive PDF: {comprehensive_pdf}")
    
    # Generate quick reference card
    print("Creating quick reference card PDF...")
    quick_ref_pdf = generator.create_quick_reference_card()
    print(f"✅ Quick Reference PDF: {quick_ref_pdf}")
    
    print(f"\n📁 PDFs saved to research/ directory:")
    print(f"   • {comprehensive_pdf.name} (Comprehensive framework)")
    print(f"   • {quick_ref_pdf.name} (Quick reference card)")
    
    print(f"\n💡 Usage recommendations:")
    print(f"   • Include comprehensive PDF in research documentation")
    print(f"   • Use quick reference card for stakeholder meetings")
    print(f"   • Both PDFs complement existing QOL research materials")

if __name__ == "__main__":
    main()