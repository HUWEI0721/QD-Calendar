from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_migrate import Migrate
from config import config
from models import db, User
import os


def create_app(config_name='default'):
    """应用工厂函数"""
    app = Flask(__name__)
    
    # 加载配置
    app.config.from_object(config[config_name])
    
    # 初始化扩展
    db.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    jwt = JWTManager(app)
    migrate = Migrate(app, db)
    
    # JWT 错误处理
    @jwt.invalid_token_loader
    def invalid_token_callback(error_string):
        return jsonify({
            'message': 'Token 无效或已过期',
            'error': error_string
        }), 422
    
    @jwt.unauthorized_loader
    def unauthorized_callback(error_string):
        return jsonify({
            'message': '缺少认证 Token',
            'error': error_string
        }), 401
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_data):
        return jsonify({
            'message': 'Token 已过期，请重新登录'
        }), 401
    
    # 注册 API
    api = Api(app, prefix='/api')
    
    # 导入资源
    from resources.auth import (
        RegisterResource, LoginResource, GuestLoginResource,
        RefreshTokenResource, UserProfileResource
    )
    from resources.events import (
        EventListResource, EventDetailResource,
        EventCalendarResource, ImageUploadResource, UpcomingEventsResource
    )
    from resources.members import (
        MemberListResource, MemberDetailResource, MemberStatsResource
    )
    from resources.analytics import (
        AnalyticsOverviewResource, AnalyticsEventsResource, AnalyticsMembersResource
    )
    
    # 认证相关路由
    api.add_resource(RegisterResource, '/auth/register')
    api.add_resource(LoginResource, '/auth/login')
    api.add_resource(GuestLoginResource, '/auth/guest-login')
    api.add_resource(RefreshTokenResource, '/auth/refresh')
    api.add_resource(UserProfileResource, '/auth/profile')
    
    # 日程相关路由
    api.add_resource(EventListResource, '/events')
    api.add_resource(EventDetailResource, '/events/<int:event_id>')
    api.add_resource(EventCalendarResource, '/calendar')
    api.add_resource(ImageUploadResource, '/upload/image')
    api.add_resource(UpcomingEventsResource, '/events/upcoming')
    
    # 人员管理路由
    api.add_resource(MemberListResource, '/members')
    api.add_resource(MemberDetailResource, '/members/<int:member_id>')
    api.add_resource(MemberStatsResource, '/members/stats')
    
    # 数据分析路由
    api.add_resource(AnalyticsOverviewResource, '/analytics/overview')
    api.add_resource(AnalyticsEventsResource, '/analytics/events')
    api.add_resource(AnalyticsMembersResource, '/analytics/members')
    
    # 错误处理
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'message': '资源不存在'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'message': '服务器内部错误'}), 500
    
    # 健康检查
    @app.route('/api/health')
    def health_check():
        return jsonify({'status': 'ok', 'message': 'QD-Calendar API is running'}), 200
    
    # 静态文件服务 - 提供上传的图片访问
    @app.route('/uploads/<path:filename>')
    def uploaded_file(filename):
        """提供上传文件的访问"""
        upload_folder = app.config['UPLOAD_FOLDER']
        # 如果是相对路径，转换为绝对路径
        if not os.path.isabs(upload_folder):
            backend_dir = os.path.dirname(os.path.abspath(__file__))
            upload_folder = os.path.join(backend_dir, upload_folder)
        
        return send_from_directory(upload_folder, filename)
    
    # 创建数据库表和初始管理员用户
    with app.app_context():
        db.create_all()
        
        # 检查是否存在管理员账户
        admin = User.query.filter_by(role='admin').first()
        if not admin:
            admin_username = app.config['ADMIN_USERNAME']
            admin_password = app.config['ADMIN_PASSWORD']
            
            admin = User(username=admin_username, role='admin', email='admin@qd-calendar.com')
            admin.set_password(admin_password)
            
            try:
                db.session.add(admin)
                db.session.commit()
                app.logger.info(f"初始管理员账户已创建: {admin_username}")
            except Exception as e:
                db.session.rollback()
                app.logger.error(f"创建管理员账户失败: {str(e)}")
    
    return app


if __name__ == '__main__':
    # 从环境变量获取配置名称
    config_name = os.getenv('FLASK_ENV', 'development')
    app = create_app(config_name)
    app.run(host='0.0.0.0', port=5002, debug=True)

