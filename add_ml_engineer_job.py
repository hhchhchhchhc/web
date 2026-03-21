#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

category, _ = Category.objects.get_or_create(
    name='职位推荐',
    defaults={'description': '优质远程工作和职位机会推荐', 'order': 80}
)

full_content = '''
<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', sans-serif; line-height: 1.8; color: #333;">
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 24px; margin-bottom: 24px; border-radius: 8px;">
        <h2 style="color: white; margin-bottom: 12px; font-size: 24px;">💼 Machine Learning Engineer</h2>
        <div style="display: flex; gap: 16px; flex-wrap: wrap; margin-top: 16px;">
            <span style="background: rgba(255,255,255,0.2); padding: 6px 12px; border-radius: 4px;">⏰ Hourly Contract</span>
            <span style="background: rgba(255,255,255,0.2); padding: 6px 12px; border-radius: 4px;">🌍 Remote</span>
            <span style="background: rgba(255,255,255,0.2); padding: 6px 12px; border-radius: 4px;">💰 $100-$120/hour</span>
        </div>
    </div>

    <div style="background: #e3f2fd; border-left: 4px solid #2196f3; padding: 16px; margin-bottom: 24px; border-radius: 4px;">
        <p style="margin: 0; color: #1565c0; font-size: 16px;"><strong>🔥 本月已招聘73人</strong></p>
    </div>

    <h2 style="color: #667eea; margin-top: 32px; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 2px solid #667eea;">🏢 关于公司</h2>

    <div style="background: #fff; border: 1px solid #e0e0e0; border-radius: 8px; padding: 20px; margin-bottom: 24px;">
        <p style="margin: 0 0 12px 0;"><strong style="color: #667eea;">Mercor</strong></p>
        <p style="margin: 0; color: #555; line-height: 1.8;">Mercor 与领先的 AI 实验室和企业合作，利用人类专业知识训练前沿模型。您将参与专注于训练和增强 AI 系统的项目，获得有竞争力的报酬，与顶尖研究人员合作，并帮助塑造您专业领域的下一代 AI 系统。</p>
        <p style="margin: 12px 0 0 0;"><a href="https://mercor.com" target="_blank" style="color: #667eea; text-decoration: none;">🔗 mercor.com</a></p>
    </div>

    <h2 style="color: #667eea; margin-top: 32px; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 2px solid #667eea;">📋 职位描述</h2>

    <div style="background: #fff; border: 1px solid #e0e0e0; border-radius: 8px; padding: 20px; margin-bottom: 24px;">
        <p style="color: #555; line-height: 1.8; margin-bottom: 16px;">Mercor 正在与一家领先的 AI 研究实验室合作，支持对先进机器学习系统的评估。我们正在寻找经验丰富的机器学习工程师和研究人员，为设计高质量的评估套件做出贡献，这些套件用于衡量 AI 在实际机器学习工程任务中的表现。</p>
        <p style="color: #555; line-height: 1.8;">这项工作专注于将实际的 ML 研究和工程工作流程转化为前沿模型的结构化基准测试。这是一个基于项目的远程机会，适合具有实践 ML 研究经验的专家。</p>
    </div>

    <h2 style="color: #667eea; margin-top: 32px; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 2px solid #667eea;">🎯 核心职责</h2>

    <div style="background: #f8f9fa; border-radius: 8px; padding: 20px; margin-bottom: 24px;">
        <ul style="line-height: 2; margin: 0; padding-left: 24px; color: #555;">
            <li>设计和编写机器学习工程任务的详细评估套件</li>
            <li>评估 AI 生成的解决方案，涵盖模型训练、调试、优化和实验等领域</li>
        </ul>
    </div>

    <h2 style="color: #667eea; margin-top: 32px; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 2px solid #667eea;">✅ 理想资格</h2>

    <div style="background: #fff; border: 1px solid #e0e0e0; border-radius: 8px; padding: 20px; margin-bottom: 24px;">
        <ul style="line-height: 2; margin: 0; padding-left: 24px; color: #555;">
            <li><strong>3年以上</strong>机器学习工程或应用 ML 研究经验</li>
            <li>具有模型开发、实验和评估的实践经验</li>
            <li>具有 ML 研究背景（<strong>强烈推荐</strong>行业实验室或学术环境）</li>
            <li>对 ML 系统设计选择和权衡有很强的推理能力</li>
            <li>清晰的书面沟通能力和对技术细节的高度关注</li>
        </ul>
    </div>'''

full_content += '''
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
        <p style="color: #2e7d32; line-height: 1.8; margin-bottom: 12px;"><strong>通过推荐赚取高达 $480</strong></p>
        <p style="color: #555; line-height: 1.8; margin-bottom: 12px;">分享下面的推荐链接，每成功推荐一人即可赚取高达 $480。您可以推荐的人数没有限制。可能适用限制条件。</p>
        <div style="background: white; border-radius: 6px; padding: 12px; margin-top: 12px;">
            <a href="https://t.mercor.com/K1xwq" target="_blank" style="color: #667eea; text-decoration: none; word-break: break-all;">https://t.mercor.com/K1xwq</a>
        </div>
    </div>

    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 8px; padding: 20px; text-align: center; margin-top: 32px;">
        <h3 style="color: white; margin: 0 0 12px 0;">💡 为什么选择这个职位？</h3>
        <ul style="list-style: none; padding: 0; margin: 0; line-height: 2;">
            <li>💰 高时薪：$100-$120/小时</li>
            <li>🌍 完全远程，灵活时间</li>
            <li>🤝 与顶尖 AI 研究人员合作</li>
            <li>🚀 参与前沿 AI 系统开发</li>
            <li>📈 本月已招聘73人，机会真实可靠</li>
        </ul>
    </div>
</div>
'''

tool, created = Tool.objects.update_or_create(
    slug='ml-engineer-mercor',
    defaults={
        'name': 'Machine Learning Engineer - Mercor',
        'short_description': '远程ML工程师职位，$100-$120/小时，与领先AI实验室合作，设计ML评估套件',
        'full_description': full_content,
        'website_url': 'https://t.mercor.com/K1xwq',
        'category': category,
        'is_featured': True,
        'is_published': True,
    }
)

print('✓ 已添加：Machine Learning Engineer - Mercor' if created else '✓ 已更新：Machine Learning Engineer - Mercor')
