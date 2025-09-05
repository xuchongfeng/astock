import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { Layout, Menu, Spin, Dropdown } from 'antd';
import {
  HomeOutlined,
  BarChartOutlined,
  RiseOutlined,
  StockOutlined,
  UserOutlined,
  SettingOutlined,
  WalletOutlined,
  FolderOutlined,
  TagOutlined,
  DownOutlined,
  FireOutlined,
  TrophyOutlined,
  DatabaseOutlined
} from '@ant-design/icons';

// 导入页面组件
import HomePage from './pages/HomePage';
import IndustryPage from './pages/IndustryPage';
import CompanyDetail from './pages/CompanyDetail';
import IndustryStats from "./components/IndustryStats";
import StockDailyPage from "./pages/StockDailyPage";
import StockDailyDetailPage from "./pages/StockDailyDetailPage";
import UserWatchlistPage from './pages/UserWatchlistPage';
import StockNotePage from './pages/StockNotePage';
import ThsIndexPage from './pages/ThsIndexPage';
import ThsHotPage from './pages/ThsHotPage';
import StrategyPage from './pages/StrategyPage';
import StrategyStockPage from './pages/StrategyStockPage';
import UserPortfolioPage from './pages/UserPortfolioPage';
import SnowballPage from './pages/SnowballPage';
import TagManagementPage from './pages/TagManagementPage';
import StockTagPage from './pages/StockTagPage';
import FeaturesPage from './pages/FeaturesPage';
import NewsHotPage from './pages/NewsHotPage';
import StockAnalysisPage from './pages/StockAnalysisPage';

const { Header, Content, Footer } = Layout;

const App = () => {
  localStorage.setItem('userId', 1);
  const [loading] = useState(false);

  // 板块下拉菜单项
  const sectorMenuItems = [
    {
      key: 'industry',
      icon: <BarChartOutlined />,
      label: <Link to="/industry">行业分析</Link>,
    },
    {
      key: 'ths-index',
      icon: <BarChartOutlined />,
      label: <Link to="/ths-index">同花顺概念板块</Link>,
    },
  ];

  // 榜单下拉菜单项
  const rankingMenuItems = [
    {
      key: 'ths-hot',
      icon: <FireOutlined />,
      label: <Link to="/ths-hot">个股热榜</Link>,
    },
    {
      key: 'news-hot',
      icon: <TrophyOutlined />,
      label: <Link to="/news-hot">新闻热榜</Link>,
    },
  ];

  // 策略下拉菜单项
  const strategyMenuItems = [
    {
      key: 'strategy',
      icon: <SettingOutlined />,
      label: <Link to="/strategy">交易策略</Link>,
    },
    {
      key: 'strategy-stock',
      icon: <StockOutlined />,
      label: <Link to="/strategy-stock">策略选股</Link>,
    },
  ];

  // 个股数据下拉菜单项
  const stockDataMenuItems = [
    {
      key: 'tag-management',
      icon: <TagOutlined />,
      label: <Link to="/tag-management">标签管理</Link>,
    },
    {
      key: 'stock-tag',
      icon: <TagOutlined />,
      label: <Link to="/stock-tag">股票标签</Link>,
    },
    {
      key: 'stock-analysis',
      icon: <DatabaseOutlined />,
      label: <Link to="/stock-analysis">个股分析</Link>,
    },
  ];

  // 用户中心下拉菜单项
  const userMenuItems = [
    {
      key: 'watchlist',
      icon: <StockOutlined />,
      label: <Link to="/watchlist">自选股票</Link>,
    },
    {
      key: 'stock-note',
      icon: <StockOutlined />,
      label: <Link to="/stock-note">股票笔记</Link>,
    },
    {
      key: 'user-portfolio',
      icon: <WalletOutlined />,
      label: <Link to="/user-portfolio">我的投资组合</Link>,
    },
    {
      key: 'snowball',
      icon: <FolderOutlined />,
      label: <Link to="/snowball">我的雪球</Link>,
    },
  ];

  return (
    <Router>
      <Layout style={{ minHeight: '100vh' }}>
        {/* 顶部菜单栏 */}
        <Header style={{
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', // 渐变背景
          padding: 0,
          height: 80, // 增加高度
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          zIndex: 1000,
          boxShadow: '0 4px 20px rgba(102, 126, 234, 0.3)' // 带颜色的阴影
        }}>
          <div style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            height: '100%',
            padding: '0 24px',
            maxWidth: '1600px', // 同步调整菜单栏宽度
            margin: '0 auto'
          }}>
            {/* Logo区域 */}
            <div className="logo" style={{
              display: 'flex',
              alignItems: 'center',
              minWidth: '200px' // 固定最小宽度
            }}>
              <Link to="/features" style={{ textDecoration: 'none' }}>
                <div className="logo-content" style={{ display: 'flex', alignItems: 'center' }}>
                  <RiseOutlined style={{ fontSize: 32, color: '#ffffff' }} />
                  <div style={{ marginLeft: 12, color: '#fff' }}>
                    <div style={{ fontWeight: 'bold', lineHeight: '1.1', fontSize: '18px' }}>赌性坚强</div>
                  </div>
                </div>
              </Link>
            </div>

            {/* 导航菜单 */}
            <Menu
              theme="light"
              mode="horizontal"
              defaultSelectedKeys={['1']}
              style={{
                background: 'transparent',
                border: 'none',
                flex: 1,
                justifyContent: 'center',
                minWidth: '900px', // 增加最小宽度，因为增加了个股数据菜单
                color: '#fff'
              }}
              className="custom-menu"
            >
              {/* 市场概览菜单项 */}
              <Menu.Item key="1" style={{ padding: '0 20px' }}>
                <div style={{
                  display: 'flex',
                  alignItems: 'center',
                  cursor: 'pointer',
                  color: '#fff',
                  padding: '8px 12px',
                  borderRadius: '6px',
                  transition: 'background-color 0.3s',
                }}>
                  <HomeOutlined style={{ marginRight: '8px' }} />
                  <Link to="/" style={{ color: '#fff', textDecoration: 'none' }}>市场概览</Link>
                </div>
              </Menu.Item>
              
              {/* 交易数据菜单项 */}
              <Menu.Item key="stock-daily-detail" style={{ padding: '0 20px' }}>
                <div style={{
                  display: 'flex',
                  alignItems: 'center',
                  cursor: 'pointer',
                  color: '#fff',
                  padding: '8px 12px',
                  borderRadius: '6px',
                  transition: 'background-color 0.3s',
                }}>
                  <StockOutlined style={{ marginRight: '8px' }} />
                  <Link to="/stock-daily-detail" style={{ color: '#fff', textDecoration: 'none' }}>交易数据</Link>
                </div>
              </Menu.Item>
              
              {/* 板块下拉菜单 */}
              <Menu.Item key="sector" style={{ padding: '0 20px' }}>
                <Dropdown
                  menu={{ items: sectorMenuItems }}
                  placement="bottomCenter"
                  trigger={['click']}
                >
                  <div style={{
                    display: 'flex',
                    alignItems: 'center',
                    cursor: 'pointer',
                    color: '#fff',
                    padding: '8px 12px',
                    borderRadius: '6px',
                    transition: 'background-color 0.3s',
                  }}>
                    <BarChartOutlined style={{ marginRight: '8px' }} />
                    <span style={{ marginRight: '4px' }}>板块</span>
                    <DownOutlined style={{ fontSize: '12px' }} />
                  </div>
                </Dropdown>
              </Menu.Item>

              {/* 榜单下拉菜单 */}
              <Menu.Item key="ranking" style={{ padding: '0 20px' }}>
                <Dropdown
                  menu={{ items: rankingMenuItems }}
                  placement="bottomCenter"
                  trigger={['click']}
                >
                  <div style={{
                    display: 'flex',
                    alignItems: 'center',
                    cursor: 'pointer',
                    color: '#fff',
                    padding: '8px 12px',
                    borderRadius: '6px',
                    transition: 'background-color 0.3s',
                  }}>
                    <TrophyOutlined style={{ marginRight: '8px' }} />
                    <span style={{ marginRight: '4px' }}>榜单</span>
                    <DownOutlined style={{ fontSize: '12px' }} />
                  </div>
                </Dropdown>
              </Menu.Item>

              {/* 策略下拉菜单 */}
              <Menu.Item key="strategy-menu" style={{ padding: '0 20px' }}>
                <Dropdown
                  menu={{ items: strategyMenuItems }}
                  placement="bottomCenter"
                  trigger={['click']}
                >
                  <div style={{
                    display: 'flex',
                    alignItems: 'center',
                    cursor: 'pointer',
                    color: '#fff',
                    padding: '8px 12px',
                    borderRadius: '6px',
                    transition: 'background-color 0.3s',
                  }}>
                    <SettingOutlined style={{ marginRight: '8px' }} />
                    <span style={{ marginRight: '4px' }}>策略</span>
                    <DownOutlined style={{ fontSize: '12px' }} />
                  </div>
                </Dropdown>
              </Menu.Item>

              {/* 个股数据下拉菜单 */}
              <Menu.Item key="stock-data" style={{ padding: '0 20px' }}>
                <Dropdown
                  menu={{ items: stockDataMenuItems }}
                  placement="bottomCenter"
                  trigger={['click']}
                >
                  <div style={{
                    display: 'flex',
                    alignItems: 'center',
                    cursor: 'pointer',
                    color: '#fff',
                    padding: '8px 12px',
                    borderRadius: '6px',
                    transition: 'background-color 0.3s',
                  }}>
                    <DatabaseOutlined style={{ marginRight: '8px' }} />
                    <span style={{ marginRight: '4px' }}>个股数据</span>
                    <DownOutlined style={{ fontSize: '12px' }} />
                  </div>
                </Dropdown>
              </Menu.Item>
            </Menu>

            {/* 右侧用户区域 */}
            <div className="user-menu" style={{
              display: 'flex',
              alignItems: 'center',
              minWidth: '120px' // 给用户区域固定最小宽度
            }}>
              <Dropdown
                menu={{ items: userMenuItems }}
                placement="bottomRight"
                trigger={['click']}
              >
                <div style={{
                  display: 'flex',
                  alignItems: 'center',
                  cursor: 'pointer',
                  color: '#fff',
                  padding: '8px 12px',
                  borderRadius: '6px',
                  transition: 'background-color 0.3s',
                  ':hover': {
                    backgroundColor: 'rgba(255, 255, 255, 0.1)'
                  }
                }}>
                  <UserOutlined style={{ color: '#fff', fontSize: '18px', marginRight: '8px' }} />
                  <span style={{ color: '#fff', fontSize: '14px', marginRight: '4px' }}>用户中心</span>
                  <DownOutlined style={{ color: '#fff', fontSize: '12px' }} />
                </div>
              </Dropdown>
            </div>
          </div>
        </Header>

        {/* 主要内容区域 */}
        <Content style={{
          marginTop: 80, // 调整为新的Header高度
          padding: '24px',
          minHeight: 'calc(100vh - 80px)',
          background: '#f5f7fa'
        }}>
          <div style={{
            maxWidth: '1600px', // 增加内容区域最大宽度
            margin: '0 auto',
            background: '#fff',
            borderRadius: '8px',
            boxShadow: '0 2px 8px rgba(0,0,0,0.09)',
            overflow: 'hidden'
          }}>
            <Spin spinning={loading} size="large">
              <div style={{ padding: '24px' }}>
                <Routes>
                  <Route path="/" element={<HomePage />} />
                  <Route path="/features" element={<FeaturesPage />} />
                  <Route path="/industry" element={<IndustryPage />} />
                  <Route path="/company/:id" element={<CompanyDetail />} />
                  <Route path="/industry_stats" element={<IndustryStats />} />
                  <Route path="/stock-daily" element={<StockDailyPage />} />
                  <Route path="/stock-daily-detail" element={<StockDailyDetailPage />} />
                  <Route path="/watchlist" element={<UserWatchlistPage />} />
                  <Route path="/stock-note" element={<StockNotePage />} />
                  <Route path="/ths-index" element={<ThsIndexPage />} />
                  <Route path="/ths-hot" element={<ThsHotPage />} />
                  <Route path="/news-hot" element={<NewsHotPage />} />
                  <Route path="/strategy" element={<StrategyPage />} />
                  <Route path="/strategy-stock" element={<StrategyStockPage />} />
                  <Route path="/user-portfolio" element={<UserPortfolioPage />} />
                  <Route path="/snowball" element={<SnowballPage />} />
                  <Route path="/tag-management" element={<TagManagementPage />} />
                  <Route path="/stock-tag" element={<StockTagPage />} />
                  <Route path="/stock-analysis" element={<StockAnalysisPage />} />
                </Routes>
              </div>
            </Spin>
          </div>
        </Content>

        {/* 底部 */}
        <Footer style={{
          textAlign: 'center',
          padding: '16px 24px',
          background: '#f0f2f5',
          borderTop: '1px solid #e8e8e8'
        }}>
          永不言弃投资平台 ©{new Date().getFullYear()} 提供专业量化分析工具
        </Footer>
      </Layout>

      <style jsx global>{`
        .ant-layout {
          background-color: #f5f7fa;
        }

        /* 顶部菜单样式 */
        .ant-menu-horizontal {
          line-height: 80px; /* 调整为新的Header高度 */
        }

        .ant-menu-horizontal > .ant-menu-item {
          border-bottom: none;
          padding: 0 20px; /* 增加左右间距 */
          margin: 0 4px; /* 增加菜单项之间的间距 */
          font-size: 14px; /* 调整字体大小 */
        }

        .ant-menu-horizontal > .ant-menu-item:hover {
          background-color: rgba(255, 255, 255, 0.1);
          border-bottom: 2px solid #2a9d8f;
        }

        .ant-menu-horizontal > .ant-menu-item-selected {
          background-color: rgba(255, 255, 255, 0.1);
          border-bottom: 2px solid #2a9d8f;
        }

        .ant-menu-horizontal > .ant-menu-item > a {
          color: #fff;
          text-decoration: none;
          white-space: nowrap; /* 防止文字换行 */
        }

        .ant-menu-horizontal > .ant-menu-item:hover > a {
          color: #2a9d8f;
        }

        .ant-menu-horizontal > .ant-menu-item-selected > a {
          color: #2a9d8f;
        }

        /* Logo样式 */
        .logo-content:hover {
          opacity: 0.8;
          transition: opacity 0.3s;
        }

        /* 卡片样式 */
        .ant-card {
          border-radius: 8px;
          overflow: hidden;
          border: 1px solid #e8e8e8;
          margin-bottom: 16px;
          transition: box-shadow 0.3s;
          box-shadow: 0 2px 8px rgba(0,0,0,0.09);
        }

        .ant-card:hover {
          box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }

        .ant-card-head {
          background: #fafafa !important;
        }

        /* 表格样式 */
        .ant-table-row:hover {
          background: rgba(42, 157, 143, 0.05) !important;
        }

        .ant-table-thead > tr > th {
          background: #fafafa !important;
          font-weight: bold !important;
          color: rgba(0,0,0,0.85) !important;
        }

        /* 自定义菜单样式 */
        .custom-menu.ant-menu-horizontal {
          background: transparent !important;
          border: none !important;
        }

        .custom-menu.ant-menu-horizontal > .ant-menu-item {
          color: #fff !important;
          border-bottom: none !important;
          margin: 0 8px !important;
          border-radius: 6px !important;
          transition: all 0.3s ease !important;
        }

        .custom-menu.ant-menu-horizontal > .ant-menu-item:hover {
          background: rgba(255, 255, 255, 0.15) !important;
          color: #fff !important;
          transform: translateY(-2px) !important;
          box-shadow: 0 4px 12px rgba(255, 255, 255, 0.2) !important;
        }

        .custom-menu.ant-menu-horizontal > .ant-menu-item-selected {
          background: rgba(255, 255, 255, 0.2) !important;
          color: #fff !important;
          border-bottom: 3px solid #fff !important;
          font-weight: 600 !important;
        }

        .custom-menu.ant-menu-horizontal > .ant-menu-item > a {
          color: #fff !important;
          text-decoration: none !important;
          white-space: nowrap !important;
          font-weight: 500 !important;
          transition: all 0.3s ease !important;
        }

        .custom-menu.ant-menu-horizontal > .ant-menu-item:hover > a {
          color: #fff !important;
        }

        .custom-menu.ant-menu-horizontal > .ant-menu-item-selected > a {
          color: #fff !important;
          font-weight: 600 !important;
        }

        /* 菜单图标样式 */
        .custom-menu .ant-menu-item-icon {
          color: #fff !important;
          margin-right: 8px !important;
          font-size: 16px !important;
        }

        .custom-menu .ant-menu-item:hover .ant-menu-item-icon {
          color: #fff !important;
          transform: scale(1.1) !important;
          transition: transform 0.3s ease !important;
        }

        /* 用户区域样式优化 */
        .user-menu {
          background: rgba(255, 255, 255, 0.1) !important;
          padding: 8px 16px !important;
          border-radius: 20px !important;
          border: 1px solid rgba(255, 255, 255, 0.2) !important;
          transition: all 0.3s ease !important;
        }

        .user-menu:hover {
          background: rgba(255, 255, 255, 0.2) !important;
          border-color: rgba(255, 255, 255, 0.3) !important;
          transform: translateY(-1px) !important;
          box-shadow: 0 4px 12px rgba(255, 255, 255, 0.15) !important;
        }

        /* 用户中心下拉菜单样式 */
        .ant-dropdown-menu {
          border-radius: 8px !important;
          box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15) !important;
          border: 1px solid #e8e8e8 !important;
          padding: 8px 0 !important;
        }

        .ant-dropdown-menu-item {
          padding: 12px 20px !important;
          transition: all 0.3s ease !important;
          border-radius: 4px !important;
          margin: 2px 8px !important;
        }

        .ant-dropdown-menu-item:hover {
          background-color: #f5f7fa !important;
          transform: translateX(4px) !important;
        }

        .ant-dropdown-menu-item-icon {
          margin-right: 12px !important;
          color: #667eea !important;
          font-size: 16px !important;
        }

        .ant-dropdown-menu-item a {
          color: #333 !important;
          text-decoration: none !important;
          font-weight: 500 !important;
          display: flex !important;
          align-items: center !important;
        }

        .ant-dropdown-menu-item:hover a {
          color: #667eea !important;
        }

        /* 主导航下拉菜单样式 */
        .custom-menu .ant-menu-item .ant-dropdown {
          background: transparent !important;
        }

        .custom-menu .ant-menu-item .ant-dropdown-trigger {
          color: #fff !important;
          transition: all 0.3s ease !important;
        }

        .custom-menu .ant-menu-item .ant-dropdown-trigger:hover {
          background: rgba(255, 255, 255, 0.15) !important;
          transform: translateY(-2px) !important;
          box-shadow: 0 4px 12px rgba(255, 255, 255, 0.2) !important;
        }

        /* 下拉菜单项样式统一 */
        .ant-dropdown-menu-item {
          font-size: 14px !important;
          line-height: 1.5 !important;
        }

        .ant-dropdown-menu-item-icon {
          font-size: 16px !important;
        }

        /* Logo悬停效果 */
        .logo-content {
          transition: all 0.3s ease !important;
        }

        .logo-content:hover {
          transform: scale(1.05) !important;
          filter: brightness(1.1) !important;
        }

        /* 响应式设计 */
        @media (max-width: 1200px) {
          .ant-menu-horizontal > .ant-menu-item {
            padding: 0 16px;
            margin: 0 2px;
            font-size: 13px;
          }
        }

        @media (max-width: 768px) {
          .ant-menu-horizontal > .ant-menu-item {
            padding: 0 12px;
            margin: 0 1px;
            font-size: 12px;
          }

          .logo-content > div {
            font-size: 14px;
          }

          .logo-content > div > div:last-child {
            font-size: 10px;
          }
        }

        @media (max-width: 576px) {
          .ant-menu-horizontal {
            display: none;
          }

          .logo-content > div {
            display: none;
          }
        }
      `}</style>
    </Router>
  );
};

export default App; 