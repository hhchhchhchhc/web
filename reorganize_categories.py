#!/usr/bin/env python3
import os
import django
from django.utils.text import slugify
from collections import defaultdict

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

# 定义新的分类体系
CATEGORY_MAPPING = {
    'AI工具': {
        'keywords': ['ai', 'gpt', 'chatgpt', '智能', '生成', 'midjourney', 'stable diffusion'],
        'patterns': ['ai', 'gpt', '智能']
    },
    '影视动漫': {
        'keywords': ['影视', '电影', '电视', '动漫', '视频', '直播', '纪录片', '短剧'],
        'patterns': ['影视', '动漫', '视频', '电影']
    },
    '音乐音频': {
        'keywords': ['音乐', '音频', '歌曲', 'spotify', '网易云'],
        'patterns': ['音乐', '音频']
    },
    '图书阅读': {
        'keywords': ['电子书', '图书', '小说', '阅读', '古籍', 'pdf', 'epub'],
        'patterns': ['书', '阅读', '小说']
    },
    '学习教育': {
        'keywords': ['学习', '教育', '课程', '培训', '考试', '考证', '搜题', '慕课', '四六级'],
        'patterns': ['学习', '教育', '考']
    },
    '设计素材': {
        'keywords': ['设计', '素材', '图片', '壁纸', '模板', 'ps', 'pr', 'ae', '字体', '图标'],
        'patterns': ['设计', '素材', '图片', '壁纸']
    },
    '开发编程': {
        'keywords': ['开发', '编程', 'github', 'code', '代码', 'api', '技术'],
        'patterns': ['开发', '编程', '代码']
    },
    '办公效率': {
        'keywords': ['办公', 'ppt', 'word', 'excel', '文档', '写作', '翻译', '简历'],
        'patterns': ['办公', 'ppt', '文档']
    },
    '资源下载': {
        'keywords': ['下载', '网盘', '磁力', 'bt', '种子', '资源', '软件下载'],
        'patterns': ['下载', '网盘', '磁力']
    },
    '实用工具': {
        'keywords': ['工具', '转换', '压缩', '解析', '查询', '搜索', '导航'],
        'patterns': ['工具', '转换', '查询']
    },
    '生活服务': {
        'keywords': ['地图', '天气', '购物', '旅游', '美食', '健康'],
        'patterns': ['地图', '购物', '旅游']
    }
}

def categorize_tool(name, url, old_category):
    """智能分类工具"""
    text = f"{name} {url} {old_category}".lower()

    scores = defaultdict(int)
    for cat_name, rules in CATEGORY_MAPPING.items():
        for keyword in rules['keywords']:
            if keyword in text:
                scores[cat_name] += 1
        for pattern in rules['patterns']:
            if pattern in text:
                scores[cat_name] += 2

    if scores:
        return max(scores.items(), key=lambda x: x[1])[0]
    return '其他资源'

print('开始智能重组分类...')

# 获取所有工具
tools = Tool.objects.all()
print(f'找到 {tools.count()} 个工具')

# 分析并重新分类
new_categories = defaultdict(list)
for tool in tools:
    old_cat = tool.category.name if tool.category else '未分类'
    new_cat = categorize_tool(tool.name, tool.website_url, old_cat)
    new_categories[new_cat].append(tool)

print(f'\n新分类统计:')
for cat_name, tools_list in sorted(new_categories.items(), key=lambda x: len(x[1]), reverse=True):
    print(f'  {cat_name}: {len(tools_list)} 个')

print('\n创建新分类并迁移工具...')
category_cache = {}
migrated = 0

for cat_name, tools_list in new_categories.items():
    if cat_name not in category_cache:
        cat, created = Category.objects.get_or_create(
            name=cat_name,
            defaults={'slug': slugify(cat_name, allow_unicode=True)}
        )
        category_cache[cat_name] = cat

    category = category_cache[cat_name]
    for tool in tools_list:
        tool.category = category
        tool.save()
        migrated += 1
        if migrated % 500 == 0:
            print(f'  已迁移 {migrated}/{tools.count()}')

print(f'\n✓ 完成！共迁移 {migrated} 个工具到 {len(category_cache)} 个新分类')

# 删除旧的空分类
print('\n清理旧分类...')
deleted = Category.objects.filter(tools__isnull=True).delete()
print(f'✓ 删除了 {deleted[0]} 个空分类')
