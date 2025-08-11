CREATE TABLE IF NOT EXISTS `ipo_stock` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `ts_code` VARCHAR(16) NOT NULL UNIQUE COMMENT 'TS代码',
    `name` VARCHAR(64) NOT NULL COMMENT '股票名称',
    `ipo_date` DATE COMMENT '上市日期',
    `issue_date` DATE COMMENT '发行日期',
    `amount` FLOAT COMMENT '发行总量（万股）',
    `market_amount` FLOAT COMMENT '发行流通市值（万元）',
    `price` FLOAT COMMENT '发行价格',
    `pe` FLOAT COMMENT '发行市盈率',
    `limit_amount` FLOAT COMMENT '发行后总股本（万股）',
    `funds` FLOAT COMMENT '募集资金（万元）',
    `ballot` FLOAT COMMENT '中签率',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    
    -- 索引
    INDEX `idx_ipo_date` (`ipo_date`),
    INDEX `idx_issue_date` (`issue_date`),
    INDEX `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='IPO新股信息表'; 