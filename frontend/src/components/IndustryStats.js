import React, { useState, useEffect } from 'react';
import {
  Card, Row, Col, Tabs, Table, Statistic, DatePicker, Select, Spin, Radio, Tag
} from 'antd';
import {
  AreaChartOutlined, BarChartOutlined, TableOutlined,
  RiseOutlined, FallOutlined, LineChartOutlined
} from '@ant-design/icons';
import ReactECharts from 'echarts-for-react';
import moment from 'moment';
import { industryStatsApi } from '../api/industryStatsApi';
import { formatDate, formatCurrency, formatPercent } from '../utils/formatters';

const { RangePicker } = DatePicker;
const { TabPane } = Tabs;
const { Option } = Select;

const IndustryStats = ({ industryId, industryName }) => {
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState([]);
  const [dateRange, setDateRange] = useState([
    moment().subtract(1, 'months'),
    moment()
  ]);
  const [activeTab, setActiveTab] = useState('chart');
  const [metric, setMetric] = useState('total_amount');
  const [period, setPeriod] = useState('daily');
  const [latestStats, setLatestStats] = useState(null);

  // 获取行业统计数据
  useEffect(() => {
    const fetchData = async () => {
      if (!industryId) return;

      setLoading(true);
      try {
        const [start, end] = dateRange;
        const statsData = await industryStatsApi.getIndustryStats(
          industryId,
          formatDate(start, 'YYYY-MM-DD'),
          formatDate(end, 'YYYY-MM-DD')
        );
        setStats(statsData);

        // 获取最新统计数据
        // const latest = await industryStatsApi.getLatestIndustryStats(industryId);
        // setLatestStats(latest);
      } catch (error) {
        console.error('加载行业数据失败:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [industryId, dateRange]);

  // 图表配置
  const getChartOption = () => {
    console.log(stats);
    const dates = stats.map(item => formatDate(item.stat_date, 'MM-DD'));
    const values = stats.map(item => item[metric]);

    return {
      tooltip: {
        trigger: 'axis',
        formatter: (params) => {
          console.log(params);
          const data = params[0].data;
          const item = stats.find(s => formatDate(s.stat_date, 'MM-DD') === params[0].name);
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
        name: metric === 'total_amount' ? '成交额(元)' : '公司数量(家)',
        nameTextStyle: {
          padding: [0, 0, 0, 30]
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

  // 表格列定义
  const columns = [
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

  // 指标选择器
  const metricOptions = [
    { label: '成交总额', value: 'total_amount', icon: <RiseOutlined /> },
    { label: '上涨公司', value: 'up_count', icon: <RiseOutlined /> },
    { label: '下跌公司', value: 'down_count', icon: <FallOutlined /> }
  ];

  // 周期选择器
  const periodOptions = [
    { label: '日数据', value: 'daily' },
    { label: '周数据', value: 'weekly' },
    { label: '月数据', value: 'monthly' }
  ];

  return (
    <Card
      title={`${industryName} - 行业统计数据`}
      extra={
        <RangePicker
          value={dateRange}
          onChange={setDateRange}
          disabledDate={current => current && current > moment().endOf('day')}
          style={{ width: 250 }}
        />
      }
    >
      <Spin spinning={loading}>
        {latestStats && (
          <Row gutter={16} style={{ marginBottom: 24 }}>
            <Col span={6}>
              <Card bordered={false}>
                <Statistic
                  title="公司总数"
                  value={latestStats.company_count}
                  suffix="家"
                />
              </Card>
            </Col>
            <Col span={6}>
              <Card bordered={false}>
                <Statistic
                  title="成交总额"
                  value={formatCurrency(latestStats.total_amount)}
                />
              </Card>
            </Col>
            <Col span={6}>
              <Card bordered={false}>
                <Statistic
                  title="上涨公司"
                  value={latestStats.up_count}
                  suffix="家"
                  valueStyle={{ color: '#52c41a' }}
                />
              </Card>
            </Col>
            <Col span={6}>
              <Card bordered={false}>
                <Statistic
                  title="下跌公司"
                  value={latestStats.down_count}
                  suffix="家"
                  valueStyle={{ color: '#ff4d4f' }}
                />
              </Card>
            </Col>
          </Row>
        )}

        <Tabs
          activeKey={activeTab}
          onChange={setActiveTab}
          tabBarExtraContent={
            <div style={{ display: 'flex', gap: 16 }}>
              <Radio.Group
                value={metric}
                onChange={e => setMetric(e.target.value)}
                optionType="button"
                buttonStyle="solid"
              >
                {metricOptions.map(option => (
                  <Radio.Button key={option.value} value={option.value}>
                    {option.icon} {option.label}
                  </Radio.Button>
                ))}
              </Radio.Group>

              <Select
                value={period}
                onChange={setPeriod}
                style={{ width: 120 }}
              >
                {periodOptions.map(option => (
                  <Option key={option.value} value={option.value}>
                    {option.label}
                  </Option>
                ))}
              </Select>
            </div>
          }
        >
          <TabPane
            tab={
              <span>
                <AreaChartOutlined />
                趋势图表
              </span>
            }
            key="chart"
          >
            <div style={{ height: 400 }}>
              {stats.length > 0 ? (
                <ReactECharts option={getChartOption()} style={{ height: '100%' }} />
              ) : (
                <div style={{
                  height: '100%',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  color: '#8c8c8c'
                }}>
                  暂无数据
                </div>
              )}
            </div>
          </TabPane>

          <TabPane
            tab={
              <span>
                <TableOutlined />
                数据表格
              </span>
            }
            key="table"
          >
            <Table
              columns={columns}
              dataSource={stats}
              rowKey="id"
              pagination={{ pageSize: 10 }}
              scroll={{ x: 'max-content' }}
            />
          </TabPane>
        </Tabs>
      </Spin>
    </Card>
  );
};

export default IndustryStats;