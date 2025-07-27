import React from 'react';
import { Table, Card, Statistic, Tag } from 'antd';
import { formatCurrency } from '../utils/formatters';

const IndustryRanking = ({ data }) => {
  const columns = [
    {
      title: '排名',
      dataIndex: 'rank',
      key: 'rank',
      width: 80,
      render: (text) => (
        <Tag color={text <= 3 ? '#1890ff' : '#8c8c8c'} style={{ fontSize: 16 }}>
          {text}
        </Tag>
      )
    },
    {
      title: '行业名称',
      dataIndex: 'industry_name',
      key: 'industry_name'
    },
    {
      title: '成交总额',
      dataIndex: 'total_amount',
      key: 'total_amount',
      render: amount => formatCurrency(amount),
      sorter: (a, b) => a.total_amount - b.total_amount
    },
    {
      title: '公司数量',
      dataIndex: 'company_count',
      key: 'company_count',
      align: 'center'
    },
    {
      title: '上涨公司',
      dataIndex: 'up_count',
      key: 'up_count',
      render: count => <Tag color="#52c41a">{count}家</Tag>,
      align: 'center',
      sorter: (a, b) => a.up_count - b.up_count
    },
    {
      title: '下跌公司',
      dataIndex: 'down_count',
      key: 'down_count',
      render: count => <Tag color="#ff4d4f">{count}家</Tag>,
      align: 'center',
      sorter: (a, b) => a.down_count - b.down_count
    },
    {
      title: '涨跌比',
      key: 'ratio',
      render: (_, record) => {
        const ratio = record.up_count / (record.down_count || 1);
        return (
          <div>
            <span>{ratio.toFixed(2)}:1</span>
            <div style={{ marginTop: 4 }}>
              <div style={{
                height: 4,
                background: '#52c41a',
                width: `${ratio * 10}%`,
                maxWidth: '100%'
              }} />
              <div style={{
                height: 4,
                background: '#ff4d4f',
                width: '100%',
                marginTop: 2
              }} />
            </div>
          </div>
        );
      }
    }
  ];

  return (
    <Card title="行业成交额排行榜" bordered={false}>
      <Table
        columns={columns}
        dataSource={data}
        rowKey="industry_id"
        pagination={false}
        scroll={{ x: 'max-content' }}
      />

      {data.length > 0 && (
        <div style={{ marginTop: 24, display: 'flex', justifyContent: 'space-around' }}>
          <Statistic
            title="总成交额"
            value={formatCurrency(data.reduce((sum, item) => sum + item.total_amount, 0))}
          />
          <Statistic
            title="平均成交额"
            value={formatCurrency(data.reduce((sum, item) => sum + item.total_amount, 0) / data.length)}
          />
          <Statistic
            title="总上涨公司"
            value={data.reduce((sum, item) => sum + item.up_count, 0)}
            suffix="家"
          />
          <Statistic
            title="总下跌公司"
            value={data.reduce((sum, item) => sum + item.down_count, 0)}
            suffix="家"
          />
        </div>
      )}
    </Card>
  );
};

export default IndustryRanking;