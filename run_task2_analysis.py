#!/usr/bin/env python3
"""
Run Task 2: Bayesian Change Point Detection for Brent Oil Prices
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Try to import PyMC
try:
    import pymc as pm
    import arviz as az
    print("PyMC and ArviZ imported successfully")
except ImportError:
    print("PyMC not installed. Installing...")
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pymc"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "arviz"])
    import pymc as pm
    import arviz as az

from datetime import datetime
import os

# Set plotting style
plt.style.use('default')
sns.set_palette("husl")

print("=" * 60)
print("TASK 2: BAYESIAN CHANGE POINT DETECTION FOR BRENT OIL PRICES")
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
price_df['Log_Return'] = np.log(price_df['Price']).diff()
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
plt.show()

# Summary statistics
print("\nSummary Statistics:")
print(f"Price statistics:")
print(price_df['Price'].describe())
print(f"\nLog Return statistics:")
print(price_df['Log_Return'].describe())
print(f"\nVolatility clustering evidence:")
print(f"Autocorrelation of squared returns (lag 1): {price_df['Log_Return'].dropna().pow(2).autocorr(lag=1):.4f}")

# 2. Build the Bayesian Change Point Model
print("\n2. BUILDING THE BAYESIAN CHANGE POINT MODEL")
print("-" * 50)

# Prepare data for change point analysis
returns_data = price_df['Log_Return'].dropna().values
n_obs = len(returns_data)

print(f"Preparing change point analysis with {n_obs} observations")
print(f"Date range for analysis: {price_df['Date'].iloc[1]} to {price_df['Date'].iloc[-1]}")

# Build Bayesian change point model
print("\nBuilding Bayesian change point model...")

with pm.Model() as change_point_model:
    # Define the Switch Point (tau): Discrete uniform prior over all possible days
    tau = pm.DiscreteUniform('tau', lower=0, upper=n_obs-1)
    
    # Define "Before" and "After" Parameters: Two means (μ₁, μ₂)
    mu_1 = pm.Normal('mu_1', mu=0, sigma=0.01)  # Mean before change point
    mu_2 = pm.Normal('mu_2', mu=0, sigma=0.01)  # Mean after change point
    
    # Prior for standard deviation (assumed same before and after)
    sigma = pm.HalfCauchy('sigma', beta=0.01)
    
    # Use a Switch Function: Select correct parameter based on time index
    mu = pm.math.switch(tau >= np.arange(n_obs), mu_1, mu_2)
    
    # Define the Likelihood: Normal distribution with switching mean
    likelihood = pm.Normal('y', mu=mu, sigma=sigma, observed=returns_data)
    
    print("Model structure:")
    print(f"- Change point tau: Uniform(0, {n_obs-1})")
    print(f"- Mean before: Normal(0, 0.01)")
    print(f"- Mean after: Normal(0, 0.01)")
    print(f"- Standard deviation: HalfCauchy(0, 0.01)")
    print(f"- Likelihood: Normal(mu, sigma)")

# 3. Run the Sampler
print("\n3. RUNNING MCMC SAMPLING")
print("-" * 50)

with change_point_model:
    # Use Metropolis sampler for discrete parameter (tau)
    step = pm.Metropolis()
    
    # Run the Sampler: Use pm.sample() to run the MCMC simulation
    print("Running MCMC sampling...")
    trace = pm.sample(
        draws=5000,  # Reduced for faster execution
        tune=1000,
        step=step,
        chains=2,  # Reduced for faster execution
        random_seed=42,
        progressbar=True,
        return_inferencedata=True
    )

print("\nMCMC sampling completed!")
print(f"Total samples: {trace.posterior.dims['draw'] * trace.posterior.dims['chain']}")
print(f"Chains: {trace.posterior.dims['chain']}")
print(f"Draws per chain: {trace.posterior.dims['draw']}")

# 4. Interpret the Model Output
print("\n4. MODEL INTERPRETATION AND CONVERGENCE CHECKS")
print("-" * 50)

# Check for Convergence: Use pm.summary() and look for r_hat values close to 1.0
print("Convergence diagnostics (R-hat):")
summary = az.summary(trace, var_names=['tau', 'mu_1', 'mu_2', 'sigma'], round_to=4)
print(summary)

# Check R-hat values
r_hat_values = summary['r_hat']
if all(r_hat < 1.1 for r_hat in r_hat_values):
    print("✓ All R-hat values < 1.1 - Good convergence!")
else:
    print("⚠ Some R-hat values ≥ 1.1 - Potential convergence issues")

# Examine trace plots using pm.plot_trace()
print("\nGenerating trace plots...")
az.plot_trace(trace, var_names=['tau', 'mu_1', 'mu_2', 'sigma'])
plt.tight_layout()
plt.savefig('reports/task2_trace_plots.png', dpi=300, bbox_inches='tight')
plt.show()

# 5. Identify the Change Point and Quantify Impact
print("\n5. CHANGE POINT IDENTIFICATION AND IMPACT QUANTIFICATION")
print("-" * 50)

# Extract posterior samples
tau_samples = trace.posterior['tau'].values.flatten()
mu_1_samples = trace.posterior['mu_1'].values.flatten()
mu_2_samples = trace.posterior['mu_2'].values.flatten()
sigma_samples = trace.posterior['sigma'].values.flatten()

# Calculate summary statistics
tau_mean = np.mean(tau_samples)
tau_median = np.median(tau_samples)
tau_hpd = az.hdi(tau_samples, hdi_prob=0.95)

mu_1_mean = np.mean(mu_1_samples)
mu_2_mean = np.mean(mu_2_samples)
mu_1_hpd = az.hdi(mu_1_samples, hdi_prob=0.95)
mu_2_hpd = az.hdi(mu_2_samples, hdi_prob=0.95)

print(f"Change Point Location:")
print(f"- Mean: {tau_mean:.1f} (day index)")
print(f"- Median: {tau_median:.1f} (day index)")
print(f"- 95% HDI: [{tau_hpd[0]:.1f}, {tau_hpd[1]:.1f}]")

# Convert to actual dates
change_point_date = price_df['Date'].iloc[int(tau_median) + 1]  # +1 because we used returns
print(f"- Estimated Date: {change_point_date.strftime('%Y-%m-%d')}")

print(f"\nMean Before Change Point: {mu_1_mean:.6f} (95% HDI: [{mu_1_hpd[0]:.6f}, {mu_1_hpd[1]:.6f}])")
print(f"Mean After Change Point: {mu_2_mean:.6f} (95% HDI: [{mu_2_hpd[0]:.6f}, {mu_2_hpd[1]:.6f}])")
print(f"Difference: {mu_2_mean - mu_1_mean:.6f}")
if mu_1_mean != 0:
    print(f"Percent Change: {((mu_2_mean - mu_1_mean) / abs(mu_1_mean) * 100):.2f}%")

# Plot posterior distribution of tau
print("\nGenerating posterior distributions...")
fig, axes = plt.subplots(2, 2, figsize=(12, 8))

# Change point posterior - A sharp, narrow peak indicates high certainty
az.plot_posterior(trace, var_names=['tau'], ax=axes[0, 0])
axes[0, 0].set_title('Posterior Distribution of Change Point (tau)')

# Means posterior
az.plot_posterior(trace, var_names=['mu_1'], ax=axes[0, 1])
axes[0, 1].set_title('Posterior Distribution of Mean Before Change Point')

az.plot_posterior(trace, var_names=['mu_2'], ax=axes[1, 0])
axes[1, 0].set_title('Posterior Distribution of Mean After Change Point')

az.plot_posterior(trace, var_names=['sigma'], ax=axes[1, 1])
axes[1, 1].set_title('Posterior Distribution of Standard Deviation')

plt.tight_layout()
plt.savefig('reports/task2_posterior_distributions.png', dpi=300, bbox_inches='tight')
plt.show()

# 6. Associate Changes with Causes
print("\n6. EVENT ASSOCIATION ANALYSIS")
print("-" * 50)

# Find events near the change point
event_window = pd.Timedelta(days=60)  # Look 60 days before and after
nearby_events = events_df[
    (events_df['Date'] >= change_point_date - event_window) &
    (events_df['Date'] <= change_point_date + event_window)
].sort_values('Date')

print(f"Events within ±60 days of detected change point:")
if len(nearby_events) > 0:
    for _, event in nearby_events.iterrows():
        days_diff = (event['Date'] - change_point_date).days
        direction = "before" if days_diff < 0 else "after" if days_diff > 0 else "on"
        print(f"- {event['Date'].strftime('%Y-%m-%d')} ({abs(days_diff)} days {direction}): {event['Event']} ({event['Event_Type']}, Severity: {event['Severity']})")
else:
    print("No major events found within ±60 days of the change point.")

# Visualize change point on the data
fig, axes = plt.subplots(2, 1, figsize=(15, 10))

# Plot with change point on returns
axes[0].plot(price_df['Date'][1:], returns_data, linewidth=0.5, alpha=0.7, label='Log Returns')
axes[0].axvline(change_point_date, color='red', linestyle='--', linewidth=2, label=f'Detected Change Point: {change_point_date.strftime("%Y-%m-%d")}')
axes[0].set_title('Log Returns with Detected Change Point', fontsize=14, fontweight='bold')
axes[0].set_xlabel('Date')
axes[0].set_ylabel('Log Return')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# Add nearby events
for _, event in nearby_events.iterrows():
    axes[0].axvline(event['Date'], color='orange', alpha=0.5, linestyle=':')
    axes[0].text(event['Date'], returns_data.max() * 0.8, event['Event'][:20] + '...', 
                rotation=90, fontsize=8, color='orange')

# Plot cumulative returns with change point
cumulative_returns = np.cumsum(returns_data)
axes[1].plot(price_df['Date'][1:], cumulative_returns, linewidth=1, label='Cumulative Log Returns')
axes[1].axvline(change_point_date, color='red', linestyle='--', linewidth=2, label=f'Detected Change Point: {change_point_date.strftime("%Y-%m-%d")}')
axes[1].set_title('Cumulative Log Returns with Detected Change Point', fontsize=14, fontweight='bold')
axes[1].set_xlabel('Date')
axes[1].set_ylabel('Cumulative Log Return')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

# Add nearby events
for _, event in nearby_events.iterrows():
    axes[1].axvline(event['Date'], color='orange', alpha=0.5, linestyle=':')

plt.tight_layout()
plt.savefig('reports/task2_change_point_visualization.png', dpi=300, bbox_inches='tight')
plt.show()

# 7. Quantified Impact Analysis
print("\n7. QUANTIFIED IMPACT ANALYSIS")
print("-" * 50)

print("QUANTIFIED IMPACT SUMMARY:")
print("=" * 40)

if len(nearby_events) > 0:
    # Find the closest event
    closest_event = nearby_events.iloc[(nearby_events['Date'] - change_point_date).abs().argmin()]
    days_to_event = (closest_event['Date'] - change_point_date).days
    
    print(f"Closest Event: {closest_event['Event']}")
    print(f"Event Date: {closest_event['Date'].strftime('%Y-%m-%d')}")
    print(f"Event Type: {closest_event['Event_Type']}")
    print(f"Severity: {closest_event['Severity']}")
    print(f"Days from Change Point: {days_to_event}")
    
    # Calculate price impact
    price_before = np.exp(mu_1_mean) - 1  # Convert log return to approximate percentage
    price_after = np.exp(mu_2_mean) - 1
    
    print(f"\nIMPACT QUANTIFICATION:")
    print(f"Average daily return before change point: {price_before*100:.4f}%")
    print(f"Average daily return after change point: {price_after*100:.4f}%")
    print(f"Daily return change: {(price_after - price_before)*100:.4f}%")
    
    # Annualized impact
    annualized_before = (1 + price_before) ** 252 - 1
    annualized_after = (1 + price_after) ** 252 - 1
    annualized_change = annualized_after - annualized_before
    
    print(f"\nANNUALIZED IMPACT:")
    print(f"Annualized return before: {annualized_before*100:.2f}%")
    print(f"Annualized return after: {annualized_after*100:.2f}%")
    print(f"Annualized change: {annualized_change*100:.2f}%")
    
else:
    print("No specific event association found within the search window.")
    print(f"Change point detected at: {change_point_date.strftime('%Y-%m-%d')}")
    print(f"Average daily return before: {np.exp(mu_1_mean) - 1:.6f}")
    print(f"Average daily return after: {np.exp(mu_2_mean) - 1:.6f}")

print("\n" + "=" * 60)
print("TASK 2 ANALYSIS COMPLETE!")
print("=" * 60)
print(f"Files generated:")
print(f"- reports/task2_price_analysis.png")
print(f"- reports/task2_trace_plots.png") 
print(f"- reports/task2_posterior_distributions.png")
print(f"- reports/task2_change_point_visualization.png")
