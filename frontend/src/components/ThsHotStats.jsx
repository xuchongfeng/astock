import React, { useState, useEffect } from 'react';
import { Card, Row, Col, Statistic, Select, DatePicker, Button, Spin, Alert } from 'antd';
import { fetchHotDataStatistics, fetchDataTypes } from '../api/thsHot';
import { ReloadOutlined, BarChartOutlined } from '@ant-design/icons';
import dayjs from 'dayjs';

const { RangePicker } = DatePicker;
const { Option } = Select;

const ThsHotStats = () => {
  const [loading, setLoading] = useState(false);
  const [stats, setStats] = useState(null);
  const [dataTypes, setDataTypes] = useState([]);
  const [filters, setFilters] = useState({
    start_date: dayjs().subtract(7, 'day').format('YYYY-MM-DD'),
    end_date: dayjs().format('YYYY-MM-DD')
  });

  useEffect(() => {
    fetchDataTypesList();
    fetchStats();
  }, [filters]);

  const fetchDataTypesList = async () => {
    try {
      const response = await fetchDataTypes();
      setDataTypes(response.data.data_types);
    } catch (error) {
      console.error('获取数据类型失败:', error);
    }
  };

  const fetchStats = async () => {
    setLoading(true);
    try {
      const response = await fetchHotDataStatistics(filters);
      setStats(response.data);
    } catch (error) {
      console.error('获取统计信息失败:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDateRangeChange = (dates) => {
    if (dates) {
      setFilters({
        start_date: dates[0].format('YYYY-MM-DD'),
        end_date: dates[1].format('YYYY-MM-DD')
      });
    } else {
      setFilters({
        start_date: dayjs().subtract(7, 'day').format('YYYY-MM-DD'),
        end_date: dayjs().format('YYYY-MM-DD')
      });
    }
  };

  const handleRefresh = () => {
    fetchStats();
  };

  if (!stats) {
    return (
      <Card>
        <div style={{ textAlign: 'center', padding: '20px' }}>
          <Spin size="large" />
          <div style={{ marginTop: '10px' }}>加载统计信息中...</div>
        </div>
      </Card>
    );
  }

  return (
    <Card
      title={
        <span>
          <BarChartOutlined style={{ marginRight: 8 }} />
          热榜数据统计
        </span>
      }
      extra={
        <Button icon={<ReloadOutlined />} onClick={handleRefresh}>
          刷新
        </Button>
      }
    >
      {/* 过滤条件 */}
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={8}>
          <RangePicker
            value={[dayjs(filters.start_date), dayjs(filters.end_date)]}
            onChange={handleDateRangeChange}
            style={{ width: '100%' }}
          />
        </Col>
        <Col span={8}>
          <Select
            placeholder="选择数据类型"
            style={{ width: '100%' }}
            allowClear
          >
            {dataTypes.map(type => (
              <Option key={type} value={type}>{type}</Option>
            ))}
          </Select>
        </Col>
      </Row>

      {/* 统计信息 */}
      <Row gutter={16}>
        <Col span={8}>
          <Card>
            <Statistic
              title="数据日期范围"
              value={`${stats.date_range.start_date || 'N/A'} 至 ${stats.date_range.end_date || 'N/A'}`}
              valueStyle={{ fontSize: '14px' }}
            />
          </Card>
        </Col>
        <Col span={8}>
          <Card>
            <Statistic
              title="数据类型数量"
              value={stats.type_statistics.length}
              suffix="种"
            />
          </Card>
        </Col>
        <Col span={8}>
          <Card>
            <Statistic
              title="总记录数"
              value={stats.type_statistics.reduce((sum, item) => sum + item.count, 0)}
              suffix="条"
            />
          </Card>
        </Col>
      </Row>

      {/* 各类型数据统计 */}
      <Card title="各类型数据统计" style={{ marginTop: 16 }}>
        <Row gutter={[16, 16]}>
          {stats.type_statistics.map((item, index) => (
            <Col span={6} key={index}>
              <Card size="small">
                <Statistic
                  title={item.data_type}
                  value={item.count}
                  suffix="条"
                  valueStyle={{ 
                    color: item.count > 1000 ? '#52c41a' : 
                           item.count > 500 ? '#fa8c16' : '#1890ff'
                  }}
                />
              </Card>
            </Col>
          ))}
        </Row>
      </Card>

      {/* 数据概览 */}
      <Card title="数据概览" style={{ marginTop: 16 }}>
        <Alert
          message="数据说明"
          description={
            <div>
              <p>• 热榜数据每日盘中提取4次，收盘后4次，最晚22点提取一次</p>
              <p>• 支持热股、ETF、可转债、行业板块、概念板块、期货、港股、热基、美股等类型</p>
              <p>• 数据包含排行、涨跌幅、当前价格、热度值、标签、上榜解读等信息</p>
              <p>• 可通过日期范围、数据类型等条件进行筛选和统计</p>
            </div>
          }
          type="info"
          showIcon
        />
      </Card>
    </Card>
  );
};

export default ThsHotStats; 