import React from 'react';
import { Card, Row, Col } from 'react-bootstrap';

const StatisticsPanel = ({ statistics }) => {
  if (!statistics || !statistics.price_stats) {
    return <div>Loading statistics...</div>;
  }

  const formatNumber = (num, decimals = 2) => {
    return num ? num.toFixed(decimals) : 'N/A';
  };

  const formatPercent = (num, decimals = 2) => {
    return num ? `${num.toFixed(decimals)}%` : 'N/A';
  };

  const statCards = [
    {
      title: 'Current Price',
      value: `$${formatNumber(statistics.price_stats?.current)}`,
      change: null,
      icon: '📈'
    },
    {
      title: 'Average Price',
      value: `$${formatNumber(statistics.price_stats?.mean)}`,
      change: null,
      icon: '📊'
    },
    {
      title: 'Price Range',
      value: `$${formatNumber(statistics.price_stats?.min)} - $${formatNumber(statistics.price_stats?.max)}`,
      change: null,
      icon: '📉'
    },
    {
      title: 'Volatility',
      value: formatNumber(statistics.return_stats?.std * 100, 4),
      change: null,
      icon: '📊'
    },
    {
      title: 'Total Events',
      value: statistics.dataset_info?.total_events || 0,
      change: null,
      icon: '📅'
    },
    {
      title: 'Change Points',
      value: statistics.dataset_info?.total_change_points || 0,
      change: null,
      icon: '🔄'
    }
  ];

  return (
    <div className="statistics-panel">
      <Row>
        {statCards.map((stat, index) => (
          <Col key={index} md={2} sm={6} className="mb-3">
            <div className="stat-card">
              <div className="d-flex justify-content-between align-items-start">
                <div>
                  <h6>{stat.title}</h6>
                  <div className="stat-value">{stat.value}</div>
                  {stat.change && (
                    <div className={`stat-change ${stat.change >= 0 ? 'positive' : 'negative'}`}>
                      {stat.change >= 0 ? '↑' : '↓'} {Math.abs(stat.change).toFixed(2)}%
                    </div>
                  )}
                </div>
                <div className="stat-icon">
                  <span style={{ fontSize: '1.5rem' }}>{stat.icon}</span>
                </div>
              </div>
            </div>
          </Col>
        ))}
      </Row>

      <Row className="mt-4">
        <Col md={6}>
          <Card className="h-100">
            <Card.Header>
              <h6 className="mb-0">Price Statistics</h6>
            </Card.Header>
            <Card.Body>
              <div className="row">
                <div className="col-6">
                  <p><strong>Mean:</strong> ${formatNumber(statistics.price_stats?.mean)}</p>
                  <p><strong>Median:</strong> ${formatNumber(statistics.price_stats?.median)}</p>
                  <p><strong>Std Dev:</strong> ${formatNumber(statistics.price_stats?.std)}</p>
                </div>
                <div className="col-6">
                  <p><strong>Min:</strong> ${formatNumber(statistics.price_stats?.min)}</p>
                  <p><strong>Max:</strong> ${formatNumber(statistics.price_stats?.max)}</p>
                  <p><strong>Current:</strong> ${formatNumber(statistics.price_stats?.current)}</p>
                </div>
              </div>
            </Card.Body>
          </Card>
        </Col>
        <Col md={6}>
          <Card className="h-100">
            <Card.Header>
              <h6 className="mb-0">Return Statistics</h6>
            </Card.Header>
            <Card.Body>
              <div className="row">
                <div className="col-6">
                  <p><strong>Mean Return:</strong> {formatNumber(statistics.return_stats?.mean, 6)}</p>
                  <p><strong>Std Dev:</strong> {formatNumber(statistics.return_stats?.std, 6)}</p>
                  <p><strong>Min Return:</strong> {formatNumber(statistics.return_stats?.min, 6)}</p>
                </div>
                <div className="col-6">
                  <p><strong>Max Return:</strong> {formatNumber(statistics.return_stats?.max, 6)}</p>
                  <p><strong>Volatility Clustering:</strong> {formatNumber(statistics.return_stats?.volatility_clustering, 4)}</p>
                  <p><strong>Annualized Vol:</strong> {formatNumber(statistics.return_stats?.std * Math.sqrt(252) * 100, 2)}%</p>
                </div>
              </div>
            </Card.Body>
          </Card>
        </Col>
      </Row>

      <Row className="mt-3">
        <Col>
          <Card>
            <Card.Header>
              <h6 className="mb-0">Dataset Information</h6>
            </Card.Header>
            <Card.Body>
              <div className="row">
                <div className="col-md-3">
                  <p><strong>Total Records:</strong> {statistics.dataset_info?.total_records?.toLocaleString()}</p>
                  <p><strong>Total Events:</strong> {statistics.dataset_info?.total_events}</p>
                </div>
                <div className="col-md-3">
                  <p><strong>Change Points:</strong> {statistics.dataset_info?.total_change_points}</p>
                  <p><strong>Data Period:</strong></p>
                </div>
                <div className="col-md-6">
                  <p><strong>Start Date:</strong> {statistics.dataset_info?.date_range?.start ? new Date(statistics.dataset_info.date_range.start).toLocaleDateString() : 'N/A'}</p>
                  <p><strong>End Date:</strong> {statistics.dataset_info?.date_range?.end ? new Date(statistics.dataset_info.date_range.end).toLocaleDateString() : 'N/A'}</p>
                </div>
              </div>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default StatisticsPanel;
