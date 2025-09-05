import React, { useState, useEffect } from 'react';
import { Card, Row, Col, Statistic, Table, Tag, Typography, Select, Input, Space, Progress } from 'antd';
import { 
  RiseOutlined, 
  FallOutlined, 
  BarChartOutlined,
  StockOutlined,
  DatabaseOutlined,
  LineChartOutlined
} from '@ant-design/icons';

const { Title, Text } = Typography;
const { Option } = Select;
const { Search } = Input;

// 简单的饼图组件
const SimplePieChart = ({ data, title, size = 120 }) => {
  const total = data.reduce((sum, item) => sum + item.value, 0);
  let currentAngle = 0;
  
  const colors = ['#1890ff', '#52c41a', '#faad14', '#f5222d', '#722ed1', '#13c2c2', '#eb2f96', '#fa8c16', '#a0d911', '#2f54eb'];

  return (
    <div style={{ textAlign: 'center' }}>
      <Text strong style={{ fontSize: '12px', marginBottom: '8px', display: 'block' }}>{title}</Text>
      <div style={{ position: 'relative', width: size, height: size, margin: '0 auto' }}>
        <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
          {data.map((item, index) => {
            const percentage = item.value / total;
            const startAngle = currentAngle;
            const endAngle = currentAngle + percentage * 2 * Math.PI;
            
            const x1 = size / 2 + (size / 2 - 10) * Math.cos(startAngle);
            const y1 = size / 2 + (size / 2 - 10) * Math.sin(startAngle);
            const x2 = size / 2 + (size / 2 - 10) * Math.cos(endAngle);
            const y2 = size / 2 + (size / 2 - 10) * Math.sin(endAngle);
            
            const largeArcFlag = percentage > 0.5 ? 1 : 0;
            
            const pathData = [
              `M ${size / 2} ${size / 2}`,
              `L ${x1} ${y1}`,
              `A ${size / 2 - 10} ${size / 2 - 10} 0 ${largeArcFlag} 1 ${x2} ${y2}`,
              'Z'
            ].join(' ');
            
            currentAngle = endAngle;
            
            return (
              <path
                key={index}
                d={pathData}
                fill={colors[index % colors.length]}
                stroke="#fff"
                strokeWidth="1"
              />
            );
          })}
        </svg>
        <div style={{
          position: 'absolute',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          fontSize: '12px',
          fontWeight: 'bold',
          color: '#666'
        }}>
          {total.toFixed(1)}%
        </div>
      </div>
      <div style={{ marginTop: '8px', fontSize: '10px' }}>
        {data.map((item, index) => (
          <div key={index} style={{ marginBottom: '2px' }}>
            <span style={{
              display: 'inline-block',
              width: '8px',
              height: '8px',
              backgroundColor: colors[index % colors.length],
              marginRight: '4px',
              borderRadius: '2px'
            }}></span>
            {item.name}: {item.value.toFixed(1)}%
          </div>
        ))}
      </div>
    </div>
  );
};

// 简单的K线图组件
const SimpleKLineChart = ({ stockCode }) => {
  // 模拟K线数据
  const mockKLineData = [
    { date: '2024-01-08', open: 12.50, high: 12.80, low: 12.45, close: 12.75, volume: 125680 },
    { date: '2024-01-09', open: 12.75, high: 12.90, low: 12.60, close: 12.85, volume: 118920 },
    { date: '2024-01-10', open: 12.85, high: 13.00, low: 12.70, close: 12.95, volume: 132450 },
    { date: '2024-01-11', open: 12.95, high: 13.10, low: 12.80, close: 13.05, volume: 145680 },
    { date: '2024-01-12', open: 13.05, high: 13.20, low: 12.90, close: 13.15, volume: 156890 },
    { date: '2024-01-15', open: 13.15, high: 13.25, low: 12.95, close: 12.85, volume: 142340 },
    { date: '2024-01-16', open: 12.85, high: 13.00, low: 12.70, close: 12.90, volume: 138760 },
    { date: '2024-01-17', open: 12.90, high: 13.05, low: 12.75, close: 12.85, volume: 125680 }
  ];

  const renderKLine = (data) => {
    const maxPrice = Math.max(...data.map(d => d.high));
    const minPrice = Math.min(...data.map(d => d.low));
    const priceRange = maxPrice - minPrice;
    const chartHeight = 200;
    const chartWidth = 600;
    const barWidth = Math.max(20, (chartWidth - 40) / data.length);
    const padding = 20;

    return (
      <div style={{ 
        width: chartWidth, 
        height: chartHeight + 40, 
        border: '1px solid #e8e8e8',
        padding: `${padding}px`,
        backgroundColor: '#fafafa',
        position: 'relative'
      }}>
        {/* 价格刻度 */}
        <div style={{ 
          position: 'absolute', 
          left: padding, 
          top: padding, 
          height: chartHeight,
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'space-between',
          fontSize: '10px',
          color: '#666',
          width: '40px'
        }}>
          <span>{maxPrice.toFixed(2)}</span>
          <span>{((maxPrice + minPrice) / 2).toFixed(2)}</span>
          <span>{minPrice.toFixed(2)}</span>
        </div>

        {/* K线图主体 */}
        <svg 
          width={chartWidth - 60} 
          height={chartHeight} 
          style={{ 
            marginLeft: '50px',
            marginTop: '0px'
          }}
        >
          {/* 网格线 */}
          <defs>
            <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">
              <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#f0f0f0" strokeWidth="0.5"/>
            </pattern>
          </defs>
          <rect width="100%" height="100%" fill="url(#grid)" />

          {data.map((item, index) => {
            const x = index * barWidth + barWidth / 2;
            const openY = ((maxPrice - item.open) / priceRange) * chartHeight;
            const closeY = ((maxPrice - item.close) / priceRange) * chartHeight;
            const highY = ((maxPrice - item.high) / priceRange) * chartHeight;
            const lowY = ((maxPrice - item.low) / priceRange) * chartHeight;
            
            const isGreen = item.close >= item.open;
            const color = isGreen ? '#52c41a' : '#ff4d4f';
            const bodyWidth = Math.max(2, barWidth * 0.6);
            
            return (
              <g key={index}>
                {/* 影线（最高价到最低价） */}
                <line
                  x1={x}
                  y1={highY}
                  x2={x}
                  y2={lowY}
                  stroke={color}
                  strokeWidth="1"
                />
                {/* K线实体（开盘价到收盘价） */}
                <rect
                  x={x - bodyWidth / 2}
                  y={Math.min(openY, closeY)}
                  width={bodyWidth}
                  height={Math.max(1, Math.abs(closeY - openY))}
                  fill={color}
                  stroke={color}
                  strokeWidth="0.5"
                />
              </g>
            );
          })}
        </svg>

        {/* 日期标签 */}
        <div style={{
          display: 'flex',
          justifyContent: 'space-between',
          marginTop: '10px',
          marginLeft: '50px',
          marginRight: '20px'
        }}>
          {data.map((item, index) => (
            <div key={index} style={{
              fontSize: '10px',
              color: '#666',
              textAlign: 'center',
              width: barWidth
            }}>
              {item.date.slice(5)}
            </div>
          ))}
        </div>
      </div>
    );
  };

  return (
    <div>
      <div style={{ marginBottom: '16px' }}>
        <Text strong>K线图 ({stockCode})</Text>
      </div>
      {renderKLine(mockKLineData)}
    </div>
  );
};

const StockAnalysisPage = () => {
  const [loading, setLoading] = useState(false);
  const [selectedStock, setSelectedStock] = useState('000001');
  const [stockData, setStockData] = useState(null);

  // 模拟股票数据
  const mockStockData = {
    code: '000001',
    name: '平安银行',
    currentPrice: 12.85,
    change: 0.23,
    changePercent: 1.82,
    volume: 125680000,
    turnover: 161.2,
    marketCap: 2489.6,
    pe: 8.5,
    pb: 0.8,
    dividend: 0.35,
    dividendYield: 2.72,
    industry: '银行',
    sector: '金融',
    riskLevel: '低风险',
    technicalScore: 78,
    fundamentalScore: 85,
    overallScore: 82
  };

  // 模拟持股比例数据
  const mockHoldingData = {
    // 流通股结构
    circulation: [
      { name: '流通A股', value: 65.2 },
      { name: '限售股', value: 34.8 }
    ],
    // 十大股东持股
    topHolders: [
      { name: '平安集团', value: 42.1 },
      { name: '汇丰银行', value: 18.5 },
      { name: '社保基金', value: 8.2 },
      { name: '其他机构', value: 31.2 }
    ],
    // 基金持有情况
    fundHolding: [
      { name: '公募基金', value: 15.8 },
      { name: '私募基金', value: 8.3 },
      { name: '保险资金', value: 12.1 },
      { name: '其他资金', value: 63.8 }
    ],
    // 解禁股信息
    unlockInfo: [
      { name: '已解禁', value: 78.5 },
      { name: '待解禁', value: 21.5 }
    ]
  };

  // 模拟财务指标数据
  const financialData = [
    { year: '2023', revenue: 1647.8, netProfit: 455.2, growth: 12.5, roe: 12.8 },
    { year: '2022', revenue: 1464.2, netProfit: 404.6, growth: 8.9, roe: 11.9 },
    { year: '2021', revenue: 1344.8, netProfit: 371.5, growth: 6.2, roe: 10.8 },
    { year: '2020', revenue: 1266.9, netProfit: 349.8, growth: 3.1, roe: 9.9 },
    { year: '2019', revenue: 1229.1, netProfit: 339.2, growth: 1.8, roe: 9.2 }
  ];

  // 模拟技术指标数据
  const technicalData = [
    { indicator: 'RSI', value: 65, status: '中性', color: 'orange' },
    { indicator: 'MACD', value: 0.15, status: '金叉', color: 'green' },
    { indicator: 'KDJ', value: 72, status: '超买', color: 'red' },
    { indicator: 'BOLL', value: '中轨', status: '正常', color: 'blue' },
    { indicator: 'MA', value: '5日均线', status: '支撑', color: 'green' }
  ];

  useEffect(() => {
    // 模拟数据加载
    setLoading(true);
    setTimeout(() => {
      setStockData(mockStockData);
      setLoading(false);
    }, 1000);
  }, [selectedStock]);

  const columns = [
    {
      title: '年份',
      dataIndex: 'year',
      key: 'year',
      width: 60,
    },
    {
      title: '营收(亿)',
      dataIndex: 'revenue',
      key: 'revenue',
      width: 80,
      render: (value) => value.toFixed(1),
    },
    {
      title: '净利(亿)',
      dataIndex: 'netProfit',
      key: 'netProfit',
      width: 80,
      render: (value) => value.toFixed(1),
    },
    {
      title: '增长(%)',
      dataIndex: 'growth',
      key: 'growth',
      width: 70,
      render: (value) => (
        <span style={{ color: value > 0 ? '#52c41a' : '#ff4d4f' }}>
          {value > 0 ? '+' : ''}{value}%
        </span>
      ),
    },
    {
      title: 'ROE(%)',
      dataIndex: 'roe',
      key: 'roe',
      width: 70,
      render: (value) => `${value}%`,
    },
  ];

  const technicalColumns = [
    {
      title: '指标',
      dataIndex: 'indicator',
      key: 'indicator',
      width: 60,
    },
    {
      title: '数值',
      dataIndex: 'value',
      key: 'value',
      width: 80,
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      width: 80,
      render: (status, record) => (
        <Tag color={record.color} size="small">{status}</Tag>
      ),
    },
  ];

  const getRiskColor = (level) => {
    const colorMap = {
      '低风险': 'green',
      '中风险': 'orange',
      '高风险': 'red'
    };
    return colorMap[level] || 'default';
  };

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '50px' }}>
        <div>正在加载个股分析数据...</div>
      </div>
    );
  }

  return (
    <div style={{ padding: '16px' }}>
      <Card
        title={
          <Space>
            <DatabaseOutlined style={{ color: '#1890ff' }} />
            <Title level={4} style={{ margin: 0 }}>个股分析 - {stockData?.name}</Title>
          </Space>
        }
        extra={
          <Space>
            <Select
              defaultValue="000001"
              style={{ width: 120 }}
              onChange={setSelectedStock}
              size="small"
            >
              <Option value="000001">平安银行</Option>
              <Option value="000002">万科A</Option>
              <Option value="000858">五粮液</Option>
              <Option value="000725">京东方A</Option>
            </Select>
            <Search
              placeholder="输入股票代码或名称"
              style={{ width: 180 }}
              onSearch={(value) => console.log('搜索:', value)}
              size="small"
            />
          </Space>
        }
        size="small"
      >
        {stockData && (
          <>
            {/* 股票概览 - 紧凑布局 + 基本介绍 */}
            <Card size="small" title="股票概览" style={{ marginBottom: '16px' }}>
              <Row gutter={16}>
                {/* 左侧：紧凑的股票概览 */}
                <Col span={12}>
                  <div style={{ 
                    padding: '16px', 
                    backgroundColor: '#f8f9fa', 
                    borderRadius: '8px',
                    border: '1px solid #e8e8e8'
                  }}>
                    <div style={{ textAlign: 'center', marginBottom: '16px' }}>
                      <Title level={5} style={{ margin: '0 0 8px 0' }}>
                        {stockData.name} ({stockData.code})
                      </Title>
                      <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#1890ff' }}>
                        ¥{stockData.currentPrice}
                      </div>
                      <div style={{ 
                        fontSize: '14px', 
                        color: stockData.change > 0 ? '#52c41a' : '#ff4d4f',
                        marginTop: '6px'
                      }}>
                        {stockData.change > 0 ? '+' : ''}{stockData.change} ({stockData.changePercent}%)
                        {stockData.change > 0 ? <RiseOutlined /> : <FallOutlined />}
                      </div>
                    </div>
                    
                    <Row gutter={12}>
                      <Col span={8}>
                        <Statistic title="成交量" value={stockData.volume} suffix="手" size="small" />
                      </Col>
                      <Col span={8}>
                        <Statistic title="成交额" value={stockData.turnover} suffix="亿" size="small" />
                      </Col>
                      <Col span={8}>
                        <Statistic title="市值" value={stockData.marketCap} suffix="亿" size="small" />
                      </Col>
                    </Row>
                    <Row gutter={12} style={{ marginTop: '12px' }}>
                      <Col span={8}>
                        <Statistic title="PE" value={stockData.pe} size="small" />
                      </Col>
                      <Col span={8}>
                        <Statistic title="PB" value={stockData.pb} size="small" />
                      </Col>
                      <Col span={8}>
                        <Statistic title="股息率" value={stockData.dividendYield} suffix="%" size="small" />
                      </Col>
                    </Row>
                    <Row gutter={12} style={{ marginTop: '12px' }}>
                      <Col span={8}>
                        <div style={{ textAlign: 'center' }}>
                          <Text strong style={{ fontSize: '11px' }}>行业</Text><br />
                          <Tag color="blue" size="small">{stockData.industry}</Tag>
                        </div>
                      </Col>
                      <Col span={8}>
                        <div style={{ textAlign: 'center' }}>
                          <Text strong style={{ fontSize: '11px' }}>板块</Text><br />
                          <Tag color="green" size="small">{stockData.sector}</Tag>
                        </div>
                      </Col>
                      <Col span={8}>
                        <div style={{ textAlign: 'center' }}>
                          <Text strong style={{ fontSize: '11px' }}>风险等级</Text><br />
                          <Tag color={getRiskColor(stockData.riskLevel)} size="small">{stockData.riskLevel}</Tag>
                        </div>
                      </Col>
                    </Row>
                    <Row gutter={12} style={{ marginTop: '12px' }}>
                      <Col span={8}>
                        <div style={{ textAlign: 'center' }}>
                          <Text strong style={{ fontSize: '11px' }}>每股分红</Text><br />
                          <Text style={{ fontSize: '11px' }}>¥{stockData.dividend}</Text>
                        </div>
                      </Col>
                      <Col span={8}>
                        <div style={{ textAlign: 'center' }}>
                          <Text strong style={{ fontSize: '11px' }}>投资建议</Text><br />
                          <Tag color="green" size="small">买入</Tag>
                        </div>
                      </Col>
                      <Col span={8}>
                        <div style={{ textAlign: 'center' }}>
                          <Text strong style={{ fontSize: '11px' }}>综合评分</Text><br />
                          <Text style={{ fontSize: '14px', fontWeight: 'bold', color: '#1890ff' }}>{stockData.overallScore}分</Text>
                        </div>
                      </Col>
                    </Row>
                  </div>
                </Col>
                
                {/* 右侧：股票基本介绍 */}
                <Col span={12}>
                  <div style={{ 
                    padding: '16px', 
                    backgroundColor: '#f8f9fa', 
                    borderRadius: '8px',
                    border: '1px solid #e8e8e8',
                    height: '100%'
                  }}>
                    <Title level={5} style={{ margin: '0 0 16px 0', color: '#333' }}>公司基本信息</Title>
                    
                    <div style={{ marginBottom: '16px' }}>
                      <Text strong style={{ fontSize: '13px', color: '#333' }}>公司介绍：</Text>
                      <div style={{ 
                        marginTop: '8px', 
                        fontSize: '12px', 
                        color: '#666', 
                        lineHeight: '1.6',
                        backgroundColor: '#fff',
                        padding: '12px',
                        borderRadius: '4px',
                        border: '1px solid #f0f0f0'
                      }}>
                        平安银行股份有限公司是中国平安保险（集团）股份有限公司控股的一家跨区域经营的股份制商业银行，为大陆12家全国性股份制商业银行之一。公司总部位于广东省深圳市，是中国平安集团三大业务支柱之一。
                      </div>
                    </div>
                    
                    <div style={{ marginBottom: '16px' }}>
                      <Text strong style={{ fontSize: '13px', color: '#333' }}>主要业务：</Text>
                      <div style={{ 
                        marginTop: '8px', 
                        fontSize: '12px', 
                        color: '#666', 
                        lineHeight: '1.6',
                        backgroundColor: '#fff',
                        padding: '12px',
                        borderRadius: '4px',
                        border: '1px solid #f0f0f0'
                      }}>
                        公司主要经营人民币和外币存款、贷款、结算、票据贴现、发行金融债券、代理发行、代理兑付、承销政府债券、买卖政府债券、同业拆借、提供信用证服务及担保、代理收付款项及代理保险业务等。
                      </div>
                    </div>
                    
                    <div style={{ marginBottom: '16px' }}>
                      <Text strong style={{ fontSize: '13px', color: '#333' }}>发展历程：</Text>
                      <div style={{ 
                        marginTop: '8px', 
                        fontSize: '12px', 
                        color: '#666', 
                        lineHeight: '1.6',
                        backgroundColor: '#fff',
                        padding: '12px',
                        borderRadius: '4px',
                        border: '1px solid #f0f0f0'
                      }}>
                        公司前身为深圳发展银行，成立于1987年。2012年6月，深圳发展银行吸收合并平安银行，并更名为平安银行。经过多年发展，已成为中国最具竞争力的商业银行之一。
                      </div>
                    </div>
                    
                    <div>
                      <Text strong style={{ fontSize: '13px', color: '#333' }}>核心优势：</Text>
                      <div style={{ 
                        marginTop: '8px', 
                        fontSize: '12px', 
                        color: '#666', 
                        lineHeight: '1.6',
                        backgroundColor: '#fff',
                        padding: '12px',
                        borderRadius: '4px',
                        border: '1px solid #f0f0f0'
                      }}>
                        依托中国平安集团的综合金融平台，在零售银行、公司银行、投资银行等领域具有显著优势。拥有强大的科技实力和创新能力，致力于为客户提供优质的金融服务。
                      </div>
                    </div>
                  </div>
                </Col>
              </Row>
            </Card>

            {/* K线图、持股分析、解禁信息 - 三列布局 */}
            <Card size="small" title="K线图与持股分析" style={{ marginBottom: '16px' }}>
              <Row gutter={16}>
                <Col span={12}>
                  <SimpleKLineChart stockCode={stockData.code} />
                </Col>
                <Col span={6}>
                  <Row gutter={16}>
                    <Col span={12}>
                      <SimplePieChart 
                        data={mockHoldingData.circulation} 
                        title="流通股结构" 
                        size={80}
                      />
                    </Col>
                    <Col span={12}>
                      <SimplePieChart 
                        data={mockHoldingData.topHolders} 
                        title="十大股东" 
                        size={80}
                      />
                    </Col>
                  </Row>
                  <Row gutter={16} style={{ marginTop: '16px' }}>
                    <Col span={12}>
                      <SimplePieChart 
                        data={mockHoldingData.fundHolding} 
                        title="基金持有" 
                        size={80}
                      />
                    </Col>
                    <Col span={12}>
                      <SimplePieChart 
                        data={mockHoldingData.unlockInfo} 
                        title="解禁股情况" 
                        size={80}
                      />
                    </Col>
                  </Row>
                </Col>
                <Col span={6}>
                  <div style={{ 
                    padding: '16px', 
                    backgroundColor: '#fafafa', 
                    borderRadius: '6px',
                    fontSize: '12px',
                    border: '1px solid #e8e8e8',
                    height: '100%'
                  }}>
                    <div style={{ 
                      textAlign: 'center', 
                      marginBottom: '12px', 
                      fontSize: '14px', 
                      fontWeight: 'bold', 
                      color: '#333',
                      backgroundColor: '#f5f5f5',
                      padding: '8px',
                      borderRadius: '4px',
                      border: '1px solid #d9d9d9'
                    }}>
                      📅 解禁时间信息
                    </div>
                    <Text strong style={{ color: '#333', fontSize: '13px' }}>详细解禁计划：</Text>
                    <div style={{ marginTop: '12px', lineHeight: '1.6' }}>
                      <div style={{ marginBottom: '6px', padding: '6px', backgroundColor: '#fff', borderRadius: '4px', border: '1px solid #f0f0f0' }}>
                        2024年3月：解禁2.1亿股 (8.5%)
                      </div>
                      <div style={{ marginBottom: '6px', padding: '6px', backgroundColor: '#fff', borderRadius: '4px', border: '1px solid #f0f0f0' }}>
                        2024年6月：解禁1.8亿股 (7.3%)
                      </div>
                      <div style={{ marginBottom: '6px', padding: '6px', backgroundColor: '#fff', borderRadius: '4px', border: '1px solid #f0f0f0' }}>
                        2024年9月：解禁1.2亿股 (4.9%)
                      </div>
                      <div style={{ marginBottom: '6px', padding: '6px', backgroundColor: '#fff', borderRadius: '4px', border: '1px solid #f0f0f0' }}>
                        2024年12月：解禁0.8亿股 (3.2%)
                      </div>
                    </div>
                  </div>
                </Col>
              </Row>
            </Card>

            {/* 技术指标和财务指标 */}
            <Row gutter={16}>
              <Col span={12}>
                <Card size="small" title="技术指标">
                  <Table
                    dataSource={technicalData}
                    columns={technicalColumns}
                    pagination={false}
                    size="small"
                  />
                </Card>
              </Col>
              <Col span={12}>
                <Card size="small" title="财务指标">
                  <Table
                    dataSource={financialData}
                    columns={columns}
                    pagination={false}
                    size="small"
                  />
                </Card>
              </Col>
            </Row>
          </>
        )}
      </Card>
    </div>
  );
};

export default StockAnalysisPage;
