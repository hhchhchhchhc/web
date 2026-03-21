# 部署指南

当前线上拓扑按这套来维护：

- 源站：VPS / 本地服务器
- Web：`nginx`
- App：`gunicorn`
- 入口：`Cloudflare` 或 `cloudflared tunnel`

仓库里的自动化脚本已经按这个结构整理好了。

## 一键发布

本地机器执行：

```bash
cd /home/user/tool_aggregator
SERVER_HOST=your-server-ip \
SERVER_USER=your-ssh-user \
bash deploy.sh
```

这条命令会做两件事：

1. `git push origin main`
2. SSH 到服务器执行 `scripts/deploy_server.sh`

如果服务器 SSH 端口不是 `22`：

```bash
SERVER_HOST=your-server-ip \
SERVER_USER=your-ssh-user \
SERVER_PORT=2222 \
bash deploy.sh
```

如果这次只想触发远程部署，不想先 `git push`：

```bash
SERVER_HOST=your-server-ip \
SERVER_USER=your-ssh-user \
PUSH_FIRST=0 \
bash deploy.sh
```

## 服务器脚本

服务器上也可以直接执行：

```bash
cd /var/www/tool_aggregator/code
bash scripts/deploy_server.sh
```

默认会执行：

1. `git fetch` + `git pull --ff-only`
2. `pip install -r requirements.txt`
3. `python manage.py check --deploy`
4. `python manage.py migrate --noinput`
5. `python manage.py collectstatic --noinput`
6. 重启 `gunicorn`
7. 重启 `nginx`
8. 如果存在 `cloudflared` 服务则自动重启

默认路径和服务名：

```bash
APP_DIR=/var/www/tool_aggregator
CODE_DIR=/var/www/tool_aggregator/code
VENV_DIR=/var/www/tool_aggregator/venv
APP_ENV_FILE=/var/www/tool_aggregator/.env
GUNICORN_SERVICE=gunicorn
NGINX_SERVICE=nginx
CLOUDFLARED_SERVICE=cloudflared
BRANCH=main
```

如果你的服务名不同，可以覆盖：

```bash
GUNICORN_SERVICE=tool-aggregator \
NGINX_SERVICE=nginx \
CLOUDFLARED_SERVICE=cloudflared-tunnel \
bash scripts/deploy_server.sh
```

## 前置条件

服务器上需要已经完成这些准备：

- 代码目录存在：`/var/www/tool_aggregator/code`
- 虚拟环境存在：`/var/www/tool_aggregator/venv`
- 环境变量文件存在：`/var/www/tool_aggregator/.env`
- 部署用户对项目目录有写权限
- 部署用户可以执行 `systemctl restart gunicorn nginx`

推荐做法是给部署用户配 `sudo` 免密，仅允许重启这些服务。

## 验证命令

发布后检查：

```bash
systemctl status gunicorn --no-pager
systemctl status nginx --no-pager
systemctl status cloudflared --no-pager
curl -I https://ai-tool.indevs.in
```

如果 tunnel 有问题，再单独跑：

```bash
sudo bash fix_cloudflare_tunnel.sh
```

如果你看到的是 `Cloudflare Tunnel error 1033`，建议直接带上域名跑：

```bash
sudo SITE_HOST=ai-tool.indevs.in bash fix_cloudflare_tunnel.sh
```

## 常见问题

### 1. `deploy_server.sh` 提示不能写代码目录

说明你是错的用户在跑脚本，或者目录 owner 不对。先确认：

```bash
whoami
ls -ld /var/www/tool_aggregator /var/www/tool_aggregator/code
```

### 2. `systemctl restart` 权限不足

给当前部署用户加 sudo 规则，或者手动执行：

```bash
sudo systemctl restart gunicorn
sudo systemctl restart nginx
sudo systemctl restart cloudflared
```

### 3. Cloudflare 前台还没更新

这通常不是 DNS 延迟，而是源站没完成这几步之一：

- 新代码还没 `git pull`
- `collectstatic` 没跑
- `gunicorn` 没重启
- `cloudflared` 还连着旧进程

### 4. Cloudflare 返回 `1033`

`1033` 不是 Django 报错，它通常表示 Cloudflare 边缘已经知道这是一个 Tunnel hostname，但当前无法把这个 hostname 解析到可用的 tunnel。

优先排查：

```bash
sudo SITE_HOST=ai-tool.indevs.in bash fix_cloudflare_tunnel.sh
sudo journalctl -u cloudflared -n 50 --no-pager
systemctl cat cloudflared
```

重点看这几个点：

- `cloudflared` 服务是否真的在运行
- `ExecStart` 是否用了正确的 `--config` 或 token
- `config.yml` 里的 `tunnel:` 和 `credentials-file:` 是否匹配
- `ingress` 里是否还包含 `ai-tool.indevs.in`
- Cloudflare Zero Trust 后台的 Public Hostname 是否还指向这个 tunnel

如果服务在跑，但 `cloudflared tunnel info <tunnel-id>` 查不到 tunnel，通常说明：

- tunnel 被删了
- 当前机器上的凭据文件不是这个 tunnel 的
- 服务切到了另一份旧配置
