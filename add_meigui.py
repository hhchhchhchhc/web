import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

# 创建内容创作分类
category, _ = Category.objects.get_or_create(
    name='内容创作',
    defaults={'description': 'AI驱动的内容创作和营销工具', 'order': 7}
)

# 添加玫瑰小程序
tool, created = Tool.objects.get_or_create(
    name='玫瑰小程序',
    defaults={
        'short_description': 'AI图文带货工具，一键生成小红书/抖音笔记内容',
        'full_description': '''玫瑰小程序是专业的AI图文带货工具：
- 适合不想拍视频、专注图文带货的创作者
- 上传产品图+填写卖点，AI自动优化文案
- 自动生成符合平台风格的图文内容（标题、文案、标签）
- 一键发布至小红书/抖音，流程丝滑
- 高效产出平台适配内容

操作简单：创作 → 笔记一条龙 → 笔记图 → 上传图片 → AI生成 → 发布''',
        'website_url': 'https://weixin.qq.com',
        'category': category,
        'is_published': True,
    }
)

if created:
    print(f'✅ 已添加: {tool.name}')
else:
    print(f'⚠️  已存在: {tool.name}')
