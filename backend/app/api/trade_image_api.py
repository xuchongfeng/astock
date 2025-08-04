from flask import Blueprint, request, jsonify
import logging
import os
from werkzeug.utils import secure_filename
import datetime
from app.services.trade_image_service import (
    process_and_save_trade_image, 
    process_trade_image, 
    batch_process_images
)
from app.services.ocr_service import ocr_service

bp = Blueprint('trade_image', __name__, url_prefix='/api/trade_image')

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 配置上传文件夹
UPLOAD_FOLDER = 'uploads/trade_images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff'}

# 确保上传文件夹存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """检查文件扩展名是否允许"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/upload', methods=['POST'])
def upload_and_process():
    """
    上传并处理交易图片
    POST /api/trade_image/upload
    Content-Type: multipart/form-data
    """
    try:
        # 检查是否有文件
        if 'file' not in request.files:
            return jsonify({'error': '没有上传文件'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': '没有选择文件'}), 400
        
        # 检查文件类型
        if not allowed_file(file.filename):
            return jsonify({'error': '不支持的文件类型'}), 400
        
        # 获取参数
        user_id = request.form.get('user_id', type=int)
        trade_date = request.form.get('trade_date')
        
        if not user_id:
            return jsonify({'error': '缺少user_id参数'}), 400
        
        # 保存文件
        filename = secure_filename(file.filename)
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        
        logger.info(f"文件已保存: {file_path}")
        
        # 处理图片
        result = process_and_save_trade_image(file_path, user_id, trade_date)
        
        result['filename'] = filename
        result['file_path'] = file_path
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"上传处理失败: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/process', methods=['POST'])
def process_existing_image():
    """
    处理已存在的图片文件
    POST /api/trade_image/process
    {
        "image_path": "/path/to/image.jpg",
        "user_id": 1,
        "trade_date": "2024-01-15"
    }
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': '缺少请求数据'}), 400
        
        image_path = data.get('image_path')
        user_id = data.get('user_id')
        trade_date = data.get('trade_date')
        
        if not image_path or not user_id:
            return jsonify({'error': '缺少必要参数'}), 400
        
        # 处理图片
        result = process_and_save_trade_image(image_path, user_id, trade_date)
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"处理图片失败: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/batch_process', methods=['POST'])
def batch_process_images_api():
    """
    批量处理图片文件夹
    POST /api/trade_image/batch_process
    {
        "image_folder": "/path/to/images",
        "user_id": 1,
        "trade_date": "2024-01-15"
    }
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': '缺少请求数据'}), 400
        
        image_folder = data.get('image_folder')
        user_id = data.get('user_id')
        trade_date = data.get('trade_date')
        
        if not image_folder or not user_id:
            return jsonify({'error': '缺少必要参数'}), 400
        
        # 批量处理
        results = batch_process_images(image_folder, user_id, trade_date)
        
        # 统计结果
        total_images = len(results)
        success_count = sum(1 for r in results if r.get('success'))
        total_recognized = sum(r.get('total_recognized', 0) for r in results)
        total_saved = sum(r.get('total_saved', 0) for r in results)
        
        return jsonify({
            'success': True,
            'total_images': total_images,
            'success_count': success_count,
            'total_recognized': total_recognized,
            'total_saved': total_saved,
            'results': results
        })
        
    except Exception as e:
        logger.error(f"批量处理失败: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/preview', methods=['POST'])
def preview_recognition():
    """
    预览OCR识别结果，不保存到数据库
    POST /api/trade_image/preview
    {
        "image_path": "/path/to/image.jpg",
        "user_id": 1,
        "trade_date": "2024-01-15"
    }
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': '缺少请求数据'}), 400
        
        image_path = data.get('image_path')
        user_id = data.get('user_id')
        trade_date = data.get('trade_date')
        
        if not image_path or not user_id:
            return jsonify({'error': '缺少必要参数'}), 400
        
        # 只处理图片，不保存
        trade_records = process_trade_image(image_path, user_id, trade_date)
        
        return jsonify({
            'success': True,
            'total_recognized': len(trade_records),
            'trade_records': trade_records,
            'image_path': image_path
        })
        
    except Exception as e:
        logger.error(f"预览识别失败: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/supported_formats', methods=['GET'])
def get_supported_formats():
    """
    获取支持的图片格式
    GET /api/trade_image/supported_formats
    """
    return jsonify({
        'supported_formats': list(ALLOWED_EXTENSIONS),
        'upload_folder': UPLOAD_FOLDER
    })

@bp.route('/test_ocr', methods=['POST'])
def test_ocr():
    """
    测试OCR识别功能
    POST /api/trade_image/test_ocr
    {
        "image_path": "/path/to/image.jpg"
    }
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': '缺少请求数据'}), 400
        
        image_path = data.get('image_path')
        if not image_path:
            return jsonify({'error': '缺少image_path参数'}), 400
        
        # 测试OCR识别
        # 提取文本
        text = ocr_service.extract_text_from_image(image_path)
        
        # 解析交易数据
        transactions = ocr_service.parse_transaction_data(text)
        
        return jsonify({
            'success': True,
            'extracted_text': text,
            'parsed_transactions': transactions,
            'total_transactions': len(transactions)
        })
        
    except Exception as e:
        logger.error(f"OCR测试失败: {str(e)}")
        return jsonify({'error': str(e)}), 500 