import React, { useEffect, useState } from 'react';
import { Table, Card, Input, DatePicker, Button, Form, message } from 'antd';
import { thsIndexApi } from '../api/thsIndexApi';
import moment from 'moment';

const ThsIndexPage = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [pagination, setPagination] = useState({ current: 1, pageSize: 20, total: 0 });
  const [form] = Form.useForm();

  const fetchData = async (params = {}) => {
    setLoading(true);
    try {
      const res = await thsIndexApi.getList({
        page: params.page || pagination.current,
        page_size: params.pageSize || pagination.pageSize,
        ...params.filters
      });
      setData(res.data.data);
      setPagination({
        current: params.page || pagination.current,
        pageSize: params.pageSize || pagination.pageSize,
        total: res.data.total
      });
    } catch (e) {
      message.error('加载数据失败');
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchData({ page: 1 });
    // eslint-disable-next-line
  }, []);

  const handleTableChange = (pag, filters, sorter) => {
    fetchData({
      page: pag.current,
      pageSize: pag.pageSize,
      filters: form.getFieldsValue(),
      sortField: sorter.field,
      sortOrder: sorter.order
    });
  };

  const handleSearch = () => {
    fetchData({ page: 1, filters: form.getFieldsValue() });
  };

  const columns = [
    { title: 'TS指数代码', dataIndex: 'ts_code', key: 'ts_code', width: 120 },
    { title: '交易日', dataIndex: 'trade_date', key: 'trade_date', width: 110 },
    { title: '收盘点位', dataIndex: 'close', key: 'close', align: 'right' },
    { title: '开盘点位', dataIndex: 'open', key: 'open', align: 'right' },
    { title: '最高点位', dataIndex: 'high', key: 'high', align: 'right' },
    { title: '最低点位', dataIndex: 'low', key: 'low', align: 'right' },
    { title: '昨日收盘点', dataIndex: 'pre_close', key: 'pre_close', align: 'right' },
    { title: '平均价', dataIndex: 'avg_price', key: 'avg_price', align: 'right' },
    { title: '涨跌点位', dataIndex: 'change', key: 'change', align: 'right' },
    { title: '涨跌幅', dataIndex: 'pct_change', key: 'pct_change', align: 'right' },
    { title: '成交量', dataIndex: 'vol', key: 'vol', align: 'right' },
    { title: '换手率', dataIndex: 'turnover_rate', key: 'turnover_rate', align: 'right' },
    { title: '总市值', dataIndex: 'total_mv', key: 'total_mv', align: 'right' },
    { title: '流通市值', dataIndex: 'float_mv', key: 'float_mv', align: 'right' },
    { title: '创建时间', dataIndex: 'created_at', key: 'created_at', width: 120 },
    { title: '更新时间', dataIndex: 'updated_at', key: 'updated_at', width: 120 },
  ];

  return (
    <div style={{ padding: 24 }}>
      <Card title="同花顺指数行情">
        <Form form={form} layout="inline" style={{ marginBottom: 16 }}>
          <Form.Item name="ts_code" label="TS指数代码">
            <Input placeholder="如 885001.TI" style={{ width: 160 }} />
          </Form.Item>
          <Form.Item name="trade_date" label="交易日">
            <DatePicker style={{ width: 140 }} />
          </Form.Item>
          <Form.Item>
            <Button type="primary" onClick={handleSearch}>查询</Button>
          </Form.Item>
        </Form>
        <Table
          columns={columns}
          dataSource={data}
          rowKey={record => `${record.ts_code}-${record.trade_date}`}
          loading={loading}
          pagination={pagination}
          onChange={handleTableChange}
          scroll={{ x: 'max-content' }}
          bordered
        />
      </Card>
    </div>
  );
};

export default ThsIndexPage; 