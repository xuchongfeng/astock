from flask import Blueprint, request, jsonify
from app.services.article_service import article_service
from sqlalchemy import desc, asc
from app.models.article import Article
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

bp = Blueprint('article', __name__, url_prefix='/api/articles')

@bp.route('/', methods=['GET'])
def list_articles():
    """获取文章列表"""
    try:
        # 获取查询参数
        filters = {}
        for key in ['user_id', 'status', 'category', 'is_public', 'tags', 'title', 'content']:
            value = request.args.get(key)
            if value:
                filters[key] = value
        
        # 分页参数
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', 20))
        
        # 排序参数
        sort_fields = request.args.get('sort_fields')
        
        # 获取查询对象
        query = article_service.get_all_articles(filters, query_only=True)
        total = query.count()
        
        # 应用排序
        if sort_fields:
            for field in sort_fields.split(','):
                field = field.strip()
                if not field:
                    continue
                if field.startswith('-'):
                    # 降序排序
                    field_name = field[1:]
                    if field_name in ['id', 'created_at', 'updated_at', 'published_at', 'view_count', 'like_count']:
                        query = query.order_by(desc(getattr(Article, field_name)))
                else:
                    # 升序排序
                    if field in ['id', 'created_at', 'updated_at', 'published_at', 'view_count', 'like_count']:
                        query = query.order_by(asc(getattr(Article, field)))
        
        # 应用分页
        items = query.offset((page - 1) * page_size).limit(page_size).all()
        
        # 格式化返回数据
        result_data = [item.as_dict() for item in items]
        
        return jsonify({
            'data': result_data,
            'total': total,
            'page': page,
            'page_size': page_size
        })
        
    except Exception as e:
        logger.error(f"获取文章列表失败: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:article_id>', methods=['GET'])
def get_article(article_id):
    """获取单篇文章"""
    try:
        article = article_service.get_article_by_id(article_id)
        if not article:
            return jsonify({'error': '文章不存在'}), 404
        
        # 增加浏览次数
        article_service.increment_view_count(article_id)
        
        return jsonify(article.as_dict())
        
    except Exception as e:
        logger.error(f"获取文章失败: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/', methods=['POST'])
def create_article():
    """创建文章"""
    try:
        data = request.json
        if not data:
            return jsonify({'error': '请求数据不能为空'}), 400
        
        # 验证必填字段
        required_fields = ['user_id', 'title', 'content']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'{field} 不能为空'}), 400
        
        article = article_service.create_article(data)
        if not article:
            return jsonify({'error': '创建文章失败'}), 500
        
        return jsonify(article.as_dict()), 201
        
    except Exception as e:
        logger.error(f"创建文章失败: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:article_id>', methods=['PUT'])
def update_article(article_id):
    """更新文章"""
    try:
        data = request.json
        if not data:
            return jsonify({'error': '请求数据不能为空'}), 400
        
        article = article_service.update_article(article_id, data)
        if not article:
            return jsonify({'error': '文章不存在或更新失败'}), 404
        
        return jsonify(article.as_dict())
        
    except Exception as e:
        logger.error(f"更新文章失败: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:article_id>', methods=['DELETE'])
def delete_article(article_id):
    """删除文章"""
    try:
        success = article_service.delete_article(article_id)
        if not success:
            return jsonify({'error': '文章不存在或删除失败'}), 404
        
        return jsonify({'message': '删除成功'})
        
    except Exception as e:
        logger.error(f"删除文章失败: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:article_id>/like', methods=['POST'])
def like_article(article_id):
    """点赞文章"""
    try:
        success = article_service.increment_like_count(article_id)
        if not success:
            return jsonify({'error': '文章不存在'}), 404
        
        return jsonify({'message': '点赞成功'})
        
    except Exception as e:
        logger.error(f"点赞文章失败: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/user/<int:user_id>', methods=['GET'])
def get_user_articles(user_id):
    """获取用户文章"""
    try:
        status = request.args.get('status')
        articles = article_service.get_user_articles(user_id, status)
        
        result_data = [article.as_dict() for article in articles]
        
        return jsonify({
            'data': result_data,
            'total': len(result_data)
        })
        
    except Exception as e:
        logger.error(f"获取用户文章失败: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/public', methods=['GET'])
def get_public_articles():
    """获取公开文章"""
    try:
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', 20))
        
        offset = (page - 1) * page_size
        articles = article_service.get_public_articles(page_size, offset)
        
        result_data = [article.as_dict() for article in articles]
        
        return jsonify({
            'data': result_data,
            'page': page,
            'page_size': page_size
        })
        
    except Exception as e:
        logger.error(f"获取公开文章失败: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/user/<int:user_id>/statistics', methods=['GET'])
def get_user_article_statistics(user_id):
    """获取用户文章统计"""
    try:
        statistics = article_service.get_article_statistics(user_id)
        return jsonify(statistics)
        
    except Exception as e:
        logger.error(f"获取用户文章统计失败: {str(e)}")
        return jsonify({'error': str(e)}), 500
