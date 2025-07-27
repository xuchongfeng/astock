import React, { useState, useEffect } from 'react';
import { Table, Input, Button, Row, Col, Card, message } from 'antd';
import { stockApi } from '../api/stockApi';
import CompanyInfoCard from '../components/CompanyInfoCard';
import { formatDate } from "../utils/formatters";
import { StarFilled, StarOutlined, LineChartOutlined } from '@ant-design/icons';
import { watchlistApi } from '../api/watchlistApi';

const HomePage = () => {
  const [companies, setCompanies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [pagination, setPagination] = useState({
    current: 1,
    pageSize: 10,
    total: 0
  });
  const [searchQuery, setSearchQuery] = useState('');
  const [watchlistStatus, setWatchlistStatus] = useState({}); // { ts_code: true/false }
  const [watchlistLoading, setWatchlistLoading] = useState({}); // { ts_code: true/false }

  const userId = localStorage.getItem('userId');

  useEffect(() => {
    fetchCompanies();
  }, [pagination.current, searchQuery]);

  useEffect(() => {
    // 每次公司列表变化时，批量检查关注状态
    if (companies.length && userId) {
      const fetchStatuses = async () => {
        const statusObj = {};
        await Promise.all(companies.map(async (company) => {
          try {
            statusObj[company.ts_code] = await watchlistApi.isInWatchlist(userId, company.ts_code);
          } catch {
            statusObj[company.ts_code] = false;
          }
        }));
        setWatchlistStatus(statusObj);
      };
      fetchStatuses();
    }
  }, [companies, userId]);

  const fetchCompanies = async () => {
    setLoading(true);
    try {
      const params = {
        page: pagination.current,
        page_size: pagination.pageSize,
        ...(searchQuery && { search: searchQuery })
      };

      const response = await stockApi.getCompanies(params);
      setCompanies(response.data.data);
      setPagination({
        ...pagination,
        total: response.data.total
      });
    } catch (error) {
      console.error('获取公司列表失败:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleTableChange = (pagination) => {
    setPagination(pagination);
  };

  const handleSearch = (value) => {
    setSearchQuery(value);
    setPagination({ ...pagination, current: 1 });
  };

  const handleToggleWatchlist = async (ts_code) => {
    if (!userId) {
      message.warning('请先登录');
      return;
    }
    setWatchlistLoading((prev) => ({ ...prev, [ts_code]: true }));
    try {
      if (watchlistStatus[ts_code]) {
        await watchlistApi.removeFromWatchlist(userId, ts_code);
        setWatchlistStatus((prev) => ({ ...prev, [ts_code]: false }));
        message.success('已取消收藏');
      } else {
        await watchlistApi.addToWatchlist(userId, ts_code);
        setWatchlistStatus((prev) => ({ ...prev, [ts_code]: true }));
        message.success('已收藏');
      }
    } catch (error) {
      message.error('操作失败');
    } finally {
      setWatchlistLoading((prev) => ({ ...prev, [ts_code]: false }));
    }
  };

  const columns = [
    {
      title: '代码',
      dataIndex: 'ts_code',
      key: 'ts_code',
      render: (text, record) => (
        <span style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <Button type="link">{text}</Button>
          <Button
            type="text"
            icon={watchlistStatus[text] ? <StarFilled style={{ color: '#faad14' }} /> : <StarOutlined />}
            loading={!!watchlistLoading[text]}
            onClick={() => handleToggleWatchlist(text)}
            size="small"
          />
        </span>
      )
    },
    {
      title: '公司名称',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: '行业',
      dataIndex: 'industry',
      key: 'industry',
    },
    {
      title: '上市日期',
      dataIndex: 'list_date',
      key: 'list_date',
      render: (list_date) => (formatDate(list_date))
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      render: (status) => (
        <span style={{ color: status === '在市' ? '#52c41a' : '#f5222d' }}>
          {status}
        </span>
      )
    }
  ];

  return (
    <div style={{ padding: 20 }}>
      {/* 同花顺行业数据入口 */}
      <div style={{ marginBottom: 16 }}>
        <Button 
          type="primary" 
          icon={<LineChartOutlined />}
          href="https://q.10jqka.com.cn/thshy/" 
          target="_blank"
          rel="noopener noreferrer"
        >
          同花顺行业数据
        </Button>
      </div>

      <Card title="A股上市公司" extra={
        <Input.Search
          placeholder="搜索股票代码或公司名称"
          onSearch={handleSearch}
          style={{ width: 300 }}
        />
      }>
        <Table
          columns={columns}
          dataSource={companies}
          loading={loading}
          pagination={pagination}
          onChange={handleTableChange}
          rowKey="id"
          expandable={{
            expandedRowRender: record => <CompanyInfoCard company={record} />,
            rowExpandable: record => !!record.id,
          }}
        />
      </Card>
    </div>
  );
};

export default HomePage;