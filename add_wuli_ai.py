#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

category = Category.objects.get(name='免费用最高级大模型')

tool_data = {
    'name': '呜哩AI - 一站式AIGC创意平台',
    'short_description': '集成通义万相、即梦、可灵等顶级国产AI模型，免费积分体系',
    'full_description': '''**平台特色：**
呜哩 AI (wuli.art) 是一站式AIGC创意平台，集成了国内最顶尖的多个大模型能力，无需在多个平台注册和付费。

**集成的顶级模型：**
- 通义万相 2.6 (Alibaba) - 擅长艺术风格和写实摄影，中文理解极强
- Seedream 4.5 / 即梦 (ByteDance) - 光影处理和细节表现出色
- 可灵 Q1 (Kuaishou) - 国产AI视频"天花板"，支持文生视频和图生视频
- Qwen Image 2.0 - 阿里最新多模态图像生成模型

**核心功能：**
- 图片生成：参考生图、高清修复、多种艺术风格
- 视频生成：文生视频、图生视频、高质量输出
- 生成速度：图片几秒到十几秒，视频1-2分钟
- 分辨率：支持2K/4K高清增强输出

**免费使用方式：**
- 每日签到获取积分
- 邀请好友赠送积分
- 活动奖励免费额度

**使用技巧：**
- 画人像选Seedream模型
- 画艺术海报选通义万相
- 视频生成选可灵Q1
- 灵活切换模型发挥各自长处''',
    'website_url': 'https://wuli.art/',
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
