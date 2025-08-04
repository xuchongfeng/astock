from app import db
import datetime

class UserTradeRecord(db.Model):
    __tablename__ = 'user_trade_record'

    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False, index=True, comment='用户ID')
    stock_code = db.Column(db.String(16), nullable=False, index=True, comment='股票代码')
    stock_name = db.Column(db.String(64), nullable=False, comment='股票名称')
    trade_date = db.Column(db.Date, nullable=False, index=True, comment='交易日期')
    order_time = db.Column(db.Time, nullable=False, comment='委托时间')
    order_price = db.Column(db.Numeric(12, 4), nullable=False, comment='委托价格')
    order_quantity = db.Column(db.Integer, nullable=False, comment='委托数量')
    order_type = db.Column(db.String(32), nullable=False, comment='委托类型：collateral_buy/collateral_sell/margin_buy/margin_sell/normal_buy/normal_sell')
    execution_price = db.Column(db.Numeric(12, 4), nullable=True, comment='成交价格')
    execution_quantity = db.Column(db.Integer, nullable=True, comment='成交数量')
    status = db.Column(db.String(32), nullable=True, comment='交易状态：已成/部撤/撤单')
    trade_amount = db.Column(db.Numeric(20, 4), nullable=True, comment='交易金额')
    commission = db.Column(db.Numeric(12, 4), nullable=True, comment='手续费')
    stamp_duty = db.Column(db.Numeric(12, 4), nullable=True, comment='印花税')
    transfer_fee = db.Column(db.Numeric(12, 4), nullable=True, comment='过户费')
    total_fee = db.Column(db.Numeric(12, 4), nullable=True, comment='总费用')
    source = db.Column(db.String(32), nullable=False, default='ocr', comment='数据来源：ocr/manual/api')
    image_path = db.Column(db.String(255), nullable=True, comment='原始图片路径')
    ocr_text = db.Column(db.Text, nullable=True, comment='OCR识别文本')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now, comment='创建时间')
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment='更新时间')

    __table_args__ = (
        db.Index('idx_user_date', 'user_id', 'trade_date'),
        db.Index('idx_stock_date', 'stock_code', 'trade_date'),
        db.Index('idx_order_time', 'order_time'),
    )

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns} 