# QD日历启动检查清单

使用此清单确保正确配置和启动项目。

## 📋 环境准备

### 系统要求
- [ ] Python 3.8+ 已安装
  ```bash
  python3 --version
  ```
- [ ] Node.js 16+ 已安装
  ```bash
  node --version
  ```
- [ ] MySQL 5.7+ 已安装并运行
  ```bash
  mysql --version
  systemctl status mysql  # Linux
  ```

## 🗄️ 数据库配置

- [ ] MySQL 服务已启动
- [ ] 创建数据库
  ```sql
  CREATE DATABASE qd_calendar CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
  ```
- [ ] 数据库连接信息正确
  - 主机: localhost
  - 端口: 3306
  - 用户名: ________
  - 密码: ________

## 🔧 后端配置

### 环境设置
- [ ] 进入后端目录
  ```bash
  cd backend
  ```
- [ ] 创建虚拟环境
  ```bash
  python3 -m venv env
  ```
- [ ] 激活虚拟环境
  ```bash
  source env/bin/activate  # Mac/Linux
  # 或
  env\Scripts\activate  # Windows
  ```
- [ ] 安装依赖
  ```bash
  pip install -r requirements.txt
  ```

### 环境变量配置
- [ ] 复制环境变量文件
  ```bash
  cp .env.example .env
  ```
- [ ] 编辑 .env 文件，配置以下项：

#### 必需配置
- [ ] SECRET_KEY（生成随机字符串）
  ```bash
  python3 -c "import secrets; print(secrets.token_hex(32))"
  ```
- [ ] JWT_SECRET_KEY（生成随机字符串）
- [ ] DB_HOST（通常为 localhost）
- [ ] DB_PORT（通常为 3306）
- [ ] DB_NAME（qd_calendar）
- [ ] DB_USER（你的数据库用户名）
- [ ] DB_PASSWORD（你的数据库密码）

#### 可选配置
- [ ] ADMIN_USERNAME（默认 admin）
- [ ] ADMIN_PASSWORD（默认 admin123，建议修改）
- [ ] OSS_ACCESS_KEY_ID（如需图片上传）
- [ ] OSS_ACCESS_KEY_SECRET（如需图片上传）
- [ ] OSS_BUCKET_NAME（如需图片上传）
- [ ] OSS_ENDPOINT（如需图片上传）
- [ ] OSS_DOMAIN（如需图片上传）

### 数据库初始化
- [ ] 运行初始化脚本
  ```bash
  python init_db.py
  ```
- [ ] 确认看到成功信息
  - 管理员账户已创建
  - 示例日程已创建

### 启动后端服务
- [ ] 启动 Flask 应用
  ```bash
  python app.py
  ```
- [ ] 验证服务运行
  - 看到 "Running on http://0.0.0.0:5000"
  - 浏览器访问 http://localhost:5000/api/health
  - 应该返回 `{"status": "ok", ...}`

## 🎨 前端配置

### 环境设置
- [ ] 打开新终端窗口
- [ ] 进入前端目录
  ```bash
  cd frontend
  ```
- [ ] 安装依赖
  ```bash
  npm install
  # 或
  yarn install
  ```
  
### 启动前端服务
- [ ] 启动开发服务器
  ```bash
  npm run dev
  # 或
  yarn dev
  ```
- [ ] 验证服务运行
  - 看到 "Local: http://localhost:3000"
  - 浏览器自动打开或手动访问

## 🌐 访问应用

### 功能测试
- [ ] 访问首页 http://localhost:3000
- [ ] 页面正常显示，无控制台错误

### 游客模式测试
- [ ] 点击"游客浏览"按钮
- [ ] 成功进入日历视图
- [ ] 可以查看日程
- [ ] 无法看到管理功能

### 管理员登录测试
- [ ] 点击"登录"按钮
- [ ] 输入管理员账号
  - 用户名: admin
  - 密码: admin123（或你设置的密码）
- [ ] 登录成功，跳转到首页
- [ ] 可以看到"管理面板"按钮

### 管理员功能测试
- [ ] 点击"管理面板"
- [ ] 进入管理页面
- [ ] 可以看到示例日程列表
- [ ] 点击"创建日程"
- [ ] 填写日程信息
  - 标题: 测试日程
  - 日期: 选择今天
  - 优先级: 高
  - 状态: 待处理
- [ ] 点击"创建"按钮
- [ ] 创建成功，列表中显示新日程

### 日历视图测试
- [ ] 点击"日历视图"
- [ ] 看到月历展示
- [ ] 今天的日期有标识
- [ ] 有日程的日期显示事件数量
- [ ] 点击有日程的日期
- [ ] 弹出日程列表
- [ ] 点击日程
- [ ] 显示详细信息

### 编辑和删除测试
- [ ] 回到管理面板
- [ ] 点击一个日程的"编辑"
- [ ] 修改标题或其他信息
- [ ] 保存成功
- [ ] 点击"删除"按钮
- [ ] 确认删除
- [ ] 删除成功

### 注册新用户测试
- [ ] 退出登录
- [ ] 点击"注册账号"
- [ ] 填写注册信息
  - 用户名: testuser2
  - 密码: password123
- [ ] 注册成功
- [ ] 使用新账号登录
- [ ] 只能查看日程，无法管理

## 🔍 常见问题检查

### 后端无法启动
- [ ] 检查 Python 版本
- [ ] 检查虚拟环境是否激活
- [ ] 检查依赖是否安装完整
- [ ] 检查 .env 文件是否存在
- [ ] 检查数据库连接配置
- [ ] 查看错误日志

### 前端无法启动
- [ ] 检查 Node.js 版本
- [ ] 检查 npm 安装是否完成
- [ ] 删除 node_modules 重新安装
  ```bash
  rm -rf node_modules
  npm install
  ```
- [ ] 检查端口 3000 是否被占用

### 无法连接数据库
- [ ] MySQL 服务是否运行
- [ ] 数据库是否已创建
- [ ] 用户名密码是否正确
- [ ] 主机和端口是否正确
- [ ] 防火墙是否阻止连接

### API 请求失败
- [ ] 后端服务是否运行
- [ ] 检查浏览器控制台错误
- [ ] 检查网络请求状态码
- [ ] 验证 token 是否有效
- [ ] 检查 CORS 配置

### 图片上传失败
- [ ] OSS 配置是否填写
- [ ] AccessKey 是否正确
- [ ] Bucket 权限是否配置
- [ ] 文件大小是否超限
- [ ] 文件格式是否支持

## 📱 移动端测试（可选）

- [ ] 在手机浏览器打开
- [ ] 页面自动适配
- [ ] 触摸操作正常
- [ ] 响应速度可接受

## 🚀 生产部署检查（可选）

如果要部署到生产环境，额外检查：

### 安全配置
- [ ] 修改默认管理员密码
- [ ] 使用强密钥
- [ ] 配置 HTTPS
- [ ] 限制 CORS 源
- [ ] 配置防火墙

### 性能优化
- [ ] 启用数据库索引
- [ ] 配置静态资源缓存
- [ ] 启用 Gzip 压缩
- [ ] 考虑使用 CDN

### 监控和备份
- [ ] 配置日志
- [ ] 设置监控告警
- [ ] 配置自动备份
- [ ] 准备恢复方案

## ✅ 完成确认

- [ ] 所有核心功能正常工作
- [ ] 没有控制台错误
- [ ] 用户体验流畅
- [ ] 准备开始使用

## 📞 获取帮助

如果遇到问题：
1. 查看 [QUICKSTART.md](./QUICKSTART.md) 快速启动指南
2. 查看 [README.md](./README.md) 详细文档
3. 查看后端日志和前端控制台
4. 提交 GitHub Issue

---

**恭喜！如果所有项目都打勾，你的 QD日历已经准备就绪！** 🎉

**开始创建你的第一个日程吧！** ✨

