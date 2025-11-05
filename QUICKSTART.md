# QD日历 - 快速启动指南

本指南将帮助你在5分钟内启动 QD日历应用。

## 前置条件

确保你的系统已安装：
- Python 3.8 或更高版本
- Node.js 16 或更高版本
- MySQL 5.7 或更高版本

## 第一步：数据库准备

1. 启动 MySQL 服务

2. 创建数据库：
```sql
CREATE DATABASE qd_calendar CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

## 第二步：后端启动

1. 打开终端，进入后端目录：
```bash
cd backend
```

2. 创建并激活虚拟环境：
```bash
# macOS/Linux
python3 -m venv env
source env/bin/activate

# Windows
python -m venv env
env\Scripts\activate
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

4. 配置环境变量：
```bash
cp .env.example .env
```

编辑 `.env` 文件，至少需要配置：
```env
# 数据库配置（必须）
DB_HOST=localhost
DB_PORT=3306
DB_NAME=qd_calendar
DB_USER=root
DB_PASSWORD=你的MySQL密码

# 密钥配置（必须）
SECRET_KEY=请修改为随机字符串
JWT_SECRET_KEY=请修改为随机字符串

# 管理员配置（可选，默认 admin/admin123）
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123

# OSS 配置（可选，如果不使用图片上传功能可以跳过）
# OSS_ACCESS_KEY_ID=your-key
# OSS_ACCESS_KEY_SECRET=your-secret
# OSS_BUCKET_NAME=your-bucket
# OSS_ENDPOINT=oss-cn-hangzhou.aliyuncs.com
# OSS_DOMAIN=https://your-bucket.oss-cn-hangzhou.aliyuncs.com
```

5. 启动后端服务：
```bash
python app.py
```

你应该看到：
```
 * Running on http://0.0.0.0:5000
```

**保持这个终端窗口打开！**

## 第三步：前端启动

1. 打开新的终端窗口，进入前端目录：
```bash
cd frontend
```

2. 安装依赖：
```bash
npm install
# 或
yarn install
```

3. 启动开发服务器：
```bash
npm run dev
# 或
yarn dev
```

你应该看到：
```
  VITE ready in xxx ms

  ➜  Local:   http://localhost:3000/
```

## 第四步：访问应用

在浏览器中打开：http://localhost:3000

### 登录选项

#### 选项1：游客浏览（最快）
1. 点击"游客浏览"按钮
2. 立即进入日历视图（只读模式）

#### 选项2：管理员登录
1. 点击"登录"按钮
2. 输入默认管理员账号：
   - 用户名：`admin`
   - 密码：`admin123`
3. 登录后可以创建和管理日程

#### 选项3：注册新账号
1. 点击"注册账号"
2. 填写用户名和密码
3. 注册成功后返回登录页面
4. 使用新账号登录（普通用户，只能查看）

## 第五步：测试功能

### 管理员操作流程

1. **创建日程**
   - 登录管理员账号
   - 点击"管理面板"按钮
   - 点击"创建日程"
   - 填写日程信息
   - （可选）上传背景图片
   - 点击"创建"

2. **查看日程**
   - 点击"日历视图"
   - 在日历中查看已创建的日程
   - 点击日期查看当天所有日程
   - 点击日程查看详情

3. **编辑日程**
   - 在管理面板中找到要编辑的日程
   - 点击"编辑"按钮
   - 修改信息后保存

4. **删除日程**
   - 在管理面板中点击"删除"按钮
   - 确认删除

### 普通用户/游客操作

1. 浏览日历视图
2. 查看日程详情
3. 使用筛选功能

## 常见问题

### Q1: 后端启动失败，提示数据库连接错误
**A:** 检查 `.env` 文件中的数据库配置是否正确，确保 MySQL 服务已启动。

### Q2: 前端启动后无法访问后端接口
**A:** 确保后端服务正在运行（http://localhost:5000），Vite 会自动代理 `/api` 请求。

### Q3: 上传图片失败
**A:** 如果没有配置阿里云 OSS，图片上传功能将不可用。这不影响其他功能的使用。

### Q4: 忘记管理员密码
**A:** 
1. 停止后端服务
2. 删除数据库中的 users 表
3. 重新启动后端，会自动创建新的管理员账号

### Q5: 端口被占用
**A:** 
- 后端：修改 `app.py` 中的端口号
- 前端：修改 `vite.config.js` 中的端口号

## 下一步

- 阅读完整的 [README.md](./README.md) 了解更多功能
- 查看 [API 文档](./backend/README.md) 了解接口详情
- 自定义样式和配置

## 生产部署

开发测试完成后，参考 README.md 中的部署章节进行生产环境部署。

## 获取帮助

遇到问题？
- 查看项目 Issues
- 阅读详细文档
- 提交新的 Issue

祝使用愉快！🎉

