import React, { useEffect, useState } from 'react';
import { Table, Button, message } from 'antd';
import { fetchIndustryStats, deleteIndustryStats } from '../api/industryStats';

const IndustryStatsList = () => {
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
      const res = await fetchIndustryStats(params);
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
    await deleteIndustryStats(id);
    message.success('删除成功');
    loadData(pagination.current, pagination.pageSize, sorter);
  };

  const columns = [
    { title: 'ID', dataIndex: 'id' },
    { title: '行业ID', dataIndex: 'industry_id' },
    { title: '统计日期', dataIndex: 'stat_date' },
    { title: '公司数', dataIndex: 'company_count' },
    { title: '总成交额', dataIndex: 'total_amount' },
    { title: '上涨数', dataIndex: 'up_count' },
    { title: '下跌数', dataIndex: 'down_count' },
    { title: '平盘数', dataIndex: 'flat_count' },
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

export default IndustryStatsList;
