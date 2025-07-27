
import os
import sys

# 让脚本可以导入 app 相关模块
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.stock_company import StockCompany
from app.models.industry import Industry

def init_industry():
    with create_app().app_context():
        # 读取所有公司行业字段，去重
        industries = db.session.query(StockCompany.industry).distinct().all()
        industries = [i[0] for i in industries if i[0]]  # 去除None和空值

        count = 0
        for name in industries:
            # 检查是否已存在
            exists = Industry.query.filter_by(name=name).first()
            if not exists:
                industry = Industry(name=name)
                db.session.add(industry)
                count += 1
        db.session.commit()
        print(f"已插入 {count} 个新行业。")

if __name__ == '__main__':
    init_industry()