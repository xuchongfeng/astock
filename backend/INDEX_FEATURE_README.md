# 指数功能说明文档

## 概述

本系统新增了完整的指数相关功能，包括指数基本信息和日线行情数据的管理。这些功能基于Tushare的API接口，提供了完整的CRUD操作和查询功能。

## 功能特性

### 1. 指数基本信息 (Index Basic)
- **数据来源**: Tushare `index_basic` 接口
- **主要字段**:
  - `ts_code`: TS代码（唯一标识）
  - `name`: 指数简称
  - `fullname`: 指数全称
  - `market`: 市场（SSE、SZSE、CSI、SW、CICC、MSCI、OTH）
  - `publisher`: 发布方
  - `index_type`: 指数风格
  - `category`: 指数类别
  - `base_date`: 基期
  - `base_point`: 基点
  - `list_date`: 发布日期
  - `weight_rule`: 加权方式
  - `desc`: 描述
  - `exp_date`: 终止日期

### 2. 指数日线行情 (Index Daily)
- **数据来源**: Tushare `index_daily` 接口
- **主要字段**:
  - `ts_code`: TS代码
  - `trade_date`: 交易日期
  - `close`: 收盘点位
  - `open`: 开盘点位
  - `high`: 最高点位
  - `low`: 最低点位
  - `pre_close`: 昨收点位
  - `change`: 涨跌点位
  - `pct_chg`: 涨跌幅（%）
  - `vol`: 成交量
  - `amount`: 成交额（千元）

## 数据库表结构

### index_basic 表
```sql
CREATE TABLE index_basic (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    ts_code VARCHAR(16) NOT NULL UNIQUE COMMENT 'TS代码',
    name VARCHAR(64) NOT NULL COMMENT '简称',
    fullname VARCHAR(128) COMMENT '指数全称',
    market VARCHAR(16) COMMENT '市场',
    publisher VARCHAR(32) COMMENT '发布方',
    index_type VARCHAR(32) COMMENT '指数风格',
    category VARCHAR(32) COMMENT '指数类别',
    base_date VARCHAR(8) COMMENT '基期',
    base_point DECIMAL(12,2) COMMENT '基点',
    list_date VARCHAR(8) COMMENT '发布日期',
    weight_rule VARCHAR(32) COMMENT '加权方式',
    `desc` TEXT COMMENT '描述',
    exp_date VARCHAR(8) COMMENT '终止日期',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_market (market),
    INDEX idx_publisher (publisher),
    INDEX idx_category (category)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='指数基本信息表';
```

### index_daily 表
```sql
CREATE TABLE index_daily (
    id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    ts_code VARCHAR(16) NOT NULL COMMENT 'TS代码',
    trade_date DATE NOT NULL COMMENT '交易日期',
    close DECIMAL(12,4) COMMENT '收盘点位',
    open DECIMAL(12,4) COMMENT '开盘点位',
    high DECIMAL(12,4) COMMENT '最高点位',
    low DECIMAL(12,4) COMMENT '最低点位',
    pre_close DECIMAL(12,4) COMMENT '昨收点位',
    change DECIMAL(12,4) COMMENT '涨跌点位',
    pct_chg DECIMAL(8,4) COMMENT '涨跌幅（%）',
    vol DECIMAL(20,4) COMMENT '成交量',
    amount DECIMAL(20,4) COMMENT '成交额（千元）',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    UNIQUE KEY uk_ts_code_trade_date (ts_code, trade_date),
    INDEX idx_trade_date (trade_date),
    INDEX idx_ts_code (ts_code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='指数日线行情表';
```

## API接口

### 指数基本信息API (`/api/index_basic`)

#### GET 接口
- `GET /index_basic` - 获取所有指数基本信息
- `GET /index_basic/<ts_code>` - 根据TS代码获取指数基本信息
- `GET /index_basic/market/<market>` - 根据市场获取指数基本信息
- `GET /index_basic/publisher/<publisher>` - 根据发布方获取指数基本信息
- `GET /index_basic/category/<category>` - 根据指数类别获取指数基本信息
- `GET /index_basic/search?keyword=<keyword>` - 搜索指数基本信息

#### POST 接口
- `POST /index_basic` - 创建指数基本信息

#### PUT 接口
- `PUT /index_basic/<ts_code>` - 更新指数基本信息

#### DELETE 接口
- `DELETE /index_basic/<ts_code>` - 删除指数基本信息

### 指数日线行情API (`/api/index_daily`)

#### GET 接口
- `GET /index_daily` - 获取所有指数日线行情
- `GET /index_daily/<ts_code>` - 根据TS代码获取指数日线行情
- `GET /index_daily/<ts_code>/range?start_date=<date>&end_date=<date>` - 根据日期范围获取指数日线行情
- `GET /index_daily/date/<trade_date>` - 根据交易日期获取所有指数日线行情
- `GET /index_daily/<ts_code>/latest` - 获取指定指数的最新日线行情
- `GET /index_daily/<ts_code>/statistics?days=<days>` - 获取指定指数的统计信息

#### POST 接口
- `POST /index_daily` - 创建指数日线行情
- `POST /index_daily/batch` - 批量创建指数日线行情

#### PUT 接口
- `PUT /index_daily/<ts_code>/<trade_date>` - 更新指数日线行情

#### DELETE 接口
- `DELETE /index_daily/<ts_code>/<trade_date>` - 删除指数日线行情

## 服务层功能

### IndexBasicService
- `get_all_index_basic()` - 获取所有指数基本信息
- `get_index_basic_by_ts_code(ts_code)` - 根据TS代码获取指数基本信息
- `get_index_basic_by_market(market)` - 根据市场获取指数基本信息
- `get_index_basic_by_publisher(publisher)` - 根据发布方获取指数基本信息
- `get_index_basic_by_category(category)` - 根据指数类别获取指数基本信息
- `search_index_basic(keyword)` - 搜索指数基本信息
- `create_index_basic(data)` - 创建指数基本信息
- `update_index_basic(ts_code, data)` - 更新指数基本信息
- `delete_index_basic(ts_code)` - 删除指数基本信息

### IndexDailyService
- `get_all_index_daily()` - 获取所有指数日线行情
- `get_index_daily_by_ts_code(ts_code, limit)` - 根据TS代码获取指数日线行情
- `get_index_daily_by_date_range(ts_code, start_date, end_date)` - 根据日期范围获取指数日线行情
- `get_index_daily_by_trade_date(trade_date)` - 根据交易日期获取所有指数日线行情
- `get_latest_index_daily(ts_code)` - 获取指定指数的最新日线行情
- `get_index_daily_statistics(ts_code, days)` - 获取指定指数的统计信息
- `create_index_daily(data)` - 创建指数日线行情
- `batch_create_index_daily(data_list)` - 批量创建指数日线行情
- `update_index_daily(ts_code, trade_date, data)` - 更新指数日线行情
- `delete_index_daily(ts_code, trade_date)` - 删除指数日线行情

## 初始化脚本

### 1. 指数基本信息初始化 (`scripts/init_index_basic.py`)
- 从Tushare获取所有市场的指数基本信息
- 支持增量更新
- 支持按市场、发布方分别获取

### 2. 指数日线行情初始化 (`scripts/init_index_daily.py`)
- 支持按指数代码初始化
- 支持按市场批量初始化
- 支持按日期范围获取数据
- 支持增量更新

### 3. 总初始化脚本 (`init_all.py`)
- 已更新，包含指数相关初始化脚本
- 按顺序执行所有初始化操作

## 使用方法

### 1. 环境准备
```bash
# 安装依赖
pip install tushare pandas

# 设置Tushare token
export TUSHARE_TOKEN="your_token_here"
```

### 2. 数据库初始化
```bash
# 运行SQL脚本创建表
mysql -u username -p database_name < app/models/sql/index_basic.sql
mysql -u username -p database_name < app/models/sql/index_daily.sql
```

### 3. 数据初始化
```bash
# 初始化指数基本信息
cd backend
python scripts/init_index_basic.py

# 初始化指数日线行情
python scripts/init_index_daily.py

# 或者运行总初始化脚本
python init_all.py
```

### 4. 功能测试
```bash
# 运行集成测试
python test_index_integration.py
```

## 注意事项

1. **Tushare Token**: 需要有效的Tushare Pro token才能获取数据
2. **数据更新**: 建议定期运行初始化脚本以获取最新数据
3. **数据库连接**: 确保数据库连接配置正确
4. **内存使用**: 批量处理大量数据时注意内存使用情况
5. **API限制**: 注意Tushare的API调用频率限制

## 扩展功能

### 1. 指数成分股管理
- 可以扩展指数成分股信息表
- 支持成分股权重查询

### 2. 指数技术指标
- 可以基于日线数据计算技术指标
- 支持移动平均线、RSI等常用指标

### 3. 指数对比分析
- 支持多个指数的对比分析
- 提供相关性分析功能

### 4. 实时数据更新
- 可以集成实时数据源
- 支持定时自动更新

## 故障排除

### 常见问题

1. **表不存在错误**
   - 检查SQL脚本是否已执行
   - 确认数据库连接正常

2. **Tushare API错误**
   - 检查token是否有效
   - 确认API调用频率未超限

3. **数据格式错误**
   - 检查日期格式是否正确
   - 确认数值字段类型匹配

4. **内存不足**
   - 减少批量处理的数据量
   - 分批处理大量数据

### 日志查看
```bash
# 查看应用日志
tail -f logs/app.log

# 查看初始化脚本日志
python scripts/init_index_basic.py 2>&1 | tee init.log
```

## 联系支持

如有问题或建议，请联系开发团队或查看相关文档。
