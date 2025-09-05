# AStock - A股数据管理系统

## 项目简介

AStock 是一个基于 Flask + React 的 A股数据管理系统，提供股票基础信息、行情数据、行业分类、概念板块等数据的存储、查询和管理功能。系统支持数据的自动同步、实时查询和可视化展示。

## 功能特性

### 🏢 股票管理
- **公司信息管理**: 支持 A股上市公司的基本信息管理
- **股票代码管理**: 统一的股票代码体系，支持沪深两市
- **公司分类**: 按地区、行业、市场类型等维度分类管理

### 📊 行情数据
- **日线数据**: 完整的股票日线行情数据
- **历史数据**: 支持历史数据的批量导入和查询
- **增量更新**: 智能检测数据更新状态，支持增量同步
- **数据统计**: 提供成交量、成交额、涨跌幅等关键指标

### 🏭 行业管理
- **行业分类**: 支持多级行业分类体系
- **行业统计**: 按行业统计公司数量、交易数据等
- **动态更新**: 支持行业数据的动态更新和管理

### 🎯 概念板块
- **同花顺概念**: 集成同花顺概念板块数据
- **东方财富概念**: 支持东方财富概念板块管理
- **成分股管理**: 概念板块下的成分股管理
- **板块行情**: 概念板块的整体行情数据

### 🔥 热榜数据
- **同花顺热榜**: 集成同花顺App热榜数据
- **多类型支持**: 支持热股、ETF、可转债、行业板块、概念板块、期货、港股、热基、美股等
- **实时排行**: 每日盘中4次、收盘后4次数据更新
- **热度分析**: 提供热度值、上榜解读、标签等详细信息

### 👥 用户系统
- **用户管理**: 完整的用户注册、登录、权限管理
- **自选股**: 用户可添加关注股票，构建个人股票池
- **个性化**: 支持用户个性化设置和数据展示

## 技术架构

### 后端技术栈
- **框架**: Flask 2.x
- **数据库**: MySQL 8.0+
- **ORM**: SQLAlchemy
- **API**: RESTful API 设计
- **数据源**: Tushare Pro API
- **并发**: 多线程 + 线程池
- **日志**: Python logging 模块

### 前端技术栈
- **框架**: React 18.x
- **UI组件**: Ant Design 5.x
- **路由**: React Router 6.x
- **状态管理**: React Hooks
- **HTTP客户端**: Axios
- **样式**: CSS3 + Ant Design 主题

### 数据库设计
- **股票公司表** (`stock_company`): 公司基本信息
- **日线数据表** (`stock_daily`): 股票日线行情
- **行业表** (`industry`): 行业分类信息
- **行业统计表** (`industry_stats`): 行业统计数据
- **同花顺概念表** (`ths_index`): 同花顺概念板块
- **同花顺成分表** (`ths_member`): 概念板块成分股
- **东方财富概念表** (`dc_index`): 东方财富概念板块
- **东方财富成分表** (`dc_member`): 概念板块成分股
- **同花顺热榜表** (`ths_hot`): 同花顺App热榜数据
- **用户表** (`user`): 用户信息
- **用户自选股表** (`user_stock`): 用户关注的股票

## 项目结构

```
astock/
├── backend/                    # 后端代码
│   ├── app/
│   │   ├── api/               # API接口层
│   │   ├── models/            # 数据模型层
│   │   ├── services/          # 业务逻辑层
│   │   ├── scripts/           # 数据初始化脚本
│   │   ├── __init__.py        # Flask应用初始化
│   │   └── config.py          # 配置文件
│   ├── requirements.txt       # Python依赖
│   └── run.py                 # 启动脚本
├── frontend/                   # 前端代码
│   ├── src/
│   │   ├── api/               # API调用封装
│   │   ├── pages/             # 页面组件
│   │   ├── components/        # 通用组件
│   │   ├── App.js             # 主应用组件
│   │   └── index.js           # 入口文件
│   ├── package.json           # Node.js依赖
│   └── public/                # 静态资源
├── docs/                       # 项目文档
├── scripts/                    # 部署脚本
└── README.md                   # 项目说明
```

## 部署指南

### 环境要求
- **Python**: 3.8+
- **Node.js**: 16+
- **MySQL**: 8.0+
- **Redis**: 6.0+ (可选，用于缓存)

### 后端部署

1. **克隆项目**
```bash
git clone <repository-url>
cd astock/backend
```

2. **创建虚拟环境**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows
```

3. **安装依赖**
```bash
pip install -r requirements.txt
```

4. **配置数据库**
```bash
# 创建数据库
mysql -u root -p
CREATE DATABASE astock CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 配置数据库连接
cp config.py.example config.py
# 编辑 config.py 中的数据库连接信息
```

5. **初始化数据**
```bash
# 初始化公司数据
python app/scripts/init_stock_company.py

# 初始化行业数据
python app/scripts/init_industry.py

# 初始化日线数据
python app/scripts/init_stock_daily.py

# 初始化概念板块数据
python app/scripts/init_ths_index.py
python app/scripts/init_dc_index.py
```

6. **启动服务**
```bash
python run.py
```

### 前端部署

1. **安装依赖**
```bash
cd frontend
npm install
```

2. **配置环境变量**
```bash
cp .env.example .env
# 编辑 .env 中的API地址
```

3. **开发环境启动**
```bash
npm start
```

4. **生产环境构建**
```bash
npm run build
```

### Docker 部署 (推荐)

1. **构建镜像**
```bash
docker-compose build
```

2. **启动服务**
```bash
docker-compose up -d
```

## 界面截图

### 股票列表页面
![股票列表页面](docs/images/stock-list.png)

### 行情数据页面
![行情数据页面](docs/images/stock-daily.png)

### 行业管理页面
![行业管理页面](docs/images/industry.png)

### 概念板块页面
![概念板块页面](docs/images/concept.png)

### 用户自选股页面
![用户自选股页面](docs/images/user-stocks.png)

## 功能规划

### 已完成功能 ✅
- [x] 股票基础信息管理
- [x] 日线行情数据管理
- [x] 行业分类管理
- [x] 同花顺概念板块
- [x] 东方财富概念板块
- [x] 同花顺热榜数据
- [x] 用户系统基础功能
- [x] 数据自动同步脚本
- [x] RESTful API 接口
- [x] 前端基础页面

### 开发中功能 🚧
- [ ] 实时行情推送
- [ ] 技术指标计算
- [ ] 数据可视化图表
- [ ] 用户权限管理

### 计划功能 📋
- [ ] 财务数据管理
- [ ] 新闻资讯集成
- [ ] 投资组合管理
- [ ] 风险分析工具
- [ ] 移动端适配
- [ ] 数据导出功能
- [ ] 系统监控告警

## 技术路线图 (Roadmap)

### Phase 1: 基础功能完善 (Q1 2025)
- [ ] 完善用户权限系统
- [ ] 优化数据同步性能
- [ ] 增加数据质量检查
- [ ] 完善错误处理机制

### Phase 2: 功能扩展 (Q2 2025)
- [ ] 集成更多数据源
- [ ] 增加技术分析指标
- [ ] 实现实时数据推送
- [ ] 优化前端用户体验

### Phase 3: 智能化升级 (Q3 2025)
- [ ] 机器学习模型集成
- [ ] 智能投资建议
- [ ] 风险预警系统
- [ ] 个性化推荐

### Phase 4: 生态建设 (Q4 2025)
- [ ] 开放API平台
- [ ] 第三方插件系统
- [ ] 社区功能建设
- [ ] 商业化探索

## 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 联系方式

- **项目维护者**: [Xu ChongFeng]
- **邮箱**: [far.far.away.away@gmail.com]
- **项目地址**: [GitHub Repository URL]
- **问题反馈**: [Issues Page URL]

## 致谢

感谢以下开源项目和服务：
- [Flask](https://flask.palletsprojects.com/) - Python Web框架
- [React](https://reactjs.org/) - 前端框架
- [Ant Design](https://ant.design/) - UI组件库
- [Tushare](https://tushare.pro/) - 金融数据服务
- [MySQL](https://www.mysql.com/) - 数据库服务

---

**注意**: 本项目仅供学习和研究使用，请勿用于商业用途。使用Tushare等第三方数据服务时，请遵守相关服务条款。 