#!/bin/bash
# Cloudflare Tunnel 自动诊断和修复脚本
# 使用方法: sudo SITE_HOST=ai-tool.indevs.in bash fix_cloudflare_tunnel.sh

set -euo pipefail

CLOUDFLARED_SERVICE="${CLOUDFLARED_SERVICE:-cloudflared}"
GUNICORN_SERVICE="${GUNICORN_SERVICE:-gunicorn}"
NGINX_SERVICE="${NGINX_SERVICE:-nginx}"
SITE_HOST="${SITE_HOST:-ai-tool.indevs.in}"

print_header() {
    echo "=========================================="
    echo "$1"
    echo "=========================================="
    echo ""
}

print_section() {
    echo ""
    echo "$1"
    echo "----------------------------------------"
}

service_exists() {
    systemctl list-unit-files "${1}.service" --no-legend 2>/dev/null | grep -q "^${1}\.service"
}

extract_service_execstart() {
    systemctl cat "$1" 2>/dev/null | sed -n 's/^ExecStart=//p' | tail -n 1
}

discover_config_path() {
    local execstart="$1"
    local candidate=""

    candidate="$(printf '%s\n' "$execstart" | sed -n 's/.*--config[= ]\([^ ]*\).*/\1/p' | head -n 1)"
    if [ -n "$candidate" ] && [ -f "$candidate" ]; then
        printf '%s\n' "$candidate"
        return
    fi

    for path in \
        /etc/cloudflared/config.yml \
        /etc/cloudflared/config.yaml \
        /root/.cloudflared/config.yml \
        /root/.cloudflared/config.yaml \
        /home/*/.cloudflared/config.yml \
        /home/*/.cloudflared/config.yaml
    do
        if ls $path >/dev/null 2>&1; then
            ls $path 2>/dev/null | head -n 1
            return
        fi
    done
}

extract_yaml_value() {
    local key="$1"
    local file="$2"
    sed -n "s/^[[:space:]]*${key}:[[:space:]]*//p" "$file" | head -n 1 | tr -d '"' | tr -d "'"
}

validate_origin() {
    local config_file="$1"
    local service_url=""

    service_url="$(grep -E '^[[:space:]]*service:[[:space:]]*' "$config_file" | head -n 1 | sed 's/^[^:]*:[[:space:]]*//' | tr -d '"' | tr -d "'")"
    if [ -z "$service_url" ]; then
        echo "⚠️  未在配置中解析到 ingress service，跳过源站探测"
        return
    fi

    if [[ "$service_url" == http://* || "$service_url" == https://* ]]; then
        if curl -sS -I --max-time 5 "$service_url" >/dev/null; then
            echo "✅ Tunnel 源站可访问: $service_url"
        else
            echo "⚠️  Tunnel 源站不可访问: $service_url"
        fi
    else
        echo "ℹ️  Tunnel 指向非 HTTP 服务: $service_url"
    fi
}

print_header "Cloudflare Tunnel 诊断和修复工具"

if [ "$EUID" -ne 0 ]; then
    echo "❌ 请使用 sudo 运行此脚本"
    exit 1
fi

print_section "步骤 1/6: 检查 cloudflared 安装"
if ! command -v cloudflared >/dev/null 2>&1; then
    echo "❌ cloudflared 未安装"
    echo "正在安装 cloudflared..."
    wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
    dpkg -i cloudflared-linux-amd64.deb
    rm cloudflared-linux-amd64.deb
    echo "✅ cloudflared 安装完成"
else
    echo "✅ cloudflared 已安装: $(cloudflared --version)"
fi

print_section "步骤 2/6: 检查 cloudflared 服务"
if service_exists "$CLOUDFLARED_SERVICE"; then
    echo "✅ 发现服务: $CLOUDFLARED_SERVICE"
else
    echo "❌ 未发现服务: $CLOUDFLARED_SERVICE"
    echo "请确认服务名是否正确，例如:"
    echo "  sudo CLOUDFLARED_SERVICE=cloudflared-tunnel bash fix_cloudflare_tunnel.sh"
    exit 1
fi

if systemctl is-active --quiet "$CLOUDFLARED_SERVICE"; then
    echo "✅ $CLOUDFLARED_SERVICE 服务正在运行"
else
    echo "❌ $CLOUDFLARED_SERVICE 服务未运行，尝试启动"
    systemctl start "$CLOUDFLARED_SERVICE" || true
fi

EXECSTART="$(extract_service_execstart "$CLOUDFLARED_SERVICE")"
if [ -n "$EXECSTART" ]; then
    echo "ExecStart: $EXECSTART"
fi

CONFIG_PATH="$(discover_config_path "$EXECSTART" || true)"

print_section "步骤 3/6: 检查 tunnel 配置和凭据"
if [ -n "${CONFIG_PATH:-}" ] && [ -f "$CONFIG_PATH" ]; then
    echo "✅ 找到配置文件: $CONFIG_PATH"

    TUNNEL_ID="$(extract_yaml_value tunnel "$CONFIG_PATH")"
    CREDENTIALS_FILE="$(extract_yaml_value credentials-file "$CONFIG_PATH")"

    if [ -n "$TUNNEL_ID" ]; then
        echo "✅ Tunnel ID: $TUNNEL_ID"
    else
        echo "⚠️  未在配置中找到 tunnel 字段"
    fi

    if grep -q "$SITE_HOST" "$CONFIG_PATH"; then
        echo "✅ Hostname 已出现在 ingress 中: $SITE_HOST"
    else
        echo "⚠️  ingress 中未找到 hostname: $SITE_HOST"
    fi

    if [ -n "$CREDENTIALS_FILE" ]; then
        if [ -f "$CREDENTIALS_FILE" ]; then
            echo "✅ 凭据文件存在: $CREDENTIALS_FILE"
        else
            echo "❌ 凭据文件不存在: $CREDENTIALS_FILE"
        fi
    else
        echo "⚠️  未在配置中找到 credentials-file 字段"
    fi

    if cloudflared tunnel ingress validate --config "$CONFIG_PATH"; then
        echo "✅ ingress 配置校验通过"
    else
        echo "❌ ingress 配置校验失败"
    fi

    validate_origin "$CONFIG_PATH"
else
    echo "⚠️  未自动发现 config.yml/config.yaml"
    echo "请检查 systemd 服务是否通过 token 启动，或者配置文件在非默认路径"
fi

if [ -n "${TUNNEL_ID:-}" ]; then
    if cloudflared tunnel info "$TUNNEL_ID" >/tmp/cloudflared_tunnel_info.txt 2>&1; then
        echo "✅ Cloudflare 可解析该 tunnel"
        sed -n '1,20p' /tmp/cloudflared_tunnel_info.txt
    else
        echo "⚠️  无法获取 tunnel info，常见原因是未登录、凭据丢失或 tunnel 已被删除"
        sed -n '1,20p' /tmp/cloudflared_tunnel_info.txt
    fi
fi

print_section "步骤 4/6: 检查 Web 服务"
for service in "$GUNICORN_SERVICE" "$NGINX_SERVICE"; do
    if service_exists "$service"; then
        if systemctl is-active --quiet "$service"; then
            echo "✅ $service 服务正常"
        else
            echo "⚠️  $service 未运行，正在重启"
            systemctl restart "$service" || true
        fi
    else
        echo "⚠️  未发现服务: $service"
    fi
done

print_section "步骤 5/6: 查看最近日志并重启服务"
echo "Cloudflared 最近日志:"
journalctl -u "$CLOUDFLARED_SERVICE" -n 30 --no-pager || true

echo ""
echo "重启相关服务..."
systemctl restart "$CLOUDFLARED_SERVICE" || true
service_exists "$GUNICORN_SERVICE" && systemctl restart "$GUNICORN_SERVICE" || true
service_exists "$NGINX_SERVICE" && systemctl restart "$NGINX_SERVICE" || true

echo "等待服务启动..."
sleep 3

print_section "步骤 6/6: 状态总结"
for service in "$CLOUDFLARED_SERVICE" "$GUNICORN_SERVICE" "$NGINX_SERVICE"; do
    if service_exists "$service"; then
        if systemctl is-active --quiet "$service"; then
            echo "✅ $service: 运行中"
        else
            echo "❌ $service: 未运行"
        fi
    fi
done

echo ""
echo "外部探测:"
if curl -sS -I --max-time 10 "https://$SITE_HOST" >/tmp/cloudflare_probe.txt 2>&1; then
    sed -n '1,10p' /tmp/cloudflare_probe.txt
else
    echo "⚠️  无法通过 Cloudflare 访问 https://$SITE_HOST"
    sed -n '1,10p' /tmp/cloudflare_probe.txt
fi

echo ""
print_header "诊断结束"
echo "如果仍然看到 Cloudflare 1033，优先检查这三项："
echo "1. tunnel 本身是否仍存在，并且 cloudflared 使用的是对应凭据"
echo "2. Cloudflare Zero Trust 里的 Public Hostname 是否仍绑定到 $SITE_HOST"
echo "3. systemd 里的 ExecStart 是否指向了正确的 config 或 token"
echo ""
