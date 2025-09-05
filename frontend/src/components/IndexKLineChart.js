import React, { useState, useEffect } from 'react';
import ReactECharts from 'echarts-for-react';
import { Spin, Card, Row, Col, Statistic } from 'antd';
import { RiseOutlined, FallOutlined } from '@ant-design/icons';

const IndexKLineChart = ({ indexData, height = 300 }) => {
  const [loading, setLoading] = useState(false);

  // 生成模拟的K线数据（实际项目中应该从API获取）
  const generateMockData = (basePrice, days = 30) => {
    const data = [];
    const volume = [];
    let currentPrice = basePrice;
    
    for (let i = 0; i < days; i++) {
      const date = new Date();
      date.setDate(date.getDate() - (days - i - 1));
      const dateStr = date.toISOString().slice(0, 10);
      
      // 模拟价格波动
      const change = (Math.random() - 0.5) * 0.02; // ±1%的波动
      const open = currentPrice;
      const close = currentPrice * (1 + change);
      const high = Math.max(open, close) * (1 + Math.random() * 0.01);
      const low = Math.min(open, close) * (1 - Math.random() * 0.01);
      
      data.push([dateStr, open, close, low, high]);
      volume.push(Math.floor(Math.random() * 1000 + 500)); // 模拟成交量
      
      currentPrice = close;
    }
    
    return { data, volume };
  };

  const { data, volume } = generateMockData(indexData.current, 30);

  const option = {
    title: {
      text: `${indexData.name} K线图`,
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
      <div style={{ textAlign: 'center', marginBottom: '12px' }}>
        <Row gutter={16}>
          <Col span={8}>
            <Statistic
              title="最新点位"
              value={indexData.current}
              valueStyle={{ 
                color: indexData.changePercent > 0 ? '#f5222d' : '#52c41a',
                fontSize: '16px',
                fontWeight: 'bold'
              }}
              suffix={
                <span style={{ fontSize: '12px' }}>
                  {indexData.change > 0 ? '+' : ''}{indexData.change}
                  ({indexData.changePercent > 0 ? '+' : ''}{indexData.changePercent}%)
                </span>
              }
            />
          </Col>
          <Col span={8}>
            <Statistic
              title="成交量"
              value={indexData.volume}
              suffix="亿"
              valueStyle={{ fontSize: '16px' }}
            />
          </Col>
          <Col span={8}>
            <Statistic
              title="成交额"
              value={indexData.turnover}
              suffix="亿"
              valueStyle={{ fontSize: '16px' }}
            />
          </Col>
        </Row>
      </div>
      
      <ReactECharts
        option={option}
        style={{ height: height - 80 }}
        notMerge={true}
      />
    </Card>
  );
};

export default IndexKLineChart;
