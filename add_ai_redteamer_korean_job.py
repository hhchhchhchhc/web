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
        <h2 style="color: white; margin-bottom: 12px; font-size: 24px;">💼 AI Red-Teamer — Adversarial AI Testing (Advanced); English & Korean</h2>
        <div style="display: flex; gap: 16px; flex-wrap: wrap; margin-top: 16px;">
            <span style="background: rgba(255,255,255,0.2); padding: 6px 12px; border-radius: 4px;">⏰ Hourly Contract</span>
            <span style="background: rgba(255,255,255,0.2); padding: 6px 12px; border-radius: 4px;">🌍 Remote</span>
            <span style="background: rgba(255,255,255,0.2); padding: 6px 12px; border-radius: 4px;">💰 $50.5/hour</span>
        </div>
    </div>

    <div style="background: #e3f2fd; border-left: 4px solid #2196f3; padding: 16px; margin-bottom: 24px; border-radius: 4px;">
        <p style="margin: 0; color: #1565c0; font-size: 16px;"><strong>🔥 本月已招聘25人</strong></p>
    </div>

    <div style="background: #fff3e0; border-left: 4px solid #ff9800; padding: 16px; margin-bottom: 24px; border-radius: 4px;">
        <h3 style="color: #e65100; margin: 0 0 8px 0;">📍 地点和语言要求</h3>
        <p style="margin: 0 0 8px 0; color: #666;">🌍 地区限制：美国、韩国</p>
        <p style="margin: 0; color: #666;">🗣️ 语言要求：英语和韩语母语级流利度</p>
    </div>

    <h2 style="color: #667eea; margin-top: 32px; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 2px solid #667eea;">🎯 职位背景</h2>

    <div style="background: #fff; border: 1px solid #e0e0e0; border-radius: 8px; padding: 20px; margin-bottom: 24px;">
        <p style="color: #555; line-height: 1.8; margin-bottom: 12px;">在Mercor，我们相信最安全的AI是已经被我们攻击过的AI。我们正在组建红队项目——由人类数据专家探测AI模型的对抗性输入，发现漏洞，生成使AI更安全的红队数据。</p>
        <p style="color: #555; line-height: 1.8;">该项目涉及审查涉及敏感话题（如偏见、错误信息或有害行为）的AI输出。所有工作都是基于文本的，参与高敏感度项目是可选的，并有明确的指南和健康资源支持。</p>
    </div>

    <h2 style="color: #667eea; margin-top: 32px; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 2px solid #667eea;">📋 核心职责</h2>

    <div style="background: #f8f9fa; border-radius: 8px; padding: 20px; margin-bottom: 24px;">
        <ul style="line-height: 2; margin: 0; padding-left: 24px; color: #555;">
            <li>对对话AI模型和代理进行红队测试：越狱、提示词注入、滥用案例、偏见利用、多轮操纵</li>
            <li>生成高质量人类数据：标注失败、分类漏洞、标记系统性风险</li>
            <li>应用结构化方法：遵循分类法、基准和手册保持测试一致性</li>
            <li>可重现的文档：生成客户可以采取行动的报告、数据集和攻击案例</li>
        </ul>
    </div>

    <h2 style="color: #667eea; margin-top: 32px; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 2px solid #667eea;">✅ 任职要求</h2>

    <div style="background: #fff; border: 1px solid #e0e0e0; border-radius: 8px; padding: 20px; margin-bottom: 24px;">
        <ul style="line-height: 2; margin: 0; padding-left: 24px; color: #555;">
            <li>具有红队测试经验（AI对抗性工作、网络安全、社会技术探测）</li>
            <li>好奇心强且具有对抗性思维：本能地将系统推向极限</li>
            <li>结构化思维：使用框架或基准，而非随机攻击</li>
            <li>沟通能力强：能向技术和非技术利益相关者清晰解释风险</li>
            <li>适应性强：能够在不同项目和客户之间灵活切换</li>
        </ul>
    </div>

    <h2 style="color: #667eea; margin-top: 32px; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 2px solid #667eea;">🎁 加分项</h2>

    <div style="background: #e8f5e9; border-radius: 8px; padding: 20px; margin-bottom: 24px;">
        <ul style="line-height: 2; margin: 0; padding-left: 24px; color: #2e7d32;">
            <li><strong>对抗性机器学习：</strong>越狱数据集、提示词注入、RLHF/DPO攻击、模型提取</li>
            <li><strong>网络安全：</strong>渗透测试、漏洞开发、逆向工程</li>
            <li><strong>社会技术风险：</strong>骚扰/虚假信息探测、滥用分析、对话AI测试</li>
            <li><strong>创意探测：</strong>心理学、表演、写作等非常规对抗性思维</li>
        </ul>
    </div>

    <h2 style="color: #667eea; margin-top: 32px; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 2px solid #667eea;">🎯 成功标准</h2>

    <div style="background: #fff9e6; border-radius: 8px; padding: 20px; margin-bottom: 24px;">
        <ul style="line-height: 2; margin: 0; padding-left: 24px; color: #555;">
            <li>发现自动化测试遗漏的漏洞</li>
            <li>提供可重现的成果，增强客户AI系统</li>
            <li>扩大评估覆盖范围：测试更多场景，减少生产中的意外</li>
            <li>因为您已经像对手一样探测过，Mercor客户信任其AI的安全性</li>
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
        <p style="color: #2e7d32; line-height: 1.8; margin-bottom: 12px;"><strong>通过推荐赚取高达 $210</strong></p>
        <p style="color: #555; line-height: 1.8; margin-bottom: 12px;">分享下面的推荐链接，每成功推荐一人即可赚取高达 $210。您可以推荐的人数没有限制。可能适用限制条件。</p>
        <div style="background: white; border-radius: 6px; padding: 12px; margin-top: 12px;">
            <a href="https://t.mercor.com/nXvuz" target="_blank" style="color: #667eea; text-decoration: none; word-break: break-all;">https://t.mercor.com/nXvuz</a>
        </div>
    </div>

    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 8px; padding: 20px; text-align: center; margin-top: 32px;">
        <h3 style="color: white; margin: 0 0 12px 0;">💡 为什么选择这个职位？</h3>
        <ul style="list-style: none; padding: 0; margin: 0; line-height: 2;">
            <li>💰 时薪：$50.5/小时</li>
            <li>🌍 完全远程，灵活时间</li>
            <li>🔥 本月已招聘25人，机会真实可靠</li>
            <li>🤖 参与前沿AI安全红队测试</li>
            <li>🎁 推荐奖励高达 $210/人</li>
            <li>🗣️ 英语+韩语双语优势</li>
        </ul>
    </div>
</div>
'''

tool, created = Tool.objects.update_or_create(
    slug='ai-redteamer-korean-mercor',
    defaults={
        'name': 'AI Red-Teamer — Adversarial AI Testing (Advanced); English & Korean',
        'short_description': '远程AI红队测试专家，$50.5/小时，英语+韩语，对抗性AI测试和漏洞发现',
        'full_description': full_content,
        'website_url': 'https://t.mercor.com/nXvuz',
        'category': category,
        'is_featured': True,
        'is_published': True,
    }
)

print('✓ 已添加：AI Red-Teamer — Adversarial AI Testing (Advanced); English & Korean' if created else '✓ 已更新：AI Red-Teamer — Adversarial AI Testing (Advanced); English & Korean')
