from flask import Blueprint, request, jsonify
from app.services.user_trade_service import (
    get_all_trades, get_trade_by_id, create_trade, update_trade, delete_trade,
    get_latest_buy_trade, calculate_profit_loss
)
from app.services.user_position_service import update_position_after_trade
from app.services.trade_image_service import process_and_save_trade_image
from app.models.stock_company import StockCompany
from app.models.user_trade import UserTrade
import os
from werkzeug.utils import secure_filename
import datetime

bp = Blueprint('user_trade', __name__, url_prefix='/api/user_trade')

# 配置上传文件夹
UPLOAD_FOLDER = 'uploads/trade_images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff'}

# 确保上传文件夹存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """检查文件扩展名是否允许"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/<int:user_id>', methods=['GET'])
def list_trades(user_id):
    filters = {'user_id': user_id}
    for key in ['ts_code', 'trade_type', 'trade_date']:
        value = request.args.get(key)
        if value:
            filters[key] = value
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 20))
    query = get_all_trades(filters, query_only=True)
    # 默认按照创建时间倒序排列
    query = query.order_by(UserTrade.created_at.desc())
    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    result = []
    for i in items:
        d = i.as_dict()
        company = StockCompany.query.filter_by(ts_code=i.ts_code).first()
        d['stock_info'] = company.as_dict() if company else None
        result.append(d)
    return jsonify({'data': result, 'total': total})

@bp.route('/<int:user_id>/<int:trade_id>', methods=['GET'])
def get_trade(user_id, trade_id):
    trade = get_trade_by_id(trade_id)
    if not trade or trade.user_id != user_id:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(trade.as_dict())

@bp.route('/<int:user_id>', methods=['POST'])
def add_trade(user_id):
    data = request.json
    data['user_id'] = user_id
    
    ts_code = data.get('ts_code')
    trade_type = data.get('trade_type')
    quantity = int(data.get('quantity', 0))
    price = float(data.get('price', 0))
    
    # 验证必要参数
    if not ts_code or not trade_type or quantity <= 0 or price <= 0:
        return jsonify({'error': '缺少必要参数或参数无效'}), 400
    
    try:
        # 如果是卖出交易，自动计算盈利
        if trade_type == 'sell':
            sell_price = price
            sell_quantity = quantity
            
            # 获取最近的买入记录
            latest_buy = get_latest_buy_trade(user_id, ts_code)
            
            if latest_buy:
                buy_price = float(latest_buy.price)
                buy_quantity = int(latest_buy.quantity)
                
                # 计算盈利/亏损
                profit_loss = calculate_profit_loss(sell_price, sell_quantity, buy_price, buy_quantity)
                data['profit_loss'] = profit_loss
        
        # 创建交易记录
        trade = create_trade(data)
        
        # 更新持仓
        update_position_after_trade(user_id, ts_code, trade_type, quantity, price)
        
        return jsonify(trade.as_dict()), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'交易失败: {str(e)}'}), 500

@bp.route('/<int:user_id>/upload_image', methods=['POST'])
def upload_trade_image(user_id):
    """
    上传交易图片并解析记录
    POST /api/user_trade/<user_id>/upload_image
    Content-Type: multipart/form-data
    """
    try:
        # 检查是否有文件
        if 'images[0]' not in request.files:
            return jsonify({'error': '没有上传文件'}), 400
        
        file = request.files['images[0]']
        if file.filename == '':
            return jsonify({'error': '没有选择文件'}), 400
        
        # 检查文件类型
        if not allowed_file(file.filename):
            return jsonify({'error': '不支持的文件类型'}), 400
        
        # 获取交易日期参数
        trade_date = request.form.get('trade_date')
        if not trade_date:
            trade_date = datetime.datetime.now().strftime('%Y-%m-%d')
        
        # 保存文件
        filename = secure_filename(file.filename)
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        
        # 处理图片并保存交易记录
        result = process_and_save_trade_image(file_path, user_id, trade_date)
        
        if result['success']:
            return jsonify({
                'success': True,
                'message': f'成功识别并保存 {result["total_saved"]} 条交易记录',
                'total_recognized': result['total_recognized'],
                'total_saved': result['total_saved'],
                'saved_records': result['saved_records'],
                'filename': filename
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': result['error']
            }), 500
        
    except Exception as e:
        return jsonify({'error': f'上传处理失败: {str(e)}'}), 500

@bp.route('/<int:user_id>/parse_image', methods=['POST'])
def parse_trade_image(user_id):
    """
    解析已存在的交易图片
    POST /api/user_trade/<user_id>/parse_image
    {
        "image_path": "/path/to/image.jpg",
        "trade_date": "2024-01-15"
    }
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': '缺少请求数据'}), 400
        
        image_path = data.get('image_path')
        trade_date = data.get('trade_date')
        
        if not image_path:
            return jsonify({'error': '缺少image_path参数'}), 400
        
        if not trade_date:
            trade_date = datetime.datetime.now().strftime('%Y-%m-%d')
        
        # 处理图片并保存交易记录
        result = process_and_save_trade_image(image_path, user_id, trade_date)
        
        if result['success']:
            return jsonify({
                'success': True,
                'message': f'成功识别并保存 {result["total_saved"]} 条交易记录',
                'total_recognized': result['total_recognized'],
                'total_saved': result['total_saved'],
                'saved_records': result['saved_records']
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': result['error']
            }), 500
        
    except Exception as e:
        return jsonify({'error': f'解析图片失败: {str(e)}'}), 500

@bp.route('/<int:user_id>/<int:trade_id>', methods=['PUT'])
def edit_trade(user_id, trade_id):
    trade = get_trade_by_id(trade_id)
    if not trade or trade.user_id != user_id:
        return jsonify({'error': 'Not found'}), 404
    data = request.json
    trade = update_trade(trade_id, data)
    if not trade:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(trade.as_dict())

@bp.route('/<int:user_id>/<int:trade_id>', methods=['DELETE'])
def remove_trade(user_id, trade_id):
    trade = get_trade_by_id(trade_id)
    if not trade or trade.user_id != user_id:
        return jsonify({'error': 'Not found'}), 404
    success = delete_trade(trade_id)
    if not success:
        return jsonify({'error': 'Not found'}), 404
    return jsonify({'result': 'success'}) 