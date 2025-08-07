-- DeepSeek对话记录表
CREATE TABLE IF NOT EXISTS `deepseek` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `session_id` VARCHAR(100) NOT NULL COMMENT '会话ID',
    `type` VARCHAR(20) NOT NULL COMMENT '类型：个股/大盘/行业',
    `content` TEXT NOT NULL COMMENT '返回内容',
    `date` DATE NOT NULL COMMENT '日期',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    
    -- 索引
    INDEX `idx_session_id` (`session_id`),
    INDEX `idx_type` (`type`),
    INDEX `idx_date` (`date`),
    INDEX `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='DeepSeek对话记录表'; 