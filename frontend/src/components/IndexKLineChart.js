import React, { useState, useEffect } from 'react';
import ReactECharts from 'echarts-for-react';
import { Spin, Card, Row, Col, Statistic, message } from 'antd';
import { RiseOutlined, FallOutlined } from '@ant-design/icons';
import { indexApi } from '../api/indexApi';
import moment from 'moment';

const IndexKLineChart = ({ indexData, height = 300 }) => {
  const [loading, setLoading] = useState(false);
  const [chartData, setChartData] = useState({ data: [], volume: [] });
  const [realTimeData, setRealTimeData] = useState(indexData);

  // 获取指数代码映射
  const getIndexCode = (name) => {
    const codeMap = {
      '上证指数': '000001.SH',
      '深证成指': '399107.SZ', 
      '创业板指': '399006.SZ'
    };
    return codeMap[name] || '000001.SH';
  };

  // 从API获取K线数据
  const fetchKlineData = async () => {
    if (!indexData || !indexData.name) return;
    
    setLoading(true);
    try {
      const tsCode = getIndexCode(indexData.name);
      const endDate = moment().format('YYYY-MM-DD');
      const startDate = moment().subtract(30, 'days').format('YYYY-MM-DD');
      
      const response = await indexApi.getIndexDaily(tsCode, startDate, endDate);
      
      if (response.code === 200 && response.data) {
        const klineData = response.data.map(item => [
          item.trade_date,
          parseFloat(item.open || 0),
          parseFloat(item.close || 0),
          parseFloat(item.low || 0),
          parseFloat(item.high || 0)
        ]);
        
        const volumeData = response.data.map(item => parseFloat(item.vol || 0));
        
        setChartData({
          data: klineData,
          volume: volumeData
        });
        
        // 更新实时数据
        if (response.data.length > 0) {
          const latest = response.data[0];
          setRealTimeData({
            ...indexData,
            current: parseFloat(latest.close || 0),
            change: parseFloat(latest.change || 0),
            changePercent: parseFloat(latest.pct_chg || 0),
            volume: parseFloat(latest.vol || 0) / 10000, // 转换为亿
            turnover: parseFloat(latest.amount || 0) / 100000 // 转换为亿
          });
        }
      } else {
        message.error('获取K线数据失败');
      }
    } catch (error) {
      console.error('获取K线数据失败:', error);
      message.error('获取K线数据失败');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchKlineData();
  }, [indexData.name]);

  const { data, volume } = chartData;

  const option = {
    title: {
      text: `${realTimeData.name} K线图`,
      left: 'center',
      textStyle: {
        fontSize: 14,
        fontWeight: 'bold'
      }
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'cross' },
      formatter: function (params) {
        const date = params[0].axisValue;
        let tooltip = `<div style="font-weight: bold; margin-bottom: 8px;">${date}</div>`;
        
        params.forEach(param => {
          if (param.seriesName === 'K线') {
            const [open, close, low, high] = param.data;
            tooltip += `
              <div style="margin: 4px 0;">
                <span style="color: #666;">开盘：</span>${open.toFixed(2)}<br/>
                <span style="color: #666;">收盘：</span>${close.toFixed(2)}<br/>
                <span style="color: #666;">最高：</span>${high.toFixed(2)}<br/>
                <span style="color: #666;">最低：</span>${low.toFixed(2)}
              </div>
            `;
          } else if (param.seriesName === '成交量') {
            tooltip += `<div style="margin: 4px 0;"><span style="color: #666;">成交量：</span>${param.data}万手</div>`;
          }
        });
        
        return tooltip;
      }
    },
    grid: [
      { left: '8%', right: '8%', height: '60%' },
      { left: '8%', right: '8%', top: '72%', height: '16%' }
    ],
    xAxis: [
      {
        type: 'category',
        data: data.map(item => item[0]),
        scale: true,
        boundaryGap: false,
        axisLine: { onZero: false },
        splitLine: { show: false },
        min: 'dataMin',
        max: 'dataMax',
        axisPointer: { z: 100 },
        axisLabel: { 
          show: true,
          formatter: function(value) {
            return value.slice(5); // 只显示月-日
          }
        }
      },
      {
        type: 'category',
        gridIndex: 1,
        data: data.map(item => item[0]),
        scale: true,
        boundaryGap: false,
        axisLine: { onZero: false },
        splitLine: { show: false },
        min: 'dataMin',
        max: 'dataMax',
        axisTick: { show: false },
        axisLabel: { show: false }
      }
    ],
    yAxis: [
      {
        scale: true,
        splitArea: { show: true },
        axisLabel: {
          formatter: function (val) {
            return val.toFixed(0);
          }
        },
        axisLine: { show: true },
        axisTick: { show: true },
        splitLine: { show: true }
      },
      {
        scale: true,
        gridIndex: 1,
        splitNumber: 2,
        axisLabel: {
          formatter: function (val) {
            if (val >= 1000) return (val / 1000).toFixed(1) + 'K';
            return val;
          }
        },
        axisLine: { show: true },
        axisTick: { show: true },
        splitLine: { show: false }
      }
    ],
    dataZoom: [
      {
        type: 'inside',
        xAxisIndex: [0, 1],
        start: 50,
        end: 100
      }
    ],
    series: [
      {
        name: 'K线',
        type: 'candlestick',
        data: data.map(item => [item[1], item[2], item[3], item[4]]),
        itemStyle: {
          color: '#ef232a',
          color0: '#14b143',
          borderColor: '#ef232a',
          borderColor0: '#14b143'
        }
      },
      {
        name: '成交量',
        type: 'bar',
        xAxisIndex: 1,
        yAxisIndex: 1,
        data: volume,
        color: '#b0b0b0',
        barWidth: '60%',
        tooltip: { show: false }
      }
    ]
  };

  return (
    <Card 
      size="small" 
      style={{ height: '100%' }}
      bodyStyle={{ padding: '12px' }}
    >
      <Spin spinning={loading}>
        <div style={{ textAlign: 'center', marginBottom: '12px' }}>
          <Row gutter={16}>
            <Col span={8}>
              <Statistic
                title="最新点位"
                value={realTimeData.current}
                precision={2}
                valueStyle={{ 
                  color: realTimeData.changePercent > 0 ? '#f5222d' : '#52c41a',
                  fontSize: '16px',
                  fontWeight: 'bold'
                }}
                suffix={
                  <span style={{ fontSize: '12px' }}>
                    {realTimeData.change > 0 ? '+' : ''}{realTimeData.change.toFixed(2)}
                    ({realTimeData.changePercent > 0 ? '+' : ''}{realTimeData.changePercent.toFixed(2)}%)
                  </span>
                }
              />
            </Col>
            <Col span={8}>
              <Statistic
                title="成交量"
                value={realTimeData.volume}
                precision={2}
                suffix="亿"
                valueStyle={{ fontSize: '16px' }}
              />
            </Col>
            <Col span={8}>
              <Statistic
                title="成交额"
                value={realTimeData.turnover}
                precision={2}
                suffix="亿"
                valueStyle={{ fontSize: '16px' }}
              />
            </Col>
          </Row>
        </div>
        
        {data.length > 0 ? (
          <ReactECharts
            option={option}
            style={{ height: height - 80 }}
            notMerge={true}
          />
        ) : (
          <div style={{ 
            height: height - 80, 
            display: 'flex', 
            alignItems: 'center', 
            justifyContent: 'center',
            color: '#999'
          }}>
            暂无数据
          </div>
        )}
      </Spin>
    </Card>
  );
};

export default IndexKLineChart;
