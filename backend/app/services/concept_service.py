from app.models.concept import Concept
from app import db

def get_all_concepts():
    """获取所有概念股分类"""
    return Concept.query.all()

def get_concept_by_id(concept_id):
    """根据ID获取概念股分类"""
    return Concept.query.get(concept_id)

def get_concept_by_code(code):
    """根据代码获取概念股分类"""
    return Concept.query.filter_by(code=code).first()

def create_concept(code, name, src='ts'):
    """创建概念股分类"""
    concept = Concept(code=code, name=name, src=src)
    db.session.add(concept)
    db.session.commit()
    return concept

def update_concept(concept_id, **kwargs):
    """更新概念股分类"""
    concept = get_concept_by_id(concept_id)
    if concept:
        for key, value in kwargs.items():
            if hasattr(concept, key):
                setattr(concept, key, value)
        db.session.commit()
    return concept

def delete_concept(concept_id):
    """删除概念股分类"""
    concept = get_concept_by_id(concept_id)
    if concept:
        db.session.delete(concept)
        db.session.commit()
        return True
    return False

def get_concepts_by_src(src):
    """根据来源获取概念股分类"""
    return Concept.query.filter_by(src=src).all() 