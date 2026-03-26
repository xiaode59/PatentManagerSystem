from flask import Blueprint, request
from app.appService.RAGService import rag_service
from app.utils.ResponseForm import ResponseForm

ai_bp = Blueprint('ai', __name__)

@ai_bp.route('/ai/ask', methods=['POST'])
def ask_question():
    """AI问答接口"""
    data = request.get_json()
    
    # 验证参数
    if not data or 'question' not in data:
        return ResponseForm.error('请提供问题')
    
    question = data['question'].strip()
    
    if not question:
        return ResponseForm.error('问题不能为空')
    
    # 调用RAG服务生成回答
    result = rag_service.generate_answer(question)
    
    if result['success']:
        return ResponseForm.success('获取回答成功', {
            'answer': result['answer'],
            'references': result.get('references', []),
            'mode': result.get('mode', 'unknown')
        })
    else:
        return ResponseForm.error(result.get('message', '生成回答失败'))


@ai_bp.route('/ai/status', methods=['GET'])
def get_status():
    """获取AI助手状态"""
    # 检查向量数据库状态
    try:
        info = rag_service.get_collection_info()
        if info['success']:
            db_status = f"已初始化，文档数: {info['count']}"
        else:
            db_status = "未初始化"
    except Exception:
        db_status = "未初始化"
    
    return ResponseForm.success('AI助手状态', {
        'status': 'online',
        'db_status': db_status,
        'ready': True
    })


@ai_bp.route('/ai/init-db', methods=['POST'])
def init_database():
    """初始化向量数据库（构建知识库）"""
    try:
        # 初始化
        init_result = rag_service.initialize()
        if not init_result['success']:
            return ResponseForm.error(init_result['message'])
        
        # 构建知识库
        build_result = rag_service.build_knowledge_base()
        
        if build_result['success']:
            return ResponseForm.success('知识库构建成功', {
                'document_count': build_result['count']
            })
        else:
            return ResponseForm.error(build_result['message'])
            
    except Exception as e:
        return ResponseForm.error(f'初始化失败: {str(e)}')


@ai_bp.route('/ai/search', methods=['POST'])
def search_knowledge():
    """知识库搜索"""
    data = request.get_json()
    
    if not data or 'query' not in data:
        return ResponseForm.error('请提供搜索关键词')
    
    query = data['query'].strip()
    top_k = data.get('top_k', 3)
    
    result = rag_service.similarity_search(query, top_k=top_k)
    
    if result['success']:
        return ResponseForm.success('搜索成功', {
            'results': result.get('results', [])
        })
    else:
        return ResponseForm.error(result.get('message', '搜索失败'))
