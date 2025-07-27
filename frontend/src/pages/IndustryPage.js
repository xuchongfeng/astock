import React, { useState, useEffect } from 'react';
import {
  Row, Col, Card, Select, Statistic, Tabs, Table, Spin, Radio, DatePicker, Empty, Tag
} from 'antd';
import {
  BarChartOutlined, RiseOutlined, FallOutlined,
  LineChartOutlined, StockOutlined, DatabaseOutlined
} from '@ant-design/icons';
import ReactECharts from 'echarts-for-react';
import { industryApi } from '../api/industryApi';
import { industryStatsApi } from '../api/industryStatsApi';
import { formatDate, formatCurrency, formatPercent } from '../utils/formatters';
import IndustryStatsCard from '../components/IndustryStatsCard';
import moment from "moment";

const { TabPane } = Tabs;
const { Option } = Select;
const { RangePicker } = DatePicker;

const IndustryPage = () => {
  const [industries, setIndustries] = useState([]);
  const [selectedIndustry, setSelectedIndustry] = useState(null);
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState([]);
  const [latestStats, setLatestStats] = useState(null);
  const [rankingData, setRankingData] = useState([]);
  const [activeTab, setActiveTab] = useState('stats');
  const [metric, setMetric] = useState('total_amount');
  const [period, setPeriod] = useState('daily');
  const [dateRange, setDateRange] = useState([
    moment().subtract(1, 'months'),
    moment()
  ]);
  const [error, setError] = useState(null);

  // 获取行业列表
  useEffect(() => {
    const fetchIndustries = async () => {
      setLoading(true);
      try {
        const response = await industryApi.getAllIndustries();
        setIndustries(response.data);
        if (response.length > 0) {
          setSelectedIndustry(response[0].id);
        }
      } catch (error) {
        console.error('获取行业列表失败:', error);
        setError('加载行业列表失败，请稍后重试');
      } finally {
        setLoading(false);
      }
    };

    fetchIndustries();
  }, []);

  // 获取行业统计数据
  useEffect(() => {
    const fetchIndustryData = async () => {
      if (!selectedIndustry) return;

      setLoading(true);
      setError(null);

      try {
        // 获取最新统计数据
        const latest = await industryStatsApi.getLatestIndustryStats(selectedIndustry);
        setLatestStats(latest.data[0]);

        // 获取历史统计数据
        const [start, end] = dateRange;
        const statsData = await industryStatsApi.getIndustryStats(
          selectedIndustry,
          formatDate(start, 'YYYY-MM-DD'),
          formatDate(end, 'YYYY-MM-DD')
        );
        setStats(statsData.data);

        // 获取行业排行榜
        const today = new Date().toISOString().split('T')[0];
        const ranking = await industryStatsApi.getIndustryRanking('total_amount', today, 10);
        setRankingData(ranking.data);
      } catch (error) {
        console.error('获取行业数据失败:', error);
        setError('加载行业数据失败，请检查网络连接');
      } finally {
        setLoading(false);
      }
    };

    fetchIndustryData();
  }, [selectedIndustry, dateRange]);

  // 行业趋势图表配置
  const getTrendChartOption = () => {
    if (!stats || stats.length === 0) {
      return {
        title: {
          text: '暂无数据',
          left: 'center',
          top: 'center',
          textStyle: {
            color: '#8c8c8c',
            fontSize: 16
          }
        }
      };
    }

    const dates = stats.map(item => formatDate(item.stat_date, 'MM-DD'));
    const values = stats.map(item => item[metric]);

    return {
      tooltip: {
        trigger: 'axis',
        formatter: (params) => {
          console.log(params)
          const item = stats.find(s =>
            formatDate(s.stat_date, 'MM-DD') === params[0].name
          );
          return `
            <div style="margin-bottom: 5px; font-weight: bold">${formatDate(item.stat_date, 'YYYY-MM-DD')}</div>
            <div>成交总额: ${formatCurrency(item.total_amount)}</div>
            <div>上涨公司: ${item.up_count}家</div>
            <div>下跌公司: ${item.down_count}家</div>
            <div>平盘公司: ${item.flat_count}家</div>
          `;
        }
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
      },
      xAxis: {
        type: 'category',
        data: dates,
        axisLabel: {
          rotate: 45
        }
      },
      yAxis: {
        type: 'value',
        name: metric === 'total_amount' ? '成交额(亿元)' : '公司数量(家)',
        nameTextStyle: {
          padding: [0, 0, 0, 30]
        },

        axisLabel: {
          formatter: function(value) {
          if (metric === 'total_amount') {
            // 将元转换为亿元并保留两位小数
            return (value / 100000000).toFixed(2);
          }
          return value;
        }
  }
      },
      series: [{
        data: values,
        type: 'line',
        smooth: true,
        lineStyle: {
          width: 3,
          color: '#1890ff'
        },
        areaStyle: {
          color: {
            type: 'linear',
            x: 0,
            y: 0,
            x2: 0,
            y2: 1,
            colorStops: [{
              offset: 0, color: 'rgba(24, 144, 255, 0.5)'
            }, {
              offset: 1, color: 'rgba(24, 144, 255, 0.1)'
            }]
          }
        },
        markPoint: {
          data: [
            { type: 'max', name: '最大值' },
            { type: 'min', name: '最小值' }
          ]
        }
      }]
    };
  };

  // 行业对比图表配置
  const getComparisonChartOption = () => {
    if (!rankingData || rankingData.length === 0) {
      return {
        title: {
          text: '暂无数据',
          left: 'center',
          top: 'center',
          textStyle: {
            color: '#8c8c8c',
            fontSize: 16
          }
        }
      };
    }

    const industryNames = rankingData.map(item => item.industry_name);
    const amounts = rankingData.map(item => item.total_amount);

    return {
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'shadow'
        },
        formatter: (params) => {
          const item = rankingData[params[0].dataIndex];
          return `
            <div style="margin-bottom: 5px; font-weight: bold">${item.industry_name}</div>
            <div>成交总额: ${formatCurrency(item.total_amount)}</div>
            <div>公司数量: ${item.company_count}家</div>
            <div>上涨公司: ${item.up_count}家</div>
            <div>下跌公司: ${item.down_count}家</div>
          `;
        }
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
      },
      xAxis: {
        type: 'category',
        data: industryNames,
        axisLabel: {
          interval: 0,
          rotate: 45
        }
      },
      yAxis: {
        type: 'value',
        name: '成交额(元)'
      },
      series: [{
        data: amounts,
        type: 'bar',
        itemStyle: {
          color: function(params) {
            const colors = [
              '#1890ff', '#52c41a', '#faad14', '#ff4d4f',
              '#13c2c2', '#722ed1', '#eb2f96', '#fa8c16',
              '#a0d911', '#f5222d'
            ];
            return colors[params.dataIndex % colors.length];
          }
        }
      }]
    };
  };

  // 行业排行榜表格列定义
  const rankingColumns = [
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

  // 行业统计数据表格列定义
  const statsColumns = [
    {
      title: '统计日期',
      dataIndex: 'stat_date',
      key: 'stat_date',
      render: date => formatDate(date, 'YYYY-MM-DD'),
      sorter: (a, b) => new Date(a.stat_date) - new Date(b.stat_date)
    },
    {
      title: '公司总数',
      dataIndex: 'company_count',
      key: 'company_count',
      align: 'center'
    },
    {
      title: '成交总额',
      dataIndex: 'total_amount',
      key: 'total_amount',
      render: amount => formatCurrency(amount),
      sorter: (a, b) => a.total_amount - b.total_amount
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
      title: '平盘公司',
      dataIndex: 'flat_count',
      key: 'flat_count',
      render: count => <Tag color="#8c8c8c">{count}家</Tag>,
      align: 'center',
      sorter: (a, b) => a.flat_count - b.flat_count
    }
  ];

  // 指标选择器
  const metricOptions = [
    { label: '成交总额', value: 'total_amount', icon: <RiseOutlined /> },
    { label: '上涨公司', value: 'up_count', icon: <RiseOutlined /> },
    { label: '下跌公司', value: 'down_count', icon: <FallOutlined /> }
  ];

  return (
    <div style={{ padding: 24 }}>
      <Card
        title="行业数据分析"
        bordered={false}
        extra={
          <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
            <Select
              value={selectedIndustry}
              onChange={setSelectedIndustry}
              style={{ width: 300 }}
              loading={loading}
              placeholder="选择行业"
            >
              {industries.map(industry => (
                <Select.Option key={industry.id} value={industry.id}>
                  {industry.name}
                </Select.Option>
              ))}
            </Select>

            <Tabs activeKey={activeTab} onChange={setActiveTab} size="small">
              <TabPane tab="行业统计" key="stats" />
              <TabPane tab="行业排行" key="ranking" />
            </Tabs>
          </div>
        }
      >
        {error && (
          <div style={{
            padding: 16,
            marginBottom: 16,
            background: '#fff1f0',
            border: '1px solid #ffccc7',
            borderRadius: 4
          }}>
            <div style={{ color: '#ff4d4f' }}>{error}</div>
          </div>
        )}

        <Spin spinning={loading}>
          {activeTab === 'stats' ? (
            <div>
              {latestStats && (
                <Row gutter={16} style={{ marginBottom: 24 }}>
                  <Col span={6}>
                    <IndustryStatsCard
                      title="公司总数"
                      value={latestStats.company_count}
                      suffix="家"
                      icon={<DatabaseOutlined />}
                      color="#1890ff"
                    />
                  </Col>
                  <Col span={6}>
                    <IndustryStatsCard
                      title="成交总额"
                      value={formatCurrency(latestStats.total_amount)}
                      icon={<RiseOutlined />}
                      color="#52c41a"
                    />
                  </Col>
                  <Col span={6}>
                    <IndustryStatsCard
                      title="上涨公司"
                      value={latestStats.up_count}
                      suffix="家"
                      icon={<RiseOutlined />}
                      color="#52c41a"
                    />
                  </Col>
                  <Col span={6}>
                    <IndustryStatsCard
                      title="下跌公司"
                      value={latestStats.down_count}
                      suffix="家"
                      icon={<FallOutlined />}
                      color="#ff4d4f"
                    />
                  </Col>
                </Row>
              )}

              <Card
                title="行业趋势分析"
                extra={
                  <div style={{ display: 'flex', gap: 16 }}>
                    <RangePicker
                      value={dateRange}
                      onChange={setDateRange}
                      disabledDate={current => current && current > moment().endOf('day')}
                      style={{ width: 250 }}
                    />

                    <Radio.Group
                      value={metric}
                      onChange={e => setMetric(e.target.value)}
                      buttonStyle="solid"
                    >
                      {metricOptions.map(option => (
                        <Radio.Button key={option.value} value={option.value}>
                          {option.icon} {option.label}
                        </Radio.Button>
                      ))}
                    </Radio.Group>
                  </div>
                }
              >
                {stats.length > 0 ? (
                  <ReactECharts
                    option={getTrendChartOption()}
                    style={{ height: 400 }}
                  />
                ) : (
                  <Empty
                    description="暂无行业数据"
                    image={Empty.PRESENTED_IMAGE_SIMPLE}
                    style={{ padding: 40 }}
                  />
                )}

                <Table
                  columns={statsColumns}
                  dataSource={stats}
                  rowKey="id"
                  pagination={{ pageSize: 5 }}
                  style={{ marginTop: 24 }}
                  scroll={{ x: 'max-content' }}
                />
              </Card>
            </div>
          ) : (
            <div>
              <Card
                title="行业排行榜"
                extra={
                  <Radio.Group
                    value={period}
                    onChange={e => setPeriod(e.target.value)}
                    buttonStyle="solid"
                  >
                    <Radio.Button value="daily">日榜</Radio.Button>
                    <Radio.Button value="weekly">周榜</Radio.Button>
                    <Radio.Button value="monthly">月榜</Radio.Button>
                  </Radio.Group>
                }
              >
                {rankingData.length > 0 ? (
                  <ReactECharts
                    option={getComparisonChartOption()}
                    style={{ height: 400 }}
                  />
                ) : (
                  <Empty
                    description="暂无排行榜数据"
                    image={Empty.PRESENTED_IMAGE_SIMPLE}
                    style={{ padding: 40 }}
                  />
                )}

                <Table
                  columns={rankingColumns}
                  dataSource={rankingData}
                  rowKey="id"
                  pagination={{ pageSize: 10 }}
                  style={{ marginTop: 24 }}
                  scroll={{ x: 'max-content' }}
                />
              </Card>
            </div>
          )}
        </Spin>
      </Card>
    </div>
  );
};

export default IndustryPage;