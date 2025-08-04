from app import db
from app.models.stock_daily_basic import StockDailyBasic
from typing import List, Dict, Optional
import datetime


class StockDailyBasicService:
    """股票每日指标服务类"""
    
    @staticmethod
    def get_by_ts_code(ts_code: str, start_date: Optional[str] = None, end_date: Optional[str] = None) -> List[Dict]:
        """
        根据股票代码获取每日指标数据
        :param ts_code: 股票代码
        :param start_date: 开始日期 (YYYY-MM-DD)
        :param end_date: 结束日期 (YYYY-MM-DD)
        :return: 每日指标数据列表
        """
        query = StockDailyBasic.query.filter(StockDailyBasic.ts_code == ts_code)
        
        if start_date:
            query = query.filter(StockDailyBasic.trade_date >= start_date)
        if end_date:
            query = query.filter(StockDailyBasic.trade_date <= end_date)
            
        query = query.order_by(StockDailyBasic.trade_date.desc())
        
        results = query.all()
        return [item.as_dict() for item in results]
    
    @staticmethod
    def get_by_trade_date(trade_date: str) -> List[Dict]:
        """
        根据交易日期获取所有股票的每日指标数据
        :param trade_date: 交易日期 (YYYY-MM-DD)
        :return: 每日指标数据列表
        """
        results = StockDailyBasic.query.filter(
            StockDailyBasic.trade_date == trade_date
        ).all()
        
        return [item.as_dict() for item in results]
    
    @staticmethod
    def get_latest_by_ts_code(ts_code: str) -> Optional[Dict]:
        """
        获取指定股票的最新每日指标数据
        :param ts_code: 股票代码
        :return: 最新每日指标数据
        """
        result = StockDailyBasic.query.filter(
            StockDailyBasic.ts_code == ts_code
        ).order_by(StockDailyBasic.trade_date.desc()).first()
        
        return result.as_dict() if result else None
    
    @staticmethod
    def get_by_pe_range(min_pe: float, max_pe: float, trade_date: str = None) -> List[Dict]:
        """
        根据市盈率范围获取股票数据
        :param min_pe: 最小市盈率
        :param max_pe: 最大市盈率
        :param trade_date: 交易日期，默认为最新日期
        :return: 符合条件的股票列表
        """
        query = StockDailyBasic.query.filter(
            StockDailyBasic.pe >= min_pe,
            StockDailyBasic.pe <= max_pe,
            StockDailyBasic.pe.isnot(None)
        )
        
        if trade_date:
            query = query.filter(StockDailyBasic.trade_date == trade_date)
        else:
            # 获取最新交易日期
            latest_date = db.session.query(db.func.max(StockDailyBasic.trade_date)).scalar()
            if latest_date:
                query = query.filter(StockDailyBasic.trade_date == latest_date)
        
        results = query.all()
        return [item.as_dict() for item in results]
    
    @staticmethod
    def get_by_pb_range(min_pb: float, max_pb: float, trade_date: str = None) -> List[Dict]:
        """
        根据市净率范围获取股票数据
        :param min_pb: 最小市净率
        :param max_pb: 最大市净率
        :param trade_date: 交易日期，默认为最新日期
        :return: 符合条件的股票列表
        """
        query = StockDailyBasic.query.filter(
            StockDailyBasic.pb >= min_pb,
            StockDailyBasic.pb <= max_pb,
            StockDailyBasic.pb.isnot(None)
        )
        
        if trade_date:
            query = query.filter(StockDailyBasic.trade_date == trade_date)
        else:
            # 获取最新交易日期
            latest_date = db.session.query(db.func.max(StockDailyBasic.trade_date)).scalar()
            if latest_date:
                query = query.filter(StockDailyBasic.trade_date == latest_date)
        
        results = query.all()
        return [item.as_dict() for item in results]
    
    @staticmethod
    def get_by_turnover_rate(min_rate: float, max_rate: float, trade_date: str = None) -> List[Dict]:
        """
        根据换手率范围获取股票数据
        :param min_rate: 最小换手率
        :param max_rate: 最大换手率
        :param trade_date: 交易日期，默认为最新日期
        :return: 符合条件的股票列表
        """
        query = StockDailyBasic.query.filter(
            StockDailyBasic.turnover_rate >= min_rate,
            StockDailyBasic.turnover_rate <= max_rate,
            StockDailyBasic.turnover_rate.isnot(None)
        )
        
        if trade_date:
            query = query.filter(StockDailyBasic.trade_date == trade_date)
        else:
            # 获取最新交易日期
            latest_date = db.session.query(db.func.max(StockDailyBasic.trade_date)).scalar()
            if latest_date:
                query = query.filter(StockDailyBasic.trade_date == latest_date)
        
        results = query.all()
        return [item.as_dict() for item in results]
    
    @staticmethod
    def get_market_summary(trade_date: str = None) -> Dict:
        """
        获取市场概况统计
        :param trade_date: 交易日期，默认为最新日期
        :return: 市场概况数据
        """
        if not trade_date:
            # 获取最新交易日期
            latest_date = db.session.query(db.func.max(StockDailyBasic.trade_date)).scalar()
            if latest_date:
                trade_date = latest_date.strftime('%Y-%m-%d')
            else:
                return {}
        
        # 统计各项指标
        stats = db.session.query(
            db.func.count(StockDailyBasic.ts_code).label('total_stocks'),
            db.func.avg(StockDailyBasic.pe).label('avg_pe'),
            db.func.avg(StockDailyBasic.pb).label('avg_pb'),
            db.func.avg(StockDailyBasic.turnover_rate).label('avg_turnover_rate'),
            db.func.sum(StockDailyBasic.total_mv).label('total_market_value'),
            db.func.sum(StockDailyBasic.circ_mv).label('total_circulation_value')
        ).filter(StockDailyBasic.trade_date == trade_date).first()
        
        return {
            'trade_date': trade_date,
            'total_stocks': stats.total_stocks,
            'avg_pe': float(stats.avg_pe) if stats.avg_pe else None,
            'avg_pb': float(stats.avg_pb) if stats.avg_pb else None,
            'avg_turnover_rate': float(stats.avg_turnover_rate) if stats.avg_turnover_rate else None,
            'total_market_value': float(stats.total_market_value) if stats.total_market_value else None,
            'total_circulation_value': float(stats.total_circulation_value) if stats.total_circulation_value else None
        }


# 创建全局服务实例
stock_daily_basic_service = StockDailyBasicService() 