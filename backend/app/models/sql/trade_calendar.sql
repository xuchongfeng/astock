CREATE TABLE IF NOT EXISTS `trade_calendar` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `exchange` VARCHAR(8) NOT NULL COMMENT '交易所 SSE上交所 SZSE深交所',
    `cal_date` DATE NOT NULL COMMENT '日历日期',
    `is_open` BOOLEAN NOT NULL COMMENT '是否交易 0休市 1交易',
    `pretrade_date` DATE COMMENT '上一交易日',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    
    -- 索引
    INDEX `idx_exchange` (`exchange`),
    INDEX `idx_cal_date` (`cal_date`),
    INDEX `idx_created_at` (`created_at`),
    
    -- 唯一约束
    UNIQUE KEY `uk_exchange_cal_date` (`exchange`, `cal_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='交易日历表'; 