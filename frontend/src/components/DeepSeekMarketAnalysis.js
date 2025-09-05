import React, { useState, useEffect } from 'react';
import { 
  Card, 
  Button, 
  Spin, 
  Typography, 
  Space, 
  Tag, 
  Divider,
  Row,
  Col,
  Alert,
  Tooltip,
  message
} from 'antd';
import { 
  RobotOutlined, 
  ReloadOutlined, 
  CalendarOutlined,
  BulbOutlined,
  ArrowUpOutlined,
  WarningOutlined,
  CheckCircleOutlined
} from '@ant-design/icons';
import { deepseekApi } from '../api/deepseekApi';
import { formatDate } from '../utils/formatters';

const { Title, Text, Paragraph } = Typography;

const DeepSeekMarketAnalysis = ({ date = null, height = 400 }) => {
  const [loading, setLoading] = useState(false);
  const [analysisData, setAnalysisData] = useState(null);
  const [error, setError] = useState(null);
  const [lastUpdate, setLastUpdate] = useState(null);

  // 如果没有指定日期，使用今天
  const analysisDate = date || new Date();

  useEffect(() => {
    fetchMarketAnalysis();
  }, [analysisDate]);

  const fetchMarketAnalysis = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await deepseekApi.getMarketOverview(formatDate(analysisDate, 'YYYY-MM-DD'));
      
      if (response.data.success) {
        setAnalysisData(response.data);
        setLastUpdate(new Date());
        message.success('市场分析获取成功');
      } else {
        setError(response.data.error || '获取市场分析失败');
        message.error('获取市场分析失败');
      }
    } catch (error) {
      console.error('获取市场分析失败:', error);
      setError('网络请求失败，请稍后重试');
      message.error('网络请求失败');
    } finally {
      setLoading(false);
    }
  };

  const handleRefresh = () => {
    fetchMarketAnalysis();
  };

  // 解析分析内容，提取关键信息
  const parseAnalysisContent = (content) => {
    if (!content) return { sections: [] };
    
    // 简单的文本解析，提取标题和内容
    const lines = content.split('\n').filter(line => line.trim());
    const sections = [];
    let currentSection = null;
    
    lines.forEach(line => {
      const trimmedLine = line.trim();
      
      // 检测标题行（通常包含数字和点，或者特定关键词）
      if (/^\d+\./.test(trimmedLine) || 
          /^[一二三四五六七八九十]+、/.test(trimmedLine) ||
          /^(大盘指数|市场情绪|板块轮动|资金流向|成交量|技术面|政策面|外围市场|市场预测|投资建议)/.test(trimmedLine)) {
        
        if (currentSection) {
          sections.push(currentSection);
        }
        
        currentSection = {
          title: trimmedLine,
          content: []
        };
      } else if (currentSection && trimmedLine) {
        currentSection.content.push(trimmedLine);
      }
    });
    
    if (currentSection) {
      sections.push(currentSection);
    }
    
    return { sections };
  };

  const { sections = [] } = parseAnalysisContent(analysisData?.analysis);

  // 获取图标和颜色
  const getSectionIcon = (title) => {
    if (title.includes('大盘指数')) return <ArrowUpOutlined style={{ color: '#1890ff' }} />;
    if (title.includes('市场情绪')) return <BulbOutlined style={{ color: '#faad14' }} />;
    if (title.includes('板块轮动')) return <ReloadOutlined style={{ color: '#52c41a' }} />;
    if (title.includes('资金流向')) return <ArrowUpOutlined style={{ color: '#722ed1' }} />;
    if (title.includes('成交量')) return <ArrowUpOutlined style={{ color: '#13c2c2' }} />;
    if (title.includes('技术面')) return <ArrowUpOutlined style={{ color: '#eb2f96' }} />;
    if (title.includes('政策面')) return <CheckCircleOutlined style={{ color: '#52c41a' }} />;
    if (title.includes('外围市场')) return <ArrowUpOutlined style={{ color: '#fa8c16' }} />;
    if (title.includes('市场预测')) return <BulbOutlined style={{ color: '#1890ff' }} />;
    if (title.includes('投资建议')) return <WarningOutlined style={{ color: '#faad14' }} />;
    return <BulbOutlined style={{ color: '#666' }} />;
  };

  const getSectionColor = (title) => {
    if (title.includes('投资建议')) return 'orange';
    if (title.includes('市场预测')) return 'blue';
    if (title.includes('风险')) return 'red';
    return 'default';
  };

  return (
    <Card
      title={
        <Space>
          <RobotOutlined style={{ color: '#1890ff' }} />
          <span>DeepSeek 每日行情分析</span>
          <Tag color="blue" icon={<CalendarOutlined />}>
            {formatDate(analysisDate, 'YYYY-MM-DD')}
          </Tag>
        </Space>
      }
      extra={
        <Space>
          <Tooltip title="刷新分析">
            <Button 
              type="text" 
              icon={<ReloadOutlined />} 
              onClick={handleRefresh}
              loading={loading}
            />
          </Tooltip>
        </Space>
      }
      style={{ height: '100%' }}
      bodyStyle={{ padding: '16px', height: height - 120, overflow: 'auto' }}
    >
      {loading ? (
        <div style={{ textAlign: 'center', padding: '40px 0' }}>
          <Spin size="large" />
          <div style={{ marginTop: '16px' }}>
            <Text type="secondary">AI正在分析市场数据，请稍候...</Text>
          </div>
        </div>
      ) : error ? (
        <Alert
          message="获取分析失败"
          description={error}
          type="error"
          showIcon
          action={
            <Button size="small" onClick={handleRefresh}>
              重试
            </Button>
          }
        />
      ) : analysisData ? (
        <div>
          {/* 分析概览 */}
          <div style={{ marginBottom: '20px', padding: '16px', background: '#f6f8fa', borderRadius: '8px' }}>
            <Row gutter={16} align="middle">
              <Col flex="auto">
                <Title level={5} style={{ margin: 0, color: '#1890ff' }}>
                  <BulbOutlined style={{ marginRight: '8px' }} />
                  AI市场分析概览
                </Title>
                <Text type="secondary">
                  基于{formatDate(analysisDate, 'YYYY年MM月DD日')}市场数据的智能分析
                </Text>
              </Col>
              <Col>
                <Tag color="green" icon={<CheckCircleOutlined />}>
                  分析完成
                </Tag>
              </Col>
            </Row>
            {lastUpdate && (
              <div style={{ marginTop: '8px', fontSize: '12px', color: '#666' }}>
                最后更新：{lastUpdate.toLocaleString('zh-CN')}
              </div>
            )}
          </div>

          {/* 分析内容 */}
          {sections.length > 0 ? (
            <div>
              {sections.map((section, index) => (
                <div key={index} style={{ marginBottom: '20px' }}>
                  <div style={{ marginBottom: '12px' }}>
                    <Tag 
                      color={getSectionColor(section.title)} 
                      icon={getSectionIcon(section.title)}
                      style={{ fontSize: '14px', padding: '4px 12px' }}
                    >
                      {section.title}
                    </Tag>
                  </div>
                  
                  <div style={{ 
                    padding: '12px 16px', 
                    background: '#fff', 
                    border: '1px solid #f0f0f0',
                    borderRadius: '6px',
                    lineHeight: '1.6'
                  }}>
                    {section.content.map((line, lineIndex) => (
                      <Paragraph key={lineIndex} style={{ margin: '8px 0', fontSize: '14px' }}>
                        {line}
                      </Paragraph>
                    ))}
                  </div>
                  
                  {index < sections.length - 1 && <Divider style={{ margin: '16px 0' }} />}
                </div>
              ))}
            </div>
          ) : (
            <div style={{ 
              padding: '40px 20px', 
              textAlign: 'center',
              color: '#666'
            }}>
              <BulbOutlined style={{ fontSize: '48px', marginBottom: '16px' }} />
              <div>AI分析内容解析中...</div>
              <div style={{ fontSize: '12px', marginTop: '8px' }}>
                如果内容显示异常，请点击刷新按钮重试
              </div>
            </div>
          )}

          {/* 原始内容（调试用，可以隐藏） */}
          {process.env.NODE_ENV === 'development' && (
            <details style={{ marginTop: '20px' }}>
              <summary style={{ cursor: 'pointer', color: '#666' }}>
                查看原始分析内容
              </summary>
              <pre style={{ 
                background: '#f5f5f5', 
                padding: '12px', 
                borderRadius: '4px',
                fontSize: '12px',
                overflow: 'auto',
                maxHeight: '200px'
              }}>
                {analysisData.analysis}
              </pre>
            </details>
          )}
        </div>
      ) : (
        <div style={{ textAlign: 'center', padding: '40px 0', color: '#666' }}>
          <RobotOutlined style={{ fontSize: '48px', marginBottom: '16px' }} />
          <div>点击刷新按钮获取AI市场分析</div>
        </div>
      )}
    </Card>
  );
};

export default DeepSeekMarketAnalysis;
