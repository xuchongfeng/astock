import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Card,
  Row,
  Col,
  Statistic,
  Tag,
  Typography,
  Button,
  Space,
  Spin,
  Alert,
  Timeline,
  Divider
} from 'antd';
import {
  ArrowLeftOutlined,
  EditOutlined,
  DeleteOutlined,
  ReloadOutlined,
  TrophyOutlined,
  FireOutlined,
  TagOutlined,
  ClockCircleOutlined
} from '@ant-design/icons';
import { fetchHotDataById, fetchHotDataByTsCode } from '../api/thsHot';

const { Title, Text, Paragraph } = Typography;

const ThsHotDetailPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [hotData, setHotData] = useState(null);
  const [historyData, setHistoryData] = useState([]);
  const [historyLoading, setHistoryLoading] = useState(false);

  useEffect(() => {
    if (id) {
      fetchHotData();
    }
  }, [id]);

  const fetchHotData = async () => {
    setLoading(true);
    try {
      const response = await fetchHotDataById(id);
      setHotData(response.data);
      
      // 获取该股票的历史热榜数据
      if (response.data.ts_code) {
        fetchHistoryData(response.data.ts_code);
      }
    } catch (error) {
      console.error('获取热榜数据失败:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchHistoryData = async (tsCode) => {
    setHistoryLoading(true);
    try {
      const response = await fetchHotDataByTsCode(tsCode, { limit: 20 });
      setHistoryData(response.data.data);
    } catch (error) {
      console.error('获取历史数据失败:', error);
    } finally {
      setHistoryLoading(false);
    }
  };

  const handleBack = () => {
    navigate('/ths-hot');
  };

  const handleEdit = () => {
    navigate(`/ths-hot/edit/${id}`);
  };

  const handleDelete = () => {
    // 这里可以添加删除确认逻辑
    console.log('删除操作');
  };

  const renderConceptTags = (concept) => {
    if (!concept) return '-';
    
    try {
      const concepts = JSON.parse(concept);
      if (Array.isArray(concepts)) {
        return concepts.map((c, index) => (
          <Tag key={index} color="blue" icon={<TagOutlined />}>
            {c}
          </Tag>
        ));
      }
      return concept;
    } catch {
      return concept;
    }
  };

  const renderRankIcon = (rank) => {
    if (rank === 1) return <TrophyOutlined style={{ color: '#f50', fontSize: '20px' }} />;
    if (rank <= 3) return <TrophyOutlined style={{ color: '#fa8c16', fontSize: '18px' }} />;
    if (rank <= 10) return <TrophyOutlined style={{ color: '#52c41a', fontSize: '16px' }} />;
    return null;
  };

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '50px' }}>
        <Spin size="large" />
        <div style={{ marginTop: '20px' }}>加载数据中...</div>
      </div>
    );
  }

  if (!hotData) {
    return (
      <Alert
        message="数据不存在"
        description="请求的热榜数据不存在或已被删除"
        type="error"
        showIcon
        action={
          <Button size="small" onClick={handleBack}>
            返回列表
          </Button>
        }
      />
    );
  }

  return (
    <div style={{ padding: '24px' }}>
      {/* 页面头部 */}
      <div style={{ marginBottom: '24px' }}>
        <Button icon={<ArrowLeftOutlined />} onClick={handleBack} style={{ marginRight: '16px' }}>
          返回列表
        </Button>
        <Space>
          <Button icon={<EditOutlined />} onClick={handleEdit} type="primary">
            编辑
          </Button>
          <Button icon={<DeleteOutlined />} onClick={handleDelete} danger>
            删除
          </Button>
          <Button icon={<ReloadOutlined />} onClick={fetchHotData}>
            刷新
          </Button>
        </Space>
      </div>

      {/* 基本信息 */}
      <Card title="基本信息" style={{ marginBottom: '24px' }}>
        <Row gutter={24}>
          <Col span={8}>
            <div style={{ textAlign: 'center', marginBottom: '16px' }}>
              {renderRankIcon(hotData.rank)}
            </div>
            <Statistic
              title="排行"
              value={hotData.rank}
              suffix="名"
              valueStyle={{ fontSize: '32px', color: '#1890ff' }}
            />
          </Col>
          <Col span={8}>
            <Statistic
              title="股票代码"
              value={hotData.ts_code}
              valueStyle={{ fontSize: '24px' }}
            />
            <Text type="secondary">代码</Text>
          </Col>
          <Col span={8}>
            <Statistic
              title="股票名称"
              value={hotData.ts_name}
              valueStyle={{ fontSize: '24px' }}
            />
            <Text type="secondary">名称</Text>
          </Col>
        </Row>
      </Card>

      {/* 详细数据 */}
      <Row gutter={24} style={{ marginBottom: '24px' }}>
        <Col span={12}>
          <Card title="市场表现">
            <Row gutter={16}>
              <Col span={12}>
                <Statistic
                  title="涨跌幅"
                  value={hotData.pct_change}
                  suffix="%"
                  valueStyle={{ 
                    color: hotData.pct_change >= 0 ? '#52c41a' : '#ff4d4f',
                    fontSize: '20px'
                  }}
                />
              </Col>
              <Col span={12}>
                <Statistic
                  title="当前价格"
                  value={hotData.current_price}
                  suffix="元"
                  valueStyle={{ fontSize: '20px' }}
                />
              </Col>
            </Row>
            <Row gutter={16} style={{ marginTop: '16px' }}>
              <Col span={12}>
                <Statistic
                  title="热度值"
                  value={hotData.hot}
                  valueStyle={{ fontSize: '20px' }}
                />
              </Col>
              <Col span={12}>
                <Statistic
                  title="数据类型"
                  value={hotData.data_type}
                  valueStyle={{ fontSize: '20px' }}
                />
              </Col>
            </Row>
          </Card>
        </Col>
        <Col span={12}>
          <Card title="其他信息">
            <div style={{ marginBottom: '16px' }}>
              <Text strong>交易日期：</Text>
              <Text>{hotData.trade_date}</Text>
            </div>
            <div style={{ marginBottom: '16px' }}>
              <Text strong>排行榜时间：</Text>
              <Text>{hotData.rank_time || '-'}</Text>
            </div>
            <div style={{ marginBottom: '16px' }}>
              <Text strong>创建时间：</Text>
              <Text>{hotData.created_at}</Text>
            </div>
            <div style={{ marginBottom: '16px' }}>
              <Text strong>更新时间：</Text>
              <Text>{hotData.updated_at}</Text>
            </div>
          </Card>
        </Col>
      </Row>

      {/* 标签信息 */}
      <Card title="标签信息" style={{ marginBottom: '24px' }}>
        <div style={{ marginBottom: '16px' }}>
          <Text strong>概念标签：</Text>
          <div style={{ marginTop: '8px' }}>
            {renderConceptTags(hotData.concept)}
          </div>
        </div>
        <div>
          <Text strong>上榜解读：</Text>
          <Paragraph style={{ marginTop: '8px', marginBottom: 0 }}>
            {hotData.rank_reason || '暂无上榜解读'}
          </Paragraph>
        </div>
      </Card>

      {/* 历史热榜记录 */}
      <Card 
        title={
          <span>
            <ClockCircleOutlined style={{ marginRight: 8 }} />
            {hotData.ts_name} 历史热榜记录
          </span>
        }
        extra={
          <Button 
            size="small" 
            icon={<ReloadOutlined />} 
            onClick={() => fetchHistoryData(hotData.ts_code)}
            loading={historyLoading}
          >
            刷新
          </Button>
        }
      >
        {historyLoading ? (
          <div style={{ textAlign: 'center', padding: '20px' }}>
            <Spin />
          </div>
        ) : historyData.length > 0 ? (
          <Timeline>
            {historyData.map((item, index) => (
              <Timeline.Item
                key={index}
                dot={
                  <div style={{ 
                    width: '20px', 
                    height: '20px', 
                    borderRadius: '50%', 
                    backgroundColor: item.rank <= 3 ? '#f50' : item.rank <= 10 ? '#fa8c16' : '#52c41a',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: 'white',
                    fontSize: '12px',
                    fontWeight: 'bold'
                  }}>
                    {item.rank}
                  </div>
                }
              >
                <div style={{ marginBottom: '8px' }}>
                  <Text strong>{item.trade_date}</Text>
                  <Text type="secondary" style={{ marginLeft: '16px' }}>
                    {item.data_type} • 排行第{item.rank}名
                  </Text>
                  {item.pct_change !== null && (
                    <Text 
                      style={{ 
                        marginLeft: '16px',
                        color: item.pct_change >= 0 ? '#52c41a' : '#ff4d4f'
                      }}
                    >
                      {item.pct_change >= 0 ? '+' : ''}{item.pct_change}%
                    </Text>
                  )}
                </div>
                {item.rank_reason && (
                  <Text type="secondary">{item.rank_reason}</Text>
                )}
              </Timeline.Item>
            ))}
          </Timeline>
        ) : (
          <Alert
            message="暂无历史记录"
            description="该股票暂无其他热榜记录"
            type="info"
            showIcon
          />
        )}
      </Card>
    </div>
  );
};

export default ThsHotDetailPage; 