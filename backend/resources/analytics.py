"""
数据分析 API 资源
"""
from flask import request, current_app
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from models import db, Event, Member, event_members
from datetime import datetime, timedelta
from sqlalchemy import func, extract


class AnalyticsOverviewResource(Resource):
    """数据分析总览"""
    
    @jwt_required()
    def get(self):
        """获取数据分析总览"""
        try:
            # 获取查询参数
            year = request.args.get('year', datetime.now().year, type=int)
            month = request.args.get('month', datetime.now().month, type=int)
            
            # 计算月份的起止日期
            start_date = datetime(year, month, 1).date()
            if month == 12:
                end_date = datetime(year + 1, 1, 1).date()
            else:
                end_date = datetime(year, month + 1, 1).date()
            
            # 1. 本月活动总数
            total_events = Event.query.filter(
                Event.event_date >= start_date,
                Event.event_date < end_date
            ).count()
            
            # 2. 本月已完成活动数
            completed_events = Event.query.filter(
                Event.event_date >= start_date,
                Event.event_date < end_date,
                Event.status == 'completed'
            ).count()
            
            # 3. 本月活动参与总人次
            total_participants = db.session.query(
                func.count(event_members.c.member_id)
            ).join(
                Event, Event.id == event_members.c.event_id
            ).filter(
                Event.event_date >= start_date,
                Event.event_date < end_date
            ).scalar() or 0
            
            # 4. 本月活动覆盖人数（去重）
            unique_participants = db.session.query(
                func.count(func.distinct(event_members.c.member_id))
            ).join(
                Event, Event.id == event_members.c.event_id
            ).filter(
                Event.event_date >= start_date,
                Event.event_date < end_date
            ).scalar() or 0
            
            # 5. 按状态统计
            status_stats = db.session.query(
                Event.status,
                func.count(Event.id).label('count')
            ).filter(
                Event.event_date >= start_date,
                Event.event_date < end_date
            ).group_by(Event.status).all()
            
            # 6. 按优先级统计
            priority_stats = db.session.query(
                Event.priority,
                func.count(Event.id).label('count')
            ).filter(
                Event.event_date >= start_date,
                Event.event_date < end_date
            ).group_by(Event.priority).all()
            
            # 7. 每日活动数量趋势
            daily_stats = db.session.query(
                Event.event_date,
                func.count(Event.id).label('count')
            ).filter(
                Event.event_date >= start_date,
                Event.event_date < end_date
            ).group_by(Event.event_date).order_by(Event.event_date).all()
            
            return {
                'period': {
                    'year': year,
                    'month': month,
                    'start_date': start_date.isoformat(),
                    'end_date': (end_date - timedelta(days=1)).isoformat()
                },
                'overview': {
                    'total_events': total_events,
                    'completed_events': completed_events,
                    'completion_rate': round(completed_events / total_events * 100, 1) if total_events > 0 else 0,
                    'total_participants': total_participants,
                    'unique_participants': unique_participants,
                    'avg_participants_per_event': round(total_participants / total_events, 1) if total_events > 0 else 0
                },
                'status_distribution': [
                    {'status': status, 'count': count, 'label': get_status_label(status)}
                    for status, count in status_stats
                ],
                'priority_distribution': [
                    {'priority': priority, 'count': count, 'label': get_priority_label(priority)}
                    for priority, count in priority_stats
                ],
                'daily_trend': [
                    {'date': date.isoformat(), 'count': count}
                    for date, count in daily_stats
                ]
            }, 200
            
        except Exception as e:
            current_app.logger.error(f"获取数据分析总览失败: {str(e)}")
            import traceback
            current_app.logger.error(traceback.format_exc())
            return {'message': '获取数据分析失败'}, 500


class AnalyticsEventsResource(Resource):
    """活动详细分析"""
    
    @jwt_required()
    def get(self):
        """获取活动详细分析"""
        try:
            # 获取查询参数
            year = request.args.get('year', datetime.now().year, type=int)
            month = request.args.get('month', datetime.now().month, type=int)
            
            # 计算月份的起止日期
            start_date = datetime(year, month, 1).date()
            if month == 12:
                end_date = datetime(year + 1, 1, 1).date()
            else:
                end_date = datetime(year, month + 1, 1).date()
            
            # 获取活动列表及其参与人数
            events = Event.query.filter(
                Event.event_date >= start_date,
                Event.event_date < end_date
            ).order_by(Event.event_date.desc()).all()
            
            events_data = []
            for event in events:
                participant_count = event.members.count()
                events_data.append({
                    'id': event.id,
                    'title': event.title,
                    'event_date': event.event_date.isoformat(),
                    'start_time': event.start_time.strftime('%H:%M') if event.start_time else None,
                    'status': event.status,
                    'priority': event.priority,
                    'participant_count': participant_count,
                    'creator_name': event.creator.username if event.creator else None
                })
            
            # 参与人数 TOP 5 活动
            top_events = sorted(events_data, key=lambda x: x['participant_count'], reverse=True)[:5]
            
            return {
                'events': events_data,
                'top_events': top_events,
                'total': len(events_data)
            }, 200
            
        except Exception as e:
            current_app.logger.error(f"获取活动详细分析失败: {str(e)}")
            return {'message': '获取活动详细分析失败'}, 500


class AnalyticsMembersResource(Resource):
    """人员参与分析"""
    
    @jwt_required()
    def get(self):
        """获取人员参与分析"""
        try:
            # 获取查询参数
            year = request.args.get('year', datetime.now().year, type=int)
            month = request.args.get('month', datetime.now().month, type=int)
            
            # 计算月份的起止日期
            start_date = datetime(year, month, 1).date()
            if month == 12:
                end_date = datetime(year + 1, 1, 1).date()
            else:
                end_date = datetime(year, month + 1, 1).date()
            
            # 统计各人员的参与次数
            member_stats = db.session.query(
                Member.id,
                Member.name,
                Member.department,
                func.count(event_members.c.event_id).label('event_count')
            ).join(
                event_members, Member.id == event_members.c.member_id
            ).join(
                Event, Event.id == event_members.c.event_id
            ).filter(
                Event.event_date >= start_date,
                Event.event_date < end_date
            ).group_by(
                Member.id, Member.name, Member.department
            ).order_by(
                func.count(event_members.c.event_id).desc()
            ).all()
            
            # 按部门统计参与情况
            department_stats = db.session.query(
                Member.department,
                func.count(func.distinct(Member.id)).label('member_count'),
                func.count(event_members.c.event_id).label('event_count')
            ).join(
                event_members, Member.id == event_members.c.member_id
            ).join(
                Event, Event.id == event_members.c.event_id
            ).filter(
                Event.event_date >= start_date,
                Event.event_date < end_date,
                Member.department.isnot(None)
            ).group_by(
                Member.department
            ).all()
            
            return {
                'member_participation': [
                    {
                        'member_id': member_id,
                        'name': name,
                        'department': department,
                        'event_count': event_count
                    }
                    for member_id, name, department, event_count in member_stats
                ],
                'department_participation': [
                    {
                        'department': dept,
                        'member_count': member_count,
                        'event_count': event_count,
                        'avg_events_per_member': round(event_count / member_count, 1) if member_count > 0 else 0
                    }
                    for dept, member_count, event_count in department_stats
                ],
                'top_participants': [
                    {
                        'member_id': member_id,
                        'name': name,
                        'department': department,
                        'event_count': event_count
                    }
                    for member_id, name, department, event_count in member_stats[:10]
                ]
            }, 200
            
        except Exception as e:
            current_app.logger.error(f"获取人员参与分析失败: {str(e)}")
            import traceback
            current_app.logger.error(traceback.format_exc())
            return {'message': '获取人员参与分析失败'}, 500


def get_status_label(status):
    """获取状态标签"""
    labels = {
        'pending': '待处理',
        'in_progress': '进行中',
        'completed': '已完成',
        'cancelled': '已取消'
    }
    return labels.get(status, status)


def get_priority_label(priority):
    """获取优先级标签"""
    labels = {
        'high': '高',
        'medium': '中',
        'low': '低'
    }
    return labels.get(priority, priority)

