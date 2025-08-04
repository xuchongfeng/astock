import React, { useState, useEffect } from 'react';
import {
  Card,
  Table,
  Button,
  Modal,
  Form,
  Input,
  Select,
  message,
  Popconfirm,
  Tabs,
  Row,
  Col,
  Typography,
  Space,
  Tag,
  Tooltip
} from 'antd';
import {
  PlusOutlined,
  EditOutlined,
  DeleteOutlined,
  PlusCircleOutlined,
  MinusCircleOutlined,
  FolderOutlined,
  StockOutlined
} from '@ant-design/icons';
import { snowballApi } from '../api/snowballApi';
import { stockApi } from '../api/stockApi';
import { formatDate, formatCurrency } from '../utils/formatters';

const { Title } = Typography;
const { TabPane } = Tabs;
const { Option } = Select;

const SnowballPage = () => {
  const userId = localStorage.getItem('userId') || 1;
  
  // 分组相关状态
  const [groups, setGroups] = useState([]);
  const [groupLoading, setGroupLoading] = useState(false);
  const [groupModalVisible, setGroupModalVisible] = useState(false);
  const [editingGroup, setEditingGroup] = useState(null);
  const [groupForm] = Form.useForm();
  
  // 分组内股票相关状态
  const [selectedGroup, setSelectedGroup] = useState(null);
  const [groupStocks, setGroupStocks] = useState([]);
  const [stockLoading, setStockLoading] = useState(false);
  const [stockModalVisible, setStockModalVisible] = useState(false);
  const [stockForm] = Form.useForm();
  
  // 股票搜索相关状态
  const [stockOptions, setStockOptions] = useState([]);
  const [stockSearchLoading, setStockSearchLoading] = useState(false);
  


  useEffect(() => {
    fetchGroups();
  }, [userId]);

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

  // 获取分组列表
  const fetchGroups = async () => {
    setGroupLoading(true);
    try {
      const response = await snowballApi.getGroups();
      const data = response.data.data.stocks || [];
      setGroups(data);
      
      // 如果有分组，默认选择第一个
      if (data.length > 0 && !selectedGroup) {
        setSelectedGroup(data[0]);
        fetchGroupStocks(data[0].id);
      }
    } catch (error) {
      console.error('获取分组失败:', error);
      message.error('获取分组失败');
    } finally {
      setGroupLoading(false);
    }
  };

  // 获取分组内股票
  const fetchGroupStocks = async (groupId) => {
    if (!groupId) return;
    
    setStockLoading(true);
    try {
      const response = await snowballApi.getGroupStocks(groupId);
      console.log(response.data.data.stocks)
      const data = response.data.data.stocks || [];
      console.log(data);
      setGroupStocks(data);
    } catch (error) {
      console.error('获取分组股票失败:', error);
      message.error('获取分组股票失败');
    } finally {
      setStockLoading(false);
    }
  };

  // 分组相关操作
  const handleGroupAdd = () => {
    setEditingGroup(null);
    groupForm.resetFields();
    setGroupModalVisible(true);
  };

  const handleGroupEdit = (record) => {
    setEditingGroup(record);
    groupForm.setFieldsValue({
      name: record.name,
      description: record.description
    });
    setGroupModalVisible(true);
  };

  const handleGroupDelete = async (id) => {
    try {
      await snowballApi.deleteGroup(id);
      message.success('删除分组成功');
      fetchGroups();
      if (selectedGroup && selectedGroup.id === id) {
        setSelectedGroup(null);
        setGroupStocks([]);
      }
    } catch (error) {
      message.error('删除分组失败');
    }
  };

  const handleGroupOk = async () => {
    try {
      const values = await groupForm.validateFields();
      const payload = {
        ...values
      };
      
      if (editingGroup) {
        await snowballApi.updateGroup(editingGroup.id, payload);
        message.success('更新分组成功');
      } else {
        await snowballApi.createGroup(payload);
        message.success('创建分组成功');
      }
      setGroupModalVisible(false);
      fetchGroups();
    } catch (error) {
      message.error('操作失败');
    }
  };

  // 分组内股票相关操作
  const handleStockAdd = () => {
    stockForm.resetFields();
    setStockModalVisible(true);
  };

  const handleStockDelete = async (stockId) => {
    try {
      await snowballApi.removeStockFromGroup(selectedGroup.id, stockId);
      message.success('移除股票成功');
      fetchGroupStocks(selectedGroup.id);
    } catch (error) {
      message.error('移除股票失败');
    }
  };

  const handleStockOk = async () => {
    try {
      const values = await stockForm.validateFields();
      const payload = {
        stock_code: values.ts_code,
        group_name: selectedGroup.name,
        note: values.note || ''
      };
      
      await snowballApi.addStockToGroup(selectedGroup.id, payload);
      message.success('添加股票成功');
      setStockModalVisible(false);
      fetchGroupStocks(selectedGroup.id);
    } catch (error) {
      message.error('添加股票失败');
    }
  };

  // 选择分组
  const handleGroupSelect = (group) => {
    setSelectedGroup(group);
    fetchGroupStocks(group.id);
  };



  // 分组表格列定义
  const groupColumns = [
    {
      title: '分组名称',
      dataIndex: 'name',
      key: 'name',
      width: 200,
      render: (text, record) => (
        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <FolderOutlined style={{ color: '#1890ff' }} />
          <span style={{ fontWeight: 'bold' }}>{text}</span>
          {selectedGroup && selectedGroup.id === record.id && (
            <Tag color="blue">当前</Tag>
          )}
        </div>
      )
    },
    {
      title: '描述',
      dataIndex: 'description',
      key: 'description',
      ellipsis: true
    },
    {
      title: '股票数量',
      key: 'stock_count',
      width: 100,
      align: 'center',
      render: (_, record) => record.stock_count || 0
    },
    {
      title: '创建时间',
      dataIndex: 'created_at',
      key: 'created_at',
      width: 120,
      render: value => formatDate(value, 'YYYY-MM-DD')
    },
    {
      title: '操作',
      key: 'action',
      width: 150,
      render: (_, record) => (
        <Space>
          <Button 
            type="text" 
            icon={<EditOutlined />} 
            onClick={() => handleGroupEdit(record)}
          />
          <Popconfirm title="确定删除此分组？" onConfirm={() => handleGroupDelete(record.id)}>
            <Button type="text" danger icon={<DeleteOutlined />} />
          </Popconfirm>
        </Space>
      )
    }
  ];

  // 分组内股票表格列定义
  const stockColumns = [
    {
      title: '股票代码',
      dataIndex: 'symbol',
      key: 'symbol',
      width: 120,
      render: text => <span style={{ fontWeight: 'bold' }}>{text}</span>
    },
    {
      title: '股票名称',
      dataIndex: 'name',
      key: 'name',
      width: 140,
      render: (_, record) => record.name || ''
    },
    {
      title: '当前价格',
      key: 'current_price',
      width: 120,
      align: 'right',
      render: (_, record) => {
        const currentPrice = record.latest_price?.close || record.avg_price || '-';
        return currentPrice !== '-' ? formatCurrency(currentPrice) : currentPrice;
      }
    },
    {
      title: '涨跌幅',
      key: 'pct_chg',
      width: 100,
      align: 'right',
      render: (_, record) => {
        const pctChg = record.pct_chg;
        if (pctChg === undefined || pctChg === null) return '-';
        const color = pctChg >= 0 ? '#cf1322' : '#389e0d';
        const sign = pctChg >= 0 ? '+' : '';
        return <span style={{ color, fontWeight: 'bold' }}>{sign}{pctChg.toFixed(2)}%</span>;
      }
    },
    {
      title: '备注',
      dataIndex: 'note',
      key: 'note',
      ellipsis: true
    },
    {
      title: '添加时间',
      dataIndex: 'created_at',
      key: 'created_at',
      width: 120,
      render: value => formatDate(value, 'YYYY-MM-DD')
    },
    {
      title: '操作',
      key: 'action',
      width: 100,
      render: (_, record) => (
        <Space>
          <Popconfirm title="确定移除此股票？" onConfirm={() => handleStockDelete(record.id)}>
            <Button type="text" danger icon={<MinusCircleOutlined />} />
          </Popconfirm>
        </Space>
      )
    }
  ];

  return (
    <div style={{ padding: 24 }}>
      <Card>
        <Title level={4} style={{ marginBottom: 24 }}>
          <StockOutlined style={{ marginRight: 8 }} />
          我的雪球
        </Title>

        <Row gutter={24}>
          {/* 左侧分组列表 */}
          <Col span={8}>
            <Card 
              title="股票分组" 
              extra={
                <Button type="primary" icon={<PlusOutlined />} onClick={handleGroupAdd}>
                  创建分组
                </Button>
              }
            >
              <Table
                columns={groupColumns}
                dataSource={groups}
                rowKey="id"
                loading={groupLoading}
                pagination={false}
                size="small"
                onRow={(record) => ({
                  onClick: () => handleGroupSelect(record),
                  style: {
                    cursor: 'pointer',
                    backgroundColor: selectedGroup && selectedGroup.id === record.id ? '#f0f8ff' : 'transparent'
                  }
                })}
              />
            </Card>
          </Col>

          {/* 右侧分组内股票 */}
          <Col span={16}>
            {selectedGroup ? (
              <Card 
                title={
                  <span>
                    <FolderOutlined style={{ marginRight: 8 }} />
                    {selectedGroup.name}
                  </span>
                }
                extra={
                  <Button type="primary" icon={<PlusCircleOutlined />} onClick={handleStockAdd}>
                    添加股票
                  </Button>
                }
              >
                <Table
                  columns={stockColumns}
                  dataSource={groupStocks}
                  rowKey="id"
                  loading={stockLoading}
                  pagination={{ pageSize: 10 }}
                  scroll={{ x: 'max-content' }}
                />
              </Card>
            ) : (
              <Card>
                <div style={{ textAlign: 'center', padding: '60px 0', color: '#8c8c8c' }}>
                  <FolderOutlined style={{ fontSize: 48, marginBottom: 16 }} />
                  <div>请选择一个分组查看股票</div>
                </div>
              </Card>
            )}
          </Col>
        </Row>
      </Card>

      {/* 分组编辑模态框 */}
      <Modal
        title={editingGroup ? '编辑分组' : '创建分组'}
        open={groupModalVisible}
        onOk={handleGroupOk}
        onCancel={() => setGroupModalVisible(false)}
        destroyOnClose
      >
        <Form form={groupForm} layout="vertical">
          <Form.Item 
            name="name" 
            label="分组名称" 
            rules={[{ required: true, message: '请输入分组名称' }]}
          >
            <Input placeholder="请输入分组名称" />
          </Form.Item>
          <Form.Item name="description" label="分组描述">
            <Input.TextArea rows={3} placeholder="请输入分组描述（可选）" />
          </Form.Item>
        </Form>
      </Modal>

      {/* 添加股票模态框 */}
      <Modal
        title="添加股票到分组"
        open={stockModalVisible}
        onOk={handleStockOk}
        onCancel={() => setStockModalVisible(false)}
        destroyOnClose
      >
        <Form form={stockForm} layout="vertical">
          <Form.Item 
            name="ts_code" 
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
            />
          </Form.Item>
          <Form.Item name="note" label="备注">
            <Input.TextArea rows={3} placeholder="请输入备注（可选）" />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default SnowballPage; 