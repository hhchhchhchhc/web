#!/usr/bin/env python3
import os
import django
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

# Create VPN category
category, _ = Category.objects.get_or_create(
    name='免费赠送VPN',
    defaults={'slug': slugify('免费赠送VPN', allow_unicode=True)}
)

# Create or update VPN tool
Tool.objects.update_or_create(
    name='免费VPN订阅',
    defaults={
        'slug': slugify('免费VPN订阅', allow_unicode=True),
        'short_description': '免费VPN服务，支持Clash Verge和v2raya客户端',
        'full_description': '''免费VPN订阅服务

Clash Verge订阅链接：
https://times1770483933.subxiandan.top:9604/v2b/shandian/api/v1/client/subscribe?token=d33ab98ae6a869132c2041b2349b755c

v2raya美国节点1：
vless://c521e23c-2d0b-4c2d-9982-707be5e9f9fe@98.92.241.91:443?type=tcp&encryption=none&security=none#us-qfcu1fjh

v2raya美国节点2：
vless://94cf70af-2bbf-47e9-a002-0865f1a58974@104.250.139.178:11021?encryption=none&flow=xtls-rprx-vision&security=reality&sni=apple.com&fp=chrome&pbk=pp9zGF8QJ1ofMRPwkl7h5FYJqOiEitUvz7Jjvei3XRA&sid=1497de28&type=tcp&headerType=none#US%E7%BE%8E%E5%9B%BD

使用说明：
1. Clash Verge用户：复制订阅链接到客户端
2. v2raya用户：复制vless链接导入配置

更多节点资源：
https://linux.do/tag/193-tag/193 - Linux.do社区VPN节点分享''',
        'website_url': 'https://times1770483933.subxiandan.top:9604/v2b/shandian/api/v1/client/subscribe?token=d33ab98ae6a869132c2041b2349b755c',
        'category': category,
        'is_published': True,
        'is_featured': True
    }
)

print("✅ VPN工具添加成功！")
