import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

# 创建AI课程分类
category, _ = Category.objects.get_or_create(
    name='AI课程',
    defaults={'description': 'AI相关的学习课程和教程', 'order': 5}
)

# 添加大模型面试专栏
tool, created = Tool.objects.get_or_create(
    name='大模型面试专栏课程',
    defaults={
        'short_description': '大模型面试必备课程，涵盖技术原理、面试技巧和实战经验',
        'full_description': '''大模型面试专栏课程，助你顺利通过AI岗位面试：
- 大模型技术原理深度讲解
- 常见面试题目和答题技巧
- 实战项目经验分享
- 行业最新动态和趋势
- 适合求职者和转行人员

百度网盘链接，提取码: cjjc''',
        'website_url': 'https://pan.baidu.com/s/1YYtaDSCmLkZukV90wdMOgQ?pwd=cjjc',
        'category': category,
        'is_published': True,
    }
)

if created:
    print(f'✅ 已添加: {tool.name}')
else:
    print(f'⚠️  已存在: {tool.name}')
