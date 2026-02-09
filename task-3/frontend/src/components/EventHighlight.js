import React, { useState } from "react";
import { Card, Row, Col, Badge, Button, Collapse } from "react-bootstrap";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine,
} from "recharts";

const EventHighlight = ({ events, prices }) => {
  const [selectedEvent, setSelectedEvent] = useState(null);
  const [expandedEvent, setExpandedEvent] = useState(null);

  // Get price data around an event
  const getPriceDataAroundEvent = (
    eventDate,
    daysBefore = 30,
    daysAfter = 30,
  ) => {
    const eventDateTime = new Date(eventDate);
    const startDate = new Date(eventDateTime);
    startDate.setDate(startDate.getDate() - daysBefore);
    const endDate = new Date(eventDateTime);
    endDate.setDate(endDate.getDate() + daysAfter);

    return prices
      .filter((price) => {
        const priceDate = new Date(price.date);
        return priceDate >= startDate && priceDate <= endDate;
      })
      .map((price) => ({
        ...price,
        date: new Date(price.date),
        formattedDate: new Date(price.date).toLocaleDateString(),
      }));
  };

  // Calculate price impact of an event
  const calculateEventImpact = (event) => {
    const beforeData = prices.filter(
      (price) => new Date(price.date) < new Date(event.date),
    );
    const afterData = prices.filter(
      (price) => new Date(price.date) >= new Date(event.date),
    );

    if (beforeData.length === 0 || afterData.length === 0) {
      return null;
    }

    const beforePrice = beforeData[beforeData.length - 1].price;
    const afterPrice = afterData[0].price;
    const priceChange = ((afterPrice - beforePrice) / beforePrice) * 100;

    return {
      beforePrice,
      afterPrice,
      priceChange,
      daysDifference: Math.ceil(
        (new Date(afterData[0].date) -
          new Date(beforeData[beforeData.length - 1].date)) /
          (1000 * 60 * 60 * 24),
      ),
    };
  };

  const getSeverityColor = (severity) => {
    switch (severity) {
      case "High":
        return "danger";
      case "Medium":
        return "warning";
      case "Low":
        return "success";
      default:
        return "secondary";
    }
  };

  const getEventTypeColor = (eventType) => {
    const colors = {
      "Geopolitical Conflict": "danger",
      "OPEC Decision": "warning",
      "International Sanctions": "info",
      "Economic Shock": "dark",
      "Natural Disaster": "success",
      "Market Event": "primary",
      "Environmental Disaster": "success",
      "Health Crisis": "danger",
    };
    return colors[eventType] || "secondary";
  };

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="tooltip-custom">
          <p>
            <strong>Date:</strong> {label}
          </p>
          <p>
            <strong>Price:</strong> ${payload[0].value.toFixed(2)}
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <div>
      <Row className="mb-4">
        <Col md={8}>
          <Card>
            <Card.Header>
              <h5 className="mb-0">Event Impact Analysis</h5>
            </Card.Header>
            <Card.Body>
              {selectedEvent ? (
                <div>
                  <div className="mb-3">
                    <Button
                      variant="secondary"
                      onClick={() => setSelectedEvent(null)}
                      className="mb-3"
                    >
                      ← Back to Events List
                    </Button>
                    <h6>{selectedEvent.event}</h6>
                    <p className="text-muted">
                      {new Date(selectedEvent.date).toLocaleDateString()} •{" "}
                      {selectedEvent.event_type}
                    </p>
                    <div className="mb-3">
                      <Badge
                        bg={getSeverityColor(selectedEvent.severity)}
                        className="me-2"
                      >
                        {selectedEvent.severity} Severity
                      </Badge>
                      <Badge bg={getEventTypeColor(selectedEvent.event_type)}>
                        {selectedEvent.event_type}
                      </Badge>
                    </div>
                    <p>{selectedEvent.description}</p>
                  </div>

                  <div className="event-impact-chart">
                    <h6>Price Impact Around Event</h6>
                    <ResponsiveContainer width="100%" height={300}>
                      <LineChart
                        data={getPriceDataAroundEvent(selectedEvent.date)}
                      >
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
                          x={new Date(selectedEvent.date).toLocaleDateString()}
                          stroke="#ff6b6b"
                          strokeDasharray="5 5"
                          label="Event Date"
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

                  {calculateEventImpact(selectedEvent) && (
                    <div className="mt-3">
                      <h6>Quantified Impact</h6>
                      <Row>
                        <Col md={4}>
                          <p>
                            <strong>Price Before:</strong> $
                            {calculateEventImpact(
                              selectedEvent,
                            ).beforePrice.toFixed(2)}
                          </p>
                          <p>
                            <strong>Price After:</strong> $
                            {calculateEventImpact(
                              selectedEvent,
                            ).afterPrice.toFixed(2)}
                          </p>
                        </Col>
                        <Col md={4}>
                          <p>
                            <strong>Price Change:</strong>
                            <span
                              className={
                                calculateEventImpact(selectedEvent)
                                  .priceChange >= 0
                                  ? "text-success"
                                  : "text-danger"
                              }
                            >
                              {" "}
                              {calculateEventImpact(selectedEvent)
                                .priceChange >= 0
                                ? "+"
                                : ""}
                              {calculateEventImpact(
                                selectedEvent,
                              ).priceChange.toFixed(2)}
                              %
                            </span>
                          </p>
                          <p>
                            <strong>Time Gap:</strong>{" "}
                            {calculateEventImpact(selectedEvent).daysDifference}{" "}
                            days
                          </p>
                        </Col>
                      </Row>
                    </div>
                  )}
                </div>
              ) : (
                <div>
                  <p className="text-muted">
                    Select an event to view its impact on oil prices
                  </p>
                  <div className="table-responsive">
                    <table className="table table-hover">
                      <thead>
                        <tr>
                          <th>Date</th>
                          <th>Event</th>
                          <th>Type</th>
                          <th>Severity</th>
                          <th>Impact</th>
                          <th>Action</th>
                        </tr>
                      </thead>
                      <tbody>
                        {events.slice(0, 20).map((event, index) => {
                          const impact = calculateEventImpact(event);
                          return (
                            <tr key={index} className="event-card">
                              <td>
                                {new Date(event.date).toLocaleDateString()}
                              </td>
                              <td>
                                <div>
                                  <strong>{event.event}</strong>
                                  <br />
                                  <small className="text-muted">
                                    {event.duration}
                                  </small>
                                </div>
                              </td>
                              <td>
                                <Badge bg={getEventTypeColor(event.event_type)}>
                                  {event.event_type}
                                </Badge>
                              </td>
                              <td>
                                <Badge bg={getSeverityColor(event.severity)}>
                                  {event.severity}
                                </Badge>
                              </td>
                              <td>
                                {impact ? (
                                  <span
                                    className={
                                      impact.priceChange >= 0
                                        ? "text-success"
                                        : "text-danger"
                                    }
                                  >
                                    {impact.priceChange >= 0 ? "↑" : "↓"}{" "}
                                    {Math.abs(impact.priceChange).toFixed(2)}%
                                  </span>
                                ) : (
                                  <span className="text-muted">N/A</span>
                                )}
                              </td>
                              <td>
                                <Button
                                  size="sm"
                                  variant="primary"
                                  onClick={() => setSelectedEvent(event)}
                                >
                                  Analyze
                                </Button>
                              </td>
                            </tr>
                          );
                        })}
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
              <h6 className="mb-0">Event Statistics</h6>
            </Card.Header>
            <Card.Body>
              <div className="mb-3">
                <h6>By Event Type</h6>
                {Object.entries(
                  events.reduce((acc, event) => {
                    acc[event.event_type] = (acc[event.event_type] || 0) + 1;
                    return acc;
                  }, {}),
                ).map(([type, count]) => (
                  <div
                    key={type}
                    className="d-flex justify-content-between align-items-center mb-2"
                  >
                    <span>{type}</span>
                    <Badge bg={getEventTypeColor(type)}>{count}</Badge>
                  </div>
                ))}
              </div>

              <div className="mb-3">
                <h6>By Severity</h6>
                {Object.entries(
                  events.reduce((acc, event) => {
                    acc[event.severity] = (acc[event.severity] || 0) + 1;
                    return acc;
                  }, {}),
                ).map(([severity, count]) => (
                  <div
                    key={severity}
                    className="d-flex justify-content-between align-items-center mb-2"
                  >
                    <span>{severity}</span>
                    <Badge bg={getSeverityColor(severity)}>{count}</Badge>
                  </div>
                ))}
              </div>

              <div>
                <h6>High Impact Events</h6>
                <small className="text-muted">
                  Events with price change &gt; 10% in either direction
                </small>
                <div className="mt-2">
                  {events
                    .map((event) => ({
                      event,
                      impact: calculateEventImpact(event),
                    }))
                    .filter(
                      ({ impact }) =>
                        impact && Math.abs(impact.priceChange) > 10,
                    )
                    .slice(0, 5)
                    .map(({ event, impact }, index) => (
                      <div key={index} className="mb-2 p-2 border rounded">
                        <small>
                          <strong>{event.event}</strong>
                        </small>
                        <br />
                        <small className="text-muted">
                          {new Date(event.date).toLocaleDateString()}
                        </small>
                        <br />
                        <small
                          className={
                            impact.priceChange >= 0
                              ? "text-success"
                              : "text-danger"
                          }
                        >
                          {impact.priceChange >= 0 ? "↑" : "↓"}{" "}
                          {Math.abs(impact.priceChange).toFixed(2)}%
                        </small>
                      </div>
                    ))}
                </div>
              </div>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default EventHighlight;
