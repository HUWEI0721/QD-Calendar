# -*- coding: utf-8 -*-
"""清除测试活动数据（没有图片的活动）"""
from app import create_app
from models import db, Event

app = create_app()

with app.app_context():
    # 删除所有没有背景图片的活动
    events_without_image = Event.query.filter(
        (Event.background_image == None) | (Event.background_image == '')
    ).all()
    
    print(f"[INFO] Found {len(events_without_image)} events without images")
    
    for event in events_without_image:
        print(f"[DELETE] {event.title} ({event.event_date})")
        db.session.delete(event)
    
    db.session.commit()
    print(f"\n[SUCCESS] Deleted {len(events_without_image)} events without images")
    
    # 显示剩余活动
    remaining = Event.query.all()
    print(f"\n[INFO] Remaining events: {len(remaining)}")
    for e in remaining:
        has_image = "✓" if e.background_image else "✗"
        print(f"  {has_image} {e.title} ({e.event_date})")


