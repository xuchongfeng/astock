import React, { useEffect, useState } from 'react';
import { Table, Card, Input, DatePicker, Button, Form, message, Tag, Collapse, Spin } from 'antd';
import { thsIndexApi } from '../api/thsIndexApi';
import { thsMemberApi } from '../api/thsMemberApi';
import { formatDate } from '../utils/formatters';
import { CaretRightOutlined, CaretDownOutlined } from '@ant-design/icons';
import moment from 'moment';

const { Panel } = Collapse;

const ThsIndexPage = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [pagination, setPagination] = useState({ current: 1, pageSize: 20, total: 0 });
  const [form] = Form.useForm();
  const [expandedRows, setExpandedRows] = useState(new Set());
  const [memberData, setMemberData] = useState({});
  const [memberLoading, setMemberLoading] = useState({});
  
  // 设置默认日期为今天
  const defaultDate = moment();
  
  // 设置默认排序为涨跌幅倒序
  const [sorter, setSorter] = useState({ field: 'pct_change', order: 'descend' });

  const fetchData = async (params = {}) => {
    setLoading(true);
    try {
      // 处理查询参数，格式化日期字段
      const queryParams = { ...params };
      if (queryParams.filters && queryParams.filters.trade_date) {
        // 将 moment 对象格式化为 YYYY-MM-DD 字符串
        queryParams.filters.trade_date = queryParams.filters.trade_date.format('YYYY-MM-DD');
      }
      
      // 构建API请求参数
      const apiParams = {
        page: queryParams.page || pagination.current,
        page_size: queryParams.pageSize || pagination.pageSize,
        ...queryParams.filters
      };
      
      // 添加排序参数
      if (queryParams.sortField && queryParams.sortOrder) {
        const sortPrefix = queryParams.sortOrder === 'descend' ? '-' : '';
        apiParams.sort_fields = `${sortPrefix}${queryParams.sortField}`;
      }
      
      const res = await thsIndexApi.getList(apiParams);
      setData(res.data.data);
      setPagination({
        current: queryParams.page || pagination.current,
        pageSize: queryParams.pageSize || pagination.pageSize,
        total: res.data.total
      });
    } catch (e) {
      message.error('加载数据失败');
    }
    setLoading(false);
  };

  // 获取概念成分股数据
  const fetchMemberData = async (ts_code) => {
    console.log('开始获取成分股数据:', ts_code);
    
    if (memberData[ts_code]) {
      console.log('成分股数据已缓存，直接返回:', ts_code);
      return; // 如果已经加载过，直接返回
    }

    setMemberLoading(prev => ({ ...prev, [ts_code]: true }));
    try {
      console.log('发送API请求获取成分股:', ts_code);
      
      // 获取当前选中的交易日期，如果没有则使用最新日期
      const selectedDate = form.getFieldValue('trade_date');
      let tradeDate = null;
      
      if (selectedDate) {
        tradeDate = selectedDate.format('YYYY-MM-DD');
      } else {
        // 如果没有选择日期，使用当前记录的交易日期
        const currentRecord = data.find(item => item.ts_code === ts_code);
        if (currentRecord && currentRecord.trade_date) {
          tradeDate = currentRecord.trade_date;
        }
      }
      
      console.log('使用交易日期:', tradeDate);
      
      const res = await thsMemberApi.getByTsCode(ts_code, { 
        page_size: 100,
        trade_date: tradeDate
      });
      console.log('成分股API响应:', res);
      
      if (res.data && res.data.data) {
        console.log('成分股数据:', res.data.data);
        console.log('成分股数据获取成功:', ts_code, '数量:', res.data.data.length);
        setMemberData(prev => ({ ...prev, [ts_code]: res.data.data }));
      } else {
        console.warn('成分股API响应格式异常:', res);
        setMemberData(prev => ({ ...prev, [ts_code]: [] }));
      }
    } catch (e) {
      console.error('获取成分股数据失败:', ts_code, e);
      message.error(`加载成分股数据失败: ${e.message || '未知错误'}`);
      setMemberData(prev => ({ ...prev, [ts_code]: [] }));
    } finally {
      setMemberLoading(prev => ({ ...prev, [ts_code]: false }));
    }
  };

  // 处理行展开
  const handleExpand = (expanded, record) => {
    console.log('行展开事件:', expanded, record);
    
    if (expanded) {
      // 展开时加载成分股数据
      console.log('展开行，开始加载成分股:', record.ts_code);
      fetchMemberData(record.ts_code);
    }
    
    // 使用与rowKey相同的格式作为展开行的标识
    const rowKey = `${record.ts_code}-${record.trade_date}`;
    const newExpandedRows = new Set(expandedRows);
    if (expanded) {
      newExpandedRows.add(rowKey);
    } else {
      newExpandedRows.delete(rowKey);
    }
    setExpandedRows(newExpandedRows);
    console.log('更新展开行状态:', Array.from(newExpandedRows));
  };

  useEffect(() => {
    // 设置表单默认值
    form.setFieldsValue({
      trade_date: defaultDate
    });
    
    // 使用默认日期和默认排序获取数据
    fetchData({ 
      page: 1, 
      filters: { trade_date: defaultDate },
      sortField: sorter.field,
      sortOrder: sorter.order
    });
    // eslint-disable-next-line
  }, []);

  const handleTableChange = (pag, filters, sorterObj) => {
    // 构建排序参数
    let sortField = null;
    let sortOrder = null;
    
    if (sorterObj && sorterObj.field && sorterObj.order) {
      sortField = sorterObj.field;
      sortOrder = sorterObj.order;
      // 更新排序状态
      setSorter({ field: sortField, order: sortOrder });
    }
    
    fetchData({
      page: pag.current,
      pageSize: pag.pageSize,
      filters: form.getFieldsValue(),
      sortField: sortField,
      sortOrder: sortOrder
    });
  };

  const handleSearch = () => {
    fetchData({ page: 1, filters: form.getFieldsValue() });
  };

  const handleClearFilters = () => {
    form.resetFields();
    // 重置后重新设置默认日期
    form.setFieldsValue({
      trade_date: defaultDate
    });
    // 重置排序状态到默认值
    setSorter({ field: 'pct_change', order: 'descend' });
    fetchData({ 
      page: 1, 
      filters: { trade_date: defaultDate },
      sortField: 'pct_change',
      sortOrder: 'descend'
    });
  };

  // 获取涨跌颜色
  const getChangeColor = (change, pct_change) => {
    if (change > 0 || pct_change > 0) return '#f5222d';
    if (change < 0 || pct_change < 0) return '#52c41a';
    return '#666';
  };

  // 成分股表格列定义
  const memberColumns = [
    {
      title: '股票代码',
      dataIndex: 'con_code',
      key: 'con_code',
      width: 120,
      render: (text) => <Tag color="blue">{text}</Tag>
    },
    {
      title: '股票名称',
      dataIndex: 'con_name',
      key: 'con_name',
      width: 150
    },
    {
      title: '涨跌幅',
      dataIndex: 'pct_chg',
      key: 'pct_chg',
      width: 100,
      align: 'right',
      render: (value, record) => {
        if (value === null || value === undefined) return '-';
        const color = value > 0 ? '#f5222d' : value < 0 ? '#52c41a' : '#666';
        return (
          <span style={{ color, fontWeight: 'bold' }}>
            {value > 0 ? '+' : ''}{Number(value).toFixed(2)}%
          </span>
        );
      }
    },
    {
      title: '涨跌额',
      dataIndex: 'change',
      key: 'change',
      width: 100,
      align: 'right',
      render: (value, record) => {
        if (value === null || value === undefined) return '-';
        const color = value > 0 ? '#f5222d' : value < 0 ? '#52c41a' : '#666';
        return (
          <span style={{ color, fontWeight: 'bold' }}>
            {value > 0 ? '+' : ''}{Number(value).toFixed(2)}
          </span>
        );
      }
    },
    {
      title: '收盘价',
      dataIndex: 'close',
      key: 'close',
      width: 100,
      align: 'right',
      render: (value) => value ? Number(value).toFixed(2) : '-'
    },
    {
      title: '昨收价',
      dataIndex: 'pre_close',
      key: 'pre_close',
      width: 100,
      align: 'right',
      render: (value) => value ? Number(value).toFixed(2) : '-'
    },
    {
      title: '成交量',
      dataIndex: 'vol',
      key: 'vol',
      width: 100,
      align: 'right',
      render: (value) => value ? `${(Number(value) / 100).toFixed(0)}手` : '-'
    },
    {
      title: '成交额',
      dataIndex: 'amount',
      key: 'amount',
      width: 120,
      align: 'right',
      render: (value) => value ? `${(Number(value) / 10000).toFixed(2)}万` : '-'
    },
    {
      title: '换手率',
      dataIndex: 'turnover_rate',
      key: 'turnover_rate',
      width: 100,
      align: 'right',
      render: (value) => value ? `${Number(value).toFixed(2)}%` : '-'
    },
    {
      title: '权重',
      dataIndex: 'weight',
      key: 'weight',
      width: 100,
      align: 'right',
      render: (value) => value ? `${Number(value).toFixed(2)}%` : '-'
    },
    {
      title: '纳入日期',
      dataIndex: 'in_date',
      key: 'in_date',
      width: 120,
      render: (value) => formatDate(value, 'YYYY-MM-DD')
    },
    {
      title: '剔除日期',
      dataIndex: 'out_date',
      key: 'out_date',
      width: 120,
      render: (value) => formatDate(value, 'YYYY-MM-DD')
    },
    {
      title: '是否最新',
      dataIndex: 'is_new',
      key: 'is_new',
      width: 100,
      render: (value) => (
        <Tag color={value === 'Y' ? 'green' : 'orange'}>
          {value === 'Y' ? '是' : '否'}
        </Tag>
      )
    }
  ];

  const columns = [
    { 
      title: '概念板块名称', 
      key: 'concept_name', 
      width: 200,
      render: (_, record) => (
        <div>
          <div style={{ fontWeight: 'bold', marginBottom: 4 }}>
            {record.name || '未知概念板块'}
          </div>
          <Tag color="blue" style={{ fontSize: '12px' }}>
            {record.ts_code}
          </Tag>
        </div>
      )
    },
    { 
      title: '交易日', 
      dataIndex: 'trade_date', 
      key: 'trade_date', 
      width: 110,
      render: (value) => formatDate(value, 'YYYY-MM-DD')
    },
    { 
      title: '涨跌幅', 
      dataIndex: 'pct_change', 
      key: 'pct_change', 
      align: 'right',
      width: 100,
      sorter: true,
      render: (val, record) => (
        <span style={{ 
          color: getChangeColor(record.change, val),
          fontWeight: 'bold',
          fontSize: '14px'
        }}>
          {val ? `${val > 0 ? '+' : ''}${Number(val).toFixed(2)}%` : '-'}
        </span>
      )
    },
    { 
      title: '涨跌点位', 
      dataIndex: 'change', 
      key: 'change', 
      align: 'right',
      width: 100,
      render: (val, record) => (
        <span style={{ 
          color: getChangeColor(val, record.pct_change),
          fontWeight: 'bold'
        }}>
          {val ? `${val > 0 ? '+' : ''}${Number(val).toFixed(2)}` : '-'}
        </span>
      )
    },
    { 
      title: '收盘点位', 
      dataIndex: 'close', 
      key: 'close', 
      align: 'right', 
      width: 100,
      render: (value) => value ? Number(value).toFixed(2) : '-'
    },
    { 
      title: '开盘点位', 
      dataIndex: 'open', 
      key: 'open', 
      align: 'right', 
      width: 100,
      render: (value) => value ? Number(value).toFixed(2) : '-'
    },
    { 
      title: '最高点位', 
      dataIndex: 'high', 
      key: 'high', 
      align: 'right', 
      width: 100,
      render: (value) => value ? Number(value).toFixed(2) : '-'
    },
    { 
      title: '最低点位', 
      dataIndex: 'low', 
      key: 'low', 
      align: 'right', 
      width: 100,
      render: (value) => value ? Number(value).toFixed(2) : '-'
    },
    { 
      title: '昨日收盘点', 
      dataIndex: 'pre_close', 
      key: 'pre_close', 
      align: 'right', 
      width: 100,
      render: (value) => value ? Number(value).toFixed(2) : '-'
    },
    { 
      title: '平均价', 
      dataIndex: 'avg_price', 
      key: 'avg_price', 
      align: 'right', 
      width: 100,
      render: (value) => value ? Number(value).toFixed(2) : '-'
    },
    { 
      title: '成交量', 
      dataIndex: 'vol', 
      key: 'vol', 
      align: 'right', 
      width: 100,
      sorter: true,
      render: (value) => value ? `${(value / 10000).toFixed(2)}万` : '-'
    },
    { 
      title: '换手率', 
      dataIndex: 'turnover_rate', 
      key: 'turnover_rate', 
      align: 'right', 
      width: 100,
      render: (value) => value ? `${Number(value).toFixed(2)}%` : '-'
    },
    { 
      title: '总市值', 
      dataIndex: 'total_mv', 
      key: 'total_mv', 
      align: 'right', 
      width: 120,
      render: (value) => value ? `${(Number(value) / 100000000).toFixed(2)}亿` : '-'
    },
    { 
      title: '流通市值', 
      dataIndex: 'float_mv', 
      key: 'float_mv', 
      align: 'right', 
      width: 120,
      render: (value) => value ? `${(Number(value) / 100000000).toFixed(2)}亿` : '-'
    },
    { 
      title: '创建时间', 
      dataIndex: 'created_at', 
      key: 'created_at', 
      width: 120,
      render: (value) => formatDate(value, 'YYYY-MM-DD')
    },
    { 
      title: '更新时间', 
      dataIndex: 'updated_at', 
      key: 'updated_at', 
      width: 120,
      render: (value) => formatDate(value, 'YYYY-MM-DD')
    },
  ];

  // 展开行渲染
  const expandedRowRender = (record) => {
    console.log('渲染展开行:', record);
    const members = memberData[record.ts_code] || [];
    const isLoading = memberLoading[record.ts_code];
    
    console.log('渲染展开行:', record.ts_code, {
      members: members,
      memberCount: members.length,
      isLoading: isLoading,
      memberDataKeys: Object.keys(memberData),
      recordTsCode: record.ts_code
    });
    
    if (isLoading) {
      console.log('显示加载状态:', record.ts_code);
      return (
        <div style={{ padding: '20px', textAlign: 'center' }}>
          <Spin size="small" />
          <div style={{ marginTop: '10px' }}>加载成分股数据中...</div>
        </div>
      );
    }

    if (members.length === 0) {
      console.log('显示空数据状态:', record.ts_code);
      return (
        <div style={{ padding: '20px', textAlign: 'center', color: '#999' }}>
          暂无成分股数据
        </div>
      );
    }

    console.log('显示成分股表格:', record.ts_code, '数量:', members.length);
    return (
      <div style={{ padding: '0 20px 20px 20px' }}>
        <div style={{ marginBottom: '16px', fontWeight: 'bold', color: '#1890ff' }}>
          {record.name || record.ts_code} 成分股列表 ({members.length}只)
          {record.trade_date && (
            <span style={{ marginLeft: '16px', fontSize: '14px', color: '#666' }}>
              交易日期: {record.trade_date}
            </span>
          )}
        </div>
        <Table
          columns={memberColumns}
          dataSource={members}
          rowKey="con_code"
          pagination={false}
          size="small"
          bordered
          scroll={{ x: 'max-content' }}
        />
      </div>
    );
  };

  return (
    <div style={{ padding: 24 }}>
      <Card title="同花顺概念板块行情">
        <Form form={form} layout="inline" style={{ marginBottom: 16 }}>
          <Form.Item name="ts_code" label="概念板块代码">
            <Input placeholder="如 885001.TI" style={{ width: 160 }} />
          </Form.Item>
          <Form.Item name="trade_date" label="交易日">
            <DatePicker 
              style={{ width: 140 }} 
              placeholder="选择交易日期"
              allowClear={false}
            />
          </Form.Item>
          <Form.Item>
            <Button type="primary" onClick={handleSearch} style={{ marginRight: 8 }}>
              查询
            </Button>
            <Button onClick={handleClearFilters}>
              清除筛选
            </Button>
          </Form.Item>
        </Form>
        <Table
          columns={columns}
          dataSource={data}
          rowKey={record => `${record.ts_code}-${record.trade_date}`}
          loading={loading}
          expandable={{
            expandedRowRender,
            expandedRowKeys: Array.from(expandedRows),
            onExpand: handleExpand,
            expandIcon: ({ expanded, onExpand, record }) => (
              <span onClick={(e) => onExpand(record, e)}>
                {expanded ? <CaretDownOutlined /> : <CaretRightOutlined />}
              </span>
            ),
            expandIconColumnIndex: 0
          }}
          pagination={{
            ...pagination,
            showSizeChanger: true,
            showQuickJumper: true,
            showTotal: (total, range) => `第 ${range[0]}-${range[1]} 条，共 ${total} 条`
          }}
          onChange={handleTableChange}
          scroll={{ x: 'max-content' }}
          bordered
          size="middle"
          defaultSortOrder="descend"
        />
      </Card>
    </div>
  );
};

export default ThsIndexPage; 