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

    <h2 style="color: #667eea; margin-top: 32px; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 2px solid #667eea;">🏢 关于公司</h2>

    <div style="background: #fff; border: 1px solid #e0e0e0; border-radius: 8px; padding: 20px; margin-bottom: 24px;">
        <p style="margin: 0 0 12px 0;"><strong style="color: #667eea;">Mercor</strong></p>
        <p style="margin: 0; color: #555; line-height: 1.8;">Mercor 与领先的 AI 实验室和企业合作，利用人类专业知识训练前沿模型。您将参与专注于训练和增强 AI 系统的项目，获得有竞争力的报酬，与顶尖研究人员合作，并帮助塑造您专业领域的下一代 AI 系统。</p>
    </div>

    <h2 style="color: #667eea; margin-top: 32px; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 2px solid #667eea;">🎯 项目背景</h2>

    <div style="background: #fff; border: 1px solid #e0e0e0; border-radius: 8px; padding: 20px; margin-bottom: 24px;">
        <p style="color: #555; line-height: 1.8; margin-bottom: 12px;">Mercor 与领先的 AI 团队合作，提高通用对话 AI 系统的质量、实用性和可靠性。这些系统用于广泛的日常和专业场景，其有效性取决于它们对真实用户问题的回答是否清晰、准确和有帮助。</p>
        <p style="color: #555; line-height: 1.8;">在金融领域，即使是小错误或不清晰的推理也可能产生重大的下游影响。该项目专注于评估和改进对话 AI 系统如何推理、解释和回应金融相关查询。您的专业知识有助于确保模型输出反映真实世界的金融知识、合理的定量推理和清晰的专业沟通。</p>
    </div>'''

tool, created = Tool.objects.update_or_create(
    slug='finance-expert-mercor',
    defaults={
        'name': 'Finance Expert - Mercor',
        'short_description': '远程金融专家，$105/小时，评估和改进AI金融回答质量，需5年+金融经验',
        'full_description': full_content,
        'website_url': 'https://t.mercor.com/QM9GY',
        'category': category,
        'is_featured': True,
        'is_published': True,
    }
)

print('✓ 已添加：Finance Expert - Mercor' if created else '✓ 已更新：Finance Expert - Mercor')
