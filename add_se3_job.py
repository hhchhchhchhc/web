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
        <h2 style="color: white; margin-bottom: 12px; font-size: 24px;">💼 Software Engineer III</h2>
        <div style="display: flex; gap: 16px; flex-wrap: wrap; margin-top: 16px;">
            <span style="background: rgba(255,255,255,0.2); padding: 6px 12px; border-radius: 4px;">💼 Full-time</span>
            <span style="background: rgba(255,255,255,0.2); padding: 6px 12px; border-radius: 4px;">📍 New York, NY</span>
            <span style="background: rgba(255,255,255,0.2); padding: 6px 12px; border-radius: 4px;">💰 $80-$110/hour</span>
        </div>
    </div>

    <div style="background: #fff3e0; border-left: 4px solid #ff9800; padding: 16px; margin-bottom: 24px; border-radius: 4px;">
        <h3 style="color: #e65100; margin: 0 0 8px 0;">📍 地点要求</h3>
        <p style="margin: 0; color: #666;">🇺🇸 美国（完全远程，需符合ET或PT时区工作时间）</p>
    </div>

    <h2 style="color: #667eea; margin-top: 32px; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 2px solid #667eea;">📋 职位描述</h2>

    <div style="background: #fff; border: 1px solid #e0e0e0; border-radius: 8px; padding: 20px; margin-bottom: 24px;">
        <p style="color: #555; line-height: 1.8;">知名科技公司招聘软件工程师加入面试体验团队，开发支持每年数十万次面试的AI招聘基础设施，使用GPT-4o等尖端AI技术。</p>
    </div>

    <h2 style="color: #667eea; margin-top: 32px; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 2px solid #667eea;">🎯 核心职责</h2>

    <div style="background: #f8f9fa; border-radius: 8px; padding: 20px; margin-bottom: 24px;">
        <ul style="line-height: 2; margin: 0; padding-left: 24px; color: #555;">
            <li>开发和增强AI驱动的面试工具和自动化系统</li>
            <li>使用React构建前端用户界面</li>
            <li>构建支持面试调度、AI转录/总结的后端服务</li>
            <li>与AI/ML团队合作集成GPT-4o等AI技术</li>
            <li>使用Cursor、Claude Code等AI开发工具加速开发</li>
        </ul>
    </div>

    <h2 style="color: #667eea; margin-top: 32px; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 2px solid #667eea;">✅ 任职要求</h2>

    <div style="background: #fff; border: 1px solid #e0e0e0; border-radius: 8px; padding: 20px; margin-bottom: 24px;">
        <ul style="line-height: 2; margin: 0; padding-left: 24px; color: #555;">
            <li>计算机科学或相关领域学士学位</li>
            <li><strong>4年+</strong>软件工程经验（Java、C++、C#）</li>
            <li>熟悉Python、PHP或JavaScript</li>
            <li>精通React、Vue等前端框架</li>
            <li>优秀的问题解决和沟通能力</li>
        </ul>
    </div>

    <div style="background: #fff3e0; border-left: 4px solid #ff9800; padding: 16px; margin: 24px 0; border-radius: 4px;">
        <h3 style="color: #e65100; margin: 0 0 8px 0;">💼 雇主信息</h3>
        <p style="margin: 0; color: #666; line-height: 1.8;">此职位通过Cincinnatus雇佣（W-2全职），Cincinnatus是企业人才公司，提供工资、福利和合规服务。</p>
    </div>

    <h2 style="color: #667eea; margin-top: 32px; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 2px solid #667eea;">🎁 推荐奖励</h2>

    <div style="background: #e8f5e9; border-radius: 8px; padding: 20px; margin-bottom: 24px;">
        <p style="color: #2e7d32; line-height: 1.8; margin-bottom: 12px;"><strong>通过推荐赚取高达 $440</strong></p>
        <div style="background: white; border-radius: 6px; padding: 12px; margin-top: 12px;">
            <a href="https://t.mercor.com/G1JGy" target="_blank" style="color: #667eea; text-decoration: none; word-break: break-all;">https://t.mercor.com/G1JGy</a>
        </div>
    </div>

    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 8px; padding: 20px; text-align: center; margin-top: 32px;">
        <h3 style="color: white; margin: 0 0 12px 0;">💡 为什么选择这个职位？</h3>
        <ul style="list-style: none; padding: 0; margin: 0; line-height: 2;">
            <li>💰 时薪：$80-$110</li>
            <li>💼 W-2全职，含福利</li>
            <li>🌍 完全远程工作</li>
            <li>🤖 使用GPT-4o、Cursor等前沿AI工具</li>
            <li>🎁 推荐奖励 $440/人</li>
        </ul>
    </div>
</div>
'''

tool, created = Tool.objects.update_or_create(
    slug='software-engineer-iii-mercor',
    defaults={
        'name': 'Software Engineer III - Mercor',
        'short_description': '全职软件工程师，$80-$110/小时，纽约远程，开发AI面试工具，需4年+经验',
        'full_description': full_content,
        'website_url': 'https://t.mercor.com/G1JGy',
        'category': category,
        'is_featured': True,
        'is_published': True,
    }
)

print('✓ 已添加：Software Engineer III - Mercor' if created else '✓ 已更新：Software Engineer III - Mercor')
