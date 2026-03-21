#!/usr/bin/env python
"""
迁移工具分类脚本
将"1"分类中的所有工具移到"效率工具"分类，然后删除"1"分类
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

def migrate_category():
    try:
        # 查找"1"分类
        old_category = Category.objects.get(name='1')
        print(f'找到分类: {old_category.name} (ID: {old_category.id})')

        # 查找"效率工具"分类
        target_category = Category.objects.get(name='效率工具')
        print(f'目标分类: {target_category.name} (ID: {target_category.id})')

        # 获取"1"分类下的所有工具
        tools = Tool.objects.filter(category=old_category)
        tool_count = tools.count()
        print(f'\n找到 {tool_count} 个工具需要迁移:')

        for tool in tools:
            print(f'  - {tool.name}')

        # 迁移工具
        updated = tools.update(category=target_category)
        print(f'\n✅ 成功迁移 {updated} 个工具到"{target_category.name}"')

        # 删除"1"分类
        old_category.delete()
        print(f'✅ 已删除分类"{old_category.name}"')

        print('\n迁移完成！')

    except Category.DoesNotExist as e:
        print(f'❌ 错误: 找不到指定的分类 - {e}')
    except Exception as e:
        print(f'❌ 发生错误: {e}')

if __name__ == '__main__':
    migrate_category()
