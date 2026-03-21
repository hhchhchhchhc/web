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
        <h2 style="color: white; margin-bottom: 12px; font-size: 24px;">💼 Software Expert (Operating System)</h2>
        <div style="display: flex; gap: 16px; flex-wrap: wrap; margin-top: 16px;">
            <span style="background: rgba(255,255,255,0.2); padding: 6px 12px; border-radius: 4px;">⏰ Hourly Contract</span>
            <span style="background: rgba(255,255,255,0.2); padding: 6px 12px; border-radius: 4px;">🌍 Remote</span>
            <span style="background: rgba(255,255,255,0.2); padding: 6px 12px; border-radius: 4px;">💰 $0-$100/hour</span>
        </div>
    </div>

    <div style="background: #e3f2fd; border-left: 4px solid #2196f3; padding: 16px; margin-bottom: 24px; border-radius: 4px;">
        <p style="margin: 0; color: #1565c0; font-size: 16px;"><strong>🔥 本月已招聘141人</strong></p>
    </div>

    <div style="background: #fff3e0; border-left: 4px solid #ff9800; padding: 16px; margin-bottom: 24px; border-radius: 4px;">
        <h3 style="color: #e65100; margin: 0 0 8px 0;">📍 重要要求</h3>
        <ul style="margin: 8px 0 0 0; padding-left: 24px; color: #666; line-height: 1.8;">
            <li>必须拥有物理 Mac 设备</li>
            <li>需要流利的英语能力</li>
        </ul>
    </div>
'''

tool, created = Tool.objects.update_or_create(
    slug='software-expert-os-mercor',
    defaults={
        'name': 'Software Expert (Operating System) - Mercor',
        'short_description': '远程操作系统专家，$0-$100/小时，为AI训练收集屏幕录制和标注数据，需Mac设备',
        'full_description': full_content,
        'website_url': 'https://t.mercor.com/BzQSY',
        'category': category,
        'is_featured': True,
        'is_published': True,
    }
)

print('✓ 已添加：Software Expert (Operating System) - Mercor' if created else '✓ 已更新：Software Expert (Operating System) - Mercor')
