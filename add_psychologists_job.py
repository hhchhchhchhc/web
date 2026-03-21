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
        <h2 style="color: white; margin-bottom: 12px; font-size: 24px;">💼 Psychologists</h2>
        <div style="display: flex; gap: 16px; flex-wrap: wrap; margin-top: 16px;">
            <span style="background: rgba(255,255,255,0.2); padding: 6px 12px; border-radius: 4px;">⏰ Hourly Contract</span>
            <span style="background: rgba(255,255,255,0.2); padding: 6px 12px; border-radius: 4px;">🌍 Remote</span>
            <span style="background: rgba(255,255,255,0.2); padding: 6px 12px; border-radius: 4px;">💰 $30-$80/hour</span>
        </div>
    </div>

    <div style="background: #e3f2fd; border-left: 4px solid #2196f3; padding: 16px; margin-bottom: 24px; border-radius: 4px;">
        <p style="margin: 0; color: #1565c0; font-size: 16px;"><strong>🔥 本月已招聘137人</strong></p>
    </div>

    <h2 style="color: #667eea; margin-top: 32px; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 2px solid #667eea;">📋 职位描述</h2>

    <div style="background: #fff; border: 1px solid #e0e0e0; border-radius: 8px; padding: 20px; margin-bottom: 24px;">
        <p style="color: #555; line-height: 1.8; margin-bottom: 12px;">Mercor与顶级AI研究机构合作，招聘经验丰富的心理学家参与高影响力项目，专注于评估和改进AI系统在心理学相关任务上的表现。</p>
        <p style="color: #555; line-height: 1.8;">承包商将设计、审查和完善涵盖临床、认知、发展和社会心理学的提示词和输出。该工作非常适合具有扎实学术基础并能够批判性评估AI生成内容的推理和清晰度的心理学家。</p>
    </div>

    <h2 style="color: #667eea; margin-top: 32px; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 2px solid #667eea;">🎯 核心职责</h2>

    <div style="background: #f8f9fa; border-radius: 8px; padding: 20px; margin-bottom: 24px;">
        <ul style="line-height: 2; margin: 0; padding-left: 24px; color: #555;">
            <li>开发反映真实世界场景、理论和研究应用的细致心理学任务</li>
            <li>审查AI生成的回答，评估概念准确性、伦理合理性和心理学洞察力</li>
            <li>创建展示最佳实践推理和临床或学术标准的基准答案</li>
            <li>记录模型局限性并提出改进心理学相关输出的建议</li>
            <li>使用结构化书面反馈与研究人员和同行评审员异步协作</li>
        </ul>
    </div>

    <h2 style="color: #667eea; margin-top: 32px; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 2px solid #667eea;">✅ 理想资格</h2>

    <div style="background: #fff; border: 1px solid #e0e0e0; border-radius: 8px; padding: 20px; margin-bottom: 24px;">
        <ul style="line-height: 2; margin: 0; padding-left: 24px; color: #555;">
            <li>心理学或密切相关领域的<strong>PhD或PsyD学位</strong></li>
            <li><strong>3年+</strong>临床实践、学术研究、教学或应用心理学经验</li>
            <li>深入了解心理学理论、诊断标准、研究方法和伦理考虑</li>
            <li>强大的分析和沟通能力，包括批判推理和逻辑的能力</li>
            <li>熟悉不同心理学子领域的学术和应用背景</li>
        </ul>
    </div>

    <h2 style="color: #667eea; margin-top: 32px; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 2px solid #667eea;">📅 工作详情</h2>

    <div style="background: #fff9e6; border-radius: 8px; padding: 20px; margin-bottom: 24px;">
        <ul style="line-height: 2; margin: 0; padding-left: 24px; color: #555;">
            <li><strong>预期投入：</strong>每周10小时以上</li>
            <li><strong>任务类型：</strong>开放式推理、基于场景的判断、文献综合、伦理审查</li>
            <li><strong>工作模式：</strong>交付成果驱动，包含同行验证和结构化质量检查</li>
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
        <p style="color: #2e7d32; line-height: 1.8; margin-bottom: 12px;"><strong>通过推荐赚取高达 $320</strong></p>
        <p style="color: #555; line-height: 1.8; margin-bottom: 12px;">分享下面的推荐链接，每成功推荐一人即可赚取高达 $320。您可以推荐的人数没有限制。可能适用限制条件。</p>
        <div style="background: white; border-radius: 6px; padding: 12px; margin-top: 12px;">
            <a href="https://t.mercor.com/aEFz6" target="_blank" style="color: #667eea; text-decoration: none; word-break: break-all;">https://t.mercor.com/aEFz6</a>
        </div>
    </div>

    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 8px; padding: 20px; text-align: center; margin-top: 32px;">
        <h3 style="color: white; margin: 0 0 12px 0;">💡 为什么选择这个职位？</h3>
        <ul style="list-style: none; padding: 0; margin: 0; line-height: 2;">
            <li>💰 时薪：$30-$80/小时</li>
            <li>🌍 完全远程，灵活时间</li>
            <li>🔥 本月已招聘137人，机会真实可靠</li>
            <li>🤖 与顶级AI研究机构合作</li>
            <li>🎁 推荐奖励高达 $320/人</li>
            <li>🧠 运用心理学专业知识塑造AI系统</li>
        </ul>
    </div>
</div>
'''

tool, created = Tool.objects.update_or_create(
    slug='psychologists-mercor',
    defaults={
        'name': 'Psychologists - Mercor',
        'short_description': '远程心理学家，$30-$80/小时，评估和改进AI心理学任务表现，需PhD/PsyD学位和3年+经验',
        'full_description': full_content,
        'website_url': 'https://t.mercor.com/aEFz6',
        'category': category,
        'is_featured': True,
        'is_published': True,
    }
)

print('✓ 已添加：Psychologists - Mercor' if created else '✓ 已更新：Psychologists - Mercor')
