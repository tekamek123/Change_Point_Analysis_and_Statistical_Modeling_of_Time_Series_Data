import React from 'react';
import { Card } from 'react-bootstrap';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const VolatilityAnalysis = ({ volatilityData, prices }) => {
  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="tooltip-custom">
          <p><strong>Date:</strong> {label}</p>
          <p><strong>Volatility:</strong> {payload[0].value.toFixed(6)}</p>
        </div>
      );
    }
    return null;
  };

  return (
    <Card className="volatility-chart">
      <Card.Header>
        <h5 className="mb-0">Volatility Analysis</h5>
      </Card.Header>
      <Card.Body>
        {volatilityData.volatility_data && (
          <div>
            <h6>Rolling Volatility (30-day window)</h6>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={volatilityData.volatility_data.window_30 || []}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis 
                  dataKey="date"
                  tick={{ fontSize: 12 }}
                  tickFormatter={(value) => new Date(value).toLocaleDateString()}
                />
                <YAxis 
                  tick={{ fontSize: 12 }}
                  tickFormatter={(value) => value.toFixed(4)}
                />
                <Tooltip content={<CustomTooltip />} />
                <Line
                  type="monotone"
                  dataKey="volatility"
                  stroke="#dc2626"
                  strokeWidth={2}
                  dot={false}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        )}
      </Card.Body>
    </Card>
  );
};

export default VolatilityAnalysis;
