import React, { useState, useEffect } from 'react';
import { Tag, Tooltip, Button, Modal, Form, DatePicker, Input, message } from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons';
import { tagApi } from '../api/tagApi';
import TagSelector from './TagSelector';
import moment from 'moment';

const StockTags = ({ 
  tsCode, 
  showManage = false, 
  onTagsChange,
  maxDisplay = 3 
}) => {
  const [stockTags, setStockTags] = useState([]);
  const [tags, setTags] = useState([]);
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [editingTag, setEditingTag] = useState(null);
  const [form] = Form.useForm();
  const userId = localStorage.getItem('userId') || 1;

  useEffect(() => {
    if (tsCode) {
      fetchStockTags();
      fetchTags();
    }
  }, [tsCode]);

  const fetchStockTags = async () => {
    setLoading(true);
    try {
      const response = await tagApi.getStockTags(tsCode, { user_id: userId });
      const tags = response.data.data || [];
      setStockTags(tags);
      onTagsChange?.(tags);
    } catch (error) {
      console.error('获取股票标签失败:', error);
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

  const handleAddTag = () => {
    setEditingTag(null);
    form.resetFields();
    form.setFieldsValue({ ts_code: tsCode });
    setModalVisible(true);
  };

  const handleEditTag = (stockTag) => {
    setEditingTag(stockTag);
    form.setFieldsValue({
      ts_code: stockTag.ts_code,
      tag_id: stockTag.tag_id,
      start_date: stockTag.start_date ? moment(stockTag.start_date) : null,
      end_date: stockTag.end_date ? moment(stockTag.end_date) : null,
      note: stockTag.note
    });
    setModalVisible(true);
  };

  const handleDeleteTag = async (stockTag) => {
    try {
      await tagApi.deleteStockTag(stockTag.ts_code, stockTag.tag_id);
      message.success('删除标签成功');
      fetchStockTags();
    } catch (error) {
      message.error('删除标签失败');
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

      if (editingTag) {
        await tagApi.updateStockTag(editingTag.ts_code, editingTag.tag_id, payload);
        message.success('更新标签成功');
      } else {
        await tagApi.addStockTag(values.ts_code, payload);
        message.success('添加标签成功');
      }
      setModalVisible(false);
      fetchStockTags();
    } catch (error) {
      message.error('操作失败');
    }
  };

  const getTagInfo = (tagId) => {
    const tag = tags.find(t => t.id === tagId);
    return tag || { name: '未知标签', color: '#1890ff' };
  };

  const renderTag = (stockTag) => {
    const tagInfo = getTagInfo(stockTag.tag_id);
    const tooltipContent = (
      <div>
        <div>标签: {tagInfo.name}</div>
        {stockTag.start_date && <div>开始: {new Date(stockTag.start_date).toLocaleDateString()}</div>}
        {stockTag.end_date && <div>结束: {new Date(stockTag.end_date).toLocaleDateString()}</div>}
        {stockTag.note && <div>备注: {stockTag.note}</div>}
      </div>
    );

    return (
      <Tooltip key={stockTag.id} title={tooltipContent}>
        <Tag 
          color={tagInfo.color}
          style={{ marginBottom: 4 }}
        >
          {tagInfo.name}
          {showManage && (
            <span style={{ marginLeft: 4 }}>
              <Button 
                type="text" 
                size="small" 
                icon={<EditOutlined />} 
                onClick={(e) => {
                  e.stopPropagation();
                  handleEditTag(stockTag);
                }}
              />
              <Button 
                type="text" 
                size="small" 
                danger 
                icon={<DeleteOutlined />} 
                onClick={(e) => {
                  e.stopPropagation();
                  handleDeleteTag(stockTag);
                }}
              />
            </span>
          )}
        </Tag>
      </Tooltip>
    );
  };

  const displayedTags = stockTags.slice(0, maxDisplay);
  const hiddenCount = stockTags.length - maxDisplay;

  return (
    <div>
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: 4, alignItems: 'center' }}>
        {displayedTags.map(renderTag)}
        {hiddenCount > 0 && (
          <Tooltip title={`还有 ${hiddenCount} 个标签`}>
            <Tag color="default">+{hiddenCount}</Tag>
          </Tooltip>
        )}
        {showManage && (
          <Button 
            type="text" 
            size="small" 
            icon={<PlusOutlined />} 
            onClick={handleAddTag}
            style={{ marginLeft: 4 }}
          />
        )}
      </div>

      <Modal
        title={editingTag ? '编辑股票标签' : '添加股票标签'}
        open={modalVisible}
        onOk={handleModalOk}
        onCancel={() => setModalVisible(false)}
        destroyOnClose
        width={500}
      >
        <Form form={form} layout="vertical">
          <Form.Item 
            name="ts_code" 
            label="股票代码" 
            rules={[{ required: true, message: '请输入股票代码' }]}
          >
            <Input placeholder="请输入股票代码" disabled />
          </Form.Item>
          <Form.Item 
            name="tag_id" 
            label="标签" 
            rules={[{ required: true, message: '请选择标签' }]}
          >
            <TagSelector mode="single" showCreate={false} showManage={false} />
          </Form.Item>
          <Form.Item name="start_date" label="开始日期">
            <DatePicker style={{ width: '100%' }} />
          </Form.Item>
          <Form.Item name="end_date" label="结束日期">
            <DatePicker style={{ width: '100%' }} />
          </Form.Item>
          <Form.Item name="note" label="备注">
            <Input.TextArea rows={3} placeholder="请输入备注" />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default StockTags; 