import React, { useState, useEffect } from 'react';
import { 
  Card, 
  Table, 
  Button, 
  Modal, 
  Form, 
  Input, 
  DatePicker, 
  Select, 
  message, 
  Popconfirm,
  Tag,
  Space,
  Typography,
  Row,
  Col
} from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined, TagOutlined } from '@ant-design/icons';
import { tagApi } from '../api/tagApi';
import TagSelector from '../components/TagSelector';
import moment from 'moment';

const { Title } = Typography;
const { Option } = Select;
const { RangePicker } = DatePicker;

const StockTagPage = () => {
  const [stockTags, setStockTags] = useState([]);
  const [tags, setTags] = useState([]);
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [editingStockTag, setEditingStockTag] = useState(null);
  const [form] = Form.useForm();
  const userId = localStorage.getItem('userId') || 1;

  useEffect(() => {
    fetchStockTags();
    fetchTags();
  }, []);

  const fetchStockTags = async () => {
    setLoading(true);
    try {
      const response = await tagApi.getUserStockTags(userId);
      setStockTags(response.data.data || []);
    } catch (error) {
      console.error('获取股票标签失败:', error);
      message.error('获取股票标签失败');
    } finally {
      setLoading(false);
    }
  };

  const fetchTags = async () => {
    try {
      const response = await tagApi.getTags();
      setTags(response.data.data || []);
    } catch (error) {
      console.error('获取标签失败:', error);
    }
  };

  const handleAdd = () => {
    setEditingStockTag(null);
    form.resetFields();
    setModalVisible(true);
  };

  const handleEdit = (record) => {
    setEditingStockTag(record);
    form.setFieldsValue({
      ts_code: record.ts_code,
      tag_id: record.tag_id,
      start_date: record.start_date ? moment(record.start_date) : null,
      end_date: record.end_date ? moment(record.end_date) : null,
      note: record.note
    });
    setModalVisible(true);
  };

  const handleDelete = async (id) => {
    try {
      // 这里需要根据实际的API调整
      await tagApi.deleteStockTag(editingStockTag.ts_code, editingStockTag.tag_id);
      message.success('删除股票标签成功');
      fetchStockTags();
    } catch (error) {
      message.error('删除股票标签失败');
    }
  };

  const handleModalOk = async () => {
    try {
      const values = await form.validateFields();
      const payload = {
        ts_code: values.ts_code,
        tag_id: values.tag_id,
        user_id: userId,
        start_date: values.start_date?.format('YYYY-MM-DD'),
        end_date: values.end_date?.format('YYYY-MM-DD'),
        note: values.note
      };

      if (editingStockTag) {
        await tagApi.updateStockTag(editingStockTag.ts_code, editingStockTag.tag_id, payload);
        message.success('更新股票标签成功');
      } else {
        await tagApi.addStockTag(values.ts_code, payload);
        message.success('添加股票标签成功');
      }
      setModalVisible(false);
      fetchStockTags();
    } catch (error) {
      message.error('操作失败');
    }
  };

  const getTagName = (tagId) => {
    const tag = tags.find(t => t.id === tagId);
    return tag ? tag.name : '未知标签';
  };

  const getTagColor = (tagId) => {
    const tag = tags.find(t => t.id === tagId);
    return tag ? tag.color : '#1890ff';
  };

  const columns = [
    {
      title: '股票代码',
      dataIndex: 'ts_code',
      key: 'ts_code',
      width: 120,
      render: (text) => <Tag color="blue">{text}</Tag>
    },
    {
      title: '标签',
      dataIndex: 'tag_id',
      key: 'tag_id',
      width: 150,
      render: (tagId) => (
        <Tag color={getTagColor(tagId)}>
          {getTagName(tagId)}
        </Tag>
      )
    },
    {
      title: '开始日期',
      dataIndex: 'start_date',
      key: 'start_date',
      width: 120,
      render: (value) => value ? new Date(value).toLocaleDateString() : '-'
    },
    {
      title: '结束日期',
      dataIndex: 'end_date',
      key: 'end_date',
      width: 120,
      render: (value) => value ? new Date(value).toLocaleDateString() : '-'
    },
    {
      title: '备注',
      dataIndex: 'note',
      key: 'note',
      ellipsis: true
    },
    {
      title: '创建时间',
      dataIndex: 'created_at',
      key: 'created_at',
      width: 120,
      render: (value) => new Date(value).toLocaleDateString()
    },
    {
      title: '操作',
      key: 'action',
      width: 120,
      render: (_, record) => (
        <Space>
          <Button 
            type="text" 
            icon={<EditOutlined />} 
            onClick={() => handleEdit(record)}
          />
          <Popconfirm title="确定删除此股票标签？" onConfirm={() => handleDelete(record.id)}>
            <Button type="text" danger icon={<DeleteOutlined />} />
          </Popconfirm>
        </Space>
      )
    }
  ];

  return (
    <div style={{ padding: 24 }}>
      <Card>
        <Title level={4} style={{ marginBottom: 24 }}>
          <TagOutlined style={{ marginRight: 8 }} />
          股票标签管理
        </Title>
        
        <div style={{ marginBottom: 16 }}>
          <Button type="primary" icon={<PlusOutlined />} onClick={handleAdd}>
            添加股票标签
          </Button>
        </div>
        
        <Table
          columns={columns}
          dataSource={stockTags}
          rowKey="id"
          loading={loading}
          pagination={{ pageSize: 20 }}
        />
      </Card>

      <Modal
        title={editingStockTag ? '编辑股票标签' : '添加股票标签'}
        open={modalVisible}
        onOk={handleModalOk}
        onCancel={() => setModalVisible(false)}
        destroyOnClose
        width={600}
      >
        <Form form={form} layout="vertical">
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item 
                name="ts_code" 
                label="股票代码" 
                rules={[{ required: true, message: '请输入股票代码' }]}
              >
                <Input placeholder="请输入股票代码" />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item 
                name="tag_id" 
                label="标签" 
                rules={[{ required: true, message: '请选择标签' }]}
              >
                <Select placeholder="请选择标签">
                  {tags.map(tag => (
                    <Option key={tag.id} value={tag.id}>
                      <Tag color={tag.color}>{tag.name}</Tag>
                    </Option>
                  ))}
                </Select>
              </Form.Item>
            </Col>
          </Row>
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item name="start_date" label="开始日期">
                <DatePicker style={{ width: '100%' }} />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item name="end_date" label="结束日期">
                <DatePicker style={{ width: '100%' }} />
              </Form.Item>
            </Col>
          </Row>
          <Form.Item name="note" label="备注">
            <Input.TextArea rows={3} placeholder="请输入备注" />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default StockTagPage; 