import React from 'react';
import ReactECharts from 'echarts-for-react';
import {formatCurrency, formatDate, formatPercent} from '../utils/formatters';

const StockDailyChart = ({ data, loading }) => {
  if (loading || !data || data.length === 0) {
    return (
      <div style={{
        height: 400,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        border: '1px dashed #e8e8e8',
        borderRadius: 4,
        marginBottom: 24
      }}>
        <div style={{ color: '#8c8c8c' }}>
          {loading ? '数据加载中...' : '暂无数据'}
        </div>
      </div>
    );
  }

  // 准备图表数据
  const dates = data.map(item => formatDate(item.trade_date, 'MM-DD'));
  const values = data.map(item => [
    item.open,
    item.close,
    item.low,
    item.high
  ]);
  const volumes = data.map(item => item.vol);

  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross'
      },
      formatter: (params) => {
        const item = data.find(d =>
          formatDate(d.trade_date, 'MM-DD') === params[0].name
        );
        return `
          <div style="margin-bottom: 5px; font-weight: bold">${formatDate(item.trade_date, 'YYYY-MM-DD')}</div>
          <div>开盘价: ${formatCurrency(item.open)}</div>
          <div>收盘价: ${formatCurrency(item.close)}</div>
          <div>最高价: ${formatCurrency(item.high)}</div>
          <div>最低价: ${formatCurrency(item.low)}</div>
          <div>涨跌幅: ${item.pct_chg > 0 ? '+' : ''}${formatPercent(item.pct_chg)}</div>
          <div>成交量: ${(item.vol / 100).toFixed(2)}万手</div>
          <div>成交额: ${formatCurrency(item.amount)}</div>
        `;
      }
    },
    grid: [
      {
        left: '10%',
        right: '10%',
        height: '60%',
        top: 20
      },
      {
        left: '10%',
        right: '10%',
        height: '15%',
        top: '75%'
      }
    ],
    xAxis: [
      {
        type: 'category',
        data: dates,
        scale: true,
        boundaryGap: false,
        axisLine: { onZero: false },
        axisLabel: {
          formatter: value => formatDate(value, 'MM-DD')
        },
        splitLine: { show: false },
        splitNumber: 20,
        min: 'dataMin',
        max: 'dataMax'
      },
      {
        type: 'category',
        gridIndex: 1,
        data: dates,
        axisLabel: { show: false },
        axisLine: { show: false },
        axisTick: { show: false },
        splitLine: { show: false }
      }
    ],
    yAxis: [
      {
        scale: true,
        splitArea: {
          show: true
        },
        axisLabel: {
          formatter: value => value.toFixed(2)
        }
      },
      {
        scale: true,
        gridIndex: 1,
        splitNumber: 2,
        axisLabel: { show: false },
        axisLine: { show: false },
        axisTick: { show: false },
        splitLine: { show: false }
      }
    ],
    dataZoom: [
      {
        type: 'inside',
        xAxisIndex: [0, 1],
        start: 50,
        end: 100
      },
      {
        show: true,
        xAxisIndex: [0, 1],
        type: 'slider',
        bottom: 20,
        start: 50,
        end: 100,
        height: 20,
        backgroundColor: '#f5f7fa',
        fillerColor: 'rgba(24, 144, 255, 0.2)',
        borderColor: '#d9d9d9',
        textStyle: {
          color: '#8c8c8c'
        }
      }
    ],
    series: [
      {
        name: 'K线',
        type: 'candlestick',
        data: values,
        itemStyle: {
          color: '#ef232a',
          color0: '#14b143',
          borderColor: '#ef232a',
          borderColor0: '#14b143'
        },
        markPoint: {
          label: {
            formatter: param => param.value > 0 ? param.value : ''
          },
          data: [
            {
              name: '最高值',
              type: 'max',
              valueDim: 'highest'
            },
            {
              name: '最低值',
              type: 'min',
              valueDim: 'lowest'
            }
          ]
        }
      },
      {
        name: '成交量',
        type: 'bar',
        xAxisIndex: 1,
        yAxisIndex: 1,
        data: volumes,
        itemStyle: {
          color: function(params) {
            const item = data[params.dataIndex];
            return item.close >= item.open ? '#14b143' : '#ef232a';
          }
        }
      }
    ]
  };

  return (
    <ReactECharts
      option={option}
      style={{ height: 500 }}
      theme="light"
      notMerge={true}
      lazyUpdate={true}
    />
  );
};

export default StockDailyChart;