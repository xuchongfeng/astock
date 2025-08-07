import React, { useEffect, useState } from 'react';
import { Table, Button, Modal, Form, Input, DatePicker, Select, message, Popconfirm, Card, Space, Checkbox, Tabs } from 'antd';
import { strategyApi } from '../api/strategyApi';
import moment from 'moment';
import { formatDate, formatCurrency } from '../utils/formatters';
import KLineChart from '../components/KLineChart';
import { StarFilled, StarOutlined, RobotOutlined, FolderOutlined, MessageOutlined } from '@ant-design/icons';
import { watchlistApi } from '../api/watchlistApi';
import { snowballApi } from '../api/snowballApi';
import { deepseekApi } from '../api/deepseekApi';
import MarkdownRenderer from '../components/MarkdownRenderer';

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
  
  // 雪球分组相关状态
  const [snowballModal, setSnowballModal] = useState({ visible: false, ts_code: '', stock_name: '' });
  const [snowballGroups, setSnowballGroups] = useState([]);
  const [selectedGroups, setSelectedGroups] = useState([]);
  const [snowballLoading, setSnowballLoading] = useState(false);
  
  // DeepSeek分析相关状态
  const [deepseekModal, setDeepseekModal] = useState({ visible: false, ts_code: '', stock_name: '' });
  const [deepseekAnalysis, setDeepseekAnalysis] = useState('');
  const [deepseekLoading, setDeepseekLoading] = useState(false);
  const [deepseekDailyAnalysis, setDeepseekDailyAnalysis] = useState('');
  const [deepseekDailyLoading, setDeepseekDailyLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('basic');
  
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

  // 雪球分组相关处理函数
  const handleAddToSnowball = async (ts_code, stock_name) => {
    if (!userId) {
      message.warning('请先登录');
      return;
    }
    
    setSnowballModal({ visible: true, ts_code, stock_name });
    setSelectedGroups([]);
    
    // 获取雪球分组列表
    try {
      setSnowballLoading(true);
      const response = await snowballApi.getGroups();
      const groups = response.data.data.stocks || [];
      setSnowballGroups(groups);
    } catch (error) {
      console.error('获取雪球分组失败:', error);
      message.error('获取分组列表失败');
    } finally {
      setSnowballLoading(false);
    }
  };

  const handleSnowballOk = async () => {
    if (selectedGroups.length === 0) {
      message.warning('请至少选择一个分组');
      return;
    }

    try {
      setSnowballLoading(true);
      
      // 批量添加到选中的分组
      const promises = selectedGroups.map(groupId => {
        const group = snowballGroups.find(g => g.id === groupId);
        return snowballApi.addStockToGroup(groupId, {
          stock_code: snowballModal.ts_code,
          group_name: group.name,
          note: `从策略股票页面添加`
        });
      });

      await Promise.all(promises);
      message.success(`已成功添加到 ${selectedGroups.length} 个分组`);
      setSnowballModal({ visible: false, ts_code: '', stock_name: '' });
      setSelectedGroups([]);
    } catch (error) {
      console.error('添加到雪球分组失败:', error);
      message.error('添加到分组失败');
    } finally {
      setSnowballLoading(false);
    }
  };

  const handleSnowballCancel = () => {
    setSnowballModal({ visible: false, ts_code: '', stock_name: '' });
    setSelectedGroups([]);
  };

  const handleGroupSelectionChange = (checkedValues) => {
    setSelectedGroups(checkedValues);
  };

  // DeepSeek分析相关处理函数
  const handleDeepseekAnalysis = async (ts_code, stock_name) => {
    setDeepseekModal({ visible: true, ts_code, stock_name });
    setDeepseekAnalysis('');
    setDeepseekDailyAnalysis('');
    setActiveTab('basic');
    setDeepseekLoading(true);
    setDeepseekDailyLoading(true);
    
    // 分别获取基础分析和走势分析，任何一个完成都可以展示
    const fetchBasicAnalysis = async () => {
      try {
        const response = await deepseekApi.getStockBasicAnalysis(ts_code);
        const analysis = response.data.analysis || response.analysis || '';
        setDeepseekAnalysis(analysis);
        if (analysis) {
          setActiveTab('basic');
        }
      } catch (error) {
        console.error('获取基础分析失败:', error);
        setDeepseekAnalysis('');
      } finally {
        setDeepseekLoading(false);
      }
    };

    const fetchDailyAnalysis = async () => {
      try {
        const response = await deepseekApi.getStockDailyAnalysis(ts_code);
        const analysis = response.data.analysis || response.analysis || '';
        setDeepseekDailyAnalysis(analysis);
        if (analysis && !deepseekAnalysis) {
          setActiveTab('daily');
        }
      } catch (error) {
        console.error('获取走势分析失败:', error);
        setDeepseekDailyAnalysis('');
      } finally {
        setDeepseekDailyLoading(false);
      }
    };

    // 并行执行两个请求
    Promise.allSettled([fetchBasicAnalysis(), fetchDailyAnalysis()]).then((results) => {
      const hasSuccess = results.some(result => result.status === 'fulfilled');
      if (!hasSuccess) {
        message.error('获取分析报告失败，请稍后重试');
      }
    });
  };

  const handleDeepseekCancel = () => {
    setDeepseekModal({ visible: false, ts_code: '', stock_name: '' });
    setDeepseekAnalysis('');
    setDeepseekDailyAnalysis('');
  };

  const handleTabChange = (key) => {
    setActiveTab(key);
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
    { 
      title: '股票名称', 
      key: 'stock_name', 
      width: 250, 
      render: (_, record) => (
        <Space>
          <span>{record.stock_info?.name || ''}</span>
          <Button
            type="text"
            icon={<RobotOutlined />}
            onClick={() => handleDeepseekAnalysis(record.ts_code, record.stock_info?.name || record.ts_code)}
            size="small"
            title="DeepSeek分析"
          />
          <Button
            type="text"
            icon={<FolderOutlined />}
            onClick={() => handleAddToSnowball(record.ts_code, record.stock_info?.name || record.ts_code)}
            size="small"
            title="收藏到雪球分组"
          />
        </Space>
      )
    },
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
        
        {/* 新增关联模态框 */}
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

        {/* 雪球分组选择模态框 */}
        <Modal
          title={`收藏到雪球分组 - ${snowballModal.stock_name || snowballModal.ts_code}`}
          open={snowballModal.visible}
          onOk={handleSnowballOk}
          onCancel={handleSnowballCancel}
          confirmLoading={snowballLoading}
          destroyOnClose
          width={500}
        >
          <div style={{ marginBottom: 16 }}>
            <p style={{ color: '#666', marginBottom: 16 }}>
              请选择要添加到哪些分组（可多选）：
            </p>
            {snowballLoading ? (
              <div style={{ textAlign: 'center', padding: '20px' }}>
                正在加载分组列表...
              </div>
            ) : (
              <Checkbox.Group
                value={selectedGroups}
                onChange={handleGroupSelectionChange}
                style={{ width: '100%' }}
              >
                <div style={{ maxHeight: '300px', overflowY: 'auto' }}>
                  {snowballGroups.map(group => (
                    <div key={group.id} style={{ marginBottom: 8 }}>
                      <Checkbox value={group.id}>
                        <Space>
                          <FolderOutlined style={{ color: '#1890ff' }} />
                          <span style={{ fontWeight: 'bold' }}>{group.name}</span>
                          {group.description && (
                            <span style={{ color: '#8c8c8c', fontSize: '12px' }}>
                              ({group.description})
                            </span>
                          )}
                        </Space>
                      </Checkbox>
                    </div>
                  ))}
                </div>
              </Checkbox.Group>
            )}
          </div>
        </Modal>

        {/* DeepSeek分析模态框 */}
        <Modal
          title={`DeepSeek分析 - ${deepseekModal.stock_name || deepseekModal.ts_code}`}
          open={deepseekModal.visible}
          onCancel={handleDeepseekCancel}
          footer={null}
          destroyOnClose
          width={900}
          style={{ top: 20 }}
        >
          <Tabs 
            activeKey={activeTab} 
            onChange={handleTabChange}
            type="card"
          >
            <Tabs.TabPane 
              tab="个股分析" 
              key="basic"
            >
              <MarkdownRenderer 
                content={deepseekAnalysis} 
                loading={deepseekLoading}
              />
            </Tabs.TabPane>
            <Tabs.TabPane 
              tab="走势分析" 
              key="daily"
            >
              <MarkdownRenderer 
                content={deepseekDailyAnalysis} 
                loading={deepseekDailyLoading}
              />
            </Tabs.TabPane>
          </Tabs>
        </Modal>
      </Card>
    </div>
  );
};

export default StrategyStockPage; 