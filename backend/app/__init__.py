
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from .config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*", "allow_headers": "*"}})

    from app.api.stock_company_api import bp as stock_company_bp
    app.register_blueprint(stock_company_bp)

    from app.api.stock_daily_api import bp as stock_daily_bp
    app.register_blueprint(stock_daily_bp)

    from app.api.stock_daily_basic_api import bp as stock_daily_basic_bp
    app.register_blueprint(stock_daily_basic_bp)

    from app.api.index_daily_basic_api import bp as index_daily_basic_bp
    app.register_blueprint(index_daily_basic_bp)

    from app.api.trade_calendar_api import bp as trade_calendar_bp
    app.register_blueprint(trade_calendar_bp)

    from app.api.stock_minute_api import bp as stock_minute_bp
    app.register_blueprint(stock_minute_bp)

    from app.api.industry_api import bp as industry_bp
    app.register_blueprint(industry_bp)

    from app.api.industry_stats_api import bp as industry_stats_bp
    app.register_blueprint(industry_stats_bp)

    from app.api.user_api import bp as user_bp
    app.register_blueprint(user_bp)

    from app.api.user_stock_api import bp as user_stock_bp
    app.register_blueprint(user_stock_bp)

    from app.api.ths_hot_api import bp as ths_hot_bp
    app.register_blueprint(ths_hot_bp)

    from app.api.stock_note_api import bp as stock_note_bp
    app.register_blueprint(stock_note_bp)

    from app.api.ths_index_daily_api import bp as ths_index_daily_bp
    app.register_blueprint(ths_index_daily_bp)

    from app.api.ths_index_api import bp as ths_index_bp
    app.register_blueprint(ths_index_bp)

    from app.api.ths_member_api import bp as ths_member_bp
    app.register_blueprint(ths_member_bp)

    from app.api.strategy_api import bp as strategy_bp
    app.register_blueprint(strategy_bp)
    from app.api.strategy_stock_api import bp as strategy_stock_bp
    app.register_blueprint(strategy_stock_bp)

    from app.api.user_position_api import bp as user_position_bp
    app.register_blueprint(user_position_bp)

    from app.api.user_trade_api import bp as user_trade_bp
    app.register_blueprint(user_trade_bp)

    from app.api.concept_api import bp as concept_bp
    app.register_blueprint(concept_bp)

    from app.api.xueqiu_api import bp as xueqiu_bp
    app.register_blueprint(xueqiu_bp)

    from app.api.tag_api import tag_bp
    app.register_blueprint(tag_bp)

    from app.api.deepseek_api import bp as deepseek_bp
    app.register_blueprint(deepseek_bp)

    from app.api.deepseek_analysis_api import bp as deepseek_analysis_bp
    app.register_blueprint(deepseek_analysis_bp)

    from app.api.trade_image_api import bp as trade_image_bp
    app.register_blueprint(trade_image_bp)

    from app.api.dc_hot_api import dc_hot_bp
    app.register_blueprint(dc_hot_bp)

    return app