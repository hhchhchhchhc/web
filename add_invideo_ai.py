#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

category = Category.objects.get(name='AI视频工具')

tool_data = {
    'name': 'Invideo AI - 一键生成商用广告视频',
    'short_description': '提示即可生成专业广告视频，150美元重制星巴克7900万观看广告',
    'full_description': '''**平台亮点：**
Invideo AI 是一款强大的AI视频广告生成工具，能够通过简单的文字提示快速创建专业级商用广告视频。

**成功案例：**
- 星巴克原版广告获得7900万次观看
- Invideo仅用150美元成功重制该广告
- 创始人和企业现在只需提示和点击即可创建自己的广告

**核心功能：**
- 一键生成商用广告视频
- AI自动匹配素材和配乐
- 专业级视频剪辑效果
- 支持多种广告风格和场景
- 快速迭代和修改

**适用场景：**
- 品牌广告制作
- 产品宣传视频
- 社交媒体营销
- 电商推广视频

**使用方式：**
可以免费体验基础功能，快速上手制作专业广告视频。''',
    'website_url': 'https://invideo.io/',
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
