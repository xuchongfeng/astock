#!/usr/bin/env python3
"""
交易图片识别测试脚本
"""

import requests
import json
import os
import sys

# 服务器地址
BASE_URL = "http://localhost:5000"

def test_upload_image():
    """测试上传图片功能"""
    print("测试上传图片功能...")
    
    # 图片文件路径（需要替换为实际的图片路径）
    image_path = "test_trade_image.jpg"
    
    if not os.path.exists(image_path):
        print(f"图片文件不存在: {image_path}")
        return
    
    try:
        with open(image_path, 'rb') as f:
            files = {'file': f}
            data = {
                'user_id': 1,
                'trade_date': '2024-01-15'
            }
            
            response = requests.post(f"{BASE_URL}/api/trade_image/upload", 
                                  files=files, data=data)
            
            if response.status_code == 200:
                result = response.json()
                print("✓ 上传成功")
                print(f"识别记录数: {result.get('total_recognized', 0)}")
                print(f"保存记录数: {result.get('total_saved', 0)}")
                print(f"保存的记录: {json.dumps(result.get('saved_records', []), ensure_ascii=False, indent=2)}")
            else:
                print(f"✗ 上传失败: {response.status_code}")
                print(response.text)
                
    except Exception as e:
        print(f"✗ 测试失败: {str(e)}")

def test_process_existing_image():
    """测试处理已存在的图片"""
    print("\n测试处理已存在的图片...")
    
    # 图片文件路径
    image_path = "test_trade_image.jpg"
    
    if not os.path.exists(image_path):
        print(f"图片文件不存在: {image_path}")
        return
    
    try:
        data = {
            'image_path': os.path.abspath(image_path),
            'user_id': 1,
            'trade_date': '2024-01-15'
        }
        
        response = requests.post(f"{BASE_URL}/api/trade_image/process", 
                              json=data)
        
        if response.status_code == 200:
            result = response.json()
            print("✓ 处理成功")
            print(f"识别记录数: {result.get('total_recognized', 0)}")
            print(f"保存记录数: {result.get('total_saved', 0)}")
        else:
            print(f"✗ 处理失败: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"✗ 测试失败: {str(e)}")

def test_preview_recognition():
    """测试预览识别功能"""
    print("\n测试预览识别功能...")
    
    # 图片文件路径
    image_path = "test_trade_image.jpg"
    
    if not os.path.exists(image_path):
        print(f"图片文件不存在: {image_path}")
        return
    
    try:
        data = {
            'image_path': os.path.abspath(image_path),
            'user_id': 1,
            'trade_date': '2024-01-15'
        }
        
        response = requests.post(f"{BASE_URL}/api/trade_image/preview", 
                              json=data)
        
        if response.status_code == 200:
            result = response.json()
            print("✓ 预览成功")
            print(f"识别记录数: {result.get('total_recognized', 0)}")
            print(f"识别结果: {json.dumps(result.get('trade_records', []), ensure_ascii=False, indent=2)}")
        else:
            print(f"✗ 预览失败: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"✗ 测试失败: {str(e)}")

def test_ocr_function():
    """测试OCR功能"""
    print("\n测试OCR功能...")
    
    # 图片文件路径
    image_path = "test_trade_image.jpg"
    
    if not os.path.exists(image_path):
        print(f"图片文件不存在: {image_path}")
        return
    
    try:
        data = {
            'image_path': os.path.abspath(image_path)
        }
        
        response = requests.post(f"{BASE_URL}/api/trade_image/test_ocr", 
                              json=data)
        
        if response.status_code == 200:
            result = response.json()
            print("✓ OCR测试成功")
            print(f"提取的文本:\n{result.get('extracted_text', '')}")
            print(f"解析的交易记录: {json.dumps(result.get('parsed_transactions', []), ensure_ascii=False, indent=2)}")
        else:
            print(f"✗ OCR测试失败: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"✗ 测试失败: {str(e)}")

def test_supported_formats():
    """测试获取支持的格式"""
    print("\n测试获取支持的格式...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/trade_image/supported_formats")
        
        if response.status_code == 200:
            result = response.json()
            print("✓ 获取成功")
            print(f"支持的格式: {result.get('supported_formats', [])}")
            print(f"上传文件夹: {result.get('upload_folder', '')}")
        else:
            print(f"✗ 获取失败: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"✗ 测试失败: {str(e)}")

def main():
    """主测试函数"""
    print("交易图片识别功能测试")
    print("=" * 50)
    
    # 检查服务器是否运行
    try:
        response = requests.get(f"{BASE_URL}/api/trade_image/supported_formats", timeout=5)
        if response.status_code != 200:
            print("✗ 服务器未运行或模块未正确加载")
            print("请确保服务器正在运行: python run.py")
            return
    except Exception as e:
        print(f"✗ 无法连接到服务器: {str(e)}")
        print("请确保服务器正在运行: python run.py")
        return
    
    # 运行测试
    test_supported_formats()
    test_ocr_function()
    test_preview_recognition()
    test_process_existing_image()
    test_upload_image()
    
    print("\n" + "=" * 50)
    print("测试完成!")

if __name__ == "__main__":
    main() 