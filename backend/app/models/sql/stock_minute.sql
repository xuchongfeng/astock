CREATE TABLE IF NOT EXISTS `stock_minute` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `ts_code` VARCHAR(16) NOT NULL COMMENT 'TS代码',
    `trade_time` DATETIME NOT NULL COMMENT '交易时间',
    `open` FLOAT COMMENT '开盘价',
    `high` FLOAT COMMENT '最高价',
    `low` FLOAT COMMENT '最低价',
    `close` FLOAT COMMENT '收盘价',
    `pre_close` FLOAT COMMENT '昨收价',
    `change` FLOAT COMMENT '涨跌额',
    `pct_chg` FLOAT COMMENT '涨跌幅',
    `vol` BIGINT COMMENT '成交量（手）',
    `amount` FLOAT COMMENT '成交额（千元）',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    
    -- 索引
    INDEX `idx_ts_code` (`ts_code`),
    INDEX `idx_trade_time` (`trade_time`),
    INDEX `idx_created_at` (`created_at`),
    
    -- 唯一约束
    UNIQUE KEY `uk_ts_code_trade_time` (`ts_code`, `trade_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='分钟行情数据表'; 