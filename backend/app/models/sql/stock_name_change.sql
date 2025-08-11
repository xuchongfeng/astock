CREATE TABLE IF NOT EXISTS `stock_name_change` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `ts_code` VARCHAR(16) NOT NULL COMMENT 'TS代码',
    `name` VARCHAR(64) NOT NULL COMMENT '证券名称',
    `start_date` DATE COMMENT '开始日期',
    `end_date` DATE COMMENT '结束日期',
    `ann_date` DATE COMMENT '公告日期',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    
    -- 索引
    INDEX `idx_ts_code` (`ts_code`),
    INDEX `idx_start_date` (`start_date`),
    INDEX `idx_end_date` (`end_date`),
    INDEX `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='股票曾用名表'; 