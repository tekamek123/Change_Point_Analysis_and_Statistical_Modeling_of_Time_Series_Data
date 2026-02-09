# Task 3: Interactive Dashboard for Brent Oil Price Analysis

## Overview

This project delivers a comprehensive interactive dashboard for visualizing Brent oil price analysis results, allowing stakeholders to explore how various events affect oil prices through intuitive visualizations and data exploration tools.

## Architecture

The application follows a modern full-stack architecture:

```
task-3/
├── backend/          # Flask API server
│   ├── app.py        # Main Flask application
│   ├── requirements.txt
│   └── README.md
├── frontend/         # React dashboard
│   ├── src/
│   │   ├── components/
│   │   ├── App.js
│   │   └── ...
│   ├── public/
│   ├── package.json
│   └── README.md
└── README.md         # This file
```

## Features

### Backend (Flask)
- **RESTful API**: Clean, documented endpoints for all data needs
- **Data Serving**: Historical prices, events, change points, and analysis results
- **Filtering Support**: Date ranges, event types, severity levels
- **Analysis Endpoints**: Correlations, volatility, statistics
- **CORS Enabled**: Seamless frontend integration

### Frontend (React)
- **Interactive Visualizations**: Multiple chart types with Recharts
- **Event Highlight Functionality**: Click events to see price impacts
- **Drill-down Capability**: Deep analysis of specific events and change points
- **Responsive Design**: Optimized for desktop, tablet, and mobile
- **Real-time Filtering**: Dynamic data filtering without page reloads

### Key Dashboard Features
1. **Price Analysis Tab**: Historical trends with event and change point overlays
2. **Event Analysis Tab**: Detailed event impact visualization
3. **Change Points Tab**: Statistical change point detection results
4. **Volatility Tab**: Rolling volatility analysis
5. **Correlations Tab**: Event-price correlation tables

## Quick Start

### Prerequisites
- Python 3.8+ for backend
- Node.js 14+ for frontend
- npm or yarn package manager

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python app.py
```
The API will be available at `http://localhost:5000`

### Frontend Setup
```bash
cd frontend
npm install
npm start
```
The dashboard will be available at `http://localhost:3000`

## API Endpoints

| Endpoint | Method | Description | Parameters |
|----------|--------|-------------|------------|
| `/api/health` | GET | Health check | - |
| `/api/prices/historical` | GET | Historical price data | `start_date`, `end_date` |
| `/api/events` | GET | Events data | `event_type`, `severity`, `start_date`, `end_date` |
| `/api/change-points` | GET | Change point results | - |
| `/api/statistics/summary` | GET | Summary statistics | - |
| `/api/correlation/events-prices` | GET | Event-price correlations | `window_days` |
| `/api/volatility/analysis` | GET | Volatility analysis | - |

## Dashboard Components

### Filter Panel
- **Date Range Selection**: Interactive date pickers for start/end dates
- **Event Type Filter**: Filter by geopolitical conflicts, OPEC decisions, etc.
- **Severity Filter**: Filter by High/Medium/Low severity events
- **Reset Function**: Quickly reset all filters to default

### Statistics Panel
- **Key Indicators**: Current price, average price, volatility metrics
- **Dataset Information**: Total records, date ranges, event counts
- **Real-time Updates**: Statistics update with filtered data

### Price Chart
- **Multiple Views**: Price, log returns, cumulative returns
- **Event Overlays**: Visual markers for major events
- **Change Point Lines**: Vertical lines at detected structural breaks
- **Interactive Tooltips**: Hover for detailed information

### Event Analysis
- **Event List**: Table of all events with impact calculations
- **Impact Visualization**: Price charts around specific events
- **Quantified Impact**: Before/after price changes and percentages
- **Event Statistics**: Distribution by type and severity

### Change Points View
- **Statistical Results**: T-statistics, p-values, significance levels
- **Impact Analysis**: Mean changes before/after each change point
- **Event Association**: Nearby events and temporal relationships
- **Significance Indicators**: Visual markers for statistical significance

## Data Integration

The dashboard integrates data from previous tasks:
- **Task 1**: Event dataset and historical price data
- **Task 2**: Change point detection results and statistical analysis
- **Real-time Calculations**: Event impacts, correlations, volatility metrics

## Technical Implementation

### Backend Technologies
- **Flask**: Lightweight, flexible web framework
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computations
- **Flask-CORS**: Cross-origin resource sharing

### Frontend Technologies
- **React 18**: Modern component-based framework
- **Recharts**: Declarative charting library
- **React Bootstrap**: Responsive UI components
- **Axios**: Promise-based HTTP client
- **React Datepicker**: Date selection components

### Performance Features
- **Efficient Data Loading**: Parallel API calls for optimal performance
- **Component Memoization**: Prevent unnecessary re-renders
- **Lazy Loading**: Load data only when needed
- **Responsive Charts**: Optimized rendering for different screen sizes

## Usage Examples

### Analyzing Event Impact
1. Navigate to the "Event Analysis" tab
2. Browse the event list or use filters to find specific events
3. Click "Analyze" on any event to see detailed price impact
4. View the price chart with the event date marked
5. Review quantified impact metrics

### Exploring Change Points
1. Go to the "Change Points" tab
2. Review the statistical significance of detected change points
3. Click "Analyze" on any change point for detailed view
4. Examine nearby events and their temporal relationships
5. Review the quantified impact on mean returns

### Custom Date Analysis
1. Use the Filter Panel to select a specific date range
2. Apply event type or severity filters if needed
3. All dashboard views will update automatically
4. Switch between tabs to see different aspects of the filtered data

## Screenshots

*(Include screenshots demonstrating dashboard functionality)*

1. **Main Dashboard View**: Overview with statistics and price chart
2. **Event Impact Analysis**: Detailed event analysis with price charts
3. **Change Point Visualization**: Statistical results with event associations
4. **Mobile Responsive View**: Optimized layout for mobile devices

## Future Enhancements

### Advanced Features
- **Real-time Data Integration**: Live price feeds and event updates
- **Machine Learning Integration**: Predictive models and forecasting
- **Advanced Visualizations**: Heatmaps, correlation matrices, network graphs
- **Export Functionality**: PDF reports, CSV data export
- **User Preferences**: Customizable dashboard layouts and settings

### Technical Improvements
- **Database Integration**: PostgreSQL or MongoDB for better data management
- **Caching Layer**: Redis for improved performance
- **Authentication**: User accounts and saved preferences
- **API Documentation**: OpenAPI/Swagger documentation
- **Testing Suite**: Comprehensive unit and integration tests

## Troubleshooting

### Common Issues
1. **Backend Not Running**: Ensure Flask server is running on port 5000
2. **CORS Errors**: Check that Flask-CORS is properly configured
3. **Data Loading Issues**: Verify data files exist in correct paths
4. **Chart Rendering**: Check browser console for JavaScript errors

### Development Tips
- Use browser developer tools to debug API calls
- Check network tab for failed requests
- Monitor console for React component errors
- Verify data formats match expected schemas

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is part of the Brent Oil Price Analysis training module.
