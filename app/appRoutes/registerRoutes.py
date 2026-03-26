from flask import Blueprint, request
from app.appService.UserService import UserServiceImpl
from app.utils.ResponseForm import ResponseForm

register_bp = Blueprint('register', __name__)
user_service = UserServiceImpl()

@register_bp.route('/register', methods=['POST'])
def register():
    '''用户注册'''
    data = request.get_json()
    
    # 验证参数
    required_fields = ['username', 'email', 'password', 'confirm_password']
    for field in required_fields:
        if field not in data or not data[field]:
            return ResponseForm.error(f'请提供{field}')
    
    # 验证密码一致性
    if data['password'] != data['confirm_password']:
        return ResponseForm.error('两次输入的密码不一致')
    
    # 调用服务层注册
    result = user_service.register_user(
        data['username'],
        data['email'],
        data['password']
    )
    
    if result['success']:
        return ResponseForm.success('注册成功')
    else:
        return ResponseForm.error(result['message'])
