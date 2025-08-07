CREATE TABLE IF NOT EXISTS `index_daily_basic` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `ts_code` VARCHAR(20) NOT NULL COMMENT 'TS代码',
    `trade_date` DATE NOT NULL COMMENT '交易日期',
    `total_mv` FLOAT COMMENT '当日总市值（元）',
    `float_mv` FLOAT COMMENT '当日流通市值（元）',
    `total_share` FLOAT COMMENT '当日总股本（股）',
    `float_share` FLOAT COMMENT '当日流通股本（股）',
    `free_share` FLOAT COMMENT '当日自由流通股本（股）',
    `turnover_rate` FLOAT COMMENT '换手率',
    `turnover_rate_f` FLOAT COMMENT '换手率(基于自由流通股本)',
    `pe` FLOAT COMMENT '市盈率',
    `pe_ttm` FLOAT COMMENT '市盈率TTM',
    `pb` FLOAT COMMENT '市净率',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    
    -- 索引
    INDEX `idx_ts_code` (`ts_code`),
    INDEX `idx_trade_date` (`trade_date`),
    INDEX `idx_created_at` (`created_at`),
    
    -- 唯一约束
    UNIQUE KEY `uk_ts_code_trade_date` (`ts_code`, `trade_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='大盘指数每日指标表'; 