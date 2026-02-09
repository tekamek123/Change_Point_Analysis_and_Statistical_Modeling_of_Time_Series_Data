#!/usr/bin/env python3
"""
Generate Task 2 Summary Report for Brent Oil Price Change Point Analysis
"""

import os
import sys
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.platypus.frames import Frame
from reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate

def create_task2_report():
    """Generate comprehensive Task 2 report"""
    
    # Create reports directory if it doesn't exist
    os.makedirs('reports', exist_ok=True)
    
    # Setup document
    doc = SimpleDocTemplate(
        'reports/task2_change_point_report.pdf',
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18
    )
    
    # Get styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=1,  # Center alignment
        textColor=colors.darkblue
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=12,
        textColor=colors.darkblue
    )
    
    # Build content
    content = []
    
    # Title page
    content.append(Paragraph("Task 2: Bayesian Change Point Detection", title_style))
    content.append(Paragraph("Brent Oil Price Analysis", title_style))
    content.append(Spacer(1, 50))
    content.append(Paragraph(f"Generated on: {datetime.now().strftime('%B %d, %Y')}", styles['Normal']))
    content.append(Spacer(1, 30))
    
    # Executive Summary
    content.append(Paragraph("Executive Summary", heading_style))
    summary_text = """
    This report presents the application of Bayesian change point detection to identify structural breaks 
    in Brent oil price returns from 1987-2022. Using PyMC for Bayesian inference, we implemented a 
    discrete change point model that detects significant shifts in the mean of log returns. The analysis 
    reveals one major structural break, which we associate with key geopolitical and economic events. 
    This approach provides a statistically rigorous framework for understanding market regime changes 
    and their relationship to major world events.
    """
    content.append(Paragraph(summary_text, styles['Normal']))
    content.append(Spacer(1, 20))
    
    # Methodology
    content.append(Paragraph("Methodology", heading_style))
    methodology_text = """
    <b>Bayesian Change Point Model:</b><br/>
    • Discrete uniform prior for change point location (τ)<br/>
    • Normal priors for means before and after change point<br/>
    • Half-Cauchy prior for standard deviation<br/>
    • Normal likelihood with switching mean function<br/><br/>
    
    <b>MCMC Sampling:</b><br/>
    • Metropolis sampler for discrete parameters<br/>
    • 10,000 draws with 2,000 tuning steps<br/>
    • 4 parallel chains for convergence assessment<br/>
    • R-hat statistics for convergence diagnostics<br/><br/>
    
    <b>Data Preparation:</b><br/>
    • Daily Brent oil prices (1987-2022)<br/>
    • Log returns for statistical properties<br/>
    • Event dataset for association analysis
    """
    content.append(Paragraph(methodology_text, styles['Normal']))
    content.append(Spacer(1, 20))
    
    # Key Findings
    content.append(Paragraph("Key Findings", heading_style))
    findings_text = """
    <b>Structural Break Detection:</b><br/>
    • Single significant change point detected in the return series<br/>
    • Posterior distribution provides uncertainty quantification<br/>
    • 95% highest density interval for change point location<br/><br/>
    
    <b>Statistical Impact:</b><br/>
    • Quantified difference in mean returns before and after break<br/>
    • Percentage change in return characteristics<br/>
    • Model convergence diagnostics confirm reliable inference<br/><br/>
    
    <b>Event Association:</b><br/>
    • Major geopolitical events correlated with detected change point<br/>
    • Context provided by historical oil market events<br/>
    • Temporal proximity analysis for event attribution
    """
    content.append(Paragraph(findings_text, styles['Normal']))
    content.append(Spacer(1, 20))
    
    # Technical Implementation
    content.append(Paragraph("Technical Implementation", heading_style))
    tech_text = """
    <b>Model Specification:</b><br/>
    τ ~ DiscreteUniform(0, N-1)<br/>
    μ₁ ~ Normal(0, 0.01)  # Mean before change point<br/>
    μ₂ ~ Normal(0, 0.01)  # Mean after change point<br/>
    σ ~ HalfCauchy(0, 0.01)  # Standard deviation<br/>
    yᵢ ~ Normal(μᵢ, σ)  # Likelihood with switching mean<br/><br/>
    
    <b>Computational Details:</b><br/>
    • PyMC 4.x for probabilistic programming<br/>
    • ArviZ for diagnostics and visualization<br/>
    • MCMC sampling with Metropolis algorithm<br/>
    • Convergence assessment via R-hat and ESS
    """
    content.append(Paragraph(tech_text, styles['Normal']))
    content.append(Spacer(1, 20))
    
    # Limitations and Extensions
    content.append(Paragraph("Limitations and Extensions", heading_style))
    limitations_text = """
    <b>Current Limitations:</b><br/>
    • Single change point assumption (real markets have multiple breaks)<br/>
    • Mean-only modeling (ignores volatility changes)<br/>
    • Independence assumption (ignores autocorrelation)<br/>
    • No exogenous variables in current model<br/><br/>
    
    <b>Proposed Extensions:</b><br/>
    • Multiple change point detection<br/>
    • Joint mean-volatility change point models<br/>
    • Regime-switching models with Markov dynamics<br/>
    • Integration of event indicators and economic variables<br/>
    • Real-time change point detection algorithms<br/>
    • Machine learning approaches for pattern recognition
    """
    content.append(Paragraph(limitations_text, styles['Normal']))
    content.append(Spacer(1, 20))
    
    # Practical Applications
    content.append(Paragraph("Practical Applications", heading_style))
    applications_text = """
    <b>Risk Management:</b><br/>
    • Early warning system for market regime changes<br/>
    • Dynamic risk model adjustments<br/>
    • Stress testing scenarios based on historical breaks<br/><br/>
    
    <b>Trading Strategies:</b><br/>
    • Strategy adaptation around detected change points<br/>
    • Portfolio rebalancing triggers<br/>
    • Volatility forecasting improvements<br/><br/>
    
    <b>Policy Analysis:</b><br/>
    • Quantifying market impacts of policy decisions<br/>
    • Event study methodology enhancement<br/>
    • Economic impact assessment framework
    """
    content.append(Paragraph(applications_text, styles['Normal']))
    content.append(Spacer(1, 20))
    
    # Conclusions
    content.append(Paragraph("Conclusions", heading_style))
    conclusions_text = """
    The Bayesian change point analysis successfully identified a significant structural break in Brent 
    oil price returns, demonstrating the power of probabilistic programming for financial time series 
    analysis. The integration of statistical modeling with historical event context provides a comprehensive 
    framework for understanding market dynamics. While the current single change point model has limitations, 
    it establishes a foundation for more sophisticated analyses that could incorporate multiple breaks, 
    volatility changes, and exogenous factors.
    
    This approach bridges the gap between statistical detection and economic interpretation, providing 
    valuable insights for researchers, traders, and policymakers interested in understanding the dynamics 
    of oil price movements and their relationship to global events.
    """
    content.append(Paragraph(conclusions_text, styles['Normal']))
    
    # Build PDF
    doc.build(content)
    print("Task 2 report generated: reports/task2_change_point_report.pdf")

if __name__ == "__main__":
    create_task2_report()
