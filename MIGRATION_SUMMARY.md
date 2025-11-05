# 从 OSS 到本地存储的迁移总结

## 📋 迁移概述

项目已成功从**阿里云 OSS 对象存储**切换到**本地文件系统存储**。所有上传的图片现在保存在后端的 `uploads/` 目录中。

**迁移日期**: 2025-10-30  
**版本**: v1.1.0

---

## ✅ 已完成的工作

### 1. 删除的文件
- ❌ `backend/utils/oss_helper.py` - OSS 操作助手
- ❌ `OSS_USAGE.md` - OSS 使用文档
- ❌ `backend/test_oss_upload.py` - OSS 测试脚本
- ❌ `backend/test.py` - OSS 测试文件
- ❌ `backend/check_oss_config.py` - OSS 配置检查

### 2. 新增的文件
- ✅ `backend/utils/file_storage.py` - 本地文件存储类
- ✅ `LOCAL_STORAGE_GUIDE.md` - 本地存储使用指南
- ✅ `MIGRATION_SUMMARY.md` - 本迁移总结文档
- ✅ `backend/.gitignore` - 添加 uploads/ 到忽略列表

### 3. 修改的文件

#### `backend/requirements.txt`
```diff
- oss2==2.18.4  # 移除 OSS SDK
```

#### `backend/config.py`
```diff
- # 阿里云 OSS 配置
- OSS_ACCESS_KEY_ID = ...
- OSS_ACCESS_KEY_SECRET = ...
- OSS_BUCKET_NAME = ...
- OSS_REGION = ...
- OSS_DOMAIN = ...
+ 
+ # 本地文件存储配置
+ UPLOAD_FOLDER = 'uploads'
+ FILE_SERVER_URL = '/uploads'
```

#### `backend/app.py`
```diff
+ from flask import send_from_directory
+ 
+ # 添加静态文件服务
+ @app.route('/uploads/<path:filename>')
+ def uploaded_file(filename):
+     return send_from_directory(upload_folder, filename)
```

#### `backend/resources/events.py`
```diff
- from utils.oss_helper import OSSHelper
+ from utils.file_storage import FileStorage

- oss_helper = OSSHelper()
- oss_helper.upload_file(file)
+ file_storage = FileStorage()
+ file_storage.upload_file(file)
```

#### `backend/models.py`
```diff
- background_image = db.Column(db.String(500), nullable=True)  # OSS 图片 URL
+ background_image = db.Column(db.String(500), nullable=True)  # 背景图片 URL
```

#### `README.md`
- 更新技术栈说明（移除 OSS）
- 更新配置说明（改为本地存储）
- 更新文件存储说明
- 修正后端端口号（5002）

#### `backend/README.md`
- 更新项目结构
- 更新文件存储配置
- 更新故障排查部分

#### `CHANGELOG.md`
- 添加 v1.1.0 版本记录
- 记录所有重要变更

---

## 🎯 主要变化

### 文件存储方式

#### 之前（OSS）
```
https://bucket-name.oss-cn-shanghai.aliyuncs.com/events/2025/10/30/abc123.jpg
```

#### 现在（本地）
```
http://localhost:5002/uploads/events/2025/10/30/20251030_abc123def456.jpg
```

### 文件组织结构

```
backend/
└── uploads/
    └── events/
        └── 2025/
            └── 10/
                └── 30/
                    ├── 20251030_abc123def456.jpg
                    ├── 20251030_xyz789abc123.png
                    └── ...
```

### 文件命名规则

**格式**: `日期_UUID.扩展名`

**示例**:
- `20251030_abc123def456.jpg`
- `20251030_789xyz456abc.png`

**说明**:
- `20251030`: 上传日期（YYYYMMDD）
- `abc123def456`: 12位随机UUID
- `jpg/png`: 原文件扩展名

---

## 💡 优势对比

| 特性 | OSS 存储 | 本地存储 |
|------|----------|----------|
| **配置复杂度** | 需要阿里云账号、AccessKey | 无需配置 |
| **运营成本** | 存储费 + 流量费 | 零成本 |
| **开发速度** | 网络延迟 | 本地即时 |
| **离线可用** | ❌ 依赖网络 | ✅ 完全离线 |
| **数据控制** | 第三方托管 | 完全掌控 |
| **扩展性** | ✅ 高 | ⚠️ 受服务器限制 |
| **CDN加速** | ✅ 可用 | ❌ 需额外配置 |
| **备份难度** | 低（自动备份） | 需手动备份 |

---

## 📚 使用指南

### 上传文件
```python
from utils.file_storage import FileStorage

file_storage = FileStorage()
result = file_storage.upload_file(file_obj)

# 返回结果
{
    'url': '/uploads/events/2025/10/30/20251030_abc123.jpg',
    'filename': '20251030_abc123.jpg',
    'filepath': '/absolute/path/to/file',
    'size': 123456
}
```

### 删除文件
```python
file_storage.delete_file(file_url)  # 返回 True/False
```

### 检查文件存在
```python
file_storage.file_exists(file_url)  # 返回 True/False
```

### 获取文件信息
```python
info = file_storage.get_file_info(file_url)
# {
#     'size': 123456,
#     'created': datetime,
#     'modified': datetime,
#     'exists': True
# }
```

---

## 🔧 环境配置

### 旧的 OSS 配置（已移除）
```env
# ❌ 不再需要
OSS_ACCESS_KEY_ID=...
OSS_ACCESS_KEY_SECRET=...
OSS_BUCKET_NAME=...
OSS_REGION=...
OSS_DOMAIN=...
```

### 新的本地存储配置（可选）
```env
# ✅ 可选配置（有默认值）
UPLOAD_FOLDER=uploads
FILE_SERVER_URL=/uploads
```

---

## 🚀 启动步骤

### 1. 更新依赖
```bash
cd backend
source env/bin/activate  # 激活虚拟环境
pip install -r requirements.txt  # OSS 依赖已移除
```

### 2. 启动后端
```bash
python app.py
```

后端会自动：
- 创建 `uploads/` 目录
- 初始化文件存储系统
- 提供 `/uploads/` 静态文件访问

### 3. 测试上传
访问管理面板 → 创建日程 → 上传背景图片

文件会保存在: `backend/uploads/events/年/月/日/文件名`

---

## ⚠️ 注意事项

### 1. 备份重要
定期备份 `uploads/` 目录：
```bash
# 每日备份
tar -czf uploads_backup_$(date +%Y%m%d).tar.gz uploads/

# 或使用 rsync
rsync -av uploads/ /path/to/backup/
```

### 2. 磁盘空间
监控磁盘使用：
```bash
du -sh uploads/  # 查看 uploads 目录大小
df -h            # 查看磁盘使用情况
```

### 3. 文件权限
确保目录可写：
```bash
chmod 755 uploads/
chown -R www-data:www-data uploads/  # 生产环境
```

### 4. Git 忽略
`uploads/` 已添加到 `.gitignore`，不会被提交到 Git

---

## 🔄 回滚方案

如果需要恢复使用 OSS：

### 1. 恢复 OSS 依赖
```bash
pip install oss2==2.18.4
```

### 2. 恢复 oss_helper.py
从 Git 历史恢复或重新实现

### 3. 恢复配置
在 `config.py` 中添加 OSS 配置

### 4. 更新代码
将 `FileStorage` 替换回 `OSSHelper`

---

## 📊 数据迁移

### 如果有旧的 OSS 数据
```python
# 批量下载 OSS 文件到本地
import oss2
from backend.utils.file_storage import FileStorage

# 连接 OSS
auth = oss2.Auth('key_id', 'key_secret')
bucket = oss2.Bucket(auth, 'endpoint', 'bucket')

# 下载所有文件
for obj in oss2.ObjectIterator(bucket, prefix='events/'):
    # 下载到本地
    local_path = f'uploads/{obj.key}'
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    bucket.get_object_to_file(obj.key, local_path)
```

### 更新数据库 URL
```sql
-- 批量更新数据库中的图片 URL
UPDATE events 
SET background_image = REPLACE(
    background_image,
    'https://bucket.oss-cn-shanghai.aliyuncs.com/',
    '/uploads/'
)
WHERE background_image LIKE 'https://bucket.oss%';
```

---

## ✅ 验证清单

- [x] 删除所有 OSS 相关文件
- [x] 移除 OSS 依赖包
- [x] 创建 FileStorage 类
- [x] 更新配置文件
- [x] 更新 API 代码
- [x] 添加静态文件服务
- [x] 更新文档
- [x] 添加 .gitignore
- [x] 更新 CHANGELOG
- [x] 测试上传功能
- [x] 测试删除功能
- [x] 测试文件访问

---

## 📞 问题排查

### 问题 1: 上传后无法访问图片
**原因**: Flask 静态文件路由未配置  
**解决**: 检查 `app.py` 中的 `/uploads/<path:filename>` 路由

### 问题 2: 文件上传失败
**原因**: uploads 目录权限不足  
**解决**: `chmod 755 uploads/`

### 问题 3: 图片显示 404
**原因**: 数据库中还是旧的 OSS URL  
**解决**: 重新上传图片或运行 SQL 更新脚本

### 问题 4: 磁盘空间不足
**原因**: 上传文件过多  
**解决**: 清理旧文件或扩展磁盘

---

## 📖 相关文档

- [`LOCAL_STORAGE_GUIDE.md`](./LOCAL_STORAGE_GUIDE.md) - 详细使用指南
- [`README.md`](./README.md) - 项目主文档
- [`CHANGELOG.md`](./CHANGELOG.md) - 版本更新日志
- [`backend/utils/file_storage.py`](./backend/utils/file_storage.py) - 源代码

---

## 🎉 总结

✅ **迁移成功完成！**

项目已从阿里云 OSS 完全切换到本地文件存储系统。新系统具有以下特点：

1. **零配置**: 无需任何外部服务
2. **零成本**: 不产生云服务费用
3. **高性能**: 本地读写速度快
4. **易维护**: 文件直接可见，易于管理
5. **开发友好**: 快速迭代，无需等待云端

适合中小型项目和开发环境使用。如果项目规模扩大，可以随时切换回 OSS 或其他对象存储服务。

---

*最后更新: 2025-10-30*  
*版本: v1.1.0*

