#!/usr/bin/env python3
"""
Flask Backend for Brent Oil Price Analysis Dashboard
API endpoints for serving analysis results and data
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import numpy as np
import json
import os
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

# Load data at startup
def load_data():
    """Load all necessary data files"""
    global price_df, events_df, change_points
    
    # Load price data
    price_path = os.path.join(os.path.dirname(__file__), '..', '..', 'Data', 'raw', 'BrentOilPrices.csv')
    price_df = pd.read_csv(price_path)
    
    # Convert dates
    def parse_dates(date_str):
        try:
            return pd.to_datetime(date_str, format='%d-%b-%Y')
        except:
            return pd.to_datetime(date_str)
    
    price_df['Date'] = price_df['Date'].apply(parse_dates)
    price_df = price_df.dropna(subset=['Date'])
    price_df = price_df.sort_values('Date').reset_index(drop=True)
    
    # Calculate log returns
    price_df['Log_Return'] = np.log(price_df['Price']).diff()
    price_df['Cumulative_Return'] = np.cumsum(price_df['Log_Return'])
    
    # Load events data
    events_path = os.path.join(os.path.dirname(__file__), '..', '..', 'Data', 'events', 'oil_market_events_fixed.csv')
    events_df = pd.read_csv(events_path)
    events_df['Date'] = pd.to_datetime(events_df['Date'])
    
    # Load change point results (from Task 2 analysis)
    change_points = [
        {'date': '2020-04-22', 't_stat': -3.418, 'p_value': 0.000681, 
         'mean_before': -0.008210, 'mean_after': 0.007886, 'percent_change': 196.06,
         'closest_event': 'Negative Oil Prices (-$37/barrel)', 'event_days_away': -2},
        {'date': '2014-01-16', 't_stat': 3.115, 'p_value': 0.001943,
         'mean_before': -0.000131, 'mean_after': -0.003466, 'percent_change': -2544.19,
         'closest_event': 'No major event found', 'event_days_away': None},
        {'date': '2014-01-17', 't_stat': 3.034, 'p_value': 0.002540,
         'mean_before': -0.000128, 'mean_after': -0.003383, 'percent_change': -2552.04,
         'closest_event': 'No major event found', 'event_days_away': None}
    ]
    
    return price_df, events_df, change_points

# Initialize data
price_df, events_df, change_points = load_data()

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'data_loaded': len(price_df) > 0 and len(events_df) > 0
    })

@app.route('/api/prices/historical', methods=['GET'])
def get_historical_prices():
    """Get historical price data with optional filtering"""
    try:
        # Get query parameters
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        # Filter data
        filtered_df = price_df.copy()
        
        if start_date:
            filtered_df = filtered_df[filtered_df['Date'] >= pd.to_datetime(start_date)]
        if end_date:
            filtered_df = filtered_df[filtered_df['Date'] <= pd.to_datetime(end_date)]
        
        # Convert to JSON-serializable format
        data = []
        for _, row in filtered_df.iterrows():
            data.append({
                'date': row['Date'].isoformat(),
                'price': float(row['Price']),
                'log_return': float(row['Log_Return']) if pd.notna(row['Log_Return']) else None,
                'cumulative_return': float(row['Cumulative_Return']) if pd.notna(row['Cumulative_Return']) else None
            })
        
        return jsonify({
            'data': data,
            'total_records': len(data),
            'date_range': {
                'start': filtered_df['Date'].min().isoformat() if len(filtered_df) > 0 else None,
                'end': filtered_df['Date'].max().isoformat() if len(filtered_df) > 0 else None
            }
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/events', methods=['GET'])
def get_events():
    """Get events data with optional filtering"""
    try:
        # Get query parameters
        event_type = request.args.get('event_type')
        severity = request.args.get('severity')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        # Filter data
        filtered_df = events_df.copy()
        
        if event_type:
            filtered_df = filtered_df[filtered_df['Event_Type'] == event_type]
        if severity:
            filtered_df = filtered_df[filtered_df['Severity'] == severity]
        if start_date:
            filtered_df = filtered_df[filtered_df['Date'] >= pd.to_datetime(start_date)]
        if end_date:
            filtered_df = filtered_df[filtered_df['Date'] <= pd.to_datetime(end_date)]
        
        # Convert to JSON-serializable format
        data = []
        for _, row in filtered_df.iterrows():
            data.append({
                'date': row['Date'].isoformat(),
                'event': row['Event'],
                'event_type': row['Event_Type'],
                'severity': row['Severity'],
                'description': row['Description'],
                'duration': row['Duration']
            })
        
        return jsonify({
            'data': data,
            'total_records': len(data),
            'event_types': events_df['Event_Type'].unique().tolist(),
            'severities': events_df['Severity'].unique().tolist()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/change-points', methods=['GET'])
def get_change_points():
    """Get change point analysis results"""
    try:
        return jsonify({
            'data': change_points,
            'total_change_points': len(change_points)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/statistics/summary', methods=['GET'])
def get_summary_statistics():
    """Get summary statistics for the dataset"""
    try:
        # Calculate statistics
        stats = {
            'price_stats': {
                'mean': float(price_df['Price'].mean()),
                'median': float(price_df['Price'].median()),
                'std': float(price_df['Price'].std()),
                'min': float(price_df['Price'].min()),
                'max': float(price_df['Price'].max()),
                'current': float(price_df['Price'].iloc[-1])
            },
            'return_stats': {
                'mean': float(price_df['Log_Return'].mean()),
                'std': float(price_df['Log_Return'].std()),
                'min': float(price_df['Log_Return'].min()),
                'max': float(price_df['Log_Return'].max()),
                'volatility_clustering': float(price_df['Log_Return'].dropna().pow(2).autocorr(lag=1))
            },
            'dataset_info': {
                'total_records': len(price_df),
                'date_range': {
                    'start': price_df['Date'].min().isoformat(),
                    'end': price_df['Date'].max().isoformat()
                },
                'total_events': len(events_df),
                'total_change_points': len(change_points)
            }
        }
        
        return jsonify(stats)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/correlation/events-prices', methods=['GET'])
def get_event_price_correlation():
    """Analyze correlation between events and price changes"""
    try:
        # Get query parameters
        window_days = int(request.args.get('window_days', 30))
        
        correlations = []
        
        for _, event in events_df.iterrows():
            event_date = event['Date']
            
            # Find price data around event
            start_date = event_date - timedelta(days=window_days)
            end_date = event_date + timedelta(days=window_days)
            
            price_window = price_df[
                (price_df['Date'] >= start_date) & 
                (price_df['Date'] <= end_date)
            ].copy()
            
            if len(price_window) > 10:  # Ensure sufficient data
                # Calculate price change before and after event
                before_event = price_window[price_window['Date'] < event_date]
                after_event = price_window[price_window['Date'] >= event_date]
                
                if len(before_event) > 0 and len(after_event) > 0:
                    price_before = before_event['Price'].mean()
                    price_after = after_event['Price'].mean()
                    price_change = ((price_after - price_before) / price_before) * 100
                    
                    correlations.append({
                        'event_date': event_date.isoformat(),
                        'event': event['Event'],
                        'event_type': event['Event_Type'],
                        'severity': event['Severity'],
                        'price_before': float(price_before),
                        'price_after': float(price_after),
                        'price_change_percent': float(price_change),
                        'window_days': window_days
                    })
        
        # Sort by absolute price change
        correlations.sort(key=lambda x: abs(x['price_change_percent']), reverse=True)
        
        return jsonify({
            'data': correlations,
            'window_days': window_days,
            'total_correlations': len(correlations)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/volatility/analysis', methods=['GET'])
def get_volatility_analysis():
    """Get volatility analysis data"""
    try:
        # Calculate rolling volatility
        window_sizes = [7, 30, 90]  # 1 week, 1 month, 3 months
        
        volatility_data = {}
        
        for window in window_sizes:
            rolling_vol = price_df['Log_Return'].rolling(window=window).std()
            
            vol_data = []
            for i, vol in enumerate(rolling_vol):
                if pd.notna(vol):
                    vol_data.append({
                        'date': price_df['Date'].iloc[i].isoformat(),
                        'volatility': float(vol),
                        'window_size': window
                    })
            
            volatility_data[f'window_{window}'] = vol_data
        
        # Find high volatility periods
        high_vol_threshold = price_df['Log_Return'].rolling(window=30).std().quantile(0.9)
        high_vol_periods = price_df[
            price_df['Log_Return'].rolling(window=30).std() > high_vol_threshold
        ]['Date'].tolist()
        
        return jsonify({
            'volatility_data': volatility_data,
            'high_volatility_periods': [date.isoformat() for date in high_vol_periods],
            'volatility_threshold': float(high_vol_threshold)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("Starting Flask backend server...")
    print("Available endpoints:")
    print("- GET /api/health - Health check")
    print("- GET /api/prices/historical - Historical price data")
    print("- GET /api/events - Events data")
    print("- GET /api/change-points - Change point analysis")
    print("- GET /api/statistics/summary - Summary statistics")
    print("- GET /api/correlation/events-prices - Event-price correlations")
    print("- GET /api/volatility/analysis - Volatility analysis")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
