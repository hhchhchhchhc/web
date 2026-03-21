import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

# 创建AI搜索分类
category, _ = Category.objects.get_or_create(
    name='AI搜索',
    defaults={'description': 'AI驱动的智能搜索工具', 'order': 2}
)

# 更新seekall.ai
tool = Tool.objects.get(name='Seekall.ai')
tool.category = category
tool.short_description = '一键咨询几十个大模型，快速获取AI答案'
tool.full_description = '''Seekall.ai让你一键咨询几十个大模型：
- 同时查询ChatGPT、Claude、Gemini等主流大模型
- 对比不同模型的回答质量
- 快速找到最佳答案
- 节省切换多个平台的时间
- 提升AI使用效率10倍

一个工具，搞定所有大模型。'''
tool.save()

print(f'✅ 已更新: {tool.name}')
print(f'   分类: {tool.category.name}')
print(f'   描述: {tool.short_description}')
