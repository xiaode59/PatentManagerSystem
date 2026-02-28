from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import logging

db = SQLAlchemy()

def setup_logging():
    '''日志配置'''
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/PatentMain.log'),
            logging.StreamHandler()
        ]
    )

def create_app(config_name='development'):
    '''创建Flask应用'''
    app = Flask(__name__, static_folder='HTML', template_folder='HTML')
    
    # 加载配置
    if config_name == 'development':
        from config import DevelopmentConfig
        app.config.from_object(DevelopmentConfig)
    else:
        from config import ProductionConfig
        app.config.from_object(ProductionConfig)
    
    # 初始化扩展
    db.init_app(app)
    CORS(app, supports_credentials=True)
    
    # 设置日志
    setup_logging()
    
    # 注册蓝图
    from app.appRoutes.loginRoutes import login_bp
    from app.appRoutes.registerRoutes import register_bp
    
    app.register_blueprint(login_bp, url_prefix='/api')
    app.register_blueprint(register_bp, url_prefix='/api')
    
    # 创建数据库表
    with app.app_context():
        db.create_all()
    
    @app.route('/')
    def index():
        '''首页'''
        return app.send_static_file('index.html')
    
    @app.route('/login')
    def login_page():
        '''登录页面'''
        return app.send_static_file('login.html')
    
    return app
