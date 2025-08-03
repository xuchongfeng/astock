import React, { useState, useEffect } from 'react';
import ReactECharts from 'echarts-for-react';
import { DatePicker, Spin } from 'antd';
import moment from 'moment';
import { stockDailyApi } from '../api/stockDailyApi';
import { formatDate } from '../utils/formatters';

const { RangePicker } = DatePicker;

const KLineChart = ({ tsCode, height = 500, miniMode = false, lazyLoad = false, shouldLoad = false }) => {
  // 默认区间为3个月
  const [dateRange, setDateRange] = useState([
    moment().subtract(5, 'months'),
    moment()
  ]);
  const [data, setData] = useState([]);
  const [volume, setVolume] = useState([]);
  const [loading, setLoading] = useState(false);
  const [hasLoaded, setHasLoaded] = useState(false);

  // 根据lazyLoad参数决定是否自动加载
  useEffect(() => {
    if (!lazyLoad && tsCode) {
      fetchChartData();
    }
  }, [tsCode, dateRange, lazyLoad]);

  // 懒加载逻辑：当组件被渲染时才开始加载
  useEffect(() => {
    if (lazyLoad && shouldLoad && tsCode && !hasLoaded) {
      // 添加一个小延迟，确保组件已经稳定渲染
      const timer = setTimeout(() => {
        fetchChartData();
      }, 100);
      
      return () => clearTimeout(timer);
    }
  }, [shouldLoad, hasLoaded, lazyLoad]); // 移除tsCode依赖，避免tsCode变化时重新触发

  const fetchChartData = async () => {
    if (!tsCode) return;
    
    // 如果是懒加载模式，只有在shouldLoad为true时才加载
    if (lazyLoad && !shouldLoad) {
      console.log('KLineChart: 跳过加载 for', tsCode, '因为shouldLoad为false');
      return;
    }

    console.log('KLineChart: 开始加载数据 for', tsCode, 'lazyLoad:', lazyLoad, 'shouldLoad:', shouldLoad);
    
    setLoading(true);
    try {
      const [start, end] = dateRange;
      
      const response = await stockDailyApi.getDailyData(
        tsCode,
        null, // trade_date
        formatDate(start, 'YYYY-MM-DD'),
        formatDate(end, 'YYYY-MM-DD')
      );

      // 结构：trade_date, open, close, low, high, vol
      console.log(response.data);
      const chartData = response.data.map(item => [
        item.trade_date,
        item.open,
        item.close,
        item.low,
        item.high
      ]);
      const volumeData = response.data.map(item => item.vol || item.volume || 0);

      console.log('KLineChart: 数据加载完成 for', tsCode, 'records:', chartData.length);
      setData(chartData);
      setVolume(volumeData);
      setHasLoaded(true);
    } catch (error) {
      console.error('获取K线数据失败:', error);
    } finally {
      setLoading(false);
    }
  };

  const option = {
    title: miniMode ? undefined : {
      text: `${tsCode} 日K线图`,
      left: 'center'
    },
    tooltip: miniMode ? undefined : {
      trigger: 'axis',
      axisPointer: { type: 'cross' }
    },
    axisPointer: miniMode ? undefined : {
      link: [{ xAxisIndex: 'all' }],
      label: {
        backgroundColor: '#777'
      }
    },
    grid: miniMode
      ? [{ left: 0, right: 0, top: 0, bottom: 0 }]
      : [
          { left: '8%', right: '8%', height: '60%' },
          { left: '8%', right: '8%', top: '72%', height: '16%' }
        ],
    xAxis: [
      {
        type: 'category',
        data: data.map(item => {
          let d = item[0];
          // 已为YYYY-MM-DD
          if (/^\d{4}-\d{2}-\d{2}$/.test(d)) return d;
          // 20240601
          if (/^\d{8}$/.test(d)) return d.slice(0,4) + '-' + d.slice(4,6) + '-' + d.slice(6,8);
          // Date对象
          if (d instanceof Date) return d.toISOString().slice(0, 10);
          // 形如 'Fri, 21 Feb 2025 00:00:00 GMT'
          if (typeof d === 'string' && d.match(/^[A-Za-z]{3},/)) {
            const dateObj = new Date(d);
            if (!isNaN(dateObj.getTime())) return dateObj.toISOString().slice(0, 10);
          }
          // 其它字符串尝试直接new Date
          const tryDate = new Date(d);
          if (!isNaN(tryDate.getTime())) return tryDate.toISOString().slice(0, 10);
          return d;
        }),
        scale: true,
        boundaryGap: false,
        axisLine: miniMode ? { show: false } : { onZero: false },
        splitLine: { show: false },
        min: 'dataMin',
        max: 'dataMax',
        axisPointer: miniMode ? undefined : { z: 100 },
        axisLabel: miniMode ? { show: false } : undefined,
        axisTick: miniMode ? { show: false } : undefined
      },
      {
        type: 'category',
        gridIndex: 1,
        data: data.map(item => {
          let d = item[0];
          if (/^\d{4}-\d{2}-\d{2}$/.test(d)) return d;
          if (/^\d{8}$/.test(d)) return d.slice(0,4) + '-' + d.slice(4,6) + '-' + d.slice(6,8);
          if (d instanceof Date) return d.toISOString().slice(0, 10);
          if (typeof d === 'string' && d.match(/^[A-Za-z]{3},/)) {
            const dateObj = new Date(d);
            if (!isNaN(dateObj.getTime())) return dateObj.toISOString().slice(0, 10);
          }
          const tryDate = new Date(d);
          if (!isNaN(tryDate.getTime())) return tryDate.toISOString().slice(0, 10);
          return d;
        }),
        scale: true,
        boundaryGap: false,
        axisLine: miniMode ? { show: false } : { onZero: false },
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
        splitArea: { show: !miniMode },
        axisLabel: miniMode ? { show: false } : undefined,
        axisLine: miniMode ? { show: false } : undefined,
        axisTick: miniMode ? { show: false } : undefined,
        splitLine: miniMode ? { show: false } : undefined
      },
      {
        scale: true,
        gridIndex: 1,
        splitNumber: 2,
        axisLabel: miniMode ? { show: false } : {
          formatter: function (val) {
            if (val >= 100000000) return (val / 100000000).toFixed(1) + '亿';
            if (val >= 10000) return (val / 10000).toFixed(1) + '万';
            return val;
          }
        },
        axisLine: miniMode ? { show: false } : undefined,
        axisTick: miniMode ? { show: false } : undefined,
        splitLine: miniMode ? { show: false } : undefined
      }
    ],
    dataZoom: miniMode ? undefined : [
      {
        type: 'inside',
        xAxisIndex: [0, 1],
        start: 50,
        end: 100
      },
      {
        show: true,
        type: 'slider',
        xAxisIndex: [0, 1],
        top: '90%',
        start: 50,
        end: 100
      }
    ],
    series: [
      {
        name: tsCode,
        type: 'candlestick',
        data: data.map(item => [item[1], item[2], item[3], item[4]]),
        itemStyle: {
          color: '#ef232a',
          color0: '#14b143',
          borderColor: '#ef232a',
          borderColor0: '#14b143'
        }
      },
      !miniMode && {
        name: '成交量',
        type: 'bar',
        xAxisIndex: 1,
        yAxisIndex: 1,
        data: volume,
        color: '#b0b0b0',
        barWidth: '60%',
        tooltip: { show: false }
      }
    ].filter(Boolean)
  };

  return (
    <Spin spinning={loading}>
      {!miniMode && (
        <div style={{ textAlign: 'right', marginBottom: 10 }}>
          <RangePicker
            value={dateRange}
            onChange={setDateRange}
            disabledDate={current => current && current > moment().endOf('day')}
          />
        </div>
      )}
      <ReactECharts
        option={option}
        style={{ height }}
        notMerge={true}
      />
    </Spin>
  );
};

export default KLineChart;