#!/usr/bin/env python3
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category

# 从HTML菜单提取的正确分类URL映射
CATEGORY_URLS = {
    'AI写作工具': 'https://ai-bot.cn/favorites/ai-writing-tools/',
    'AI图像工具': 'https://ai-bot.cn/favorites/ai-image-tools/',
    'AI视频工具': 'https://ai-bot.cn/favorites/ai-video-tools/',
    'AI办公工具': 'https://ai-bot.cn/favorites/ai-office-tools/',
    'AI智能体': 'https://ai-bot.cn/favorites/ai-agent/',
    'AI聊天助手': 'https://ai-bot.cn/favorites/ai-chatbots/',
    'AI编程工具': 'https://ai-bot.cn/favorites/ai-programming-tools/',
    'AI设计工具': 'https://ai-bot.cn/favorites/ai-design-tools/',
    'AI音频工具': 'https://ai-bot.cn/favorites/ai-audio-tools/',
    'AI搜索引擎': 'https://ai-bot.cn/favorites/ai-search-engines/',
    'AI开发平台': 'https://ai-bot.cn/favorites/ai-frameworks/',
    'AI学习网站': 'https://ai-bot.cn/favorites/websites-to-learn-ai/',
    'AI训练模型': 'https://ai-bot.cn/favorites/ai-models/',
    'AI内容检测': 'https://ai-bot.cn/favorites/ai-content-detection-and-optimization-tools/',
    'AI提示指令': 'https://ai-bot.cn/favorites/ai-prompt-tools/',
}

print('更新分类URL...\n')

updated = 0
for cat_name, cat_url in CATEGORY_URLS.items():
    try:
        cat = Category.objects.get(name=cat_name)
        cat.url = cat_url
        cat.save()
        print(f'✓ {cat_name}')
        updated += 1
    except Category.DoesNotExist:
        print(f'✗ 未找到: {cat_name}')

print(f'\n完成！更新了 {updated} 个分类')
