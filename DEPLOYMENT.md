# 部署指南

## 当前状态
✅ 所有配置文件已创建
✅ Git 仓库已初始化
✅ 代码已提交到本地仓库

## 生成的密钥
```
SECRET_KEY=ynz4t0*$p=*(=f_(my9wrnca60x\4ypi68bv%+\kz32rl0nb*d
```

---

## 第一步：推送到 GitHub

### 1.1 在 GitHub 创建新仓库
1. 访问 https://github.com/new
2. 仓库名称：`tool_aggregator`
3. 设为 Private（推荐）或 Public
4. **不要**勾选 "Add a README file"
5. 点击 "Create repository"

### 1.2 推送代码
复制你的 GitHub 仓库 URL，然后执行：

```bash
cd /home/user/tool_aggregator
git remote add origin https://github.com/你的用户名/tool_aggregator.git
git branch -M main
git push -u origin main
```

---

## 第二步：部署到 Railway

### 2.1 创建 Railway 项目
1. 访问 https://railway.app
2. 点击 "Login" → 使用 GitHub 登录
3. 点击 "New Project"
4. 选择 "Deploy from GitHub repo"
5. 选择 `tool_aggregator` 仓库
6. Railway 会自动开始部署

### 2.2 添加 PostgreSQL 数据库
1. 在项目页面，点击 "New" 按钮
2. 选择 "Database"
3. 选择 "Add PostgreSQL"
4. Railway 会自动创建数据库并注入 `DATABASE_URL` 环境变量

### 2.3 配置环境变量
在 Railway 项目中，点击你的服务 → "Variables" 标签，添加以下环境变量：

```
DJANGO_SETTINGS_MODULE=config.settings_prod
SECRET_KEY=ynz4t0*$p=*(=f_(my9wrnca60x\4ypi68bv%+\kz32rl0nb*d
ALLOWED_HOSTS=*.railway.app,你的域名.com
DEBUG=False
```

**注意**：将 `你的域名.com` 替换为你的实际域名

### 2.4 等待部署完成
- Railway 会自动重新部署
- 在 "Deployments" 标签查看部署日志
- 部署成功后，会显示一个 Railway 提供的 URL（如 `xxx.railway.app`）

### 2.5 创建超级用户
1. 在 Railway 项目页面，点击你的服务
2. 点击 "Settings" → 找到 "Service" 部分
3. 向下滚动找到 "Deploy Logs" 或使用 Railway CLI
4. 或者使用 Railway CLI：
   ```bash
   # 安装 Railway CLI
   npm i -g @railway/cli

   # 登录
   railway login

   # 链接到项目
   railway link

   # 运行命令
   railway run python manage.py createsuperuser
   ```

---

## 第三步：配置自定义域名

### 3.1 在 Railway 添加域名
1. 在 Railway 项目中，点击你的服务
2. 点击 "Settings" 标签
3. 找到 "Domains" 部分
4. 点击 "Custom Domain"
5. 输入你的域名（如 `tools.yourdomain.com` 或 `yourdomain.com`）
6. Railway 会提供一个 CNAME 记录值（类似 `xxx.railway.app`）

### 3.2 配置 DNS
在你的域名提供商（阿里云/腾讯云/Cloudflare 等）：

1. 登录域名管理控制台
2. 找到 DNS 解析设置
3. 添加 CNAME 记录：
   - **记录类型**：CNAME
   - **主机记录**：`tools`（如果用子域名）或 `@`（如果用根域名）
   - **记录值**：Railway 提供的值（如 `xxx.railway.app`）
   - **TTL**：默认值（如 600）
4. 保存设置

### 3.3 等待 DNS 传播
- DNS 传播通常需要 5-30 分钟
- 可以用 `nslookup 你的域名.com` 检查是否生效
- Railway 会自动配置 SSL 证书（Let's Encrypt）

---

## 第四步：验证部署

### 4.1 访问网站
- Railway URL: `https://xxx.railway.app`
- 自定义域名: `https://你的域名.com`

### 4.2 测试功能
- [ ] 首页可以访问
- [ ] 工具列表页正常
- [ ] 管理后台可以登录：`https://你的域名.com/admin`
- [ ] 可以添加分类和工具

### 4.3 添加初始数据
1. 登录管理后台
2. 添加 2-3 个分类（如：开发工具、设计工具、效率工具）
3. 添加一些工具测试

---

## 快速命令参考

### 推送到 GitHub
```bash
cd /home/user/tool_aggregator
git remote add origin https://github.com/你的用户名/tool_aggregator.git
git branch -M main
git push -u origin main
```

### 后续更新代码
```bash
cd /home/user/tool_aggregator
git add .
git commit -m "更新说明"
git push
```

### 查看 Railway 日志
```bash
railway logs
```

### 在 Railway 运行命令
```bash
railway run python manage.py migrate
railway run python manage.py createsuperuser
railway run python manage.py collectstatic
```

---

## 故障排查

### 部署失败
1. 检查 Railway 部署日志
2. 确认 `requirements.txt` 中的包版本兼容
3. 确认环境变量配置正确

### 静态文件 404
1. 确认 `DJANGO_SETTINGS_MODULE=config.settings_prod`
2. 检查 Railway 日志中 `collectstatic` 是否成功

### 数据库连接错误
1. 确认 PostgreSQL 数据库已添加
2. 检查 `DATABASE_URL` 环境变量是否存在

### 域名无法访问
1. 检查 DNS 配置是否正确
2. 等待 DNS 传播完成（最多 24 小时）
3. 确认 `ALLOWED_HOSTS` 包含你的域名

---

## 成本说明

**Railway 免费额度**：
- 500 小时/月（约 20 天运行时间）
- 100GB 出站流量
- 512MB RAM
- 1GB 存储

**对于小规模应用（<1000 访问/天）**：
- 完全免费
- 如需 24/7 运行，升级到 Hobby 计划（$5/月）

---

## 下一步优化

1. **添加 Cloudflare CDN**：加速全球访问
2. **配置监控**：Railway 内置监控和告警
3. **定期备份**：导出数据库数据
4. **添加更多功能**：搜索、评论、用户系统等

---

## 需要帮助？

如果遇到问题，可以：
1. 查看 Railway 文档：https://docs.railway.app
2. 查看 Django 部署文档：https://docs.djangoproject.com/en/5.0/howto/deployment/
3. 检查部署日志找到具体错误信息
