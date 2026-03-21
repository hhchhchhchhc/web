import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

# 创建副业赚钱分类
category, _ = Category.objects.get_or_create(
    name='副业赚钱',
    defaults={'description': '正规无门槛的副业和赚钱方法', 'order': 15}
)

# 添加网盘拉新
tool, created = Tool.objects.get_or_create(
    name='网盘拉新副业',
    defaults={
        'short_description': '正规无门槛的副业，通过推广网盘获得收益',
        'full_description': '''网盘拉新是一个正规无门槛的副业项目：
- 无需投资，零成本启动
- 推广主流网盘平台（百度网盘、阿里云盘等）
- 每成功邀请一个用户获得佣金
- 适合学生、宝妈、上班族等所有人群
- 时间自由，随时随地可做

详细教程和操作方法请查看文章。''',
        'website_url': 'https://mp.weixin.qq.com/s/raWsl7Ixd8N0ydqBZn7hjA',
        'category': category,
        'is_published': True,
    }
)

if created:
    print(f'✅ 已添加: {tool.name}')
else:
    print(f'⚠️  已存在: {tool.name}')
