import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

# 获取或创建AI工具分类
category, _ = Category.objects.get_or_create(
    name='AI工具',
    defaults={'description': 'AI相关工具和服务', 'order': 1}
)

# 添加seekall.ai
tool, created = Tool.objects.get_or_create(
    name='Seekall.ai',
    defaults={
        'short_description': 'AI驱动的智能搜索插件，提升搜索效率和准确度',
        'full_description': '''Seekall.ai是一款AI驱动的智能搜索插件：
- 智能理解搜索意图
- 聚合多个搜索引擎结果
- AI总结和提炼关键信息
- 提升搜索效率10倍以上
- 支持多种浏览器

让搜索更智能，节省大量时间。''',
        'website_url': 'https://seekall.ai',
        'category': category,
        'is_published': True,
    }
)

if created:
    print(f'✅ 已添加: {tool.name}')
else:
    print(f'⚠️  已存在: {tool.name}')
