#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

# 工具数据（移除DecompGRU相关内容）
tool_data = {
    'name': '🎁 知识星球限时福利 - 免费VPS+学术论文+Opus 4.6',
    'short_description': '加入知识星球获取：免费VPS、学术论文下载、Opus 4.6无限用、量化策略源码、Tardis数据等超值福利',
    'full_description': '''## 🎁 加入「财富自由之路」知识星球获取超值福利

**入群福利（星球票价199元）：**
- 一年2核2G VPS服务器（价值200-800元）
- 永久免费下载知网、万方、维普等学术论文
- Claude Opus 4.6无限使用
- 量化交易策略源码
- Tardis高频数据访问
- 专业投资交流社群

**适合人群：**
- 量化交易研究者
- 学术论文需求者
- AI工具使用者
- 投资学习者

加入即可获得以上所有福利，性价比极高。''',
    'website_url': 'https://t.zsxq.com/Fed8e',
    'category_name': '🎁 限时福利'
}

# 添加工具
try:
    category = Category.objects.get(name=tool_data['category_name'])

    tool, created = Tool.objects.get_or_create(
        name=tool_data['name'],
        defaults={
            'short_description': tool_data['short_description'],
            'full_description': tool_data['full_description'],
            'website_url': tool_data['website_url'],
            'category': category
        }
    )

    if created:
        print(f'✓ 已恢复工具: {tool.name}')
        print(f'  分类: {category.name}')
        print(f'  URL: {tool.website_url}')
        print(f'\n✓ 已移除DecompGRU相关描述')
    else:
        # 如果工具已存在，更新描述
        tool.short_description = tool_data['short_description']
        tool.full_description = tool_data['full_description']
        tool.save()
        print(f'✓ 已更新工具: {tool.name}')
        print(f'  分类: {category.name}')
        print(f'  URL: {tool.website_url}')
        print(f'\n✓ 已移除DecompGRU相关描述')
except Category.DoesNotExist:
    print(f'✗ 分类不存在: {tool_data["category_name"]}')
except Exception as e:
    print(f'✗ 操作失败: {e}')
