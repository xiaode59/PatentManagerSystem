from app import db
import datetime

class PatentModel(db.Model):
    """专利/软著信息模型"""
    __tablename__ = 'patents'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)  # 名称
    type = db.Column(db.String(20), nullable=False)   # 类型: invention/utility/software
    application_no = db.Column(db.String(50))         # 申请号
    registration_no = db.Column(db.String(50))        # 登记号
    applicant = db.Column(db.String(100))             # 申请人
    inventor = db.Column(db.String(100))             # 发明人
    status = db.Column(db.String(20), default='applied')  # 状态
    application_date = db.Column(db.Date)              # 申请日
    publish_date = db.Column(db.Date)                 # 公开日
    grant_date = db.Column(db.Date)                   # 授权日
    description = db.Column(db.Text)                 # 摘要/描述
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'type_name': self.get_type_name(),
            'application_no': self.application_no,
            'registration_no': self.registration_no,
            'applicant': self.applicant,
            'inventor': self.inventor,
            'status': self.status,
            'status_name': self.get_status_name(),
            'application_date': self.application_date.strftime('%Y-%m-%d') if self.application_date else None,
            'publish_date': self.publish_date.strftime('%Y-%m-%d') if self.publish_date else None,
            'grant_date': self.grant_date.strftime('%Y-%m-%d') if self.grant_date else None,
            'description': self.description,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }
    
    def get_type_name(self):
        type_map = {
            'invention': '发明专利',
            'utility': '实用新型',
            'software': '软件著作权'
        }
        return type_map.get(self.type, self.type)
    
    def get_status_name(self):
        status_map = {
            'applied': '已申请',
            'published': '已公开',
            'examining': '审查中',
            'granted': '已授权',
            'rejected': '已驳回',
            'withdrawn': '已撤回'
        }
        return status_map.get(self.status, self.status)
