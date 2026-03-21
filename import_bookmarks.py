#!/usr/bin/env python
"""
导入书签文件到数据库
从HTML书签文件中提取分类和工具，导入到Django数据库
"""
import os
import django
from bs4 import BeautifulSoup
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

def parse_bookmarks(html_file):
    """解析HTML书签文件"""
    with open(html_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    categories_data = []
    current_category = None

    # 查找所有DL标签（书签列表容器）
    for dl in soup.find_all('dl'):
        # 查找该DL前面的H3标签（分类名称）
        h3 = dl.find_previous_sibling('h3')
        if h3:
            category_name = h3.get_text(strip=True)
            if category_name:
                current_category = category_name
                categories_data.append({
                    'name': category_name,
                    'tools': []
                })

        # 提取该分类下的所有书签链接
        if current_category and categories_data:
            for a in dl.find_all('a', href=True):
                tool_data = {
                    'name': a.get_text(strip=True),
                    'url': a.get('href'),
                    'icon': a.get('icon', '')
                }
                if tool_data['name'] and tool_data['url']:
                    categories_data[-1]['tools'].append(tool_data)

    return categories_data

def import_to_database(categories_data):
    """导入数据到数据库"""
    stats = {'categories': 0, 'tools': 0, 'skipped': 0}

    for cat_data in categories_data:
        # 创建或获取分类
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={'slug': slugify(cat_data['name'], allow_unicode=True)}
        )
        if created:
            stats['categories'] += 1
            print(f'✅ 创建分类: {category.name}')

        # 导入该分类下的工具
        for tool_data in cat_data['tools']:
            # 检查URL是否已存在
            if Tool.objects.filter(website_url=tool_data['url']).exists():
                stats['skipped'] += 1
                continue

            # 生成唯一slug
            base_slug = slugify(tool_data['name'], allow_unicode=True)
            if not base_slug:
                import uuid
                base_slug = f"tool-{uuid.uuid4().hex[:8]}"
            slug = base_slug
            counter = 1
            while Tool.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            # 创建工具
            Tool.objects.create(
                name=tool_data['name'],
                slug=slug,
                short_description=f"来自书签: {tool_data['name']}",
                website_url=tool_data['url'],
                category=category,
                is_published=True
            )
            stats['tools'] += 1

    return stats

def main():
    html_file = os.path.expanduser('~/图片/奔跑中的奶酪5000个实用网站书签.html')

    print('开始解析书签文件...')
    categories_data = parse_bookmarks(html_file)
    print(f'解析完成，找到 {len(categories_data)} 个分类')

    print('\n开始导入数据库...')
    stats = import_to_database(categories_data)

    print(f'\n导入完成！')
    print(f'  新增分类: {stats["categories"]}')
    print(f'  新增工具: {stats["tools"]}')
    print(f'  跳过重复: {stats["skipped"]}')

if __name__ == '__main__':
    main()
