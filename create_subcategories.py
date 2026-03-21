#!/usr/bin/env python3
import os
import django
from django.utils.text import slugify
from collections import defaultdict

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

# 定义每个主分类的子分类及其关键词
SUBCATEGORY_MAPPING = {
    'AI工具': {
        'AI学习资源': {
            'keywords': ['教程', '课程', '学习', 'tutorial', 'course', 'learning', '入门', '教学'],
            'patterns': ['教程', '课程', '学习']
        },
        'AI研究论文': {
            'keywords': ['论文', 'paper', 'arxiv', '研究', 'research', 'publication', 'journal'],
            'patterns': ['论文', 'paper', 'arxiv']
        },
        'AI开发工具': {
            'keywords': ['工具', 'tool', 'framework', '框架', 'library', '库', 'api', 'gpu'],
            'patterns': ['工具', 'tool', 'gpu']
        },
        'AI求职招聘': {
            'keywords': ['招聘', '求职', 'job', '面试', 'career', '简历', '内推'],
            'patterns': ['招聘', '求职', 'job']
        },
        'AI学术会议': {
            'keywords': ['会议', 'conference', 'workshop', '研讨会', 'seminar', 'symposium'],
            'patterns': ['会议', 'conference', 'workshop']
        }
    },
    '图书阅读': {
        '电子书搜索': {
            'keywords': ['电子书', 'ebook', '图书', '书籍', 'book', '小说'],
            'patterns': ['书', 'book', 'ebook']
        },
        '学术论文': {
            'keywords': ['论文', 'paper', 'arxiv', '学术', 'academic', 'research'],
            'patterns': ['论文', 'paper', 'academic']
        },
        '在线阅读': {
            'keywords': ['阅读', 'read', '在线', 'online', '文档', 'doc'],
            'patterns': ['阅读', 'read']
        },
        '图书资源': {
            'keywords': ['资源', 'resource', '图书馆', 'library', '文献'],
            'patterns': ['资源', '图书馆']
        }
    },
    '设计素材': {
        '图片素材': {
            'keywords': ['图片', '素材', 'image', 'photo', '壁纸', '图标', 'icon'],
            'patterns': ['图片', '素材', 'image']
        },
        '设计工具': {
            'keywords': ['设计', 'design', 'ps', 'photoshop', '编辑', 'editor', '抠图'],
            'patterns': ['设计', 'design', '抠图']
        },
        '模板资源': {
            'keywords': ['模板', 'template', 'ppt', '样式'],
            'patterns': ['模板', 'template']
        },
        '表情包': {
            'keywords': ['表情', 'emoji', '表情包', 'sticker'],
            'patterns': ['表情']
        },
        '考试资料': {
            'keywords': ['考试', '资格证', '题库', '考证', '培训', '软考'],
            'patterns': ['考试', '考证', '题库']
        }
    },
    '资源下载': {
        '网盘资源': {
            'keywords': ['网盘', '百度云', '阿里云盘', 'pan', '云盘', '分享'],
            'patterns': ['网盘', '云盘', 'pan']
        },
        '文档下载': {
            'keywords': ['文档', '下载', 'pdf', 'doc', '文库', 'csdn'],
            'patterns': ['文档', '文库', 'pdf']
        },
        '游戏下载': {
            'keywords': ['游戏', 'game', '破解', '单机'],
            'patterns': ['游戏', 'game']
        },
        '论文下载': {
            'keywords': ['论文', 'paper', 'sci-hub', '学术'],
            'patterns': ['论文', 'sci-hub']
        },
        '标准规范': {
            'keywords': ['标准', '规范', 'standard', '国标'],
            'patterns': ['标准', '规范']
        }
    },
    '学习教育': {
        '机器学习': {
            'keywords': ['机器学习', 'machine learning', 'ml', '深度学习', 'deep learning'],
            'patterns': ['机器学习', '深度学习']
        },
        '编程教程': {
            'keywords': ['编程', 'programming', 'code', '代码', 'python', 'java'],
            'patterns': ['编程', 'programming', 'code']
        },
        '留学考试': {
            'keywords': ['留学', '考试', 'gre', 'toefl', '雅思', '托福'],
            'patterns': ['留学', '考试']
        },
        '在线课程': {
            'keywords': ['课程', 'course', 'mooc', '慕课', '网课'],
            'patterns': ['课程', 'course', 'mooc']
        }
    },
    '影视动漫': {
        '影视资源': {
            'keywords': ['电影', '电视', '影视', 'movie', 'video', '视频'],
            'patterns': ['电影', '影视', 'movie']
        },
        '视频教程': {
            'keywords': ['教程', 'tutorial', '讲座', 'lecture', '演讲'],
            'patterns': ['教程', 'tutorial', '讲座']
        },
        '动漫资源': {
            'keywords': ['动漫', 'anime', '漫画', 'manga'],
            'patterns': ['动漫', 'anime']
        }
    },
    '其他资源': {
        '方言词典': {
            'keywords': ['方言', '词典', '粤语', '潮汕', '闽南', '上海话'],
            'patterns': ['方言', '词典', '粤语']
        },
        '游戏娱乐': {
            'keywords': ['游戏', 'game', '娱乐', '排行'],
            'patterns': ['游戏', '娱乐']
        },
        '行业资讯': {
            'keywords': ['资讯', '新闻', '行业', '协会'],
            'patterns': ['资讯', '行业']
        },
        '其他工具': {
            'keywords': ['工具', 'tool'],
            'patterns': ['工具']
        }
    },
    '开发编程': {
        '编程学习': {
            'keywords': ['学习', '教程', 'tutorial', '入门', 'course'],
            'patterns': ['学习', '教程']
        },
        '代码资源': {
            'keywords': ['github', 'code', '代码', 'repository', '开源'],
            'patterns': ['github', 'code', '代码']
        },
        '开发社区': {
            'keywords': ['社区', 'community', '论坛', 'forum', '博客'],
            'patterns': ['社区', '论坛', '博客']
        },
        '技术博客': {
            'keywords': ['博客', 'blog', '技术', 'tech'],
            'patterns': ['博客', 'blog']
        }
    },
    '实用工具': {
        '在线工具': {
            'keywords': ['在线', 'online', '工具', 'tool', '转换'],
            'patterns': ['在线', '工具']
        },
        '格式转换': {
            'keywords': ['转换', 'convert', 'pdf', '格式'],
            'patterns': ['转换', 'convert']
        },
        '导航网站': {
            'keywords': ['导航', 'navigation', '网址'],
            'patterns': ['导航']
        }
    },
    '音乐音频': {
        '音乐下载': {
            'keywords': ['音乐', 'music', '下载', '无损', '网易云'],
            'patterns': ['音乐', 'music', '下载']
        },
        '音频素材': {
            'keywords': ['音频', 'audio', '素材', 'sound'],
            'patterns': ['音频', 'audio', '素材']
        },
        '音乐服务': {
            'keywords': ['spotify', 'netflix', '订阅', '会员'],
            'patterns': ['spotify', '订阅']
        }
    },
    '办公效率': {
        'PPT模板': {
            'keywords': ['ppt', 'powerpoint', '模板', '幻灯片'],
            'patterns': ['ppt', '模板']
        },
        '文档工具': {
            'keywords': ['文档', 'document', 'word', 'excel', '表格'],
            'patterns': ['文档', 'word', 'excel']
        },
        '写作翻译': {
            'keywords': ['写作', '翻译', 'translate', '校对'],
            'patterns': ['写作', '翻译']
        }
    },
    '生活服务': {
        '地图服务': {
            'keywords': ['地图', 'map', '导航', '地理'],
            'patterns': ['地图', 'map']
        },
        '购物优惠': {
            'keywords': ['购物', '优惠', '返利', '比价'],
            'patterns': ['购物', '优惠']
        }
    }
}

def categorize_tool(tool, parent_category, subcategories):
    """为工具分配子分类"""
    text = f"{tool.name} {tool.website_url}".lower()

    scores = defaultdict(int)
    for subcat_name, rules in subcategories.items():
        for keyword in rules['keywords']:
            if keyword in text:
                scores[subcat_name] += 1
        for pattern in rules['patterns']:
            if pattern in text:
                scores[subcat_name] += 2

    if scores:
        return max(scores.items(), key=lambda x: x[1])[0]
    return list(subcategories.keys())[0]  # 默认第一个子分类

print('开始创建子分类结构...\n')

stats = {'created': 0, 'migrated': 0}
category_cache = {}

for main_cat_name, subcats in SUBCATEGORY_MAPPING.items():
    try:
        main_category = Category.objects.get(name=main_cat_name)
        tools = main_category.tools.all()

        if tools.count() == 0:
            print(f'跳过 {main_cat_name}（无工具）')
            continue

        print(f'\n处理 {main_cat_name} ({tools.count()} 个工具)')

        # 创建子分类
        for subcat_name in subcats.keys():
            full_name = f"{main_cat_name} > {subcat_name}"
            cat, created = Category.objects.get_or_create(
                name=full_name,
                defaults={'slug': slugify(full_name, allow_unicode=True)}
            )
            category_cache[full_name] = cat
            if created:
                stats['created'] += 1
                print(f'  创建子分类: {subcat_name}')

        # 分配工具到子分类
        subcat_stats = defaultdict(int)
        for tool in tools:
            subcat_name = categorize_tool(tool, main_cat_name, subcats)
            full_name = f"{main_cat_name} > {subcat_name}"
            tool.category = category_cache[full_name]
            tool.save()
            stats['migrated'] += 1
            subcat_stats[subcat_name] += 1

            if stats['migrated'] % 500 == 0:
                print(f'  已迁移 {stats["migrated"]} 个工具...')

        print(f'  分配结果:')
        for subcat, count in sorted(subcat_stats.items(), key=lambda x: x[1], reverse=True):
            print(f'    {subcat}: {count} 个')

    except Category.DoesNotExist:
        print(f'警告: 未找到主分类 {main_cat_name}')

print(f'\n✓ 完成！')
print(f'  创建子分类: {stats["created"]} 个')
print(f'  迁移工具: {stats["migrated"]} 个')
