#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

category = Category.objects.get(name='搜索工具')

tool_data = {
    'name': 'Z-Library永久访问指南',
    'short_description': '告别寻址困扰，使用zlib.re永久入口自动跳转最新可用地址',
    'full_description': '''**永久访问地址：**
http://zlib.re

**使用方法：**
1. 打开浏览器
2. 地址栏输入 zlib.re
3. 按下回车
4. 自动跳转至当前Z-Library最新可用官方地址

**核心优势：**
- 无需记住繁杂的备用域名
- 自动检测并跳转至最新可用地址
- 无论官方如何更迭，此入口永指真身
- 建议直接收藏到浏览器

**重要提示：**
如果能搜书但无法下载或提示限额，不是网站问题，是因为未登录！

**解决方案：**
- 必须登录账号才能下载
- 游客权限极低
- 登录后下载按钮即可使用
- 每日下载额度恢复正常

**使用要点：**
1. 访问认准：http://zlib.re
2. 遇到下载问题：先登录账号''',
    'website_url': 'http://zlib.re',
    'category': category
}

tool, created = Tool.objects.get_or_create(
    name=tool_data['name'],
    defaults=tool_data
)

if created:
    print(f'✓ 已添加: {tool.name} → {category.name}')
else:
    print(f'- 已存在: {tool.name}')

print('\n完成！')
