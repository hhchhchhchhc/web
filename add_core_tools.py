#!/usr/bin/env python3
import os
import django
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

# 视频倍速工具
video_cat, _ = Category.objects.get_or_create(
    name='视频工具',
    defaults={'slug': slugify('视频工具', allow_unicode=True)}
)

Tool.objects.get_or_create(
    name='Video Speed Controller插件',
    defaults={
        'slug': slugify('Video Speed Controller插件', allow_unicode=True),
        'short_description': '普通网页视频0.07-16倍速随意切换',
        'full_description': '实现普通网页视频0.07-16倍速随意切换的浏览器插件',
        'website_url': 'https://share.note.youdao.com/share/?id=8a6ec1dbc0b011b52fb3338cf12ce02c&type=note',
        'category': video_cat,
        'is_published': True,
        'is_featured': True
    }
)

print('✓ 添加视频倍速插件')

# 创建核心分类
free_cat, _ = Category.objects.get_or_create(
    name='免费用最高级大模型',
    defaults={
        'slug': slugify('免费用最高级大模型', allow_unicode=True),
        'description': '免费使用Claude Opus 4.6等顶级AI模型的方法'
    }
)

print('✓ 创建"免费用最高级大模型"分类')

# 7个方法
methods = [
    {
        'name': 'Arena.ai无限用Opus 4.6',
        'url': 'https://arena.ai/',
        'desc': '无限使用Claude Opus 4.6的免费平台'
    },
    {
        'name': 'Ami.dev白嫖Opus',
        'url': 'https://www.ami.dev/docs/install',
        'desc': '配合2925无限邮箱自动机白嫖Opus额度'
    },
    {
        'name': 'Bolt.new白嫖',
        'url': 'https://bolt.new/',
        'desc': '白嫖bolt.new的AI模型额度'
    },
    {
        'name': 'Antigravity2API Opus',
        'url': 'https://antigravity.dev/',
        'desc': '使用Google Pro账号通过antigravity2api访问Opus'
    },
    {
        'name': 'GitHub Copilot Pro教育优惠',
        'url': 'https://education.github.com/',
        'desc': '学生可申请2个账号，包含Opus 4.6访问权限'
    },
    {
        'name': 'AnyRouter注册福利',
        'url': 'https://anyrouter.ai/',
        'desc': '注册送50刀，邀请送50刀，签到送25刀，教育邮箱送75刀'
    },
    {
        'name': 'Google Droid白嫖',
        'url': 'https://droid.google.com/',
        'desc': '每个谷歌号白嫖1k万token以上，可批量注册谷歌号'
    }
]

for method in methods:
    slug = slugify(method['name'], allow_unicode=True)
    counter = 1
    while Tool.objects.filter(slug=slug).exists():
        slug = f"{slugify(method['name'], allow_unicode=True)}-{counter}"
        counter += 1

    Tool.objects.create(
        name=method['name'],
        slug=slug,
        short_description=method['desc'],
        full_description=method['desc'],
        website_url=method['url'],
        category=free_cat,
        is_published=True,
        is_featured=True
    )
    print(f'✓ {method["name"]}')

print(f'\n完成！添加了8个工具')
