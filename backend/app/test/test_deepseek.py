#!/usr/bin/env python3
"""
DeepSeek模块测试脚本
"""

import requests
import json
import os

# 设置环境变量（如果没有设置的话）
if not os.getenv('DEEPSEEK_API_KEY'):
    print("警告: 请设置DEEPSEEK_API_KEY环境变量")
    print("export DEEPSEEK_API_KEY='your_api_key'")

# 服务器地址
BASE_URL = "http://localhost:5000"

def test_get_models():
    """测试获取模型列表"""
    print("测试获取模型列表...")
    try:
        response = requests.get(f"{BASE_URL}/api/deepseek/models")
        if response.status_code == 200:
            data = response.json()
            print("✓ 获取模型列表成功")
            print(f"可用模型: {json.dumps(data, ensure_ascii=False, indent=2)}")
        else:
            print(f"✗ 获取模型列表失败: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"✗ 请求失败: {str(e)}")

def test_get_balance():
    """测试查询余额"""
    print("\n测试查询余额...")
    try:
        response = requests.get(f"{BASE_URL}/api/deepseek/balance")
        if response.status_code == 200:
            data = response.json()
            print("✓ 查询余额成功")
            print(f"余额信息: {json.dumps(data, ensure_ascii=False, indent=2)}")
        else:
            print(f"✗ 查询余额失败: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"✗ 请求失败: {str(e)}")

def test_single_chat():
    """测试单轮对话"""
    print("\n测试单轮对话...")
    try:
        data = {
            "message": "你好，请简单介绍一下自己",
            "model": "deepseek-chat",
            "temperature": 0.7,
            "max_tokens": 200
        }
        response = requests.post(f"{BASE_URL}/api/deepseek/chat/single", json=data)
        if response.status_code == 200:
            result = response.json()
            print("✓ 单轮对话成功")
            if 'choices' in result and len(result['choices']) > 0:
                content = result['choices'][0]['message']['content']
                print(f"AI回复: {content}")
            else:
                print(f"完整响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
        else:
            print(f"✗ 单轮对话失败: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"✗ 请求失败: {str(e)}")

def test_multi_round_chat():
    """测试多轮对话"""
    print("\n测试多轮对话...")
    try:
        # 第一轮对话
        conversation_history = [
            {"role": "user", "content": "你好"},
            {"role": "assistant", "content": "你好！有什么可以帮助你的吗？"}
        ]
        
        data = {
            "conversation_history": conversation_history,
            "message": "请介绍一下你的能力",
            "model": "deepseek-chat",
            "temperature": 0.7,
            "max_tokens": 300
        }
        
        response = requests.post(f"{BASE_URL}/api/deepseek/chat/continue", json=data)
        if response.status_code == 200:
            result = response.json()
            print("✓ 多轮对话成功")
            if 'choices' in result and len(result['choices']) > 0:
                content = result['choices'][0]['message']['content']
                print(f"AI回复: {content}")
            if 'updated_conversation_history' in result:
                print(f"更新后的对话历史长度: {len(result['updated_conversation_history'])}")
        else:
            print(f"✗ 多轮对话失败: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"✗ 请求失败: {str(e)}")

def test_chat_completion():
    """测试完整对话接口"""
    print("\n测试完整对话接口...")
    try:
        data = {
            "messages": [
                {"role": "user", "content": "请用一句话总结人工智能的发展趋势"}
            ],
            "model": "deepseek-chat",
            "temperature": 0.7,
            "max_tokens": 150
        }
        
        response = requests.post(f"{BASE_URL}/api/deepseek/chat", json=data)
        if response.status_code == 200:
            result = response.json()
            print("✓ 完整对话接口成功")
            if 'choices' in result and len(result['choices']) > 0:
                content = result['choices'][0]['message']['content']
                print(f"AI回复: {content}")
            if 'usage' in result:
                usage = result['usage']
                print(f"Token使用情况: {usage}")
        else:
            print(f"✗ 完整对话接口失败: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"✗ 请求失败: {str(e)}")

def main():
    """主测试函数"""
    print("开始测试DeepSeek模块...")
    print("=" * 50)
    
    # 检查服务器是否运行
    try:
        response = requests.get(f"{BASE_URL}/api/deepseek/models", timeout=5)
        if response.status_code != 200:
            print("✗ 服务器未运行或DeepSeek模块未正确加载")
            print("请确保:")
            print("1. 服务器正在运行 (python run.py)")
            print("2. DeepSeek模块已正确注册")
            return
    except Exception as e:
        print(f"✗ 无法连接到服务器: {str(e)}")
        print("请确保服务器正在运行: python run.py")
        return
    
    # 运行测试
    test_get_models()
    test_get_balance()
    test_single_chat()
    test_multi_round_chat()
    test_chat_completion()
    
    print("\n" + "=" * 50)
    print("测试完成!")

if __name__ == "__main__":
    main() 