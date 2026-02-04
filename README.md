# Brent Oil Price Analysis: Impact of Major Events on Market Dynamics

## Overview

This project analyzes how significant political and economic events affect Brent oil prices using Bayesian change point detection. As data scientists at Birhan Energies, we aim to provide actionable intelligence for investors, policymakers, and energy companies navigating the volatile global energy market.

## Business Context

**Client:** Birhan Energies - Leading consultancy firm specializing in data-driven insights for the energy sector

**Challenge:** The oil market's extreme volatility makes it difficult for:
- Investors to make informed decisions and manage risks
- Policymakers to develop strategies for economic stability and energy security  
- Energy companies to plan operations, control costs, and secure supply chains

## Objectives

1. **Identify** key events that have significantly impacted Brent oil prices over the past decade
2. **Quantify** how much these events affect price changes using statistical methods
3. **Provide** clear, data-driven insights to guide investment strategies, policy development, and operational planning

## Data

### Dataset Description
- **Source:** Historical Brent oil prices
- **Period:** May 20, 1987 to September 30, 2022 (daily data)
- **Format:** CSV file with daily price records

### Data Fields
- **Date:** Date of recorded Brent oil price (format: 'day-month-year', e.g., 20-May-87)
- **Price:** Brent oil price in USD per barrel

### Data Location
```
Data/raw/BrentOilPrices.csv
```

## Methodology

### Core Approach: Bayesian Change Point Detection
- **Framework:** PyMC for Bayesian inference and change point detection
- **Focus:** Identifying structural breaks in oil price time series
- **Analysis:** Correlating detected change points with major events:
  - Political decisions
  - Conflicts in oil-producing regions
  - International economic sanctions
  - OPEC policy changes

## Project Structure

```
week11/
├── README.md                 # Project documentation
├── .gitignore               # Git ignore file
├── Data/
│   └── raw/
│       └── BrentOilPrices.csv  # Raw dataset
├── notebooks/               # Jupyter notebooks for analysis
├── src/                     # Source code for models and utilities
├── reports/                 # Analysis reports and findings
└── dashboard/               # Interactive dashboard for insights
```

## Deliverables

### 1. Deep Analysis Report
- Comprehensive Bayesian change point analysis
- Statistical quantification of event impacts
- Data-driven insights and recommendations

### 2. Interactive Dashboard
- Visual exploration of oil price trends
- Event correlation visualization
- Key insights and patterns

### 3. Technical Implementation
- Bayesian inference models using PyMC
- Change point detection algorithms
- Statistical analysis and validation

## Key Focus Areas

- **Bayesian Inference:** Master concepts and implementation using PyMC
- **Change Point Detection:** Identify structural breaks in time series data
- **Event Correlation:** Link detected change points to real-world events
- **Insight Communication:** Clear reporting and intuitive visualization

## Getting Started

### Prerequisites
- Python 3.8+
- PyMC for Bayesian modeling
- Data analysis libraries (pandas, numpy, matplotlib, seaborn)
- Dashboard framework (Streamlit/Dash/Plotly)

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd week11

# Install dependencies
pip install -r requirements.txt
```

### Usage
1. **Data Exploration:** Explore the historical oil price data
2. **Model Building:** Implement Bayesian change point detection
3. **Analysis:** Run statistical analysis and identify key events
4. **Visualization:** Generate insights through the interactive dashboard

## Success Criteria

- **Deep Analysis:** Well-explained Bayesian change point model implementation
- **Technical Mastery:** Strong understanding of Bayesian inference concepts
- **Functional Dashboard:** Quality insights delivered efficiently
- **Clear Communication:** Compelling reports and intuitive visualizations

## Project Timeline

1. **Data Preparation:** Clean and preprocess historical price data
2. **Model Development:** Implement Bayesian change point detection
3. **Event Mapping:** Correlate change points with historical events
4. **Analysis & Insights:** Generate statistical findings and recommendations
5. **Dashboard Development:** Build interactive visualization tool
6. **Reporting:** Create comprehensive analysis report

---

**Note:** This project focuses on quality insights over technical complexity, emphasizing clear communication and actionable intelligence for energy sector stakeholders.
