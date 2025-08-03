#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
标签初始化脚本
用于初始化一些常用的股票标签
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app.services import tag_service


def init_default_tags():
    """初始化默认标签"""
    
    # 走势标签
    trend_tags = [
        {
            'name': '强势上涨',
            'description': '股票处于强势上涨趋势',
            'color': '#f5222d',
            'category': 'trend'
        },
        {
            'name': '温和上涨',
            'description': '股票处于温和上涨趋势',
            'color': '#fa8c16',
            'category': 'trend'
        },
        {
            'name': '横盘整理',
            'description': '股票处于横盘整理状态',
            'color': '#52c41a',
            'category': 'trend'
        },
        {
            'name': '温和下跌',
            'description': '股票处于温和下跌趋势',
            'color': '#1890ff',
            'category': 'trend'
        },
        {
            'name': '强势下跌',
            'description': '股票处于强势下跌趋势',
            'color': '#722ed1',
            'category': 'trend'
        },
        {
            'name': '突破',
            'description': '股票突破重要阻力位',
            'color': '#eb2f96',
            'category': 'trend'
        },
        {
            'name': '回调',
            'description': '股票出现回调',
            'color': '#faad14',
            'category': 'trend'
        }
    ]
    
    # 状态标签
    status_tags = [
        {
            'name': '关注',
            'description': '需要关注的股票',
            'color': '#1890ff',
            'category': 'status'
        },
        {
            'name': '买入',
            'description': '建议买入的股票',
            'color': '#52c41a',
            'category': 'status'
        },
        {
            'name': '卖出',
            'description': '建议卖出的股票',
            'color': '#f5222d',
            'category': 'status'
        },
        {
            'name': '持有',
            'description': '建议持有的股票',
            'color': '#fa8c16',
            'category': 'status'
        },
        {
            'name': '观望',
            'description': '建议观望的股票',
            'color': '#722ed1',
            'category': 'status'
        },
        {
            'name': '停牌',
            'description': '股票停牌',
            'color': '#8c8c8c',
            'category': 'status'
        },
        {
            'name': '退市风险',
            'description': '存在退市风险的股票',
            'color': '#ff4d4f',
            'category': 'status'
        }
    ]
    
    # 自定义标签
    custom_tags = [
        {
            'name': '龙头股',
            'description': '行业龙头股票',
            'color': '#52c41a',
            'category': 'custom'
        },
        {
            'name': '绩优股',
            'description': '业绩优秀的股票',
            'color': '#1890ff',
            'category': 'custom'
        },
        {
            'name': '成长股',
            'description': '具有成长性的股票',
            'color': '#fa8c16',
            'category': 'custom'
        },
        {
            'name': '价值股',
            'description': '具有投资价值的股票',
            'color': '#722ed1',
            'category': 'custom'
        },
        {
            'name': '概念股',
            'description': '热门概念股票',
            'color': '#eb2f96',
            'category': 'custom'
        },
        {
            'name': 'ST股',
            'description': 'ST股票',
            'color': '#ff4d4f',
            'category': 'custom'
        },
        {
            'name': '新股',
            'description': '新上市的股票',
            'color': '#13c2c2',
            'category': 'custom'
        }
    ]
    
    all_tags = trend_tags + status_tags + custom_tags
    
    created_count = 0
    skipped_count = 0
    
    for tag_data in all_tags:
        try:
            # 检查标签是否已存在
            existing_tag = tag_service.get_tag_by_name(tag_data['name'])
            if existing_tag:
                print(f"标签 '{tag_data['name']}' 已存在，跳过")
                skipped_count += 1
                continue
            
            # 创建标签
            tag = tag_service.create_tag(**tag_data)
            print(f"创建标签: {tag.name} ({tag.category})")
            created_count += 1
            
        except Exception as e:
            print(f"创建标签 '{tag_data['name']}' 失败: {str(e)}")
    
    print(f"\n初始化完成:")
    print(f"创建标签: {created_count} 个")
    print(f"跳过标签: {skipped_count} 个")


def main():
    """主函数"""
    print("开始初始化标签...")
    init_default_tags()
    print("标签初始化完成!")


if __name__ == '__main__':
    main() 