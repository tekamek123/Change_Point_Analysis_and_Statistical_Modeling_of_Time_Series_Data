import React, { useState, useEffect } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';
import PriceChart from './components/PriceChart';
import EventHighlight from './components/EventHighlight';
import StatisticsPanel from './components/StatisticsPanel';
import FilterPanel from './components/FilterPanel';
import VolatilityAnalysis from './components/VolatilityAnalysis';
import ChangePointsView from './components/ChangePointsView';
import { Container, Row, Col, Nav, Tab } from 'react-bootstrap';

function App() {
  const [data, setData] = useState({
    prices: [],
    events: [],
    changePoints: [],
    statistics: {},
    correlations: [],
    volatility: {}
  });
  const [filters, setFilters] = useState({
    startDate: '1987-05-20',
    endDate: '2022-11-14',
    eventType: 'all',
    severity: 'all'
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      
      // Fetch all data in parallel
      const [
        pricesResponse,
        eventsResponse,
        changePointsResponse,
        statisticsResponse,
        correlationsResponse,
        volatilityResponse
      ] = await Promise.all([
        fetch('/api/prices/historical'),
        fetch('/api/events'),
        fetch('/api/change-points'),
        fetch('/api/statistics/summary'),
        fetch('/api/correlation/events-prices?window_days=30'),
        fetch('/api/volatility/analysis')
      ]);

      const [
        pricesData,
        eventsData,
        changePointsData,
        statisticsData,
        correlationsData,
        volatilityData
      ] = await Promise.all([
        pricesResponse.json(),
        eventsResponse.json(),
        changePointsResponse.json(),
        statisticsResponse.json(),
        correlationsResponse.json(),
        volatilityResponse.json()
      ]);

      setData({
        prices: pricesData.data || [],
        events: eventsData.data || [],
        changePoints: changePointsData.data || [],
        statistics: statisticsData || {},
        correlations: correlationsData.data || [],
        volatility: volatilityData || {}
      });

      setLoading(false);
    } catch (err) {
      setError('Failed to fetch data. Please ensure the backend server is running.');
      setLoading(false);
    }
  };

  const handleFilterChange = (newFilters) => {
    setFilters(newFilters);
  };

  const filteredData = {
    ...data,
    prices: data.prices.filter(price => {
      const priceDate = new Date(price.date);
      const start = new Date(filters.startDate);
      const end = new Date(filters.endDate);
      return priceDate >= start && priceDate <= end;
    }),
    events: data.events.filter(event => {
      const eventDate = new Date(event.date);
      const start = new Date(filters.startDate);
      const end = new Date(filters.endDate);
      const dateMatch = eventDate >= start && eventDate <= end;
      const typeMatch = filters.eventType === 'all' || event.event_type === filters.eventType;
      const severityMatch = filters.severity === 'all' || event.severity === filters.severity;
      return dateMatch && typeMatch && severityMatch;
    })
  };

  if (loading) {
    return (
      <div className="d-flex justify-content-center align-items-center vh-100">
        <div className="text-center">
          <div className="spinner-border text-primary" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
          <p className="mt-3">Loading Brent Oil Price Dashboard...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="d-flex justify-content-center align-items-center vh-100">
        <div className="alert alert-danger" role="alert">
          <h4 className="alert-heading">Error</h4>
          <p>{error}</p>
          <hr />
          <p className="mb-0">
            Please make sure the Flask backend server is running on localhost:5000
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="App">
      <header className="bg-dark text-white py-3 mb-4">
        <Container>
          <h1 className="text-center mb-0">Brent Oil Price Analysis Dashboard</h1>
          <p className="text-center mb-0 mt-2">Interactive visualization of oil price trends and market events</p>
        </Container>
      </header>

      <Container fluid>
        <Row className="mb-4">
          <Col>
            <FilterPanel 
              filters={filters} 
              onFilterChange={handleFilterChange}
              eventTypes={[...new Set(data.events.map(e => e.event_type))]}
              severities={[...new Set(data.events.map(e => e.severity))]}
            />
          </Col>
        </Row>

        <Row className="mb-4">
          <Col>
            <StatisticsPanel statistics={data.statistics} />
          </Col>
        </Row>

        <Tab.Container id="dashboard-tabs" defaultActiveKey="prices">
          <Row>
            <Col>
              <Nav variant="tabs" className="mb-4">
                <Nav.Item>
                  <Nav.Link eventKey="prices">Price Analysis</Nav.Link>
                </Nav.Item>
                <Nav.Item>
                  <Nav.Link eventKey="events">Event Analysis</Nav.Link>
                </Nav.Item>
                <Nav.Item>
                  <Nav.Link eventKey="change-points">Change Points</Nav.Link>
                </Nav.Item>
                <Nav.Item>
                  <Nav.Link eventKey="volatility">Volatility</Nav.Link>
                </Nav.Item>
                <Nav.Item>
                  <Nav.Link eventKey="correlations">Correlations</Nav.Link>
                </Nav.Item>
              </Nav>
            </Col>
          </Row>

          <Row>
            <Col>
              <Tab.Content>
                <Tab.Pane eventKey="prices">
                  <PriceChart 
                    prices={filteredData.prices} 
                    events={filteredData.events}
                    changePoints={data.changePoints}
                  />
                </Tab.Pane>
                
                <Tab.Pane eventKey="events">
                  <EventHighlight 
                    events={filteredData.events}
                    prices={filteredData.prices}
                  />
                </Tab.Pane>
                
                <Tab.Pane eventKey="change-points">
                  <ChangePointsView 
                    changePoints={data.changePoints}
                    prices={filteredData.prices}
                    events={data.events}
                  />
                </Tab.Pane>
                
                <Tab.Pane eventKey="volatility">
                  <VolatilityAnalysis 
                    volatilityData={data.volatility}
                    prices={filteredData.prices}
                  />
                </Tab.Pane>
                
                <Tab.Pane eventKey="correlations">
                  <div className="card">
                    <div className="card-header">
                      <h5 className="card-title mb-0">Event-Price Correlations</h5>
                    </div>
                    <div className="card-body">
                      <div className="table-responsive">
                        <table className="table table-striped">
                          <thead>
                            <tr>
                              <th>Event Date</th>
                              <th>Event</th>
                              <th>Type</th>
                              <th>Severity</th>
                              <th>Price Before</th>
                              <th>Price After</th>
                              <th>Change %</th>
                            </tr>
                          </thead>
                          <tbody>
                            {data.correlations.slice(0, 20).map((corr, index) => (
                              <tr key={index}>
                                <td>{new Date(corr.event_date).toLocaleDateString()}</td>
                                <td>{corr.event}</td>
                                <td>{corr.event_type}</td>
                                <td>
                                  <span className={`badge bg-${corr.severity === 'High' ? 'danger' : corr.severity === 'Medium' ? 'warning' : 'info'}`}>
                                    {corr.severity}
                                  </span>
                                </td>
                                <td>${corr.price_before.toFixed(2)}</td>
                                <td>${corr.price_after.toFixed(2)}</td>
                                <td className={corr.price_change_percent >= 0 ? 'text-success' : 'text-danger'}>
                                  {corr.price_change_percent >= 0 ? '+' : ''}{corr.price_change_percent.toFixed(2)}%
                                </td>
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>
                    </div>
                  </div>
                </Tab.Pane>
              </Tab.Content>
            </Col>
          </Row>
        </Tab.Container>
      </Container>

      <footer className="bg-dark text-white py-3 mt-5">
        <Container>
          <p className="text-center mb-0">
            Brent Oil Price Analysis Dashboard - Task 3
          </p>
          <p className="text-center mb-0">
            Data Period: {new Date(filters.startDate).toLocaleDateString()} - {new Date(filters.endDate).toLocaleDateString()}
          </p>
        </Container>
      </footer>
    </div>
  );
}

export default App;
