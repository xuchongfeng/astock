import React, { useEffect, useState } from 'react';
import { Table, Button, message } from 'antd';
import { fetchStockDaily, deleteStockDaily } from '../api/stockDaily';

const StockDailyList = () => {
  const [data, setData] = useState([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(false);
  const [pagination, setPagination] = useState({ current: 1, pageSize: 20 });
  const [sorter, setSorter] = useState({});

  const loadData = async (page = 1, pageSize = 20, sorter = {}) => {
    setLoading(true);
    try {
      const params = {
        page,
        pageSize,
        sortFields: sorter.field ? (sorter.order === 'descend' ? `-${sorter.field}` : sorter.field) : undefined,
      };
      const res = await fetchStockDaily(params);
      setData(res.data.data);
      setTotal(res.data.total);
      setPagination({ current: page, pageSize });
    } catch (e) {
      message.error('加载数据失败');
    }
    setLoading(false);
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleTableChange = (pagination, filters, sorter) => {
    loadData(pagination.current, pagination.pageSize, sorter);
  };

  const handleDelete = async (id) => {
    await deleteStockDaily(id);
    message.success('删除成功');
    loadData(pagination.current, pagination.pageSize, sorter);
  };

  const columns = [
    { title: 'ID', dataIndex: 'id' },
    { title: '股票代码', dataIndex: 'ts_code' },
    { title: '交易日期', dataIndex: 'trade_date' },
    { title: '开盘价', dataIndex: 'open' },
    { title: '收盘价', dataIndex: 'close' },
    { title: '成交量', dataIndex: 'vol' },
    { title: '成交额', dataIndex: 'amount' },
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
      pagination={{ ...pagination, total }}
      onChange={handleTableChange}
    />
  );
};

export default StockDailyList;
