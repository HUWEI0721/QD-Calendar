"""
数据库迁移脚本：为 events 表添加新字段
- organizer_department: 举办部门
- expected_participants: 预计参与人数  
- location: 活动地点

运行方式：
python migrations/add_event_fields.py
"""

import sys
import os

# 添加父目录到路径以便导入
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from sqlalchemy import text

def migrate():
    """执行数据库迁移"""
    app = create_app()
    
    with app.app_context():
        try:
            print("开始执行数据库迁移...")
            
            # 检查字段是否已存在
            result = db.session.execute(text("SHOW COLUMNS FROM events LIKE 'organizer_department'"))
            if result.fetchone():
                print("字段 organizer_department 已存在，跳过")
            else:
                db.session.execute(text("ALTER TABLE events ADD COLUMN organizer_department VARCHAR(100) NULL COMMENT '举办部门'"))
                print("✓ 添加字段: organizer_department")
            
            result = db.session.execute(text("SHOW COLUMNS FROM events LIKE 'expected_participants'"))
            if result.fetchone():
                print("字段 expected_participants 已存在，跳过")
            else:
                db.session.execute(text("ALTER TABLE events ADD COLUMN expected_participants INT NULL COMMENT '预计参与人数'"))
                print("✓ 添加字段: expected_participants")
            
            result = db.session.execute(text("SHOW COLUMNS FROM events LIKE 'location'"))
            if result.fetchone():
                print("字段 location 已存在，跳过")
            else:
                db.session.execute(text("ALTER TABLE events ADD COLUMN location VARCHAR(200) NULL COMMENT '活动地点'"))
                print("✓ 添加字段: location")
            
            db.session.commit()
            print("\n✅ 数据库迁移成功完成！")
            print("\n新增字段说明：")
            print("  - organizer_department: 举办部门 (VARCHAR(100))")
            print("  - expected_participants: 预计参与人数 (INT)")
            print("  - location: 活动地点 (VARCHAR(200))")
            
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ 迁移失败: {str(e)}")
            raise

if __name__ == '__main__':
    migrate()


