#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

category = Category.objects.get(name='职位推荐')

full_content = '''
<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', sans-serif; line-height: 1.8; color: #333;">
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 24px; margin-bottom: 24px; border-radius: 8px;">
        <h2 style="color: white; margin-bottom: 12px; font-size: 24px;">💼 Physics (PhD)</h2>
        <div style="display: flex; gap: 16px; flex-wrap: wrap; margin-top: 16px;">
            <span style="background: rgba(255,255,255,0.2); padding: 6px 12px; border-radius: 4px;">⏰ Hourly Contract</span>
            <span style="background: rgba(255,255,255,0.2); padding: 6px 12px; border-radius: 4px;">🌍 Remote</span>
            <span style="background: rgba(255,255,255,0.2); padding: 6px 12px; border-radius: 4px;">💰 $73.29/hour</span>
        </div>
    </div>

    <div style="background: #e3f2fd; border-left: 4px solid #2196f3; padding: 16px; margin-bottom: 24px; border-radius: 4px;">
        <p style="margin: 0; color: #1565c0; font-size: 16px;"><strong>🔥 本月已招聘6人</strong></p>
    </div>

    <div style="background: #fff3e0; border-left: 4px solid #ff9800; padding: 16px; margin-bottom: 24px; border-radius: 4px;">
        <h3 style="color: #e65100; margin: 0 0 8px 0;">📍 地点要求</h3>
        <p style="margin: 0; color: #666;">🇺🇸 美国 | 🇬🇧 英国 | 🇨🇦 加拿大 | 🇪🇺 欧盟</p>
    </div>

    <h2 style="color: #667eea; margin-top: 32px; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 2px solid #667eea;">🎯 职位背景</h2>

    <div style="background: #fff; border: 1px solid #e0e0e0; border-radius: 8px; padding: 20px; margin-bottom: 24px;">
        <p style="color: #555; line-height: 1.8; margin-bottom: 12px;">Mercor与领先的AI团队合作，提高通用对话AI系统的质量、实用性和可靠性。这些系统用于广泛的日常和专业场景，其有效性取决于它们如何清晰、准确和有帮助地回答真实用户问题。</p>
        <p style="color: #555; line-height: 1.8;">在物理相关场景中，对话AI系统必须展示强大的理论基础、定量严谨性和精确推理。该项目专注于评估和改进模型如何跨基础和高级主题解释、推理和回答物理相关问题。</p>
    </div>

    <h2 style="color: #667eea; margin-top: 32px; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 2px solid #667eea;">📋 核心职责</h2>

    <div style="background: #f8f9fa; border-radius: 8px; padding: 20px; margin-bottom: 24px;">
        <ul style="line-height: 2; margin: 0; padding-left: 24px; color: #555;">
            <li>编写和完善提示词以指导模型在物理场景中的行为</li>
            <li>评估LLM生成的物理相关查询回答的概念准确性、数学正确性和推理质量</li>
            <li>使用权威公共来源和领域知识进行事实核查</li>
            <li>标注模型回答，识别优势、改进领域以及事实或概念上的不准确之处</li>
            <li>评估不同受众的解释清晰度、结构和适当性</li>
            <li>确保模型回答符合预期的对话行为和系统指南</li>
            <li>遵循清晰的分类法、基准和详细的评估指南应用一致的评估标准</li>
        </ul>
    </div>

    <h2 style="color: #667eea; margin-top: 32px; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 2px solid #667eea;">✅ 任职要求</h2>

    <div style="background: #fff; border: 1px solid #e0e0e0; border-radius: 8px; padding: 20px; margin-bottom: 24px;">
        <p style="color: #555; margin-bottom: 12px;"><strong>必备条件：</strong></p>
        <ul style="line-height: 2; margin: 0 0 16px 0; padding-left: 24px; color: #555;">
            <li>拥有物理学或密切相关领域的<strong>PhD学位</strong></li>
            <li>在以下一个或多个子领域具有深厚专业知识：
                <ul style="margin-top: 8px;">
                    <li>经典力学与动力学</li>
                    <li>电磁学、光学与信号</li>
                    <li>热力学与统计物理</li>
                    <li>量子物理</li>
                    <li>相对论、宇宙学与高能物理</li>
                </ul>
            </li>
            <li>有使用大型语言模型（LLM）的丰富经验，了解人们如何以及为何使用它们</li>
            <li>出色的写作能力，能够清晰解释复杂的物理概念</li>
            <li>高度注重细节，能够发现他人可能忽略的细微问题</li>
            <li>有审查或编辑技术或学术写作的经验</li>
        </ul>
    </div>

    <h2 style="color: #667eea; margin-top: 32px; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 2px solid #667eea;">🎁 加分项</h2>

    <div style="background: #e8f5e9; border-radius: 8px; padding: 20px; margin-bottom: 24px;">
        <ul style="line-height: 2; margin: 0; padding-left: 24px; color: #2e7d32;">
            <li>有RLHF、模型评估或数据标注工作经验</li>
            <li>有教学、指导或向非专业受众解释物理概念的经验</li>
            <li>熟悉评估标准、基准或结构化审查框架</li>
        </ul>
    </div>

    <h2 style="color: #667eea; margin-top: 32px; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 2px solid #667eea;">🎯 成功标准</h2>

    <div style="background: #fff9e6; border-radius: 8px; padding: 20px; margin-bottom: 24px;">
        <ul style="line-height: 2; margin: 0; padding-left: 24px; color: #555;">
            <li>识别物理相关模型输出中的概念不准确性或薄弱推理</li>
            <li>您的反馈提高AI解释的严谨性、清晰度和正确性</li>
            <li>提供一致、可重现的评估成果，增强模型性能</li>
            <li>因为您的严格评估，Mercor客户信任其AI系统在物理场景中的表现</li>
        </ul>
    </div>

    <h2 style="color: #667eea; margin-top: 32px; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 2px solid #667eea;">💼 合同和付款条款</h2>

    <div style="background: #fff9e6; border-radius: 8px; padding: 20px; margin-bottom: 24px;">
        <ul style="line-height: 2; margin: 0; padding-left: 24px; color: #555;">
            <li>您将作为<strong>独立承包商</strong>参与</li>
            <li>这是一个<strong>完全远程</strong>的职位，可以按照您自己的时间表完成</li>
            <li>项目可以根据需求和表现进行延长、缩短或提前结束</li>
            <li>在Mercor的工作不涉及访问任何雇主、客户或机构的机密或专有信息</li>
            <li>根据提供的服务，每周通过<strong>Stripe或Wise</strong>付款</li>
        </ul>
    </div>

    <div style="background: #fff3e0; border-left: 4px solid #ff9800; padding: 16px; margin: 24px 0; border-radius: 4px;">
        <h3 style="color: #e65100; margin: 0 0 8px 0;">⚠️ 注意事项</h3>
        <p style="margin: 0; color: #666; line-height: 1.8;">目前我们无法支持H1-B或STEM OPT候选人。</p>
    </div>

    <h2 style="color: #667eea; margin-top: 32px; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 2px solid #667eea;">🎁 推荐奖励</h2>

    <div style="background: #e8f5e9; border-radius: 8px; padding: 20px; margin-bottom: 24px;">
        <p style="color: #2e7d32; line-height: 1.8; margin-bottom: 12px;"><strong>通过推荐赚取高达 $300</strong></p>
        <p style="color: #555; line-height: 1.8; margin-bottom: 12px;">分享下面的推荐链接，每成功推荐一人即可赚取高达 $300。您可以推荐的人数没有限制。可能适用限制条件。</p>
        <div style="background: white; border-radius: 6px; padding: 12px; margin-top: 12px;">
            <a href="https://t.mercor.com/w3GOa" target="_blank" style="color: #667eea; text-decoration: none; word-break: break-all;">https://t.mercor.com/w3GOa</a>
        </div>
    </div>

    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 8px; padding: 20px; text-align: center; margin-top: 32px;">
        <h3 style="color: white; margin: 0 0 12px 0;">💡 为什么选择这个职位？</h3>
        <ul style="list-style: none; padding: 0; margin: 0; line-height: 2;">
            <li>💰 时薪：$73.29/小时</li>
            <li>🌍 完全远程，灵活时间</li>
            <li>🔥 本月已招聘6人，机会真实可靠</li>
            <li>🤖 与领先AI团队合作</li>
            <li>🎁 推荐奖励高达 $300/人</li>
            <li>🔬 运用物理专业知识塑造AI系统</li>
        </ul>
    </div>
</div>
'''

tool, created = Tool.objects.update_or_create(
    slug='physics-phd-mercor',
    defaults={
        'name': 'Physics (PhD) - Mercor',
        'short_description': '远程物理学博士，$73.29/小时，评估和改进AI物理任务表现，需PhD学位',
        'full_description': full_content,
        'website_url': 'https://t.mercor.com/w3GOa',
        'category': category,
        'is_featured': True,
        'is_published': True,
    }
)

print('✓ 已添加：Physics (PhD) - Mercor' if created else '✓ 已更新：Physics (PhD) - Mercor')
