#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Tool, Category

category = Category.objects.get(id=706)

tools_data = [
    {
        'name': 'laozhang.ai - 国内直连Claude API',
        'slug': 'laozhangai-china-direct',
        'short_description': '国内可直接访问的Claude API平台，无需科学上网，新用户赠送体验额度，支持Claude 3.5 Sonnet等模型',
        'full_description': '''laozhang.ai - 国内直连Claude API

💡 推荐指数：⭐⭐⭐⭐

免费额度：新用户赠送一定额度
支持模型：Claude 3.5 Sonnet、GPT-4等
特点：国内可直接访问，无需科学上网

使用方法：
1. 访问 laozhang.ai 注册账号
2. 完成实名认证（国内平台要求）
3. 获取API密钥
4. 使用OpenAI兼容格式调用

注意事项：
• 国内平台需遵守相关法律法规
• 需要实名认证
• 价格通常比官方略高
• 选择信誉良好的平台，注意数据隐私''',
        'website_url': 'https://laozhang.ai',
    },
]

print(f'准备添加 {len(tools_data)} 个国内平台工具\n')

for tool_data in tools_data:
    existing = Tool.objects.filter(slug=tool_data['slug']).first()
    if existing:
        print(f'⏭️  跳过已存在: {tool_data["name"]}')
        continue

    tool = Tool.objects.create(**{**tool_data, 'category': category, 'is_featured': True, 'is_published': True})
    print(f'✅ 成功添加: {tool.name}')

print('\n完成国内平台工具添加！')
