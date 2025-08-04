#!/usr/bin/env python3
"""
股票日线数据获取示例脚本
展示如何自定义配置运行多线程数据获取
"""

import sys
import os
import time
import logging

# 添加脚本路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from init_stock_daily import main as run_stock_daily
from config import THREADING_CONFIG, TUSHARE_CONFIG, DB_CONFIG, LOGGING_CONFIG

def custom_config_example():
    """自定义配置示例"""
    print("=== 股票日线数据获取 - 自定义配置示例 ===")
    
    # 示例1: 高性能配置（更多线程，更小批次）
    print("\n1. 高性能配置:")
    THREADING_CONFIG.update({
        'max_workers': 20,      # 增加线程数
        'batch_size': 30,       # 减小批次大小
        'batch_delay': 0.5,     # 减少延迟
    })
    TUSHARE_CONFIG.update({
        'retry_times': 2,       # 减少重试次数
        'retry_delay': 0.5,     # 减少重试延迟
    })
    
    print(f"线程数: {THREADING_CONFIG['max_workers']}")
    print(f"批次大小: {THREADING_CONFIG['batch_size']}")
    print(f"重试次数: {TUSHARE_CONFIG['retry_times']}")
    
    # 运行高性能配置
    start_time = time.time()
    success, failed, elapsed = run_stock_daily()
    print(f"高性能配置完成，耗时: {elapsed:.2f}秒")
    
    # 示例2: 稳定配置（较少线程，更大批次）
    print("\n2. 稳定配置:")
    THREADING_CONFIG.update({
        'max_workers': 5,       # 减少线程数
        'batch_size': 100,      # 增大批次大小
        'batch_delay': 2,       # 增加延迟
    })
    TUSHARE_CONFIG.update({
        'retry_times': 5,       # 增加重试次数
        'retry_delay': 2,       # 增加重试延迟
    })
    
    print(f"线程数: {THREADING_CONFIG['max_workers']}")
    print(f"批次大小: {THREADING_CONFIG['batch_size']}")
    print(f"重试次数: {TUSHARE_CONFIG['retry_times']}")
    
    # 运行稳定配置
    start_time = time.time()
    success, failed, elapsed = run_stock_daily()
    print(f"稳定配置完成，耗时: {elapsed:.2f}秒")

def production_config():
    """生产环境配置"""
    print("\n=== 生产环境配置 ===")
    
    # 生产环境推荐配置
    THREADING_CONFIG.update({
        'max_workers': 8,       # 适中的线程数
        'batch_size': 50,       # 适中的批次大小
        'batch_delay': 1,       # 适中的延迟
    })
    TUSHARE_CONFIG.update({
        'retry_times': 3,       # 适中的重试次数
        'retry_delay': 1,       # 适中的重试延迟
    })
    
    # 设置日志文件
    LOGGING_CONFIG.update({
        'file': 'stock_daily_production.log',
        'level': 'INFO',
    })
    
    print("生产环境配置:")
    print(f"- 线程数: {THREADING_CONFIG['max_workers']}")
    print(f"- 批次大小: {THREADING_CONFIG['batch_size']}")
    print(f"- 重试次数: {TUSHARE_CONFIG['retry_times']}")
    print(f"- 日志文件: {LOGGING_CONFIG['file']}")
    
    # 运行生产配置
    success, failed, elapsed = run_stock_daily()
    print(f"生产配置完成，耗时: {elapsed:.2f}秒")
    print(f"成功: {success}, 失败: {failed}")

def test_config():
    """测试环境配置"""
    print("\n=== 测试环境配置 ===")
    
    # 测试环境配置（少量数据，快速验证）
    THREADING_CONFIG.update({
        'max_workers': 3,       # 少量线程
        'batch_size': 10,       # 小批次
        'batch_delay': 0.5,     # 短延迟
    })
    TUSHARE_CONFIG.update({
        'retry_times': 2,       # 少量重试
        'retry_delay': 0.5,     # 短重试延迟
    })
    
    print("测试环境配置:")
    print(f"- 线程数: {THREADING_CONFIG['max_workers']}")
    print(f"- 批次大小: {THREADING_CONFIG['batch_size']}")
    print(f"- 重试次数: {TUSHARE_CONFIG['retry_times']}")
    
    # 运行测试配置
    success, failed, elapsed = run_stock_daily()
    print(f"测试配置完成，耗时: {elapsed:.2f}秒")
    print(f"成功: {success}, 失败: {failed}")

def main():
    """主函数"""
    print("股票日线数据获取 - 多线程配置示例")
    print("=" * 50)
    
    # 显示当前默认配置
    print("当前默认配置:")
    print(f"- 线程数: {THREADING_CONFIG['max_workers']}")
    print(f"- 批次大小: {THREADING_CONFIG['batch_size']}")
    print(f"- 重试次数: {TUSHARE_CONFIG['retry_times']}")
    
    # 运行不同配置示例
    try:
        # 测试配置
        test_config()
        
        # 生产配置
        production_config()
        
        # 自定义配置示例
        custom_config_example()
        
    except KeyboardInterrupt:
        print("\n用户中断执行")
    except Exception as e:
        print(f"执行过程中发生错误: {e}")
        logging.error(f"执行错误: {e}")

if __name__ == "__main__":
    main() 