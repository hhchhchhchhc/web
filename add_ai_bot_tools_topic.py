#!/usr/bin/env python3
import os
import re
import shutil
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, TopicPage

SOURCE_TXT = '/home/user/图片/ai_bot_tools_分类排版.txt'
STATIC_TXT = 'static/ai_bot_tools_分类排版.txt'
TOPIC_SLUG = 'ai-bot-tools-categories-5000'

CATEGORY_HEADER_RE = re.compile(r'^分类:\s*(.*?)\s+数量:\s*(\d+)\s*$', re.MULTILINE)
ITEM_RE = re.compile(r'^\d+\.\s*(.*?)\n\s*链接:\s*(\S+)\s*$', re.MULTILINE)
TOTAL_RE = re.compile(r'总工具数:\s*(\d+)')


def ensure_category(name: str, desc: str, order: int = 0):
    cat, _ = Category.objects.get_or_create(
        name=name,
        defaults={'description': desc, 'order': order},
    )
    return cat


def parse_sections(text: str):
    headers = list(CATEGORY_HEADER_RE.finditer(text))
    sections = []
    for i, m in enumerate(headers):
        start = m.end()
        end = headers[i + 1].start() if i + 1 < len(headers) else len(text)
        body = text[start:end]
        items = ITEM_RE.findall(body)
        sections.append({
            'name': m.group(1).strip(),
            'count': int(m.group(2)),
            'items': items,
        })
    return sections


def build_intro(text: str, sections: list[dict], sample_per_category: int = 30):
    total = TOTAL_RE.search(text)
    total_count = int(total.group(1)) if total else sum(s['count'] for s in sections)

    lines = [
        '来源文件：ai_bot_tools_分类排版.txt（ai-bot.cn/ai-tools/page/1-500）',
        f'总工具数：{total_count}',
        f'分类数：{len(sections)}',
        '',
        '以下为每个分类的代表性条目（每类最多展示前 30 条）：',
        '',
    ]

    for sec in sections:
        lines.append(f"【{sec['name']}】共 {sec['count']} 个")
        if not sec['items']:
            lines.append('- 暂无可解析条目')
            lines.append('')
            continue

        sampled = sec['items'][:sample_per_category]
        for name, url in sampled:
            lines.append(f'- {name} | {url}')

        omitted = max(0, sec['count'] - len(sampled))
        if omitted > 0:
            lines.append(f'- ……其余 {omitted} 个见完整清单')
        lines.append('')

    lines.append('完整清单路径：/static/ai_bot_tools_分类排版.txt')
    return '\n'.join(lines)


def main():
    if not os.path.exists(SOURCE_TXT):
        raise FileNotFoundError(f'找不到源文件: {SOURCE_TXT}')

    os.makedirs('static', exist_ok=True)
    shutil.copyfile(SOURCE_TXT, STATIC_TXT)

    text = open(SOURCE_TXT, 'r', encoding='utf-8').read()
    sections = parse_sections(text)
    intro = build_intro(text, sections)

    categories = [
        ensure_category('AI工具', 'AI 工具集合与导航', 1),
        ensure_category('AI编程开发', 'AI 编程、框架与开发工具', 2),
    ]

    topic, created = TopicPage.objects.update_or_create(
        slug=TOPIC_SLUG,
        defaults={
            'title': 'AI Bot 工具分类排版（5000工具）',
            'meta_description': '基于 ai-bot.cn 的 5000 个工具分类清单，按分类汇总并展示代表条目，附完整原始列表。',
            'intro': intro,
            'is_published': True,
        }
    )
    topic.categories.set(categories)

    print('✅ 原始文件已复制到 static/ai_bot_tools_分类排版.txt')
    print(('✅ 已创建专题: ' if created else '♻️ 已更新专题: ') + topic.title)
    print(f'✅ 专题 slug: {topic.slug}')
    print(f'✅ 分类数: {len(sections)}')


if __name__ == '__main__':
    main()
