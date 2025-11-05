# QD日历部署指南

本指南详细说明如何在生产环境中部署 QD日历应用。

## 目录
- [服务器要求](#服务器要求)
- [后端部署](#后端部署)
- [前端部署](#前端部署)
- [Nginx 配置](#nginx-配置)
- [SSL 证书](#ssl-证书)
- [性能优化](#性能优化)
- [监控和日志](#监控和日志)
- [备份策略](#备份策略)

## 服务器要求

### 最低配置
- CPU: 2核
- 内存: 2GB
- 存储: 20GB
- 系统: Ubuntu 20.04+ / CentOS 7+

### 推荐配置
- CPU: 4核
- 内存: 4GB
- 存储: 50GB SSD
- 系统: Ubuntu 22.04 LTS

### 软件要求
- Python 3.8+
- Node.js 16+
- MySQL 5.7+ 或 MariaDB 10.3+
- Nginx 1.18+
- PM2 (Node进程管理)
- Supervisor (Python进程管理)

## 后端部署

### 1. 安装系统依赖

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip python3-venv mysql-server nginx supervisor

# CentOS/RHEL
sudo yum install python3 python3-pip mysql-server nginx supervisor
```

### 2. 配置 MySQL

```bash
# 启动 MySQL 服务
sudo systemctl start mysql
sudo systemctl enable mysql

# 安全配置
sudo mysql_secure_installation

# 创建数据库和用户
sudo mysql -u root -p
```

在 MySQL 中执行：
```sql
CREATE DATABASE qd_calendar CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'qd_user'@'localhost' IDENTIFIED BY '强密码';
GRANT ALL PRIVILEGES ON qd_calendar.* TO 'qd_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 3. 部署后端代码

```bash
# 创建应用目录
sudo mkdir -p /var/www/qd-calendar
sudo chown $USER:$USER /var/www/qd-calendar

# 上传代码
cd /var/www/qd-calendar
# 使用 git 或 scp 上传代码
git clone <your-repo-url> .
# 或
scp -r ./backend user@server:/var/www/qd-calendar/

# 进入后端目录
cd backend

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 安装生产服务器
pip install gunicorn
```

### 4. 配置环境变量

```bash
# 创建 .env 文件
nano .env
```

填入配置：
```env
FLASK_ENV=production
SECRET_KEY=生成一个强随机字符串
JWT_SECRET_KEY=生成另一个强随机字符串

DB_HOST=localhost
DB_PORT=3306
DB_NAME=qd_calendar
DB_USER=qd_user
DB_PASSWORD=你的数据库密码

OSS_ACCESS_KEY_ID=你的阿里云AccessKey
OSS_ACCESS_KEY_SECRET=你的阿里云Secret
OSS_BUCKET_NAME=你的Bucket名称
OSS_ENDPOINT=oss-cn-hangzhou.aliyuncs.com
OSS_DOMAIN=https://你的Bucket.oss-cn-hangzhou.aliyuncs.com

ADMIN_USERNAME=admin
ADMIN_PASSWORD=修改为强密码
```

生成密钥：
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

### 5. 初始化数据库

```bash
source venv/bin/activate
python init_db.py
```

### 6. 配置 Supervisor

创建配置文件：
```bash
sudo nano /etc/supervisor/conf.d/qd-calendar.conf
```

内容：
```ini
[program:qd-calendar]
directory=/var/www/qd-calendar/backend
command=/var/www/qd-calendar/backend/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 app:app
user=www-data
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
stderr_logfile=/var/log/qd-calendar/error.log
stdout_logfile=/var/log/qd-calendar/access.log
```

创建日志目录：
```bash
sudo mkdir -p /var/log/qd-calendar
sudo chown www-data:www-data /var/log/qd-calendar
```

启动服务：
```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start qd-calendar
```

检查状态：
```bash
sudo supervisorctl status qd-calendar
```

## 前端部署

### 1. 构建前端

在本地或服务器上：
```bash
cd frontend

# 安装依赖
npm install

# 构建生产版本
npm run build

# dist 目录包含构建产物
```

### 2. 上传到服务器

```bash
# 创建前端目录
sudo mkdir -p /var/www/qd-calendar/frontend

# 上传构建产物
scp -r ./dist/* user@server:/var/www/qd-calendar/frontend/

# 设置权限
sudo chown -R www-data:www-data /var/www/qd-calendar/frontend
```

## Nginx 配置

### 1. 创建站点配置

```bash
sudo nano /etc/nginx/sites-available/qd-calendar
```

内容：
```nginx
# HTTP 重定向到 HTTPS
server {
    listen 80;
    listen [::]:80;
    server_name your-domain.com www.your-domain.com;
    
    # 强制 HTTPS
    return 301 https://$server_name$request_uri;
}

# HTTPS 服务器
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name your-domain.com www.your-domain.com;

    # SSL 证书
    ssl_certificate /etc/ssl/certs/your-domain.crt;
    ssl_certificate_key /etc/ssl/private/your-domain.key;
    
    # SSL 配置
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    # 前端静态文件
    root /var/www/qd-calendar/frontend;
    index index.html;

    # Gzip 压缩
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;

    # 前端路由
    location / {
        try_files $uri $uri/ /index.html;
        
        # 缓存静态资源
        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }

    # API 代理
    location /api {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # 超时设置
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # 安全头
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;

    # 日志
    access_log /var/log/nginx/qd-calendar-access.log;
    error_log /var/log/nginx/qd-calendar-error.log;
}
```

### 2. 启用站点

```bash
# 创建符号链接
sudo ln -s /etc/nginx/sites-available/qd-calendar /etc/nginx/sites-enabled/

# 测试配置
sudo nginx -t

# 重启 Nginx
sudo systemctl restart nginx
```

## SSL 证书

### 使用 Let's Encrypt（免费）

```bash
# 安装 Certbot
sudo apt install certbot python3-certbot-nginx

# 获取证书
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# 自动续期
sudo certbot renew --dry-run
```

### 使用自签名证书（仅测试）

```bash
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /etc/ssl/private/qd-calendar.key \
    -out /etc/ssl/certs/qd-calendar.crt
```

## 性能优化

### 1. 数据库优化

编辑 MySQL 配置：
```bash
sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
```

添加：
```ini
[mysqld]
# 连接池
max_connections = 200

# 查询缓存
query_cache_size = 64M
query_cache_type = 1

# InnoDB 优化
innodb_buffer_pool_size = 1G
innodb_log_file_size = 256M
innodb_flush_log_at_trx_commit = 2
```

重启 MySQL：
```bash
sudo systemctl restart mysql
```

### 2. Redis 缓存（可选）

```bash
# 安装 Redis
sudo apt install redis-server

# 启动服务
sudo systemctl start redis
sudo systemctl enable redis

# 在后端安装 Redis 支持
pip install redis flask-caching
```

### 3. CDN 配置

将静态资源上传到 CDN：
- 图片文件
- JavaScript 文件
- CSS 文件
- 字体文件

更新前端构建配置使用 CDN URL。

## 监控和日志

### 1. 日志收集

```bash
# 查看后端日志
sudo tail -f /var/log/qd-calendar/access.log
sudo tail -f /var/log/qd-calendar/error.log

# 查看 Nginx 日志
sudo tail -f /var/log/nginx/qd-calendar-access.log
sudo tail -f /var/log/nginx/qd-calendar-error.log

# 查看 Supervisor 日志
sudo supervisorctl tail -f qd-calendar
```

### 2. 日志轮转

创建配置：
```bash
sudo nano /etc/logrotate.d/qd-calendar
```

内容：
```
/var/log/qd-calendar/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    missingok
    sharedscripts
    postrotate
        supervisorctl restart qd-calendar > /dev/null 2>&1 || true
    endscript
}
```

### 3. 系统监控

使用工具：
- Prometheus + Grafana
- New Relic
- Datadog
- 阿里云监控

## 备份策略

### 1. 数据库备份

创建备份脚本：
```bash
sudo nano /usr/local/bin/backup-qd-calendar.sh
```

内容：
```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/var/backups/qd-calendar"
DB_NAME="qd_calendar"
DB_USER="qd_user"
DB_PASS="你的密码"

mkdir -p $BACKUP_DIR

# 备份数据库
mysqldump -u $DB_USER -p$DB_PASS $DB_NAME | gzip > $BACKUP_DIR/db_$DATE.sql.gz

# 删除30天前的备份
find $BACKUP_DIR -name "db_*.sql.gz" -mtime +30 -delete

echo "备份完成: $DATE"
```

设置权限和定时任务：
```bash
sudo chmod +x /usr/local/bin/backup-qd-calendar.sh

# 添加到 crontab（每天凌晨3点备份）
sudo crontab -e
```

添加：
```
0 3 * * * /usr/local/bin/backup-qd-calendar.sh >> /var/log/qd-calendar-backup.log 2>&1
```

### 2. 代码备份

使用 Git 进行版本控制，定期推送到远程仓库。

### 3. OSS 备份

阿里云 OSS 自带版本控制和跨区域复制功能。

## 故障恢复

### 数据库恢复

```bash
# 恢复最新备份
gunzip < /var/backups/qd-calendar/db_YYYYMMDD_HHMMSS.sql.gz | \
    mysql -u qd_user -p qd_calendar
```

### 应用重启

```bash
# 重启后端
sudo supervisorctl restart qd-calendar

# 重启 Nginx
sudo systemctl restart nginx

# 重启 MySQL
sudo systemctl restart mysql
```

## 安全检查清单

- [ ] 修改所有默认密码
- [ ] 启用 HTTPS
- [ ] 配置防火墙
- [ ] 限制 SSH 访问
- [ ] 启用 fail2ban
- [ ] 定期更新系统和依赖
- [ ] 配置数据库访问限制
- [ ] 启用应用日志
- [ ] 配置备份策略
- [ ] 设置监控告警

## 维护建议

1. **每周**
   - 检查日志错误
   - 监控磁盘使用
   - 检查备份状态

2. **每月**
   - 更新系统补丁
   - 更新应用依赖
   - 审查访问日志
   - 性能分析

3. **每季度**
   - 安全审计
   - 容量规划
   - 灾难恢复演练

## 扩展部署

### Docker 部署

创建 `Dockerfile`（后端）：
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

创建 `docker-compose.yml`：
```yaml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "5000:5000"
    environment:
      - DB_HOST=mysql
    depends_on:
      - mysql
      
  mysql:
    image: mysql:8.0
    environment:
      - MYSQL_DATABASE=qd_calendar
      - MYSQL_ROOT_PASSWORD=rootpass
    volumes:
      - mysql_data:/var/lib/mysql
      
  frontend:
    image: nginx:alpine
    volumes:
      - ./frontend/dist:/usr/share/nginx/html
    ports:
      - "80:80"

volumes:
  mysql_data:
```

### Kubernetes 部署

需要准备：
- Deployment YAML
- Service YAML
- Ingress YAML
- ConfigMap/Secret

详细配置请参考 Kubernetes 文档。

---

部署遇到问题？查看[故障排查指南](./backend/README.md#故障排查)或提交 Issue。

