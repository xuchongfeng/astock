import React, { useEffect, useState } from 'react';
import { Table, Button, Modal, Form, Input, DatePicker, Select, message, Popconfirm, Card } from 'antd';
import { strategyApi } from '../api/strategyApi';
import moment from 'moment';
import { formatDate, formatCurrency } from '../utils/formatters';
import KLineChart from '../components/KLineChart';
import { StarFilled, StarOutlined } from '@ant-design/icons';
import { watchlistApi } from '../api/watchlistApi';

const StrategyStockPage = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [strategies, setStrategies] = useState([]);
  const [modalVisible, setModalVisible] = useState(false);
  const [editing, setEditing] = useState(null);
  const [form] = Form.useForm();
  const [filterStrategyId, setFilterStrategyId] = useState();
  const [filterDate, setFilterDate] = useState();
  const [pagination, setPagination] = useState({ current: 1, pageSize: 20, total: 0 });
  const [sorter, setSorter] = useState({});
  const [watchlistStatus, setWatchlistStatus] = useState({}); // { ts_code: true/false }
  const [watchlistLoading, setWatchlistLoading] = useState({}); // { ts_code: true/false }
  const userId = localStorage.getItem('userId');

  const fetchStrategies = async () => {
    try {
      const res = await strategyApi.getStrategies();
      setStrategies(res.data.data);
    } catch {}
  };

  const fetchData = async (strategy_id, page = pagination.current, pageSize = pagination.pageSize, sortField = sorter.field, sortOrder = sorter.order, date = filterDate) => {
    setLoading(true);
    try {
      const params = { page, page_size: pageSize };
      if (strategy_id) params.strategy_id = strategy_id;
      if (date) params.date = date.format('YYYY-MM-DD');
      if (sortField) {
        params.sort_field = sortOrder === 'descend' ? `-${sortField}` : sortField;
      }
      const res = await strategyApi.getStrategyStocks(params);
      setData(res.data.data);
      setPagination({
        current: page,
        pageSize,
        total: res.data.total || 0
      });
    } catch {
      message.error('加载数据失败');
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchStrategies();
    fetchData();
  }, []);

  React.useEffect(() => {
    if (data && data.length && userId) {
      const fetchStatuses = async () => {
        const statusObj = {};
        await Promise.all(data.map(async (row) => {
          if (!row.ts_code) return;
          try {
            statusObj[row.ts_code] = await watchlistApi.isInWatchlist(userId, row.ts_code);
          } catch {
            statusObj[row.ts_code] = false;
          }
        }));
        setWatchlistStatus(statusObj);
      };
      fetchStatuses();
    }
  }, [data, userId]);

  const handleAdd = () => {
    setEditing(null);
    form.resetFields();
    setModalVisible(true);
  };

  const handleEdit = (record) => {
    setEditing(record);
    form.setFieldsValue({
      ...record,
      date: record.date ? moment(record.date) : null,
    });
    setModalVisible(true);
  };

  const handleDelete = async (id) => {
    try {
      await strategyApi.deleteStrategyStock(id);
      message.success('删除成功');
      fetchData(filterStrategyId);
    } catch {
      message.error('删除失败');
    }
  };

  const handleOk = async () => {
    try {
      const values = await form.validateFields();
      const payload = {
        ...values,
        date: values.date ? values.date.format('YYYY-MM-DD') : undefined,
      };
      if (editing) {
        // 通常不支持编辑主键，略过
      } else {
        await strategyApi.addStrategyStock(payload);
        message.success('新增成功');
      }
      setModalVisible(false);
      fetchData(filterStrategyId);
    } catch {}
  };

  const handleStrategyFilter = (strategy_id) => {
    setFilterStrategyId(strategy_id);
    fetchData(strategy_id, 1, pagination.pageSize, sorter.field, sorter.order, filterDate);
  };

  const handleDateFilter = (date) => {
    setFilterDate(date);
    fetchData(filterStrategyId, 1, pagination.pageSize, sorter.field, sorter.order, date);
  };

  const handleClearFilters = () => {
    setFilterStrategyId(undefined);
    setFilterDate(undefined);
    fetchData(undefined, 1, pagination.pageSize, sorter.field, sorter.order, undefined);
  };

  const handleTableChange = (pag, filters, sorterObj) => {
    setSorter({ field: sorterObj.field, order: sorterObj.order });
    fetchData(filterStrategyId, pag.current, pag.pageSize, sorterObj.field, sorterObj.order, filterDate);
  };

  const handleToggleWatchlist = async (ts_code) => {
    if (!userId) {
      message.warning('请先登录');
      return;
    }
    setWatchlistLoading((prev) => ({ ...prev, [ts_code]: true }));
    try {
      if (watchlistStatus[ts_code]) {
        await watchlistApi.removeFromWatchlist(userId, ts_code);
        setWatchlistStatus((prev) => ({ ...prev, [ts_code]: false }));
        message.success('已取消收藏');
      } else {
        await watchlistApi.addToWatchlist(userId, ts_code);
        setWatchlistStatus((prev) => ({ ...prev, [ts_code]: true }));
        message.success('已收藏');
      }
    } catch (error) {
      message.error('操作失败');
    } finally {
      setWatchlistLoading((prev) => ({ ...prev, [ts_code]: false }));
    }
  };

  const columns = [
    { title: '策略ID', dataIndex: 'strategy_id', key: 'strategy_id', width: 80 },
    {
      title: '股票代码',
      dataIndex: 'ts_code',
      key: 'ts_code',
      width: 180,
      render: (text, record) => (
        <span style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          {text}
          <span>
            <span style={{ color: watchlistStatus[record.ts_code] ? '#faad14' : '#aaa', marginRight: 4 }}>
              {watchlistStatus[record.ts_code] ? '已收藏' : '未收藏'}
            </span>
            <span>
              <a onClick={() => handleToggleWatchlist(record.ts_code)} style={{ fontSize: 18 }}>
                {watchlistStatus[record.ts_code] ? <StarFilled style={{ color: '#faad14' }} /> : <StarOutlined />}
              </a>
            </span>
          </span>
        </span>
      )
    },
    { title: '股票名称', key: 'stock_name', width: 140, render: (_, record) => record.stock_info?.name || '' },
    { title: '评级', dataIndex: 'rating', key: 'rating', width: 80, sorter: true },
    { title: '5日均额', dataIndex: 'avg_amount_5d', key: 'avg_amount_5d', width: 120, render: val => val ? formatCurrency(val) : '-', sorter: true },
    { title: '关联日期', dataIndex: 'date', key: 'date', width: 140, render: val => val ? formatDate(val, 'YYYY-MM-DD') : '' },
    {
      title: '操作',
      key: 'action',
      render: (_, record) => (
        <Popconfirm title="确定删除？" onConfirm={() => handleDelete(record.id)}>
          <Button type="link" danger>删除</Button>
        </Popconfirm>
      ),
    },
  ];

  return (
    <div style={{ padding: 24 }}>
      <Card title="策略关联股票管理">
        <div style={{ marginBottom: 16 }}>
          <Select
            allowClear
            placeholder="筛选策略"
            style={{ width: 200, marginRight: 8 }}
            value={filterStrategyId}
            onChange={handleStrategyFilter}
          >
            {strategies.map(s => (
              <Select.Option key={s.id} value={s.id}>{s.name}</Select.Option>
            ))}
          </Select>
          <DatePicker
            placeholder="筛选关联日期"
            style={{ width: 200, marginRight: 8 }}
            value={filterDate}
            onChange={handleDateFilter}
            allowClear
          />
          <Button onClick={handleClearFilters} style={{ marginRight: 8 }}>清除筛选</Button>
          <Button type="primary" onClick={handleAdd}>新增关联</Button>
        </div>
        <Table
          columns={columns}
          dataSource={data}
          rowKey="id"
          loading={loading}
          bordered
          pagination={pagination}
          onChange={handleTableChange}
          expandable={{
            expandedRowRender: record => record.ts_code ? <KLineChart tsCode={record.ts_code} /> : null,
            rowExpandable: record => !!record.ts_code,
          }}
        />
        <Modal
          title={editing ? '编辑关联' : '新增关联'}
          open={modalVisible}
          onOk={handleOk}
          onCancel={() => setModalVisible(false)}
          destroyOnClose
        >
          <Form form={form} layout="vertical">
            <Form.Item name="strategy_id" label="策略" rules={[{ required: true, message: '请选择策略' }]}> 
              <Select placeholder="请选择策略">
                {strategies.map(s => (
                  <Select.Option key={s.id} value={s.id}>{s.name}</Select.Option>
                ))}
              </Select>
            </Form.Item>
            <Form.Item name="ts_code" label="股票代码" rules={[{ required: true, message: '请输入股票代码' }]}> 
              <Input />
            </Form.Item>
            <Form.Item name="date" label="关联日期"> 
              <DatePicker style={{ width: '100%' }} />
            </Form.Item>
          </Form>
        </Modal>
      </Card>
    </div>
  );
};

export default StrategyStockPage; 