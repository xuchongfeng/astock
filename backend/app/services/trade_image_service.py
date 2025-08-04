import os
import sys
import datetime
import logging
from typing import List, Dict, Optional
import re

# 添加路径以便导入其他模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import db
from app.models.user_trade import UserTrade
from app.models.stock_company import StockCompany
from app.services.ocr_service import ocr_service

logger = logging.getLogger(__name__)

def process_trade_image(image_path: str, user_id: int, trade_date: str = None) -> List[Dict]:
    """
    处理交易图片，识别并转换为交易记录
    :param image_path: 图片路径
    :param user_id: 用户ID
    :param trade_date: 交易日期，默认为今天
    :return: 交易记录列表
    """
    try:
        # 验证图片文件
        if not os.path.exists(image_path):
            raise Exception(f"图片文件不存在: {image_path}")
        
        # 设置交易日期
        if not trade_date:
            trade_date = datetime.datetime.now().strftime('%Y-%m-%d')
        
        # OCR识别
        transactions = ocr_service.process_transaction_image(image_path)
        
        # 转换为user_trade记录
        trade_records = []
        for transaction in transactions:
            trade_record = _convert_to_user_trade(transaction, user_id, trade_date, image_path)
            if trade_record:
                trade_records.append(trade_record)
        
        logger.info(f"成功识别 {len(trade_records)} 条交易记录")
        return trade_records
        
    except Exception as e:
        logger.error(f"处理交易图片失败: {str(e)}")
        raise

def _convert_to_user_trade(transaction: Dict, user_id: int, trade_date: str, image_path: str) -> Optional[Dict]:
    """
    将OCR识别的交易数据转换为user_trade记录
    :param transaction: OCR识别的交易数据
    :param user_id: 用户ID
    :param trade_date: 交易日期
    :param image_path: 图片路径
    :return: user_trade记录
    """
    try:
        # 获取股票代码
        stock_code = _get_stock_code_by_name(transaction['stock_name'])
        if not stock_code:
            logger.warning(f"未找到股票代码: {transaction['stock_name']}")
            return None
        
        # 确定交易类型
        trade_type = _determine_trade_type(transaction['order_type'])
        if not trade_type:
            logger.warning(f"无法确定交易类型: {transaction['order_type']}")
            return None
        
        # 计算交易金额
        trade_amount = transaction['order_price'] * transaction['order_quantity']
        
        # 构建user_trade记录
        trade_record = {
            'user_id': user_id,
            'ts_code': stock_code,
            'trade_type': trade_type,
            'quantity': transaction['order_quantity'],
            'price': transaction['order_price'],
            'trade_date': datetime.datetime.strptime(trade_date, '%Y-%m-%d').date(),
            'profit_loss': None,  # 需要后续计算
            'note': f"OCR识别 - {transaction['stock_name']} {transaction['order_type']} {transaction['status'] or '未知状态'}",
            'created_at': datetime.datetime.now(),
            'updated_at': datetime.datetime.now()
        }
        
        # 如果有成交价格，使用成交价格
        if transaction.get('execution_price'):
            trade_record['price'] = transaction['execution_price']
            trade_record['quantity'] = transaction.get('execution_quantity', transaction['order_quantity'])
            trade_record['note'] += f" 成交价:{transaction['execution_price']}"
        
        return trade_record
        
    except Exception as e:
        logger.error(f"转换交易记录失败: {str(e)}")
        return None

def _get_stock_code_by_name(stock_name: str) -> Optional[str]:
    """
    根据股票名称获取股票代码
    :param stock_name: 股票名称
    :return: 股票代码
    """
    # 精确匹配
    stock = StockCompany.query.filter(StockCompany.name == stock_name).first()
    if stock:
        return stock.ts_code
    
    # 模糊匹配
    stock = StockCompany.query.filter(StockCompany.name.like(f'%{stock_name}%')).first()
    if stock:
        return stock.ts_code
    
    # 如果还是找不到，尝试从常见股票名称映射
    stock_name_mapping = {
        '贝达药业': '300558.SZ',
        '汉威科技': '300007.SZ',
        '硕贝德': '300322.SZ',
        '深信服': '300454.SZ',
        '天孚通信': '300394.SZ',
        # 可以继续添加更多映射
    }
    
    return stock_name_mapping.get(stock_name)

def _determine_trade_type(order_type: str) -> Optional[str]:
    """
    根据订单类型确定交易类型
    :param order_type: 订单类型
    :return: 交易类型 (buy/sell)
    """
    buy_types = ['collateral_buy', 'margin_buy', 'normal_buy']
    sell_types = ['collateral_sell', 'margin_sell', 'normal_sell']
    
    if order_type in buy_types:
        return 'buy'
    elif order_type in sell_types:
        return 'sell'
    else:
        return None

def save_trade_records(trade_records: List[Dict]) -> List[Dict]:
    """
    保存交易记录到数据库
    :param trade_records: 交易记录列表
    :return: 保存成功的记录列表
    """
    saved_records = []
    
    for trade_record in trade_records:
        try:
            # 检查是否已存在相同记录
            existing_record = UserTrade.query.filter(
                UserTrade.user_id == trade_record['user_id'],
                UserTrade.ts_code == trade_record['ts_code'],
                UserTrade.trade_date == trade_record['trade_date'],
                UserTrade.price == trade_record['price'],
                UserTrade.quantity == trade_record['quantity'],
                UserTrade.trade_type == trade_record['trade_type']
            ).first()
            
            if existing_record:
                logger.info(f"交易记录已存在，跳过: {trade_record}")
                continue
            
            # 创建新记录
            new_trade = UserTrade(**trade_record)
            db.session.add(new_trade)
            db.session.commit()
            
            saved_records.append(new_trade.as_dict())
            logger.info(f"成功保存交易记录: {new_trade.id}")
            
        except Exception as e:
            logger.error(f"保存交易记录失败: {str(e)}")
            db.session.rollback()
            continue
    
    logger.info(f"成功保存 {len(saved_records)} 条交易记录")
    return saved_records

def process_and_save_trade_image(image_path: str, user_id: int, trade_date: str = None) -> Dict:
    """
    处理交易图片并保存到数据库
    :param image_path: 图片路径
    :param user_id: 用户ID
    :param trade_date: 交易日期
    :return: 处理结果
    """
    try:
        # 处理图片
        trade_records = process_trade_image(image_path, user_id, trade_date)
        
        # 保存到数据库
        saved_records = save_trade_records(trade_records)
        
        return {
            'success': True,
            'total_recognized': len(trade_records),
            'total_saved': len(saved_records),
            'saved_records': saved_records,
            'image_path': image_path
        }
        
    except Exception as e:
        logger.error(f"处理并保存交易图片失败: {str(e)}")
        return {
            'success': False,
            'error': str(e),
            'image_path': image_path
        }

def batch_process_images(image_folder: str, user_id: int, trade_date: str = None) -> List[Dict]:
    """
    批量处理图片文件夹
    :param image_folder: 图片文件夹路径
    :param user_id: 用户ID
    :param trade_date: 交易日期
    :return: 处理结果列表
    """
    results = []
    
    # 支持的图片格式
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
    
    try:
        # 遍历文件夹
        for filename in os.listdir(image_folder):
            if any(filename.lower().endswith(ext) for ext in image_extensions):
                image_path = os.path.join(image_folder, filename)
                
                logger.info(f"处理图片: {filename}")
                result = process_and_save_trade_image(image_path, user_id, trade_date)
                result['filename'] = filename
                results.append(result)
        
        logger.info(f"批量处理完成，共处理 {len(results)} 张图片")
        return results
        
    except Exception as e:
        logger.error(f"批量处理图片失败: {str(e)}")
        return [{'success': False, 'error': str(e)}] 