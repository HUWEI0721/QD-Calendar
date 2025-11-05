"""
人员管理 API 资源
"""
from flask import request, current_app
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Member, User
from functools import wraps


def admin_required(fn):
    """装饰器：要求管理员权限"""
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        current_user_id = get_jwt_identity()
        # current_user_id 是字符串，需要转换为整数
        user = User.query.get(int(current_user_id))
        
        if not user or user.role != 'admin':
            return {'message': '需要管理员权限'}, 403
        
        return fn(*args, **kwargs)
    return wrapper


class MemberListResource(Resource):
    """人员列表资源"""
    
    @jwt_required()
    def get(self):
        """获取人员列表（所有用户可见）"""
        try:
            # 获取查询参数
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 50, type=int)
            is_active = request.args.get('is_active', None, type=str)
            search = request.args.get('search', '', type=str)
            
            # 构建查询
            query = Member.query
            
            # 筛选：是否激活
            if is_active is not None:
                query = query.filter_by(is_active=(is_active.lower() == 'true'))
            
            # 搜索：姓名、部门、职位
            if search:
                search_pattern = f'%{search}%'
                query = query.filter(
                    db.or_(
                        Member.name.like(search_pattern),
                        Member.department.like(search_pattern),
                        Member.position.like(search_pattern)
                    )
                )
            
            # 排序
            query = query.order_by(Member.created_at.desc())
            
            # 分页
            pagination = query.paginate(page=page, per_page=per_page, error_out=False)
            
            return {
                'members': [member.to_dict() for member in pagination.items],
                'total': pagination.total,
                'pages': pagination.pages,
                'current_page': page
            }, 200
            
        except Exception as e:
            current_app.logger.error(f"获取人员列表失败: {str(e)}")
            return {'message': '获取人员列表失败'}, 500
    
    @admin_required
    def post(self):
        """创建新人员（仅管理员）"""
        data = request.get_json()
        
        # 验证必填字段
        if not data.get('name'):
            return {'message': '姓名不能为空'}, 400
        
        try:
            # 创建人员
            member = Member(
                name=data['name'],
                phone=data.get('phone'),
                email=data.get('email'),
                department=data.get('department'),
                position=data.get('position'),
                is_active=data.get('is_active', True)
            )
            
            db.session.add(member)
            db.session.commit()
            
            return {
                'message': '人员创建成功',
                'member': member.to_dict()
            }, 201
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"创建人员失败: {str(e)}")
            return {'message': '创建人员失败'}, 500


class MemberDetailResource(Resource):
    """人员详情资源"""
    
    @jwt_required()
    def get(self, member_id):
        """获取人员详情"""
        member = Member.query.get(member_id)
        
        if not member:
            return {'message': '人员不存在'}, 404
        
        # 获取该人员参与的事件数量
        event_count = member.events.count()
        
        member_data = member.to_dict()
        member_data['event_count'] = event_count
        
        return member_data, 200
    
    @admin_required
    def put(self, member_id):
        """更新人员信息（仅管理员）"""
        member = Member.query.get(member_id)
        
        if not member:
            return {'message': '人员不存在'}, 404
        
        data = request.get_json()
        
        try:
            # 更新字段
            if 'name' in data:
                member.name = data['name']
            if 'phone' in data:
                member.phone = data['phone']
            if 'email' in data:
                member.email = data['email']
            if 'department' in data:
                member.department = data['department']
            if 'position' in data:
                member.position = data['position']
            if 'is_active' in data:
                member.is_active = data['is_active']
            
            db.session.commit()
            
            return {
                'message': '人员信息更新成功',
                'member': member.to_dict()
            }, 200
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"更新人员信息失败: {str(e)}")
            return {'message': '更新人员信息失败'}, 500
    
    @admin_required
    def delete(self, member_id):
        """删除人员（仅管理员）"""
        member = Member.query.get(member_id)
        
        if not member:
            return {'message': '人员不存在'}, 404
        
        try:
            db.session.delete(member)
            db.session.commit()
            
            return {'message': '人员删除成功'}, 200
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"删除人员失败: {str(e)}")
            return {'message': '删除人员失败'}, 500


class MemberStatsResource(Resource):
    """人员统计资源"""
    
    @jwt_required()
    def get(self):
        """获取人员统计信息"""
        try:
            total_members = Member.query.filter_by(is_active=True).count()
            inactive_members = Member.query.filter_by(is_active=False).count()
            
            # 按部门统计
            departments = db.session.query(
                Member.department,
                db.func.count(Member.id).label('count')
            ).filter(
                Member.is_active == True,
                Member.department.isnot(None)
            ).group_by(Member.department).all()
            
            return {
                'total_members': total_members,
                'inactive_members': inactive_members,
                'departments': [
                    {'name': dept, 'count': count} 
                    for dept, count in departments
                ]
            }, 200
            
        except Exception as e:
            current_app.logger.error(f"获取人员统计失败: {str(e)}")
            return {'message': '获取人员统计失败'}, 500

