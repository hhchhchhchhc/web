import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

# 获取分类
ai_course = Category.objects.get(name='AI课程')
fuye_zhuanqian = Category.objects.get(name='副业赚钱')

# 找到这两个工具
tools_to_move = [
    '2026年AI视频变现全攻略',
    'AI复刻技术短视频变现教程'
]

for tool_name in tools_to_move:
    try:
        tool = Tool.objects.get(name=tool_name, category=ai_course)
        tool.category = fuye_zhuanqian
        tool.save()
        print(f'✅ 已移动: {tool_name}')
    except Tool.DoesNotExist:
        print(f'⚠️  未找到: {tool_name}')

print(f'\n完成！现在"副业赚钱"分类共有 {Tool.objects.filter(category=fuye_zhuanqian).count()} 个工具')
