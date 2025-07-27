import React, { useEffect, useState } from 'react';
import { Table, Button, Modal, Form, Input, message, Popconfirm, Card } from 'antd';
import { strategyApi } from '../api/strategyApi';
import { formatDate } from '../utils/formatters';

const StrategyPage = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [editing, setEditing] = useState(null);
  const [form] = Form.useForm();

  const fetchData = async () => {
    setLoading(true);
    try {
      const res = await strategyApi.getStrategies();
      console.log(res.data);
      setData(res.data.data);
    } catch {
      message.error('加载策略失败');
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleAdd = () => {
    setEditing(null);
    form.resetFields();
    setModalVisible(true);
  };

  const handleEdit = (record) => {
    setEditing(record);
    form.setFieldsValue(record);
    setModalVisible(true);
  };

  const handleDelete = async (id) => {
    try {
      await strategyApi.deleteStrategy(id);
      message.success('删除成功');
      fetchData();
    } catch {
      message.error('删除失败');
    }
  };

  const handleOk = async () => {
    try {
      const values = await form.validateFields();
      if (editing) {
        await strategyApi.updateStrategy(editing.id, values);
        message.success('更新成功');
      } else {
        await strategyApi.addStrategy(values);
        message.success('新增成功');
      }
      setModalVisible(false);
      fetchData();
    } catch {}
  };

  const columns = [
    { title: '策略名称', dataIndex: 'name', key: 'name' },
    { title: '策略描述', dataIndex: 'description', key: 'description' },
    { title: '创建时间', dataIndex: 'created_at', key: 'created_at', width: 120, render: val => val ? formatDate(val, 'YYYY-MM-DD') : '' },
    { title: '更新时间', dataIndex: 'updated_at', key: 'updated_at', width: 120, render: val => val ? formatDate(val, 'YYYY-MM-DD') : '' },
    {
      title: '操作',
      key: 'action',
      render: (_, record) => (
        <>
          <Button type="link" onClick={() => handleEdit(record)}>编辑</Button>
          <Popconfirm title="确定删除？" onConfirm={() => handleDelete(record.id)}>
            <Button type="link" danger>删除</Button>
          </Popconfirm>
        </>
      ),
    },
  ];

  return (
    <div style={{ padding: 24 }}>
      <Card title="策略管理">
        <Button type="primary" onClick={handleAdd} style={{ marginBottom: 16 }}>新增策略</Button>
        <Table
          columns={columns}
          dataSource={data}
          rowKey="id"
          loading={loading}
          bordered
        />
        <Modal
          title={editing ? '编辑策略' : '新增策略'}
          open={modalVisible}
          onOk={handleOk}
          onCancel={() => setModalVisible(false)}
          destroyOnClose
        >
          <Form form={form} layout="vertical">
            <Form.Item name="name" label="策略名称" rules={[{ required: true, message: '请输入策略名称' }]}> 
              <Input />
            </Form.Item>
            <Form.Item name="description" label="策略描述"> 
              <Input.TextArea rows={3} />
            </Form.Item>
          </Form>
        </Modal>
      </Card>
    </div>
  );
};

export default StrategyPage; 