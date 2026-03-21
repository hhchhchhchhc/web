#!/usr/bin/env python3
import os
import django
from django.utils.text import slugify
from collections import defaultdict

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

# 定义分类关键词映射
CATEGORY_KEYWORDS = {
    'AI工具 > AI学习资源': ['教程', '课程', '学习', 'tutorial', 'course', 'learning'],
    'AI工具 > AI研究论文': ['论文', 'paper', 'arxiv', '研究', 'research'],
    'AI工具 > AI开发工具': ['开发', 'api', 'sdk', 'framework', '框架', 'library'],
    'AI工具 > AI求职招聘': ['招聘', '求职', 'job', '面试', 'career'],
    '设计素材 > 设计工具': ['设计', 'design', 'ps', 'photoshop', '抠图', '图片', 'image'],
    '设计素材 > 图片素材': ['素材', '壁纸', '图标', 'icon', 'photo'],
    '办公效率 > PPT模板': ['ppt', 'powerpoint', '幻灯片', '模板'],
    '办公效率 > 写作翻译': ['写作', '翻译', 'translate', '文案', '校对'],
    '开发编程 > 代码资源': ['github', 'code', '代码', '开源'],
    '开发编程 > 编程学习': ['编程', 'programming', 'python', 'java'],
    '影视动漫 > 影视资源': ['电影', '视频', 'video', 'movie'],
    '音乐音频 > 音乐下载': ['音乐', 'music', '歌曲'],
}

def categorize_tool(tool):
    """智能分类工具"""
    text = f"{tool.name} {tool.website_url} {tool.short_description}".lower()

    scores = defaultdict(int)
    for cat_name, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text:
                scores[cat_name] += 1

    if scores:
        return max(scores.items(), key=lambda x: x[1])[0]
    return None

print('开始重新分类工具...\n')

# 1. 处理ai-bot.cn导入的398个工具
print('1. 重新分类ai-bot.cn导入的工具...')
aibot_cat = Category.objects.get(name='AI写作工具')
aibot_tools = aibot_cat.tools.all()
print(f'   找到 {aibot_tools.count()} 个工具')

category_cache = {}
recategorized = 0

for tool in aibot_tools:
    new_cat_name = categorize_tool(tool)
    if not new_cat_name:
        continue

    if new_cat_name not in category_cache:
        cat, _ = Category.objects.get_or_create(
            name=new_cat_name,
            defaults={'slug': slugify(new_cat_name, allow_unicode=True)}
        )
        category_cache[new_cat_name] = cat

    tool.category = category_cache[new_cat_name]
    tool.save()
    recategorized += 1

print(f'   重新分类: {recategorized} 个\n')

# 2. 检查并修正其他工具的分类
print('2. 检查其他工具的分类...')
all_tools = Tool.objects.exclude(category__name='AI写作工具')
print(f'   检查 {all_tools.count()} 个工具')

adjusted = 0
for tool in all_tools:
    current_cat = tool.category.name
    suggested_cat = categorize_tool(tool)

    if suggested_cat and suggested_cat != current_cat:
        if suggested_cat not in category_cache:
            cat, _ = Category.objects.get_or_create(
                name=suggested_cat,
                defaults={'slug': slugify(suggested_cat, allow_unicode=True)}
            )
            category_cache[suggested_cat] = cat

        tool.category = category_cache[suggested_cat]
        tool.save()
        adjusted += 1

print(f'   调整分类: {adjusted} 个\n')

print(f'✓ 完成！')
print(f'  ai-bot.cn工具重新分类: {recategorized}')
print(f'  其他工具调整分类: {adjusted}')
