import datetime
import multiprocessing as mp
from functools import partial
from app import create_app, db
from app.models.stock_daily import StockDaily
from app.models.strategy import Strategy
from app.models.strategy_stock import StrategyStock

def get_avg_vol(ts_code, start_date, end_date):
    """获取区间内平均成交量"""
    q = StockDaily.query.filter(
        StockDaily.ts_code == ts_code,
        StockDaily.trade_date >= start_date,
        StockDaily.trade_date <= end_date
    )
    vols = [float(x.vol) for x in q.all() if x.vol is not None]
    return sum(vols) / len(vols) if vols else 0

def get_avg_close(ts_code, start_date, end_date):
    """获取区间内平均收盘价"""
    q = StockDaily.query.filter(
        StockDaily.ts_code == ts_code,
        StockDaily.trade_date >= start_date,
        StockDaily.trade_date <= end_date
    )
    closes = [float(x.close) for x in q.all() if x.close is not None]
    return sum(closes) / len(closes) if closes else 0

def get_avg_amount(ts_code, start_date, end_date):
    """获取区间内平均交易额"""
    q = StockDaily.query.filter(
        StockDaily.ts_code == ts_code,
        StockDaily.trade_date >= start_date,
        StockDaily.trade_date <= end_date
    )
    amounts = [float(x.amount) for x in q.all() if x.amount is not None]
    return sum(amounts) / len(amounts) if amounts else 0

def get_hit_count(ts_code, strategy_id, start_date, end_date):
    """获取指定时间段内命中策略的次数"""
    count = StrategyStock.query.filter(
        StrategyStock.ts_code == ts_code,
        StrategyStock.strategy_id == strategy_id,
        StrategyStock.date >= start_date,
        StrategyStock.date <= end_date
    ).count()
    return count

def get_all_ts_codes():
    """获取所有股票代码"""
    return [row.ts_code for row in db.session.query(StockDaily.ts_code).distinct()]

def process_stock_batch(ts_codes_batch, strategy_id, trade_date):
    """处理一批股票的策略选股"""
    app = create_app()
    with app.app_context():
        selected = []
        
        # 计算区间
        def get_date_delta(base, days):
            return base - datetime.timedelta(days=days)

        for ts_code in ts_codes_batch:
            # 先检查记录是否存在
            exists = StrategyStock.query.filter_by(strategy_id=strategy_id, ts_code=ts_code, date=trade_date).first()
            if exists:
                # 记录已存在，只计算命中次数
                hit_count_5d = get_hit_count(ts_code, strategy_id, get_date_delta(trade_date, 4), trade_date)
                hit_count_15d = get_hit_count(ts_code, strategy_id, get_date_delta(trade_date, 14), trade_date)
                hit_count_30d = get_hit_count(ts_code, strategy_id, get_date_delta(trade_date, 29), trade_date)
                selected.append((ts_code, None, hit_count_5d, hit_count_15d, hit_count_30d, True))  # True表示已存在
                continue

            # 记录不存在，执行策略计算
            # 1. 最近1日成交量 > 前5日均值*1.3
            day1 = trade_date
            day1_vol = get_avg_vol(ts_code, day1, day1)
            day1_5ago = get_date_delta(day1, 5)
            pre5_vol = get_avg_vol(ts_code, day1_5ago, get_date_delta(day1, 1))
            cond1 = pre5_vol > 0 and day1_vol > pre5_vol * 1.3

            # 2. 最近5日均量 > 前5日均量*1.2
            day5 = get_date_delta(day1, 4)
            pre5_5ago = get_date_delta(day5, 5)
            last5_vol = get_avg_vol(ts_code, day5, day1)
            pre5_vol2 = get_avg_vol(ts_code, pre5_5ago, get_date_delta(day5, 1))
            cond2 = pre5_vol2 > 0 and last5_vol > pre5_vol2 * 1.2

            # 3. 最近15日均量 > 前15日均量*1.1
            day15 = get_date_delta(day1, 14)
            pre15_15ago = get_date_delta(day15, 15)
            last15_vol = get_avg_vol(ts_code, day15, day1)
            pre15_vol = get_avg_vol(ts_code, pre15_15ago, get_date_delta(day15, 1))
            cond3 = pre15_vol > 0 and last15_vol > pre15_vol * 1.1

            # 4. 当日收盘价 > 最近5日均价*1.05
            last5_close = get_avg_close(ts_code, day5, day1)
            day1_close = get_avg_close(ts_code, day1, day1)
            cond4 = last5_close > 0 and day1_close > last5_close * 1.05

            # 5. 最近5日均价 > 前5日均价*1.05
            pre5_close = get_avg_close(ts_code, pre5_5ago, get_date_delta(day5, 1))
            cond5 = pre5_close > 0 and last5_close > pre5_close * 1.05

            # 6. 最近15日均价 > 前15日均价*1.1
            last15_close = get_avg_close(ts_code, day15, day1)
            pre15_close = get_avg_close(ts_code, pre15_15ago, get_date_delta(day15, 1))
            cond6 = pre15_close > 0 and last15_close > pre15_close * 1.1

            # 1,2,3为或，4,5,6为或，最终为(1或2或3)且(4或5或6)
            if (cond1 or cond2 or cond3) and (cond4 or cond5 or cond6):
                avg_amount_5d = get_avg_amount(ts_code, day5, day1)
                # 计算命中次数
                hit_count_5d = get_hit_count(ts_code, strategy_id, get_date_delta(trade_date, 4), trade_date)
                hit_count_15d = get_hit_count(ts_code, strategy_id, get_date_delta(trade_date, 14), trade_date)
                hit_count_30d = get_hit_count(ts_code, strategy_id, get_date_delta(trade_date, 29), trade_date)
                selected.append((ts_code, avg_amount_5d, hit_count_5d, hit_count_15d, hit_count_30d, False))  # False表示新记录
        
        return selected

def run_strategy_parallel(strategy_id, trade_date=None, num_processes=6):
    """
    使用多进程执行策略选股
    :param strategy_id: 策略ID
    :param trade_date: 选股基准日（默认今天）
    :param num_processes: 进程数
    """
    app = create_app()
    with app.app_context():
        if trade_date is None:
            trade_date = datetime.date.today()
        elif isinstance(trade_date, str):
            trade_date = datetime.datetime.strptime(trade_date, '%Y-%m-%d').date()

        ts_codes = get_all_ts_codes()
        print(f"总股票数：{len(ts_codes)}")
        
        # 分批处理
        batch_size = len(ts_codes) // num_processes + 1
        batches = [ts_codes[i:i + batch_size] for i in range(0, len(ts_codes), batch_size)]
        
        # 使用多进程处理
        with mp.Pool(processes=num_processes) as pool:
            process_func = partial(process_stock_batch, strategy_id=strategy_id, trade_date=trade_date)
            results = pool.map(process_func, batches)
        
        # 合并结果
        all_selected = []
        for batch_result in results:
            all_selected.extend(batch_result)
        
        # 写入数据库
        for ts_code, avg_amount_5d, hit_count_5d, hit_count_15d, hit_count_30d, is_existing in all_selected:
            if is_existing:
                # 更新已存在记录的命中次数
                exists = StrategyStock.query.filter_by(strategy_id=strategy_id, ts_code=ts_code, date=trade_date).first()
                exists.hit_count_5d = hit_count_5d
                exists.hit_count_15d = hit_count_15d
                exists.hit_count_30d = hit_count_30d
            else:
                # 新增记录
                exists = StrategyStock.query.filter_by(strategy_id=strategy_id, ts_code=ts_code, date=trade_date).first()
                if not exists:
                    db.session.add(StrategyStock(
                        strategy_id=strategy_id, 
                        ts_code=ts_code, 
                        date=trade_date, 
                        avg_amount_5d=avg_amount_5d,
                        hit_count_5d=hit_count_5d,
                        hit_count_15d=hit_count_15d,
                        hit_count_30d=hit_count_30d
                    ))
                else:
                    exists.avg_amount_5d = avg_amount_5d
                    exists.hit_count_5d = hit_count_5d
                    exists.hit_count_15d = hit_count_15d
                    exists.hit_count_30d = hit_count_30d
        db.session.commit()
        
        print(f"策略选股完成，入选股票数：{len(all_selected)}")

if __name__ == '__main__':
    # 获取最近60天的数据
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=1)
    
    current_date = start_date
    while current_date <= end_date:
        print(f"执行策略选股，日期：{current_date}")
        run_strategy_parallel(strategy_id=1, trade_date=current_date, num_processes=6)
        current_date += datetime.timedelta(days=1)
    
    print("最近60天策略选股完成")