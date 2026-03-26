from app.appModels.PatentModel import PatentModel
from app import db
from datetime import datetime

class PatentService:
    """专利/软著管理服务"""
    
    def get_all_patents(self, page=1, per_page=20, keyword='', status='', patent_type=''):
        """获取专利列表"""
        query = PatentModel.query
        
        if keyword:
            query = query.filter(
                db.or_(
                    PatentModel.name.like(f'%{keyword}%'),
                    PatentModel.applicant.like(f'%{keyword}%'),
                    PatentModel.application_no.like(f'%{keyword}%')
                )
            )
        
        if status:
            query = query.filter(PatentModel.status == status)
        
        if patent_type:
            query = query.filter(PatentModel.type == patent_type)
        
        query = query.order_by(PatentModel.created_at.desc())
        
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return {
            'items': [p.to_dict() for p in pagination.items],
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page
        }
    
    def get_patent_by_id(self, patent_id):
        """根据ID获取专利"""
        patent = PatentModel.query.get(patent_id)
        return patent.to_dict() if patent else None
    
    def create_patent(self, data):
        """创建专利记录"""
        try:
            patent = PatentModel(
                name=data.get('name'),
                type=data.get('type', 'invention'),
                application_no=data.get('application_no'),
                registration_no=data.get('registration_no'),
                applicant=data.get('applicant'),
                inventor=data.get('inventor'),
                status=data.get('status', 'applied'),
                application_date=datetime.strptime(data['application_date'], '%Y-%m-%d').date() if data.get('application_date') else None,
                publish_date=datetime.strptime(data['publish_date'], '%Y-%m-%d').date() if data.get('publish_date') else None,
                grant_date=datetime.strptime(data['grant_date'], '%Y-%m-%d').date() if data.get('grant_date') else None,
                description=data.get('description'),
                created_by=data.get('created_by')
            )
            db.session.add(patent)
            db.session.commit()
            return {'success': True, 'id': patent.id}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'message': str(e)}
    
    def update_patent(self, patent_id, data):
        """更新专利记录"""
        try:
            patent = PatentModel.query.get(patent_id)
            if not patent:
                return {'success': False, 'message': '专利不存在'}
            
            for key, value in data.items():
                if hasattr(patent, key) and key not in ['id', 'created_at']:
                    if key in ['application_date', 'publish_date', 'grant_date'] and value:
                        setattr(patent, key, datetime.strptime(value, '%Y-%m-%d').date())
                    elif key not in ['created_by']:
                        setattr(patent, key, value)
            
            db.session.commit()
            return {'success': True}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'message': str(e)}
    
    def delete_patent(self, patent_id):
        """删除专利记录"""
        try:
            patent = PatentModel.query.get(patent_id)
            if not patent:
                return {'success': False, 'message': '专利不存在'}
            
            db.session.delete(patent)
            db.session.commit()
            return {'success': True}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'message': str(e)}
    
    def get_statistics(self):
        """获取统计信息"""
        total = PatentModel.query.count()
        by_type = db.session.query(
            PatentModel.type, 
            db.func.count(PatentModel.id)
        ).group_by(PatentModel.type).all()
        
        by_status = db.session.query(
            PatentModel.status,
            db.func.count(PatentModel.id)
        ).group_by(PatentModel.status).all()
        
        return {
            'total': total,
            'by_type': {t: c for t, c in by_type},
            'by_status': {s: c for s, c in by_status}
        }
