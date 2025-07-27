/**
 * A股数据分析平台 - 数据格式化工具
 * 提供日期、数字、金额等常用格式化功能
 */
import {Tag} from "antd";

// 日期格式化
export const formatDate = (dateString, format = 'YYYY-MM-DD') => {
  if (!dateString) return '';

  const date = new Date(dateString);
  if (isNaN(date.getTime())) return dateString;

  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');

  return format
    .replace('YYYY', year)
    .replace('MM', month)
    .replace('DD', day);
};

// 数字格式化（添加千位分隔符）
export const formatNumber = (num, precision = 0) => {
  if (num === null || num === undefined) return '0';
  const fixedNum = Number(num).toFixed(precision);
  return fixedNum.replace(/\B(?=(\d{3})+(?!\d))/g, ',');
};

// 金额格式化（转换为亿元/万元/元）
export const formatCurrency = (amount, precision = 2) => {
  if (amount === null || amount === undefined) return '0';

  const absAmount = Math.abs(amount);

  if (absAmount >= 100000000) { // 大于1亿
    return `${formatNumber(amount / 100000000, precision)}亿`;
  } else if (absAmount >= 10000) { // 大于1万
    return `${formatNumber(amount / 10000, precision)}万`;
  } else {
    return `${formatNumber(amount, precision)}元`;
  }
};

// 百分比格式化
export const formatPercent = (value, precision = 2) => {
  if (value === null || value === undefined) return '0.00%';

  const numericValue = Number(value);
  if (isNaN(numericValue)) return '0.00%';

  return `${numericValue.toFixed(precision)}%`;
};

// 格式化涨跌幅数字（带符号和颜色）
export const formatChange = (value, precision = 2) => {
  if (value === null || value === undefined) return '0.00%';

  const numericValue = Number(value);
  if (isNaN(numericValue)) return '0.00%';

  const prefix = numericValue > 0 ? '+' : '';
  const text = `${prefix}${numericValue.toFixed(precision)}%`;

  if (numericValue > 0) {
    return <span style={{ color: '#cf1322' }}>{text}</span>;
  } else if (numericValue < 0) {
    return <span style={{ color: '#389e0d' }}>{text}</span>;
  } else {
    return text;
  }
};

// 格式化股票状态
export const formatStatus = (status) => {
  switch (status) {
    case '在市':
      return <Tag color="green">在市</Tag>;
    case '退市':
      return <Tag color="red">退市</Tag>;
    case '暂停上市':
      return <Tag color="orange">暂停上市</Tag>;
    default:
      return <Tag>{status || '未知'}</Tag>;
  }
};

// 格式化股票代码（添加交易所后缀）
export const formatStockCode = (code, exchange) => {
  if (!code) return '';

  const standardCode = code.trim().toUpperCase();

  // 如果已经是标准格式（带后缀）
  if (standardCode.endsWith('.SH') || standardCode.endsWith('.SZ')) {
    return standardCode;
  }

  // 根据交易所添加后缀
  switch (exchange) {
    case 'SSE':
      return `${standardCode}.SH`;
    case 'SZSE':
      return `${standardCode}.SZ`;
    case 'BSE':
      return `${standardCode}.BJ`;
    default:
      return standardCode;
  }
};

// 简写公司名称（解决长名称问题）
export const shortenCompanyName = (name, maxLength = 16) => {
  if (!name || name.length <= maxLength) return name;

  // 尝试去除"股份有限公司"部分
  const shortened = name.replace(/股份有限公司$/, '');
  if (shortened.length <= maxLength) return shortened;

  // 尝试去除地域前缀
  const geoShortened = shortened.replace(/^(北京市|上海市|天津市|重庆市|广东省|江苏省|浙江省|福建省|安徽省|江西省|山东省|山西省|河南省|河北省|湖南省|湖北省|广西壮族自治区|海南省|四川省|贵州省|云南省|陕西省|甘肃省|青海省|黑龙江省|吉林省|辽宁省|内蒙古自治区|宁夏回族自治区|新疆维吾尔自治区|西藏自治区|)/, '');
  if (geoShortened.length <= maxLength) return geoShortened;

  // 最后手段：截断
  return `${name.substring(0, maxLength)}...`;
};

// 获取行业颜色（为不同行业分配固定颜色）
export const getIndustryColor = (industryName) => {
  const industryColors = {
    '电子': '#108ee9',
    '医药生物': '#f50',
    '计算机': '#2db7f5',
    '化工': '#87d068',
    '机械设备': '#108ee9',
    '传媒': '#ffc069',
    '通信': '#a0d911',
    '食品饮料': '#722ed1',
    '家用电器': '#13c2c2',
    '建筑装饰': '#52c41a',
    '房地产': '#faad14',
    '汽车': '#1890ff',
    '银行': '#ffc53d',
    '非银金融': '#ffec3d',
    '有色金属': '#597ef7',
    '电气设备': '#b37feb',
    '国防军工': '#ff85c0',
    '轻工制造': '#5cdbd3',
    '交通运输': '#bae637',
    '公用事业': '#ff9c6e',
    '采掘': '#d48806',
    '钢铁': '#ffc069',
    '商业贸易': '#ffa940',
    '农林牧渔': '#7cb305',
    '综合': '#d3adf7',
  };

  return industryColors[industryName] || '#8c8c8c';
};