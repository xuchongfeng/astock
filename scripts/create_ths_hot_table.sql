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

-- 添加唯一约束，防止重复数据
ALTER TABLE `ths_hot` 
ADD UNIQUE KEY `uk_trade_date_data_type_ts_code` (`trade_date`, `data_type`, `ts_code`);

-- 插入示例数据（可选）
INSERT INTO `ths_hot` (`trade_date`, `data_type`, `ts_code`, `ts_name`, `rank`, `pct_change`, `current_price`, `concept`, `rank_reason`, `hot`, `rank_time`) VALUES
('2024-01-15', '热股', '000001.SZ', '平安银行', 1, 2.5, 12.34, '["银行", "金融科技"]', '银行股领涨，金融科技概念活跃', 150000.0, '09:30:00'),
('2024-01-15', '热股', '000002.SZ', '万科A', 2, 1.8, 18.56, '["房地产", "物业管理"]', '房地产政策利好，物业管理概念走强', 120000.0, '09:30:00'),
('2024-01-15', 'ETF', '510300.SH', '沪深300ETF', 1, 0.8, 3.45, '["指数ETF", "蓝筹股"]', '大盘指数上涨，蓝筹股表现稳健', 80000.0, '09:30:00'),
('2024-01-15', '概念板块', 'AI概念', '人工智能', 1, 3.2, NULL, '["AI", "科技"]', 'AI概念股集体走强，科技股领涨', 200000.0, '09:30:00');

-- 查看表结构
DESCRIBE `ths_hot`;

-- 查看索引
SHOW INDEX FROM `ths_hot`; 