import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { Layout, Menu, Card, Spin } from 'antd';
import {
  HomeOutlined,
  BarChartOutlined,
  DatabaseOutlined,
  RiseOutlined,
  StockOutlined,
  UserOutlined,
  StrategyStockOutlined,
  WalletOutlined
} from '@ant-design/icons';

// 导入页面组件
import HomePage from './pages/HomePage';
import IndustryPage from './pages/IndustryPage';
import CompanyDetail from './pages/CompanyDetail';
import StockWatchlist from './pages/StockWatchlist';
import IndustryStats from "./components/IndustryStats";
import StockDailyPage from "./pages/StockDailyPage";
import StockDailyDetailPage from "./pages/StockDailyDetailPage";
import UserWatchlistPage from './pages/UserWatchlistPage';
import StockNotePage from './pages/StockNotePage';
import ThsIndexPage from './pages/ThsIndexPage';
import StrategyPage from './pages/StrategyPage';
import StrategyStockPage from './pages/StrategyStockPage';
import UserPortfolioPage from './pages/UserPortfolioPage';


const { Header, Content, Footer, Sider } = Layout;

const App = () => {
  localStorage.setItem('userId', 1);
  const [collapsed, setCollapsed] = useState(false);
  const [loading, setLoading] = useState(false);
  const [marketStatus] = useState({
    date: '2023-11-15',
    status: '交易中',
    shanghai: '+0.55%',
    shenzhen: '+0.78%',
    chinext: '+1.35%',
    star: '+2.12%'
  });

  return (
    <Router>
      <Layout style={{ minHeight: '100vh' }}>
        <Sider
          collapsible
          collapsed={collapsed}
          onCollapse={setCollapsed}
          theme="dark"
        >
          <div className="logo" style={{ height: 64, padding: 16 }}>
            <Link to="/">
              <div className="logo-content" style={{ display: 'flex', alignItems: 'center' }}>
                <RiseOutlined style={{ fontSize: 32, color: '#2a9d8f' }} />
                {!collapsed && (
                  <div style={{ marginLeft: 8, color: '#fff' }}>
                    <div style={{ fontWeight: 'bold', lineHeight: '1.1' }}>永不言弃</div>
                    <div style={{ fontSize: 12, opacity: 0.7 }}>投资平台</div>
                  </div>
                )}
              </div>
            </Link>
          </div>

          <Menu theme="dark" mode="inline" defaultSelectedKeys={['1']}>
            <Menu.Item key="1" icon={<HomeOutlined />}>
              <Link to="/">首页概览</Link>
            </Menu.Item>
              <Menu.Item key="stock-daily-detail">
                  <Link to="/stock-daily-detail">
                      <StockOutlined />
                      <span>股票每日数据</span>
                  </Link>
              </Menu.Item>
            <Menu.Item key="2" icon={<StockOutlined />}>
              <Link to="/watchlist">自选股票</Link>
            </Menu.Item>
            <Menu.Item key="3" icon={<BarChartOutlined />}>
              <Link to="/industry">行业分析</Link>
            </Menu.Item>
            <Menu.Item key="6" icon={<StockOutlined />}>
              <Link to="/stock-note">股票笔记</Link>
            </Menu.Item>
            <Menu.Item key="7" icon={<StockOutlined />}>
              <Link to="/strategy">交易策略</Link>
            </Menu.Item>
            <Menu.Item key="8" icon={<StockOutlined />}>
              <Link to="/strategy-stock">策略选股</Link>
            </Menu.Item>
            <Menu.Item key="9" icon={<UserOutlined />}>
              <Link to="/user-portfolio">我的投资组合</Link>
            </Menu.Item>

          </Menu>
        </Sider>

        <Layout>
          <Header style={{ background: '#fff', padding: 0, height: 64 }}>
            <div style={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              height: '100%',
              padding: '0 24px'
            }}>
              <div className="header-actions">
                <div className="search-bar" style={{ marginRight: 16 }}>
                  {/* 搜索框占位 */}
                </div>
                <div className="user-menu">
                  {/* 用户菜单占位 */}
                </div>
              </div>
            </div>
          </Header>

          <Content style={{ margin: '16px' }}>
            <Spin spinning={loading} size="large">
              <Card bordered={false} style={{ minHeight: 'calc(100vh - 150px)' }}>
                <Routes>
                  <Route path="/" element={<HomePage />} />
                  <Route path="/industry" element={<IndustryPage />} />
                  <Route path="/company/:id" element={<CompanyDetail />} />
                  <Route path="/industry_stats" element={<IndustryStats />} />
                  <Route path="/stock-daily" element={<StockDailyPage />} />
                  <Route path="/stock-daily-detail" element={<StockDailyDetailPage />} />
                  <Route path="/watchlist" element={<UserWatchlistPage />} />
                  <Route path="/stock-note" element={<StockNotePage />} />
                  <Route path="/ths-index" element={<ThsIndexPage />} />
                  <Route path="/strategy" element={<StrategyPage />} />
                  <Route path="/strategy-stock" element={<StrategyStockPage />} />
                  <Route path="/user-portfolio" element={<UserPortfolioPage />} />
                </Routes>
              </Card>
            </Spin>
          </Content>

          <Footer style={{
            textAlign: 'center',
            padding: '16px 24px',
          }}>
            永不言弃投资平台 ©{new Date().getFullYear()} 提供专业量化分析工具
          </Footer>
        </Layout>
      </Layout>

      <style jsx global>{`
        .ant-layout {
          background-color: #f5f7fa;
        }
        
        .market-status {
          display: flex;
          align-items: center;
          gap: 16px;
          font-size: 14px;
          color: rgba(0,0,0,0.85);
        }
        
        .market-date {
          font-weight: bold;
          color: #2a9d8f;
        }
        
        .market-tag {
          display: inline-flex;
          align-items: center;
          background: rgba(42, 157, 143, 0.1);
          border-radius: 4px;
          padding: 2px 8px;
          border: 1px solid rgba(42, 157, 143, 0.3);
        }
        
        .market-status-tag {
          background: rgba(66, 135, 245, 0.1);
          border: 1px solid rgba(66, 135, 245, 0.3);
        }
        
        .market-label {
          opacity: 0.7;
          margin-right: 4px;
        }
        
        .market-value {
          font-weight: bold;
        }
        
        .up {
          color: #cf1322;
        }
        
        .down {
          color: #389e0d;
        }
        
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
        
        .ant-table-row:hover {
          background: rgba(42, 157, 143, 0.05) !important;
        }
        
        .ant-table-thead > tr > th {
          background: #fafafa !important;
          font-weight: bold !important;
          color: rgba(0,0,0,0.85) !important;
        }
      `}</style>
    </Router>
  );
};

export default App;