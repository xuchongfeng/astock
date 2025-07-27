import React, { useState, useEffect } from 'react';
import {
  Card, Row, Col, Form, Input, Button, DatePicker, Select,
  Spin, Statistic, Tabs, message
} from 'antd';
import {
  StockOutlined, LineChartOutlined, TableOutlined,
  DownloadOutlined, SearchOutlined
} from '@ant-design/icons';
import moment from 'moment';
import StockDailyTable from '../components/StockDailyTable';
import StockDailyChart from '../components/StockDailyChart';
import { stockDailyApi } from '../api/stockDailyApi';
import { stockApi } from '../api/stockApi';
import { formatDate, formatCurrency } from '../utils/formatters';

const { RangePicker } = DatePicker;
const { TabPane } = Tabs;
const { Option } = Select;

const StockDailyPage = () => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState([]);
  const [latestData, setLatestData] = useState(null);
  const [pagination, setPagination] = useState({
    current: 1,
    pageSize: 20,
    total: 0
  });
  const [activeTab, setActiveTab] = useState('chart');
  
  // 股票搜索相关状态
  const [stockOptions, setStockOptions] = useState([]);
  const [stockSearchLoading, setStockSearchLoading] = useState(false);

  // 初始化表单值
  const [formValues, setFormValues] = useState({
    tsCode: '000001.SH',
    dateRange: [
      moment().subtract(3, 'months'),
      moment()
    ]
  });

  // 搜索股票
  const handleStockSearch = async (value) => {
    if (!value || value.length < 2) {
      setStockOptions([]);
      return;
    }
    
    setStockSearchLoading(true);
    try {
      const response = await stockApi.getCompanies({ search: value, page_size: 20 });
      const stocks = response.data || [];
      const options = stocks.map(stock => ({
        value: stock.ts_code,
        label: `${stock.ts_code} - ${stock.name}`
      }));
      setStockOptions(options);
    } catch (error) {
      console.error('搜索股票失败:', error);
      setStockOptions([]);
    } finally {
      setStockSearchLoading(false);
    }
  };

  // 获取最新数据
  useEffect(() => {
    fetchLatestData();
  }, [formValues.tsCode]);

  // 获取每日数据
  useEffect(() => {
    fetchDailyData();
  }, [formValues, pagination.current]);

  const fetchLatestData = async () => {
    try {
      const response = await stockDailyApi.getLatestData(formValues.tsCode);
      setLatestData(response);
    } catch (error) {
      console.error('获取最新数据失败:', error);
    }
  };

  const fetchDailyData = async () => {
    setLoading(true);
    try {
      const [start, end] = formValues.dateRange;
      const response = await stockDailyApi.getDailyData(
        formValues.tsCode,
        formatDate(start, 'YYYY-MM-DD'),
        formatDate(end, 'YYYY-MM-DD'),
        pagination.current,
        pagination.pageSize
      );

      setData(response.data);
      setPagination({
        ...pagination,
        total: response.total
      });
    } catch (error) {
      console.error('获取每日数据失败:', error);
      message.error('获取数据失败');
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (values) => {
    setFormValues({
      ...values,
      dateRange: values.dateRange || formValues.dateRange
    });
    setPagination({
      ...pagination,
      current: 1
    });
  };

  const handleTableChange = (pagination) => {
    setPagination(pagination);
  };

  const handleExport = async () => {
    setLoading(true);
    try {
      const [start, end] = formValues.dateRange;
      const blob = await stockDailyApi.exportDailyData(
        formValues.tsCode,
        formatDate(start, 'YYYY-MM-DD'),
        formatDate(end, 'YYYY-MM-DD')
      );

      // 创建下载链接
      const url = window.URL.createObjectURL(new Blob([blob]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `${formValues.tsCode}_${moment().format('YYYYMMDD')}.csv`);
      document.body.appendChild(link);
      link.click();
      link.remove();

      message.success('导出成功');
    } catch (error) {
      console.error('导出失败:', error);
      message.error('导出失败');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: 24 }}>
      <Card
        title="股票每日数据查询"
        extra={
          <Button
            type="primary"
            icon={<DownloadOutlined />}
            onClick={handleExport}
            loading={loading}
          >
            导出数据
          </Button>
        }
      >
        <Form
          form={form}
          layout="inline"
          initialValues={formValues}
          onFinish={handleSearch}
          style={{ marginBottom: 24 }}
        >
          <Form.Item
            name="tsCode"
            label="股票代码"
            rules={[{ required: true, message: '请选择股票' }]}
          >
            <Select
              showSearch
              placeholder="搜索股票代码或名称"
              filterOption={false}
              onSearch={handleStockSearch}
              loading={stockSearchLoading}
              options={stockOptions}
              allowClear
              style={{ width: 250 }}
            />
          </Form.Item>

          <Form.Item
            name="dateRange"
            label="日期范围"
            rules={[{ required: true, message: '请选择日期范围' }]}
          >
            <RangePicker
              disabledDate={current => current && current > moment().endOf('day')}
              style={{ width: 300 }}
            />
          </Form.Item>

          <Form.Item>
            <Button
              type="primary"
              htmlType="submit"
              icon={<SearchOutlined />}
              loading={loading}
            >
              查询
            </Button>
          </Form.Item>
        </Form>

        {latestData && (
          <Row gutter={16} style={{ marginBottom: 24 }}>
            <Col span={6}>
              <Card bordered={false}>
                <Statistic
                  title="最新收盘价"
                  value={formatCurrency(latestData.close)}
                  valueStyle={{ color: '#1890ff' }}
                />
              </Card>
            </Col>
            <Col span={6}>
              <Card bordered={false}>
                <Statistic
                  title="涨跌幅"
                  value={latestData.pct_chg}
                  precision={2}
                  suffix="%"
                  valueStyle={{
                    color: latestData.pct_chg > 0 ? '#cf1322' : '#389e0d'
                  }}
                />
              </Card>
            </Col>
            <Col span={6}>
              <Card bordered={false}>
                <Statistic
                  title="成交量"
                  value={(latestData.vol / 100).toFixed(2)}
                  suffix="万手"
                />
              </Card>
            </Col>
            <Col span={6}>
              <Card bordered={false}>
                <Statistic
                  title="成交额"
                  value={formatCurrency(latestData.amount)}
                />
              </Card>
            </Col>
          </Row>
        )}

        <Tabs
          activeKey={activeTab}
          onChange={setActiveTab}
          tabBarExtraContent={
            <div style={{ display: 'flex', gap: 8 }}>
              <span style={{ lineHeight: '32px', color: '#8c8c8c' }}>
                共 {pagination.total} 条记录
              </span>
            </div>
          }
        >
          <TabPane
            tab={
              <span>
                <LineChartOutlined />
                K线图表
              </span>
            }
            key="chart"
          >
            <Spin spinning={loading}>
              <StockDailyChart data={data} loading={loading} />
            </Spin>
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
            <StockDailyTable
              data={data}
              loading={loading}
              pagination={pagination}
              onChange={handleTableChange}
            />
          </TabPane>
        </Tabs>
      </Card>
    </div>
  );
};

export default StockDailyPage;