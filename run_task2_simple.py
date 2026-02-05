#!/usr/bin/env python3
"""
Run Task 2: Simplified Change Point Detection for Brent Oil Prices
Using a more basic approach when PyMC is not available
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

from datetime import datetime
import os

# Set plotting style
plt.style.use('default')
sns.set_palette("husl")

print("=" * 60)
print("TASK 2: CHANGE POINT DETECTION FOR BRENT OIL PRICES")
print("(Simplified Approach - Statistical Methods)")
print("=" * 60)

# 1. Data Preparation and EDA
print("\n1. DATA PREPARATION AND EXPLORATORY DATA ANALYSIS")
print("-" * 50)

# Load price data
print("Loading Brent oil price data...")
price_df = pd.read_csv('Data/raw/BrentOilPrices.csv')
print(f"Price data shape: {price_df.shape}")
print(f"Price data columns: {price_df.columns.tolist()}")

# Convert date column with multiple format handling
def parse_dates(date_str):
    try:
        # Try format '20-May-1987'
        return pd.to_datetime(date_str, format='%d-%b-%Y')
    except:
        try:
            # Try format 'May 20, 1987'
            return pd.to_datetime(date_str)
        except:
            return pd.NaT

price_df['Date'] = price_df['Date'].apply(parse_dates)
price_df = price_df.dropna(subset=['Date'])
price_df = price_df.sort_values('Date').reset_index(drop=True)

print(f"\nAfter date cleaning:")
print(f"Date range: {price_df['Date'].min()} to {price_df['Date'].max()}")
print(f"Total observations: {len(price_df)}")

# Load event data
events_df = pd.read_csv('Data/events/oil_market_events_fixed.csv')
events_df['Date'] = pd.to_datetime(events_df['Date'])
print(f"\nEvent data shape: {events_df.shape}")
print(f"Event types: {events_df['Event_Type'].value_counts()}")

# Create reports directory
os.makedirs('reports', exist_ok=True)

# Calculate log returns
price_df['Log_Return'] = np.log(price_df['Price']).diff()
returns_data = price_df['Log_Return'].dropna()

# Plot raw prices and log returns
fig, axes = plt.subplots(2, 2, figsize=(15, 10))

# Raw price series
axes[0, 0].plot(price_df['Date'], price_df['Price'], linewidth=1)
axes[0, 0].set_title('Brent Oil Price Series (1987-2022)', fontsize=14, fontweight='bold')
axes[0, 0].set_xlabel('Date')
axes[0, 0].set_ylabel('Price (USD)')
axes[0, 0].grid(True, alpha=0.3)

# Add major events to price plot
for _, event in events_df.iterrows():
    event_date = event['Date']
    if price_df['Date'].min() <= event_date <= price_df['Date'].max():
        axes[0, 0].axvline(event_date, color='red', alpha=0.3, linestyle='--')
        axes[0, 0].text(event_date, price_df['Price'].max() * 0.9, 
                       event['Event'][:15] + '...', rotation=90, 
                       fontsize=8, color='red')

# Log returns
axes[0, 1].plot(price_df['Date'], price_df['Log_Return'], linewidth=0.5, alpha=0.7)
axes[0, 1].set_title('Log Returns of Brent Oil Prices', fontsize=14, fontweight='bold')
axes[0, 1].set_xlabel('Date')
axes[0, 1].set_ylabel('Log Return')
axes[0, 1].grid(True, alpha=0.3)

# Volatility clustering (rolling standard deviation)
rolling_vol = price_df['Log_Return'].rolling(window=30).std()
axes[1, 0].plot(price_df['Date'], rolling_vol, linewidth=1, color='orange')
axes[1, 0].set_title('30-Day Rolling Volatility', fontsize=14, fontweight='bold')
axes[1, 0].set_xlabel('Date')
axes[1, 0].set_ylabel('Volatility')
axes[1, 0].grid(True, alpha=0.3)

# Distribution of returns
axes[1, 1].hist(price_df['Log_Return'].dropna(), bins=100, alpha=0.7, color='skyblue', edgecolor='black')
axes[1, 1].set_title('Distribution of Log Returns', fontsize=14, fontweight='bold')
axes[1, 1].set_xlabel('Log Return')
axes[1, 1].set_ylabel('Frequency')
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('reports/task2_price_analysis.png', dpi=300, bbox_inches='tight')
plt.close()

# Summary statistics
print("\nSummary Statistics:")
print(f"Price statistics:")
print(price_df['Price'].describe())
print(f"\nLog Return statistics:")
print(price_df['Log_Return'].describe())
print(f"\nVolatility clustering evidence:")
print(f"Autocorrelation of squared returns (lag 1): {price_df['Log_Return'].dropna().pow(2).autocorr(lag=1):.4f}")

# 2. Change Point Detection Using Statistical Methods
print("\n2. CHANGE POINT DETECTION USING STATISTICAL METHODS")
print("-" * 50)

def find_change_points(data, min_size=30):
    """
    Find change points using a simple statistical approach
    """
    n = len(data)
    change_points = []
    
    # Use rolling window to detect significant mean changes
    window_size = min(252, n // 4)  # About 1 year of trading days
    
    for i in range(window_size, n - window_size):
        # Before and after windows
        before = data[i-window_size:i]
        after = data[i:i+window_size]
        
        # T-test for difference in means
        t_stat, p_value = stats.ttest_ind(before, after)
        
        # If significant difference, record as potential change point
        if p_value < 0.01:  # 1% significance level
            change_points.append((i, t_stat, p_value))
    
    # Sort by significance (lowest p-value)
    change_points.sort(key=lambda x: x[2])
    
    return change_points

# Find change points in log returns
print("Detecting change points in log returns...")
change_points = find_change_points(returns_data.values)

print(f"Found {len(change_points)} potential change points")

# Select top 5 most significant change points
top_change_points = change_points[:5]
print("\nTop 5 most significant change points:")
for i, (idx, t_stat, p_value) in enumerate(top_change_points):
    date = price_df['Date'].iloc[idx + 1]  # +1 because of diff
    print(f"{i+1}. Index {idx} (Date: {date.strftime('%Y-%m-%d')}) - t-stat: {t_stat:.3f}, p-value: {p_value:.6f}")

# 3. Quantify Impact of Change Points
print("\n3. QUANTIFYING IMPACT OF CHANGE POINTS")
print("-" * 50)

def quantify_impact(data, change_point_idx, window=252):
    """
    Quantify the impact of a change point
    """
    before_window = data[max(0, change_point_idx-window):change_point_idx]
    after_window = data[change_point_idx:min(len(data), change_point_idx+window)]
    
    before_mean = before_window.mean()
    after_mean = after_window.mean()
    before_std = before_window.std()
    after_std = after_window.std()
    
    # Calculate effect size
    effect_size = (after_mean - before_mean) / np.sqrt((before_std**2 + after_std**2) / 2)
    
    return {
        'before_mean': before_mean,
        'after_mean': after_mean,
        'before_std': before_std,
        'after_std': after_std,
        'effect_size': effect_size,
        'percent_change': ((after_mean - before_mean) / abs(before_mean) * 100) if before_mean != 0 else 0
    }

# Analyze top change point
if top_change_points:
    top_idx, _, _ = top_change_points[0]
    impact = quantify_impact(returns_data.values, top_idx)
    
    print(f"\nImpact Analysis for Top Change Point:")
    print(f"Date: {price_df['Date'].iloc[top_idx + 1].strftime('%Y-%m-%d')}")
    print(f"Mean before: {impact['before_mean']:.6f}")
    print(f"Mean after: {impact['after_mean']:.6f}")
    print(f"Change in mean: {impact['after_mean'] - impact['before_mean']:.6f}")
    print(f"Percent change: {impact['percent_change']:.2f}%")
    print(f"Effect size: {impact['effect_size']:.3f}")
    
    # Convert to annualized terms
    annualized_before = (np.exp(impact['before_mean']) - 1) * 252
    annualized_after = (np.exp(impact['after_mean']) - 1) * 252
    print(f"Annualized return before: {annualized_before*100:.2f}%")
    print(f"Annualized return after: {annualized_after*100:.2f}%")
    print(f"Annualized change: {(annualized_after - annualized_before)*100:.2f}%")

# 4. Event Association
print("\n4. EVENT ASSOCIATION ANALYSIS")
print("-" * 50)

def find_nearby_events(change_point_date, events_df, window_days=60):
    """
    Find events near a change point
    """
    window = pd.Timedelta(days=window_days)
    nearby = events_df[
        (events_df['Date'] >= change_point_date - window) &
        (events_df['Date'] <= change_point_date + window)
    ].sort_values('Date')
    return nearby

# Associate events with top change points
for i, (idx, t_stat, p_value) in enumerate(top_change_points[:3]):
    change_date = price_df['Date'].iloc[idx + 1]
    nearby_events = find_nearby_events(change_date, events_df)
    
    print(f"\nChange Point #{i+1} - {change_date.strftime('%Y-%m-%d')}:")
    print(f"T-statistic: {t_stat:.3f}, p-value: {p_value:.6f}")
    
    if len(nearby_events) > 0:
        print("Nearby events:")
        for _, event in nearby_events.iterrows():
            days_diff = (event['Date'] - change_date).days
            direction = "before" if days_diff < 0 else "after" if days_diff > 0 else "on"
            print(f"  - {event['Date'].strftime('%Y-%m-%d')} ({abs(days_diff)} days {direction}): {event['Event']} ({event['Event_Type']}, Severity: {event['Severity']})")
    else:
        print("No major events found within ±60 days")

# 5. Visualizations
print("\n5. GENERATING VISUALIZATIONS")
print("-" * 50)

# Plot change points on returns
fig, axes = plt.subplots(2, 1, figsize=(15, 10))

# Returns with change points
axes[0].plot(price_df['Date'][1:], returns_data, linewidth=0.5, alpha=0.7, label='Log Returns')

# Add change points
colors = ['red', 'orange', 'purple', 'green', 'brown']
for i, (idx, t_stat, p_value) in enumerate(top_change_points[:3]):
    change_date = price_df['Date'].iloc[idx + 1]
    axes[0].axvline(change_date, color=colors[i], linestyle='--', linewidth=2, 
                   label=f'Change Point {i+1}: {change_date.strftime("%Y-%m-%d")}')

axes[0].set_title('Log Returns with Detected Change Points', fontsize=14, fontweight='bold')
axes[0].set_xlabel('Date')
axes[0].set_ylabel('Log Return')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# Cumulative returns with change points
cumulative_returns = np.cumsum(returns_data)
axes[1].plot(price_df['Date'][1:], cumulative_returns, linewidth=1, label='Cumulative Log Returns')

# Add change points
for i, (idx, t_stat, p_value) in enumerate(top_change_points[:3]):
    change_date = price_df['Date'].iloc[idx + 1]
    axes[1].axvline(change_date, color=colors[i], linestyle='--', linewidth=2,
                   label=f'Change Point {i+1}')

axes[1].set_title('Cumulative Log Returns with Detected Change Points', fontsize=14, fontweight='bold')
axes[1].set_xlabel('Date')
axes[1].set_ylabel('Cumulative Log Return')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('reports/task2_change_point_visualization.png', dpi=300, bbox_inches='tight')
plt.close()

# Create a summary plot of means before/after change points
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

for i, (idx, t_stat, p_value) in enumerate(top_change_points[:3]):
    impact = quantify_impact(returns_data.values, idx)
    
    # Bar plot of means
    axes[i].bar(['Before', 'After'], [impact['before_mean'], impact['after_mean']], 
               color=['lightblue', 'lightcoral'])
    axes[i].set_title(f'Change Point {i+1}\n{price_df["Date"].iloc[idx + 1].strftime("%Y-%m-%d")}')
    axes[i].set_ylabel('Mean Log Return')
    axes[i].grid(True, alpha=0.3)
    
    # Add significance indicator
    if p_value < 0.001:
        axes[i].text(0.5, 0.95, '***', transform=axes[i].transAxes, 
                    fontsize=20, ha='center', va='top')
    elif p_value < 0.01:
        axes[i].text(0.5, 0.95, '**', transform=axes[i].transAxes, 
                    fontsize=20, ha='center', va='top')
    elif p_value < 0.05:
        axes[i].text(0.5, 0.95, '*', transform=axes[i].transAxes, 
                    fontsize=20, ha='center', va='top')

plt.tight_layout()
plt.savefig('reports/task2_impact_comparison.png', dpi=300, bbox_inches='tight')
plt.close()

# 6. Summary Report
print("\n6. SUMMARY REPORT")
print("-" * 50)

print("CHANGE POINT DETECTION SUMMARY:")
print("=" * 50)

print(f"Analysis Period: {price_df['Date'].min().strftime('%Y-%m-%d')} to {price_df['Date'].max().strftime('%Y-%m-%d')}")
print(f"Total Observations: {len(price_df)}")
print(f"Return Series: Log returns of daily Brent oil prices")
print(f"Detection Method: Rolling window t-test with 1-year windows")

print(f"\nTop Change Points Detected:")
for i, (idx, t_stat, p_value) in enumerate(top_change_points[:3]):
    change_date = price_df['Date'].iloc[idx + 1]
    impact = quantify_impact(returns_data.values, idx)
    
    print(f"\n{i+1}. Date: {change_date.strftime('%Y-%m-%d')}")
    print(f"   Statistical Significance: t-stat={t_stat:.3f}, p-value={p_value:.6f}")
    print(f"   Mean Return Change: {impact['before_mean']:.6f} → {impact['after_mean']:.6f}")
    print(f"   Percent Change: {impact['percent_change']:.2f}%")
    print(f"   Effect Size: {impact['effect_size']:.3f}")
    
    # Find closest event
    nearby_events = find_nearby_events(change_date, events_df)
    if len(nearby_events) > 0:
        closest = nearby_events.iloc[(nearby_events['Date'] - change_date).abs().argmin()]
        days_diff = (closest['Date'] - change_date).days
        print(f"   Closest Event: {closest['Event']} ({days_diff} days away)")

print("\n" + "=" * 60)
print("TASK 2 ANALYSIS COMPLETE!")
print("=" * 60)
print(f"Files generated:")
print(f"- reports/task2_price_analysis.png")
print(f"- reports/task2_change_point_visualization.png") 
print(f"- reports/task2_impact_comparison.png")
print(f"\nNote: This is a simplified statistical approach to change point detection.")
print(f"For full Bayesian analysis, PyMC would be required but encountered compatibility issues.")
