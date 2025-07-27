import React, { useState } from 'react';
import { Table, Tag, Tooltip, Button, message, Modal, Form, Input } from 'antd';
import { formatDate, formatCurrency, formatPercent } from '../utils/formatters';
import KLineChart from './KLineChart';
import { StarFilled, StarOutlined, MessageOutlined } from '@ant-design/icons';
import { watchlistApi } from '../api/watchlistApi';
import { stockNoteApi } from '../api/stockNoteApi';

const StockDailyDetailTable = ({ data, loading, pagination, onChange, sortConfig }) => {
  const [watchlistStatus, setWatchlistStatus] = useState({}); // { ts_code: true/false }
  const [watchlistLoading, setWatchlistLoading] = useState({}); // { ts_code: true/false }
  const [commentModal, setCommentModal] = useState({ visible: false, ts_code: '', stock_name: '' });
  const [commentForm] = Form.useForm();
  const [commentLoading, setCommentLoading] = useState(false);
  const [ratingMap, setRatingMap] = useState({}); // { ts_code: 1-5 }
  const [ratingLoading, setRatingLoading] = useState({}); // { ts_code: true/false }
  const userId = localStorage.getItem('userId');

  // 获取收藏状态和评级（只在首次渲染和data变化时批量检查）
  React.useEffect(() => {
    if (data && data.length && userId) {
      const fetchStatuses = async () => {
        const statusObj = {};
        const ratingObj = {};
        await Promise.all(data.map(async (row) => {
          console.log(row);
          if (!row.ts_code) return;
          try {
            statusObj[row.ts_code] = await watchlistApi.isInWatchlist(userId, row.ts_code);
          } catch {
            statusObj[row.ts_code] = false;
          }
          // 以后端row.rating为主（如果有），否则保留本地ratingMap
          ratingObj[row.ts_code] = (typeof row.rating === 'number' && row.rating > 0) ? row.rating : (ratingMap[row.ts_code] || 0);
        }));
        setWatchlistStatus(statusObj);
        setRatingMap(ratingObj);
      };
      fetchStatuses();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [data, userId]);

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

  const handleAddComment = (ts_code, stock_name) => {
    setCommentModal({ visible: true, ts_code, stock_name });
    commentForm.resetFields();
  };

  const handleCommentOk = async () => {
    try {
      setCommentLoading(true);
      const values = await commentForm.validateFields();
      await stockNoteApi.addNote({
        ts_code: commentModal.ts_code,
        note_date: new Date().toISOString().slice(0, 10),
        comment: values.comment
      });
      message.success('评论已添加');
      setCommentModal({ visible: false, ts_code: '', stock_name: '' });
    } catch (e) {
      // 校验失败或接口报错
    } finally {
      setCommentLoading(false);
    }
  };

  const handleRatingChange = async (ts_code, rating) => {
    if (!userId) {
      message.warning('请先登录');
      return;
    }
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

  const columns = [
    {
      title: '股票代码',
      dataIndex: 'ts_code',
      key: 'ts_code',
      render: (text) => <Tag color="blue">{text}</Tag>,
      width: 120
    },
    {
      title: '股票名称',
      dataIndex: 'stock_name',
      key: 'stock_name',
      width: 150,
      render: (text, record) => (
        <span style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          {text}
          <Button
            type="text"
            icon={watchlistStatus[record.ts_code] ? <StarFilled style={{ color: '#faad14' }} /> : <StarOutlined />}
            loading={!!watchlistLoading[record.ts_code]}
            onClick={() => handleToggleWatchlist(record.ts_code)}
            size="small"
          />
          <Button
            type="text"
            icon={<MessageOutlined />}
            onClick={() => handleAddComment(record.ts_code, record.stock_name)}
            size="small"
          />
        </span>
      )
    },
    {
      title: '我的评级',
      dataIndex: 'rating',
      key: 'rating',
      width: 120,
      render: (_, record) => renderStars(record.ts_code)
    },
    {
      title: '交易日期',
      dataIndex: 'trade_date',
      key: 'trade_date',
      sorter: true,
      sortOrder: sortConfig.field === 'trade_date' ? sortConfig.order : false,
      render: date => formatDate(date, 'YYYY-MM-DD'),
      width: 120
    },
    {
      title: '成交额(元)',
      dataIndex: 'amount',
      key: 'amount',
      sorter: true,
      sortOrder: sortConfig.field === 'amount' ? sortConfig.order : false,
      render: value => value ? formatCurrency(value) : '-',
      align: 'right',
      width: 120
    },
    {
      title: '当日涨幅',
      dataIndex: 'pct_chg',
      key: 'pct_chg',
      sorter: true,
      sortOrder: sortConfig.field === 'pct_chg' ? sortConfig.order : false,
      render: value => {
        const isPositive = value > 0;
        return (
          <Tag color={isPositive ? '#cf1322' : '#389e0d'}>
            {isPositive ? '+' : ''}{formatPercent(value)}
          </Tag>
        );
      },
      align: 'center',
      width: 100
    },
    {
      title: '3日涨幅',
      dataIndex: 'pct_chg_3d',
      key: 'pct_chg_3d',
      render: value => {
        const isPositive = value > 0;
        return (
          <Tag color={isPositive ? '#cf1322' : '#389e0d'}>
            {isPositive ? '+' : ''}{formatPercent(value)}
          </Tag>
        );
      },
      align: 'center',
      width: 100
    },
    {
      title: '5日涨幅',
      dataIndex: 'pct_chg_5d',
      key: 'pct_chg_5d',
      render: value => {
        const isPositive = value > 0;
        return (
          <Tag color={isPositive ? '#cf1322' : '#389e0d'}>
            {isPositive ? '+' : ''}{formatPercent(value)}
          </Tag>
        );
      },
      align: 'center',
      width: 100
    },
    {
      title: '15日涨幅',
      dataIndex: 'pct_chg_15d',
      key: 'pct_chg_15d',
      render: value => {
        const isPositive = value > 0;
        return (
          <Tag color={isPositive ? '#cf1322' : '#389e0d'}>
            {isPositive ? '+' : ''}{formatPercent(value)}
          </Tag>
        );
      },
      align: 'center',
      width: 100
    },
    {
      title: '30日涨幅',
      dataIndex: 'pct_chg_30d',
      key: 'pct_chg_30d',
      render: value => {
        const isPositive = value > 0;
        return (
          <Tag color={isPositive ? '#cf1322' : '#389e0d'}>
            {isPositive ? '+' : ''}{formatPercent(value)}
          </Tag>
        );
      },
      align: 'center',
      width: 100
    },
    {
      title: '60日涨幅',
      dataIndex: 'pct_chg_60d',
      key: 'pct_chg_60d',
      render: value => {
        const isPositive = value > 0;
        return (
          <Tag color={isPositive ? '#cf1322' : '#389e0d'}>
            {isPositive ? '+' : ''}{formatPercent(value)}
          </Tag>
        );
      },
      align: 'center',
      width: 100
    },

    {
      title: '换手率',
      dataIndex: 'turnover_rate',
      key: 'turnover_rate',
      render: value => value ? formatPercent(value) : '-',
      align: 'right',
      width: 100
    }
  ];

  return (
    <>
      <Table
        columns={columns}
        dataSource={data}
        rowKey={record => (record.ts_code ? `${record.ts_code}-${record.trade_date}` : record.id || record.trade_date)}
        loading={loading}
        pagination={pagination}
        onChange={onChange}
        scroll={{ x: 'max-content' }}
        size="middle"
        bordered
        showSorterTooltip={{ title: '点击排序' }}
        expandable={{
          expandedRowRender: record => record.ts_code ? <KLineChart tsCode={record.ts_code} /> : null,
          rowExpandable: record => !!record.ts_code,
        }}
      />
      <Modal
        title={`添加评论 - ${commentModal.stock_name || commentModal.ts_code}`}
        open={commentModal.visible}
        onOk={handleCommentOk}
        onCancel={() => setCommentModal({ visible: false, ts_code: '', stock_name: '' })}
        confirmLoading={commentLoading}
        destroyOnClose
      >
        <Form form={commentForm} layout="vertical">
          <Form.Item name="comment" label="评论" rules={[{ required: true, message: '请输入评论' }]}>
            <Input.TextArea rows={4} placeholder="请输入评论内容" />
          </Form.Item>
        </Form>
      </Modal>
    </>
  );
};

export default StockDailyDetailTable;