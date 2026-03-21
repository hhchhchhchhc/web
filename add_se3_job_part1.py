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
        <p style="color: #555; line-height: 1.8; margin-bottom: 12px;">一家知名科技公司正在招聘软件工程师加入其招聘产品部门的面试体验团队。该职位涉及为每年支持数十万次面试的招聘基础设施做出贡献。</p>
        <p style="color: #555; line-height: 1.8;">工程师将使用尖端 AI 技术，与跨职能合作伙伴密切合作，从构思到发布全程推进产品开发，直接影响公司在全球范围内发现和招聘顶尖人才的方式。</p>
    </div>'''

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
