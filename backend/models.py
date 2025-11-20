from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
    """用户模型"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('admin', 'user', 'guest'), default='user', nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    events = db.relationship('Event', backref='creator', lazy='dynamic', cascade='all, delete-orphan')
    
    def set_password(self, password):
        """设置密码（哈希）"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """验证密码"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'username': self.username,
            'role': self.role,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<User {self.username}>'


class Member(db.Model):
    """人员模型"""
    __tablename__ = 'members'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    department = db.Column(db.String(100), nullable=True)
    position = db.Column(db.String(100), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系会在关联表定义后添加
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'email': self.email,
            'department': self.department,
            'position': self.position,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Member {self.name}>'


# 事件参与者关联表（多对多关系）
event_members = db.Table('event_members',
    db.Column('event_id', db.Integer, db.ForeignKey('events.id', ondelete='CASCADE'), primary_key=True),
    db.Column('member_id', db.Integer, db.ForeignKey('members.id', ondelete='CASCADE'), primary_key=True),
    db.Column('created_at', db.DateTime, default=datetime.utcnow)
)


class Event(db.Model):
    """日程事件模型"""
    __tablename__ = 'events'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    event_date = db.Column(db.Date, nullable=False, index=True)
    start_time = db.Column(db.Time, nullable=True)
    end_time = db.Column(db.Time, nullable=True)
    background_image = db.Column(db.String(500), nullable=True)  # 背景图片 URL
    priority = db.Column(db.Enum('low', 'medium', 'high'), default='medium')
    status = db.Column(db.Enum('pending', 'in_progress', 'completed', 'cancelled'), default='pending')
    
    # 新增字段
    organizer_department = db.Column(db.String(100), nullable=True)  # 举办部门
    expected_participants = db.Column(db.Integer, nullable=True)  # 预计参与人数
    location = db.Column(db.String(200), nullable=True)  # 活动地点
    
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系：参与该事件的人员
    members = db.relationship('Member', secondary=event_members, backref='events', lazy='dynamic')
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'event_date': self.event_date.isoformat() if self.event_date else None,
            'start_time': self.start_time.strftime('%H:%M:%S') if self.start_time else None,
            'end_time': self.end_time.strftime('%H:%M:%S') if self.end_time else None,
            'background_image': self.background_image,
            'priority': self.priority,
            'status': self.status,
            'organizer_department': self.organizer_department,  # 新增
            'expected_participants': self.expected_participants,  # 新增
            'location': self.location,  # 新增
            'participant_count': self.members.count(),  # 实时计算参与人数
            'created_by': self.created_by,
            'creator_name': self.creator.username if self.creator else None,
            'members': [{'id': m.id, 'name': m.name} for m in self.members.all()],  # 参与人员列表
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def to_summary_dict(self):
        """转换为简要字典（用于日历视图）"""
        return {
            'id': self.id,
            'title': self.title,
            'event_date': self.event_date.isoformat() if self.event_date else None,
            'start_time': self.start_time.strftime('%H:%M') if self.start_time else None,
            'priority': self.priority,
            'status': self.status,
            'background_image': self.background_image,
            'organizer_department': self.organizer_department,
            'location': self.location,
            'expected_participants': self.expected_participants
        }
    
    def __repr__(self):
        return f'<Event {self.title} on {self.event_date}>'

