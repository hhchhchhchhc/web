#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

category = Category.objects.get(name='免费用最高级大模型')

tool_data = {
    'name': 'Google Gemini Enterprise免费版',
    'short_description': '无需信用卡，免费使用Gemini 3、Nano Banana Pro、Veo 3和深度研究',
    'full_description': '''**免费内容：**
- Gemini 3 - Google最新顶级大模型
- Nano Banana Pro - 顶级AI生图模型
- Veo 3 - AI视频生成工具
- 深度研究功能

**使用方法：**
1. 需要科学上网工具
2. 访问 https://cloud.google.com/gemini-enterprise?hl=zh_cn
3. 登录自己的谷歌账户
4. 点击中间的"开始使用"
5. 选择左边的"商务版使用一个月"
6. 如果出现网络连接错误，一直刷新即可
7. 输入自己的谷歌邮箱账号
8. 输入名字或直接点击"开始使用"

**重要提示：**
- 完全免费，无需绑定信用卡
- 商务版试用期一个月
- 需要VPN访问''',
    'website_url': 'https://cloud.google.com/gemini-enterprise?hl=zh_cn',
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
