# Brent Oil Price Analysis - Backend API

Flask backend API for serving Brent oil price analysis data and results.

## Features

- RESTful API endpoints for price data, events, and change point analysis
- Data filtering and date range selection
- Event-price correlation analysis
- Volatility analysis endpoints
- CORS support for frontend integration

## API Endpoints

### Health Check
- `GET /api/health` - Check API status and data loading

### Data Endpoints
- `GET /api/prices/historical` - Get historical price data
  - Query params: `start_date`, `end_date`
- `GET /api/events` - Get events data
  - Query params: `event_type`, `severity`, `start_date`, `end_date`
- `GET /api/change-points` - Get change point analysis results

### Analysis Endpoints
- `GET /api/statistics/summary` - Get summary statistics
- `GET /api/correlation/events-prices` - Get event-price correlations
  - Query params: `window_days` (default: 30)
- `GET /api/volatility/analysis` - Get volatility analysis

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the server:
```bash
python app.py
```

The server will start on `http://localhost:5000`

## Data Sources

The backend loads data from:
- `../../Data/raw/BrentOilPrices.csv` - Historical price data
- `../../Data/events/oil_market_events_fixed.csv` - Market events
- Change point results from Task 2 analysis

## Dependencies

- Flask 2.3.3
- Flask-CORS 4.0.0
- pandas 2.0.3
- numpy 1.24.3

## API Response Format

All endpoints return JSON responses with the following structure:
```json
{
  "data": [...],
  "total_records": 1234,
  "error": "Error message (if any)"
}
```

## Error Handling

- 404: Endpoint not found
- 500: Internal server error
- All errors include descriptive error messages
