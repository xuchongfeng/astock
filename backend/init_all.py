#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
总初始化脚本
依次执行所有必要的初始化操作
"""

import os
import sys
import subprocess
import time
from datetime import datetime

def run_script(script_name, description):
    """运行指定的初始化脚本"""
    print(f"\n{'='*60}")
    print(f"开始执行: {description}")
    print(f"脚本: {script_name}")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}")
    
    try:
        script_path = os.path.join('app', 'scripts', script_name)
        
        if not os.path.exists(script_path):
            print(f"❌ 错误: 脚本 {script_path} 不存在")
            return False
        
        print(f"执行命令: python3 {script_path}")
        result = subprocess.run(
            ['python3', script_path],
            capture_output=True,
            text=True,
            cwd=os.getcwd()
        )
        
        if result.returncode == 0:
            print(f"✅ {description} 执行成功")
            if result.stdout:
                print("输出:")
                print(result.stdout)
            return True
        else:
            print(f"❌ {description} 执行失败")
            print(f"返回码: {result.returncode}")
            if result.stderr:
                print("错误信息:")
                print(result.stderr)
            if result.stdout:
                print("输出:")
                print(result.stdout)
            return False
            
    except Exception as e:
        print(f"❌ 执行 {description} 时发生异常: {e}")
        return False

def main():
    """主函数"""
    print("🚀 开始执行总初始化脚本")
    print(f"当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"当前目录: {os.getcwd()}")
    
    # 定义要执行的初始化脚本
    init_scripts = [
        ('init_stock_daily.py', '初始化股票日线数据'),
        ('init_daily_strategy.py', '初始化日线策略数据'),
        ('init_ths_index_daily.py', '初始化同花顺指数日线数据'),
        ('init_index_basic.py', '初始化指数基本信息'),
        ('init_index_daily.py', '初始化指数日线行情数据')
    ]
    
    success_count = 0
    total_count = len(init_scripts)
    
    for i, (script, description) in enumerate(init_scripts, 1):
        print(f"\n📋 进度: {i}/{total_count}")
        
        success = run_script(script, description)
        if success:
            success_count += 1
        
        # 在脚本之间添加短暂延迟
        if i < total_count:
            print("\n⏳ 等待5秒后继续下一个脚本...")
            time.sleep(5)
    
    # 输出执行结果
    print(f"\n{'='*60}")
    print("🏁 初始化执行完成")
    print(f"{'='*60}")
    print(f"总脚本数: {total_count}")
    print(f"成功执行: {success_count}")
    print(f"失败数量: {total_count - success_count}")
    print(f"完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if success_count == total_count:
        print("\n🎉 所有初始化脚本执行成功！")
    else:
        print(f"\n⚠️  有 {total_count - success_count} 个脚本执行失败")
    
    print(f"\n{'='*60}")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断了初始化过程")
    except Exception as e:
        print(f"\n❌ 初始化过程中发生错误: {e}")
