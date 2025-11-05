# 本地文件存储指南

## 📋 概述

项目已从阿里云 OSS 存储切换到**本地文件系统存储**，所有上传的图片都保存在后端的 `uploads/` 目录中。

## 🔄 主要变更

### 替换的文件
- ✅ `utils/oss_helper.py` → `utils/file_storage.py`
- ✅ 移除了所有 OSS 相关配置和依赖

### 文件存储结构
```
backend/
├── uploads/              # 上传文件根目录
│   └── events/          # 日程图片文件夹
│       └── 2025/        # 按年份分类
│           └── 10/      # 按月份分类
│               └── 30/  # 按日期分类
│                   ├── 20251030_abc123def456.jpg
│                   ├── 20251030_xyz789abc123.png
│                   └── ...
```

### 文件命名规则
格式：`日期_UUID.扩展名`

示例：
- `20251030_abc123def456.jpg`
- `20251030_xyz789abc123.png`

说明：
- `20251030`：上传日期（YYYYMMDD格式）
- `abc123def456`：12位随机UUID（防止重名）
- `jpg/png`：原始文件扩展名

## 🎯 访问方式

### 图片 URL 格式
```
http://localhost:5002/uploads/events/2025/10/30/20251030_abc123def456.jpg
```

### 前端使用
```vue
<template>
  <div 
    class="background" 
    :style="{ backgroundImage: `url(${event.background_image})` }"
  >
  </div>
</template>
```

或直接使用 img 标签：
```vue
<img :src="event.background_image" alt="背景图" />
```

## ⚙️ 配置说明

### backend/config.py
```python
# 本地文件存储配置
UPLOAD_FOLDER = 'uploads'        # 上传文件夹（相对于 backend 目录）
FILE_SERVER_URL = '/uploads'     # 文件访问 URL 前缀
```

### 环境变量（可选）
在 `.env` 文件中可以自定义：
```env
UPLOAD_FOLDER=uploads
FILE_SERVER_URL=/uploads
```

## 📁 FileStorage 类方法

### 1. upload_file(file_obj, folder='events')
上传文件到本地

**参数**：
- `file_obj`: 文件对象
- `folder`: 子文件夹名称（默认 'events'）

**返回**：
```python
{
    'url': '/uploads/events/2025/10/30/20251030_abc123.jpg',
    'filename': '20251030_abc123.jpg',
    'filepath': '/absolute/path/to/file.jpg',
    'size': 123456
}
```

### 2. delete_file(file_url)
删除本地文件

**参数**：
- `file_url`: 文件 URL

**返回**：`True` 或 `False`

### 3. file_exists(file_url)
检查文件是否存在

**参数**：
- `file_url`: 文件 URL

**返回**：`True` 或 `False`

### 4. get_file_path(file_url)
获取文件的绝对路径

**参数**：
- `file_url`: 文件 URL

**返回**：文件的绝对路径或 `None`

### 5. get_file_info(file_url)
获取文件信息

**返回**：
```python
{
    'size': 123456,
    'created': datetime,
    'modified': datetime,
    'exists': True
}
```

## 🚀 使用示例

### 后端上传
```python
from utils.file_storage import FileStorage

# 上传文件
file_storage = FileStorage()
result = file_storage.upload_file(request.files['file'])

if result:
    print(f"文件 URL: {result['url']}")
    print(f"文件名: {result['filename']}")
```

### 后端删除
```python
# 删除文件
file_storage = FileStorage()
success = file_storage.delete_file(event.background_image)
```

## 🔍 静态文件服务

Flask 自动提供 `/uploads/` 路径的静态文件访问：

```python
# app.py 中的配置
@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(upload_folder, filename)
```

## 💡 优势

### ✅ 与 OSS 相比的优点
1. **无需配置**：不需要阿里云账号和 AccessKey
2. **零成本**：不产生存储和流量费用
3. **简单直接**：文件直接存在本地，易于管理
4. **快速开发**：无需等待 OSS 上传，本地保存速度快
5. **离线可用**：不依赖外部服务

### ⚠️ 注意事项
1. **备份重要**：定期备份 `uploads/` 文件夹
2. **磁盘空间**：注意服务器磁盘空间使用
3. **扩展性**：大规模应用建议使用 OSS 或 CDN
4. **负载均衡**：多服务器部署需要共享存储（NFS/对象存储）

## 📦 部署建议

### 开发环境
直接使用本地存储，无需额外配置。

### 生产环境

#### 方案1：单服务器
```bash
# 确保 uploads 目录有写权限
sudo chown -R www-data:www-data /path/to/backend/uploads
sudo chmod -R 755 /path/to/backend/uploads
```

#### 方案2：多服务器（需要共享存储）
```bash
# 使用 NFS 共享存储
sudo mount -t nfs nfs-server:/uploads /path/to/backend/uploads

# 或使用对象存储服务（MinIO、阿里云OSS等）
```

#### 方案3：反向代理 Nginx
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    # 前端静态文件
    location / {
        root /path/to/frontend/dist;
        try_files $uri $uri/ /index.html;
    }
    
    # API 请求
    location /api {
        proxy_pass http://localhost:5002;
    }
    
    # 上传文件（由 Nginx 直接提供，减轻后端压力）
    location /uploads {
        alias /path/to/backend/uploads;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

## 🔄 迁移说明

### 从 OSS 迁移到本地存储

如果之前使用了 OSS，现在有文件在 OSS 上：

1. **下载 OSS 文件**
```python
# 批量下载 OSS 文件到本地
import oss2

auth = oss2.Auth('your-key-id', 'your-key-secret')
bucket = oss2.Bucket(auth, 'endpoint', 'bucket-name')

for obj in oss2.ObjectIterator(bucket, prefix='events/'):
    bucket.get_object_to_file(obj.key, f'uploads/{obj.key}')
```

2. **更新数据库 URL**
```sql
-- 更新数据库中的图片 URL
UPDATE events 
SET background_image = REPLACE(
    background_image, 
    'https://bucket.oss-region.aliyuncs.com/', 
    '/uploads/'
);
```

### 从本地存储迁移到 OSS

如果以后需要迁移到 OSS：

1. 恢复使用 `utils/oss_helper.py`
2. 上传本地文件到 OSS
3. 更新数据库 URL

## 📝 维护建议

### 定期清理
```python
# 定期清理超过30天的旧文件
import os
import time
from datetime import datetime, timedelta

def cleanup_old_files(days=30):
    threshold = time.time() - (days * 86400)
    for root, dirs, files in os.walk('uploads'):
        for file in files:
            filepath = os.path.join(root, file)
            if os.path.getmtime(filepath) < threshold:
                os.remove(filepath)
```

### 磁盘空间监控
```bash
# 检查 uploads 目录大小
du -sh uploads/

# 检查磁盘使用情况
df -h
```

### 备份策略
```bash
# 每天备份 uploads 目录
0 2 * * * tar -czf /backup/uploads_$(date +\%Y\%m\%d).tar.gz /path/to/uploads
```

## 🎉 完成

本地文件存储已经配置完成，你现在可以：

1. ✅ 上传图片到本地 `uploads/` 目录
2. ✅ 通过 `/uploads/` URL 访问图片
3. ✅ 图片会自动按日期分类存储
4. ✅ 文件名包含日期和随机ID，防止冲突

**重启后端服务后即可使用！**

```bash
cd backend
python app.py
```

---

**提示**：开发阶段使用本地存储完全足够，生产环境如需更好的性能和扩展性，可以考虑使用 CDN 或对象存储服务。

