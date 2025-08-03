import React, { useState, useEffect } from 'react';
import { 
  Card, 
  Table, 
  Button, 
  Modal, 
  Form, 
  Input, 
  ColorPicker, 
  Select, 
  message, 
  Popconfirm,
  Tag,
  Space,
  Typography
} from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined, TagOutlined } from '@ant-design/icons';
import { tagApi } from '../api/tagApi';

const { Title } = Typography;
const { Option } = Select;

const TagManagementPage = () => {
  const [tags, setTags] = useState([]);
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [editingTag, setEditingTag] = useState(null);
  const [form] = Form.useForm();

  useEffect(() => {
    fetchTags();
  }, []);

  const fetchTags = async () => {
    setLoading(true);
    try {
      const response = await tagApi.getTags();
      setTags(response.data.data || []);
    } catch (error) {
      console.error('获取标签失败:', error);
      message.error('获取标签失败');
    } finally {
      setLoading(false);
    }
  };

  const handleAdd = () => {
    setEditingTag(null);
    form.resetFields();
    setModalVisible(true);
  };

  const handleEdit = (record) => {
    setEditingTag(record);
    form.setFieldsValue({
      name: record.name,
      description: record.description,
      color: record.color,
      category: record.category
    });
    setModalVisible(true);
  };

  const handleDelete = async (id) => {
    try {
      await tagApi.deleteTag(id);
      message.success('删除标签成功');
      fetchTags();
    } catch (error) {
      message.error('删除标签失败');
    }
  };

  const handleModalOk = async () => {
    try {
      const values = await form.validateFields();
      if (editingTag) {
        await tagApi.updateTag(editingTag.id, values);
        message.success('更新标签成功');
      } else {
        await tagApi.createTag(values);
        message.success('创建标签成功');
      }
      setModalVisible(false);
      fetchTags();
    } catch (error) {
      message.error('操作失败');
    }
  };

  const getCategoryText = (category) => {
    const categoryMap = {
      'trend': '走势',
      'status': '状态',
      'custom': '自定义'
    };
    return categoryMap[category] || category;
  };

  const columns = [
    {
      title: '标签名称',
      dataIndex: 'name',
      key: 'name',
      width: 200,
      render: (text, record) => (
        <Tag color={record.color} style={{ fontSize: '14px' }}>
          {text}
        </Tag>
      )
    },
    {
      title: '描述',
      dataIndex: 'description',
      key: 'description',
      ellipsis: true
    },
    {
      title: '分类',
      dataIndex: 'category',
      key: 'category',
      width: 100,
      render: (category) => (
        <Tag color="blue">{getCategoryText(category)}</Tag>
      )
    },
    {
      title: '颜色',
      dataIndex: 'color',
      key: 'color',
      width: 100,
      render: (color) => (
        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <div 
            style={{ 
              width: 20, 
              height: 20, 
              backgroundColor: color, 
              borderRadius: 4,
              border: '1px solid #d9d9d9'
            }} 
          />
          <span>{color}</span>
        </div>
      )
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
          <Popconfirm title="确定删除此标签？" onConfirm={() => handleDelete(record.id)}>
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
          标签管理
        </Title>
        
        <div style={{ marginBottom: 16 }}>
          <Button type="primary" icon={<PlusOutlined />} onClick={handleAdd}>
            新增标签
          </Button>
        </div>
        
        <Table
          columns={columns}
          dataSource={tags}
          rowKey="id"
          loading={loading}
          pagination={{ pageSize: 20 }}
        />
      </Card>

      <Modal
        title={editingTag ? '编辑标签' : '新增标签'}
        open={modalVisible}
        onOk={handleModalOk}
        onCancel={() => setModalVisible(false)}
        destroyOnClose
      >
        <Form form={form} layout="vertical">
          <Form.Item 
            name="name" 
            label="标签名称" 
            rules={[{ required: true, message: '请输入标签名称' }]}
          >
            <Input placeholder="请输入标签名称" />
          </Form.Item>
          <Form.Item name="description" label="标签描述">
            <Input.TextArea rows={3} placeholder="请输入标签描述" />
          </Form.Item>
          <Form.Item name="color" label="标签颜色" initialValue="#1890ff">
            <ColorPicker showText />
          </Form.Item>
          <Form.Item name="category" label="标签分类" initialValue="trend">
            <Select placeholder="请选择标签分类">
              <Option value="trend">走势</Option>
              <Option value="status">状态</Option>
              <Option value="custom">自定义</Option>
            </Select>
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default TagManagementPage; 