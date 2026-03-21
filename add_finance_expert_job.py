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
        <h2 style="color: white; margin-bottom: 12px; font-size: 24px;">💼 Finance Expert</h2>
        <div style="display: flex; gap: 16px; flex-wrap: wrap; margin-top: 16px;">
            <span style="background: rgba(255,255,255,0.2); padding: 6px 12px; border-radius: 4px;">⏰ Hourly Contract</span>
            <span style="background: rgba(255,255,255,0.2); padding: 6px 12px; border-radius: 4px;">🌍 Remote</span>
            <span style="background: rgba(255,255,255,0.2); padding: 6px 12px; border-radius: 4px;">💰 $105/hour</span>
        </div>
    </div>

    <div style="background: #e3f2fd; border-left: 4px solid #2196f3; padding: 16px; margin-bottom: 24px; border-radius: 4px;">
        <p style="margin: 0; color: #1565c0; font-size: 16px;"><strong>🔥 本月已招聘28人</strong></p>
    </div>

    <div style="background: #fff3e0; border-left: 4px solid #ff9800; padding: 16px; margin-bottom: 24px; border-radius: 4px;">
        <h3 style="color: #e65100; margin: 0 0 8px 0;">📍 语言要求</h3>
        <p style="margin: 0; color: #666;">需要流利的英语能力</p>
    </div>

    <h2 style="color: #667eea; margin-top: 32px; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 2px solid #667eea;">🎯 项目背景</h2>

    <div style="background: #fff; border: 1px solid #e0e0e0; border-radius: 8px; padding: 20px; margin-bottom: 24px;">
        <p style="color: #555; line-height: 1.8; margin-bottom: 12px;">Mercor 与领先的 AI 团队合作，提高通用对话 AI 系统的质量、实用性和可靠性。在金融领域，即使是小错误或不清晰的推理也可能产生重大影响。</p>
        <p style="color: #555; line-height: 1.8;">该项目专注于评估和改进对话 AI 系统如何推理、解释和回应金融相关查询。您的专业知识有助于确保模型输出反映真实世界的金融知识、合理的定量推理和清晰的专业沟通。</p>
    </div>

    <h2 style="color: #667eea; margin-top: 32px; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 2px solid #667eea;">📋 工作内容</h2>

    <div style="background: #f8f9fa; border-radius: 8px; padding: 20px; margin-bottom: 24px;">
        <ul style="line-height: 2; margin: 0; padding-left: 24px; color: #555;">
            <li>编写和完善提示词以指导模型在金融场景中的行为</li>
            <li>评估 LLM 生成的金融相关回答的准确性、推理质量和清晰度</li>
            <li>使用可信的公共来源、金融参考资料和外部工具进行事实核查</li>
            <li>标注模型回答，识别优势、改进领域以及事实或概念上的不准确之处</li>
            <li>评估回答的语气、完整性和对实际金融用例的适用性</li>
            <li>确保模型回答符合预期的对话行为和系统指南</li>
            <li>遵循清晰的分类法、基准和详细的评估指南应用一致的评估标准</li>
        </ul>
    </div>

    <h2 style="color: #667eea; margin-top: 32px; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 2px solid #667eea;">✅ 任职要求</h2>

    <div style="background: #fff; border: 1px solid #e0e0e0; border-radius: 8px; padding: 20px; margin-bottom: 24px;">
        <p style="color: #555; margin-bottom: 12px;"><strong>必备条件：</strong></p>
        <ul style="line-height: 2; margin: 0 0 16px 0; padding-left: 24px; color: #555;">
            <li><strong>至少5年</strong>金融领域实际专业经验</li>
            <li>拥有相关<strong>学士、硕士或博士学位</strong>（如金融、会计、经济学、商业或相关领域）</li>
            <li>在以下一个或多个子领域有经验：
                <ul style="margin-top: 8px;">
                    <li>投资银行</li>
                    <li>企业金融</li>
                    <li>会计与审计</li>
                    <li>资产管理</li>
                </ul>
            </li>
            <li>有使用大型语言模型（LLM）的丰富经验，了解人们如何以及为何使用它们</li>
            <li>出色的写作能力，能够清晰解释复杂的金融概念</li>
            <li>高度注重细节，能够发现他人可能忽略的细微问题</li>
        </ul>
        <p style="color: #555; margin-bottom: 12px;"><strong>加分项：</strong></p>
        <ul style="line-height: 2; margin: 0; padding-left: 24px; color: #555;">
            <li>有 RLHF、模型评估或数据标注工作经验</li>
            <li>有编写或编辑高质量金融书面内容的经验</li>
            <li>有为非专业受众翻译复杂金融概念的经验</li>
            <li>熟悉评估标准、基准或质量评分系统</li>
        </ul>
    </div>

    <h2 style="color: #667eea; margin-top: 32px; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 2px solid #667eea;">🎯 成功标准</h2>

    <div style="background: #e8f5e9; border-radius: 8px; padding: 20px; margin-bottom: 24px;">
        <ul style="line-height: 2; margin: 0; padding-left: 24px; color: #2e7d32;">
            <li>识别模型回答中的金融不准确性、错误假设和薄弱推理</li>
            <li>您的反馈直接提高金融相关 AI 输出的准确性和实用性</li>
            <li>提供清晰、可重现的评估成果，客户可以据此采取行动</li>
            <li>因为您的严格评估，Mercor 客户信任其 AI 系统在金融场景中的表现</li>
        </ul>
    </div>

    <h2 style="color: #667eea; margin-top: 32px; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 2px solid #667eea;">💼 合同和付款条款</h2>

    <div style="background: #fff9e6; border-radius: 8px; padding: 20px; margin-bottom: 24px;">
        <ul style="line-height: 2; margin: 0; padding-left: 24px; color: #555;">
            <li>您将作为<strong>独立承包商</strong>参与</li>
            <li>这是一个<strong>完全远程</strong>的职位，可以按照您自己的时间表完成</li>
            <li>项目可以根据需求和表现进行延长、缩短或提前结束</li>
            <li>在 Mercor 的工作不涉及访问任何雇主、客户或机构的机密或专有信息</li>
            <li>根据提供的服务，每周通过 <strong>Stripe 或 Wise</strong> 付款</li>
        </ul>
    </div>

    <div style="background: #fff3e0; border-left: 4px solid #ff9800; padding: 16px; margin: 24px 0; border-radius: 4px;">
        <h3 style="color: #e65100; margin: 0 0 8px 0;">⚠️ 注意事项</h3>
        <p style="margin: 0; color: #666; line-height: 1.8;">目前我们无法支持 H1-B 或 STEM OPT 候选人。</p>
    </div>

    <h2 style="color: #667eea; margin-top: 32px; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 2px solid #667eea;">🎁 推荐奖励</h2>

    <div style="background: #e8f5e9; border-radius: 8px; padding: 20px; margin-bottom: 24px;">
        <p style="color: #2e7d32; line-height: 1.8; margin-bottom: 12px;"><strong>通过推荐赚取高达 $420</strong></p>
        <p style="color: #555; line-height: 1.8; margin-bottom: 12px;">分享下面的推荐链接，每成功推荐一人即可赚取高达 $420。您可以推荐的人数没有限制。可能适用限制条件。</p>
        <div style="background: white; border-radius: 6px; padding: 12px; margin-top: 12px;">
            <a href="https://t.mercor.com/QM9GY" target="_blank" style="color: #667eea; text-decoration: none; word-break: break-all;">https://t.mercor.com/QM9GY</a>
        </div>
    </div>

    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 8px; padding: 20px; text-align: center; margin-top: 32px;">
        <h3 style="color: white; margin: 0 0 12px 0;">💡 为什么选择这个职位？</h3>
        <ul style="list-style: none; padding: 0; margin: 0; line-height: 2;">
            <li>💰 固定时薪：$105/小时</li>
            <li>🌍 完全远程，灵活时间</li>
            <li>🔥 本月已招聘28人，机会真实可靠</li>
            <li>🤖 运用金融专业知识塑造 AI 系统</li>
            <li>🎁 推荐奖励高达 $420/人</li>
        </ul>
    </div>
</div>
'''

tool, created = Tool.objects.update_or_create(
    slug='finance-expert-mercor',
    defaults={
        'name': 'Finance Expert - Mercor',
        'short_description': '远程金融专家，$105/小时，评估和改进AI金融回答质量，需5年+金融经验和相关学位',
        'full_description': full_content,
        'website_url': 'https://t.mercor.com/QM9GY',
        'category': category,
        'is_featured': True,
        'is_published': True,
    }
)

print('✓ 已添加：Finance Expert - Mercor' if created else '✓ 已更新：Finance Expert - Mercor')
