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
        <h2 style="color: white; margin-bottom: 12px; font-size: 24px;">💼 Software Engineering Expert</h2>
        <div style="display: flex; gap: 16px; flex-wrap: wrap; margin-top: 16px;">
            <span style="background: rgba(255,255,255,0.2); padding: 6px 12px; border-radius: 4px;">⏰ Hourly Contract</span>
            <span style="background: rgba(255,255,255,0.2); padding: 6px 12px; border-radius: 4px;">🌍 Remote</span>
            <span style="background: rgba(255,255,255,0.2); padding: 6px 12px; border-radius: 4px;">💰 $50-$150/hour</span>
        </div>
    </div>

    <div style="background: #e3f2fd; border-left: 4px solid #2196f3; padding: 16px; margin-bottom: 24px; border-radius: 4px;">
        <p style="margin: 0; color: #1565c0; font-size: 16px;"><strong>🔥 本月已招聘1540人</strong></p>
    </div>

    <h2 style="color: #667eea; margin-top: 32px; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 2px solid #667eea;">📋 职位描述</h2>

    <div style="background: #fff; border: 1px solid #e0e0e0; border-radius: 8px; padding: 20px; margin-bottom: 24px;">
        <p style="color: #555; line-height: 1.8;">Mercor招聘经验丰富的软件工程专业人员，支持与领先AI实验室的各种高影响力研究合作。自由职业者将通过代码验证、提示词优化、算法评估和模型基准测试等工作帮助改进AI系统。</p>
    </div>

    <h2 style="color: #667eea; margin-top: 32px; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 2px solid #667eea;">🎯 核心职责</h2>

    <div style="background: #f8f9fa; border-radius: 8px; padding: 20px; margin-bottom: 24px;">
        <ul style="line-height: 2; margin: 0; padding-left: 24px; color: #555;">
            <li>审查和优化AI生成的提示词、响应和代码</li>
            <li>验证算法和软件概念的技术准确性</li>
            <li>提供关于解决方案质量和清晰度的结构化反馈</li>
            <li>按主题、难度或语言标记和组织内容</li>
            <li>支持基准测试工作以评估模型能力</li>
        </ul>
    </div>

    <h2 style="color: #667eea; margin-top: 32px; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 2px solid #667eea;">✅ 理想资格</h2>

    <div style="background: #fff; border: 1px solid #e0e0e0; border-radius: 8px; padding: 20px; margin-bottom: 24px;">
        <ul style="line-height: 2; margin: 0; padding-left: 24px; color: #555;">
            <li><strong>2年+</strong>软件工程、技术研究或教育内容开发经验</li>
            <li>软件工程、计算机科学或相关领域学位（学士最低，硕士优先）</li>
            <li>精通Python、JavaScript、Java、C++等语言</li>
            <li>有调试、测试和验证代码的经验</li>
            <li>熟悉技术写作，注重细节</li>
        </ul>
    </div>

    <h2 style="color: #667eea; margin-top: 32px; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 2px solid #667eea;">📅 项目时间线</h2>

    <div style="background: #fff9e6; border-radius: 8px; padding: 20px; margin-bottom: 24px;">
        <ul style="line-height: 2; margin: 0; padding-left: 24px; color: #555;">
            <li><strong>开始日期：</strong>立即</li>
            <li><strong>持续时间：</strong>1-2个月</li>
            <li><strong>工作量：</strong>兼职（每周15-25小时，最多可达40小时）</li>
        </ul>
    </div>

    <h2 style="color: #667eea; margin-top: 32px; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 2px solid #667eea;">📝 申请流程</h2>

    <div style="background: #e8f5e9; border-radius: 8px; padding: 20px; margin-bottom: 24px;">
        <ol style="line-height: 2; margin: 0; padding-left: 24px; color: #2e7d32;">
            <li>上传简历</li>
            <li>AI面试：15分钟对话了解背景和经验</li>
            <li>几天内收到后续沟通和入职详情</li>
        </ol>
    </div>

    <h2 style="color: #667eea; margin-top: 32px; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 2px solid #667eea;">💼 合同和付款条款</h2>

    <div style="background: #fff9e6; border-radius: 8px; padding: 20px; margin-bottom: 24px;">
        <ul style="line-height: 2; margin: 0; padding-left: 24px; color: #555;">
            <li>独立承包商身份</li>
            <li>完全远程，自由安排时间</li>
            <li>每周通过Stripe或Wise付款</li>
        </ul>
    </div>

    <div style="background: #fff3e0; border-left: 4px solid #ff9800; padding: 16px; margin: 24px 0; border-radius: 4px;">
        <h3 style="color: #e65100; margin: 0 0 8px 0;">⚠️ 注意事项</h3>
        <p style="margin: 0; color: #666; line-height: 1.8;">目前无法支持H1-B或STEM OPT候选人。</p>
    </div>

    <h2 style="color: #667eea; margin-top: 32px; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 2px solid #667eea;">🎁 推荐奖励</h2>

    <div style="background: #e8f5e9; border-radius: 8px; padding: 20px; margin-bottom: 24px;">
        <p style="color: #2e7d32; line-height: 1.8; margin-bottom: 12px;"><strong>通过推荐赚取高达 $600</strong></p>
        <div style="background: white; border-radius: 6px; padding: 12px; margin-top: 12px;">
            <a href="https://t.mercor.com/ttewK" target="_blank" style="color: #667eea; text-decoration: none; word-break: break-all;">https://t.mercor.com/ttewK</a>
        </div>
    </div>

    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 8px; padding: 20px; text-align: center; margin-top: 32px;">
        <h3 style="color: white; margin: 0 0 12px 0;">💡 为什么选择这个职位？</h3>
        <ul style="list-style: none; padding: 0; margin: 0; line-height: 2;">
            <li>💰 灵活时薪：$50-$150</li>
            <li>🌍 完全远程，灵活时间</li>
            <li>🔥 本月已招聘1540人，大量机会</li>
            <li>🤖 参与前沿AI系统改进</li>
            <li>🎁 推荐奖励高达 $600/人</li>
        </ul>
    </div>
</div>
'''

tool, created = Tool.objects.update_or_create(
    slug='software-engineering-expert-mercor',
    defaults={
        'name': 'Software Engineering Expert - Mercor',
        'short_description': '远程软件工程专家，$50-$150/小时，代码验证和AI模型改进，需2年+经验',
        'full_description': full_content,
        'website_url': 'https://t.mercor.com/ttewK',
        'category': category,
        'is_featured': True,
        'is_published': True,
    }
)

print('✓ 已添加：Software Engineering Expert - Mercor' if created else '✓ 已更新：Software Engineering Expert - Mercor')
