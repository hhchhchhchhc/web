#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

# 获取创业资源分类
startup_category = Category.objects.get(name='创业资源')

# 1. 知乎话题精华内容
zhihu_data = {
    'name': '知乎话题精华内容挖掘',
    'short_description': '挖掘知乎高质量话题和精华内容，作为自媒体创作素材来源',
    'full_description': '''**工具用途：**
知乎作为中文互联网最大的问答社区，拥有海量高质量内容，是自媒体创作者的优质素材库。

**使用方法：**
1. 浏览知乎热榜和话题广场
2. 关注相关领域的热门话题
3. 筛选高赞回答和精华内容
4. 提取观点和素材进行二次创作

**适用场景：**
- 自媒体选题策划
- 内容创作素材收集
- 热点话题追踪
- 用户需求洞察

**创作建议：**
- 选择有争议性的话题更易引发讨论
- 关注时效性强的热门话题
- 深度内容可进行多角度解读
- 注意版权，进行原创性改编''',
    'website_url': 'https://www.zhihu.com',
    'category': startup_category
}

tool1, created1 = Tool.objects.get_or_create(
    name=zhihu_data['name'],
    defaults=zhihu_data
)
print(f'{"✓ 已添加" if created1 else "- 已存在"}: {tool1.name}')

# 2. 谷歌Trends排名作为自媒体选题
trends_data = {
    'name': '谷歌Trends自媒体选题工具',
    'short_description': '利用谷歌趋势排名发现热门话题，精准把握自媒体创作方向',
    'full_description': '''**工具用途：**
Google Trends是谷歌提供的免费趋势分析工具，可以帮助自媒体创作者发现热门话题和趋势。

**核心功能：**
- 实时热搜榜单
- 关键词搜索趋势分析
- 地区热度对比
- 相关话题推荐
- 历史趋势数据

**使用方法：**
1. 访问Google Trends网站
2. 查看实时热搜和每日趋势
3. 搜索相关领域关键词
4. 分析搜索热度和趋势走向
5. 选择上升趋势的话题进行创作

**选题策略：**
- 关注搜索量快速上升的话题
- 结合地区特点选择本地化内容
- 提前布局季节性和周期性话题
- 对比多个关键词找到蓝海领域

**适用场景：**
- 短视频选题策划
- 公众号文章选题
- 直播内容规划
- 电商选品参考''',
    'website_url': 'https://trends.google.com',
    'category': startup_category
}

tool2, created2 = Tool.objects.get_or_create(
    name=trends_data['name'],
    defaults=trends_data
)
print(f'{"✓ 已添加" if created2 else "- 已存在"}: {tool2.name}')

print('\n两个内容创作工具添加完成！')
