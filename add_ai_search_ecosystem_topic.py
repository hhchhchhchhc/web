#!/usr/bin/env python3
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, TopicPage


def get_or_create_category(name: str, description: str, order: int = 0):
    category, created = Category.objects.get_or_create(
        name=name,
        defaults={
            'description': description,
            'order': order,
        },
    )
    if created:
        print(f'✓ 创建分类: {name}')
    return category


intro = """根据整理的 txt 信息，搜索相关网站、应用及底层框架可分为以下四类：

一、通用搜索引擎与聚合 AI 搜索
- 传统大厂搜索引擎：Bing、百度、Google、Perplexity、YOU、360、搜狗、神马。
- Onion AI：AI 聚合搜索引擎，支持在 Perplexity、ChatGPT、Google 等多个 AI 搜索引擎之间无缝切换。
- 纳米搜索：360 集团推出的 AI 搜索应用，集搜索、阅读、写作和创作于一体，支持文字、语音、拍照和视频等多种搜索方式。
- 百度 AI 搜：百度基于文心大模型打造的桌面端 AI 搜索引擎，整合百度生态内海量内容。
- 梯子 AI：百度推出的无广告 AI 智能搜索助手应用，提供深度思考、智能总结等功能。
- 点线搜索：零一万物推出的 AI 搜索应用，基于智能算法学习用户行为，提供精准搜索与个性化推荐。
- BeaGo：零一万物推出的 AI 搜索助手，支持文字搜索和图像解读。
- Copilot Search：微软 Bing 推出的智能搜索模式，融合传统搜索与生成式 AI。
- Perplexity macOS 客户端：Perplexity 桌面端 AI 搜索工具，支持精确答案与网页总结。
- Brainstorm：支持多个 Agent 协作回答同一问题，从不同视角给出答案。
- Perplexica：开源 AI 驱动搜索引擎，作为 Perplexity AI 的开源替代品。
- MiniPerplx：基于 Grok 2.0 模型的开源 AI 搜索引擎。
- Perplexideez：开源本地 AI 搜索助手，支持网络与自托管应用信息搜索。
- MemFree：开源混合 AI 搜索引擎，支持文本、图像、文件、网页等多模态搜索。
- HotBot：提供新闻、图片、视频等多种搜索选项的 AI 搜索引擎。
- TurboSeek：由 Together.ai 技术支持的开源智能搜索引擎。

二、学术、科研与医疗搜索
- 百度学术：百度推出的 AI 学术搜索引擎，覆盖文献检索到论文创作。
- Kimi 学术搜索：通过搜索、分析、整合提升论文写作效率。
- Liner：面向学生与研究者，提供事实核查、自动引用和结果筛选。
- Consensus：基于向量搜索检索超 2 亿篇同行评审文献。
- Sourcely：自动搜索、总结并补充可信学术来源。
- Inciteful：通过构建与分析引用网络定位关键文献。
- Semantic Scholar：基于 NLP 的科学文献 AI 搜索引擎。
- KnowS：聚焦医学领域的生成式 AI 搜索引擎。
- MediSearch：提供基于科学证据的医疗答案。
- Suppr 超能文献：可理解复杂医学查询的 AI 医学文献搜索引擎。
- Pubmed pro：AI 医学文献检索平台，支持搜索、订阅与问答。

三、垂直行业与特定场景搜索
- 代悟：面向开发者，快速获取技术文档与代码。
- Accio：阿里巴巴面向海外推出的 B2B 对话式 AI 搜索引擎。
- Aisou.ai：商业信息智能问答平台，提供实时商业数据查询。
- 概念股搜索器：采用向量搜索技术，通过自然语言识别 A 股概念股。
- Telescope 2.0：AI 销售线索生成平台，可自定义条件精准定位线索。
- 点点：小红书推出的生活服务场景 AI 搜索助手。
- 问小团：美团推出的本地生活 AI 管家，集成在美团 App 搜索框。
- 在哪儿问问：滴滴推出的 AI 图寻应用，可通过照片搜索大致地理位置。
- 飞搜侠：面向飞书文档的高效在线搜索工具。
- YT Navigator：AI 驱动的 YouTube 内容搜索工具，支持自然语言查询。

四、AI 搜索框架与 API 底层工具
- ZeroSearch：阿里通义实验室开源的大模型搜索引擎框架，强化模型独立搜索能力。
- Sonar：Perplexity 推出的实时 AI 搜索 API。
- OpenDeepSearch：开源深度搜索工具，支持深度网络检索。
- WebAgent：阿里开源的自主搜索 AI Agent，具备端到端信息检索能力。
- OneSearch：快手推出的电商搜索端到端生成式框架。
- OmniSearch：阿里通义推出的多模态检索增强生成框架，支持自适应规划与检索调整。
- EICopilot：百度研究院推出的企业信息搜索与探索工具，面向知识图谱检索。
- Hika：免费的 AI 知识搜索工具，支持个性化交互与多维知识探索。
- Desearch：AI 深度研究工具，支持深度搜索并自动梳理研究思路与框架。"""

categories = [
    get_or_create_category('AI搜索引擎', 'AI 搜索引擎与聚合搜索工具', 1),
    get_or_create_category('科研文档', '科研、学术与医学文献检索工具', 2),
    get_or_create_category('开发者资源', '面向开发者与框架层的工具资源', 3),
]

topic, created = TopicPage.objects.update_or_create(
    slug='ai-search-sites-apps-frameworks',
    defaults={
        'title': 'AI搜索网站、应用与底层框架分类清单',
        'meta_description': '按通用搜索、学术医疗、垂直场景、框架API四大类整理AI搜索生态，便于快速选型与检索。',
        'intro': intro,
        'is_published': True,
    },
)

topic.categories.set(categories)

if created:
    print(f'✅ 已创建专题: {topic.title}')
else:
    print(f'♻️ 已更新专题: {topic.title}')

print('✅ 已绑定分类: ' + '、'.join(c.name for c in categories))
