from app.appModels.UserModel import UserModel
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class UserServiceImpl:
    
    def login_user(self, username: str, password: str) -> dict:
        '''用户登录验证'''
        user = UserModel.query.filter_by(username=username).first()
        
        if not user:
            # 尝试用邮箱登录
            user = UserModel.query.filter_by(email=username).first()
            if not user:
                return {'success': False, 'message': '用户不存在'}
        
        # 验证密码
        if check_password_hash(user.password_hash, password):
            return {
                'success': True,
                'user_id': user.id,
                'role': user.role
            }
        else:
            return {'success': False, 'message': '密码错误'}
    
    def register_user(self, username: str, email: str, password: str) -> dict:
        '''用户注册'''
        # 检查用户名是否已存在
        if UserModel.query.filter_by(username=username).first():
            return {'success': False, 'message': '用户名已存在'}
        
        # 检查邮箱是否已存在
        if UserModel.query.filter_by(email=email).first():
            return {'success': False, 'message': '邮箱已注册'}
        
        # 检查密码强度（简单检查）
        if len(password) < 6:
            return {'success': False, 'message': '密码长度至少6位'}
        
        try:
            # 创建用户
            new_user = UserModel(
                username=username,
                email=email,
                password_hash=generate_password_hash(password),
                role='student'  # 默认为学生
            )
            
            db.session.add(new_user)
            db.session.commit()
            
            return {'success': True}
            
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'message': f'注册失败: {str(e)}'}
