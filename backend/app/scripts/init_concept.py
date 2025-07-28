import tushare as ts
import pandas as pd
from app import create_app, db
from app.models.concept import Concept
from app.services.concept_service import create_concept, get_concept_by_code

def init_concept_data():
    """初始化概念股分类数据"""
    # 设置tushare token
    ts.set_token('82184947ad890848c5873e738c856ecff5d31d649d9d443c34b6f5b4')
    pro = ts.pro_api()
    
    try:
        # 获取概念股分类数据
        print("正在获取概念股分类数据...")
        df = pro.concept()
        
        if df is not None and not df.empty:
            print(f"获取到 {len(df)} 条概念股分类数据")
            
            # 清空现有数据
            Concept.query.delete()
            db.session.commit()
            print("已清空现有数据")
            
            # 批量插入数据
            records = []
            for index, row in df.iterrows():
                # 检查是否已存在
                existing = get_concept_by_code(row['code'])
                if not existing:
                    concept = Concept(
                        code=row['code'],
                        name=row['name'],
                        src=row.get('src', 'ts')
                    )
                    records.append(concept)
            
            if records:
                db.session.add_all(records)
                db.session.commit()
                print(f"成功插入 {len(records)} 条概念股分类数据")
            else:
                print("没有新的概念股分类数据需要插入")
        else:
            print("未获取到概念股分类数据")
            
    except Exception as e:
        print(f"获取概念股分类数据失败: {e}")
        db.session.rollback()

def add_sample_concepts():
    """添加示例概念股分类数据"""
    sample_concepts = [
        {'code': 'TS2', 'name': '5G', 'src': 'ts'},
        {'code': 'TS3', 'name': '机场', 'src': 'ts'},
        {'code': 'TS4', 'name': '高价股', 'src': 'ts'},
        {'code': 'TS5', 'name': '烧碱', 'src': 'ts'},
        {'code': 'TS6', 'name': 'AH溢价股', 'src': 'ts'},
        {'code': 'TS7', 'name': '保险', 'src': 'ts'},
        {'code': 'TS8', 'name': 'PVC', 'src': 'ts'},
        {'code': 'TS9', 'name': '啤酒', 'src': 'ts'},
        {'code': 'TS10', 'name': '火电', 'src': 'ts'},
        {'code': 'TS11', 'name': '银行', 'src': 'ts'},
        {'code': 'TS12', 'name': '碳纤维', 'src': 'ts'},
        {'code': 'TS13', 'name': '安邦系', 'src': 'ts'},
        {'code': 'TS14', 'name': '特高压', 'src': 'ts'},
        {'code': 'TS15', 'name': '高股息', 'src': 'ts'},
        {'code': 'TS16', 'name': '光通信', 'src': 'ts'},
        {'code': 'TS17', 'name': '草甘膦', 'src': 'ts'},
        {'code': 'TS18', 'name': '高速公路', 'src': 'ts'},
        {'code': 'TS19', 'name': '有色-铝', 'src': 'ts'},
        {'code': 'TS20', 'name': '有色-锆', 'src': 'ts'}
    ]
    
    print("正在添加示例概念股分类数据...")
    added_count = 0
    
    for concept_data in sample_concepts:
        # 检查是否已存在
        existing = get_concept_by_code(concept_data['code'])
        if not existing:
            create_concept(
                code=concept_data['code'],
                name=concept_data['name'],
                src=concept_data['src']
            )
            added_count += 1
    
    print(f"成功添加 {added_count} 条示例概念股分类数据")

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        # 初始化概念股分类数据
        init_concept_data()
        
        # 如果没有数据，添加示例数据
        concepts = Concept.query.all()
        if not concepts:
            print("没有概念股分类数据，添加示例数据...")
            # add_sample_concepts()
        
        print("概念股分类数据初始化完成") 