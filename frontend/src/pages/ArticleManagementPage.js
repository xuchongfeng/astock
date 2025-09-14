import React, { useState, useEffect } from 'react';
import {
  Card,
  Table,
  Button,
  Space,
  Tag,
  Modal,
  Form,
  Input,
  Select,
  Switch,
  message,
  Popconfirm,
  Row,
  Col,
  Statistic,
  Typography,
  Divider,
  Tooltip,
  Badge
} from 'antd';
import {
  PlusOutlined,
  EditOutlined,
  DeleteOutlined,
  EyeOutlined,
  LikeOutlined,
  FileTextOutlined,
  CalendarOutlined,
  UserOutlined,
  TagOutlined,
  BookOutlined,
  BarChartOutlined
} from '@ant-design/icons';
import { articleApi } from '../api/articleApi';
import { formatDate } from '../utils/formatters';

const { Title, Text } = Typography;
const { TextArea } = Input;
const { Option } = Select;

const ArticleManagementPage = () => {
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [editingArticle, setEditingArticle] = useState(null);
  const [form] = Form.useForm();
  const [statistics, setStatistics] = useState({
    total: 0,
    published: 0,
    draft: 0,
    archived: 0
  });

  // 获取当前用户ID（从localStorage）
  const currentUserId = parseInt(localStorage.getItem('userId') || '1');

  useEffect(() => {
    fetchArticles();
    fetchStatistics();
  }, []);

  // 获取文章列表
  const fetchArticles = async () => {
    setLoading(true);
    try {
      const response = await articleApi.getUserArticles(currentUserId);
      setArticles(response.data || []);
    } catch (error) {
      message.error('获取文章列表失败');
    } finally {
      setLoading(false);
    }
  };

  // 获取统计信息
  const fetchStatistics = async () => {
    try {
      const response = await articleApi.getUserArticleStatistics(currentUserId);
      setStatistics(response);
    } catch (error) {
      console.error('获取统计信息失败:', error);
    }
  };

  // 打开创建/编辑模态框
  const openModal = (article = null) => {
    setEditingArticle(article);
    setModalVisible(true);
    
    if (article) {
      form.setFieldsValue({
        title: article.title,
        content: article.content,
        summary: article.summary,
        tags: article.tags,
        category: article.category,
        status: article.status,
        is_public: article.is_public
      });
    } else {
      form.resetFields();
    }
  };

  // 关闭模态框
  const closeModal = () => {
    setModalVisible(false);
    setEditingArticle(null);
    form.resetFields();
  };

  // 保存文章
  const handleSave = async () => {
    try {
      const values = await form.validateFields();
      
      const articleData = {
        user_id: currentUserId,
        title: values.title,
        content: values.content,
        summary: values.summary || '',
        tags: values.tags || [],
        category: values.category || '投资思路',
        status: values.status || 'draft',
        is_public: values.is_public || false
      };

      if (editingArticle) {
        await articleApi.updateArticle(editingArticle.id, articleData);
        message.success('文章更新成功');
      } else {
        await articleApi.createArticle(articleData);
        message.success('文章创建成功');
      }

      closeModal();
      fetchArticles();
      fetchStatistics();
    } catch (error) {
      message.error(editingArticle ? '更新文章失败' : '创建文章失败');
    }
  };

  // 删除文章
  const handleDelete = async (articleId) => {
    try {
      await articleApi.deleteArticle(articleId);
      message.success('文章删除成功');
      fetchArticles();
      fetchStatistics();
    } catch (error) {
      message.error('删除文章失败');
    }
  };

  // 点赞文章
  const handleLike = async (articleId) => {
    try {
      await articleApi.likeArticle(articleId);
      message.success('点赞成功');
      fetchArticles();
    } catch (error) {
      message.error('点赞失败');
    }
  };

  // 获取状态标签颜色
  const getStatusColor = (status) => {
    const colors = {
      draft: 'orange',
      published: 'green',
      archived: 'gray'
    };
    return colors[status] || 'default';
  };

  // 获取状态文本
  const getStatusText = (status) => {
    const texts = {
      draft: '草稿',
      published: '已发布',
      archived: '已归档'
    };
    return texts[status] || status;
  };

  // 表格列定义
  const columns = [
    {
      title: '标题',
      dataIndex: 'title',
      key: 'title',
      width: 300,
      render: (title, record) => (
        <div>
          <div style={{ fontWeight: 'bold', marginBottom: 4 }}>
            {title}
          </div>
          <div style={{ fontSize: '12px', color: '#666' }}>
            {record.summary || '暂无摘要'}
          </div>
        </div>
      )
    },
    {
      title: '分类',
      dataIndex: 'category',
      key: 'category',
      width: 120,
      render: (category) => (
        <Tag color="blue" icon={<BookOutlined />}>
          {category}
        </Tag>
      )
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      width: 100,
      render: (status) => (
        <Tag color={getStatusColor(status)}>
          {getStatusText(status)}
        </Tag>
      )
    },
    {
      title: '标签',
      dataIndex: 'tags',
      key: 'tags',
      width: 150,
      render: (tags) => (
        <div>
          {tags && tags.length > 0 ? (
            tags.slice(0, 2).map((tag, index) => (
              <Tag key={index} size="small" icon={<TagOutlined />}>
                {tag}
              </Tag>
            ))
          ) : (
            <Text type="secondary">无标签</Text>
          )}
          {tags && tags.length > 2 && (
            <Tag size="small">+{tags.length - 2}</Tag>
          )}
        </div>
      )
    },
    {
      title: '公开',
      dataIndex: 'is_public',
      key: 'is_public',
      width: 80,
      render: (isPublic) => (
        <Tag color={isPublic ? 'green' : 'default'}>
          {isPublic ? '公开' : '私有'}
        </Tag>
      )
    },
    {
      title: '统计',
      key: 'stats',
      width: 120,
      render: (_, record) => (
        <Space size="small">
          <Tooltip title="浏览次数">
            <Badge count={record.view_count} showZero color="blue">
              <EyeOutlined />
            </Badge>
          </Tooltip>
          <Tooltip title="点赞次数">
            <Badge count={record.like_count} showZero color="red">
              <LikeOutlined />
            </Badge>
          </Tooltip>
        </Space>
      )
    },
    {
      title: '创建时间',
      dataIndex: 'created_at',
      key: 'created_at',
      width: 120,
      render: (date) => (
        <div>
          <div style={{ fontSize: '12px' }}>
            <CalendarOutlined style={{ marginRight: 4 }} />
            {formatDate(date, 'MM-DD')}
          </div>
          <div style={{ fontSize: '11px', color: '#999' }}>
            {formatDate(date, 'HH:mm')}
          </div>
        </div>
      )
    },
    {
      title: '操作',
      key: 'actions',
      width: 150,
      render: (_, record) => (
        <Space size="small">
          <Tooltip title="编辑">
            <Button
              type="text"
              icon={<EditOutlined />}
              onClick={() => openModal(record)}
            />
          </Tooltip>
          <Tooltip title="点赞">
            <Button
              type="text"
              icon={<LikeOutlined />}
              onClick={() => handleLike(record.id)}
            />
          </Tooltip>
          <Popconfirm
            title="确定要删除这篇文章吗？"
            onConfirm={() => handleDelete(record.id)}
            okText="确定"
            cancelText="取消"
          >
            <Tooltip title="删除">
              <Button
                type="text"
                danger
                icon={<DeleteOutlined />}
              />
            </Tooltip>
          </Popconfirm>
        </Space>
      )
    }
  ];

  return (
    <div style={{ padding: '24px', background: '#f5f7fa', minHeight: '100vh' }}>
      {/* 页面标题 */}
      <div style={{ marginBottom: '24px' }}>
        <Title level={2} style={{ margin: 0, color: '#1890ff' }}>
          <FileTextOutlined style={{ marginRight: '12px' }} />
          我的文章
        </Title>
        <Text type="secondary">
          记录您的投资思路和操作心得
        </Text>
      </div>

      {/* 统计信息 */}
      <Row gutter={16} style={{ marginBottom: '24px' }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="总文章数"
              value={statistics.total}
              prefix={<FileTextOutlined />}
              valueStyle={{ color: '#1890ff' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="已发布"
              value={statistics.published}
              prefix={<BarChartOutlined />}
              valueStyle={{ color: '#52c41a' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="草稿"
              value={statistics.draft}
              prefix={<EditOutlined />}
              valueStyle={{ color: '#faad14' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="已归档"
              value={statistics.archived}
              prefix={<DeleteOutlined />}
              valueStyle={{ color: '#666' }}
            />
          </Card>
        </Col>
      </Row>

      {/* 文章列表 */}
      <Card
        title={
          <Space>
            <FileTextOutlined />
            文章列表
          </Space>
        }
        extra={
          <Button
            type="primary"
            icon={<PlusOutlined />}
            onClick={() => openModal()}
          >
            新建文章
          </Button>
        }
      >
        <Table
          columns={columns}
          dataSource={articles}
          rowKey="id"
          loading={loading}
          pagination={{
            showSizeChanger: true,
            showQuickJumper: true,
            showTotal: (total, range) => `第 ${range[0]}-${range[1]} 条/共 ${total} 条`
          }}
          scroll={{ x: 1200 }}
        />
      </Card>

      {/* 创建/编辑文章模态框 */}
      <Modal
        title={editingArticle ? '编辑文章' : '新建文章'}
        open={modalVisible}
        onCancel={closeModal}
        onOk={handleSave}
        width={800}
        okText="保存"
        cancelText="取消"
      >
        <Form
          form={form}
          layout="vertical"
          initialValues={{
            category: '投资思路',
            status: 'draft',
            is_public: false
          }}
        >
          <Form.Item
            name="title"
            label="文章标题"
            rules={[{ required: true, message: '请输入文章标题' }]}
          >
            <Input placeholder="请输入文章标题" />
          </Form.Item>

          <Form.Item
            name="summary"
            label="文章摘要"
          >
            <TextArea
              rows={3}
              placeholder="请输入文章摘要（可选）"
            />
          </Form.Item>

          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                name="category"
                label="文章分类"
              >
                <Select placeholder="选择分类">
                  <Option value="投资思路">投资思路</Option>
                  <Option value="技术分析">技术分析</Option>
                  <Option value="基本面分析">基本面分析</Option>
                  <Option value="市场观察">市场观察</Option>
                  <Option value="操作记录">操作记录</Option>
                  <Option value="学习笔记">学习笔记</Option>
                </Select>
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                name="status"
                label="文章状态"
              >
                <Select placeholder="选择状态">
                  <Option value="draft">草稿</Option>
                  <Option value="published">已发布</Option>
                  <Option value="archived">已归档</Option>
                </Select>
              </Form.Item>
            </Col>
          </Row>

          <Form.Item
            name="tags"
            label="文章标签"
          >
            <Select
              mode="tags"
              placeholder="输入标签，按回车添加"
              style={{ width: '100%' }}
            />
          </Form.Item>

          <Form.Item
            name="is_public"
            label="公开设置"
            valuePropName="checked"
          >
            <Switch
              checkedChildren="公开"
              unCheckedChildren="私有"
            />
          </Form.Item>

          <Form.Item
            name="content"
            label="文章内容"
            rules={[{ required: true, message: '请输入文章内容' }]}
          >
            <TextArea
              rows={10}
              placeholder="请输入文章内容..."
            />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default ArticleManagementPage;
