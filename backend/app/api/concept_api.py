from flask import Blueprint, request, jsonify
from app.services.concept_service import (
    get_all_concepts, get_concept_by_id, get_concept_by_code,
    create_concept, update_concept, delete_concept, get_concepts_by_src
)

bp = Blueprint('concept', __name__, url_prefix='/api/concept')

@bp.route('/', methods=['GET'])
def list_concepts():
    """获取概念股分类列表"""
    src = request.args.get('src')
    if src:
        concepts = get_concepts_by_src(src)
    else:
        concepts = get_all_concepts()
    
    result = []
    for concept in concepts:
        result.append(concept.as_dict())
    
    return jsonify(result)

@bp.route('/<int:concept_id>', methods=['GET'])
def get_concept(concept_id):
    """获取单个概念股分类"""
    concept = get_concept_by_id(concept_id)
    if concept:
        return jsonify(concept.as_dict())
    return jsonify({'error': '概念股分类不存在'}), 404

@bp.route('/code/<code>', methods=['GET'])
def get_concept_by_code_api(code):
    """根据代码获取概念股分类"""
    concept = get_concept_by_code(code)
    if concept:
        return jsonify(concept.as_dict())
    return jsonify({'error': '概念股分类不存在'}), 404

@bp.route('/', methods=['POST'])
def add_concept():
    """创建概念股分类"""
    data = request.get_json()
    if not data or 'code' not in data or 'name' not in data:
        return jsonify({'error': '缺少必要参数'}), 400
    
    # 检查是否已存在
    existing = get_concept_by_code(data['code'])
    if existing:
        return jsonify({'error': '概念股分类代码已存在'}), 400
    
    src = data.get('src', 'ts')
    concept = create_concept(data['code'], data['name'], src)
    return jsonify(concept.as_dict()), 201

@bp.route('/<int:concept_id>', methods=['PUT'])
def modify_concept(concept_id):
    """更新概念股分类"""
    data = request.get_json()
    if not data:
        return jsonify({'error': '缺少更新数据'}), 400
    
    concept = update_concept(concept_id, **data)
    if concept:
        return jsonify(concept.as_dict())
    return jsonify({'error': '概念股分类不存在'}), 404

@bp.route('/<int:concept_id>', methods=['DELETE'])
def remove_concept(concept_id):
    """删除概念股分类"""
    success = delete_concept(concept_id)
    if success:
        return jsonify({'message': '删除成功'})
    return jsonify({'error': '概念股分类不存在'}), 404 