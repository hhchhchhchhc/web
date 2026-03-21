#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

category = Category.objects.get(name='AI工具')

tool_data = {
    'name': 'Claude Cowork最强免费替代品全面调研',
    'short_description': 'Anthropic Claude Cowork的开源免费替代方案深度对比，推荐Open Interpreter+本地模型',
    'full_description': '2026年2月最新调研报告，全面对比Claude Cowork与开源替代品。重点推荐Open Interpreter+本地模型+browser-use组合，实现接近0成本的AI Agent自动化。详细对比Open Interpreter、OpenHands、LangGraph、CrewAI等方案的能力、成本和适用场景。',
    'website_url': 'https://linux.do/t/topic/302831'
}

tool, created = Tool.objects.get_or_create(
    name=tool_data['name'],
    defaults={
        **tool_data,
        'category': category
    }
)

if created:
    print(f'✓ 已添加: {tool.name} → {category.name}')
else:
    print(f'- 已存在: {tool.name}')

print('\n完成！')
