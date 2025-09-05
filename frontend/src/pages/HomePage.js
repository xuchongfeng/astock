import React from 'react';
import { 
  Row, 
  Col, 
  Card, 
  Statistic, 
  Table, 
  Tag, 
  List, 
  Button,
  Space,
  Divider,
  Typography,
  Badge
} from 'antd';
import { 
  RiseOutlined, 
  FallOutlined, 
  LineChartOutlined,
  FireOutlined,
  TrophyOutlined,
  EyeOutlined,
  StarOutlined,
  ArrowUpOutlined,
  GlobalOutlined,
  ClockCircleOutlined
} from '@ant-design/icons';
import IndexKLineChart from '../components/IndexKLineChart';
import DeepSeekMarketAnalysis from '../components/DeepSeekMarketAnalysis';

const { Title, Text, Paragraph } = Typography;

const HomePage = () => {
  // Mock数据 - 大盘基本信息
  const marketOverview = {
    shanghai: {
      name: '上证指数',
      code: '000001.SH',
      current: 3156.67,
      change: 28.45,
      changePercent: 0.91,
      volume: 2456.78,
      turnover: 289.45
    },
    shenzhen: {
      name: '深证成指',
      code: '399001.SZ',
      current: 10234.56,
      change: -45.67,
      changePercent: -0.44,
      volume: 1987.34,
      turnover: 234.67
    },
    chuangye: {
      name: '创业板指',
      code: '399006.SZ',
      current: 2156.78,
      change: 12.34,
      changePercent: 0.58,
      volume: 567.89,
      turnover: 89.45
    }
  };

  // Mock数据 - 热门板块
  const hotSectors = [
    {
      name: '人工智能',
      code: 'BK0800',
      changePercent: 3.45,
      volume: 156.78,
      turnover: 89.45,
      leadingStock: '科大讯飞',
      leadingStockChange: 5.67,
      hotRank: 1
    },
    {
      name: '新能源车',
      code: 'BK0493',
      changePercent: 2.89,
      volume: 234.56,
      turnover: 123.45,
      leadingStock: '比亚迪',
      leadingStockChange: 4.23,
      hotRank: 2
    },
    {
      name: '半导体',
      code: 'BK0447',
      changePercent: 2.34,
      volume: 189.67,
      turnover: 98.76,
      leadingStock: '中芯国际',
      leadingStockChange: 3.89,
      hotRank: 3
    }
  ];

  // Mock数据 - 热点新闻
  const hotNews = [
    {
      id: 1,
      title: '央行宣布降准0.25个百分点，释放长期资金约5000亿元',
      source: '中国人民银行',
      publishTime: '2024-01-15 09:00:00',
      hotLevel: 5,
      category: '政策',
      readCount: 125680
    },
    {
      id: 2,
      title: '新能源汽车销量再创新高，全年突破900万辆',
      source: '中国汽车工业协会',
      publishTime: '2024-01-15 08:30:00',
      hotLevel: 4,
      category: '行业',
      readCount: 98765
    },
    {
      id: 3,
      title: 'A股三大指数集体上涨，北向资金净流入超100亿元',
      source: '证券时报',
      publishTime: '2024-01-15 08:00:00',
      hotLevel: 4,
      category: '市场',
      readCount: 87654
    }
  ];

  // Mock数据 - 热门个股
  const hotStocks = [
    {
      ts_code: '000001.SZ',
      name: '平安银行',
      current: 12.45,
      changePercent: 5.69,
      volume: 234.56,
      turnover: 28.67,
      market_cap: 2156.78,
      pe: 8.45,
      industry: '银行',
      hotRank: 1,
      reason: '业绩超预期，机构看好'
    },
    {
      ts_code: '000002.SZ',
      name: '万科A',
      current: 18.67,
      changePercent: 5.01,
      volume: 189.34,
      turnover: 35.23,
      market_cap: 1890.45,
      pe: 12.34,
      industry: '房地产',
      hotRank: 2,
      reason: '政策利好，估值修复'
    },
    {
      ts_code: '600036.SH',
      name: '招商银行',
      current: 34.56,
      changePercent: 3.69,
      volume: 156.78,
      turnover: 54.12,
      market_cap: 3456.78,
      pe: 9.87,
      industry: '银行',
      hotRank: 3,
      reason: '零售业务强劲，资产质量优良'
    }
  ];

  // 获取涨跌颜色
  const getChangeColor = (change, percent) => {
    if (change > 0 || percent > 0) return '#f5222d';
    if (change < 0 || percent < 0) return '#52c41a';
    return '#666';
  };

  // 获取涨跌图标
  const getChangeIcon = (change, percent) => {
    if (change > 0 || percent > 0) return <RiseOutlined style={{ color: '#f5222d' }} />;
    if (change < 0 || percent < 0) return <FallOutlined style={{ color: '#52c41a' }} />;
    return null;
  };

  // 获取热度等级标签
  const getHotLevelTag = (level) => {
    const colors = ['', 'blue', 'green', 'orange', 'red', 'volcano'];
    const texts = ['', '一般', '较热', '热门', '很热', '爆热'];
    return <Tag color={colors[level]} icon={<FireOutlined />}>{texts[level]}</Tag>;
  };

  // 热门板块表格列
  const sectorColumns = [
    {
      title: '排名',
      dataIndex: 'hotRank',
      key: 'hotRank',
      width: 60,
      render: (rank) => (
        <Badge count={rank} style={{ backgroundColor: rank <= 3 ? '#f5222d' : '#1890ff' }} />
      )
    },
    {
      title: '板块名称',
      dataIndex: 'name',
      key: 'name',
      width: 120,
      render: (name, record) => (
        <div>
          <div style={{ fontWeight: 'bold' }}>{name}</div>
          <div style={{ fontSize: '12px', color: '#666' }}>{record.code}</div>
        </div>
      )
    },
    {
      title: '涨跌幅',
      dataIndex: 'changePercent',
      key: 'changePercent',
      width: 100,
      align: 'right',
      render: (value) => (
        <span style={{ 
          color: getChangeColor(0, value), 
          fontWeight: 'bold',
          fontSize: '16px'
        }}>
          {value > 0 ? '+' : ''}{value}%
        </span>
      )
    },
    {
      title: '成交量(亿)',
      dataIndex: 'volume',
      key: 'volume',
      width: 120,
      align: 'right',
      render: (value) => value.toFixed(2)
    },
    {
      title: '成交额(亿)',
      dataIndex: 'turnover',
      key: 'turnover',
      width: 120,
      align: 'right',
      render: (value) => value.toFixed(2)
    },
    {
      title: '领涨股',
      dataIndex: 'leadingStock',
      key: 'leadingStock',
      width: 150,
      render: (name, record) => (
        <div>
          <div style={{ fontWeight: 'bold' }}>{name}</div>
          <div style={{ fontSize: '12px', color: getChangeColor(0, record.leadingStockChange) }}>
            {record.leadingStockChange > 0 ? '+' : ''}{record.leadingStockChange}%
          </div>
        </div>
      )
    }
  ];

  // 热门个股表格列
  const stockColumns = [
    {
      title: '排名',
      dataIndex: 'hotRank',
      key: 'hotRank',
      width: 60,
      render: (rank) => (
        <Badge count={rank} style={{ backgroundColor: rank <= 3 ? '#f5222d' : '#1890ff' }} />
      )
    },
    {
      title: '股票代码',
      dataIndex: 'ts_code',
      key: 'ts_code',
      width: 120,
      render: (code) => <Tag color="blue">{code}</Tag>
    },
    {
      title: '股票名称',
      dataIndex: 'name',
      key: 'name',
      width: 120,
      render: (name, record) => (
        <div>
          <div style={{ fontWeight: 'bold' }}>{name}</div>
          <div style={{ fontSize: '12px', color: '#666' }}>{record.industry}</div>
        </div>
      )
    },
    {
      title: '最新价',
      dataIndex: 'current',
      key: 'current',
      width: 100,
      align: 'right',
      render: (value) => (
        <span style={{ fontWeight: 'bold', fontSize: '16px' }}>
          {typeof value === 'string' ? value : value.toFixed(2)}
        </span>
      )
    },
    {
      title: '涨跌幅',
      dataIndex: 'changePercent',
      key: 'changePercent',
      width: 100,
      align: 'right',
      render: (value) => (
        <span style={{ 
          color: getChangeColor(0, value), 
          fontWeight: 'bold',
          fontSize: '14px'
        }}>
          {value > 0 ? '+' : ''}{value}%
        </span>
      )
    },
    {
      title: '成交量(万手)',
      dataIndex: 'volume',
      key: 'volume',
      width: 120,
      align: 'right',
      render: (value) => value.toFixed(0)
    },
    {
      title: '成交额(亿)',
      dataIndex: 'turnover',
      key: 'turnover',
      width: 120,
      align: 'right',
      render: (value) => value.toFixed(2)
    },
    {
      title: '市值(亿)',
      dataIndex: 'market_cap',
      key: 'market_cap',
      width: 120,
      align: 'right',
      render: (value) => value.toFixed(2)
    },
    {
      title: '市盈率',
      dataIndex: 'pe',
      key: 'pe',
      width: 100,
      align: 'right',
      render: (value) => value.toFixed(2)
    },
    {
      title: '上涨原因',
      dataIndex: 'reason',
      key: 'reason',
      width: 200,
      render: (reason) => (
        <Tag color="orange" icon={<ArrowUpOutlined />}>
          {reason}
        </Tag>
      )
    }
  ];

  return (
    <div style={{ padding: '24px', background: '#f5f7fa', minHeight: '100vh' }}>
      {/* 页面标题 */}
      <div style={{ marginBottom: '24px', textAlign: 'center' }}>
        <Title level={2} style={{ margin: 0, color: '#1890ff' }}>
          <GlobalOutlined style={{ marginRight: '12px' }} />
          市场概况
        </Title>
        <Text type="secondary">
          <ClockCircleOutlined style={{ marginRight: '8px' }} />
          数据更新时间：{new Date().toLocaleString('zh-CN')}
        </Text>
      </div>

      {/* 大盘基本信息 - 包含K线图 */}
      <Row gutter={[16, 16]} style={{ marginBottom: '24px' }}>
        <Col xs={24} lg={8}>
          <IndexKLineChart 
            indexData={marketOverview.shanghai}
            height={400}
          />
        </Col>
        <Col xs={24} lg={8}>
          <IndexKLineChart 
            indexData={marketOverview.shenzhen}
            height={400}
          />
        </Col>
        <Col xs={24} lg={8}>
          <IndexKLineChart 
            indexData={marketOverview.chuangye}
            height={400}
          />
        </Col>
      </Row>

      {/* 热门板块和热点新闻 */}
      <Row gutter={[16, 16]} style={{ marginBottom: '24px' }}>
        <Col xs={24} lg={16}>
          <Card 
            title={
              <Space>
                <TrophyOutlined style={{ color: '#faad14' }} />
                热门板块
              </Space>
            }
            extra={
              <Button type="link" size="small">
                查看更多 <EyeOutlined />
              </Button>
            }
            bordered={false}
          >
            <Table
              columns={sectorColumns}
              dataSource={hotSectors}
              pagination={false}
              size="small"
              rowKey="code"
              scroll={{ x: 800 }}
            />
          </Card>
        </Col>

        <Col xs={24} lg={8}>
          <Card 
            title={
              <Space>
                <FireOutlined style={{ color: '#f5222d' }} />
                热点新闻
              </Space>
            }
            extra={
              <Button type="link" size="small">
                更多 <EyeOutlined />
              </Button>
            }
            bordered={false}
            style={{ height: '100%' }}
          >
            <List
              size="small"
              dataSource={hotNews}
              renderItem={(item, index) => (
                <List.Item
                  key={item.id}
                  style={{ 
                    padding: '12px 0',
                    borderBottom: index < hotNews.length - 1 ? '1px solid #f0f0f0' : 'none'
                  }}
                >
                  <List.Item.Meta
                    avatar={
                      <Badge count={index + 1} style={{ 
                        backgroundColor: index < 3 ? '#f5222d' : '#1890ff' 
                      }} />
                    }
                    title={
                      <div style={{ marginBottom: '8px' }}>
                        <Space>
                          {getHotLevelTag(item.hotLevel)}
                          <Tag color="blue" size="small">{item.category}</Tag>
                        </Space>
                      </div>
                    }
                    description={
                      <div>
                        <Paragraph 
                          ellipsis={{ rows: 2, tooltip: item.title }}
                          style={{ margin: 0, fontSize: '14px', lineHeight: '1.4' }}
                        >
                          {item.title}
                        </Paragraph>
                        <div style={{ marginTop: '8px', fontSize: '12px', color: '#666' }}>
                          <Space split={<Divider type="vertical" />}>
                            <span>{item.source}</span>
                            <span>{item.publishTime}</span>
                            <span>阅读 {item.readCount.toLocaleString()}</span>
                          </Space>
                        </div>
                      </div>
                    }
                  />
                </List.Item>
              )}
            />
          </Card>
        </Col>
      </Row>

      {/* DeepSeek AI市场分析 */}
      <Row gutter={[16, 16]} style={{ marginBottom: '24px' }}>
        <Col xs={24}>
          <DeepSeekMarketAnalysis height={500} />
        </Col>
      </Row>

      {/* 热门个股 */}
      <Card 
        title={
          <Space>
            <StarOutlined style={{ color: '#faad14' }} />
            热门个股
          </Space>
        }
        extra={
          <Button type="link" size="small">
            查看更多 <EyeOutlined />
          </Button>
        }
        bordered={false}
      >
        <Table
          columns={stockColumns}
          dataSource={hotStocks}
          pagination={false}
          size="small"
          rowKey="ts_code"
          scroll={{ x: 1200 }}
        />
      </Card>
    </div>
  );
};

export default HomePage;