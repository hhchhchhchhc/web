#!/usr/bin/env python3
import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

# 加载aibot.html中的工具顺序
with open('/tmp/aibot_tool_order.json', 'r', encoding='utf-8') as f:
    aibot_order = json.load(f)

CATEGORIES = [
    'AI写作工具', 'AI图像工具', 'AI视频工具', 'AI办公工具', 'AI智能体',
    'AI聊天助手', 'AI编程工具', 'AI设计工具', 'AI音频工具', 'AI搜索引擎',
    'AI开发平台', 'AI学习网站', 'AI训练模型', 'AI内容检测', 'AI提示指令'
]

# 知名工具关键词（提高优先级）
PRIORITY_KEYWORDS = [
    'chatgpt', 'claude', 'gemini', 'gpt', 'openai', 'midjourney', 'stable diffusion',
    'github', 'copilot', 'cursor', 'notion', 'figma', 'canva', 'adobe'
]

def score_tool(tool, aibot_urls, position):
    score = 0

    # aibot.html中的位置得分（越靠前分数越高）
    if tool.website_url in aibot_urls:
        idx = aibot_urls.index(tool.website_url)
        score += 1000 - idx * 10  # 前面的工具得分更高

    # 知名工具加分
    name_lower = tool.name.lower()
    url_lower = tool.website_url.lower()
    for keyword in PRIORITY_KEYWORDS:
        if keyword in name_lower or keyword in url_lower:
            score += 100
            break

    return score

print('开始筛选精华工具...\n')

total_deleted = 0
for cat_name in CATEGORIES:
    try:
        cat = Category.objects.get(name=cat_name)
    except Category.DoesNotExist:
        continue

    tools = list(cat.tools.all())
    aibot_urls = aibot_order.get(cat_name, [])

    # 计算每个工具的得分
    tool_scores = []
    for i, tool in enumerate(tools):
        score = score_tool(tool, aibot_urls, i)
        tool_scores.append((tool, score))

    # 按得分排序
    tool_scores.sort(key=lambda x: x[1], reverse=True)

    # 保留前30个
    keep_count = min(30, len(tool_scores))
    to_keep = [t[0] for t in tool_scores[:keep_count]]
    to_delete = [t[0] for t in tool_scores[keep_count:]]

    # 删除低分工具
    for tool in to_delete:
        tool.delete()
        total_deleted += 1

    print(f'{cat_name}: 保留 {len(to_keep)}, 删除 {len(to_delete)}')

print(f'\n完成！共删除 {total_deleted} 个工具')
