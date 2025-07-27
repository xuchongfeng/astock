import React, { useEffect, useState } from 'react';
import { Table, Button, Modal, Form, Input, DatePicker, message, Popconfirm } from 'antd';
import { stockNoteApi } from '../api/stockNoteApi';
import moment from 'moment';

const StockNotePage = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [editingNote, setEditingNote] = useState(null);
  const [form] = Form.useForm();

  const fetchNotes = async () => {
    setLoading(true);
    try {
      const res = await stockNoteApi.getNotes();
      setData(res.data);
    } catch (e) {
      message.error('加载记录失败');
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchNotes();
  }, []);

  const handleAdd = () => {
    setEditingNote(null);
    form.resetFields();
    setModalVisible(true);
  };

  const handleEdit = (record) => {
    setEditingNote(record);
    form.setFieldsValue({
      ...record,
      note_date: record.note_date ? moment(record.note_date) : null,
    });
    setModalVisible(true);
  };

  const handleDelete = async (id) => {
    try {
      await stockNoteApi.deleteNote(id);
      message.success('删除成功');
      fetchNotes();
    } catch {
      message.error('删除失败');
    }
  };

  const handleOk = async () => {
    try {
      const values = await form.validateFields();
      const payload = {
        ...values,
        note_date: values.note_date ? values.note_date.format('YYYY-MM-DD') : undefined,
      };
      if (editingNote) {
        await stockNoteApi.updateNote(editingNote.id, payload);
        message.success('更新成功');
      } else {
        await stockNoteApi.addNote(payload);
        message.success('新增成功');
      }
      setModalVisible(false);
      fetchNotes();
    } catch (e) {
      // 校验失败或接口报错
    }
  };

  const columns = [
    { title: '股票代码', dataIndex: 'ts_code', key: 'ts_code' },
    { title: '日期', dataIndex: 'note_date', key: 'note_date' },
    { title: '评论', dataIndex: 'comment', key: 'comment' },
    { title: '创建时间', dataIndex: 'created_at', key: 'created_at' },
    { title: '更新时间', dataIndex: 'updated_at', key: 'updated_at' },
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
      <Button type="primary" onClick={handleAdd} style={{ marginBottom: 16 }}>新增记录</Button>
      <Table
        columns={columns}
        dataSource={data}
        rowKey="id"
        loading={loading}
        bordered
      />
      <Modal
        title={editingNote ? '编辑记录' : '新增记录'}
        open={modalVisible}
        onOk={handleOk}
        onCancel={() => setModalVisible(false)}
        destroyOnClose
      >
        <Form form={form} layout="vertical">
          <Form.Item name="ts_code" label="股票代码" rules={[{ required: true, message: '请输入股票代码' }]}> 
            <Input placeholder="如: 000001.SH" />
          </Form.Item>
          <Form.Item name="note_date" label="日期" rules={[{ required: true, message: '请选择日期' }]}> 
            <DatePicker style={{ width: '100%' }} />
          </Form.Item>
          <Form.Item name="comment" label="评论"> 
            <Input.TextArea rows={4} placeholder="请输入评论" />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default StockNotePage; 