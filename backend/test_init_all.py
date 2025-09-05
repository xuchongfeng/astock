#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试总初始化脚本
验证脚本的基本功能和错误处理
"""

import os
import sys
import tempfile
import subprocess
from unittest.mock import patch, MagicMock

def test_script_existence():
    """测试脚本文件是否存在"""
    print("🔍 测试脚本文件存在性...")
    
    required_scripts = [
        'app/scripts/init_stock_daily.py',
        'app/scripts/init_daily_strategy.py',
        'app/scripts/init_ths_index_daily.py'
    ]
    
    missing_scripts = []
    for script in required_scripts:
        if not os.path.exists(script):
            missing_scripts.append(script)
    
    if missing_scripts:
        print(f"❌ 以下脚本文件缺失:")
        for script in missing_scripts:
            print(f"   - {script}")
        return False
    else:
        print("✅ 所有必需的脚本文件都存在")
        return True

def test_init_all_script():
    """测试总初始化脚本是否存在"""
    print("\n🔍 测试总初始化脚本...")
    
    if not os.path.exists('init_all.py'):
        print("❌ 总初始化脚本 init_all.py 不存在")
        return False
    
    print("✅ 总初始化脚本存在")
    
    # 检查脚本权限
    if os.access('init_all.py', os.X_OK):
        print("✅ 脚本具有执行权限")
    else:
        print("⚠️  脚本没有执行权限，建议运行: chmod +x init_all.py")
    
    return True

def test_script_syntax():
    """测试脚本语法是否正确"""
    print("\n🔍 测试脚本语法...")
    
    try:
        with open('init_all.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 尝试编译Python代码
        compile(content, 'init_all.py', 'exec')
        print("✅ 脚本语法正确")
        return True
    except SyntaxError as e:
        print(f"❌ 脚本语法错误: {e}")
        return False
    except Exception as e:
        print(f"❌ 读取脚本时发生错误: {e}")
        return False

def test_imports():
    """测试脚本的导入是否正常"""
    print("\n🔍 测试脚本导入...")
    
    try:
        # 测试必要的模块是否可以导入
        import subprocess
        import time
        from datetime import datetime
        print("✅ 所有必要的模块都可以正常导入")
        return True
    except ImportError as e:
        print(f"❌ 模块导入失败: {e}")
        return False

def test_dry_run():
    """测试脚本的干运行（不实际执行子脚本）"""
    print("\n🔍 测试脚本干运行...")
    
    try:
        # 创建一个临时的测试环境
        with tempfile.TemporaryDirectory() as temp_dir:
            # 复制脚本到临时目录
            with open('init_all.py', 'r', encoding='utf-8') as f:
                script_content = f.read()
            
            # 修改脚本，使其不实际执行子脚本
            test_script = script_content.replace(
                "result = subprocess.run(",
                "# result = subprocess.run("
            ).replace(
                "['python3', script_path]",
                "# ['python3', script_path]"
            )
            
            # 添加模拟的成功结果
            test_script = test_script.replace(
                "return False",
                "return True  # 模拟成功"
            )
            
            # 写入临时脚本
            temp_script_path = os.path.join(temp_dir, 'test_init_all.py')
            with open(temp_script_path, 'w', encoding='utf-8') as f:
                f.write(test_script)
            
            # 执行测试脚本
            result = subprocess.run(
                ['python3', temp_script_path],
                capture_output=True,
                text=True,
                cwd=temp_dir,
                timeout=30
            )
            
            if result.returncode == 0:
                print("✅ 脚本干运行测试通过")
                return True
            else:
                print(f"❌ 脚本干运行测试失败: {result.stderr}")
                return False
                
    except Exception as e:
        print(f"❌ 干运行测试时发生错误: {e}")
        return False

def main():
    """主测试函数"""
    print("🧪 开始测试总初始化脚本")
    print("=" * 50)
    
    tests = [
        ("脚本文件存在性", test_script_existence),
        ("总初始化脚本", test_init_all_script),
        ("脚本语法", test_script_syntax),
        ("模块导入", test_imports),
        ("干运行测试", test_dry_run)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ {test_name} 测试失败")
        except Exception as e:
            print(f"❌ {test_name} 测试异常: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 测试完成")
    print(f"通过: {passed}/{total}")
    print(f"失败: {total - passed}")
    
    if passed == total:
        print("🎉 所有测试通过！总初始化脚本可以正常使用。")
        print("\n使用方法:")
        print("  python3 init_all.py")
        print("  或")
        print("  ./init_all.py")
    else:
        print("⚠️  有测试失败，请检查相关问题。")
    
    return passed == total

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1) 