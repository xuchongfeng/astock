import React from 'react';
import { Card, Statistic } from 'antd';

const IndustryStatsCard = ({ title, value, suffix, icon, color }) => {
  return (
    <Card
      bordered={false}
      bodyStyle={{
        padding: 16,
        background: `linear-gradient(135deg, ${color}10, ${color}05)`,
        borderLeft: `4px solid ${color}`,
        borderRadius: 4
      }}
    >
      <Statistic
        title={title}
        value={value}
        suffix={suffix}
        valueStyle={{
          color: color,
          fontSize: 24,
          fontWeight: 'bold'
        }}
        prefix={icon}
      />
    </Card>
  );
};

export default IndustryStatsCard;