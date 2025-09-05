/**
 * 图标验证文件
 * 列出项目中使用的所有 Ant Design 图标
 */

// 已确认可用的图标列表
export const USED_ICONS = {
  // 基础导航图标
  HomeOutlined: '首页图标',
  BarChartOutlined: '图表分析图标',
  DatabaseOutlined: '数据库图标',
  RiseOutlined: '上升趋势图标',
  StockOutlined: '股票图标',
  UserOutlined: '用户图标',
  SettingOutlined: '设置图标',
  WalletOutlined: '钱包图标',
  FolderOutlined: '文件夹图标',
  TagOutlined: '标签图标',
  
  // 热榜相关图标
  ReloadOutlined: '刷新图标',
  FireOutlined: '火焰图标',
  TrophyOutlined: '奖杯图标',
  ClockCircleOutlined: '时钟图标',
  
  // 操作图标
  SearchOutlined: '搜索图标',
  PlusOutlined: '添加图标',
  EditOutlined: '编辑图标',
  DeleteOutlined: '删除图标',
  EyeOutlined: '查看图标',
  ArrowLeftOutlined: '返回图标',
  
  // 状态图标
  ArrowUpOutlined: '上升箭头',
  ArrowDownOutlined: '下降箭头',
  MinusOutlined: '减号图标',
  TrendingUpOutlined: '上升趋势',
  TrendingDownOutlined: '下降趋势'
};

// 图标分类
export const ICON_CATEGORIES = {
  navigation: ['HomeOutlined', 'BarChartOutlined', 'DatabaseOutlined', 'RiseOutlined', 'StockOutlined'],
  user: ['UserOutlined', 'SettingOutlined', 'WalletOutlined', 'FolderOutlined', 'TagOutlined'],
  actions: ['SearchOutlined', 'PlusOutlined', 'EditOutlined', 'DeleteOutlined', 'EyeOutlined'],
  status: ['ArrowUpOutlined', 'ArrowDownOutlined', 'TrendingUpOutlined', 'TrendingDownOutlined'],
  special: ['FireOutlined', 'TrophyOutlined', 'ClockCircleOutlined', 'ReloadOutlined']
};

// 验证图标是否可用
export const validateIcon = (iconName) => {
  return USED_ICONS.hasOwnProperty(iconName);
};

// 获取图标描述
export const getIconDescription = (iconName) => {
  return USED_ICONS[iconName] || '未知图标';
};

// 推荐替代图标
export const ICON_ALTERNATIVES = {
  // 如果某个图标不存在，可以使用的替代图标
  'StrategyStockOutlined': 'SettingOutlined', // 策略相关使用设置图标
  'CustomIcon': 'QuestionOutlined' // 自定义图标使用问号图标
}; 