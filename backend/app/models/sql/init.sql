CREATE TABLE stock_company (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    ts_code VARCHAR(16) NOT NULL UNIQUE COMMENT '股票代码（如 000001.SZ）',
    symbol VARCHAR(8) NOT NULL COMMENT '股票简称代码（如 000001）',
    name VARCHAR(64) NOT NULL COMMENT '公司简称',
    area VARCHAR(32) COMMENT '所在地区',
    industry VARCHAR(64) COMMENT '所属行业',
    fullname VARCHAR(128) COMMENT '公司全称',
    enname VARCHAR(128) COMMENT '英文全称',
    market VARCHAR(16) COMMENT '市场类型（主板/中小板/创业板/科创板等）',
    list_date DATE COMMENT '上市日期',
    exchange VARCHAR(8) COMMENT '交易所（SSE, SZSE等）',
    chairman VARCHAR(32) COMMENT '董事长',
    manager VARCHAR(32) COMMENT '总经理',
    secretary VARCHAR(32) COMMENT '董秘',
    reg_capital DECIMAL(20,2) COMMENT '注册资本（万元）',
    setup_date DATE COMMENT '成立日期',
    province VARCHAR(32) COMMENT '省份',
    website VARCHAR(128) COMMENT '公司网址',
    email VARCHAR(64) COMMENT '公司邮箱',
    employees INT COMMENT '员工人数',
    main_business TEXT COMMENT '主营业务',
    business_scope TEXT COMMENT '经营范围',
    status VARCHAR(16) COMMENT '上市状态（在市/退市/暂停上市）',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='A股公司基本信息表';


CREATE TABLE stock_daily (
    id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    ts_code VARCHAR(16) NOT NULL COMMENT '股票代码（如 000001.SZ）',
    trade_date DATE NOT NULL COMMENT '交易日期',
    open DECIMAL(12,4) COMMENT '开盘价',
    high DECIMAL(12,4) COMMENT '最高价',
    low DECIMAL(12,4) COMMENT '最低价',
    close DECIMAL(12,4) COMMENT '收盘价',
    pre_close DECIMAL(12,4) COMMENT '昨收价',
    change DECIMAL(12,4) COMMENT '涨跌额',
    pct_chg DECIMAL(8,4) COMMENT '涨跌幅（%）',
    vol BIGINT COMMENT '成交量（手）',
    amount DECIMAL(20,4) COMMENT '成交额（元）',
    turnover_rate DECIMAL(8,4) COMMENT '换手率（%）',
    UNIQUE KEY uk_ts_code_trade_date (ts_code, trade_date),
    INDEX idx_trade_date (trade_date),
    INDEX idx_ts_code (ts_code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='A股公司每日交易数据表';


CREATE TABLE industry (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    name VARCHAR(64) NOT NULL UNIQUE COMMENT '行业名称',
    description VARCHAR(255) COMMENT '行业描述',
    parent_id INT DEFAULT NULL COMMENT '父行业ID（如有多级行业分类）',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='A股公司行业表';


CREATE TABLE industry_stats (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    industry_id INT NOT NULL COMMENT '行业ID',
    stat_date DATE NOT NULL COMMENT '统计日期',
    company_count INT NOT NULL COMMENT '行业下公司总数',
    total_amount DECIMAL(24,4) NOT NULL COMMENT '行业公司当日成交总额（元）',
    up_count INT NOT NULL COMMENT '上涨公司数',
    down_count INT NOT NULL COMMENT '下跌公司数',
    flat_count INT NOT NULL COMMENT '平盘公司数',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    UNIQUE KEY uk_industry_date (industry_id, stat_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='行业每日统计数据表';

CREATE TABLE user (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    username VARCHAR(64) NOT NULL UNIQUE COMMENT '用户名',
    email VARCHAR(120) NOT NULL UNIQUE COMMENT '邮箱',
    password_hash VARCHAR(128) NOT NULL COMMENT '密码哈希',
    nickname VARCHAR(64) COMMENT '昵称',
    avatar VARCHAR(255) COMMENT '头像URL',
    status VARCHAR(16) DEFAULT 'active' COMMENT '状态：active/inactive',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';

CREATE TABLE user_stock (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    user_id INT NOT NULL COMMENT '用户ID',
    ts_code VARCHAR(16) NOT NULL COMMENT '股票代码',
    rating INT NULL COMMENT '评级',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '关注时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    UNIQUE KEY uk_user_stock (user_id, ts_code),
    INDEX idx_user_id (user_id),
    INDEX idx_ts_code (ts_code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户关注股票表';


CREATE TABLE ths_index (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    ts_code VARCHAR(16) NOT NULL UNIQUE COMMENT '指数代码',
    name VARCHAR(64) NOT NULL COMMENT '指数名称',
    count INT COMMENT '成分个数',
    exchange VARCHAR(8) COMMENT '交易所',
    list_date DATE COMMENT '上市日期',
    type VARCHAR(8) COMMENT '指数类型 N-概念指数 S-特色指数 I-行业指数等',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='同花顺行业概念板块表';


CREATE TABLE ths_member (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    ts_code VARCHAR(16) NOT NULL COMMENT '板块指数代码',
    con_code VARCHAR(16) NOT NULL COMMENT '股票代码',
    con_name VARCHAR(64) COMMENT '股票名称',
    weight FLOAT COMMENT '权重',
    in_date DATE COMMENT '纳入日期',
    out_date DATE COMMENT '剔除日期',
    is_new VARCHAR(2) COMMENT '是否最新Y是N否',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    UNIQUE KEY uk_ths_member (ts_code, con_code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='同花顺概念成分表';


CREATE TABLE stock_note (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    ts_code VARCHAR(16) NOT NULL COMMENT '股票代码',
    note_date DATE NOT NULL COMMENT '记录日期',
    comment TEXT COMMENT '评论',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_ts_code (ts_code),
    INDEX idx_note_date (note_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='股票记录表';

CREATE TABLE ths_index_daily (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    ts_code VARCHAR(16) NOT NULL COMMENT 'TS指数代码',
    trade_date DATE NOT NULL COMMENT '交易日',
    close DECIMAL(16,4) COMMENT '收盘点位',
    open DECIMAL(16,4) COMMENT '开盘点位',
    high DECIMAL(16,4) COMMENT '最高点位',
    low DECIMAL(16,4) COMMENT '最低点位',
    pre_close DECIMAL(16,4) COMMENT '昨日收盘点',
    avg_price DECIMAL(16,4) COMMENT '平均价',
    `change` DECIMAL(16,4) COMMENT '涨跌点位',
    pct_change DECIMAL(8,4) COMMENT '涨跌幅',
    vol DECIMAL(20,4) COMMENT '成交量',
    turnover_rate DECIMAL(8,4) COMMENT '换手率',
    total_mv DECIMAL(20,4) COMMENT '总市值',
    float_mv DECIMAL(20,4) COMMENT '流通市值',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    UNIQUE KEY uk_ts_code_trade_date (ts_code, trade_date),
    INDEX idx_ts_code (ts_code),
    INDEX idx_trade_date (trade_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='同花顺板块指数行情表';


CREATE TABLE strategy (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    name VARCHAR(64) NOT NULL UNIQUE COMMENT '策略名称',
    description TEXT COMMENT '策略描述',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='策略表';

CREATE TABLE strategy_stock (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    strategy_id INT NOT NULL COMMENT '策略ID',
    ts_code VARCHAR(16) NOT NULL COMMENT '股票代码',
    date DATE NULL COMMENT '关联日期',
    rating INT NULL COMMENT '评级',
    avg_amount_5d DECIMAL(20,4) NULL COMMENT '最近5日平均交易额',
    hit_count_5d INT NULL COMMENT '最近5日命中策略次数',
    hit_count_15d INT NULL COMMENT '最近15日命中策略次数',
    hit_count_30d INT NULL COMMENT '最近30日命中策略次数',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (strategy_id) REFERENCES strategy(id),
    INDEX idx_strategy_id (strategy_id),
    INDEX idx_ts_code (ts_code),
    INDEX idx_date (date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='策略关联股票表';

ALTER TABLE strategy_stock ADD COLUMN rating INT NULL COMMENT '评级';
ALTER TABLE strategy_stock ADD COLUMN avg_amount_5d DECIMAL(20,4) NULL COMMENT '最近5日平均交易额';
ALTER TABLE strategy_stock ADD COLUMN hit_count_5d INT NULL COMMENT '最近5日命中策略次数';
ALTER TABLE strategy_stock ADD COLUMN hit_count_15d INT NULL COMMENT '最近15日命中策略次数';
ALTER TABLE strategy_stock ADD COLUMN hit_count_30d INT NULL COMMENT '最近30日命中策略次数';

CREATE TABLE user_position (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    user_id INT NOT NULL COMMENT '用户ID',
    ts_code VARCHAR(16) NOT NULL COMMENT '股票代码',
    quantity INT NOT NULL COMMENT '持仓数量',
    avg_price DECIMAL(12,4) NOT NULL COMMENT '平均成本',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (user_id) REFERENCES user(id),
    INDEX idx_user_id (user_id),
    INDEX idx_ts_code (ts_code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='个人持仓表';

CREATE TABLE user_trade (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    user_id INT NOT NULL COMMENT '用户ID',
    ts_code VARCHAR(16) NOT NULL COMMENT '股票代码',
    trade_type VARCHAR(8) NOT NULL COMMENT '交易类型：buy/sell',
    quantity INT NOT NULL COMMENT '交易数量',
    price DECIMAL(12,4) NOT NULL COMMENT '交易价格',
    trade_date DATE NOT NULL COMMENT '交易日期',
    profit_loss DECIMAL(12,4) NULL COMMENT '盈利/亏损',
    note TEXT NULL COMMENT '笔记',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (user_id) REFERENCES user(id),
    INDEX idx_user_id (user_id),
    INDEX idx_ts_code (ts_code),
    INDEX idx_trade_date (trade_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='交易记录表';

ALTER TABLE strategy_stock ADD INDEX idx_date (date);

-- 概念股分类表
CREATE TABLE concept (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    code VARCHAR(16) NOT NULL COMMENT '概念分类ID',
    name VARCHAR(100) NOT NULL COMMENT '概念分类名称',
    src VARCHAR(10) DEFAULT 'ts' COMMENT '来源',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    UNIQUE KEY uk_code (code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='概念股分类表';

-- 股票标签表
CREATE TABLE tag (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    name VARCHAR(64) NOT NULL UNIQUE COMMENT '标签名称',
    description VARCHAR(255) COMMENT '标签描述',
    color VARCHAR(16) DEFAULT '#1890ff' COMMENT '标签颜色',
    category VARCHAR(32) DEFAULT 'trend' COMMENT '标签分类：trend-走势，status-状态，custom-自定义',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='股票标签表';

-- 股票标签关联表
CREATE TABLE stock_tag (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    ts_code VARCHAR(16) NOT NULL COMMENT '股票代码',
    tag_id INT NOT NULL COMMENT '标签ID',
    user_id INT NULL COMMENT '用户ID（NULL表示系统标签）',
    start_date DATE NULL COMMENT '标签开始日期',
    end_date DATE NULL COMMENT '标签结束日期',
    note TEXT COMMENT '备注',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (tag_id) REFERENCES tag(id),
    FOREIGN KEY (user_id) REFERENCES user(id),
    UNIQUE KEY uk_stock_tag_user (ts_code, tag_id, user_id),
    INDEX idx_ts_code (ts_code),
    INDEX idx_tag_id (tag_id),
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='股票标签关联表';

-- 创建同花顺热榜数据表
-- 参考文档: https://tushare.pro/document/2?doc_id=320

CREATE TABLE IF NOT EXISTS `ths_hot` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `trade_date` date NOT NULL COMMENT '交易日期',
  `data_type` varchar(50) NOT NULL COMMENT '数据类型',
  `ts_code` varchar(20) NOT NULL COMMENT '股票代码',
  `ts_name` varchar(100) NOT NULL COMMENT '股票名称',
  `rank` int NOT NULL COMMENT '排行',
  `pct_change` float DEFAULT NULL COMMENT '涨跌幅%',
  `current_price` float DEFAULT NULL COMMENT '当前价格',
  `concept` text COMMENT '标签',
  `rank_reason` text COMMENT '上榜解读',
  `hot` float DEFAULT NULL COMMENT '热度值',
  `rank_time` varchar(20) DEFAULT NULL COMMENT '排行榜获取时间',
  `created_at` timestamp DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_trade_date` (`trade_date`),
  KEY `idx_ts_code` (`ts_code`),
  KEY `idx_data_type` (`data_type`),
  KEY `idx_rank` (`rank`),
  KEY `idx_trade_date_data_type` (`trade_date`, `data_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='同花顺热榜数据表';
