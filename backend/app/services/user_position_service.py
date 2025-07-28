from app.models.user_position import UserPosition
from app import db

def get_all_positions(filters=None, query_only=False):
    query = UserPosition.query
    if filters:
        for attr, value in filters.items():
            query = query.filter(getattr(UserPosition, attr) == value)
    if query_only:
        return query
    return query.all()

def get_position_by_id(position_id):
    return UserPosition.query.get(position_id)

def create_position(data):
    position = UserPosition(**data)
    db.session.add(position)
    db.session.commit()
    return position

def update_position(position_id, data):
    position = UserPosition.query.get(position_id)
    if not position:
        return None
    for key, value in data.items():
        setattr(position, key, value)
    db.session.commit()
    return position

def delete_position(position_id):
    position = UserPosition.query.get(position_id)
    if not position:
        return False
    db.session.delete(position)
    db.session.commit()
    return True

def get_position_by_user_and_stock(user_id, ts_code):
    """获取指定用户和股票的持仓记录"""
    return UserPosition.query.filter_by(user_id=user_id, ts_code=ts_code).first()

def update_position_after_trade(user_id, ts_code, trade_type, quantity, price):
    """根据交易更新持仓"""
    position = get_position_by_user_and_stock(user_id, ts_code)
    
    if trade_type == 'buy':
        # 买入：增加持仓
        if position:
            # 更新现有持仓
            new_quantity = position.quantity + quantity
            # 转换为float进行计算
            current_avg_price = float(position.avg_price) if position.avg_price else 0
            new_total_cost = (position.quantity * current_avg_price) + (quantity * price)
            new_avg_price = new_total_cost / new_quantity
            
            position.quantity = new_quantity
            position.avg_price = new_avg_price
        else:
            # 创建新持仓
            position = UserPosition(
                user_id=user_id,
                ts_code=ts_code,
                quantity=quantity,
                avg_price=price
            )
            db.session.add(position)
    
    elif trade_type == 'sell':
        # 卖出：减少持仓
        if position:
            if position.quantity >= quantity:
                # 更新持仓
                position.quantity -= quantity
                # 如果持仓为0，删除持仓记录
                if position.quantity == 0:
                    db.session.delete(position)
            else:
                # 卖出数量超过持仓，抛出异常
                raise ValueError(f"卖出数量 {quantity} 超过持仓数量 {position.quantity}")
        else:
            # 没有持仓记录，抛出异常
            raise ValueError(f"用户 {user_id} 没有股票 {ts_code} 的持仓记录")
    
    db.session.commit()
    return position 