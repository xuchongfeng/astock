import React from 'react';
import { 
  Card, 
  Row, 
  Col, 
  Typography, 
  Space, 
  Divider,
  Button,
  Tag,
  List
} from 'antd';
import { 
  DatabaseOutlined,
  RobotOutlined,
  FundOutlined,
  EyeOutlined,
  LinkOutlined,
  TrophyOutlined,
  StarOutlined,
  RocketOutlined,
  SafetyOutlined,
  TeamOutlined
} from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';

const { Title, Text, Paragraph } = Typography;

const FeaturesPage = () => {
  const navigate = useNavigate();

  const features = [
    {
      icon: <DatabaseOutlined style={{ fontSize: '48px', color: '#1890ff' }} />,
      title: '数据全面覆盖',
      subtitle: '多源数据整合，全方位股票信息',
      description: '集成Tushare、同花顺、雪球等多个权威数据源，涵盖股票基本面、技术面、资金面、消息面等全维度数据，为投资决策提供坚实的数据基础。',
      highlights: [
        '实时行情数据',
        '财务指标分析',
        '资金流向监控',
        '新闻资讯聚合'
      ],
      color: '#1890ff'
    },
    {
      icon: <RobotOutlined style={{ fontSize: '48px', color: '#52c41a' }} />,
      title: 'AI智能分析',
      subtitle: 'DeepSeek大模型驱动，专业投资洞察',
      description: '基于先进的DeepSeek大语言模型，提供智能化的股票分析、市场解读和投资建议，让每位投资者都能获得专业级的分析能力。',
      highlights: [
        '智能选股推荐',
        '市场趋势分析',
        '风险评估预警',
        '个性化投资建议'
      ],
      color: '#52c41a'
    },
    {
      icon: <FundOutlined style={{ fontSize: '48px', color: '#faad14' }} />,
      title: '策略选股系统',
      subtitle: '量化策略，科学投资方法',
      description: '提供多种量化选股策略，包括技术指标、基本面筛选、资金流向等策略组合，帮助投资者建立系统化的投资体系。',
      highlights: [
        '多策略组合',
        '回测验证',
        '风险控制',
        '动态调仓'
      ],
      color: '#faad14'
    },
    {
      icon: <EyeOutlined style={{ fontSize: '48px', color: '#eb2f96' }} />,
      title: '界面简洁美观',
      subtitle: '现代化设计，极致用户体验',
      description: '采用Ant Design设计语言，界面简洁明了，操作流畅自然，让数据分析和投资决策变得轻松愉快。',
      highlights: [
        '响应式设计',
        '直观数据展示',
        '快速操作响应',
        '个性化布局'
      ],
      color: '#eb2f96'
    },
    {
      icon: <LinkOutlined style={{ fontSize: '48px', color: '#722ed1' }} />,
      title: '生态平台打通',
      subtitle: '连接主流投资平台，数据无缝流转',
      description: '与雪球、同花顺等主流投资平台深度集成，实现数据互通、策略共享，构建完整的投资生态圈。',
      highlights: [
        '雪球数据同步',
        '同花顺板块分析',
        '策略社区分享',
        '跨平台协作'
      ],
      color: '#722ed1'
    },
    {
      icon: <TrophyOutlined style={{ fontSize: '48px', color: '#f5222d' }} />,
      title: '专业投资工具',
      subtitle: '机构级功能，个人投资者专享',
      description: '提供K线图表、技术指标、资金分析等专业投资工具，让个人投资者也能享受机构级的分析能力。',
      highlights: [
        '专业K线图表',
        '技术指标库',
        '资金流向分析',
        '投资组合管理'
      ],
      color: '#f5222d'
    }
  ];

  const statistics = [
    { label: '数据源', value: '5+', unit: '个' },
    { label: '股票覆盖', value: '5000+', unit: '只' },
    { label: '技术指标', value: '100+', unit: '种' },
    { label: '策略模型', value: '20+', unit: '套' }
  ];

  return (
    <div style={{ 
      padding: '24px', 
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      minHeight: '100vh'
    }}>
      {/* 页面头部 */}
      <div style={{ textAlign: 'center', marginBottom: '40px' }}>
        <Title level={1} style={{ color: '#fff', margin: '0 0 16px 0' }}>
          <StarOutlined style={{ marginRight: '16px' }} />
          赌性坚强 - 专业投资分析平台
        </Title>
        <Text style={{ color: '#fff', fontSize: '18px', opacity: 0.9 }}>
          让每一位投资者都能拥有专业级的分析能力
        </Text>
      </div>

      {/* 核心特色展示 */}
      <Row gutter={[24, 24]} style={{ marginBottom: '40px' }}>
        {features.map((feature, index) => (
          <Col xs={24} lg={8} key={index}>
            <Card
              hoverable
              style={{ 
                height: '100%', 
                borderRadius: '16px',
                boxShadow: '0 8px 32px rgba(0,0,0,0.1)',
                border: 'none'
              }}
              bodyStyle={{ padding: '32px 24px', textAlign: 'center' }}
            >
              <div style={{ marginBottom: '24px' }}>
                {feature.icon}
              </div>
              
              <Title level={3} style={{ margin: '0 0 8px 0', color: feature.color }}>
                {feature.title}
              </Title>
              
              <Text strong style={{ 
                display: 'block', 
                marginBottom: '16px',
                fontSize: '16px',
                color: '#666'
              }}>
                {feature.subtitle}
              </Text>
              
              <Paragraph style={{ 
                margin: '0 0 20px 0',
                lineHeight: '1.6',
                color: '#666'
              }}>
                {feature.description}
              </Paragraph>
              
              <div style={{ textAlign: 'left' }}>
                {feature.highlights.map((highlight, idx) => (
                  <div key={idx} style={{ 
                    margin: '8px 0',
                    display: 'flex',
                    alignItems: 'center'
                  }}>
                    <div style={{
                      width: '6px',
                      height: '6px',
                      borderRadius: '50%',
                      backgroundColor: feature.color,
                      marginRight: '12px'
                    }} />
                    <Text style={{ fontSize: '14px', color: '#666' }}>
                      {highlight}
                    </Text>
                  </div>
                ))}
              </div>
            </Card>
          </Col>
        ))}
      </Row>

      {/* 平台数据统计 */}
      <Card
        style={{ 
          marginBottom: '40px',
          borderRadius: '16px',
          boxShadow: '0 8px 32px rgba(0,0,0,0.1)',
          border: 'none'
        }}
        bodyStyle={{ padding: '32px' }}
      >
        <Title level={2} style={{ textAlign: 'center', margin: '0 0 32px 0' }}>
          <RocketOutlined style={{ marginRight: '16px', color: '#1890ff' }} />
          平台实力展示
        </Title>
        
        <Row gutter={[32, 32]} justify="center">
          {statistics.map((stat, index) => (
            <Col key={index} style={{ textAlign: 'center' }}>
              <div style={{ marginBottom: '8px' }}>
                <Text style={{ 
                  fontSize: '48px', 
                  fontWeight: 'bold',
                  color: '#1890ff'
                }}>
                  {stat.value}
                </Text>
                <Text style={{ 
                  fontSize: '24px', 
                  color: '#1890ff',
                  marginLeft: '4px'
                }}>
                  {stat.unit}
                </Text>
              </div>
              <Text style={{ fontSize: '16px', color: '#666' }}>
                {stat.label}
              </Text>
            </Col>
          ))}
        </Row>
      </Card>

      {/* 技术优势 */}
      <Card
        style={{ 
          marginBottom: '40px',
          borderRadius: '16px',
          boxShadow: '0 8px 32px rgba(0,0,0,0.1)',
          border: 'none'
        }}
        bodyStyle={{ padding: '32px' }}
      >
        <Title level={2} style={{ textAlign: 'center', margin: '0 0 32px 0' }}>
          <SafetyOutlined style={{ marginRight: '16px', color: '#52c41a' }} />
          技术优势
        </Title>
        
        <Row gutter={[24, 24]}>
          <Col xs={24} md={12}>
            <div style={{ 
              padding: '24px',
              background: '#f6f8fa',
              borderRadius: '12px',
              height: '100%'
            }}>
              <Title level={4} style={{ color: '#1890ff', margin: '0 0 16px 0' }}>
                <DatabaseOutlined style={{ marginRight: '8px' }} />
                数据架构
              </Title>
              <List
                size="small"
                dataSource={[
                  '分布式数据存储',
                  '实时数据同步',
                  '多源数据融合',
                  '数据质量监控'
                ]}
                renderItem={item => (
                  <List.Item style={{ border: 'none', padding: '4px 0' }}>
                    <Text style={{ fontSize: '14px', color: '#666' }}>
                      • {item}
                    </Text>
                  </List.Item>
                )}
              />
            </div>
          </Col>
          
          <Col xs={24} md={12}>
            <div style={{ 
              padding: '24px',
              background: '#f6f8fa',
              borderRadius: '12px',
              height: '100%'
            }}>
              <Title level={4} style={{ color: '#52c41a', margin: '0 0 16px 0' }}>
                <RobotOutlined style={{ marginRight: '8px' }} />
                AI能力
              </Title>
              <List
                size="small"
                dataSource={[
                  '大语言模型驱动',
                  '智能数据分析',
                  '自然语言交互',
                  '持续学习优化'
                ]}
                renderItem={item => (
                  <List.Item style={{ border: 'none', padding: '4px 0' }}>
                    <Text style={{ fontSize: '14px', color: '#666' }}>
                      • {item}
                    </Text>
                  </List.Item>
                )}
              />
            </div>
          </Col>
        </Row>
      </Card>

      {/* 行动号召 */}
      <Card
        style={{ 
          borderRadius: '16px',
          boxShadow: '0 8px 32px rgba(0,0,0,0.1)',
          border: 'none',
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
        }}
        bodyStyle={{ padding: '40px', textAlign: 'center' }}
      >
        <Title level={2} style={{ color: '#fff', margin: '0 0 16px 0' }}>
          <TeamOutlined style={{ marginRight: '16px' }} />
          开启专业投资之旅
        </Title>
        <Text style={{ 
          color: '#fff', 
          fontSize: '16px', 
          opacity: 0.9,
          display: 'block',
          marginBottom: '32px'
        }}>
          加入我们，让投资变得更简单、更专业、更高效
        </Text>
        
        <Space size="large">
          <Button 
            type="primary" 
            size="large"
            style={{ 
              height: '48px', 
              padding: '0 32px',
              borderRadius: '24px',
              fontSize: '16px'
            }}
            onClick={() => navigate('/')}
          >
            立即体验
          </Button>
          <Button 
            size="large"
            style={{ 
              height: '48px', 
              padding: '0 32px',
              borderRadius: '24px',
              fontSize: '16px',
              border: '2px solid #fff',
              color: '#fff',
              background: 'transparent'
            }}
            onClick={() => navigate('/')}
          >
            了解更多
          </Button>
        </Space>
      </Card>
    </div>
  );
};

export default FeaturesPage;
