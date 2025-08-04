import cv2
import numpy as np
import pytesseract
from PIL import Image
import re
import logging
from typing import Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class OCRService:
    """OCR识别服务类"""
    
    def __init__(self):
        """初始化OCR服务"""
        # 设置tesseract路径（Windows用户需要设置）
        # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        
        # 配置OCR参数
        self.config = '--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789.ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz年月日时分秒成交委托撤单担保品融资买入卖出已成部撤'
    
    def preprocess_image(self, image_path: str) -> np.ndarray:
        """
        预处理图片以提高OCR识别准确率
        :param image_path: 图片路径
        :return: 预处理后的图片
        """
        # 读取图片
        image = cv2.imread(image_path)
        if image is None:
            raise Exception(f"无法读取图片: {image_path}")
        
        # 转换为灰度图
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # 去噪
        denoised = cv2.medianBlur(gray, 3)
        
        # 二值化
        _, binary = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # 形态学操作，去除小噪点
        kernel = np.ones((2, 2), np.uint8)
        cleaned = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        
        return cleaned
    
    def extract_text_from_image(self, image_path: str) -> str:
        """
        从图片中提取文本
        :param image_path: 图片路径
        :return: 提取的文本
        """
        try:
            # 预处理图片
            processed_image = self.preprocess_image(image_path)
            
            # OCR识别
            text = pytesseract.image_to_string(processed_image, lang='chi_sim', config=self.config)
            
            logger.info(f"OCR识别完成，提取文本长度: {len(text)}")
            return text
            
        except Exception as e:
            logger.error(f"OCR识别失败: {str(e)}")
            raise Exception(f"OCR识别失败: {str(e)}")
    
    def parse_transaction_data(self, text: str) -> List[Dict]:
        """
        解析交易数据
        :param text: OCR识别的文本
        :return: 交易记录列表
        """
        transactions = []
        
        # 按行分割文本
        lines = text.split('\n')
        
        current_transaction = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # 尝试解析股票名称和时间
            stock_name, time_str = self._extract_stock_and_time(line)
            if stock_name and time_str:
                # 新交易记录开始
                if current_transaction:
                    transactions.append(current_transaction)
                
                current_transaction = {
                    'stock_name': stock_name,
                    'order_time': time_str,
                    'order_price': None,
                    'order_quantity': None,
                    'order_type': None,
                    'execution_price': None,
                    'execution_quantity': None,
                    'status': None
                }
                continue
            
            # 解析价格和数量
            if current_transaction:
                price, quantity, status = self._extract_price_quantity_status(line)
                if price and quantity:
                    if current_transaction['order_price'] is None:
                        # 第一行：委托信息
                        current_transaction['order_price'] = price
                        current_transaction['order_quantity'] = quantity
                        current_transaction['order_type'] = self._extract_order_type(line)
                    else:
                        # 第二行：成交信息
                        current_transaction['execution_price'] = price
                        current_transaction['execution_quantity'] = quantity
                        current_transaction['status'] = status
        
        # 添加最后一个交易记录
        if current_transaction:
            transactions.append(current_transaction)
        
        logger.info(f"解析完成，共识别 {len(transactions)} 条交易记录")
        return transactions
    
    def _extract_stock_and_time(self, line: str) -> tuple:
        """提取股票名称和时间"""
        # 匹配股票名称和时间模式
        # 例如：贝达药业 14:11:28
        pattern = r'^([^\d]+)\s+(\d{1,2}:\d{2}:\d{2})$'
        match = re.search(pattern, line)
        
        if match:
            stock_name = match.group(1).strip()
            time_str = match.group(2)
            return stock_name, time_str
        
        return None, None
    
    def _extract_price_quantity_status(self, line: str) -> tuple:
        """提取价格、数量和状态"""
        # 匹配价格、数量和状态模式
        # 例如：68.6800 5600 担保品买入
        pattern = r'(\d+\.\d+)\s+(\d+)\s+(.+)$'
        match = re.search(pattern, line)
        
        if match:
            price = float(match.group(1))
            quantity = int(match.group(2))
            status = match.group(3).strip()
            return price, quantity, status
        
        return None, None, None
    
    def _extract_order_type(self, line: str) -> str:
        """提取订单类型"""
        order_types = {
            '担保品买入': 'collateral_buy',
            '担保品卖出': 'collateral_sell',
            '融资买入': 'margin_buy',
            '融资卖出': 'margin_sell',
            '普通买入': 'normal_buy',
            '普通卖出': 'normal_sell'
        }
        
        for chinese_type, english_type in order_types.items():
            if chinese_type in line:
                return english_type
        
        return 'unknown'
    
    def validate_transaction(self, transaction: Dict) -> bool:
        """
        验证交易记录的有效性
        :param transaction: 交易记录
        :return: 是否有效
        """
        required_fields = ['stock_name', 'order_time', 'order_price', 'order_quantity']
        
        for field in required_fields:
            if not transaction.get(field):
                logger.warning(f"交易记录缺少必要字段: {field}")
                return False
        
        # 验证价格和数量
        if transaction['order_price'] <= 0 or transaction['order_quantity'] <= 0:
            logger.warning(f"价格或数量无效: {transaction}")
            return False
        
        return True
    
    def process_transaction_image(self, image_path: str) -> List[Dict]:
        """
        处理交易截图
        :param image_path: 图片路径
        :return: 有效的交易记录列表
        """
        try:
            # OCR识别
            text = self.extract_text_from_image(image_path)
            logger.info(f"OCR识别文本:\n{text}")
            
            # 解析交易数据
            transactions = self.parse_transaction_data(text)
            
            # 验证交易记录
            valid_transactions = []
            for transaction in transactions:
                if self.validate_transaction(transaction):
                    valid_transactions.append(transaction)
                else:
                    logger.warning(f"无效交易记录: {transaction}")
            
            logger.info(f"有效交易记录: {len(valid_transactions)} 条")
            return valid_transactions
            
        except Exception as e:
            logger.error(f"处理交易图片失败: {str(e)}")
            raise


# 创建全局服务实例
ocr_service = OCRService() 