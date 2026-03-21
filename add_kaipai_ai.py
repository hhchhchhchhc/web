import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

# 创建智能剪辑分类
category, _ = Category.objects.get_or_create(
    name='智能剪辑',
    defaults={'description': 'AI驱动的视频剪辑工具', 'order': 6}
)

# 添加开拍 AI
tool, created = Tool.objects.get_or_create(
    name='开拍 AI',
    defaults={
        'short_description': '全自动剪辑工具，成品即发，大幅缩短后期制作时间',
        'full_description': '''开拍 AI是全自动智能剪辑工具：
- 自动完成剪辑、配音、字幕及素材匹配
- 节奏感强，成品质量高
- 大幅缩短后期制作时间
- 适合剪辑新手和追求效率的创作者
- 特别适合混剪或带货探店类内容

导入原始素材，AI自动生成成品，快速发布。''',
        'website_url': 'https://kaipai.ai',
        'category': category,
        'is_published': True,
    }
)

if created:
    print(f'✅ 已添加: {tool.name}')
else:
    print(f'⚠️  已存在: {tool.name}')
