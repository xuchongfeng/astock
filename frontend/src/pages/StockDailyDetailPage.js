import React, { useState, useEffect } from 'react';
import {
  Card, Row, Col, Form, Input, Button, DatePicker, Select,
  Spin, Statistic, Tabs, message, Radio, Space, Alert
} from 'antd';
import {
  StockOutlined, TableOutlined, DownloadOutlined,
  SearchOutlined, SortAscendingOutlined, SortDescendingOutlined
} from '@ant-design/icons';
import moment from 'moment';
import StockDailyDetailTable from '../components/StockDailyDetailTable';
import { stockDailyApi } from '../api/stockDailyApi';
import { stockApi } from '../api/stockApi';
import { formatDate, formatCurrency } from '../utils/formatters';

const { TabPane } = Tabs;
const { Option } = Select;

const StockDailyDetailPage = () => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState([]);
  const [pagination, setPagination] = useState({
    current: 1,
    pageSize: 50,
    total: 0
  });
  const [sortConfig, setSortConfig] = useState({
    field: 'amount',
    order: 'descend'
  });
  const [selectedDate, setSelectedDate] = useState(moment());
  const [marketStats, setMarketStats] = useState(null);
  
  // 股票搜索相关状态
  const [stockOptions, setStockOptions] = useState([]);
  const [stockSearchLoading, setStockSearchLoading] = useState(false);

  // 初始化表单值
  const [formValues, setFormValues] = useState({
    tsCode: '',
    date: moment()
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
      const stocks = response.data.data || [];
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

  // 获取每日数据
  useEffect(() => {
    fetchDailyData();
  }, [formValues, pagination.current, sortConfig]);

  const fetchDailyData = async () => {
    setLoading(true);
    try {
      const response = await stockDailyApi.getDailyData(
        formValues.tsCode,
        formatDate(formValues.date, 'YYYY-MM-DD'),
        null,
        null,
        pagination.current,
        pagination.pageSize,
        sortConfig.order === 'ascend' ? sortConfig.field : "-" + sortConfig.field,
      );

      setData(response.data);
      setPagination({
        ...pagination,
        total: response.total
      });

      // 如果是全市场数据，计算市场统计
      if (!formValues.tsCode) {
        calculateMarketStats(response.data);
      }
    } catch (error) {
      console.error('获取每日数据失败:', error);
      message.error('获取数据失败');
    } finally {
      setLoading(false);
    }
  };

  const calculateMarketStats = (dailyData) => {
    if (!dailyData || dailyData.length === 0) {
      setMarketStats(null);
      return;
    }

    // 计算市场统计数据
    const totalVolume = dailyData.reduce((sum, item) => sum + item.vol, 0);
    const totalAmount = dailyData.reduce((sum, item) => sum + item.amount, 0);
    const upCount = dailyData.filter(item => item.pct_chg > 0).length;
    const downCount = dailyData.filter(item => item.pct_chg < 0).length;
    const flatCount = dailyData.filter(item => item.pct_chg === 0).length;

    setMarketStats({
      totalVolume,
      totalAmount,
      upCount,
      downCount,
      flatCount,
      companyCount: dailyData.length
    });
  };

  const handleSearch = (values) => {
    setFormValues({
      ...values,
      date: values.date || formValues.date
    });
    setPagination({
      ...pagination,
      current: 1
    });
  };

  const handleTableChange = (pagination, filters, sorter) => {
    setPagination(pagination);

    // 处理排序
    if (sorter.field) {
      setSortConfig({
        field: sorter.field,
        order: sorter.order
      });
    }
  };

  const handleExport = async () => {
    setLoading(true);
    try {
      const blob = await stockDailyApi.exportDailyData(
        formValues.tsCode,
        formatDate(formValues.date, 'YYYY-MM-DD')
      );

      // 创建下载链接
      const url = window.URL.createObjectURL(new Blob([blob]));
      const link = document.createElement('a');
      link.href = url;

      // 设置文件名
      const fileName = formValues.tsCode
        ? `${formValues.tsCode}_${formatDate(formValues.date, 'YYYYMMDD')}.csv`
        : `market_data_${formatDate(formValues.date, 'YYYYMMDD')}.csv`;

      link.setAttribute('download', fileName);
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

  const handleSortChange = (field) => {
    setSortConfig({
      field,
      order: sortConfig.order === 'ascend' ? 'descend' : 'ascend'
    });
  };

  const handleDateChange = (date) => {
    setSelectedDate(date);
    form.setFieldsValue({ date });
  };

  return (
    <div style={{ padding: 24 }}>
      <Card
        title="股票每日交易数据明细"
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
            name="date"
            label="交易日期"
            rules={[{ required: true, message: '请选择交易日期' }]}
          >
            <DatePicker
              value={selectedDate}
              onChange={handleDateChange}
              disabledDate={current => current && current > moment().endOf('day')}
              style={{ width: 180 }}
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

        {!formValues.tsCode && marketStats && (
          <div style={{ marginBottom: 24 }}>
            <Alert
              message={`${formatDate(formValues.date, 'YYYY-MM-DD')} 市场概况`}
              type="info"
              showIcon
              style={{ marginBottom: 16 }}
            />
            <Row gutter={16}>
              <Col span={6}>
                <Card bordered={false}>
                  <Statistic
                    title="公司数量"
                    value={marketStats.companyCount}
                    suffix="家"
                  />
                </Card>
              </Col>
              <Col span={6}>
                <Card bordered={false}>
                  <Statistic
                    title="总成交量"
                    value={(marketStats.totalVolume / 10000).toFixed(2)}
                    suffix="万手"
                  />
                </Card>
              </Col>
              <Col span={6}>
                <Card bordered={false}>
                  <Statistic
                    title="总成交额"
                    value={formatCurrency(marketStats.totalAmount)}
                  />
                </Card>
              </Col>
              <Col span={6}>
                <Card bordered={false}>
                  <Statistic
                    title="涨跌分布"
                    value={`${marketStats.upCount}↑ ${marketStats.flatCount}→ ${marketStats.downCount}↓`}
                  />
                </Card>
              </Col>
            </Row>
          </div>
        )}

        <div style={{ marginBottom: 16 }}>
          <Space>
            <span style={{ fontWeight: 'bold' }}>排序方式:</span>
            <Radio.Group
              value={sortConfig.field}
              onChange={e => handleSortChange(e.target.value)}
              buttonStyle="solid"
            >
              <Radio.Button value="vol">
                {sortConfig.field === 'vol' && (
                  sortConfig.order === 'ascend' ?
                  <SortAscendingOutlined /> :
                  <SortDescendingOutlined />
                )}
                成交量
              </Radio.Button>
              <Radio.Button value="amount">
                {sortConfig.field === 'amount' && (
                  sortConfig.order === 'ascend' ?
                  <SortAscendingOutlined /> :
                  <SortDescendingOutlined />
                )}
                成交额
              </Radio.Button>
              <Radio.Button value="pct_chg">
                {sortConfig.field === 'pct_chg' && (
                  sortConfig.order === 'ascend' ?
                  <SortAscendingOutlined /> :
                  <SortDescendingOutlined />
                )}
                涨跌幅
              </Radio.Button>
              <Radio.Button value="trade_date">
                {sortConfig.field === 'trade_date' && (
                  sortConfig.order === 'ascend' ?
                  <SortAscendingOutlined /> :
                  <SortDescendingOutlined />
                )}
                交易日期
              </Radio.Button>
            </Radio.Group>

            <Button
              type={sortConfig.order === 'ascend' ? 'primary' : 'default'}
              onClick={() => setSortConfig({
                ...sortConfig,
                order: sortConfig.order === 'ascend' ? 'descend' : 'ascend'
              })}
            >
              {sortConfig.order === 'ascend' ?
                <SortAscendingOutlined /> :
                <SortDescendingOutlined />
              }
              {sortConfig.order === 'ascend' ? '升序' : '降序'}
            </Button>
          </Space>
        </div>

        <Tabs
          type="card"
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
                <TableOutlined />
                交易明细
              </span>
            }
            key="table"
          >
            <StockDailyDetailTable
              data={data}
              loading={loading}
              pagination={pagination}
              onChange={handleTableChange}
              sortConfig={sortConfig}
            />
          </TabPane>
        </Tabs>
      </Card>
    </div>
  );
};

export default StockDailyDetailPage;