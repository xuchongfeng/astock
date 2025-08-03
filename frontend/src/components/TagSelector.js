import React, { useState, useEffect } from 'react';
import { Select, Tag, Button, Modal, Form, Input, ColorPicker, message } from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons';
import { tagApi } from '../api/tagApi';

const { Option } = Select;

const TagSelector = ({ 
  value = [], 
  onChange, 
  mode = 'multiple', 
  placeholder = '选择标签',
  allowClear = true,
  showCreate = true,
  showManage = true,
  category = null // 如果指定，只显示该分类的标签
}) => {
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
      const params = {};
      if (category) {
        params.category = category;
      }
      const response = await tagApi.getTags(params);
      setTags(response.data.data || []);
    } catch (error) {
      console.error('获取标签失败:', error);
      message.error('获取标签失败');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTag = () => {
    setEditingTag(null);
    form.resetFields();
    setModalVisible(true);
  };

  const handleEditTag = (tag) => {
    setEditingTag(tag);
    form.setFieldsValue({
      name: tag.name,
      description: tag.description,
      color: tag.color,
      category: tag.category
    });
    setModalVisible(true);
  };

  const handleDeleteTag = async (tagId) => {
    try {
      await tagApi.deleteTag(tagId);
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

  const renderTagOption = (tag) => (
    <Option key={tag.id} value={tag.id}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <Tag color={tag.color}>{tag.name}</Tag>
        {showManage && (
          <div style={{ marginLeft: 8 }}>
            <Button 
              type="text" 
              size="small" 
              icon={<EditOutlined />} 
              onClick={(e) => {
                e.stopPropagation();
                handleEditTag(tag);
              }}
            />
            <Button 
              type="text" 
              size="small" 
              danger 
              icon={<DeleteOutlined />} 
              onClick={(e) => {
                e.stopPropagation();
                handleDeleteTag(tag.id);
              }}
            />
          </div>
        )}
      </div>
    </Option>
  );

  const renderSelectedTag = (tagId) => {
    const tag = tags.find(t => t.id === tagId);
    if (!tag) return null;
    
    return (
      <Tag 
        key={tag.id} 
        color={tag.color}
        closable={mode === 'multiple'}
        onClose={() => {
          const newValue = value.filter(v => v !== tagId);
          onChange?.(newValue);
        }}
      >
        {tag.name}
      </Tag>
    );
  };

  return (
    <div>
      <div style={{ display: 'flex', gap: 8, marginBottom: 8 }}>
        <Select
          mode={mode}
          value={value}
          onChange={onChange}
          placeholder={placeholder}
          allowClear={allowClear}
          loading={loading}
          style={{ flex: 1 }}
          dropdownRender={(menu) => (
            <div>
              {menu}
              {showCreate && (
                <div style={{ padding: '8px', borderTop: '1px solid #f0f0f0' }}>
                  <Button 
                    type="dashed" 
                    icon={<PlusOutlined />} 
                    onClick={handleCreateTag}
                    style={{ width: '100%' }}
                  >
                    创建新标签
                  </Button>
                </div>
              )}
            </div>
          )}
        >
          {tags.map(renderTagOption)}
        </Select>
      </div>
      
      {mode === 'multiple' && value.length > 0 && (
        <div style={{ marginTop: 8 }}>
          {value.map(renderSelectedTag)}
        </div>
      )}

      <Modal
        title={editingTag ? '编辑标签' : '创建标签'}
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
            <Select>
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

export default TagSelector; 