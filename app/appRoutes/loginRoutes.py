from flask import Blueprint, request, session, render_template
from app.appService.UserService import UserServiceImpl
from app.utils.ResponseForm import ResponseForm

login_bp = Blueprint('login', __name__)
user_service = UserServiceImpl()

@login_bp.route('/', methods=['POST'])
def html_main():
    return render_template('main.html')

@login_bp.route('/login', methods=['POST'])
def login():
    '''用户登录'''
    data = request.get_json()
    
    # 验证参数
    if not data or 'username' not in data or 'password' not in data:
        return ResponseForm.error('请提供用户名和密码')
    
    username = data['username']
    password = data['password']
    
    # 调用服务层验证
    result = user_service.login_user(username, password)
    
    if result['success']:
        # 设置会话
        session['user_id'] = result['user_id']
        session['username'] = username
        session['role'] = result['role']
        
        return ResponseForm.success('登录成功', {
            'user_id': result['user_id'],
            'username': username,
            'role': result['role']
        })
    else:
        return ResponseForm.error(result['message'])
