#!/usr/bin/env python3
import os
import django
import subprocess
from bs4 import BeautifulSoup
from django.utils.text import slugify
import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

def fetch_page(url):
    """获取页面内容"""
    try:
        result = subprocess.run(['curl', '-s', '-L', url], capture_output=True, text=True, timeout=30)
        if result.returncode == 0 and result.stdout:
            return result.stdout
        print(f'curl返回码: {result.returncode}, stderr: {result.stderr[:200]}')
        return None
    except Exception as e:
        print(f'获取失败 {url}: {e}')
        return None

def extract_tools_from_homepage(html):
    """从首页提取工具链接和分类"""
    soup = BeautifulSoup(html, 'html.parser')
    tools_data = []

    # 查找所有工具卡片
    cards = soup.find_all('div', class_='url-card')
    print(f'找到 {len(cards)} 个工具卡片')

    for card in cards:
        link = card.find('a')
        if link and link.get('href'):
            detail_url = link.get('href')
            if detail_url.startswith('https://ai-bot.cn/sites/'):
                tools_data.append({'detail_url': detail_url})

    return tools_data

def extract_tool_info(html, detail_url):
    """从详情页提取工具信息"""
    soup = BeautifulSoup(html, 'html.parser')

    # 提取工具名称
    title = soup.find('h1', class_='post-title')
    name = title.get_text(strip=True) if title else '未知工具'

    # 提取实际URL
    go_link = soup.find('a', class_='go-link')
    website_url = go_link.get('href') if go_link else detail_url

    # 提取描述
    content = soup.find('div', class_='entry-content')
    description = content.get_text(strip=True)[:300] if content else name

    # 提取分类
    category_link = soup.find('a', rel='category tag')
    category_name = category_link.get_text(strip=True) if category_link else 'AI工具'

    return {
        'name': name,
        'website_url': website_url,
        'description': description,
        'category': category_name
    }

def import_to_database(tools_data):
    """导入到数据库"""
    stats = {'categories': 0, 'tools': 0, 'skipped': 0}
    category_cache = {}

    for tool_data in tools_data:
        # 创建或获取分类
        cat_name = tool_data['category']
        if cat_name not in category_cache:
            cat, created = Category.objects.get_or_create(
                name=cat_name,
                defaults={'slug': slugify(cat_name, allow_unicode=True)}
            )
            category_cache[cat_name] = cat
            if created:
                stats['categories'] += 1

        # 检查是否已存在
        if Tool.objects.filter(website_url=tool_data['website_url']).exists():
            stats['skipped'] += 1
            continue

        # 创建工具
        base_slug = slugify(tool_data['name'], allow_unicode=True) or f"tool-{hash(tool_data['website_url'])}"
        slug = base_slug
        counter = 1
        while Tool.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        Tool.objects.create(
            name=tool_data['name'],
            slug=slug,
            short_description=tool_data['description'][:300],
            full_description=tool_data['description'],
            website_url=tool_data['website_url'],
            category=category_cache[cat_name],
            is_published=True
        )
        stats['tools'] += 1

        if stats['tools'] % 50 == 0:
            print(f"  已导入 {stats['tools']} 个工具...")

    return stats

def main():
    print('开始爬取 ai-bot.cn...\n')

    # 1. 获取首页
    print('1. 获取首页...')
    homepage_html = fetch_page('https://ai-bot.cn/')
    if not homepage_html:
        print('无法获取首页，退出')
        return

    # 2. 提取工具链接
    print('2. 提取工具链接...')
    tools_list = extract_tools_from_homepage(homepage_html)
    print(f'找到 {len(tools_list)} 个工具\n')

    # 3. 爬取每个工具详情页
    print('3. 爬取工具详情...')
    tools_data = []
    for i, tool in enumerate(tools_list, 1):
        print(f'  [{i}/{len(tools_list)}] {tool["detail_url"]}')

        detail_html = fetch_page(tool['detail_url'])
        if detail_html:
            tool_info = extract_tool_info(detail_html, tool['detail_url'])
            tools_data.append(tool_info)

        time.sleep(1)  # 延迟1秒

        if i >= 50:  # 限制前50个工具用于测试
            print(f'\n  (测试模式：仅爬取前50个工具)')
            break

    # 4. 导入数据库
    print(f'\n4. 导入数据库...')
    stats = import_to_database(tools_data)

    print(f'\n✓ 完成！')
    print(f'  新增分类: {stats["categories"]}')
    print(f'  新增工具: {stats["tools"]}')
    print(f'  跳过重复: {stats["skipped"]}')

if __name__ == '__main__':
    main()
