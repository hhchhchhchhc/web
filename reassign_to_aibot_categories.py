#!/usr/bin/env python3
import os
import django
from collections import defaultdict

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

CATEGORY_KEYWORDS = {
    'AI写作工具': ['写作', '文案', '小说', '论文', 'write', 'writer', 'writing'],
    'AI图像工具': ['图像', '图片', '绘画', '画图', 'image', 'photo', 'draw', 'paint'],
    'AI视频工具': ['视频', 'video', '剪辑'],
    'AI办公工具': ['办公', 'office', 'ppt', 'excel'],
    'AI智能体': ['智能体', 'agent', 'gpt'],
    'AI聊天助手': ['聊天', 'chat', '对话', '助手', 'assistant'],
    'AI编程工具': ['编程', '代码', 'code', 'program', 'dev'],
    'AI设计工具': ['设计', 'design', 'ui', 'ux'],
    'AI音频工具': ['音频', '音乐', 'audio', 'music', '语音'],
    'AI搜索引擎': ['搜索', 'search', '引擎'],
    'AI开发平台': ['开发', '平台', 'api', 'sdk', 'framework'],
    'AI学习网站': ['学习', '教程', '课程', 'learn', 'tutorial'],
    'AI训练模型': ['模型', 'model', 'gpt', 'llm'],
    'AI内容检测': ['检测', 'detect', '查重'],
    'AI提示指令': ['提示', 'prompt', '指令'],
}

def categorize_tool(tool):
    text = f"{tool.name} {tool.website_url} {tool.short_description}".lower()
    scores = defaultdict(int)

    for cat_name, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text:
                scores[cat_name] += 1

    if scores:
        return max(scores.items(), key=lambda x: x[1])[0]
    return None

print('重新分配工具到aibot分类...\n')

category_cache = {}
for cat_name in CATEGORY_KEYWORDS.keys():
    try:
        category_cache[cat_name] = Category.objects.get(name=cat_name)
    except Category.DoesNotExist:
        pass

tools = Tool.objects.all()
reassigned = 0

for tool in tools:
    new_cat_name = categorize_tool(tool)
    if new_cat_name and new_cat_name in category_cache:
        if tool.category.name != new_cat_name:
            tool.category = category_cache[new_cat_name]
            tool.save()
            reassigned += 1
            if reassigned % 100 == 0:
                print(f'已重新分配 {reassigned} 个工具...')

print(f'\n完成！重新分配了 {reassigned} 个工具')

print('\n各分类工具数量:')
for cat_name, cat in category_cache.items():
    print(f'{cat_name}: {cat.tools.count()} 个工具')
