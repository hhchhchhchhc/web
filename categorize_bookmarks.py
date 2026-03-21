#!/usr/bin/env python3
import os
import django
import re
from collections import defaultdict

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool
from django.utils.text import slugify

# 定义分类规则
CATEGORY_RULES = {
    '社交媒体': {
        'keywords': ['微博', 'weibo', '知乎', 'zhihu', '豆瓣', 'douban', '简书', 'jianshu', 'twitter', 'facebook', 'instagram', 'reddit', 'linkedin'],
        'domains': ['weibo.com', 'zhihu.com', 'douban.com', 'jianshu.com', 'twitter.com', 'facebook.com', 'instagram.com', 'reddit.com', 'linkedin.com']
    },
    '视频平台': {
        'keywords': ['bilibili', 'youtube', '抖音', 'douyin', '快手', 'kuaishou', '西瓜', 'ixigua', '好看视频', 'haokan', '腾讯视频', 'iqiyi', '爱奇艺', 'youku', '优酷'],
        'domains': ['bilibili.com', 'youtube.com', 'douyin.com', 'kuaishou.com', 'ixigua.com', 'haokan.com', 'v.qq.com', 'iqiyi.com', 'youku.com']
    },
    '自媒体平台': {
        'keywords': ['公众号', 'weixin', '头条号', 'toutiao', '百家号', 'baijiahao', '企鹅号', '搜狐号', 'sohu', '大鱼号', 'dayu', '网易号'],
        'domains': ['mp.weixin.qq.com', 'mp.toutiao.com', 'baijiahao.baidu.com', 'om.qq.com', 'mp.sohu.com', 'mp.dayu.com', 'mp.163.com']
    },
    '直播平台': {
        'keywords': ['直播', 'live', '斗鱼', 'douyu', '虎牙', 'huya', 'twitch'],
        'domains': ['douyu.com', 'huya.com', 'twitch.tv', 'live.bilibili.com']
    },
    '音频平台': {
        'keywords': ['喜马拉雅', 'ximalaya', '荔枝', 'lizhi', '蜻蜓', 'qingting', 'spotify', 'podcast'],
        'domains': ['ximalaya.com', 'lizhi.fm', 'qingting.fm', 'spotify.com']
    },
    '热榜资讯': {
        'keywords': ['热榜', '排行', 'rank', 'top', '资讯', 'news', 'tophub', '摸鱼'],
        'domains': ['tophub.today', 'tophub.fun', 'mo.fish', 'duomoyu.com', 'the.top', 're-bang.com']
    },
    '开发工具': {
        'keywords': ['github', 'gitlab', 'coding', 'gitee', 'stackoverflow', 'csdn', '掘金', 'juejin', 'dev.to'],
        'domains': ['github.com', 'gitlab.com', 'coding.net', 'gitee.com', 'stackoverflow.com', 'csdn.net', 'juejin.cn', 'dev.to']
    },
    '设计资源': {
        'keywords': ['dribbble', 'behance', 'figma', 'sketch', 'canva', '花瓣', 'huaban', '站酷', 'zcool'],
        'domains': ['dribbble.com', 'behance.net', 'figma.com', 'sketch.com', 'canva.com', 'huaban.com', 'zcool.com.cn']
    },
    '电商平台': {
        'keywords': ['淘宝', 'taobao', '京东', 'jd.com', '拼多多', 'pinduoduo', '天猫', 'tmall', 'amazon', 'ebay'],
        'domains': ['taobao.com', 'jd.com', 'pinduoduo.com', 'tmall.com', 'amazon.com', 'ebay.com']
    },
    '学习教育': {
        'keywords': ['coursera', 'udemy', 'edx', 'mooc', '网易云课堂', '腾讯课堂', 'bilibili', '学习', 'education', 'learn'],
        'domains': ['coursera.org', 'udemy.com', 'edx.org', 'icourse163.org', 'ke.qq.com']
    },
    '搜索引擎': {
        'keywords': ['google', 'baidu', 'bing', '搜索', 'search'],
        'domains': ['google.com', 'baidu.com', 'bing.com', 'duckduckgo.com']
    },
    '云存储': {
        'keywords': ['网盘', 'drive', 'dropbox', 'onedrive', '百度网盘', '阿里云盘', 'icloud'],
        'domains': ['drive.google.com', 'dropbox.com', 'onedrive.com', 'pan.baidu.com', 'aliyundrive.com', 'icloud.com']
    },
    '邮箱服务': {
        'keywords': ['mail', 'gmail', 'outlook', 'qq邮箱', '163邮箱', '邮箱'],
        'domains': ['gmail.com', 'outlook.com', 'mail.qq.com', 'mail.163.com', 'mail.126.com']
    },
    '在线工具': {
        'keywords': ['tool', '工具', 'converter', '转换', 'editor', '编辑器'],
        'domains': []
    }
}

def categorize_bookmark(name, url):
    """根据名称和URL判断书签应该属于哪个分类"""
    name_lower = name.lower()
    url_lower = url.lower()

    for category_name, rules in CATEGORY_RULES.items():
        # 检查关键词
        for keyword in rules['keywords']:
            if keyword.lower() in name_lower or keyword.lower() in url_lower:
                return category_name

        # 检查域名
        for domain in rules['domains']:
            if domain in url_lower:
                return category_name

    return '其他网站'

def main():
    # 获取书签栏分类
    bookmarks_bar = Category.objects.get(id=13)

    # 重命名书签栏
    bookmarks_bar.name = '奔跑中的奶酪的付费书签，这里免费放送'
    bookmarks_bar.slug = slugify(bookmarks_bar.name, allow_unicode=True)
    bookmarks_bar.save()
    print(f"✓ 已重命名分类: {bookmarks_bar.name}")

    # 获取所有书签
    bookmarks = Tool.objects.filter(category_id=13)
    print(f"✓ 找到 {bookmarks.count()} 个书签")

    # 分析并分类
    category_stats = defaultdict(int)
    for bookmark in bookmarks:
        cat_name = categorize_bookmark(bookmark.name, bookmark.website_url)
        category_stats[cat_name] += 1

    print("\n分类统计:")
    for cat_name, count in sorted(category_stats.items(), key=lambda x: x[1], reverse=True):
        print(f"  {cat_name}: {count} 个")

    # 创建新分类
    print("\n创建子分类...")
    created_categories = {}
    for cat_name in category_stats.keys():
        full_name = f"{bookmarks_bar.name} - {cat_name}"
        cat, created = Category.objects.get_or_create(
            name=full_name,
            defaults={'slug': slugify(full_name, allow_unicode=True)}
        )
        created_categories[cat_name] = cat
        if created:
            print(f"  ✓ 创建: {full_name}")

    # 迁移书签
    print("\n迁移书签...")
    migrated = 0
    for bookmark in bookmarks:
        cat_name = categorize_bookmark(bookmark.name, bookmark.website_url)
        new_category = created_categories[cat_name]
        bookmark.category = new_category
        bookmark.save()
        migrated += 1
        if migrated % 500 == 0:
            print(f"  已迁移 {migrated}/{bookmarks.count()}")

    print(f"\n✓ 完成! 共迁移 {migrated} 个书签到 {len(created_categories)} 个子分类")

if __name__ == '__main__':
    main()
