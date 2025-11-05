from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from models import db, User


class RegisterResource(Resource):
    """用户注册"""
    
    def post(self):
        data = request.get_json()
        
        if not data or not data.get('username') or not data.get('password'):
            return {'message': '用户名和密码不能为空'}, 400
        
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        
        # 检查用户名是否已存在
        if User.query.filter_by(username=username).first():
            return {'message': '用户名已存在'}, 400
        
        # 检查邮箱是否已存在
        if email and User.query.filter_by(email=email).first():
            return {'message': '邮箱已被使用'}, 400
        
        # 创建新用户（默认为普通用户）
        user = User(username=username, email=email, role='user')
        user.set_password(password)
        
        try:
            db.session.add(user)
            db.session.commit()
            return {
                'message': '注册成功',
                'user': user.to_dict()
            }, 201
        except Exception as e:
            db.session.rollback()
            return {'message': f'注册失败: {str(e)}'}, 500


class LoginResource(Resource):
    """用户登录"""
    
    def post(self):
        data = request.get_json()
        
        if not data or not data.get('username') or not data.get('password'):
            return {'message': '用户名和密码不能为空'}, 400
        
        username = data.get('username')
        password = data.get('password')
        
        # 查找用户
        user = User.query.filter_by(username=username).first()
        
        if not user or not user.check_password(password):
            return {'message': '用户名或密码错误'}, 401
        
        # 创建访问令牌（identity 必须是字符串）
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))
        
        return {
            'message': '登录成功',
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': user.to_dict()
        }, 200


class GuestLoginResource(Resource):
    """游客登录（无需认证）"""
    
    def post(self):
        # 创建或获取游客账户
        guest_username = f"guest_{request.remote_addr}"
        user = User.query.filter_by(username=guest_username).first()
        
        if not user:
            user = User(username=guest_username, role='guest')
            user.set_password('guest_password')  # 游客使用默认密码
            try:
                db.session.add(user)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return {'message': f'创建游客账户失败: {str(e)}'}, 500
        
        # 创建访问令牌（identity 必须是字符串）
        access_token = create_access_token(identity=str(user.id))
        
        return {
            'message': '游客登录成功',
            'access_token': access_token,
            'user': user.to_dict()
        }, 200


class RefreshTokenResource(Resource):
    """刷新访问令牌"""
    
    @jwt_required(refresh=True)
    def post(self):
        current_user_id = get_jwt_identity()
        # current_user_id 已经是字符串，直接使用
        new_access_token = create_access_token(identity=current_user_id)
        
        return {
            'access_token': new_access_token
        }, 200


class UserProfileResource(Resource):
    """用户资料"""
    
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        # current_user_id 是字符串，需要转换为整数
        user = User.query.get(int(current_user_id))
        
        if not user:
            return {'message': '用户不存在'}, 404
        
        return user.to_dict(), 200

