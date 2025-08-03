import React, { useState, useEffect } from 'react';
import { 
  Card, 
  Tabs, 
  Table, 
  Button, 
  Modal, 
  Form, 
  Input, 
  DatePicker, 
  Select, 
  InputNumber, 
  message, 
  Popconfirm, 
  Spin,
  Typography,
  Row,
  Col,
  Statistic
} from 'antd';
import { 
  PlusOutlined, 
  EditOutlined, 
  DeleteOutlined,
  LineChartOutlined,
  PieChartOutlined
} from '@ant-design/icons';
import { userPositionApi } from '../api/userPositionApi';
import { userTradeApi } from '../api/userTradeApi';
import { stockApi } from '../api/stockApi';
import { formatDate, formatCurrency, formatPercent } from '../utils/formatters';
import KLineChart from '../components/KLineChart';
import ReactECharts from 'echarts-for-react';
import StockTags from '../components/StockTags';
import moment from 'moment';

const { Title } = Typography;
const { TabPane } = Tabs;
const { Option } = Select;

const UserPortfolioPage = () => {
  const userId = localStorage.getItem('userId') || 1;
  
  // 持仓相关状态
  const [positions, setPositions] = useState([]);
  const [positionLoading, setPositionLoading] = useState(false);
  const [positionModalVisible, setPositionModalVisible] = useState(false);
  const [editingPosition, setEditingPosition] = useState(null);
  const [positionForm] = Form.useForm();
  
  // 交易记录相关状态
  const [trades, setTrades] = useState([]);
  const [tradeLoading, setTradeLoading] = useState(false);
  const [tradeModalVisible, setTradeModalVisible] = useState(false);
  const [editingTrade, setEditingTrade] = useState(null);
  const [tradeForm] = Form.useForm();
  
  // 股票搜索相关状态
  const [stockOptions, setStockOptions] = useState([]);
  const [stockSearchLoading, setStockSearchLoading] = useState(false);
  
  // 持仓统计
  const [positionStats, setPositionStats] = useState({
    totalValue: 0,
    totalCost: 0,
    totalProfit: 0,
    profitRate: 0
  });

  useEffect(() => {
    fetchPositions();
    fetchTrades();
  }, [userId]);

  // 搜索股票
  const handleStockSearch = async (value) => {
    if (!value || value.length < 2) {
      setStockOptions([]);
      return;
    }
    
    setStockSearchLoading(true);
    try {
      const response = await stockApi.getCompanies({ search: value, page_size: 20 });
      const stocks = response.data.data || [];
      const options = stocks.map(stock => ({
        value: stock.ts_code,
        label: `${stock.ts_code} - ${stock.name}`
      }));
      setStockOptions(options);
    } catch (error) {
      console.error('搜索股票失败:', error);
      setStockOptions([]);
    } finally {
      setStockSearchLoading(false);
    }
  };

  // 获取持仓数据
  const fetchPositions = async () => {
    setPositionLoading(true);
    try {
      const response = await userPositionApi.getPositions(userId);
      const data = response.data.data || [];
      setPositions(data);
      
      // 计算持仓统计
      const totalCost = data.reduce((sum, item) => sum + (item.quantity * item.avg_price), 0);
      const totalValue = data.reduce((sum, item) => {
        // 使用当前股价计算市值
        const currentPrice = item.latest_price?.close || item.avg_price;
        return sum + (item.quantity * currentPrice);
      }, 0);
      const totalProfit = totalValue - totalCost;
      const profitRate = totalCost > 0 ? (totalProfit / totalCost) * 100 : 0;
      
      setPositionStats({
        totalValue,
        totalCost,
        totalProfit,
        profitRate
      });
    } catch (error) {
      console.error('获取持仓失败:', error);
      message.error('获取持仓失败');
    } finally {
      setPositionLoading(false);
    }
  };

  // 获取交易记录
  const fetchTrades = async () => {
    setTradeLoading(true);
    try {
      const response = await userTradeApi.getTrades(userId);
      setTrades(response.data.data || []);
    } catch (error) {
      console.error('获取交易记录失败:', error);
      message.error('获取交易记录失败');
    } finally {
      setTradeLoading(false);
    }
  };

  // 生成持仓分布饼图数据
  const getPortfolioPieData = () => {
    if (!positions || positions.length === 0) {
      return [];
    }

    return positions.map(position => {
      const currentPrice = position.latest_price?.close || position.avg_price;
      const marketValue = position.quantity * currentPrice;
      const stockName = position.stock_info?.name || position.ts_code;
      
      return {
        name: `${position.ts_code}\n${stockName}`,
        value: marketValue,
        itemStyle: {
          color: `hsl(${Math.random() * 360}, 70%, 60%)`
        }
      };
    }).filter(item => item.value > 0); // 只显示有市值的股票
  };

  // 持仓分布饼图配置
  const getPortfolioPieOption = () => {
    const pieData = getPortfolioPieData();
    
    return {
      title: {
        text: '持仓市值分布',
        left: 'center',
        textStyle: {
          fontSize: 16,
          fontWeight: 'bold'
        }
      },
      tooltip: {
        trigger: 'item',
        formatter: function(params) {
          const totalValue = positionStats.totalValue;
          const percentage = totalValue > 0 ? ((params.value / totalValue) * 100).toFixed(2) : 0;
          return `${params.name}<br/>市值: ${formatCurrency(params.value)}<br/>占比: ${percentage}%`;
        }
      },
      legend: {
        orient: 'vertical',
        left: 'left',
        top: 'middle',
        formatter: function(name) {
          const item = pieData.find(item => item.name === name);
          if (item) {
            const percentage = positionStats.totalValue > 0 ? 
              ((item.value / positionStats.totalValue) * 100).toFixed(1) : 0;
            return `${name} (${percentage}%)`;
          }
          return name;
        }
      },
      series: [
        {
          name: '持仓分布',
          type: 'pie',
          radius: ['40%', '70%'],
          center: ['60%', '50%'],
          data: pieData,
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowOffsetX: 0,
              shadowColor: 'rgba(0, 0, 0, 0.5)'
            }
          },
          label: {
            show: false
          },
          labelLine: {
            show: false
          }
        }
      ]
    };
  };

  // 持仓相关操作
  const handlePositionAdd = () => {
    setEditingPosition(null);
    positionForm.resetFields();
    setPositionModalVisible(true);
  };

  const handlePositionEdit = (record) => {
    setEditingPosition(record);
    positionForm.setFieldsValue({
      ...record,
      avg_price: record.avg_price
    });
    setPositionModalVisible(true);
  };

  const handlePositionDelete = async (id) => {
    try {
      await userPositionApi.deletePosition(userId, id);
      message.success('删除成功');
      fetchPositions();
    } catch (error) {
      message.error('删除失败');
    }
  };

  const handlePositionOk = async () => {
    try {
      const values = await positionForm.validateFields();
      const payload = {
        user_id: userId,
        ...values
      };
      
      if (editingPosition) {
        await userPositionApi.updatePosition(userId, editingPosition.id, payload);
        message.success('更新成功');
      } else {
        await userPositionApi.addPosition(userId, payload);
        message.success('添加成功');
      }
      setPositionModalVisible(false);
      fetchPositions();
    } catch (error) {
      message.error('操作失败');
    }
  };

  // 交易记录相关操作
  const handleTradeAdd = () => {
    setEditingTrade(null);
    tradeForm.resetFields();
    setTradeModalVisible(true);
  };

  const handleTradeEdit = (record) => {
    setEditingTrade(record);
    tradeForm.setFieldsValue({
      ...record,
      trade_date: record.trade_date ? moment(record.trade_date) : null,
      price: record.price
    });
    setTradeModalVisible(true);
  };

  // 新增：处理卖出操作
  const handleSellTrade = (record) => {
    setEditingTrade(null);
    tradeForm.resetFields();
    tradeForm.setFieldsValue({
      ts_code: record.ts_code,
      trade_type: 'sell',
      quantity: record.quantity,
      trade_date: moment(),
      price: null,
      profit_loss: null,
      note: ''
    });
    setTradeModalVisible(true);
  };

  const handleTradeDelete = async (id) => {
    try {
      await userTradeApi.deleteTrade(userId, id);
      message.success('删除成功');
      fetchTrades();
    } catch (error) {
      message.error('删除失败');
    }
  };

  const handleTradeOk = async () => {
    try {
      const values = await tradeForm.validateFields();
      const payload = {
        user_id: userId,
        ...values,
        trade_date: values.trade_date.format('YYYY-MM-DD')
      };
      
      if (editingTrade) {
        await userTradeApi.updateTrade(userId, editingTrade.id, payload);
        message.success('更新成功');
      } else {
        await userTradeApi.addTrade(userId, payload);
        message.success('添加成功');
      }
      setTradeModalVisible(false);
      fetchTrades();
    } catch (error) {
      message.error('操作失败');
    }
  };

  // 持仓表格列定义
  const positionColumns = [
    {
      title: '股票代码',
      dataIndex: 'ts_code',
      key: 'ts_code',
      width: 120,
      render: text => <span style={{ fontWeight: 'bold' }}>{text}</span>
    },
    {
      title: '股票名称',
      key: 'stock_name',
      width: 140,
      render: (_, record) => record.stock_info?.name || ''
    },
    {
      title: '持仓数量',
      dataIndex: 'quantity',
      key: 'quantity',
      width: 100,
      align: 'right',
      render: value => value?.toLocaleString()
    },
    {
      title: '平均成本',
      dataIndex: 'avg_price',
      key: 'avg_price',
      width: 120,
      align: 'right',
      render: value => formatCurrency(value)
    },
    {
      title: '当前价格',
      key: 'current_price',
      width: 120,
      align: 'right',
      render: (_, record) => {
        const currentPrice = record.latest_price?.close || record.avg_price;
        return formatCurrency(currentPrice);
      }
    },
    {
      title: '持仓市值',
      key: 'market_value',
      width: 120,
      align: 'right',
      render: (_, record) => {
        const currentPrice = record.latest_price?.close || record.avg_price;
        return formatCurrency(record.quantity * currentPrice);
      }
    },
    {
      title: '盈亏金额',
      key: 'profit_loss',
      width: 120,
      align: 'right',
      render: (_, record) => {
        const currentPrice = record.latest_price?.close || record.avg_price;
        const profitLoss = (currentPrice - record.avg_price) * record.quantity;
        const color = profitLoss >= 0 ? '#389e0d' : '#cf1322';
        return <span style={{ color, fontWeight: 'bold' }}>{formatCurrency(profitLoss)}</span>;
      }
    },
    {
      title: '盈亏率',
      key: 'profit_rate',
      width: 100,
      align: 'right',
      render: (_, record) => {
        const currentPrice = record.latest_price?.close || record.avg_price;
        const profitRate = record.avg_price > 0 ? ((currentPrice - record.avg_price) / record.avg_price) * 100 : 0;
        const color = profitRate >= 0 ? '#389e0d' : '#cf1322';
        return <span style={{ color, fontWeight: 'bold' }}>{profitRate.toFixed(2)}%</span>;
      }
    },
    {
      title: '标签',
      key: 'tags',
      width: 200,
      render: (_, record) => (
        <StockTags 
          tsCode={record.ts_code} 
          showManage={true}
          maxDisplay={2}
        />
      )
    },
    {
      title: '创建时间',
      dataIndex: 'created_at',
      key: 'created_at',
      width: 120,
      render: value => formatDate(value, 'YYYY-MM-DD')
    },
    {
      title: '操作',
      key: 'action',
      width: 120,
      render: (_, record) => (
        <div>
          <Button 
            type="text" 
            icon={<EditOutlined />} 
            onClick={() => handlePositionEdit(record)}
          />
          <Popconfirm title="确定删除？" onConfirm={() => handlePositionDelete(record.id)}>
            <Button type="text" danger icon={<DeleteOutlined />} />
          </Popconfirm>
        </div>
      )
    }
  ];

  // 交易记录表格列定义
  const tradeColumns = [
    {
      title: '交易日期',
      dataIndex: 'trade_date',
      key: 'trade_date',
      width: 120,
      render: value => formatDate(value, 'YYYY-MM-DD')
    },
    {
      title: '股票代码',
      dataIndex: 'ts_code',
      key: 'ts_code',
      width: 120,
      render: text => <span style={{ fontWeight: 'bold' }}>{text}</span>
    },
    {
      title: '股票名称',
      key: 'stock_name',
      width: 140,
      render: (_, record) => record.stock_info?.name || ''
    },
    {
      title: '交易类型',
      dataIndex: 'trade_type',
      key: 'trade_type',
      width: 80,
      render: value => (
        <span style={{ 
          color: value === 'buy' ? '#cf1322' : '#389e0d',
          fontWeight: 'bold'
        }}>
          {value === 'buy' ? '买入' : '卖出'}
        </span>
      )
    },
    {
      title: '交易数量',
      dataIndex: 'quantity',
      key: 'quantity',
      width: 100,
      align: 'right',
      render: value => value?.toLocaleString()
    },
    {
      title: '交易价格',
      dataIndex: 'price',
      key: 'price',
      width: 120,
      align: 'right',
      render: value => formatCurrency(value)
    },
    {
      title: '交易金额',
      key: 'trade_amount',
      width: 120,
      align: 'right',
      render: (_, record) => formatCurrency(record.quantity * record.price)
    },
    {
      title: '盈亏',
      dataIndex: 'profit_loss',
      key: 'profit_loss',
      width: 100,
      align: 'right',
      render: value => {
        if (!value) return '-';
        const isPositive = value > 0;
        return (
          <span style={{ color: isPositive ? '#cf1322' : '#389e0d' }}>
            {isPositive ? '+' : ''}{formatCurrency(value)}
          </span>
        );
      }
    },
    {
      title: '笔记',
      dataIndex: 'note',
      key: 'note',
      width: 200,
      ellipsis: true
    },
    {
      title: '操作',
      key: 'action',
      width: 150,
      render: (_, record) => (
        <div>
          <Button 
            type="text" 
            icon={<EditOutlined />} 
            onClick={() => handleTradeEdit(record)}
          />
          {record.trade_type === 'buy' && (
            <Button 
              type="text" 
              style={{ color: '#389e0d' }}
              onClick={() => handleSellTrade(record)}
            >
              卖出
            </Button>
          )}
          <Popconfirm title="确定删除？" onConfirm={() => handleTradeDelete(record.id)}>
            <Button type="text" danger icon={<DeleteOutlined />} />
          </Popconfirm>
        </div>
      )
    }
  ];

  return (
    <div style={{ padding: 24 }}>
      <Card>
        <Title level={4} style={{ marginBottom: 24 }}>我的投资组合</Title>
        
        {/* 持仓统计 */}
        <Row gutter={16} style={{ marginBottom: 24 }}>
          <Col span={6}>
            <Statistic title="持仓市值" value={positionStats.totalValue} precision={2} prefix="¥" />
          </Col>
          <Col span={6}>
            <Statistic title="总成本" value={positionStats.totalCost} precision={2} prefix="¥" />
          </Col>
          <Col span={6}>
            <Statistic 
              title="总盈亏" 
              value={positionStats.totalProfit} 
              precision={2} 
              prefix="¥"
              valueStyle={{ color: positionStats.totalProfit >= 0 ? '#cf1322' : '#389e0d' }}
            />
          </Col>
          <Col span={6}>
            <Statistic 
              title="盈亏率" 
              value={positionStats.profitRate} 
              precision={2} 
              suffix="%"
              valueStyle={{ color: positionStats.profitRate >= 0 ? '#cf1322' : '#389e0d' }}
            />
          </Col>
        </Row>

        <Tabs defaultActiveKey="positions">
          <TabPane tab="持仓管理" key="positions">
            <div style={{ marginBottom: 16 }}>
              <Button type="primary" icon={<PlusOutlined />} onClick={handlePositionAdd}>
                新增持仓
              </Button>
            </div>
            
            {/* 持仓分布饼图 */}
            {positions.length > 0 && (
              <Card 
                title={
                  <span>
                    <PieChartOutlined style={{ marginRight: 8 }} />
                    持仓分布
                  </span>
                }
                style={{ marginBottom: 16 }}
              >
                <ReactECharts 
                  option={getPortfolioPieOption()} 
                  style={{ height: '400px' }}
                  notMerge={true}
                />
              </Card>
            )}
            
            <Table
              columns={positionColumns}
              dataSource={positions}
              rowKey="id"
              loading={positionLoading}
              pagination={{ pageSize: 10 }}
              scroll={{ x: 'max-content' }}
              expandable={{
                expandedRowRender: record => record.ts_code ? <KLineChart tsCode={record.ts_code} /> : null,
                rowExpandable: record => !!record.ts_code,
              }}
            />
          </TabPane>
          
          <TabPane tab="交易记录" key="trades">
            <div style={{ marginBottom: 16 }}>
              <Button type="primary" icon={<PlusOutlined />} onClick={handleTradeAdd}>
                新增交易
              </Button>
            </div>
            <Table
              columns={tradeColumns}
              dataSource={trades}
              rowKey="id"
              loading={tradeLoading}
              pagination={{ pageSize: 10 }}
              scroll={{ x: 'max-content' }}
            />
          </TabPane>
        </Tabs>
      </Card>

      {/* 持仓编辑模态框 */}
      <Modal
        title={editingPosition ? '编辑持仓' : '新增持仓'}
        open={positionModalVisible}
        onOk={handlePositionOk}
        onCancel={() => setPositionModalVisible(false)}
        destroyOnClose
      >
        <Form form={positionForm} layout="vertical">
          <Form.Item name="ts_code" label="股票代码" rules={[{ required: true, message: '请选择股票' }]}>
            <Select
              showSearch
              placeholder="搜索股票代码或名称"
              filterOption={false}
              onSearch={handleStockSearch}
              loading={stockSearchLoading}
              options={stockOptions}
              allowClear
            />
          </Form.Item>
          <Form.Item name="quantity" label="持仓数量" rules={[{ required: true, message: '请输入持仓数量' }]}>
            <InputNumber min={1} style={{ width: '100%' }} placeholder="请输入数量" />
          </Form.Item>
          <Form.Item name="avg_price" label="平均成本" rules={[{ required: true, message: '请输入平均成本' }]}>
            <InputNumber min={0} precision={4} style={{ width: '100%' }} placeholder="请输入价格" />
          </Form.Item>
        </Form>
      </Modal>

      {/* 交易记录编辑模态框 */}
      <Modal
        title={editingTrade ? '编辑交易' : '新增交易'}
        open={tradeModalVisible}
        onOk={handleTradeOk}
        onCancel={() => setTradeModalVisible(false)}
        destroyOnClose
      >
        <Form form={tradeForm} layout="vertical">
          <Form.Item name="ts_code" label="股票代码" rules={[{ required: true, message: '请选择股票' }]}>
            <Select
              showSearch
              placeholder="搜索股票代码或名称"
              filterOption={false}
              onSearch={handleStockSearch}
              loading={stockSearchLoading}
              options={stockOptions}
              allowClear
            />
          </Form.Item>
          <Form.Item name="trade_type" label="交易类型" rules={[{ required: true, message: '请选择交易类型' }]}>
            <Select placeholder="请选择交易类型">
              <Option value="buy">买入</Option>
              <Option value="sell">卖出</Option>
            </Select>
          </Form.Item>
          <Form.Item name="quantity" label="交易数量" rules={[{ required: true, message: '请输入交易数量' }]}>
            <InputNumber min={1} style={{ width: '100%' }} placeholder="请输入数量" />
          </Form.Item>
          <Form.Item name="price" label="交易价格" rules={[{ required: true, message: '请输入交易价格' }]}>
            <InputNumber min={0} precision={4} style={{ width: '100%' }} placeholder="请输入价格" />
          </Form.Item>
          <Form.Item name="trade_date" label="交易日期" rules={[{ required: true, message: '请选择交易日期' }]}>
            <DatePicker style={{ width: '100%' }} />
          </Form.Item>
          <Form.Item name="profit_loss" label="盈亏">
            <InputNumber precision={4} style={{ width: '100%' }} placeholder="可选，卖出时填写" />
          </Form.Item>
          <Form.Item name="note" label="笔记">
            <Input.TextArea rows={3} placeholder="可选，记录交易笔记" />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default UserPortfolioPage; 