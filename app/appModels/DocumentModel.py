from app import db
import datetime

class DocumentModel(db.Model):
    """知识库文档模型"""
    __tablename__ = 'documents'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)      # 文档标题
    category = db.Column(db.String(50), nullable=False)    # 分类标签
    file_path = db.Column(db.String(500))                  # 文件路径
    file_type = db.Column(db.String(20))                   # 文件类型: pdf/mp4/txt
    content_text = db.Column(db.Text)                      # 文本内容(用于检索)
    description = db.Column(db.Text)                       # 描述
    tags = db.Column(db.String(200))                       # 标签(逗号分隔)
    is_vectorized = db.Column(db.Boolean, default=False)   # 是否已向量化
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'category': self.category,
            'category_name': self.get_category_name(),
            'file_path': self.file_path,
            'file_type': self.file_type,
            'file_type_name': self.get_file_type_name(),
            'description': self.description,
            'tags': self.tags,
            'is_vectorized': self.is_vectorized,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }
    
    def get_category_name(self):
        category_map = {
            'patent_writing': '专利撰写',
            'software_process': '软著流程',
            'case_reference': '案例参考',
            'faq': '常见问题',
            'template': '模板下载',
            'video': '教学视频'
        }
        return category_map.get(self.category, self.category)
    
    def get_file_type_name(self):
        type_map = {
            'pdf': 'PDF文档',
            'mp4': '视频',
            'txt': '文本',
            'doc': 'Word文档',
            'docx': 'Word文档'
        }
        return type_map.get(self.file_type, self.file_type)
