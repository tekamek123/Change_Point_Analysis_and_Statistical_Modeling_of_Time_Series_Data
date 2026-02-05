import React, { useState, useMemo } from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  ReferenceLine,
  ReferenceArea,
  Scatter
} from 'recharts';
import { Card, Form, Button, Row, Col } from 'react-bootstrap';

const PriceChart = ({ prices, events, changePoints }) => {
  const [chartType, setChartType] = useState('price');
  const [showEvents, setShowEvents] = useState(true);
  const [showChangePoints, setShowChangePoints] = useState(true);

  // Prepare chart data
  const chartData = useMemo(() => {
    return prices.map(price => ({
      date: new Date(price.date),
      price: price.price,
      logReturn: price.log_return,
      cumulativeReturn: price.cumulative_return,
      formattedDate: new Date(price.date).toLocaleDateString()
    }));
  }, [prices]);

  // Prepare event data for scatter plot
  const eventData = useMemo(() => {
    return events.map(event => ({
      date: new Date(event.date),
      price: prices.find(p => new Date(p.date).toDateString() === new Date(event.date).toDateString())?.price || null,
      event: event.event,
      eventType: event.event_type,
      severity: event.severity,
      formattedDate: new Date(event.date).toLocaleDateString()
    })).filter(event => event.price !== null);
  }, [events, prices]);

  // Prepare change point data
  const changePointData = useMemo(() => {
    return changePoints.map(cp => ({
      date: new Date(cp.date),
      price: prices.find(p => new Date(p.date).toDateString() === new Date(cp.date).toDateString())?.price || null,
      t_stat: cp.t_stat,
      p_value: cp.p_value,
      percent_change: cp.percent_change,
      formattedDate: new Date(cp.date).toLocaleDateString()
    })).filter(cp => cp.price !== null);
  }, [changePoints, prices]);

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="tooltip-custom">
          <p><strong>Date:</strong> {data.formattedDate}</p>
          {chartType === 'price' && (
            <p><strong>Price:</strong> ${data.price?.toFixed(2)}</p>
          )}
          {chartType === 'logReturn' && (
            <p><strong>Log Return:</strong> {data.logReturn?.toFixed(6)}</p>
          )}
          {chartType === 'cumulativeReturn' && (
            <p><strong>Cumulative Return:</strong> {data.cumulativeReturn?.toFixed(4)}</p>
          )}
          {data.event && (
            <p><strong>Event:</strong> {data.event}</p>
          )}
          {data.percent_change !== undefined && (
            <p><strong>Change:</strong> {data.percent_change.toFixed(2)}%</p>
          )}
        </div>
      );
    }
    return null;
  };

  const formatYAxis = (value) => {
    if (chartType === 'price') {
      return `$${value.toFixed(0)}`;
    }
    return value.toFixed(4);
  };

  const getLineColor = () => {
    switch (chartType) {
      case 'price':
        return '#2563eb';
      case 'logReturn':
        return '#dc2626';
      case 'cumulativeReturn':
        return '#16a34a';
      default:
        return '#2563eb';
    }
  };

  return (
    <Card className="chart-container">
      <Card.Header>
        <Card.Title className="mb-0">Brent Oil Price Analysis</Card.Title>
      </Card.Header>
      <Card.Body>
        <Row className="mb-3">
          <Col md={4}>
            <Form.Group>
              <Form.Label>Chart Type</Form.Label>
              <Form.Select 
                value={chartType} 
                onChange={(e) => setChartType(e.target.value)}
              >
                <option value="price">Price</option>
                <option value="logReturn">Log Returns</option>
                <option value="cumulativeReturn">Cumulative Returns</option>
              </Form.Select>
            </Form.Group>
          </Col>
          <Col md={4}>
            <Form.Group>
              <Form.Label>Show Events</Form.Label>
              <Form.Check 
                type="switch"
                id="show-events"
                checked={showEvents}
                onChange={(e) => setShowEvents(e.target.checked)}
                label="Display Events"
              />
            </Form.Group>
          </Col>
          <Col md={4}>
            <Form.Group>
              <Form.Label>Show Change Points</Form.Label>
              <Form.Check 
                type="switch"
                id="show-change-points"
                checked={showChangePoints}
                onChange={(e) => setShowChangePoints(e.target.checked)}
                label="Display Change Points"
              />
            </Form.Group>
          </Col>
        </Row>

        <ResponsiveContainer width="100%" height={400}>
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis 
              dataKey="formattedDate"
              tick={{ fontSize: 12 }}
              interval="preserveStartEnd"
            />
            <YAxis 
              tickFormatter={formatYAxis}
              tick={{ fontSize: 12 }}
            />
            <Tooltip content={<CustomTooltip />} />
            <Legend />

            <Line
              type="monotone"
              dataKey={chartType}
              stroke={getLineColor()}
              strokeWidth={2}
              dot={false}
              name={chartType === 'price' ? 'Price ($)' : 
                    chartType === 'logReturn' ? 'Log Return' : 
                    'Cumulative Return'}
            />

            {/* Events as scatter points */}
            {showEvents && eventData.length > 0 && (
              <Scatter
                data={eventData}
                fill="#ff6b6b"
                shape="star"
                name="Events"
              />
            )}

            {/* Change points as reference lines */}
            {showChangePoints && changePointData.map((cp, index) => (
              <ReferenceLine
                key={index}
                x={cp.formattedDate}
                stroke="#ff6b6b"
                strokeDasharray="5 5"
                label={`Change Point: ${cp.percent_change.toFixed(1)}%`}
              />
            ))}
          </LineChart>
        </ResponsiveContainer>

        {/* Event Legend */}
        {showEvents && (
          <Row className="mt-3">
            <Col>
              <h6>Event Types:</h6>
              <div className="d-flex flex-wrap gap-2">
                {Array.from(new Set(events.map(e => e.event_type))).map(type => (
                  <span key={type} className="badge bg-secondary">
                    {type}
                  </span>
                ))}
              </div>
            </Col>
          </Row>
        )}

        {/* Change Points Summary */}
        {showChangePoints && changePoints.length > 0 && (
          <Row className="mt-3">
            <Col>
              <h6>Detected Change Points:</h6>
              <div className="table-responsive">
                <table className="table table-sm">
                  <thead>
                    <tr>
                      <th>Date</th>
                      <th>T-Statistic</th>
                      <th>P-Value</th>
                      <th>Change %</th>
                      <th>Closest Event</th>
                    </tr>
                  </thead>
                  <tbody>
                    {changePoints.map((cp, index) => (
                      <tr key={index}>
                        <td>{new Date(cp.date).toLocaleDateString()}</td>
                        <td>{cp.t_stat.toFixed(3)}</td>
                        <td>{cp.p_value.toFixed(6)}</td>
                        <td className={cp.percent_change >= 0 ? 'text-success' : 'text-danger'}>
                          {cp.percent_change >= 0 ? '+' : ''}{cp.percent_change.toFixed(2)}%
                        </td>
                        <td>{cp.closest_event}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </Col>
          </Row>
        )}
      </Card.Body>
    </Card>
  );
};

export default PriceChart;
