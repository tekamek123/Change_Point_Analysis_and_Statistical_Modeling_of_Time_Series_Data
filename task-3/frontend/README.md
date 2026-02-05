# Brent Oil Price Analysis - Frontend Dashboard

React frontend dashboard for interactive visualization of Brent oil price analysis results.

## Features

### Interactive Visualizations
- **Price Analysis**: Historical price charts with event and change point overlays
- **Event Analysis**: Detailed event impact analysis with price charts
- **Change Points**: Statistical change point detection and visualization
- **Volatility Analysis**: Rolling volatility charts and analysis
- **Correlations**: Event-price correlation tables and metrics

### Dashboard Components
- **Filter Panel**: Date range, event type, and severity filters
- **Statistics Panel**: Real-time statistics and key indicators
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Interactive Charts**: Built with Recharts for smooth interactions

### Key Features
- Event highlight functionality to visualize price spikes/drops
- Drill-down capability for deeper insights
- Real-time data filtering and updates
- Tabbed interface for organized analysis views
c
## Technology Stack

- **React 18.2.0** - Frontend framework
- **Recharts 2.8.0** - Charting library
- **React Bootstrap 5.3.2** - UI components
- **Axios 1.5.0** - HTTP client
- **Date-fns 2.30.0** - Date utilities

## Setup

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm start
```

The app will run on `http://localhost:3000`

3. Build for production:
```bash
npm run build
```

## Prerequisites

The frontend requires the backend API to be running on `http://localhost:5000`. Make sure to start the backend server first.

## Project Structure

```
src/
├── components/
│   ├── PriceChart.js          # Main price visualization
│   ├── EventHighlight.js      # Event impact analysis
│   ├── ChangePointsView.js    # Change point visualization
│   ├── VolatilityAnalysis.js  # Volatility charts
│   ├── StatisticsPanel.js     # Statistics display
│   └── FilterPanel.js         # Data filtering controls
├── App.js                     # Main application component
├── App.css                    # Application styles
├── index.js                   # Application entry point
└── index.css                  # Global styles
```

## Component Descriptions

### PriceChart
- Main visualization component for price data
- Supports price, log returns, and cumulative returns
- Event and change point overlays
- Interactive tooltips and legends

### EventHighlight
- Detailed event impact analysis
- Price charts around specific events
- Quantified impact calculations
- Event statistics and categorization

### ChangePointsView
- Statistical change point visualization
- Significance testing results
- Event association analysis
- Impact quantification

### FilterPanel
- Date range selection with date pickers
- Event type and severity filtering
- Real-time filter application

### StatisticsPanel
- Real-time statistics display
- Key performance indicators
- Dataset information

## API Integration

The frontend integrates with the following backend endpoints:
- `/api/prices/historical` - Price data
- `/api/events` - Events data
- `/api/change-points` - Change point results
- `/api/statistics/summary` - Summary statistics
- `/api/correlation/events-prices` - Correlation analysis
- `/api/volatility/analysis` - Volatility data

## Responsive Design

The dashboard is fully responsive:
- **Desktop**: Full-featured layout with side-by-side panels
- **Tablet**: Adjusted layouts with stacked components
- **Mobile**: Optimized for touch interactions with simplified navigation

## Performance Optimizations

- Component memoization for expensive calculations
- Efficient data filtering and processing
- Optimized chart rendering with Recharts
- Lazy loading of large datasets

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+
