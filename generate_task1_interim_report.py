"""
Generate Task 1 Interim Report PDF - Focused 1-2 page document
Covers: 1) Planned analysis steps, 2) Structured event dataset, 3) Initial EDA findings
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from pathlib import Path
from datetime import datetime
import pandas as pd

# Define paths
BASE_DIR = Path(__file__).parent
DATA_PROCESSED = BASE_DIR / "Data" / "processed"
DATA_EVENTS = BASE_DIR / "Data" / "events"
OUTPUT_DIR = BASE_DIR / "reports"
OUTPUT_DIR.mkdir(exist_ok=True)

# Output file
OUTPUT_FILE = OUTPUT_DIR / "task1_interim_report.pdf"


def create_task1_report():
    """Create focused Task 1 interim report (1-2 pages)."""
    doc = SimpleDocTemplate(
        str(OUTPUT_FILE),
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )
    
    # Container for the 'Flowable' objects
    story = []
    
    # Define styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#1a237e'),
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading1_style = ParagraphStyle(
        'CustomHeading1',
        parent=styles['Heading1'],
        fontSize=14,
        textColor=colors.HexColor('#283593'),
        spaceAfter=6,
        spaceBefore=6,
        fontName='Helvetica-Bold'
    )
    
    heading2_style = ParagraphStyle(
        'CustomHeading2',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=colors.HexColor('#3949ab'),
        spaceAfter=4,
        spaceBefore=4,
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=10,
        leading=12,
        alignment=TA_JUSTIFY,
        spaceAfter=3
    )
    
    # Load data
    events_df = pd.read_csv(DATA_EVENTS / "oil_market_events_fixed.csv")
    
    # ===== TITLE =====
    story.append(Paragraph("Task 1 Interim Report", title_style))
    story.append(Paragraph("Brent Oil Price Analysis: Change Point Detection Foundation", 
                          ParagraphStyle('Subtitle', parent=styles['Normal'], 
                                       fontSize=12, alignment=TA_CENTER, 
                                       textColor=colors.HexColor('#5c6bc0'))))
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y')}", 
                          ParagraphStyle('Date', parent=styles['Normal'], 
                                       fontSize=10, alignment=TA_CENTER)))
    story.append(Spacer(1, 0.3*inch))
    
    # ===== SECTION 1: PLANNED ANALYSIS STEPS =====
    story.append(Paragraph("1. Planned Analysis Steps", heading1_style))
    
    analysis_steps = """
    <b>Phase 1: Data Preparation and Exploration</b>
    <br/>• Load Brent oil price data (1987-2022) and perform quality checks
    <br/>• Conduct time series analysis: trend, stationarity, volatility patterns
    <br/>• Generate initial visualizations and statistical summaries
    
    <b>Phase 2: Event Data Integration</b>
    <br/>• Compile major geopolitical events, OPEC decisions, and economic shocks
    <br/>• Create structured dataset with dates, descriptions, and categorization
    <br/>• Align event data with price timeline for correlation analysis
    
    <b>Phase 3: Bayesian Change Point Modeling</b>
    <br/>• Design Bayesian change point model using PyMC framework
    <br/>• Define prior distributions and likelihood functions
    <br/>• Implement MCMC sampling with convergence diagnostics
    
    <b>Phase 4: Analysis and Interpretation</b>
    <br/>• Detect structural breaks and map to historical events
    <br/>• Quantify impact magnitude and duration of price changes
    <br/>• Conduct validation and sensitivity analysis
    
    <b>Phase 5: Communication and Visualization</b>
    <br/>• Create interactive dashboard for stakeholder insights
    <br/>• Generate comprehensive reports with actionable recommendations
    """
    story.append(Paragraph(analysis_steps, body_style))
    story.append(Spacer(1, 0.15*inch))
    
    # ===== SECTION 2: STRUCTURED EVENT DATASET =====
    story.append(Paragraph("2. Structured Event Dataset", heading1_style))
    
    dataset_info = f"""
    <b>Dataset Overview:</b>
    <br/>• Total Events: {len(events_df)} major oil market events (1990-2022)
    <br/>• Data Fields: Date, Event, Event_Type, Severity, Description, Duration
    <br/>• Event Categories: Geopolitical Conflict, OPEC Decision, Economic Shock, Natural Disaster, etc.
    <br/>• Severity Levels: High (19), Medium (10), Low (2)
    """
    story.append(Paragraph(dataset_info, body_style))
    story.append(Spacer(1, 0.1*inch))
    
    # Create event table (showing first 15 events)
    story.append(Paragraph("<b>Sample Events Dataset:</b>", heading2_style))
    
    event_table_data = [['Date', 'Event', 'Type', 'Severity']]
    for i, (_, event) in enumerate(events_df.head(15).iterrows()):
        event_table_data.append([
            event['Date'],
            event['Event'][:30] + '...' if len(event['Event']) > 30 else event['Event'],
            event['Event_Type'][:15] + '...' if len(event['Event_Type']) > 15 else event['Event_Type'],
            event['Severity']
        ])
    
    event_table = Table(event_table_data, colWidths=[1.2*inch, 2*inch, 1.5*inch, 0.8*inch])
    event_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3949ab')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f5f5f5')),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    
    story.append(event_table)
    story.append(Spacer(1, 0.1*inch))
    
    # Event type distribution
    event_counts = events_df['Event_Type'].value_counts()
    distribution_data = [['Event Type', 'Count']]
    for event_type, count in event_counts.head(5).items():
        distribution_data.append([event_type, str(count)])
    
    story.append(Paragraph("<b>Event Type Distribution:</b>", heading2_style))
    dist_table = Table(distribution_data, colWidths=[2*inch, 1*inch])
    dist_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3949ab')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f5f5f5')),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    story.append(dist_table)
    story.append(Spacer(1, 0.15*inch))
    
    # ===== SECTION 3: INITIAL EDA FINDINGS =====
    story.append(Paragraph("3. Initial EDA Findings", heading1_style))
    
    eda_findings = """
    <b>Dataset Overview:</b>
    <br/>• Total Records: 9,011 daily price observations
    <br/>• Time Period: May 20, 1987 to November 14, 2022 (35+ years)
    <br/>• Price Range: $9.10 to $143.95 per barrel
    <br/>• Mean Price: $48.42 (Median: $38.57, Std Dev: $32.86)
    
    <b>Key Statistical Insights:</b>
    <br/>• Right-skewed distribution (mean > median)
    <br/>• High volatility with average daily volatility of 2.1%
    <br/>• Multiple extreme price events identified
    <br/>• Clear non-stationarity requiring specialized modeling
    
    <b>Temporal Patterns:</b>
    <br/>• 1990: $14.68-$41.45 (Gulf War impact)
    <br/>• 2008: $33.73-$143.95 (Financial crisis peak)
    <br/>• 2020: $9.12-$70.25 (COVID-19 pandemic)
    <br/>• 2022: $78.25-$133.18 (Russia-Ukraine conflict)
    
    <b>Event Impact Analysis:</b>
    <br/>• High-severity events: 19 total
    <br/>• Average price change: -5.73% around events
    <br/>• Largest positive: +35.36% (Iraq Invasion 1990)
    <br/>• Largest negative: -34.23% (OPEC+ Price War 2020)
    <br/>• Highest volatility: May 6, 2020 (COVID period)
    
    <b>Volatility Clustering:</b>
    <br/>• Clear patterns of high volatility during crisis periods
    <br/>• Sustained volatility during geopolitical conflicts
    <br/>• Spillover effects across related market events
    """
    story.append(Paragraph(eda_findings, body_style))
    story.append(Spacer(1, 0.1*inch))
    
    # Add key visualization if available
    viz_path = DATA_PROCESSED / "price_analysis_visualizations.png"
    if viz_path.exists():
        try:
            story.append(Paragraph("<b>Key Visualization: Price Analysis Overview</b>", heading2_style))
            img = Image(str(viz_path), width=6*inch, height=3.5*inch)
            img.hAlign = 'CENTER'
            story.append(img)
            story.append(Spacer(1, 0.1*inch))
        except Exception as e:
            pass
    
    # ===== CONCLUSION =====
    story.append(Paragraph("Conclusion", heading1_style))
    
    conclusion = """
    Task 1 has successfully established the foundation for Bayesian change point analysis 
    of Brent oil prices. The comprehensive dataset spans 35+ years with 31 major events 
    categorized by type and severity. Initial EDA reveals significant price volatility 
    ($9.10-$143.95 range) with clear correlations to geopolitical and economic events. 
    The 5-phase analysis workflow provides a structured approach for implementing robust 
    change point detection models. The foundation is complete for proceeding with 
    Bayesian analysis implementation.
    """
    story.append(Paragraph(conclusion, body_style))
    
    # Build PDF
    doc.build(story)
    print(f"\n{'='*60}")
    print("TASK 1 INTERIM REPORT GENERATED!")
    print(f"{'='*60}")
    print(f"Report saved to: {OUTPUT_FILE}")
    print(f"File size: {OUTPUT_FILE.stat().st_size / 1024:.1f} KB")
    print(f"Pages: Focused 1-2 page document")
    print(f"{'='*60}")


if __name__ == "__main__":
    create_task1_report()
