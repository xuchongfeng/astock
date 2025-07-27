import React, { useEffect, useState } from 'react';
import { Table, Button, message } from 'antd';
import { fetchStocks, deleteStock } from '../api/stock';

const StockList = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);

  const loadData = async () => {
    setLoading(true);
    try {
      const res = await fetchStocks();
      setData(res.data);
    } catch (e) {
      message.error('加载数据失败');
    }
    setLoading(false);
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleDelete = async (id) => {
    await deleteStock(id);
    message.success('删除成功');
    loadData();
  };

  const columns = [
    { title: 'ID', dataIndex: 'id' },
    { title: '股票代码', dataIndex: 'ts_code' },
    { title: '名称', dataIndex: 'name' },
    // ... 其它字段
    {
      title: '操作',
      render: (_, record) => (
        <Button danger onClick={() => handleDelete(record.id)}>删除</Button>
      ),
    },
  ];

  return (
    <Table
      rowKey="id"
      columns={columns}
      dataSource={data}
      loading={loading}
      pagination={{ pageSize: 20 }}
    />
  );
};

export default StockList;