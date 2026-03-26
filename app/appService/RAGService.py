import os
import json
from datetime import datetime
from openai import OpenAI
from app.utils.prompts import SYSTEM_PROMPT_TEMPLATE, PATENT_KNOWLEDGE


class RAGService:
    """RAG向量数据库服务"""
    
    def __init__(self):
        self.vector_store = None
        self.initialized = False
        self.collection_name = "patent_knowledge"
        
        # 初始化大模型客户端（阿里云通义千问）- 从环境变量读取敏感信息
        self.llm_client = OpenAI(
            api_key=os.environ.get("DASHSCOPE_API_KEY", ""),
            base_url=os.environ.get("DASHSCOPE_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
        )
        self.llm_model = os.environ.get("DASHSCOPE_MODEL", "qwen-plus")
        
        # 调试日志保存目录
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.debug_log_dir = os.path.join(base_dir, 'logs', 'rag_debug')
    
    def initialize(self):
        """初始化向量数据库"""
        try:
            import chromadb
            from chromadb.config import Settings
            
            # 获取数据目录
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            persist_dir = os.path.join(base_dir, 'instance', 'vector_db')
            
            # 创建目录
            os.makedirs(persist_dir, exist_ok=True)
            
            # 初始化Chroma客户端
            self.client = chromadb.PersistentClient(path=persist_dir)
            
            # 获取或创建集合
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"description": "专利知识库向量存储"}
            )
            
            self.initialized = True
            return {'success': True, 'message': '向量数据库初始化成功'}
            
        except ImportError:
            return {'success': False, 'message': '请安装chromadb: pip install chromadb'}
        except Exception as e:
            return {'success': False, 'message': f'初始化失败: {str(e)}'}
    
    def add_documents(self, documents: list, metadatas: list = None, ids: list = None):
        """添加文档到向量库"""
        if not self.initialized:
            init_result = self.initialize()
            if not init_result['success']:
                return init_result
        
        try:
            # 生成ID
            if ids is None:
                ids = [f"doc_{i}_{datetime.now().timestamp()}" for i in range(len(documents))]
            
            # 元数据
            if metadatas is None:
                metadatas = [{"source": "manual_add"} for _ in documents]
            
            # 添加文档
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            
            return {'success': True, 'count': len(documents)}
            
        except Exception as e:
            return {'success': False, 'message': f'添加文档失败: {str(e)}'}
    
    def similarity_search(self, query: str, top_k: int = 3):
        """相似度搜索"""
        if not self.initialized:
            init_result = self.initialize()
            if not init_result['success']:
                return {'success': False, 'message': init_result['message']}
        
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=top_k
            )
            
            # 格式化结果
            formatted_results = []
            if results['documents'] and len(results['documents']) > 0:
                for i, doc in enumerate(results['documents'][0]):
                    formatted_results.append({
                        'content': doc,
                        'metadata': results['metadatas'][0][i] if results['metadatas'] else {},
                        'distance': results['distances'][0][i] if results.get('distances') else None
                    })
            
            return {'success': True, 'results': formatted_results}
            
        except Exception as e:
            return {'success': False, 'message': f'搜索失败: {str(e)}'}
    
    def get_collection_info(self):
        """获取集合信息"""
        if not self.initialized:
            init_result = self.initialize()
            if not init_result['success']:
                return {'success': False, 'message': init_result['message']}
        
        try:
            count = self.collection.count()
            return {
                'success': True,
                'count': count,
                'name': self.collection_name
            }
        except Exception as e:
            return {'success': False, 'message': str(e)}
    
    def build_knowledge_base(self):
        """构建示例知识库"""
        # 使用从 prompts.py 导入的知识库数据
        documents = [item['content'] for item in PATENT_KNOWLEDGE]
        metadatas = [item['metadata'] for item in PATENT_KNOWLEDGE]
        
        return self.add_documents(documents, metadatas)
    
    def _save_debug_log(self, query: str, result: dict):
        """保存调试日志到本地"""
        try:
            os.makedirs(self.debug_log_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_filename = f"rag_response_{timestamp}.json"
            log_path = os.path.join(self.debug_log_dir, log_filename)
            
            log_data = {
                'timestamp': datetime.now().isoformat(),
                'query': query,
                'result': result
            }
            
            with open(log_path, 'w', encoding='utf-8') as f:
                json.dump(log_data, f, ensure_ascii=False, indent=2)
            
            print(f"[DEBUG] 回复已保存至: {log_path}")
            
        except Exception as e:
            print(f"[DEBUG] 保存调试日志失败: {str(e)}")
    
    def generate_answer(self, query: str) -> dict:
        """生成回答（基于RAG+大模型）"""
        # 1. 搜索相关文档
        search_result = self.similarity_search(query, top_k=3)
        
        # 2. 构建上下文
        context = ""
        references = []
        if search_result['success'] and search_result['results']:
            context = "\n\n".join([
                f"参考{i+1}: {r['content']}"
                for i, r in enumerate(search_result['results'])
            ])
            references = search_result['results']
        
        # 3. 调用大模型生成回答
        try:
            # 使用从 prompts.py 导入的系统提示词模板
            system_prompt = SYSTEM_PROMPT_TEMPLATE.format(context=context)
            
            # 调用大模型
            response = self.llm_client.chat.completions.create(
                model=self.llm_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            answer = response.choices[0].message.content
            
            result = {
                'success': True,
                'answer': answer,
                'references': references,
                'mode': 'rag' if references else 'llm_only'
            }
            
            # 4. 保存调试日志
            self._save_debug_log(query, result)
            
            print(result)
            
            return result
            
        except Exception as e:
            # 如果大模型调用失败，返回模拟回答
            print(f"LLM调用失败: {str(e)}")
            result = self._mock_answer(query)
            # 保存调试日志
            self._save_debug_log(query, result)
            return result
    
    def _generate_from_context(self, query: str, context: str, references: list) -> str:
        """基于上下文生成回答"""
        # 检查是否有相关参考
        if not references:
            return self._mock_answer(query)
        
        # 简单模板匹配生成回答
        query_lower = query.lower()
        
        if '专利' in query:
            if '申请' in query or '撰写' in query:
                return f"关于专利申请，我为您找到以下信息：\n\n{references[0]['content']}\n\n如有更多疑问，欢迎继续提问！"
            elif '保护期限' in query or '年限' in query:
                return f"关于专利保护期限：\n\n{references[1]['content']}\n\n希望对您有帮助！"
            elif '审查' in query or '流程' in query:
                return f"专利审查流程：\n\n{references[0]['content']}\n\n如需了解具体进度，请提供更多信息。"
        
        if '软著' in query or '软件著作权' in query:
            if '申请' in query or '需要' in query:
                return f"关于软著申请：\n\n{references[0]['content']}\n\n如有疑问请继续问我！"
            elif '流程' in query:
                return f"软著登记流程：\n\n{references[0]['content']}\n\n一般需要2-3个月。"
        
        # 默认返回第一条相关结果
        return f"根据我的知识库，我找到以下相关信息：\n\n{references[0]['content']}\n\n如需了解更多，请告诉我具体想了解哪方面？"
    
    def _mock_answer(self, query: str) -> dict:
        """模拟回答（当RAG不可用时）"""
        # 简单的关键词匹配
        query_lower = query.lower()
        
        if '专利' in query:
            if '申请' in query or '撰写' in query:
                return {
                    'success': True,
                    'answer': '专利申请文件主要包括：请求书、说明书、权利要求书、摘要。说明书应当对发明作出清楚、完整的说明，以本领域技术人员能够实现为准。\n\n建议您准备好技术交底书后再进行申请。',
                    'references': [],
                    'mode': 'mock'
                }
            elif '保护期限' in query:
                return {
                    'success': True,
                    'answer': '专利保护期限：\n- 发明专利：20年\n- 实用新型专利：10年\n- 外观设计专利：15年（2021年修法后）',
                    'references': [],
                    'mode': 'mock'
                }
        
        if '软著' in query or '软件著作权' in query:
            if '申请' in query or '需要' in query:
                return {
                    'success': True,
                    'answer': '软件著作权申请需要准备：\n1. 软件源代码（前、后各3000行）\n2. 软件说明书\n3. 身份证明文件\n\n可在中国版权保护中心在线提交申请。',
                    'references': [],
                    'mode': 'mock'
                }
        
        # 默认回答
        return {
            'success': True,
            'answer': f'您的问题是："{query}"\n\n感谢您的提问！关于专利和软著申请的具体问题，我可以为您提供以下帮助：\n- 专利申请流程和文件要求\n- 软著申请所需材料\n- 专利保护期限\n- 审查流程说明\n\n请告诉我您具体想了解什么？',
            'references': [],
            'mode': 'mock'
        }


# 全局服务实例
rag_service = RAGService()
