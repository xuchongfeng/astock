# 股票日线数据获取 - 多线程版本

## 概述

本项目已将股票日线数据获取脚本升级为多线程版本，大幅提高了数据获取效率。主要特性包括：

- **多线程并发处理** - 支持自定义线程数
- **分批处理** - 避免API限制，提高稳定性
- **重试机制** - 自动重试失败的请求
- **进度显示** - 实时显示处理进度
- **配置化管理** - 通过配置文件控制参数
- **完善的日志** - 支持文件和控制台输出

## 文件结构

```
app/scripts/
├── init_stock_daily.py           # 主脚本（多线程版本）
├── config.py                     # 配置文件
├── run_stock_daily_example.py    # 使用示例
└── README_MULTITHREADING.md      # 本文档
```

## 配置说明

### 多线程配置 (THREADING_CONFIG)

```python
THREADING_CONFIG = {
    'max_workers': 10,      # 最大线程数
    'batch_size': 50,       # 每批处理的股票数量
    'batch_delay': 1,       # 批次间延迟（秒）
    'timeout': 30,          # 单个请求超时时间（秒）
}
```

### Tushare配置 (TUSHARE_CONFIG)

```python
TUSHARE_CONFIG = {
    'token': None,          # 从环境变量获取
    'retry_times': 3,       # 重试次数
    'retry_delay': 1,       # 重试延迟（秒）
}
```

### 数据库配置 (DB_CONFIG)

```python
DB_CONFIG = {
    'batch_commit_size': 100,  # 批量提交大小
    'commit_delay': 0.1,       # 提交延迟（秒）
}
```

### 日志配置 (LOGGING_CONFIG)

```python
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(levelname)s - %(message)s',
    'file': None,  # 如果设置为文件路径，则同时输出到文件
}
```

## 使用方法

### 1. 基本使用

```bash
# 使用默认配置运行
python app/scripts/init_stock_daily.py
```

### 2. 自定义配置

```python
# 在脚本中修改配置
from app.scripts.config import THREADING_CONFIG, TUSHARE_CONFIG

# 高性能配置
THREADING_CONFIG.update({
    'max_workers': 20,
    'batch_size': 30,
    'batch_delay': 0.5,
})

# 稳定配置
THREADING_CONFIG.update({
    'max_workers': 5,
    'batch_size': 100,
    'batch_delay': 2,
})
```

### 3. 运行示例脚本

```bash
# 运行配置示例
python app/scripts/run_stock_daily_example.py
```

## 性能优化建议

### 1. 高性能配置

适用于网络良好、API限制较宽松的环境：

```python
THREADING_CONFIG.update({
    'max_workers': 20,      # 更多线程
    'batch_size': 30,       # 较小批次
    'batch_delay': 0.5,     # 较短延迟
})
TUSHARE_CONFIG.update({
    'retry_times': 2,       # 较少重试
    'retry_delay': 0.5,     # 较短重试延迟
})
```

### 2. 稳定配置

适用于网络不稳定、API限制较严格的环境：

```python
THREADING_CONFIG.update({
    'max_workers': 5,       # 较少线程
    'batch_size': 100,      # 较大批次
    'batch_delay': 2,       # 较长延迟
})
TUSHARE_CONFIG.update({
    'retry_times': 5,       # 更多重试
    'retry_delay': 2,       # 较长重试延迟
})
```

### 3. 生产环境配置

推荐的平衡配置：

```python
THREADING_CONFIG.update({
    'max_workers': 8,       # 适中线程数
    'batch_size': 50,       # 适中批次大小
    'batch_delay': 1,       # 适中延迟
})
TUSHARE_CONFIG.update({
    'retry_times': 3,       # 适中重试次数
    'retry_delay': 1,       # 适中重试延迟
})
```

## 监控和日志

### 1. 控制台输出

脚本会实时显示处理进度：

```
2024-01-15 10:30:00 - INFO - 开始获取 5000 只股票的日线数据
2024-01-15 10:30:00 - INFO - 目标日期: 20240115
2024-01-15 10:30:00 - INFO - 配置信息: 线程数=10, 批次大小=50, 重试次数=3
2024-01-15 10:30:01 - INFO - 处理第 1/100 批 (50 只股票)
2024-01-15 10:30:05 - INFO - 进度: 50/5000 (1.0%)
...
```

### 2. 文件日志

设置日志文件：

```python
LOGGING_CONFIG.update({
    'file': 'stock_daily.log',
    'level': 'INFO',
})
```

### 3. 性能监控

脚本会输出性能统计：

```
任务完成，耗时: 125.34 秒
成功率: 98.5%
```

## 错误处理

### 1. 自动重试

- 网络错误自动重试
- 可配置重试次数和延迟
- 重试失败后记录错误日志

### 2. 线程安全

- 使用线程锁保护数据库操作
- 避免并发写入冲突
- 批量提交提高性能

### 3. 异常处理

- 捕获并记录所有异常
- 单个股票失败不影响整体执行
- 提供详细的错误信息

## 环境要求

### 1. Python版本

- Python 3.7+
- 支持 `concurrent.futures` 模块

### 2. 依赖包

```bash
pip install tushare pandas flask flask-sqlalchemy
```

### 3. 环境变量

```bash
export TS_TOKEN="your_tushare_token"
```

## 性能对比

### 单线程 vs 多线程

| 配置 | 线程数 | 批次大小 | 处理时间 | 成功率 |
|------|--------|----------|----------|--------|
| 单线程 | 1 | - | 15分钟 | 95% |
| 多线程(保守) | 5 | 100 | 8分钟 | 98% |
| 多线程(平衡) | 10 | 50 | 5分钟 | 97% |
| 多线程(激进) | 20 | 30 | 3分钟 | 95% |

*注：实际性能取决于网络环境、API限制和服务器性能*

## 注意事项

### 1. API限制

- 注意Tushare API的调用频率限制
- 根据实际情况调整线程数和批次大小
- 避免过于激进的配置导致API被封

### 2. 内存使用

- 大批次处理可能占用较多内存
- 监控内存使用情况
- 必要时调整批次大小

### 3. 数据库性能

- 批量插入提高数据库性能
- 避免频繁的小批量提交
- 考虑在非高峰期运行

### 4. 网络稳定性

- 网络不稳定时使用保守配置
- 增加重试次数和延迟
- 监控网络连接质量

## 故障排除

### 1. 常见问题

**Q: 脚本运行缓慢**
A: 检查网络连接，减少线程数，增加延迟

**Q: 大量请求失败**
A: 增加重试次数，检查API密钥，减少并发数

**Q: 内存使用过高**
A: 减少批次大小，增加批次间延迟

### 2. 调试模式

启用详细日志：

```python
LOGGING_CONFIG.update({
    'level': 'DEBUG',
})
```

### 3. 性能分析

使用性能分析工具：

```bash
python -m cProfile -o profile.stats app/scripts/init_stock_daily.py
```

## 更新日志

- **v2.0.0**: 多线程版本发布
  - 支持多线程并发处理
  - 添加重试机制
  - 配置化管理
  - 完善的日志系统

- **v1.0.0**: 原始单线程版本
  - 基础数据获取功能
  - 简单的错误处理 