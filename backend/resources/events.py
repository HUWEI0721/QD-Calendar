from flask import request, current_app
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, date
from models import db, Event, User, Member
from utils.file_storage import FileStorage, allowed_file
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


class EventListResource(Resource):
    """日程列表资源"""
    
    @jwt_required(optional=True)
    def get(self):
        """获取日程列表（所有用户可见）"""
        # 获取查询参数
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        status = request.args.get('status')
        priority = request.args.get('priority')
        
        query = Event.query
        
        # 按日期过滤
        if start_date:
            try:
                start = datetime.strptime(start_date, '%Y-%m-%d').date()
                query = query.filter(Event.event_date >= start)
            except ValueError:
                pass
        
        if end_date:
            try:
                end = datetime.strptime(end_date, '%Y-%m-%d').date()
                query = query.filter(Event.event_date <= end)
            except ValueError:
                pass
        
        # 按状态过滤
        if status and status in ['pending', 'in_progress', 'completed', 'cancelled']:
            query = query.filter(Event.status == status)
        
        # 按优先级过滤
        if priority and priority in ['low', 'medium', 'high']:
            query = query.filter(Event.priority == priority)
        
        # 排序
        query = query.order_by(Event.event_date.asc(), Event.start_time.asc())
        
        events = query.all()
        return {
            'events': [event.to_dict() for event in events],
            'count': len(events)
        }, 200
    
    @admin_required
    def post(self):
        """创建新日程（仅管理员）"""
        current_user_id = get_jwt_identity()
        # current_user_id 是字符串，需要转换为整数
        current_user_id = int(current_user_id)
        data = request.get_json()
        
        if not data or not data.get('title') or not data.get('event_date'):
            return {'message': '标题和日期不能为空'}, 400
        
        # 验证必填字段：背景图片、地点、部门
        if not data.get('background_image'):
            return {'message': '活动海报（背景图片）不能为空，请上传图片'}, 400
        
        if not data.get('location'):
            return {'message': '活动地点不能为空'}, 400
        
        if not data.get('organizer_department'):
            return {'message': '举办部门不能为空'}, 400
        
        try:
            # 解析日期
            event_date = datetime.strptime(data['event_date'], '%Y-%m-%d').date()
            
            # 解析时间（可选）
            start_time = None
            end_time = None
            
            if data.get('start_time'):
                start_time = datetime.strptime(data['start_time'], '%H:%M:%S').time()
            
            if data.get('end_time'):
                end_time = datetime.strptime(data['end_time'], '%H:%M:%S').time()
            
            # 创建日程
            event = Event(
                title=data['title'],
                description=data.get('description', ''),
                event_date=event_date,
                start_time=start_time,
                end_time=end_time,
                background_image=data.get('background_image'),
                priority=data.get('priority', 'medium'),
                status=data.get('status', 'pending'),
                organizer_department=data.get('organizer_department'),  # 新增
                expected_participants=data.get('expected_participants'),  # 新增
                location=data.get('location'),  # 新增
                created_by=current_user_id
            )
            
            db.session.add(event)
            db.session.flush()  # 获取event.id
            
            # 添加参与人员
            if data.get('member_ids'):
                member_ids = data['member_ids']
                members = Member.query.filter(Member.id.in_(member_ids)).all()
                for member in members:
                    event.members.append(member)
            
            db.session.commit()
            
            return {
                'message': '日程创建成功',
                'event': event.to_dict()
            }, 201
            
        except ValueError as e:
            return {'message': f'日期或时间格式错误: {str(e)}'}, 400
        except Exception as e:
            db.session.rollback()
            return {'message': f'创建日程失败: {str(e)}'}, 500


class EventDetailResource(Resource):
    """日程详情资源"""
    
    @jwt_required(optional=True)
    def get(self, event_id):
        """获取日程详情（所有用户可见）"""
        event = Event.query.get(event_id)
        
        if not event:
            return {'message': '日程不存在'}, 404
        
        return event.to_dict(), 200
    
    @admin_required
    def put(self, event_id):
        """更新日程（仅管理员）"""
        event = Event.query.get(event_id)
        
        if not event:
            return {'message': '日程不存在'}, 404
        
        data = request.get_json()
        
        try:
            # 更新字段
            if 'title' in data:
                event.title = data['title']
            
            if 'description' in data:
                event.description = data['description']
            
            if 'event_date' in data:
                event.event_date = datetime.strptime(data['event_date'], '%Y-%m-%d').date()
            
            if 'start_time' in data:
                event.start_time = datetime.strptime(data['start_time'], '%H:%M:%S').time() if data['start_time'] else None
            
            if 'end_time' in data:
                event.end_time = datetime.strptime(data['end_time'], '%H:%M:%S').time() if data['end_time'] else None
            
            if 'background_image' in data:
                event.background_image = data['background_image']
            
            if 'priority' in data and data['priority'] in ['low', 'medium', 'high']:
                event.priority = data['priority']
            
            if 'status' in data and data['status'] in ['pending', 'in_progress', 'completed', 'cancelled']:
                event.status = data['status']
            
            # 新增字段更新
            if 'organizer_department' in data:
                event.organizer_department = data['organizer_department']
            
            if 'expected_participants' in data:
                event.expected_participants = data['expected_participants']
            
            if 'location' in data:
                event.location = data['location']
            
            # 更新参与人员
            if 'member_ids' in data:
                # 清空现有人员
                event.members.delete()
                # 添加新人员
                member_ids = data['member_ids']
                if member_ids:
                    members = Member.query.filter(Member.id.in_(member_ids)).all()
                    for member in members:
                        event.members.append(member)
            
            db.session.commit()
            
            return {
                'message': '日程更新成功',
                'event': event.to_dict()
            }, 200
            
        except ValueError as e:
            return {'message': f'日期或时间格式错误: {str(e)}'}, 400
        except Exception as e:
            db.session.rollback()
            return {'message': f'更新日程失败: {str(e)}'}, 500
    
    @admin_required
    def delete(self, event_id):
        """删除日程（仅管理员）"""
        event = Event.query.get(event_id)
        
        if not event:
            return {'message': '日程不存在'}, 404
        
        try:
            # 如果有背景图片，尝试删除本地文件
            if event.background_image:
                file_storage = FileStorage()
                file_storage.delete_file(event.background_image)
            
            db.session.delete(event)
            db.session.commit()
            
            return {'message': '日程删除成功'}, 200
            
        except Exception as e:
            db.session.rollback()
            return {'message': f'删除日程失败: {str(e)}'}, 500


class EventCalendarResource(Resource):
    """日历视图资源"""
    
    @jwt_required(optional=True)
    def get(self):
        """获取月历数据"""
        year = request.args.get('year', type=int)
        month = request.args.get('month', type=int)
        
        if not year or not month:
            # 默认使用当前月
            today = date.today()
            year = today.year
            month = today.month
        
        # 获取该月所有日程
        start_date = date(year, month, 1)
        
        if month == 12:
            end_date = date(year + 1, 1, 1)
        else:
            end_date = date(year, month + 1, 1)
        
        events = Event.query.filter(
            Event.event_date >= start_date,
            Event.event_date < end_date
        ).order_by(Event.event_date.asc(), Event.start_time.asc()).all()
        
        # 按日期分组
        calendar_data = {}
        for event in events:
            date_key = event.event_date.isoformat()
            if date_key not in calendar_data:
                calendar_data[date_key] = []
            calendar_data[date_key].append(event.to_summary_dict())
        
        return {
            'year': year,
            'month': month,
            'calendar': calendar_data
        }, 200


class ImageUploadResource(Resource):
    """图片上传资源"""
    
    @admin_required
    def post(self):
        """上传图片到本地存储（仅管理员）"""
        if 'file' not in request.files:
            return {'message': '没有文件上传'}, 400
        
        file = request.files['file']
        
        if file.filename == '':
            return {'message': '文件名不能为空'}, 400
        
        if not allowed_file(file.filename):
            allowed_exts = ', '.join(current_app.config['ALLOWED_EXTENSIONS'])
            return {'message': f'不支持的文件格式，允许的格式: {allowed_exts}'}, 400
        
        try:
            file_storage = FileStorage()
            result = file_storage.upload_file(file)
            
            if result:
                return {
                    'message': '图片上传成功',
                    'url': result['url'],
                    'filename': result['filename']
                }, 200
            else:
                return {'message': '图片上传失败'}, 500
                
        except Exception as e:
            current_app.logger.error(f"上传图片时出错: {str(e)}")
            return {'message': f'上传失败: {str(e)}'}, 500


class UpcomingEventsResource(Resource):
    """获取近期活动（用于首页轮播）"""
    
    @jwt_required(optional=True)
    def get(self):
        """获取当天及未来一周内的活动"""
        from datetime import timedelta
        
        today = date.today()
        next_week = today + timedelta(days=7)
        
        # 查询当天及未来7天的活动
        events = Event.query.filter(
            Event.event_date >= today,
            Event.event_date <= next_week,
            Event.status != 'cancelled'  # 排除已取消的活动
        ).order_by(Event.event_date.asc(), Event.start_time.asc()).all()
        
        return {
            'events': [event.to_dict() for event in events],
            'count': len(events),
            'start_date': today.isoformat(),
            'end_date': next_week.isoformat()
        }, 200

