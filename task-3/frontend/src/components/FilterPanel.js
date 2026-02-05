import React from 'react';
import { Form, Row, Col, Button } from 'react-bootstrap';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';

const FilterPanel = ({ filters, onFilterChange, eventTypes, severities }) => {
  const handleInputChange = (field, value) => {
    const newFilters = { ...filters, [field]: value };
    onFilterChange(newFilters);
  };

  const resetFilters = () => {
    onFilterChange({
      startDate: '1987-05-20',
      endDate: '2022-11-14',
      eventType: 'all',
      severity: 'all'
    });
  };

  return (
    <div className="filter-panel">
      <h5 className="mb-3">Data Filters</h5>
      <Form>
        <Row>
          <Col md={3}>
            <Form.Group className="mb-3">
              <Form.Label>Start Date</Form.Label>
              <DatePicker
                selected={new Date(filters.startDate)}
                onChange={(date) => handleInputChange('startDate', date.toISOString().split('T')[0])}
                selectsStart
                startDate={new Date(filters.startDate)}
                endDate={new Date(filters.endDate)}
                className="form-control"
                dateFormat="yyyy-MM-dd"
              />
            </Form.Group>
          </Col>
          <Col md={3}>
            <Form.Group className="mb-3">
              <Form.Label>End Date</Form.Label>
              <DatePicker
                selected={new Date(filters.endDate)}
                onChange={(date) => handleInputChange('endDate', date.toISOString().split('T')[0])}
                selectsEnd
                startDate={new Date(filters.startDate)}
                endDate={new Date(filters.endDate)}
                minDate={new Date(filters.startDate)}
                className="form-control"
                dateFormat="yyyy-MM-dd"
              />
            </Form.Group>
          </Col>
          <Col md={3}>
            <Form.Group className="mb-3">
              <Form.Label>Event Type</Form.Label>
              <Form.Select
                value={filters.eventType}
                onChange={(e) => handleInputChange('eventType', e.target.value)}
              >
                <option value="all">All Types</option>
                {eventTypes.map(type => (
                  <option key={type} value={type}>{type}</option>
                ))}
              </Form.Select>
            </Form.Group>
          </Col>
          <Col md={3}>
            <Form.Group className="mb-3">
              <Form.Label>Severity</Form.Label>
              <Form.Select
                value={filters.severity}
                onChange={(e) => handleInputChange('severity', e.target.value)}
              >
                <option value="all">All Severities</option>
                {severities.map(severity => (
                  <option key={severity} value={severity}>{severity}</option>
                ))}
              </Form.Select>
            </Form.Group>
          </Col>
        </Row>
        <Row>
          <Col className="text-end">
            <Button variant="secondary" onClick={resetFilters} className="me-2">
              Reset Filters
            </Button>
            <Button variant="primary">
              Apply Filters
            </Button>
          </Col>
        </Row>
      </Form>
    </div>
  );
};

export default FilterPanel;
