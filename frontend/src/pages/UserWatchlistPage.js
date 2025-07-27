import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import {Card, Table, Spin, Button, Empty, Typography, message} from 'antd';
import { StarFilled, StarOutlined } from '@ant-design/icons';
import { watchlistApi } from '../api/watchlistApi';
import { formatCurrency, formatPercent, formatDate } from '../utils/formatters';
import KLineChart from '../components/KLineChart';

const { Title } = Typography;

const UserWatchlistPage = () => {
  const { userId } = 1;
  const [loading, setLoading] = useState(true);
  const [watchlist, setWatchlist] = useState([]);
  const [isCurrentUser, setIsCurrentUser] = useState(false);
  const [ratingMap, setRatingMap] = useState({}); // { ts_code: 1-5 }
  const [ratingLoading, setRatingLoading] = useState({}); // { ts_code: true/false }
  const [sorter, setSorter] = useState({});

  // 获取当前登录用户ID（假设从上下文或localStorage获取）
  localStorage.setItem("userId", 1);
  const currentUserId = localStorage.getItem('userId');

  useEffect(() => {
    setIsCurrentUser(parseInt(userId) === parseInt(currentUserId));
    fetchWatchlist(sorter.field, sorter.order);
  }, [userId, currentUserId, sorter]);

  const fetchWatchlist = async (sortField, sortOrder) => {
    setLoading(true);
    try {
      const params = {};
      if (sortField) {
        params.sort_field = sortOrder === 'descend' ? `-${sortField}` : sortField;
      }
      const data = await watchlistApi.getUserWatchlist(userId, params);
      setWatchlist(data);
      // 评级初始化
      const ratingObj = {};
      data.forEach(row => {
        ratingObj[row.ts_code] = (typeof row.rating === 'number' && row.rating > 0) ? row.rating : 0;
      });
      setRatingMap(ratingObj);
    } catch (error) {
      console.error('加载关注列表失败:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleToggleWatchlist = async (tsCode) => {
    try {
      if (watchlist.some(item => item.ts_code === tsCode)) {
        await watchlistApi.removeFromWatchlist(userId, tsCode);
        setWatchlist(watchlist.filter(item => item.ts_code !== tsCode));
        message.success('已从关注列表移除');
      } else {
        await watchlistApi.addToWatchlist(userId, tsCode);
        fetchWatchlist();
        message.success('已添加到关注列表');
      }
    } catch (error) {
      console.error('操作失败:', error);
      message.error('操作失败');
    }
  };

  const handleRatingChange = async (ts_code, rating) => {
    setRatingLoading((prev) => ({ ...prev, [ts_code]: true }));
    try {
      await watchlistApi.updateStockRating(userId, ts_code, rating);
      setRatingMap((prev) => ({ ...prev, [ts_code]: rating }));
      message.success('评级已更新');
    } catch (e) {
      message.error('评级更新失败');
    } finally {
      setRatingLoading((prev) => ({ ...prev, [ts_code]: false }));
    }
  };

  const renderStars = (ts_code) => {
    const rating = ratingMap[ts_code] || 0;
    const loading = !!ratingLoading[ts_code];
    return (
      <span>
        {[1,2,3,4,5].map(i => (
          <span key={i} style={{ cursor: loading ? 'not-allowed' : 'pointer', marginRight: 2 }} onClick={() => !loading && handleRatingChange(ts_code, i)}>
            {i <= rating ? <StarFilled style={{ color: '#faad14', fontSize: 18, opacity: loading ? 0.5 : 1 }} /> : <StarOutlined style={{ fontSize: 18, opacity: loading ? 0.5 : 1 }} />}
          </span>
        ))}
      </span>
    );
  };

  const handleTableChange = (pagination, filters, sorterObj) => {
    setSorter({ field: sorterObj.field, order: sorterObj.order });
  };

  const columns = [
    {
      title: '股票代码',
      dataIndex: 'ts_code',
      key: 'ts_code',
      render: text => <span style={{ fontWeight: 'bold' }}>{text}</span>
    },
    {
      title: '股票名称',
      dataIndex: 'name',
      key: 'name'
    },
    {
      title: '我的评级',
      dataIndex: 'rating',
      key: 'rating',
      width: 140,
      sorter: true,
      render: (_, record) => renderStars(record.ts_code)
    },
    {
      title: '创建日期',
      dataIndex: 'created_at',
      key: 'created_at',
      width: 120,
      sorter: true,
      render: value => value ? formatDate(value, 'YYYY-MM-DD') : ''
    },
    {
      title: '3日涨幅',
      dataIndex: 'pct_chg_3d',
      key: 'pct_chg_3d',
      render: value => {
        const isPositive = value > 0;
        return (
          <span style={{ color: isPositive ? '#cf1322' : '#389e0d' }}>
            {isPositive ? '+' : ''}{formatPercent(value)}
          </span>
        );
      },
      align: 'center',
      width: 90
    },
    {
      title: '5日涨幅',
      dataIndex: 'pct_chg_5d',
      key: 'pct_chg_5d',
      render: value => {
        const isPositive = value > 0;
        return (
          <span style={{ color: isPositive ? '#cf1322' : '#389e0d' }}>
            {isPositive ? '+' : ''}{formatPercent(value)}
          </span>
        );
      },
      align: 'center',
      width: 90
    },
    {
      title: '15日涨幅',
      dataIndex: 'pct_chg_15d',
      key: 'pct_chg_15d',
      render: value => {
        const isPositive = value > 0;
        return (
          <span style={{ color: isPositive ? '#cf1322' : '#389e0d' }}>
            {isPositive ? '+' : ''}{formatPercent(value)}
          </span>
        );
      },
      align: 'center',
      width: 90
    },
    {
      title: '30日涨幅',
      dataIndex: 'pct_chg_30d',
      key: 'pct_chg_30d',
      render: value => {
        const isPositive = value > 0;
        return (
          <span style={{ color: isPositive ? '#cf1322' : '#389e0d' }}>
            {isPositive ? '+' : ''}{formatPercent(value)}
          </span>
        );
      },
      align: 'center',
      width: 90
    },
    {
      title: '60日涨幅',
      dataIndex: 'pct_chg_60d',
      key: 'pct_chg_60d',
      render: value => {
        const isPositive = value > 0;
        return (
          <span style={{ color: isPositive ? '#cf1322' : '#389e0d' }}>
            {isPositive ? '+' : ''}{formatPercent(value)}
          </span>
        );
      },
      align: 'center',
      width: 90
    },
    {
      title: '操作',
      key: 'action',
      align: 'center',
      render: (_, record) => (
        <Button
          type="text"
          icon={watchlist.some(item => item.ts_code === record.ts_code) ?
            <StarFilled style={{ color: '#faad14' }} /> :
            <StarOutlined />
          }
          onClick={() => handleToggleWatchlist(record.ts_code)}
          disabled={!isCurrentUser}
        >
          {watchlist.some(item => item.ts_code === record.ts_code) ? '取消订阅' : '订阅'}
        </Button>
      )
    }
  ];

  return (
    <div style={{ padding: 24 }}>
      <Card>
        <Title level={4} style={{ marginBottom: 24 }}>
          {isCurrentUser ? '我的关注列表' : `用户 flyfish 的关注列表`}
        </Title>

        <Spin spinning={loading}>
          {watchlist.length > 0 ? (
            <Table
              columns={columns}
              dataSource={watchlist}
              rowKey="ts_code"
              pagination={{ pageSize: 10 }}
              scroll={{ x: 'max-content' }}
              onChange={handleTableChange}
              expandable={{
                expandedRowRender: record => <KLineChart tsCode={record.ts_code} />, // 展开显示K线图
                rowExpandable: record => !!record.ts_code,
              }}
            />
          ) : (
            <Empty
              description={isCurrentUser ?
                "您还没有关注任何股票，快去添加吧！" :
                "该用户还没有关注任何股票"
              }
              image={Empty.PRESENTED_IMAGE_SIMPLE}
              style={{ padding: 40 }}
            >
              {isCurrentUser && (
                <Button type="primary" href="/stocks">
                  浏览股票列表
                </Button>
              )}
            </Empty>
          )}
        </Spin>
      </Card>
    </div>
  );
};

export default UserWatchlistPage;