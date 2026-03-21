#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Tool, Category

category = Category.objects.get(id=706)

tools_data = [
    {
        'name': 'OpenCode + GLM-4.7 - 完全免费开源方案',
        'slug': 'opencode-glm47-free',
        'short_description': '类似Claude Code的开源IDE，配合GLM-4.7模型完全免费使用，适合代码编写和调试',
        'full_description': '''OpenCode + GLM-4.7 - 完全免费开源方案

✅ 推荐指数：⭐⭐⭐⭐

免费额度：完全免费，本地部署
模型：GLM-4.7（智谱AI开源模型）
特点：类似Claude Code的开源IDE，完全免费

使用方法：
1. 下载OpenCode IDE（基于VS Code）
2. 配置GLM-4.7模型（支持本地或API调用）
3. 获得类似Claude的代码辅助功能
4. 完全免费，无使用限制

适用场景：
• 代码编写和调试
• 技术文档生成
• 不需要Claude最高级推理能力的场景''',
        'website_url': 'https://github.com/opencode',
    },
]

print(f'准备添加 {len(tools_data)} 个开源工具\n')

for tool_data in tools_data:
    existing = Tool.objects.filter(slug=tool_data['slug']).first()
    if existing:
        print(f'⏭️  跳过已存在: {tool_data["name"]}')
        continue

    tool = Tool.objects.create(**{**tool_data, 'category': category, 'is_featured': True, 'is_published': True})
    print(f'✅ 成功添加: {tool.name}')

print('\n完成开源工具添加！')
