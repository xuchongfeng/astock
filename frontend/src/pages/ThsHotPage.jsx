import React, { useState, useEffect } from 'react';
import {
  Card,
  Table,
  Input,
  Button,
  Select,
  DatePicker,
  Space,
  Tag,
  Typography,
  Row,
  Col,
  Statistic,
  message,
  Modal,
  Form,
  InputNumber,
  Spin,
  Collapse,
  Tabs
} from 'antd';
import {
  SearchOutlined,
  PlusOutlined,
  EditOutlined,
  DeleteOutlined,
  EyeOutlined,
  ReloadOutlined,
  CaretRightOutlined,
  CaretDownOutlined
} from '@ant-design/icons';
import { fetchHotDataList, fetchLatestHotData, fetchDataTypes, createHotData, updateHotData, deleteHotData } from '../api/thsHot';
import { dcHotApi } from '../api/dcHotApi';
import KLineChart from '../components/KLineChart';
import dayjs from 'dayjs';

const { Title, Text } = Typography;
const { Option } = Select;
const { TextArea } = Input;
const { Panel } = Collapse;

const ThsHotPage = () => {
  const [loading, setLoading] = useState(false);
  const [dataSource, setDataSource] = useState([]);
  const [pagination, setPagination] = useState({
    current: 1,
    pageSize: 20,
    total: 0
  });
  const [filters, setFilters] = useState({
    search: '',
    data_type: '热股',
    start_date: dayjs().format('YYYY-MM-DD'),
    end_date: ''
  });
  const [dataTypes, setDataTypes] = useState([]);
  const [modalVisible, setModalVisible] = useState(false);
  const [editingRecord, setEditingRecord] = useState(null);
  const [expandedRows, setExpandedRows] = useState(new Set());
  const [form] = Form.useForm();
  
  // 东方财富热榜相关状态
  const [dcHotDataSource, setDcHotDataSource] = useState([]);
  const [dcHotPagination, setDcHotPagination] = useState({
    current: 1,
    pageSize: 20,
    total: 0
  });
  const [dcHotFilters, setDcHotFilters] = useState({
    search: '',
    market: 'A股市场',
    hot_type: '人气榜',
    start_date: dayjs().format('YYYY-MM-DD'),
    end_date: ''
  });
  const [dcHotLoading, setDcHotLoading] = useState(false);
  const [dcHotModalVisible, setDcHotModalVisible] = useState(false);
  const [editingDcHotRecord, setEditingDcHotRecord] = useState(null);
  const [dcHotExpandedRows, setDcHotExpandedRows] = useState(new Set());
  const [dcHotForm] = Form.useForm();
  const [markets, setMarkets] = useState([]);
  const [hotTypes, setHotTypes] = useState([]);

  useEffect(() => {
    fetchData();
    fetchDataTypesList();
    fetchDcHotData();
    fetchDcHotOptions();
  }, []); // 只在组件挂载时执行一次

  useEffect(() => {
    fetchData();
  }, [pagination.current, filters]);

  useEffect(() => {
    fetchDcHotData();
  }, [dcHotPagination.current, dcHotFilters]);

  const fetchData = async () => {
    setLoading(true);
    try {
      const params = {
        page: pagination.current,
        pageSize: pagination.pageSize,
        ...filters
      };
      
      console.log('发送请求参数:', params);
      const response = await fetchHotDataList(params);
      console.log('API响应:', response);
      
      if (response.data && response.data.data) {
        setDataSource(response.data.data);
        setPagination(prev => ({
          ...prev,
          total: response.data.total || 0
        }));
      } else {
        console.warn('API响应格式异常:', response);
        setDataSource([]);
        setPagination(prev => ({ ...prev, total: 0 }));
      }
    } catch (error) {
      console.error('获取数据失败:', error);
      message.error(`获取数据失败: ${error.message || '未知错误'}`);
      setDataSource([]);
      setPagination(prev => ({ ...prev, total: 0 }));
    } finally {
      setLoading(false);
    }
  };

  // 获取东方财富热榜数据
  const fetchDcHotData = async () => {
    setDcHotLoading(true);
    try {
      const params = {
        page: dcHotPagination.current,
        pageSize: dcHotPagination.pageSize,
        ...dcHotFilters
      };
      
      console.log('发送东方财富热榜请求参数:', params);
      const response = await dcHotApi.getDcHotList(params);
      console.log('东方财富热榜API响应:', response);
      
      if (response.data && response.data.data) {
        setDcHotDataSource(response.data.data);
        setDcHotPagination(prev => ({
          ...prev,
          total: response.data.total || 0
        }));
      } else {
        console.warn('东方财富热榜API响应格式异常:', response);
        setDcHotDataSource([]);
        setDcHotPagination(prev => ({ ...prev, total: 0 }));
      }
    } catch (error) {
      console.error('获取东方财富热榜数据失败:', error);
      message.error(`获取东方财富热榜数据失败: ${error.message || '未知错误'}`);
      setDcHotDataSource([]);
      setDcHotPagination(prev => ({ ...prev, total: 0 }));
    } finally {
      setDcHotLoading(false);
    }
  };

  // 获取东方财富热榜选项数据
  const fetchDcHotOptions = async () => {
    try {
      const [marketsResponse, hotTypesResponse] = await Promise.all([
        dcHotApi.getMarkets(),
        dcHotApi.getHotTypes()
      ]);
      
      if (marketsResponse.data && marketsResponse.data.data) {
        setMarkets(marketsResponse.data.data.markets || []);
      }
      
      if (hotTypesResponse.data && hotTypesResponse.data.data) {
        setHotTypes(hotTypesResponse.data.data.hot_types || []);
      }
    } catch (error) {
      console.error('获取东方财富热榜选项数据失败:', error);
      // 设置默认值
      setMarkets(['A股市场', 'ETF基金', '港股市场', '美股市场']);
      setHotTypes(['人气榜', '飙升榜']);
    }
  };

  const fetchDataTypesList = async () => {
    try {
      console.log('获取数据类型列表...');
      const response = await fetchDataTypes();
      console.log('数据类型API响应:', response);
      
      if (response.data && response.data.data_types) {
        setDataTypes(response.data.data_types);
      } else {
        console.warn('数据类型API响应格式异常:', response);
        // 设置一些默认的数据类型
        setDataTypes(['热股', '涨停', '跌停', '龙虎榜', '资金流向']);
      }
    } catch (error) {
      console.error('获取数据类型失败:', error);
      // 设置默认数据类型
      setDataTypes(['热股', '涨停', '跌停', '龙虎榜', '资金流向']);
    }
  };

  const handleTableChange = (pagination) => {
    setPagination(pagination);
  };

  const handleSearch = () => {
    setPagination(prev => ({ ...prev, current: 1 }));
  };

  const handleReset = () => {
    setFilters({
      search: '',
      data_type: '热股',
      start_date: dayjs().format('YYYY-MM-DD'),
      end_date: ''
    });
    setPagination(prev => ({ ...prev, current: 1 }));
  };

  const handleAdd = () => {
    setEditingRecord(null);
    form.resetFields();
    setModalVisible(true);
  };

  const handleEdit = (record) => {
    setEditingRecord(record);
    form.setFieldsValue({
      ...record,
      trade_date: record.trade_date ? dayjs(record.trade_date) : null
    });
    setModalVisible(true);
  };

  const handleDelete = async (id) => {
    try {
      await deleteHotData(id);
      message.success('删除成功');
      fetchData();
    } catch (error) {
      message.error('删除失败');
    }
  };

  const handleModalOk = async () => {
    try {
      const values = await form.validateFields();
      
      if (editingRecord) {
        await updateHotData(editingRecord.id, values);
        message.success('更新成功');
      } else {
        await createHotData(values);
        message.success('创建成功');
      }
      
      setModalVisible(false);
      fetchData();
    } catch (error) {
      message.error('操作失败');
    }
  };

  // 东方财富热榜相关处理函数
  const handleDcHotTableChange = (pagination) => {
    setDcHotPagination(pagination);
  };

  const handleDcHotSearch = () => {
    setDcHotPagination(prev => ({ ...prev, current: 1 }));
  };

  const handleDcHotReset = () => {
    setDcHotFilters({
      search: '',
      market: 'A股市场',
      hot_type: '人气榜',
      start_date: dayjs().format('YYYY-MM-DD'),
      end_date: ''
    });
    setDcHotPagination(prev => ({ ...prev, current: 1 }));
  };

  const handleDcHotAdd = () => {
    setEditingDcHotRecord(null);
    dcHotForm.resetFields();
    setDcHotModalVisible(true);
  };

  const handleDcHotEdit = (record) => {
    setEditingDcHotRecord(record);
    dcHotForm.setFieldsValue({
      ...record,
      trade_date: record.trade_date ? dayjs(record.trade_date) : null
    });
    setDcHotModalVisible(true);
  };

  const handleDcHotDelete = async (id) => {
    try {
      await dcHotApi.deleteDcHot(id);
      message.success('删除成功');
      fetchDcHotData();
    } catch (error) {
      message.error('删除失败');
    }
  };

  const handleDcHotModalOk = async () => {
    try {
      const values = await dcHotForm.validateFields();
      
      if (editingDcHotRecord) {
        await dcHotApi.updateDcHot(editingDcHotRecord.id, values);
        message.success('更新成功');
      } else {
        await dcHotApi.createDcHot(values);
        message.success('创建成功');
      }
      
      setDcHotModalVisible(false);
      fetchDcHotData();
    } catch (error) {
      message.error('操作失败');
    }
  };

  const handleDcHotView = (record) => {
    Modal.info({
      title: `${record.ts_name} (${record.ts_code}) 详情`,
      width: 600,
      content: (
        <div>
          <Row gutter={16}>
            <Col span={12}>
              <Statistic title="排行" value={record.rank} />
            </Col>
            <Col span={12}>
              <Statistic title="市场" value={record.market} />
            </Col>
          </Row>
          <Row gutter={16}>
            <Col span={12}>
              <Statistic title="涨跌幅" value={record.pct_change} suffix="%" />
            </Col>
            <Col span={12}>
              <Statistic title="热点类型" value={record.hot_type} />
            </Col>
          </Row>
          <div style={{ marginTop: 16 }}>
            <Text strong>获取时间：</Text>
            <div style={{ marginTop: 8 }}>{record.rank_time || '-'}</div>
          </div>
        </div>
      )
    });
  };

  // 处理东方财富热榜行展开/收起
  const handleDcHotRowExpand = (expanded, record) => {
    const newExpandedRows = new Set(dcHotExpandedRows);
    if (expanded) {
      newExpandedRows.add(record.id);
    } else {
      newExpandedRows.delete(record.id);
    }
    setDcHotExpandedRows(newExpandedRows);
  };

  // 东方财富热榜展开行渲染函数
  const dcHotExpandedRowRender = (record) => {
    return (
      <div style={{ padding: '20px' }}>
        <Row gutter={[24, 24]}>
          <Col span={12}>
            <Card title="市场信息" size="small">
              <div style={{ 
                backgroundColor: '#f5f5f5', 
                padding: '16px', 
                borderRadius: '6px',
                minHeight: '100px'
              }}>
                <div><strong>市场：</strong>{record.market || '-'}</div>
                <div><strong>热点类型：</strong>{record.hot_type || '-'}</div>
                <div><strong>是否最新：</strong>{record.is_new === 'Y' ? '是' : '否'}</div>
                <div><strong>获取时间：</strong>{record.rank_time || '-'}</div>
              </div>
            </Card>
          </Col>
          <Col span={12}>
            <Card title="股票信息" size="small">
              <div style={{ 
                backgroundColor: '#f5f5f5', 
                padding: '16px', 
                borderRadius: '6px',
                minHeight: '100px'
              }}>
                <div><strong>股票代码：</strong>{record.ts_code || '-'}</div>
                <div><strong>股票名称：</strong>{record.ts_name || '-'}</div>
                <div><strong>数据类型：</strong>{record.data_type || '-'}</div>
                <div><strong>排行：</strong>{record.rank || '-'}</div>
              </div>
            </Card>
          </Col>
        </Row>
        <Row style={{ marginTop: '24px' }}>
          <Col span={24}>
            <Card title={`${record.ts_name} (${record.ts_code}) K线图`} size="small">
              <KLineChart 
                tsCode={record.ts_code} 
                height={400} 
                miniMode={false}
                lazyLoad={true}
                shouldLoad={true}
              />
            </Card>
          </Col>
        </Row>
      </div>
    );
  };

  // 处理行展开/收起
  const handleRowExpand = (expanded, record) => {
    const newExpandedRows = new Set(expandedRows);
    if (expanded) {
      newExpandedRows.add(record.id);
    } else {
      newExpandedRows.delete(record.id);
    }
    setExpandedRows(newExpandedRows);
  };

  // 展开行渲染函数
  const expandedRowRender = (record) => {
    return (
      <div style={{ padding: '20px' }}>
        <Row gutter={[24, 24]}>
          <Col span={12}>
            <Card title="上榜解读" size="small">
              <div style={{ 
                backgroundColor: '#f5f5f5', 
                padding: '16px', 
                borderRadius: '6px',
                minHeight: '100px',
                whiteSpace: 'pre-line',
                wordBreak: 'break-word',
                lineHeight: '1.6'
              }}>
                {record.rank_reason ? 
                  record.rank_reason.split('\\n').map((line, index) => (
                    <div key={index} style={{ marginBottom: index < record.rank_reason.split('\\n').length - 1 ? '8px' : '0' }}>
                      {line}
                    </div>
                  ))
                  : '暂无上榜解读信息'
                }
              </div>
            </Card>
          </Col>
          <Col span={12}>
            <Card title="股票标签" size="small">
              <div style={{ 
                backgroundColor: '#f5f5f5', 
                padding: '16px', 
                borderRadius: '6px',
                minHeight: '100px'
              }}>
                {record.concept ? (() => {
                  try {
                    const concepts = JSON.parse(record.concept);
                    return Array.isArray(concepts) ? 
                      concepts.map(c => <Tag key={c} color="blue" style={{ margin: '4px' }}>{c}</Tag>) : 
                      record.concept;
                  } catch {
                    return record.concept;
                  }
                })() : '暂无标签信息'}
              </div>
            </Card>
          </Col>
        </Row>
        <Row style={{ marginTop: '24px' }}>
          <Col span={24}>
            <Card title={`${record.ts_name} (${record.ts_code}) K线图`} size="small">
              <KLineChart 
                tsCode={record.ts_code} 
                height={400} 
                miniMode={false}
                lazyLoad={true}
                shouldLoad={true}
              />
            </Card>
          </Col>
        </Row>
      </div>
    );
  };

  const columns = [
    {
      title: '排行',
      dataIndex: 'rank',
      key: 'rank',
      width: 80,
      render: (rank) => (
        <Tag color={rank <= 3 ? '#f50' : rank <= 10 ? '#fa8c16' : '#52c41a'}>
          {rank}
        </Tag>
      )
    },
    {
      title: '股票代码',
      dataIndex: 'ts_code',
      key: 'ts_code',
      width: 120,
      render: (code) => <Text code>{code}</Text>
    },
    {
      title: '股票名称',
      dataIndex: 'ts_name',
      key: 'ts_name',
      width: 120
    },
    {
      title: '数据类型',
      dataIndex: 'data_type',
      key: 'data_type',
      width: 100,
      render: (type) => <Tag color="blue">{type}</Tag>
    },
    {
      title: '涨跌幅',
      dataIndex: 'pct_change',
      key: 'pct_change',
      width: 100,
      render: (value) => {
        if (value === null) return '-';
        // 修改颜色：上涨红色，下跌绿色
        const color = value >= 0 ? '#ff4d4f' : '#52c41a';
        return <Text style={{ color, fontWeight: 'bold' }}>{value >= 0 ? '+' : ''}{value}%</Text>;
      }
    },
    {
      title: '当前价格',
      dataIndex: 'current_price',
      key: 'current_price',
      width: 100,
      render: (value) => value || '-'
    },
    {
      title: '热度值',
      dataIndex: 'hot',
      key: 'hot',
      width: 120,
      render: (value) => {
        if (value === null) return '-';
        return value.toLocaleString();
      }
    },
    {
      title: '标签',
      dataIndex: 'concept',
      key: 'concept',
      width: 200,
      render: (concept) => {
        if (!concept) return '-';
        try {
          const concepts = JSON.parse(concept);
          return Array.isArray(concepts) ? concepts.map(c => <Tag key={c}>{c}</Tag>) : concept;
        } catch {
          return concept;
        }
      }
    },
    {
      title: '交易日期',
      dataIndex: 'trade_date',
      key: 'trade_date',
      width: 120
    },
    {
      title: '操作',
      key: 'action',
      width: 150,
      fixed: 'right',
      render: (_, record) => (
        <Space size="small">
          <Button
            type="link"
            icon={<EyeOutlined />}
            onClick={() => handleView(record)}
            size="small"
          >
            查看
          </Button>
          <Button
            type="link"
            icon={<EditOutlined />}
            onClick={() => handleEdit(record)}
            size="small"
          >
            编辑
          </Button>
          <Button
            type="link"
            danger
            icon={<DeleteOutlined />}
            onClick={() => handleDelete(record.id)}
            size="small"
          >
            删除
          </Button>
        </Space>
      )
    }
  ];

  // 东方财富热榜列配置
  const dcHotColumns = [
    {
      title: '排行',
      dataIndex: 'rank',
      key: 'rank',
      width: 80,
      render: (rank) => (
        <Tag color={rank <= 3 ? '#f50' : rank <= 10 ? '#fa8c16' : '#52c41a'}>
          {rank}
        </Tag>
      )
    },
    {
      title: '股票代码',
      dataIndex: 'ts_code',
      key: 'ts_code',
      width: 120,
      render: (code) => <Text code>{code}</Text>
    },
    {
      title: '股票名称',
      dataIndex: 'ts_name',
      key: 'ts_name',
      width: 120
    },
    {
      title: '市场',
      dataIndex: 'market',
      key: 'market',
      width: 100,
      render: (market) => <Tag color="purple">{market}</Tag>
    },
    {
      title: '热点类型',
      dataIndex: 'hot_type',
      key: 'hot_type',
      width: 100,
      render: (type) => <Tag color="cyan">{type}</Tag>
    },
    {
      title: '涨跌幅',
      dataIndex: 'pct_change',
      key: 'pct_change',
      width: 100,
      render: (value) => {
        if (value === null) return '-';
        // 修改颜色：上涨红色，下跌绿色
        const color = value >= 0 ? '#ff4d4f' : '#52c41a';
        return <Text style={{ color, fontWeight: 'bold' }}>{value >= 0 ? '+' : ''}{value}%</Text>;
      }
    },
    {
      title: '当前价格',
      dataIndex: 'current_price',
      key: 'current_price',
      width: 100,
      render: (value) => value || '-'
    },
    {
      title: '数据类型',
      dataIndex: 'data_type',
      key: 'data_type',
      width: 100,
      render: (type) => <Tag color="blue">{type}</Tag>
    },
    {
      title: '获取时间',
      dataIndex: 'rank_time',
      key: 'rank_time',
      width: 120
    },
    {
      title: '交易日期',
      dataIndex: 'trade_date',
      key: 'trade_date',
      width: 120
    },
    {
      title: '操作',
      key: 'action',
      width: 150,
      fixed: 'right',
      render: (_, record) => (
        <Space size="small">
          <Button
            type="link"
            icon={<EyeOutlined />}
            onClick={() => handleDcHotView(record)}
            size="small"
          >
            查看
          </Button>
          <Button
            type="link"
            icon={<EditOutlined />}
            onClick={() => handleDcHotEdit(record)}
            size="small"
          >
            编辑
          </Button>
          <Button
            type="link"
            danger
            icon={<DeleteOutlined />}
            onClick={() => handleDcHotDelete(record.id)}
            size="small"
          >
            删除
          </Button>
        </Space>
      )
    }
  ];

  const handleView = (record) => {
    Modal.info({
      title: `${record.ts_name} (${record.ts_code}) 详情`,
      width: 600,
      content: (
        <div>
          <Row gutter={16}>
            <Col span={12}>
              <Statistic title="排行" value={record.rank} />
            </Col>
            <Col span={12}>
              <Statistic title="数据类型" value={record.data_type} />
            </Col>
          </Row>
          <Row gutter={16}>
            <Col span={12}>
              <Statistic title="涨跌幅" value={record.pct_change} suffix="%" />
            </Col>
            <Col span={12}>
              <Statistic title="热度值" value={record.hot} />
            </Col>
          </Row>
          <div style={{ marginTop: 16 }}>
            <Text strong>标签：</Text>
            {record.concept && (
              <div style={{ marginTop: 8 }}>
                {(() => {
                  try {
                    const concepts = JSON.parse(record.concept);
                    return Array.isArray(concepts) ? concepts.map(c => <Tag key={c}>{c}</Tag>) : record.concept;
                  } catch {
                    return record.concept;
                  }
                })()}
              </div>
            )}
          </div>
          <div style={{ marginTop: 16 }}>
            <Text strong>上榜解读：</Text>
            <div style={{ marginTop: 8 }}>{record.rank_reason || '-'}</div>
          </div>
        </div>
      )
    });
  };

  return (
    <div style={{ padding: '24px' }}>
      <Title level={2}>热榜数据管理</Title>
      
      <Tabs
        defaultActiveKey="ths"
        items={[
          {
            key: 'ths',
            label: '同花顺热榜',
            children: (
              <>
                {/* 搜索和过滤区域 */}
                <Card style={{ marginBottom: '24px' }}>
                  <Row gutter={16} align="middle">
                    <Col span={6}>
                      <Input
                        placeholder="搜索股票代码、名称或标签"
                        value={filters.search}
                        onChange={(e) => setFilters(prev => ({ ...prev, search: e.target.value }))}
                        prefix={<SearchOutlined />}
                      />
                    </Col>
                    <Col span={4}>
                      <Select
                        placeholder="数据类型"
                        value={filters.data_type}
                        onChange={(value) => setFilters(prev => ({ ...prev, data_type: value }))}
                        allowClear
                        style={{ width: '100%' }}
                      >
                        {dataTypes.map(type => (
                          <Option key={type} value={type}>{type}</Option>
                        ))}
                      </Select>
                    </Col>
                    <Col span={4}>
                      <DatePicker
                        placeholder="开始日期"
                        value={filters.start_date ? dayjs(filters.start_date) : null}
                        onChange={(date) => setFilters(prev => ({ ...prev, start_date: date ? date.format('YYYY-MM-DD') : '' }))}
                        style={{ width: '100%' }}
                      />
                    </Col>
                    <Col span={4}>
                      <DatePicker
                        placeholder="结束日期"
                        value={filters.end_date ? dayjs(filters.end_date) : null}
                        onChange={(date) => setFilters(prev => ({ ...prev, end_date: date ? date.format('YYYY-MM-DD') : '' }))}
                        style={{ width: '100%' }}
                      />
                    </Col>
                    <Col span={6}>
                      <Space>
                        <Button type="primary" onClick={handleSearch} icon={<SearchOutlined />}>
                          搜索
                        </Button>
                        <Button onClick={handleReset}>重置</Button>
                        <Button onClick={handleAdd} type="primary" icon={<PlusOutlined />}>
                          新增
                        </Button>
                        <Button onClick={fetchData} icon={<ReloadOutlined />}>
                          刷新
                        </Button>
                      </Space>
                    </Col>
                  </Row>
                </Card>

                {/* 数据表格 */}
                <Card>
                  {loading ? (
                    <div style={{ textAlign: 'center', padding: '40px' }}>
                      <Spin size="large" />
                      <div style={{ marginTop: '16px' }}>正在加载同花顺热榜数据...</div>
                    </div>
                  ) : dataSource.length === 0 ? (
                    <div style={{ textAlign: 'center', padding: '40px', color: '#999' }}>
                      <div>暂无数据</div>
                      <div style={{ marginTop: '8px', fontSize: '14px' }}>
                        请检查网络连接或联系管理员
                      </div>
                    </div>
                  ) : (
                    <Table
                      columns={columns}
                      dataSource={dataSource}
                      loading={false}
                      pagination={{
                        ...pagination,
                        showSizeChanger: true,
                        showQuickJumper: true,
                        showTotal: (total, range) => `第 ${range[0]}-${range[1]} 条，共 ${total} 条`
                      }}
                      onChange={handleTableChange}
                      rowKey="id"
                      scroll={{ x: 1500 }}
                      size="small"
                      expandable={{
                        expandedRowRender,
                        expandedRowKeys: Array.from(expandedRows),
                        onExpand: handleRowExpand,
                        expandRowByClick: true
                      }}
                    />
                  )}
                </Card>
              </>
            )
          },
          {
            key: 'dc',
            label: '东方财富热榜',
            children: (
              <>
                {/* 搜索和过滤区域 */}
                <Card style={{ marginBottom: '24px' }}>
                  <Row gutter={16} align="middle">
                    <Col span={5}>
                      <Input
                        placeholder="搜索股票代码、名称"
                        value={dcHotFilters.search}
                        onChange={(e) => setDcHotFilters(prev => ({ ...prev, search: e.target.value }))}
                        prefix={<SearchOutlined />}
                      />
                    </Col>
                    <Col span={4}>
                      <Select
                        placeholder="市场类型"
                        value={dcHotFilters.market}
                        onChange={(value) => setDcHotFilters(prev => ({ ...prev, market: value }))}
                        style={{ width: '100%' }}
                      >
                        {markets.map(market => (
                          <Option key={market} value={market}>{market}</Option>
                        ))}
                      </Select>
                    </Col>
                    <Col span={4}>
                      <Select
                        placeholder="热点类型"
                        value={dcHotFilters.hot_type}
                        onChange={(value) => setDcHotFilters(prev => ({ ...prev, hot_type: value }))}
                        style={{ width: '100%' }}
                      >
                        {hotTypes.map(type => (
                          <Option key={type} value={type}>{type}</Option>
                        ))}
                      </Select>
                    </Col>
                    <Col span={4}>
                      <DatePicker
                        placeholder="开始日期"
                        value={dcHotFilters.start_date ? dayjs(dcHotFilters.start_date) : null}
                        onChange={(date) => setDcHotFilters(prev => ({ ...prev, start_date: date ? date.format('YYYY-MM-DD') : '' }))}
                        style={{ width: '100%' }}
                      />
                    </Col>
                    <Col span={4}>
                      <DatePicker
                        placeholder="结束日期"
                        value={dcHotFilters.end_date ? dayjs(dcHotFilters.end_date) : null}
                        onChange={(date) => setDcHotFilters(prev => ({ ...prev, end_date: date ? date.format('YYYY-MM-DD') : '' }))}
                        style={{ width: '100%' }}
                      />
                    </Col>
                    <Col span={3}>
                      <Space>
                        <Button type="primary" onClick={handleDcHotSearch} icon={<SearchOutlined />}>
                          搜索
                        </Button>
                        <Button onClick={handleDcHotReset}>重置</Button>
                        <Button onClick={handleDcHotAdd} type="primary" icon={<PlusOutlined />}>
                          新增
                        </Button>
                        <Button onClick={fetchDcHotData} icon={<ReloadOutlined />}>
                          刷新
                        </Button>
                      </Space>
                    </Col>
                  </Row>
                </Card>

                {/* 数据表格 */}
                <Card>
                  {dcHotLoading ? (
                    <div style={{ textAlign: 'center', padding: '40px' }}>
                      <Spin size="large" />
                      <div style={{ marginTop: '16px' }}>正在加载东方财富热榜数据...</div>
                    </div>
                  ) : dcHotDataSource.length === 0 ? (
                    <div style={{ textAlign: 'center', padding: '40px', color: '#999' }}>
                      <div>暂无数据</div>
                      <div style={{ marginTop: '8px', fontSize: '14px' }}>
                        请检查网络连接或联系管理员
                      </div>
                    </div>
                  ) : (
                    <Table
                      columns={dcHotColumns}
                      dataSource={dcHotDataSource}
                      loading={false}
                      pagination={{
                        ...dcHotPagination,
                        showSizeChanger: true,
                        showQuickJumper: true,
                        showTotal: (total, range) => `第 ${range[0]}-${range[1]} 条，共 ${total} 条`
                      }}
                      onChange={handleDcHotTableChange}
                      rowKey="id"
                      scroll={{ x: 1500 }}
                      size="small"
                      expandable={{
                        expandedRowRender: dcHotExpandedRowRender,
                        expandedRowKeys: Array.from(dcHotExpandedRows),
                        onExpand: handleDcHotRowExpand,
                        expandRowByClick: true
                      }}
                    />
                  )}
                </Card>
              </>
            )
          }
        ]}
      />

      {/* 新增/编辑模态框 */}
      <Modal
        title={editingRecord ? '编辑热榜数据' : '新增热榜数据'}
        open={modalVisible}
        onOk={handleModalOk}
        onCancel={() => setModalVisible(false)}
        width={600}
      >
        <Form
          form={form}
          layout="vertical"
          initialValues={{
            data_type: '热股',
            rank: 1
          }}
        >
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                name="trade_date"
                label="交易日期"
                rules={[{ required: true, message: '请选择交易日期' }]}
              >
                <DatePicker style={{ width: '100%' }} />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                name="data_type"
                label="数据类型"
                rules={[{ required: true, message: '请选择数据类型' }]}
              >
                <Select>
                  {dataTypes.map(type => (
                    <Option key={type} value={type}>{type}</Option>
                  ))}
                </Select>
              </Form.Item>
            </Col>
          </Row>
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                name="ts_code"
                label="股票代码"
                rules={[{ required: true, message: '请输入股票代码' }]}
              >
                <Input placeholder="如：000001.SZ" />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                name="ts_name"
                label="股票名称"
                rules={[{ required: true, message: '请输入股票名称' }]}
              >
                <Input placeholder="如：平安银行" />
              </Form.Item>
            </Col>
          </Row>
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                name="rank"
                label="排行"
                rules={[{ required: true, message: '请输入排行' }]}
              >
                <InputNumber min={1} style={{ width: '100%' }} />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                name="pct_change"
                label="涨跌幅(%)"
              >
                <InputNumber step={0.01} style={{ width: '100%' }} />
              </Form.Item>
            </Col>
          </Row>
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                name="current_price"
                label="当前价格"
              >
                <InputNumber step={0.01} style={{ width: '100%' }} />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                name="hot"
                label="热度值"
              >
                <InputNumber style={{ width: '100%' }} />
              </Form.Item>
            </Col>
          </Row>
          <Form.Item
            name="concept"
            label="标签"
          >
            <Input placeholder="如：银行,金融科技" />
          </Form.Item>
          <Form.Item
            name="rank_reason"
            label="上榜解读"
          >
            <TextArea rows={3} placeholder="请输入上榜解读" />
          </Form.Item>
          <Form.Item
            name="rank_time"
            label="排行榜获取时间"
          >
            <Input placeholder="如：09:30:00" />
          </Form.Item>
        </Form>
      </Modal>

      {/* 东方财富热榜新增/编辑模态框 */}
      <Modal
        title={editingDcHotRecord ? '编辑东方财富热榜数据' : '新增东方财富热榜数据'}
        open={dcHotModalVisible}
        onOk={handleDcHotModalOk}
        onCancel={() => setDcHotModalVisible(false)}
        width={600}
      >
        <Form
          form={dcHotForm}
          layout="vertical"
          initialValues={{
            market: 'A股市场',
            hot_type: '人气榜',
            is_new: 'Y'
          }}
        >
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                name="trade_date"
                label="交易日期"
                rules={[{ required: true, message: '请选择交易日期' }]}
              >
                <DatePicker style={{ width: '100%' }} />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                name="market"
                label="市场类型"
                rules={[{ required: true, message: '请选择市场类型' }]}
              >
                <Select>
                  {markets.map(market => (
                    <Option key={market} value={market}>{market}</Option>
                  ))}
                </Select>
              </Form.Item>
            </Col>
          </Row>
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                name="hot_type"
                label="热点类型"
                rules={[{ required: true, message: '请选择热点类型' }]}
              >
                <Select>
                  {hotTypes.map(type => (
                    <Option key={type} value={type}>{type}</Option>
                  ))}
                </Select>
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                name="is_new"
                label="是否最新"
                rules={[{ required: true, message: '请选择是否最新' }]}
              >
                <Select>
                  <Option value="Y">是</Option>
                  <Option value="N">否</Option>
                </Select>
              </Form.Item>
            </Col>
          </Row>
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                name="ts_code"
                label="股票代码"
                rules={[{ required: true, message: '请输入股票代码' }]}
              >
                <Input placeholder="如：000001.SZ" />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                name="ts_name"
                label="股票名称"
                rules={[{ required: true, message: '请输入股票名称' }]}
              >
                <Input placeholder="如：平安银行" />
              </Form.Item>
            </Col>
          </Row>
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                name="rank"
                label="排行"
                rules={[{ required: true, message: '请输入排行' }]}
              >
                <InputNumber min={1} style={{ width: '100%' }} />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                name="pct_change"
                label="涨跌幅(%)"
              >
                <InputNumber step={0.01} style={{ width: '100%' }} />
              </Form.Item>
            </Col>
          </Row>
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                name="current_price"
                label="当前价格"
              >
                <InputNumber step={0.01} style={{ width: '100%' }} />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                name="data_type"
                label="数据类型"
                rules={[{ required: true, message: '请输入数据类型' }]}
              >
                <Input placeholder="如：热榜" />
              </Form.Item>
            </Col>
          </Row>
          <Form.Item
            name="rank_time"
            label="排行榜获取时间"
          >
            <Input placeholder="如：09:30:00" />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default ThsHotPage; 