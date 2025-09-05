import React, { useState, useEffect } from 'react';
import { Card, List, Tag, Typography, Spin, Empty, Space } from 'antd';
import { FireOutlined, EyeOutlined, LikeOutlined, MessageOutlined } from '@ant-design/icons';

const { Title, Text } = Typography;

const NewsHotPage = () => {
  const [loading, setLoading] = useState(true);
  const [newsList, setNewsList] = useState([]);

  useEffect(() => {
    // 模拟数据加载
    setTimeout(() => {
      const mockNews = [
        {
          id: 1,
          title: '央行降准0.25个百分点，释放长期资金约5000亿元',
          summary: '中国人民银行决定于2024年1月15日下调金融机构存款准备金率0.25个百分点，释放长期资金约5000亿元。',
          category: '政策',
          hotScore: 98,
          views: 125000,
          likes: 3200,
          comments: 856,
          publishTime: '2024-01-15 09:30:00',
          source: '央行官网'
        },
        {
          id: 2,
          title: 'A股三大指数集体收涨，创业板指涨超2%',
          summary: '今日A股市场表现强劲，三大指数集体收涨，其中创业板指涨幅超过2%，科技股表现活跃。',
          category: '市场',
          hotScore: 95,
          views: 98000,
          likes: 2800,
          comments: 642,
          publishTime: '2024-01-15 15:00:00',
          source: '证券时报'
        },
        {
          id: 3,
          title: '新能源汽车销量再创新高，同比增长35%',
          summary: '2024年1月新能源汽车销量达到85万辆，同比增长35%，市场渗透率进一步提升。',
          category: '行业',
          hotScore: 92,
          views: 76000,
          likes: 2100,
          comments: 398,
          publishTime: '2024-01-15 14:30:00',
          source: '汽车工业协会'
        },
        {
          id: 4,
          title: '美联储官员暗示可能暂停加息',
          summary: '多位美联储官员表示，当前通胀压力有所缓解，可能考虑暂停加息步伐。',
          category: '国际',
          hotScore: 89,
          views: 68000,
          likes: 1800,
          comments: 325,
          publishTime: '2024-01-15 13:45:00',
          source: '路透社'
        },
        {
          id: 5,
          title: '芯片行业迎来新一轮投资热潮',
          summary: '随着AI技术快速发展，全球芯片行业迎来新一轮投资热潮，多家科技巨头加大投资力度。',
          category: '科技',
          hotScore: 87,
          views: 59000,
          likes: 1600,
          comments: 298,
          publishTime: '2024-01-15 12:20:00',
          source: '科技日报'
        },
        {
          id: 6,
          title: '房地产政策持续优化，多地放宽限购',
          summary: '为促进房地产市场健康发展，多地出台政策放宽限购条件，支持刚需和改善性住房需求。',
          category: '地产',
          hotScore: 85,
          views: 52000,
          likes: 1400,
          comments: 267,
          publishTime: '2024-01-15 11:15:00',
          source: '经济参考报'
        },
        {
          id: 7,
          title: '医药板块表现活跃，创新药概念股大涨',
          summary: '今日医药板块表现活跃，多只创新药概念股涨停，市场对医药行业前景看好。',
          category: '医药',
          hotScore: 83,
          views: 48000,
          likes: 1200,
          comments: 234,
          publishTime: '2024-01-15 10:45:00',
          source: '医药经济报'
        },
        {
          id: 8,
          title: '消费电子行业复苏迹象明显',
          summary: '随着全球经济逐步复苏，消费电子行业出现明显复苏迹象，相关企业业绩改善。',
          category: '消费',
          hotScore: 81,
          views: 42000,
          likes: 1100,
          comments: 198,
          publishTime: '2024-01-15 10:00:00',
          source: '消费日报'
        }
      ];
      setNewsList(mockNews);
      setLoading(false);
    }, 1000);
  }, []);

  const getCategoryColor = (category) => {
    const colorMap = {
      '政策': 'red',
      '市场': 'blue',
      '行业': 'green',
      '国际': 'purple',
      '科技': 'orange',
      '地产': 'cyan',
      '医药': 'magenta',
      '消费': 'geekblue'
    };
    return colorMap[category] || 'default';
  };

  const formatNumber = (num) => {
    if (num >= 10000) {
      return (num / 10000).toFixed(1) + '万';
    }
    return num.toString();
  };

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '50px' }}>
        <Spin size="large" />
        <div style={{ marginTop: '20px' }}>正在加载新闻热榜...</div>
      </div>
    );
  }

  return (
    <div style={{ padding: '24px' }}>
      <Card
        title={
          <Space>
            <FireOutlined style={{ color: '#ff4d4f' }} />
            <Title level={3} style={{ margin: 0 }}>新闻热榜</Title>
          </Space>
        }
        extra={
          <Text type="secondary">
            更新时间：{new Date().toLocaleString('zh-CN')}
          </Text>
        }
      >
        {newsList.length > 0 ? (
          <List
            dataSource={newsList}
            renderItem={(item, index) => (
              <List.Item
                key={item.id}
                style={{
                  padding: '16px 0',
                  borderBottom: index < newsList.length - 1 ? '1px solid #f0f0f0' : 'none'
                }}
              >
                <div style={{ width: '100%' }}>
                  <div style={{ display: 'flex', alignItems: 'flex-start', marginBottom: '12px' }}>
                    <div style={{
                      width: '24px',
                      height: '24px',
                      borderRadius: '50%',
                      backgroundColor: index < 3 ? '#ff4d4f' : '#d9d9d9',
                      color: '#fff',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      fontSize: '12px',
                      fontWeight: 'bold',
                      marginRight: '16px',
                      flexShrink: 0
                    }}>
                      {index + 1}
                    </div>
                    <div style={{ flex: 1 }}>
                      <div style={{ marginBottom: '8px' }}>
                        <Text strong style={{ fontSize: '16px', lineHeight: '1.5' }}>
                          {item.title}
                        </Text>
                      </div>
                      <div style={{ marginBottom: '8px' }}>
                        <Text type="secondary" style={{ fontSize: '14px', lineHeight: '1.4' }}>
                          {item.summary}
                        </Text>
                      </div>
                      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                        <Space size="middle">
                          <Tag color={getCategoryColor(item.category)}>
                            {item.category}
                          </Tag>
                          <Text type="secondary" style={{ fontSize: '12px' }}>
                            热度: {item.hotScore}
                          </Text>
                          <Text type="secondary" style={{ fontSize: '12px' }}>
                            <EyeOutlined /> {formatNumber(item.views)}
                          </Text>
                          <Text type="secondary" style={{ fontSize: '12px' }}>
                            <LikeOutlined /> {formatNumber(item.likes)}
                          </Text>
                          <Text type="secondary" style={{ fontSize: '12px' }}>
                            <MessageOutlined /> {formatNumber(item.comments)}
                          </Text>
                        </Space>
                        <div style={{ textAlign: 'right' }}>
                          <div style={{ fontSize: '12px', color: '#999' }}>
                            {item.source}
                          </div>
                          <div style={{ fontSize: '12px', color: '#999' }}>
                            {item.publishTime}
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </List.Item>
            )}
          />
        ) : (
          <Empty description="暂无新闻数据" />
        )}
      </Card>
    </div>
  );
};

export default NewsHotPage;
