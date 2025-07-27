import React from 'react';
import { Table, Tag } from 'antd';
import { formatDate, formatCurrency, formatPercent } from '../utils/formatters';
import KLineChart from './KLineChart';

const StockDailyTable = ({ data, loading, pagination, onChange }) => {
  const columns = [
    {
      title: '交易日期',
      dataIndex: 'trade_date',
      key: 'trade_date',
      sorter: true,
      render: date => formatDate(date, 'YYYY-MM-DD'),
      width: 120
    },
    {
      title: '开盘价',
      dataIndex: 'open',
      key: 'open',
      render: value => formatCurrency(value),
      align: 'right',
      width: 100
    },
    {
      title: '收盘价',
      dataIndex: 'close',
      key: 'close',
      render: value => formatCurrency(value),
      align: 'right',
      width: 100
    },
    {
      title: '最高价',
      dataIndex: 'high',
      key: 'high',
      render: value => formatCurrency(value),
      align: 'right',
      width: 100
    },
    {
      title: '最低价',
      dataIndex: 'low',
      key: 'low',
      render: value => formatCurrency(value),
      align: 'right',
      width: 100
    },
    {
      title: '涨跌幅',
      dataIndex: 'pct_chg',
      key: 'pct_chg',
      render: value => {
        const isPositive = value > 0;
        return (
          <Tag color={isPositive ? '#cf1322' : '#389e0d'}>
            {isPositive ? '+' : ''}{formatPercent(value)}
          </Tag>
        );
      },
      align: 'center',
      width: 100
    },
    {
      title: '成交量(手)',
      dataIndex: 'vol',
      key: 'vol',
      render: value => value ? (value / 100).toFixed(2) + '万' : '-',
      align: 'right',
      width: 120
    },
    {
      title: '成交额(元)',
      dataIndex: 'amount',
      key: 'amount',
      render: value => value ? formatCurrency(value) : '-',
      align: 'right',
      width: 120
    },
    {
      title: '换手率',
      dataIndex: 'turnover_rate',
      key: 'turnover_rate',
      render: value => value ? formatPercent(value) : '-',
      align: 'right',
      width: 100
    }
  ];

  return (
    <Table
      columns={columns}
      dataSource={data}
      rowKey={record => (record.ts_code ? `${record.ts_code}-${record.trade_date}` : record.id || record.trade_date)}
      loading={loading}
      pagination={pagination}
      onChange={onChange}
      scroll={{ x: 'max-content' }}
      size="middle"
      bordered
      expandable={{
        expandedRowRender: record => record.ts_code ? <KLineChart tsCode={record.ts_code} /> : null,
        rowExpandable: record => !!record.ts_code,
      }}
    />
  );
};

export default StockDailyTable;