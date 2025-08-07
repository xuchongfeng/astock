import React, { useState } from 'react';
import { Table, Tag, Tooltip, Button, message, Modal, Form, Input, Checkbox, Space, Tabs } from 'antd';
import { formatDate, formatCurrency, formatPercent } from '../utils/formatters';
import KLineChart from './KLineChart';
import { StarFilled, StarOutlined, MessageOutlined, FolderOutlined, RobotOutlined } from '@ant-design/icons';
import { watchlistApi } from '../api/watchlistApi';
import { stockNoteApi } from '../api/stockNoteApi';
import { snowballApi } from '../api/snowballApi';
import { deepseekApi } from '../api/deepseekApi';
import MarkdownRenderer from './MarkdownRenderer';

const StockDailyDetailTable = ({ data, loading, pagination, onChange, sortConfig }) => {
  const [watchlistStatus, setWatchlistStatus] = useState({}); // { ts_code: true/false }
  const [watchlistLoading, setWatchlistLoading] = useState({}); // { ts_code: true/false }
  const [commentModal, setCommentModal] = useState({ visible: false, ts_code: '', stock_name: '' });
  const [commentForm] = Form.useForm();
  const [commentLoading, setCommentLoading] = useState(false);
  const [ratingMap, setRatingMap] = useState({}); // { ts_code: 1-5 }
  const [ratingLoading, setRatingLoading] = useState({}); // { ts_code: true/false }
  
  // 雪球分组相关状态
  const [snowballModal, setSnowballModal] = useState({ visible: false, ts_code: '', stock_name: '' });
  const [snowballGroups, setSnowballGroups] = useState([]);
  const [selectedGroups, setSelectedGroups] = useState([]);
  const [snowballLoading, setSnowballLoading] = useState(false);
  
  // DeepSeek分析相关状态
  const [deepseekModal, setDeepseekModal] = useState({ visible: false, ts_code: '', stock_name: '' });
  const [deepseekAnalysis, setDeepseekAnalysis] = useState('');
  const [deepseekLoading, setDeepseekLoading] = useState(false);
  const [deepseekDailyAnalysis, setDeepseekDailyAnalysis] = useState('');
  const [deepseekDailyLoading, setDeepseekDailyLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('basic');
  
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

  // 雪球分组相关处理函数
  const handleAddToSnowball = async (ts_code, stock_name) => {
    if (!userId) {
      message.warning('请先登录');
      return;
    }
    
    setSnowballModal({ visible: true, ts_code, stock_name });
    setSelectedGroups([]);
    
    // 获取雪球分组列表
    try {
      setSnowballLoading(true);
      const response = await snowballApi.getGroups();
      const groups = response.data.data.stocks || [];
      setSnowballGroups(groups);
    } catch (error) {
      console.error('获取雪球分组失败:', error);
      message.error('获取分组列表失败');
    } finally {
      setSnowballLoading(false);
    }
  };

  const handleSnowballOk = async () => {
    if (selectedGroups.length === 0) {
      message.warning('请至少选择一个分组');
      return;
    }

    try {
      setSnowballLoading(true);
      
      // 批量添加到选中的分组
      const promises = selectedGroups.map(groupId => {
        const group = snowballGroups.find(g => g.id === groupId);
        return snowballApi.addStockToGroup(groupId, {
          stock_code: snowballModal.ts_code,
          group_name: group.name,
          note: `从股票每日数据页面添加`
        });
      });

      await Promise.all(promises);
      message.success(`已成功添加到 ${selectedGroups.length} 个分组`);
      setSnowballModal({ visible: false, ts_code: '', stock_name: '' });
      setSelectedGroups([]);
    } catch (error) {
      console.error('添加到雪球分组失败:', error);
      message.error('添加到分组失败');
    } finally {
      setSnowballLoading(false);
    }
  };

  const handleSnowballCancel = () => {
    setSnowballModal({ visible: false, ts_code: '', stock_name: '' });
    setSelectedGroups([]);
  };

  const handleGroupSelectionChange = (checkedValues) => {
    setSelectedGroups(checkedValues);
  };

  // DeepSeek分析相关处理函数
  const handleDeepseekAnalysis = async (ts_code, stock_name) => {
    setDeepseekModal({ visible: true, ts_code, stock_name });
    setDeepseekAnalysis('');
    setDeepseekDailyAnalysis('');
    setActiveTab('basic');
    setDeepseekLoading(true);
    setDeepseekDailyLoading(true);
    
    // 分别获取基础分析和走势分析，任何一个完成都可以展示
    const fetchBasicAnalysis = async () => {
      try {
        const response = await deepseekApi.getStockBasicAnalysis(ts_code);
        const analysis = response.data.analysis || response.analysis || '';
        setDeepseekAnalysis(analysis);
        if (analysis) {
          setActiveTab('basic');
        }
      } catch (error) {
        console.error('获取基础分析失败:', error);
        setDeepseekAnalysis('');
      } finally {
        setDeepseekLoading(false);
      }
    };

    const fetchDailyAnalysis = async () => {
      try {
        const response = await deepseekApi.getStockDailyAnalysis(ts_code);
        const analysis = response.data.analysis || response.analysis || '';
        setDeepseekDailyAnalysis(analysis);
        if (analysis && !deepseekAnalysis) {
          setActiveTab('daily');
        }
      } catch (error) {
        console.error('获取走势分析失败:', error);
        setDeepseekDailyAnalysis('');
      } finally {
        setDeepseekDailyLoading(false);
      }
    };

    // 并行执行两个请求
    Promise.allSettled([fetchBasicAnalysis(), fetchDailyAnalysis()]).then((results) => {
      const hasSuccess = results.some(result => result.status === 'fulfilled');
      if (!hasSuccess) {
        message.error('获取分析报告失败，请稍后重试');
      }
    });
  };

  const handleDeepseekCancel = () => {
    setDeepseekModal({ visible: false, ts_code: '', stock_name: '' });
    setDeepseekAnalysis('');
    setDeepseekDailyAnalysis('');
  };

  const handleTabChange = (key) => {
    setActiveTab(key);
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
      width: 250,
      render: (text, record) => (
        <Space>
          <span>{text}</span>
          <Button
            type="text"
            icon={watchlistStatus[record.ts_code] ? <StarFilled style={{ color: '#faad14' }} /> : <StarOutlined />}
            loading={!!watchlistLoading[record.ts_code]}
            onClick={() => handleToggleWatchlist(record.ts_code)}
            size="small"
            title="收藏到自选股"
          />
          <Button
            type="text"
            icon={<FolderOutlined />}
            onClick={() => handleAddToSnowball(record.ts_code, record.stock_name)}
            size="small"
            title="收藏到雪球分组"
          />
          <Button
            type="text"
            icon={<RobotOutlined />}
            onClick={() => handleDeepseekAnalysis(record.ts_code, record.stock_name)}
            size="small"
            title="DeepSeek分析"
          />
          <Button
            type="text"
            icon={<MessageOutlined />}
            onClick={() => handleAddComment(record.ts_code, record.stock_name)}
            size="small"
            title="添加评论"
          />
        </Space>
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

      {/* 雪球分组选择模态框 */}
      <Modal
        title={`收藏到雪球分组 - ${snowballModal.stock_name || snowballModal.ts_code}`}
        open={snowballModal.visible}
        onOk={handleSnowballOk}
        onCancel={handleSnowballCancel}
        confirmLoading={snowballLoading}
        destroyOnClose
        width={500}
      >
        <div style={{ marginBottom: 16 }}>
          <p style={{ color: '#666', marginBottom: 16 }}>
            请选择要添加到哪些分组（可多选）：
          </p>
          {snowballLoading ? (
            <div style={{ textAlign: 'center', padding: '20px' }}>
              正在加载分组列表...
            </div>
          ) : (
            <Checkbox.Group
              value={selectedGroups}
              onChange={handleGroupSelectionChange}
              style={{ width: '100%' }}
            >
              <div style={{ maxHeight: '300px', overflowY: 'auto' }}>
                {snowballGroups.map(group => (
                  <div key={group.id} style={{ marginBottom: 8 }}>
                    <Checkbox value={group.id}>
                      <Space>
                        <FolderOutlined style={{ color: '#1890ff' }} />
                        <span style={{ fontWeight: 'bold' }}>{group.name}</span>
                        {group.description && (
                          <span style={{ color: '#8c8c8c', fontSize: '12px' }}>
                            ({group.description})
                          </span>
                        )}
                      </Space>
                    </Checkbox>
                  </div>
                ))}
              </div>
            </Checkbox.Group>
          )}
        </div>
      </Modal>

      {/* DeepSeek分析模态框 */}
      <Modal
        title={`DeepSeek分析 - ${deepseekModal.stock_name || deepseekModal.ts_code}`}
        open={deepseekModal.visible}
        onCancel={handleDeepseekCancel}
        footer={null}
        destroyOnClose
        width={900}
        style={{ top: 20 }}
      >
        <Tabs 
          activeKey={activeTab} 
          onChange={handleTabChange}
          type="card"
        >
          <Tabs.TabPane 
            tab="个股分析" 
            key="basic"
          >
            <MarkdownRenderer 
              content={deepseekAnalysis} 
              loading={deepseekLoading}
            />
          </Tabs.TabPane>
          <Tabs.TabPane 
            tab="走势分析" 
            key="daily"
          >
            <MarkdownRenderer 
              content={deepseekDailyAnalysis} 
              loading={deepseekDailyLoading}
            />
          </Tabs.TabPane>
        </Tabs>
      </Modal>
    </>
  );
};

export default StockDailyDetailTable;