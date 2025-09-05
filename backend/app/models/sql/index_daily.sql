CREATE TABLE index_daily (
    id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    ts_code VARCHAR(16) NOT NULL COMMENT 'TS代码',
    trade_date DATE NOT NULL COMMENT '交易日期',
    close DECIMAL(12,4) COMMENT '收盘点位',
    open DECIMAL(12,4) COMMENT '开盘点位',
    high DECIMAL(12,4) COMMENT '最高点位',
    low DECIMAL(12,4) COMMENT '最低点位',
    pre_close DECIMAL(12,4) COMMENT '昨收点位',
    `change` DECIMAL(12,4) COMMENT '涨跌点位',
    pct_chg DECIMAL(8,4) COMMENT '涨跌幅（%）',
    vol DECIMAL(20,4) COMMENT '成交量',
    amount DECIMAL(20,4) COMMENT '成交额（千元）',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    UNIQUE KEY uk_ts_code_trade_date (ts_code, trade_date),
    INDEX idx_trade_date (trade_date),
    INDEX idx_ts_code (ts_code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='指数日线行情表';
