import React, { useState } from 'react';
import { Card, Row, Col, Tabs, List, Button, Empty, Statistic } from 'antd';
import { StarFilled, StarOutlined, PlusOutlined } from '@ant-design/icons';

const { TabPane } = Tabs;

const StockWatchlist = () => {
  const [activeTab, setActiveTab] = useState('1');
  const [watchlist] = useState([
    { id: 1, name: '贵州茅台', code: '600519.SH', price: 1735.60, change: '+2.34%', pe: 38.72 },
    { id: 2, name: '宁德时代', code: '300750.SZ', price: 207.89, change: '+1.87%', pe: 42.15 },
    { id: 3, name: '招商银行', code: '600036.SH', price: 32.21, change: '+0.89%', pe: 6.12 },
    { id: 4, name: '中国平安', code: '601318.SH', price: 45.80, change: '-0.32%', pe: 9.84 }
  ]);

  const [recentlyViewed] = useState([
    { id: 5, name: '比亚迪', code: '002594.SZ', price: 210.12, change: '+1.23%', pe: 34.28 },
    { id: 6, name: '隆基绿能', code: '601012.SH', price: 18.90, change: '+0.75%', pe: 11.23 },
    { id: 7, name: '东方财富', code: '300059.SZ', price: 13.65, change: '-0.21%', pe: 28.65 }
  ]);

  const renderStockItem = (item) => (
    <List.Item
      actions={[
        <Button type="link">详情</Button>,
        item.starred ?
          <StarFilled style={{ color: '#fadb14' }} /> :
          <StarOutlined />
      ]}
    >
      <List.Item.Meta
        title={<span><b>{item.name}</b> ({item.code})</span>}
        description={item.industry || '金融'}
      />
      <div style={{ textAlign: 'right' }}>
        <Statistic
          value={item.price}
          precision={2}
          valueStyle={{
            fontSize: 18,
            fontWeight: 'bold',
            color: item.change.startsWith('+') ? '#cf1322' : item.change.startsWith('-') ? '#389e0d' : '#000'
          }}
          suffix="元"
        />
        <div style={{ marginTop: 4 }}>
          <span style={{
            color: item.change.startsWith('+') ? '#cf1322' : item.change.startsWith('-') ? '#389e0d' : '#595959',
            fontWeight: 'bold'
          }}>
            {item.change}
          </span>
          <span style={{ marginLeft: 8, color: '#8c8c8c' }}>
            市盈率(PE): {item.pe}
          </span>
        </div>
      </div>
    </List.Item>
  );

  return (
    <Card title="我的自选股" bordered={false}>
      <Tabs activeKey={activeTab} onChange={setActiveTab}>
        <TabPane tab="自选股列表" key="1">
          {watchlist.length > 0 ? (
            <List
              itemLayout="horizontal"
              dataSource={watchlist}
              renderItem={renderStockItem}
            />
          ) : (
            <Empty
              description="您还没有添加自选股"
              image={Empty.PRESENTED_IMAGE_SIMPLE}
            >
              <Button type="primary" icon={<PlusOutlined />}>添加自选股</Button>
            </Empty>
          )}
        </TabPane>
        <TabPane tab="最近浏览" key="2">
          <List
            itemLayout="horizontal"
            dataSource={recentlyViewed}
            renderItem={renderStockItem}
          />
        </TabPane>
      </Tabs>
    </Card>
  );
};

export default StockWatchlist;