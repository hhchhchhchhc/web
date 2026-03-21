#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

# 创建或获取分类
category, _ = Category.objects.get_or_create(
    name='运营指南',
    defaults={
        'description': '公众号、自媒体运营实战指南',
        'order': 100
    }
)

# 完整的HTML内容
full_content = '''
<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', sans-serif; line-height: 1.8; color: #333;">
    <div style="background: #fff9e6; border-left: 4px solid #ffc107; padding: 16px; margin-bottom: 24px; border-radius: 4px;">
        <p>根据《从0-1做个赚钱的公众号》等资料，扩大粉丝量（涨粉）的核心在于<strong>"实战"与"顺势而为"</strong>。不要空想，要通过持续的行动、对平台规则的利用以及高质量的价值交付来实现增长。</p>
    </div>

    <h2 style="color: #07c160; margin-top: 32px; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 2px solid #07c160;">1. 内容策略：借势与模仿（最快路径）</h2>

    <h3 style="color: #333; margin-top: 20px; margin-bottom: 12px;">▸ 模仿爆款（学会"抄"与"超"）</h3>
    <p>"爆过的还会再爆"。不要闭门造车，要观察同赛道内的数据好的文章。如果一个选题火了，大概率它在你的账号上也能火。</p>
    <div style="background: #e8f5e9; border-left: 4px solid #07c160; padding: 12px 16px; margin: 12px 0; border-radius: 4px;">
        <p style="color: #2e7d32; margin: 0;">💡 新手可以通过模仿爆款的框架、选题，结合自己的经历去写，这是涨粉的捷径。</p>
    </div>

    <h3 style="color: #333; margin-top: 20px; margin-bottom: 12px;">▸ 紧跟热点与平台风向</h3>
    <p>要保持对平台的敏感度。当看到同类型的选题不断出爆文，或者某个话题（如AI、特定剧评）很火时，要立刻跟进。</p>
    <div style="background: #e8f5e9; border-left: 4px solid #07c160; padding: 12px 16px; margin: 12px 0; border-radius: 4px;">
        <p style="color: #2e7d32; margin: 0;">🚀 抓住平台推荐的流量风口，猪也能飞起来。</p>
    </div>

    <h3 style="color: #333; margin-top: 20px; margin-bottom: 12px;">▸ 深耕垂直领域</h3>
    <p>平台扶持垂直领域（如民生、养生、职场等），这些领域的单价高且流量精准。</p>
    <div style="background: #e8f5e9; border-left: 4px solid #07c160; padding: 12px 16px; margin: 12px 0; border-radius: 4px;">
        <p style="color: #2e7d32; margin: 0;">🎯 内容越细分（"一厘米宽，万米深"），越容易吸引精准粉丝。</p>
    </div>

    <h2 style="color: #07c160; margin-top: 32px; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 2px solid #07c160;">2. 利用平台新功能与机制（获取推荐流量）</h2>

    <h3 style="color: #333; margin-top: 20px; margin-bottom: 12px;">▸ 布局关键词（SEO）</h3>
    <p>公众号的流量分发逻辑发生了变化，搜索流量很重要。在文章标题和正文中布局关键词，可以增加被微信"搜一搜"和"看一看"推荐的概率。</p>

    <h3 style="color: #333; margin-top: 20px; margin-bottom: 12px;">▸ 尝试"小绿书"格式</h3>
    <p>利用公众号后台类似小红书的图文/文字短消息格式（被称为"小绿书"）。这种形式目前有流量红利，且互动性强，适合增加曝光。</p>

    <h3 style="color: #333; margin-top: 20px; margin-bottom: 12px;">▸ 利用评论区引流</h3>
    <p>积极在评论区互动，甚至利用评论区广告位增加收益。活跃的评论区能提高账号的权重和互动性。</p>

    <h2 style="color: #07c160; margin-top: 32px; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 2px solid #07c160;">3. 主动运营与引流（打破被动）</h2>

    <h3 style="color: #333; margin-top: 20px; margin-bottom: 12px;">▸ "加我送资料"（诱饵引流）</h3>
    <p>这是一种非常有效的引流方式。在文章或朋友圈中提供具体的、有价值的资料（如SOP、工具包、涨粉教程），引导用户关注公众号或添加个人微信。</p>
    <div style="background: #e8f5e9; border-left: 4px solid #07c160; padding: 12px 16px; margin: 12px 0; border-radius: 4px;">
        <p style="color: #2e7d32; margin: 0;">🎁 核心是要解决用户的具体痛点。</p>
    </div>

    <h3 style="color: #333; margin-top: 20px; margin-bottom: 12px;">▸ 私域反哺公域</h3>
    <p>建立自己的私域流量池（个人微信、社群）。通过朋友圈分享、社群互动建立信任，然后将这些精准粉丝引导至公众号，形成互动和阅读的基础数据，有助于撬动公域流量。</p>

    <h3 style="color: #333; margin-top: 20px; margin-bottom: 12px;">▸ 混圈子与"蹭"流量</h3>
    <p>在高价值的社群中活跃，提供价值，甚至争取被大V（群主）夸奖或转发，这能带来极高质量的精准粉丝。</p>

    <h3 style="color: #333; margin-top: 20px; margin-bottom: 12px;">▸ 矩阵化运营</h3>
    <p>利用AI工具（如讯飞绘文）可以实现一人管理多个账号。例如，有运营人员利用讯飞绘文的账号托管和批量生成功能，一人可同时运营50个小红书账号，打造爆文"流水线"。</p>
    <div style="background: #e8f5e9; border-left: 4px solid #07c160; padding: 12px 16px; margin: 12px 0; border-radius: 4px;">
        <p style="color: #2e7d32; margin: 0;">🤖 AI工具让规模化运营成为可能，大幅提升效率。</p>
    </div>

    <h2 style="color: #07c160; margin-top: 32px; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 2px solid #07c160;">4. 执行力与心态（长期主义）</h2>

    <h3 style="color: #333; margin-top: 20px; margin-bottom: 12px;">▸ 日更倒逼成长</h3>
    <p>保持高频更新（如日更），不仅能提升写作能力，还能增加被平台推荐的机会。</p>
    <div style="background: #e8f5e9; border-left: 4px solid #07c160; padding: 12px 16px; margin: 12px 0; border-radius: 4px;">
        <p style="color: #2e7d32; margin: 0;">💪 量大出奇迹，不要因为初期数据差就停更。</p>
    </div>

    <h3 style="color: #333; margin-top: 20px; margin-bottom: 12px;">▸ 数据分析与复盘</h3>
    <p>不要只凭感觉写。如果某类文章数据好，就盯着这个方向继续写；如果数据不好，及时调整。要对数据敏感，根据反馈迭代内容。</p>

    <h3 style="color: #333; margin-top: 20px; margin-bottom: 12px;">▸ 拒绝无效互粉</h3>
    <p>互关互阅（互粉）虽然能让数据暂时好看，但会破坏粉丝画像，影响平台推流，对长期涨粉有害无益。</p>

    <div style="background: #fff3e0; border-radius: 8px; padding: 16px; margin: 20px 0;">
        <h3 style="color: #e65100; margin-bottom: 8px;">⚡ 特别提示：突破500粉门槛</h3>
        <p style="color: #666;">如果您是刚起步，首要目标是突破500粉丝（这是开通流量主变现的门槛）。建议新手通过加入相关社群或寻找有经验的人获取具体指导，不要自己盲目摸索。</p>
    </div>

    <div style="background: #f5f5f5; border-radius: 8px; padding: 20px; margin-top: 32px; text-align: center;">
        <h3 style="color: #333; margin-bottom: 12px;">📌 总结</h3>
        <p style="color: #555;">扩大粉丝量不是靠"等"来的，而是靠写爆款选题、布局关键词、主动引流以及日复一日的坚持执行换来的。</p>
    </div>
</div>
'''

# 创建或更新工具
tool, created = Tool.objects.update_or_create(
    slug='gongzhonghao-zhangfen-zhinan',
    defaults={
        'name': '公众号涨粉实战指南',
        'short_description': '从0到1的增长策略：内容策略、平台机制、主动运营、矩阵化运营等实战方法',
        'full_description': full_content,
        'website_url': 'https://ai-tool.indevs.in/tool/gongzhonghao-zhangfen-zhinan/',
        'category': category,
        'is_featured': True,
        'is_published': True,
    }
)

if created:
    print('✓ 已添加：公众号涨粉实战指南')
else:
    print('✓ 已更新：公众号涨粉实战指南')
