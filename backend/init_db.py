"""
数据库初始化脚本
用于创建数据库表和初始数据
"""
import os
from datetime import datetime, date, time
from app import create_app
from models import db, User, Event

def init_database():
    """初始化数据库"""
    app = create_app()
    
    with app.app_context():
        # 删除所有表（谨慎使用！）
        print("警告：将删除所有现有数据！")
        confirm = input("确定要继续吗？(yes/no): ")
        
        if confirm.lower() != 'yes':
            print("已取消操作")
            return
        
        print("删除现有表...")
        db.drop_all()
        
        print("创建数据库表...")
        db.create_all()
        
        # 创建管理员用户
        print("创建管理员账户...")
        admin = User(
            username=app.config['ADMIN_USERNAME'],
            email='admin@qd-calendar.com',
            role='admin'
        )
        admin.set_password(app.config['ADMIN_PASSWORD'])
        db.session.add(admin)
        
        # 创建测试用户
        print("创建测试用户...")
        test_user = User(
            username='testuser',
            email='test@example.com',
            role='user'
        )
        test_user.set_password('password123')
        db.session.add(test_user)
        
        db.session.commit()
        
        # 创建示例日程
        print("创建示例日程...")
        
        sample_events = [
            {
                'title': '团队会议',
                'description': '讨论本月工作进展和下月计划',
                'event_date': date(2025, 11, 5),
                'start_time': time(10, 0, 0),
                'end_time': time(11, 30, 0),
                'priority': 'high',
                'status': 'pending'
            },
            {
                'title': '项目评审',
                'description': 'QD日历项目第一阶段评审',
                'event_date': date(2025, 11, 8),
                'start_time': time(14, 0, 0),
                'end_time': time(16, 0, 0),
                'priority': 'high',
                'status': 'in_progress'
            },
            {
                'title': '代码审查',
                'description': '审查前端代码质量',
                'event_date': date(2025, 11, 10),
                'start_time': time(15, 0, 0),
                'end_time': time(16, 0, 0),
                'priority': 'medium',
                'status': 'pending'
            },
            {
                'title': '客户演示',
                'description': '向客户展示日历应用功能',
                'event_date': date(2025, 11, 15),
                'start_time': time(10, 0, 0),
                'end_time': time(11, 0, 0),
                'priority': 'high',
                'status': 'pending'
            },
            {
                'title': '技术分享',
                'description': 'Vue3 Composition API 实践分享',
                'event_date': date(2025, 11, 18),
                'start_time': time(16, 0, 0),
                'end_time': time(17, 0, 0),
                'priority': 'medium',
                'status': 'pending'
            },
            {
                'title': '产品培训',
                'description': '新功能使用培训',
                'event_date': date(2025, 11, 20),
                'start_time': time(14, 0, 0),
                'end_time': time(15, 30, 0),
                'priority': 'medium',
                'status': 'pending'
            },
            {
                'title': '月度总结',
                'description': '本月工作总结和经验分享',
                'event_date': date(2025, 11, 28),
                'start_time': time(15, 0, 0),
                'end_time': time(17, 0, 0),
                'priority': 'medium',
                'status': 'pending'
            },
            {
                'title': '系统维护',
                'description': '服务器例行维护',
                'event_date': date(2025, 11, 12),
                'start_time': time(2, 0, 0),
                'end_time': time(4, 0, 0),
                'priority': 'low',
                'status': 'completed'
            }
        ]
        
        for event_data in sample_events:
            event = Event(
                **event_data,
                created_by=admin.id
            )
            db.session.add(event)
        
        db.session.commit()
        
        print("\n" + "="*50)
        print("数据库初始化完成！")
        print("="*50)
        print(f"\n管理员账户:")
        print(f"  用户名: {admin.username}")
        print(f"  密码: {app.config['ADMIN_PASSWORD']}")
        print(f"\n测试用户:")
        print(f"  用户名: testuser")
        print(f"  密码: password123")
        print(f"\n已创建 {len(sample_events)} 个示例日程")
        print("\n现在可以启动应用并登录查看！")
        print("="*50 + "\n")


if __name__ == '__main__':
    init_database()

