import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category

# 添加网盘资源分类
category, created = Category.objects.get_or_create(
    name='网盘资源',
    defaults={
        'description': '优质网盘资源和资料分享',
        'order': 16
    }
)

if created:
    print(f'✅ 已添加分类: {category.name}')
else:
    print(f'⚠️  分类已存在: {category.name}')
