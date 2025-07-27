import os
import sys
import datetime

# 让脚本可以导入 app 相关模块
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.stock_company import StockCompany
from app.models.industry import Industry
from app.models.stock_daily import StockDaily
from app.models.industry_stats import IndustryStats
from sqlalchemy import func

def init_industry_stats():
    with create_app().app_context():
        # 获取所有行业
        industries = Industry.query.all()
        
        # 获取所有交易日期
        trade_dates = db.session.query(StockDaily.trade_date).distinct().all()
        trade_dates = [date[0] for date in trade_dates]
        
        count = 0
        for industry in industries:
            # 获取该行业下的所有公司
            companies = StockCompany.query.filter_by(industry=industry.name).all()
            company_ids = [c.id for c in companies]


            print(industry, len(trade_dates), len(company_ids))

            if not company_ids:
                continue
                
            for trade_date in trade_dates:
                # 检查是否已存在该行业该日期的统计
                exists = IndustryStats.query.filter_by(
                    industry_id=industry.id, 
                    stat_date=trade_date
                ).first()
                
                if exists:
                    continue
                
                # 获取该行业下所有公司在该日期的交易数据
                daily_data = StockDaily.query.filter(
                    StockDaily.ts_code.in_([c.ts_code for c in companies]),
                    StockDaily.trade_date == trade_date
                ).all()
                
                if not daily_data:
                    continue
                
                # 统计计算
                company_count = len(companies)
                total_amount = sum(d.amount or 0 for d in daily_data)
                up_count = sum(1 for d in daily_data if d.pct_chg and d.pct_chg > 0)
                down_count = sum(1 for d in daily_data if d.pct_chg and d.pct_chg < 0)
                flat_count = sum(1 for d in daily_data if d.pct_chg and d.pct_chg == 0)
                
                # 创建统计记录
                stats = IndustryStats(
                    industry_id=industry.id,
                    stat_date=trade_date,
                    company_count=company_count,
                    total_amount=total_amount,
                    up_count=up_count,
                    down_count=down_count,
                    flat_count=flat_count
                )
                db.session.add(stats)
                count += 1
        
        db.session.commit()
        print(f"已插入 {count} 条行业统计数据。")

if __name__ == '__main__':
    init_industry_stats() 