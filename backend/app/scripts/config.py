# 脚本配置文件

# 多线程配置
THREADING_CONFIG = {
    'max_workers': 10,      # 最大线程数
    'batch_size': 50,       # 每批处理的股票数量
    'batch_delay': 1,       # 批次间延迟（秒）
    'timeout': 30,          # 单个请求超时时间（秒）
}

# Tushare配置
TUSHARE_CONFIG = {
    'token': None,          # 从环境变量获取
    'retry_times': 3,       # 重试次数
    'retry_delay': 1,       # 重试延迟（秒）
}

# 数据库配置
DB_CONFIG = {
    'batch_commit_size': 100,  # 批量提交大小
    'commit_delay': 0.1,       # 提交延迟（秒）
}

# 日志配置
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(levelname)s - %(message)s',
    'file': None,  # 如果设置为文件路径，则同时输出到文件
} 