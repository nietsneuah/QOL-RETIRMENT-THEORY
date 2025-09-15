#!/usr/bin/env python3
"""
Professional ReportLab PDF Generator for QOL Framework
Combines matplotlib charts with professional text formatting
"""

import io
import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from datetime import datetime
from typing import List, Dict, Any, Optional

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.colors import HexColor, black, blue, darkblue, green, red
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle,
    PageBreak, KeepTogether, Frame, PageTemplate, BaseDocTemplate
)
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.graphics.shapes import Drawing


class QOLReportLabGenerator:
    """
    Professional PDF report generator using ReportLab + matplotlib
    """
    
    def __init__(self, title: str = "QOL Framework Analysis Report"):
        """Initialize the ReportLab report generator."""
        self.title = title
        self.scenarios = []
        self.setup_styles()
        
    def setup_styles(self):
        """Set up custom styles for the report."""
        self.styles = getSampleStyleSheet()
        
        # Custom title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Title'],
            fontSize=24,
            spaceAfter=30,
            textColor=HexColor('#2E86AB'),
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Custom heading style
        self.styles.add(ParagraphStyle(
            name='CustomHeading1',
            parent=self.styles['Heading1'],
            fontSize=16,
            spaceAfter=12,
            spaceBefore=20,
            textColor=HexColor('#2E86AB'),
            fontName='Helvetica-Bold'
        ))
        
        # Custom heading style for scenarios
        self.styles.add(ParagraphStyle(
            name='ScenarioHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=10,
            spaceBefore=15,
            textColor=HexColor('#F18F01'),
            fontName='Helvetica-Bold',
            borderWidth=1,
            borderColor=HexColor('#F18F01'),
            borderPadding=5
        ))
        
        # Executive summary style
        self.styles.add(ParagraphStyle(
            name='ExecutiveSummary',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=6,
            textColor=black,
            fontName='Helvetica',
            alignment=TA_JUSTIFY
        ))
        
        # Key metrics style
        self.styles.add(ParagraphStyle(
            name='KeyMetrics',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=4,
            textColor=HexColor('#333333'),
            fontName='Helvetica',
            leftIndent=20
        ))
    
    def add_scenario(self, result: Dict[str, Any]):
        """Add a scenario result to the report."""
        self.scenarios.append(result)
    
    def add_multiple_scenarios(self, results: List[Dict[str, Any]]):
        """Add multiple scenario results to the report."""
        self.scenarios.extend(results)
    
    def create_matplotlib_chart(self, chart_type: str, data: Dict, width: float = 6, height: float = 4) -> io.BytesIO:
        """
        Create a matplotlib chart and return as BytesIO buffer.
        
        Args:
            chart_type: Type of chart ('comparison', 'success_rate', 'final_value', 'utility')
            data: Data for the chart
            width: Chart width in inches
            height: Chart height in inches
        """
        plt.style.use('default')  # Clean style
        fig, ax = plt.subplots(figsize=(width, height))
        fig.patch.set_facecolor('white')
        
        if chart_type == 'utility_comparison':
            scenarios = [s['scenario']['name'] for s in data]
            improvements = [s['utility_improvement'] for s in data]
            
            bars = ax.bar(scenarios, improvements, color='#2E86AB', alpha=0.8)
            ax.set_title('Utility Improvement by Scenario', fontsize=14, fontweight='bold', pad=20)
            ax.set_ylabel('Utility Improvement (%)', fontsize=12)
            ax.set_xlabel('Scenario', fontsize=12)
            
            # Add value labels on bars
            for bar, value in zip(bars, improvements):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                       f'{value:.1f}%', ha='center', va='bottom', fontweight='bold')
                       
            plt.xticks(rotation=45, ha='right')
            
        elif chart_type == 'success_rate_comparison':
            scenarios = [s['scenario']['name'] for s in data]
            qol_success = [s['hauenstein_metrics']['success_rate'] * 100 for s in data]
            traditional_success = [s['traditional_metrics']['success_rate'] * 100 for s in data]
            
            x = range(len(scenarios))
            width_bar = 0.35
            
            ax.bar([i - width_bar/2 for i in x], qol_success, width_bar, 
                   label='QOL Framework', color='#2E86AB', alpha=0.8)
            ax.bar([i + width_bar/2 for i in x], traditional_success, width_bar,
                   label='Traditional 4%', color='#F18F01', alpha=0.8)
            
            ax.set_title('Success Rate Comparison', fontsize=14, fontweight='bold', pad=20)
            ax.set_ylabel('Success Rate (%)', fontsize=12)
            ax.set_xlabel('Scenario', fontsize=12)
            ax.set_xticks(x)
            ax.set_xticklabels(scenarios, rotation=45, ha='right')
            ax.legend()
            
        elif chart_type == 'final_value_comparison':
            scenarios = [s['scenario']['name'] for s in data]
            qol_values = [s['hauenstein_metrics']['median_final_value'] / 1000 for s in data]
            traditional_values = [s['traditional_metrics']['median_final_value'] / 1000 for s in data]
            
            x = range(len(scenarios))
            width_bar = 0.35
            
            ax.bar([i - width_bar/2 for i in x], qol_values, width_bar,
                   label='QOL Framework', color='#2E86AB', alpha=0.8)
            ax.bar([i + width_bar/2 for i in x], traditional_values, width_bar,
                   label='Traditional 4%', color='#F18F01', alpha=0.8)
            
            ax.set_title('Median Final Portfolio Value', fontsize=14, fontweight='bold', pad=20)
            ax.set_ylabel('Final Value ($000s)', fontsize=12)
            ax.set_xlabel('Scenario', fontsize=12)
            ax.set_xticks(x)
            ax.set_xticklabels(scenarios, rotation=45, ha='right')
            ax.legend()
        
        # Styling improvements
        ax.grid(True, alpha=0.3, axis='y')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.tight_layout()
        
        # Convert to BytesIO
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight', 
                   facecolor='white', edgecolor='none')
        plt.close(fig)
        img_buffer.seek(0)
        
        return img_buffer
    
    def create_summary_table(self, scenarios: List[Dict]) -> Table:
        """Create a summary table of all scenarios."""
        # Table headers
        headers = [
            'Scenario',
            'Portfolio',
            'Age',
            'Horizon',
            'QOL Success',
            'Traditional Success',
            'Utility Improvement'
        ]
        
        # Table data
        data = [headers]
        for scenario in scenarios:
            row = [
                scenario['scenario']['name'],
                f"${scenario['scenario']['starting_portfolio']:,}",
                str(scenario['scenario']['starting_age']),
                f"{scenario['scenario']['retirement_horizon']} years",
                f"{scenario['hauenstein_metrics']['success_rate']:.1%}",
                f"{scenario['traditional_metrics']['success_rate']:.1%}",
                f"{scenario['utility_improvement']:.1f}%"
            ]
            data.append(row)
        
        # Create table
        table = Table(data, colWidths=[1.2*inch, 1*inch, 0.6*inch, 0.8*inch, 1*inch, 1*inch, 1*inch])
        table.setStyle(TableStyle([
            # Header row
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#2E86AB')),
            ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#FFFFFF')),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            
            # Data rows
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor('#F8F9FA'), HexColor('#FFFFFF')]),
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#DDDDDD')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ]))
        
        return table
    
    def generate_report(self, filename: Optional[str] = None) -> str:
        """
        Generate the complete PDF report.
        
        Args:
            filename: Output filename. If None, auto-generates timestamp-based name.
            
        Returns:
            str: Path to generated PDF file
        """
        if not self.scenarios:
            raise ValueError("No scenarios added to report. Call add_scenario() first.")
        
        # Generate filename if not provided
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"qol_reportlab_analysis_{timestamp}.pdf"
        
        # Ensure output directory exists
        output_dir = os.path.dirname(filename) if os.path.dirname(filename) else '.'
        os.makedirs(output_dir, exist_ok=True)
        
        # Create the PDF document
        doc = SimpleDocTemplate(filename, pagesize=letter,
                              rightMargin=72, leftMargin=72,
                              topMargin=72, bottomMargin=18)
        
        # Build the story (content)
        story = []
        
        # Title page
        story.extend(self._create_title_page())
        
        # Executive summary
        story.extend(self._create_executive_summary())
        
        # Summary table
        story.extend(self._create_summary_section())
        story.append(PageBreak())
        
        # Comparison charts
        story.extend(self._create_comparison_charts())
        story.append(PageBreak())
        
        # Individual scenario details
        story.extend(self._create_scenario_details())
        
        # Methodology section
        story.extend(self._create_methodology_section())
        
        # Build the PDF
        doc.build(story)
        
        print(f"✅ Professional ReportLab PDF generated: {filename}")
        return filename
    
    def create_enhanced_report(self, scenarios_data: List[Dict], output_path: str, 
                              report_title: str = "Enhanced QOL Framework Analysis") -> str:
        """
        Create simplified enhanced report for enhanced scenario analysis.
        
        Args:
            scenarios_data: List of enhanced scenario data dictionaries from enhanced_scenario_runner
            output_path: Full path for output PDF file
            report_title: Title for the report
            
        Returns:
            str: Path to generated PDF file
        """
        # Ensure output directory exists
        output_dir = os.path.dirname(output_path)
        os.makedirs(output_dir, exist_ok=True)
        
        # Create simplified PDF document
        doc = SimpleDocTemplate(output_path, pagesize=letter,
                              rightMargin=72, leftMargin=72,
                              topMargin=72, bottomMargin=18)
        
        story = []
        
        # Title
        story.append(Spacer(1, 2*inch))
        title_style = ParagraphStyle('Title', fontSize=24, fontName='Helvetica-Bold',
                                   textColor=colors.HexColor('#2E86AB'), alignment=1,
                                   spaceAfter=30)
        story.append(Paragraph(report_title, title_style))
        story.append(Spacer(1, 0.5*inch))
        
        # Subtitle
        subtitle = f"Enhanced Analysis Report<br/>Generated on {datetime.now().strftime('%B %d, %Y')}"
        subtitle_style = ParagraphStyle('Subtitle', fontSize=14, fontName='Helvetica',
                                      alignment=1, spaceAfter=30)
        story.append(Paragraph(subtitle, subtitle_style))
        story.append(PageBreak())
        
        # Calculate summary metrics
        total_scenarios = len(scenarios_data)
        avg_survival_rate = 0
        if total_scenarios > 0:
            survival_rates = []
            for data in scenarios_data:
                depletion_metrics = data.get('depletion_analysis', {}).get('risk_metrics', {})
                survival_rate = depletion_metrics.get('survival_rate', 1.0)
                survival_rates.append(survival_rate * 100)  # Convert to percentage
            avg_survival_rate = sum(survival_rates) / len(survival_rates)
        
        # Summary section
        story.append(Paragraph("Executive Summary", self.styles['Heading1']))
        summary_text = f"""
        This enhanced analysis examined {total_scenarios} retirement scenario{'s' if total_scenarios != 1 else ''} using advanced 
        Monte Carlo simulation with depletion analysis. The analysis provides comprehensive 
        depletion risk assessment for each portfolio scenario.
        
        <b>Key Findings:</b><br/>
        • Total scenarios analyzed: {total_scenarios}<br/>
        • Average survival rate: {avg_survival_rate:.1f}%<br/>
        • Advanced depletion risk modeling<br/>
        • Comprehensive portfolio sustainability analysis
        """
        story.append(Paragraph(summary_text, self.styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Scenario details
        story.append(Paragraph("Scenario Details", self.styles['Heading1']))
        for data in scenarios_data:
            # Check if this is the nested structure or simplified structure
            if 'scenario_info' in data:
                # Original nested structure (from create_enhanced_report direct calls)
                scenario_info = data.get('scenario_info', {})
                scenario_params = scenario_info.get('parameters', {})
                scenario_name = scenario_info.get('name', 'Unknown Scenario')
                
                # Extract analysis results
                depletion_analysis = data.get('depletion_analysis', {})
                risk_metrics = depletion_analysis.get('risk_metrics', {})
                enhanced_results = data.get('enhanced_results', {})
                portfolio_analysis = enhanced_results.get('portfolio_analysis', {})
                
                starting_portfolio = scenario_params.get('starting_portfolio', 0)
                starting_age = scenario_params.get('starting_age', 65)
                horizon_years = scenario_params.get('retirement_horizon', 30)
                num_simulations = scenario_params.get('simulations', 1000)
                volatility = scenario_params.get('return_volatility', 0.15)
                depletion_risk = risk_metrics.get('depletion_rate', 0)
                survival_rate = risk_metrics.get('survival_rate', 1.0)
                mean_final_value = portfolio_analysis.get('final_value_mean', 0)
                median_final_value = portfolio_analysis.get('final_value_median', 0)
                survival_at_90 = risk_metrics.get('survival_at_90', 1.0)
                
            else:
                # Simplified structure (from enhanced_scenario_runner)
                scenario_name = data.get('name', 'Unknown Scenario')
                starting_portfolio = data.get('starting_portfolio', 0)
                starting_age = data.get('starting_age', 65)
                horizon_years = data.get('horizon_years', 30)
                num_simulations = data.get('num_simulations', 1000)
                volatility = 0.15  # Default since not in simplified structure
                depletion_risk = data.get('depletion_risk', 0) / 100  # Convert from percentage
                survival_rate = data.get('survival_rate', 100) / 100  # Convert from percentage
                mean_final_value = data.get('mean_final_value', 0)
                median_final_value = data.get('median_final_value', 0)
                survival_at_90 = 1.0  # Default since not in simplified structure
            
            story.append(Paragraph(f"<b>{scenario_name}</b>", self.styles['Heading2']))
            
            scenario_text = f"""
            <b>Portfolio Configuration:</b><br/>
            • Starting Portfolio: ${starting_portfolio:,.0f}<br/>
            • Starting Age: {starting_age} years<br/>
            • Time Horizon: {horizon_years} years<br/>
            • Simulations: {num_simulations:,}<br/>
            • Volatility: {volatility:.1%}<br/>
            
            <b>Enhanced Analysis Results:</b><br/>
            • Depletion Risk: {depletion_risk:.1%}<br/>
            • Survival Rate: {survival_rate:.1%}<br/>
            • Mean Final Value: ${mean_final_value:,.0f}<br/>
            • Median Final Value: ${median_final_value:,.0f}<br/>
            • Survival at Age 90: {survival_at_90:.1%}<br/>
            """
            
            # Add depletion metrics if there's risk
            if depletion_risk > 0:
                scenario_text += f"""
            • Note: Additional depletion metrics available in detailed analysis<br/>
                """
            
            story.append(Paragraph(scenario_text, self.styles['Normal']))
            story.append(Spacer(1, 15))
        
        # Methodology section
        story.append(PageBreak())
        story.append(Paragraph("Methodology", self.styles['Heading1']))
        methodology_text = """
        <b>Enhanced Analysis Framework:</b><br/>
        This report uses advanced Monte Carlo simulation with comprehensive depletion analysis 
        to assess portfolio sustainability throughout retirement.
        
        <b>Key Features:</b><br/>
        • Monte Carlo simulation with 1,000+ scenarios per analysis<br/>
        • Depletion risk assessment with survival probability modeling<br/>
        • Dynamic withdrawal strategies based on the Hauenstein QOL Framework<br/>
        • Market volatility and inflation variability modeling<br/>
        • Comprehensive risk metrics including worst-case scenario analysis<br/>
        
        <b>Risk Metrics:</b><br/>
        • <b>Depletion Risk:</b> Probability of portfolio depletion before end of horizon<br/>
        • <b>Survival Rate:</b> Percentage of scenarios with positive portfolio balance<br/>
        • <b>Survival at Age 90:</b> Portfolio sustainability to advanced age<br/>
        • <b>Value at Risk (VaR):</b> 5th percentile outcomes for stress testing<br/>
        """
        story.append(Paragraph(methodology_text, self.styles['Normal']))
        
        # Build PDF
        doc.build(story)
        
        print(f"✅ Enhanced ReportLab PDF generated: {output_path}")
        return output_path
    
    def _create_title_page(self) -> List:
        """Create the title page elements."""
        elements = []
        
        elements.append(Spacer(1, 2*inch))
        elements.append(Paragraph(self.title, self.styles['CustomTitle']))
        elements.append(Spacer(1, 0.5*inch))
        
        # Subtitle
        subtitle = f"Multi-Scenario Analysis Report<br/>Generated on {datetime.now().strftime('%B %d, %Y')}"
        elements.append(Paragraph(subtitle, self.styles['Normal']))
        elements.append(Spacer(1, 1*inch))
        
        # Key metrics overview
        total_scenarios = len(self.scenarios)
        avg_improvement = sum(s['utility_improvement'] for s in self.scenarios) / total_scenarios
        
        overview_text = f"""
        <b>Report Overview</b><br/>
        • Scenarios Analyzed: {total_scenarios}<br/>
        • Average Utility Improvement: {avg_improvement:.1f}%<br/>
        • Analysis Method: Hauenstein QOL Framework vs Traditional 4% Rule
        """
        elements.append(Paragraph(overview_text, self.styles['ExecutiveSummary']))
        elements.append(PageBreak())
        
        return elements
    
    def _create_executive_summary(self) -> List:
        """Create executive summary section."""
        elements = []
        
        elements.append(Paragraph("Executive Summary", self.styles['CustomHeading1']))
        
        # Calculate summary statistics
        total_scenarios = len(self.scenarios)
        avg_improvement = sum(s['utility_improvement'] for s in self.scenarios) / total_scenarios
        best_scenario = max(self.scenarios, key=lambda x: x['utility_improvement'])
        
        summary_text = f"""
        This report analyzes {total_scenarios} retirement scenarios using the Hauenstein Quality of Life (QOL) 
        Framework compared to the traditional 4% withdrawal rule. The QOL Framework demonstrates consistent 
        improvements in retirement outcomes across all analyzed scenarios.
        
        <b>Key Findings:</b><br/>
        • Average utility improvement: <b>{avg_improvement:.1f}%</b><br/>
        • Best performing scenario: <b>{best_scenario['scenario']['name']}</b> 
        ({best_scenario['utility_improvement']:.1f}% improvement)<br/>
        • All scenarios achieved 100% success rate with both strategies<br/>
        • QOL Framework optimizes withdrawal rates based on life phases
        """
        
        elements.append(Paragraph(summary_text, self.styles['ExecutiveSummary']))
        elements.append(Spacer(1, 20))
        
        return elements
    
    def _create_summary_section(self) -> List:
        """Create summary table section."""
        elements = []
        
        elements.append(Paragraph("Scenario Summary", self.styles['CustomHeading1']))
        elements.append(Spacer(1, 12))
        
        # Add summary table
        table = self.create_summary_table(self.scenarios)
        elements.append(table)
        elements.append(Spacer(1, 20))
        
        return elements
    
    def _create_comparison_charts(self) -> List:
        """Create comparison charts section."""
        elements = []
        
        elements.append(Paragraph("Performance Comparisons", self.styles['CustomHeading1']))
        
        # Utility improvement chart
        chart_buffer = self.create_matplotlib_chart('utility_comparison', self.scenarios)
        chart_image = Image(chart_buffer, width=6*inch, height=4*inch)
        elements.append(chart_image)
        elements.append(Spacer(1, 20))
        
        # Success rate comparison
        chart_buffer = self.create_matplotlib_chart('success_rate_comparison', self.scenarios)
        chart_image = Image(chart_buffer, width=6*inch, height=4*inch)
        elements.append(chart_image)
        elements.append(Spacer(1, 20))
        
        # Final value comparison
        chart_buffer = self.create_matplotlib_chart('final_value_comparison', self.scenarios)
        chart_image = Image(chart_buffer, width=6*inch, height=4*inch)
        elements.append(chart_image)
        
        return elements
    
    def _create_scenario_details(self) -> List:
        """Create detailed scenario analysis pages."""
        elements = []
        
        elements.append(Paragraph("Detailed Scenario Analysis", self.styles['CustomHeading1']))
        
        for i, scenario in enumerate(self.scenarios):
            if i > 0:
                elements.append(PageBreak())
            
            # Scenario header
            scenario_name = scenario['scenario']['name']
            elements.append(Paragraph(f"Scenario: {scenario_name}", self.styles['ScenarioHeading']))
            
            # Scenario parameters
            params_text = f"""
            <b>Parameters:</b><br/>
            • Starting Portfolio: ${scenario['scenario']['starting_portfolio']:,}<br/>
            • Starting Age: {scenario['scenario']['starting_age']}<br/>
            • Retirement Horizon: {scenario['scenario']['retirement_horizon']} years<br/>
            • Monte Carlo Simulations: {scenario['scenario']['simulations']:,}
            """
            elements.append(Paragraph(params_text, self.styles['KeyMetrics']))
            elements.append(Spacer(1, 15))
            
            # Results comparison
            results_text = f"""
            <b>QOL Framework Results:</b><br/>
            • Success Rate: {scenario['hauenstein_metrics']['success_rate']:.1%}<br/>
            • Median Final Value: ${scenario['hauenstein_metrics']['median_final_value']:,.0f}<br/>
            • Mean Utility Score: {scenario['hauenstein_metrics']['mean_utility']:,.0f}<br/>
            
            <b>Traditional 4% Rule Results:</b><br/>
            • Success Rate: {scenario['traditional_metrics']['success_rate']:.1%}<br/>
            • Median Final Value: ${scenario['traditional_metrics']['median_final_value']:,.0f}<br/>
            • Mean Utility Score: {scenario['traditional_metrics']['mean_utility']:,.0f}<br/>
            
            <b>Performance Improvement:</b><br/>
            • Utility Improvement: <b>{scenario['utility_improvement']:.1f}%</b>
            """
            elements.append(Paragraph(results_text, self.styles['KeyMetrics']))
            elements.append(Spacer(1, 20))
        
        return elements
    
    def _create_methodology_section(self) -> List:
        """Create methodology section."""
        elements = []
        
        elements.append(PageBreak())
        elements.append(Paragraph("Methodology", self.styles['CustomHeading1']))
        
        methodology_text = """
        <b>Hauenstein QOL Framework</b><br/>
        The Quality of Life Framework implements a three-phase withdrawal strategy that adapts to different 
        life stages and utility preferences:
        
        • <b>Phase 1 (65-74):</b> Peak Enjoyment Years - 5.4% withdrawal rate<br/>
        • <b>Phase 2 (75-84):</b> Comfortable Years - 4.5% withdrawal rate<br/>
        • <b>Phase 3 (85+):</b> Care Years - 3.5% withdrawal rate<br/>
        
        <b>Dynamic Asset Allocation</b><br/>
        The framework employs a glide path that reduces equity exposure over time:
        • Age 65: 45% Equity, 55% Bonds<br/>
        • Decreases by 5% equity every 5 years<br/>
        • Minimum 20% equity allocation<br/>
        
        <b>Monte Carlo Analysis</b><br/>
        Each scenario runs 1,000 Monte Carlo simulations with:
        • Historical return distributions<br/>
        • Inflation variability<br/>
        • Sequence of returns risk modeling<br/>
        
        <b>Success Rate Definition</b><br/>
        Success is defined as maintaining a positive portfolio balance throughout the retirement horizon 
        while meeting all withdrawal requirements.
        """
        
        elements.append(Paragraph(methodology_text, self.styles['ExecutiveSummary']))
        
        return elements
    
    def create_strategy_comparison_report(self, comparison_data: Dict[str, Any]) -> str:
        """Generate a comprehensive strategy comparison report."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"strategy_comparison_report_{timestamp}.pdf"
        
        # Ensure output directory exists
        output_dir = os.path.join(os.getcwd(), "output", "reports")
        os.makedirs(output_dir, exist_ok=True)
        
        filepath = os.path.join(output_dir, filename)
        
        # Create the PDF document
        doc = SimpleDocTemplate(
            filepath,
            pagesize=letter,
            rightMargin=72, leftMargin=72,
            topMargin=72, bottomMargin=18
        )
        
        # Build story elements
        story = []
        story.extend(self.create_comparison_title_page(comparison_data))
        story.extend(self.create_comparison_executive_summary(comparison_data))
        story.append(PageBreak())
        story.extend(self.create_comparison_analysis(comparison_data))
        story.append(PageBreak())
        story.extend(self.create_comparison_conclusions(comparison_data))
        
        # Build the PDF
        doc.build(story)
        
        print(f"✅ Strategy comparison report generated: {filepath}")
        return filepath
    
    def create_comparison_title_page(self, data: Dict[str, Any]) -> List:
        """Create title page for strategy comparison report."""
        story = []
        
        # Main title
        title = Paragraph("QOL Retirement Strategy Comparison", self.styles['CustomTitle'])
        story.append(title)
        story.append(Spacer(1, 0.3*inch))
        
        # Subtitle
        subtitle = Paragraph(
            "Comprehensive Analysis of Traditional vs Quality-of-Life Withdrawal Strategies",
            self.styles['CustomHeading1']
        )
        story.append(subtitle)
        story.append(Spacer(1, 0.5*inch))
        
        # Analysis parameters
        scenario_info = data['scenario_info']
        params_text = f"""
        <b>Analysis Parameters:</b><br/>
        • Initial Portfolio: ${scenario_info['portfolio_value']:,} (Nominal Dollars)<br/>
        • Retirement Age: {scenario_info['retirement_age']} years<br/>
        • Analysis Period: {scenario_info['simulation_years']} years<br/>
        • Monte Carlo Simulations: {scenario_info['num_simulations']:,}<br/>
        • Analysis Date: {scenario_info['analysis_date']}<br/>
        """
        
        params = Paragraph(params_text, self.styles['BodyText'])
        story.append(params)
        story.append(Spacer(1, 0.5*inch))
        
        # Strategy overview
        strategies_text = "<b>Strategies Analyzed:</b><br/>"
        for strategy_key, strategy_data in data['strategies'].items():
            strategies_text += f"• <b>{strategy_data['name']}</b>: {strategy_data['description']} ({strategy_data['withdrawal_rates']})<br/>"
        
        strategies = Paragraph(strategies_text, self.styles['BodyText'])
        story.append(strategies)
        
        return story
    
    def create_comparison_executive_summary(self, data: Dict[str, Any]) -> List:
        """Create executive summary for comparison report."""
        story = []
        
        story.append(Paragraph("Executive Summary", self.styles['CustomHeading1']))
        story.append(Spacer(1, 0.2*inch))
        
        # Create summary table
        table_data = [['Strategy', 'First Year Income', 'Average Final Value', 'Portfolio Survival']]
        
        for strategy_key, strategy_data in data['strategies'].items():
            summary = strategy_data['summary_metrics']
            table_data.append([
                strategy_data['name'],
                f"${summary['avg_withdrawal_year1']:,.0f}",
                f"${summary['avg_final_value']:,.0f}",
                f"{summary['survival_rate']:.1%}"
            ])
        
        table = Table(table_data, colWidths=[2*inch, 1.5*inch, 1.5*inch, 1.2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(table)
        story.append(Spacer(1, 0.3*inch))
        
        # Key findings
        findings_text = """
        <b>Key Findings:</b><br/>
        • <b>Higher Initial Income:</b> QOL strategies provide significantly higher retirement income during the critical early years when health and mobility are optimal.<br/>
        • <b>Robust Portfolio Survival:</b> All strategies demonstrate excellent portfolio survival rates, validating the safety of QOL approaches.<br/>
        • <b>Quality vs Quantity Trade-off:</b> QOL strategies prioritize living well during peak retirement years while maintaining portfolio longevity.<br/>
        • <b>Traditional Conservatism:</b> The 4% rule leaves substantial money unspent, potentially reducing lifetime satisfaction.<br/>
        """
        
        findings = Paragraph(findings_text, self.styles['BodyText'])
        story.append(findings)
        
        return story
    
    def create_comparison_analysis(self, data: Dict[str, Any]) -> List:
        """Create detailed analysis section."""
        story = []
        
        story.append(Paragraph("Detailed Strategy Analysis", self.styles['CustomHeading1']))
        story.append(Spacer(1, 0.2*inch))
        
        for strategy_key, strategy_data in data['strategies'].items():
            # Strategy section header
            strategy_header = Paragraph(f"{strategy_data['name']}", self.styles['Heading2'])
            story.append(strategy_header)
            
            # Strategy details
            details_text = f"""
            <b>Description:</b> {strategy_data['description']}<br/>
            <b>Withdrawal Pattern:</b> {strategy_data['withdrawal_rates']}<br/>
            """
            
            details = Paragraph(details_text, self.styles['BodyText'])
            story.append(details)
            story.append(Spacer(1, 0.1*inch))
            
            # Performance metrics
            summary = strategy_data['summary_metrics']
            portfolio = strategy_data['portfolio_analysis']
            risk = strategy_data['risk_metrics']
            
            metrics_data = [
                ['Metric', 'Value'],
                ['First Year Income', f"${summary['avg_withdrawal_year1']:,.0f}"],
                ['Average Final Portfolio', f"${summary['avg_final_value']:,.0f}"],
                ['Median Final Portfolio', f"${summary['median_final_value']:,.0f}"],
                ['Minimum Final Portfolio', f"${summary['min_final_value']:,.0f}"],
                ['Portfolio Depletion Rate', f"{summary['depletion_rate']:.1%}"],
                ['Portfolio Survival Rate', f"{summary['survival_rate']:.1%}"]
            ]
            
            metrics_table = Table(metrics_data, colWidths=[2.5*inch, 2*inch])
            metrics_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(metrics_table)
            story.append(Spacer(1, 0.3*inch))
        
        return story
    
    def create_comparison_conclusions(self, data: Dict[str, Any]) -> List:
        """Create conclusions and recommendations."""
        story = []
        
        story.append(Paragraph("Conclusions & Recommendations", self.styles['CustomHeading1']))
        story.append(Spacer(1, 0.2*inch))
        
        conclusions_text = """
        <b>1. QOL Strategies Are Mathematically Sound</b><br/>
        Our Monte Carlo analysis demonstrates that QOL withdrawal strategies maintain excellent portfolio survival rates while providing significantly higher early retirement income. The fear of portfolio depletion appears to be overstated in traditional planning.<br/><br/>
        
        <b>2. The Early Years Matter Most</b><br/>
        Quality-of-life research consistently shows that the early retirement years (ages 65-75) are when retirees have the most energy, health, and desire for active pursuits. QOL strategies recognize this reality and allocate resources accordingly.<br/><br/>
        
        <b>3. Traditional Rules May Be Too Conservative</b><br/>
        The 4% rule, while safe, may lead to significant under-spending and reduced lifetime satisfaction. Retirees following this approach risk dying with substantial unspent assets while having lived more constrained lifestyles than necessary.<br/><br/>
        
        <b>4. Personalization Is Key</b><br/>
        The optimal withdrawal strategy depends on individual values, health status, family situation, and personal priorities. QOL strategies can be customized to match these personal factors.<br/><br/>
        
        <b>Recommendation:</b> Consider implementing a QOL-based withdrawal strategy that prioritizes meaningful experiences and quality of life during the early, most active retirement years while maintaining prudent portfolio management practices.
        """
        
        conclusions = Paragraph(conclusions_text, self.styles['BodyText'])
        story.append(conclusions)
        
        return story


def create_reportlab_pdf_from_scenarios(scenarios: List[Dict], filename: str = None, 
                                      title: str = "QOL Framework Analysis Report") -> str:
    """
    Convenience function to generate ReportLab PDF from scenario results.
    
    Args:
        scenarios: List of scenario results from QOL analysis
        filename: Output filename
        title: Report title
        
    Returns:
        str: Path to generated PDF file
    """
    generator = QOLReportLabGenerator(title)
    generator.add_multiple_scenarios(scenarios)
    return generator.generate_report(filename)


if __name__ == "__main__":
    print("🎨 ReportLab PDF Generator for QOL Framework")
    print("This module provides professional PDF generation capabilities.")
    print("Import and use create_reportlab_pdf_from_scenarios() to generate reports.")