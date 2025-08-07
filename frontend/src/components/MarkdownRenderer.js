import React from 'react';
import ReactMarkdown from 'react-markdown';
import { Typography, Divider, Alert } from 'antd';

const { Title, Paragraph, Text } = Typography;

const MarkdownRenderer = ({ content, loading = false }) => {
  if (loading) {
    return (
      <div style={{ padding: '20px', textAlign: 'center' }}>
        <div>正在生成分析报告...</div>
      </div>
    );
  }

  if (!content) {
    return (
      <Alert
        message="暂无分析数据"
        description="请稍后再试或联系管理员"
        type="info"
        showIcon
      />
    );
  }

  // 自定义Markdown组件渲染
  const components = {
    h1: ({ children }) => <Title level={1}>{children}</Title>,
    h2: ({ children }) => <Title level={2}>{children}</Title>,
    h3: ({ children }) => <Title level={3}>{children}</Title>,
    h4: ({ children }) => <Title level={4}>{children}</Title>,
    h5: ({ children }) => <Title level={5}>{children}</Title>,
    p: ({ children }) => <Paragraph>{children}</Paragraph>,
    strong: ({ children }) => <Text strong>{children}</Text>,
    em: ({ children }) => <Text italic>{children}</Text>,
    code: ({ children, inline }) => 
      inline ? (
        <Text code>{children}</Text>
      ) : (
        <pre style={{ 
          backgroundColor: '#f6f8fa', 
          padding: '12px', 
          borderRadius: '6px',
          overflow: 'auto',
          fontSize: '14px',
          lineHeight: '1.5'
        }}>
          <code>{children}</code>
        </pre>
      ),
    blockquote: ({ children }) => (
      <blockquote style={{
        borderLeft: '4px solid #1890ff',
        margin: '16px 0',
        padding: '0 16px',
        color: '#666',
        fontStyle: 'italic'
      }}>
        {children}
      </blockquote>
    ),
    ul: ({ children }) => (
      <ul style={{ paddingLeft: '20px' }}>
        {children}
      </ul>
    ),
    ol: ({ children }) => (
      <ol style={{ paddingLeft: '20px' }}>
        {children}
      </ol>
    ),
    li: ({ children }) => <li style={{ marginBottom: '4px' }}>{children}</li>,
    table: ({ children }) => (
      <div style={{ overflow: 'auto', margin: '16px 0' }}>
        <table style={{
          width: '100%',
          borderCollapse: 'collapse',
          border: '1px solid #d9d9d9'
        }}>
          {children}
        </table>
      </div>
    ),
    th: ({ children }) => (
      <th style={{
        border: '1px solid #d9d9d9',
        padding: '8px 12px',
        backgroundColor: '#fafafa',
        fontWeight: 'bold',
        textAlign: 'left'
      }}>
        {children}
      </th>
    ),
    td: ({ children }) => (
      <td style={{
        border: '1px solid #d9d9d9',
        padding: '8px 12px'
      }}>
        {children}
      </td>
    ),
    hr: () => <Divider />,
  };

  return (
    <div style={{ 
      padding: '16px',
      backgroundColor: '#fff',
      borderRadius: '8px',
      maxHeight: '600px',
      overflow: 'auto'
    }}>
      <ReactMarkdown components={components}>
        {content}
      </ReactMarkdown>
    </div>
  );
};

export default MarkdownRenderer; 