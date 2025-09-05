import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { 
  Card, 
  Row, 
  Col, 
  Tabs, 
  Descriptions, 
  Tag, 
  Statistic, 
  Table, 
  Timeline, 
  Progress, 
  Divider,
  Space,
  Typography,
  Avatar,
  List,
  Badge
} from 'antd';
import { 
  RiseOutlined, 
  FallOutlined, 
  MinusOutlined,
  TrophyOutlined,
  TeamOutlined,
  GlobalOutlined,
  CalendarOutlined,
  BankOutlined,
  BarChartOutlined,
  FileTextOutlined,
  UserOutlined,
  EnvironmentOutlined
} from '@ant-design/icons';
import KLineChart from '../components/KLineChart';

const { TabPane } = Tabs;
const { Title, Text, Paragraph } = Typography;

const CompanyDetail = () => {
  const { id } = useParams();
  const [activeTab, setActiveTab] = useState('basic');

  // Mock数据 - 公司基本信息
  const company = {
    id: parseInt(id),
    ts_code: '600519.SH',
    symbol: '600519',
    name: '贵州茅台',
    industry: '饮料制造业',
    fullname: '贵州茅台酒股份有限公司',
    list_date: '2001-08-27',
    exchange: 'SSE',
    chairman: '丁雄军',
    reg_capital: 125619.78,
    setup_date: '1999-11-20',
    province: '贵州省',
    city: '遵义市',
    website: 'www.moutaichina.com',
    employees: 29971,
    status: '在市',
    main_business: '茅台酒及系列产品的生产与销售',
    business_scope: '茅台酒系列产品的生产与销售;饮料、食品、包装材料的生产与销售等',
    market: '主板',
    area: '贵州',
    phone: '0851-22386000',
    email: 'moutai@moutaichina.com',
    address: '贵州省遵义市仁怀市茅台镇'
  };

  // Mock数据 - 市场表现
  const marketData = {
    current_price: 1688.00,
    change: 25.50,
    pct_change: 1.53,
    open: 1665.00,
    high: 1695.00,
    low: 1660.00,
    pre_close: 1662.50,
    volume: 1250000,
    turnover: 2100000000,
    market_cap: 2120000000000,
    pe_ratio: 35.6,
    pb_ratio: 12.8,
    dividend_yield: 1.2
  };

  // Mock数据 - 财务数据
  const financialData = {
    revenue: 127500000000, // 1275亿
    net_profit: 62700000000, // 627亿
    total_assets: 2800000000000, // 2.8万亿
    total_liabilities: 800000000000, // 8000亿
    operating_cash_flow: 85000000000, // 850亿
    roe: 22.4, // 22.4%
    roa: 18.6, // 18.6%
    debt_ratio: 28.6, // 28.6%
    gross_margin: 91.2, // 91.2%
    net_margin: 49.2, // 49.2%
    current_ratio: 3.2,
    quick_ratio: 2.8
  };

  // Mock数据 - 股东结构
  const shareholders = [
    { rank: 1, name: '中国贵州茅台酒厂(集团)有限责任公司', type: '国有', shares: 678000000, ratio: 54.00, change: 0 },
    { rank: 2, name: '香港中央结算有限公司', type: '外资', shares: 123000000, ratio: 9.79, change: 0.15 },
    { rank: 3, name: '中国证券金融股份有限公司', type: '国有', shares: 45600000, ratio: 3.63, change: -0.08 },
    { rank: 4, name: '中央汇金资产管理有限责任公司', type: '国有', shares: 23400000, ratio: 1.86, change: 0 },
    { rank: 5, name: '全国社保基金一零八组合', type: '社保', shares: 18900000, ratio: 1.50, change: 0.02 }
  ];

  // Mock数据 - 公司新闻
  const news = [
    { 
      id: 1, 
      title: '贵州茅台发布2024年第一季度业绩报告', 
      date: '2024-04-28', 
      type: '业绩公告',
      summary: '公司2024年第一季度实现营业收入同比增长15.6%，净利润同比增长18.2%'
    },
    { 
      id: 2, 
      title: '贵州茅台荣获"2024年度最具价值品牌"称号', 
      date: '2024-04-15', 
      type: '荣誉奖项',
      summary: '在2024年度品牌价值评选中，贵州茅台品牌价值突破2万亿元'
    },
    { 
      id: 3, 
      title: '贵州茅台与多家企业签署战略合作协议', 
      date: '2024-04-10', 
      type: '合作签约',
      summary: '公司与多家知名企业签署战略合作协议，共同推进白酒产业发展'
    },
    { 
      id: 4, 
      title: '贵州茅台发布ESG可持续发展报告', 
      date: '2024-03-28', 
      type: 'ESG报告',
      summary: '公司发布2023年度ESG可持续发展报告，展示在环境保护、社会责任等方面的成果'
    }
  ];

  // Mock数据 - 行业对比
  const industryComparison = [
    { company: '贵州茅台', market_cap: 2120000000000, pe: 35.6, roe: 22.4, revenue: 127500000000 },
    { company: '五粮液', market_cap: 680000000000, pe: 28.3, roe: 18.6, revenue: 68000000000 },
    { company: '泸州老窖', market_cap: 420000000000, pe: 32.1, roe: 16.8, revenue: 42000000000 },
    { company: '洋河股份', market_cap: 380000000000, pe: 25.4, roe: 15.2, revenue: 38000000000 },
    { company: '山西汾酒', market_cap: 320000000000, pe: 38.9, roe: 19.1, revenue: 32000000000 }
  ];

  // 股东结构表格列定义
  const shareholderColumns = [
    { title: '排名', dataIndex: 'rank', key: 'rank', width: 80 },
    { title: '股东名称', dataIndex: 'name', key: 'name', width: 300 },
    { title: '类型', dataIndex: 'type', key: 'type', width: 100, render: (type) => {
      const colors = { '国有': 'red', '外资': 'blue', '社保': 'green', '个人': 'orange' };
      return <Tag color={colors[type]}>{type}</Tag>;
    }},
    { title: '持股数量(股)', dataIndex: 'shares', key: 'shares', width: 150, render: (value) => (value / 10000).toFixed(0) + '万' },
    { title: '持股比例(%)', dataIndex: 'ratio', key: 'ratio', width: 120, render: (value) => value.toFixed(2) },
    { title: '变动(%)', dataIndex: 'change', key: 'change', width: 100, render: (value) => {
      if (value > 0) return <span style={{ color: '#f5222d' }}>+{value.toFixed(2)}</span>;
      if (value < 0) return <span style={{ color: '#52c41a' }}>{value.toFixed(2)}</span>;
      return <span style={{ color: '#666' }}>0.00</span>;
    }}
  ];

  // 行业对比表格列定义
  const comparisonColumns = [
    { title: '公司名称', dataIndex: 'company', key: 'company', width: 150 },
    { title: '市值(亿元)', dataIndex: 'market_cap', key: 'market_cap', width: 120, render: (value) => (value / 100000000).toFixed(0) },
    { title: '市盈率(PE)', dataIndex: 'pe', key: 'pe', width: 120, render: (value) => value.toFixed(1) },
    { title: 'ROE(%)', dataIndex: 'roe', key: 'roe', width: 100, render: (value) => value.toFixed(1) },
    { title: '营收(亿元)', dataIndex: 'revenue', key: 'revenue', width: 120, render: (value) => (value / 100000000).toFixed(0) }
  ];

  // 获取涨跌颜色
  const getChangeColor = (change) => {
    if (change > 0) return '#f5222d';
    if (change < 0) return '#52c41a';
    return '#666';
  };

  // 获取涨跌图标
  const getChangeIcon = (change) => {
    if (change > 0) return <RiseOutlined style={{ color: '#f5222d' }} />;
    if (change < 0) return <FallOutlined style={{ color: '#52c41a' }} />;
    return <MinusOutlined style={{ color: '#666' }} />;
  };

  return (
    <div style={{ padding: 24, background: '#f5f5f5', minHeight: '100vh' }}>
      {/* 页面标题和概览 */}
      <Card style={{ marginBottom: 24 }}>
        <Row gutter={24} align="middle">
          <Col span={16}>
            <Title level={2} style={{ margin: 0 }}>
              {company.name} ({company.ts_code})
            </Title>
            <Text type="secondary" style={{ fontSize: 16 }}>
              {company.fullname}
            </Text>
            <div style={{ marginTop: 16 }}>
              <Space size="large">
                <Tag color="blue" icon={<BankOutlined />}>{company.industry}</Tag>
                <Tag color="green" icon={<EnvironmentOutlined />}>{company.province} {company.city}</Tag>
                <Tag color="orange" icon={<CalendarOutlined />}>{company.market}</Tag>
                <Tag color={company.status === '在市' ? 'green' : 'red'} icon={<TrophyOutlined />}>
                  {company.status}
                </Tag>
              </Space>
            </div>
          </Col>
          <Col span={8} style={{ textAlign: 'right' }}>
            <Statistic
              title="当前股价"
              value={marketData.current_price}
              precision={2}
              valueStyle={{ color: getChangeColor(marketData.change), fontSize: 32, fontWeight: 'bold' }}
              suffix="元"
            />
            <div style={{ marginTop: 8 }}>
              <Space>
                {getChangeIcon(marketData.change)}
                <Text style={{ color: getChangeColor(marketData.change), fontSize: 18, fontWeight: 'bold' }}>
                  {marketData.change > 0 ? '+' : ''}{marketData.change.toFixed(2)} ({marketData.pct_change > 0 ? '+' : ''}{marketData.pct_change.toFixed(2)}%)
                </Text>
              </Space>
            </div>
          </Col>
        </Row>
      </Card>

      {/* 主要指标卡片 */}
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="总市值"
              value={marketData.market_cap / 100000000}
              precision={0}
              suffix="亿元"
              valueStyle={{ color: '#1890ff' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="市盈率(PE)"
              value={marketData.pe_ratio}
              precision={1}
              valueStyle={{ color: '#52c41a' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="市净率(PB)"
              value={marketData.pb_ratio}
              precision={1}
              valueStyle={{ color: '#faad14' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="股息率"
              value={marketData.dividend_yield}
              precision={2}
              suffix="%"
              valueStyle={{ color: '#f5222d' }}
            />
          </Card>
        </Col>
      </Row>

      {/* 主要内容区域 */}
      <Card>
        <Tabs activeKey={activeTab} onChange={setActiveTab} size="large">
          {/* 基本信息 */}
          <TabPane tab="基本信息" key="basic">
            <Row gutter={24}>
              <Col span={12}>
                <Title level={4}>公司概况</Title>
                <Descriptions bordered column={1} size="small">
                  <Descriptions.Item label="股票代码">
                    <Tag color="blue">{company.ts_code}</Tag>
                  </Descriptions.Item>
                  <Descriptions.Item label="公司全称">{company.fullname}</Descriptions.Item>
                  <Descriptions.Item label="上市状态">
                    <Tag color="green">{company.status}</Tag>
                  </Descriptions.Item>
                  <Descriptions.Item label="交易所">{company.exchange}</Descriptions.Item>
                  <Descriptions.Item label="上市日期">{company.list_date}</Descriptions.Item>
                  <Descriptions.Item label="行业">{company.industry}</Descriptions.Item>
                  <Descriptions.Item label="注册资本">
                    {(company.reg_capital / 10000).toFixed(2)}万元
                  </Descriptions.Item>
                  <Descriptions.Item label="员工人数">
                    <Space>
                      <TeamOutlined />
                      {company.employees.toLocaleString()}人
                    </Space>
                  </Descriptions.Item>
                  <Descriptions.Item label="成立日期">{company.setup_date}</Descriptions.Item>
                  <Descriptions.Item label="省份">{company.province}</Descriptions.Item>
                  <Descriptions.Item label="城市">{company.city}</Descriptions.Item>
                  <Descriptions.Item label="董事长">
                    <Space>
                      <UserOutlined />
                      {company.chairman || '未知'}
                    </Space>
                  </Descriptions.Item>
                  <Descriptions.Item label="联系电话">{company.phone}</Descriptions.Item>
                  <Descriptions.Item label="电子邮箱">{company.email}</Descriptions.Item>
                  <Descriptions.Item label="公司网址">
                    <a href={`http://${company.website}`} target="_blank" rel="noreferrer">
                      <Space>
                        <GlobalOutlined />
                        {company.website}
                      </Space>
                    </a>
                  </Descriptions.Item>
                  <Descriptions.Item label="公司地址">{company.address}</Descriptions.Item>
                </Descriptions>
              </Col>
              <Col span={12}>
                <Title level={4}>主营业务</Title>
                <Card size="small" style={{ marginBottom: 16 }}>
                  <Paragraph>{company.main_business}</Paragraph>
                </Card>
                
                <Title level={4}>经营范围</Title>
                <Card size="small">
                  <Paragraph>{company.business_scope}</Paragraph>
                </Card>
              </Col>
            </Row>
          </TabPane>

          {/* 财务数据 */}
          <TabPane tab="财务数据" key="financial">
            <Row gutter={24}>
              <Col span={12}>
                <Title level={4}>主要财务指标</Title>
                <Row gutter={16}>
                  <Col span={12}>
                    <Card size="small">
                      <Statistic
                        title="营业收入"
                        value={financialData.revenue / 100000000}
                        precision={0}
                        suffix="亿元"
                        valueStyle={{ color: '#1890ff' }}
                      />
                    </Card>
                  </Col>
                  <Col span={12}>
                    <Card size="small">
                      <Statistic
                        title="净利润"
                        value={financialData.net_profit / 100000000}
                        precision={0}
                        suffix="亿元"
                        valueStyle={{ color: '#52c41a' }}
                      />
                    </Card>
                  </Col>
                  <Col span={12}>
                    <Card size="small">
                      <Statistic
                        title="总资产"
                        value={financialData.total_assets / 100000000}
                        precision={0}
                        suffix="亿元"
                        valueStyle={{ color: '#faad14' }}
                      />
                    </Card>
                  </Col>
                  <Col span={12}>
                    <Card size="small">
                      <Statistic
                        title="总负债"
                        value={financialData.total_liabilities / 100000000}
                        precision={0}
                        suffix="亿元"
                        valueStyle={{ color: '#f5222d' }}
                      />
                    </Card>
                  </Col>
                </Row>
              </Col>
              <Col span={12}>
                <Title level={4}>财务比率</Title>
                <Row gutter={16}>
                  <Col span={12}>
                    <Card size="small">
                      <Statistic
                        title="ROE"
                        value={financialData.roe}
                        precision={1}
                        suffix="%"
                        valueStyle={{ color: '#1890ff' }}
                      />
                    </Card>
                  </Col>
                  <Col span={12}>
                    <Card size="small">
                      <Statistic
                        title="ROA"
                        value={financialData.roa}
                        precision={1}
                        suffix="%"
                        valueStyle={{ color: '#52c41a' }}
                      />
                    </Card>
                  </Col>
                  <Col span={12}>
                    <Card size="small">
                      <Card size="small">
                        <Statistic
                          title="资产负债率"
                          value={financialData.debt_ratio}
                          precision={1}
                          suffix="%"
                          valueStyle={{ color: '#faad14' }}
                        />
                      </Card>
                    </Card>
                  </Col>
                  <Col span={12}>
                    <Card size="small">
                      <Statistic
                        title="毛利率"
                        value={financialData.gross_margin}
                        precision={1}
                        suffix="%"
                        valueStyle={{ color: '#f5222d' }}
                      />
                    </Card>
                  </Col>
                </Row>
              </Col>
            </Row>
            
            <Divider />
            
            <Title level={4}>财务指标趋势</Title>
            <Row gutter={16}>
              <Col span={8}>
                <Card size="small">
                  <div style={{ textAlign: 'center' }}>
                    <Progress
                      type="circle"
                      percent={financialData.roe}
                      format={(percent) => `${percent}%`}
                      strokeColor="#1890ff"
                    />
                    <div style={{ marginTop: 16 }}>
                      <Text strong>ROE</Text>
                    </div>
                  </div>
                </Card>
              </Col>
              <Col span={8}>
                <Card size="small">
                  <div style={{ textAlign: 'center' }}>
                    <Progress
                      type="circle"
                      percent={financialData.gross_margin}
                      format={(percent) => `${percent}%`}
                      strokeColor="#52c41a"
                    />
                    <div style={{ marginTop: 16 }}>
                      <Text strong>毛利率</Text>
                    </div>
                  </div>
                </Card>
              </Col>
              <Col span={8}>
                <Card size="small">
                  <div style={{ textAlign: 'center' }}>
                    <Progress
                      type="circle"
                      percent={100 - financialData.debt_ratio}
                      format={(percent) => `${100 - financialData.debt_ratio}%`}
                      strokeColor="#faad14"
                    />
                    <div style={{ marginTop: 16 }}>
                      <Text strong>权益比率</Text>
                    </div>
                  </div>
                </Card>
              </Col>
            </Row>
          </TabPane>

          {/* 市场表现 */}
          <TabPane tab="市场表现" key="market">
            <Row gutter={24}>
              <Col span={12}>
                <Title level={4}>今日行情</Title>
                <Descriptions bordered column={2} size="small">
                  <Descriptions.Item label="开盘价">{marketData.open.toFixed(2)}元</Descriptions.Item>
                  <Descriptions.Item label="最高价">{marketData.high.toFixed(2)}元</Descriptions.Item>
                  <Descriptions.Item label="最低价">{marketData.low.toFixed(2)}元</Descriptions.Item>
                  <Descriptions.Item label="昨收价">{marketData.pre_close.toFixed(2)}元</Descriptions.Item>
                  <Descriptions.Item label="成交量">{(marketData.volume / 10000).toFixed(0)}万手</Descriptions.Item>
                  <Descriptions.Item label="成交额">{(marketData.turnover / 100000000).toFixed(2)}亿元</Descriptions.Item>
                </Descriptions>
              </Col>
              <Col span={12}>
                <Title level={4}>估值指标</Title>
                <Descriptions bordered column={2} size="small">
                  <Descriptions.Item label="市盈率(PE)">{marketData.pe_ratio.toFixed(1)}</Descriptions.Item>
                  <Descriptions.Item label="市净率(PB)">{marketData.pb_ratio.toFixed(1)}</Descriptions.Item>
                  <Descriptions.Item label="股息率">{marketData.dividend_yield.toFixed(2)}%</Descriptions.Item>
                  <Descriptions.Item label="总市值">{(marketData.market_cap / 100000000).toFixed(0)}亿元</Descriptions.Item>
                </Descriptions>
              </Col>
            </Row>
            
            <Divider />
            
            <Title level={4}>K线图</Title>
            <div style={{ height: 500 }}>
              <KLineChart tsCode={company.ts_code} />
            </div>
          </TabPane>

          {/* 股东结构 */}
          <TabPane tab="股东结构" key="shareholders">
            <Title level={4}>前十大股东</Title>
            <Table
              columns={shareholderColumns}
              dataSource={shareholders}
              pagination={false}
              size="small"
              bordered
            />
            
            <Divider />
            
            <Title level={4}>股东类型分布</Title>
            <Row gutter={16}>
              <Col span={8}>
                <Card size="small">
                  <div style={{ textAlign: 'center' }}>
                    <Progress
                      type="circle"
                      percent={54}
                      format={(percent) => `${percent}%`}
                      strokeColor="#f5222d"
                    />
                    <div style={{ marginTop: 16 }}>
                      <Text strong>国有股东</Text>
                    </div>
                  </div>
                </Card>
              </Col>
              <Col span={8}>
                <Card size="small">
                  <div style={{ textAlign: 'center' }}>
                    <Progress
                      type="circle"
                      percent={9.79}
                      format={(percent) => `${percent}%`}
                      strokeColor="#1890ff"
                    />
                    <div style={{ marginTop: 16 }}>
                      <Text strong>外资股东</Text>
                    </div>
                  </div>
                </Card>
              </Col>
              <Col span={8}>
                <Card size="small">
                  <div style={{ textAlign: 'center' }}>
                    <Progress
                      type="circle"
                      percent={36.21}
                      format={(percent) => `${percent}%`}
                      strokeColor="#52c41a"
                    />
                    <div style={{ marginTop: 16 }}>
                      <Text strong>其他股东</Text>
                    </div>
                  </div>
                </Card>
              </Col>
            </Row>
          </TabPane>

          {/* 公司新闻 */}
          <TabPane tab="公司新闻" key="news">
            <Title level={4}>最新动态</Title>
            <List
              itemLayout="vertical"
              size="large"
              pagination={{
                onChange: (page) => {
                  console.log(page);
                },
                pageSize: 10,
              }}
              dataSource={news}
              renderItem={(item) => (
                <List.Item
                  key={item.id}
                  extra={
                    <Space>
                      <Badge status="processing" text={item.type} />
                      <Text type="secondary">{item.date}</Text>
                    </Space>
                  }
                >
                  <List.Item.Meta
                    title={<a href="#">{item.title}</a>}
                    description={item.summary}
                  />
                </List.Item>
              )}
            />
          </TabPane>

          {/* 行业对比 */}
          <TabPane tab="行业对比" key="comparison">
            <Title level={4}>同行业公司对比</Title>
            <Table
              columns={comparisonColumns}
              dataSource={industryComparison}
              pagination={false}
              size="small"
              bordered
              rowClassName={(record) => record.company === '贵州茅台' ? 'highlight-row' : ''}
            />
            
            <Divider />
            
            <Title level={4}>行业地位分析</Title>
            <Row gutter={16}>
              <Col span={8}>
                <Card size="small">
                  <div style={{ textAlign: 'center' }}>
                    <Progress
                      type="circle"
                      percent={100}
                      format={() => '1'}
                      strokeColor="#f5222d"
                    />
                    <div style={{ marginTop: 16 }}>
                      <Text strong>市值排名</Text>
                    </div>
                  </div>
                </Card>
              </Col>
              <Col span={8}>
                <Card size="small">
                  <div style={{ textAlign: 'center' }}>
                    <Progress
                      type="circle"
                      percent={100}
                      format={() => '1'}
                      strokeColor="#1890ff"
                    />
                    <div style={{ marginTop: 16 }}>
                      <Text strong>营收排名</Text>
                    </div>
                  </div>
                </Card>
              </Col>
              <Col span={8}>
                <Card size="small">
                  <div style={{ textAlign: 'center' }}>
                    <Progress
                      type="circle"
                      percent={100}
                      format={() => '1'}
                      strokeColor="#52c41a"
                    />
                    <div style={{ marginTop: 16 }}>
                      <Text strong>净利润排名</Text>
                    </div>
                  </div>
                </Card>
              </Col>
            </Row>
          </TabPane>
        </Tabs>
      </Card>
    </div>
  );
};

export default CompanyDetail;