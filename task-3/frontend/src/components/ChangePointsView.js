import React, { useState } from 'react';
import { Card, Row, Col, Badge, Button } from 'react-bootstrap';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts';

const ChangePointsView = ({ changePoints, prices, events }) => {
  const [selectedChangePoint, setSelectedChangePoint] = useState(null);

  // Get price data around a change point
  const getPriceDataAroundChangePoint = (changePointDate, daysBefore = 60, daysAfter = 60) => {
    const cpDateTime = new Date(changePointDate);
    const startDate = new Date(cpDateTime);
    startDate.setDate(startDate.getDate() - daysBefore);
    const endDate = new Date(cpDateTime);
    endDate.setDate(endDate.getDate() + daysAfter);

    return prices.filter(price => {
      const priceDate = new Date(price.date);
      return priceDate >= startDate && priceDate <= endDate;
    }).map(price => ({
      ...price,
      date: new Date(price.date),
      formattedDate: new Date(price.date).toLocaleDateString()
    }));
  };

  // Find events near a change point
  const getEventsNearChangePoint = (changePointDate, daysWindow = 30) => {
    const cpDateTime = new Date(changePointDate);
    const startDate = new Date(cpDateTime);
    startDate.setDate(startDate.getDate() - daysWindow);
    const endDate = new Date(cpDateTime);
    endDate.setDate(endDate.getDate() + daysWindow);

    return events.filter(event => {
      const eventDate = new Date(event.date);
      return eventDate >= startDate && eventDate <= endDate;
    }).map(event => ({
      ...event,
      daysFromChangePoint: Math.ceil((new Date(event.date) - cpDateTime) / (1000 * 60 * 60 * 24))
    })).sort((a, b) => Math.abs(a.daysFromChangePoint) - Math.abs(b.daysFromChangePoint));
  };

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="tooltip-custom">
          <p><strong>Date:</strong> {label}</p>
          <p><strong>Price:</strong> ${payload[0].value.toFixed(2)}</p>
        </div>
      );
    }
    return null;
  };

  const getSignificanceColor = (pValue) => {
    if (pValue < 0.001) return 'danger';
    if (pValue < 0.01) return 'warning';
    if (pValue < 0.05) return 'info';
    return 'secondary';
  };

  const getSignificanceStars = (pValue) => {
    if (pValue < 0.001) return '***';
    if (pValue < 0.01) return '**';
    if (pValue < 0.05) return '*';
    return '';
  };

  return (
    <div>
      <Row className="mb-4">
        <Col md={8}>
          <Card>
            <Card.Header>
              <h5 className="mb-0">Change Point Analysis</h5>
            </Card.Header>
            <Card.Body>
              {selectedChangePoint ? (
                <div>
                  <div className="mb-3">
                    <Button 
                      variant="secondary" 
                      onClick={() => setSelectedChangePoint(null)}
                      className="mb-3"
                    >
                      ← Back to All Change Points
                    </Button>
                    <h6>Change Point Analysis</h6>
                    <p className="text-muted">
                      {new Date(selectedChangePoint.date).toLocaleDateString()}
                    </p>
                    <div className="mb-3">
                      <Badge bg={getSignificanceColor(selectedChangePoint.p_value)} className="me-2">
                        {getSignificanceStars(selectedChangePoint.p_value)} p={selectedChangePoint.p_value.toFixed(6)}
                      </Badge>
                      <Badge bg="primary">
                        T-stat: {selectedChangePoint.t_stat.toFixed(3)}
                      </Badge>
                    </div>
                  </div>

                  <div className="mb-4">
                    <h6>Price Impact Around Change Point</h6>
                    <ResponsiveContainer width="100%" height={300}>
                      <LineChart data={getPriceDataAroundChangePoint(selectedChangePoint.date)}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis 
                          dataKey="formattedDate"
                          tick={{ fontSize: 12 }}
                        />
                        <YAxis 
                          tick={{ fontSize: 12 }}
                          tickFormatter={(value) => `$${value.toFixed(0)}`}
                        />
                        <Tooltip content={<CustomTooltip />} />
                        <ReferenceLine 
                          x={new Date(selectedChangePoint.date).toLocaleDateString()} 
                          stroke="#ff6b6b" 
                          strokeDasharray="5 5"
                          label="Change Point"
                        />
                        <Line
                          type="monotone"
                          dataKey="price"
                          stroke="#2563eb"
                          strokeWidth={2}
                          dot={false}
                        />
                      </LineChart>
                    </ResponsiveContainer>
                  </div>

                  <div className="mb-4">
                    <h6>Quantified Impact</h6>
                    <Row>
                      <Col md={4}>
                        <p><strong>Mean Before:</strong> {selectedChangePoint.mean_before?.toFixed(6)}</p>
                        <p><strong>Mean After:</strong> {selectedChangePoint.mean_after?.toFixed(6)}</p>
                      </Col>
                      <Col md={4}>
                        <p><strong>Change:</strong> 
                          <span className={selectedChangePoint.percent_change >= 0 ? 'text-success' : 'text-danger'}>
                            {' '}{selectedChangePoint.percent_change >= 0 ? '+' : ''}{selectedChangePoint.percent_change.toFixed(2)}%
                          </span>
                        </p>
                        <p><strong>Effect Size:</strong> {selectedChangePoint.effect_size?.toFixed(3)}</p>
                      </Col>
                      <Col md={4}>
                        <p><strong>Closest Event:</strong> {selectedChangePoint.closest_event}</p>
                        <p><strong>Days Away:</strong> {selectedChangePoint.event_days_away}</p>
                      </Col>
                    </Row>
                  </div>

                  <div>
                    <h6>Nearby Events</h6>
                    <div className="table-responsive">
                      <table className="table table-sm">
                        <thead>
                          <tr>
                            <th>Event</th>
                            <th>Date</th>
                            <th>Type</th>
                            <th>Days from CP</th>
                          </tr>
                        </thead>
                        <tbody>
                          {getEventsNearChangePoint(selectedChangePoint.date).map((event, index) => (
                            <tr key={index}>
                              <td>{event.event}</td>
                              <td>{new Date(event.date).toLocaleDateString()}</td>
                              <td>
                                <Badge bg="secondary">{event.event_type}</Badge>
                              </td>
                              <td>
                                <span className={event.daysFromChangePoint >= 0 ? 'text-success' : 'text-danger'}>
                                  {event.daysFromChangePoint >= 0 ? '+' : ''}{event.daysFromChangePoint}
                                </span>
                              </td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </div>
                </div>
              ) : (
                <div>
                  <p className="text-muted">Select a change point to view detailed analysis</p>
                  <div className="table-responsive">
                    <table className="table table-hover">
                      <thead>
                        <tr>
                          <th>Date</th>
                          <th>T-Statistic</th>
                          <th>P-Value</th>
                          <th>Significance</th>
                          <th>Mean Before</th>
                          <th>Mean After</th>
                          <th>Change %</th>
                          <th>Closest Event</th>
                          <th>Action</th>
                        </tr>
                      </thead>
                      <tbody>
                        {changePoints.map((cp, index) => (
                          <tr key={index} className="event-card">
                            <td>{new Date(cp.date).toLocaleDateString()}</td>
                            <td>{cp.t_stat.toFixed(3)}</td>
                            <td>{cp.p_value.toFixed(6)}</td>
                            <td>
                              <Badge bg={getSignificanceColor(cp.p_value)}>
                                {getSignificanceStars(cp.p_value)}
                              </Badge>
                            </td>
                            <td>{cp.mean_before?.toFixed(6)}</td>
                            <td>{cp.mean_after?.toFixed(6)}</td>
                            <td className={cp.percent_change >= 0 ? 'text-success' : 'text-danger'}>
                              {cp.percent_change >= 0 ? '+' : ''}{cp.percent_change.toFixed(2)}%
                            </td>
                            <td>{cp.closest_event}</td>
                            <td>
                              <Button 
                                size="sm" 
                                variant="primary"
                                onClick={() => setSelectedChangePoint(cp)}
                              >
                                Analyze
                              </Button>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}
            </Card.Body>
          </Card>
        </Col>
        <Col md={4}>
          <Card>
            <Card.Header>
              <h6 className="mb-0">Change Point Statistics</h6>
            </Card.Header>
            <Card.Body>
              <div className="mb-3">
                <h6>Summary</h6>
                <p><strong>Total Change Points:</strong> {changePoints.length}</p>
                <p><strong>Highly Significant:</strong> {changePoints.filter(cp => cp.p_value < 0.001).length}</p>
                <p><strong>Very Significant:</strong> {changePoints.filter(cp => cp.p_value < 0.01).length}</p>
                <p><strong>Significant:</strong> {changePoints.filter(cp => cp.p_value < 0.05).length}</p>
              </div>

              <div className="mb-3">
                <h6>Impact Distribution</h6>
                <p><strong>Positive Changes:</strong> {changePoints.filter(cp => cp.percent_change > 0).length}</p>
                <p><strong>Negative Changes:</strong> {changePoints.filter(cp => cp.percent_change < 0).length}</p>
                <p><strong>Average Impact:</strong> {(changePoints.reduce((sum, cp) => sum + cp.percent_change, 0) / changePoints.length).toFixed(2)}%</p>
                <p><strong>Max Positive:</strong> {Math.max(...changePoints.map(cp => cp.percent_change)).toFixed(2)}%</p>
                <p><strong>Max Negative:</strong> {Math.min(...changePoints.map(cp => cp.percent_change)).toFixed(2)}%</p>
              </div>

              <div>
                <h6>Significance Levels</h6>
                <div className="mb-2">
                  <small><strong>***</strong> p &lt; 0.001 (Highly Significant)</small>
                </div>
                <div className="mb-2">
                  <small><strong>**</strong> p &lt; 0.01 (Very Significant)</small>
                </div>
                <div className="mb-2">
                  <small><strong>*</strong> p &lt; 0.05 (Significant)</small>
                </div>
              </div>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default ChangePointsView;
