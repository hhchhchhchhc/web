#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

category, _ = Category.objects.get_or_create(
    name='创业资源',
    defaults={'description': '创业、副业相关资源和工具', 'order': 70}
)

full_content = '''
<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', sans-serif; line-height: 1.8; color: #333;">
    <div style="background: linear-gradient(135deg, #ff2442 0%, #ff6b6b 100%); color: white; padding: 24px; margin-bottom: 24px; border-radius: 8px; text-align: center;">
        <h2 style="color: white; margin-bottom: 12px; font-size: 24px;">📊 小红书博主信息数据库</h2>
        <p style="font-size: 16px; opacity: 0.95;">14000位赚钱、创业、副业相关博主信息</p>
    </div>

    <div style="background: #fff3e0; border-left: 4px solid #ff9800; padding: 16px; margin-bottom: 24px; border-radius: 4px;">
        <h3 style="color: #e65100; margin: 0 0 12px 0;">📦 资源说明</h3>
        <p style="margin: 0; color: #666; line-height: 1.8;">本资源包含<strong style="color: #ff2442;">14000位</strong>小红书博主的详细信息，涵盖赚钱、创业、副业等相关领域，是进行市场调研、竞品分析、合作对接的宝贵资料。</p>
    </div>

    <h2 style="color: #ff2442; margin-top: 32px; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 2px solid #ff2442;">📋 资源内容</h2>

    <div style="background: #fff; border: 1px solid #e0e0e0; border-radius: 8px; padding: 20px; margin-bottom: 24px;">
        <ul style="line-height: 2; margin: 0; padding-left: 24px; color: #555;">
            <li>📝 <strong>博主数量：</strong>14000位</li>
            <li>🎯 <strong>领域范围：</strong>赚钱、创业、副业相关</li>
            <li>📊 <strong>文件格式：</strong>Excel表格（.xlsx）</li>
            <li>💼 <strong>信息维度：</strong>博主账号、粉丝数据、内容方向等</li>
        </ul>
    </div>

    <h2 style="color: #ff2442; margin-top: 32px; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 2px solid #ff2442;">💡 使用场景</h2>

    <div style="display: grid; gap: 16px; margin-bottom: 24px;">
        <div style="background: #f8f9fa; border-left: 4px solid #28a745; padding: 16px; border-radius: 4px;">
            <h3 style="color: #28a745; margin: 0 0 8px 0; font-size: 18px;">🔍 市场调研</h3>
            <p style="margin: 0; color: #555;">了解小红书创业赛道的博主分布和内容趋势</p>
        </div>

        <div style="background: #f8f9fa; border-left: 4px solid #007bff; padding: 16px; border-radius: 4px;">
            <h3 style="color: #007bff; margin: 0 0 8px 0; font-size: 18px;">🤝 合作对接</h3>
            <p style="margin: 0; color: #555;">寻找合适的博主进行商业合作或推广</p>
        </div>

        <div style="background: #f8f9fa; border-left: 4px solid #dc3545; padding: 16px; border-radius: 4px;">
            <h3 style="color: #dc3545; margin: 0 0 8px 0; font-size: 18px;">📈 竞品分析</h3>
            <p style="margin: 0; color: #555;">分析同领域博主的运营策略和内容方向</p>
        </div>

        <div style="background: #f8f9fa; border-left: 4px solid #ffc107; padding: 16px; border-radius: 4px;">
            <h3 style="color: #f57c00; margin: 0 0 8px 0; font-size: 18px;">✍️ 内容参考</h3>
            <p style="margin: 0; color: #555;">学习优秀博主的内容创作思路和选题方向</p>
        </div>
    </div>

    <h2 style="color: #ff2442; margin-top: 32px; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 2px solid #ff2442;">📥 下载方式</h2>

    <div style="background: #e3f2fd; border-radius: 8px; padding: 20px; margin-bottom: 24px;">
        <div style="margin-bottom: 16px;">
            <strong style="color: #1976d2; font-size: 16px;">百度网盘下载：</strong>
        </div>
        <div style="background: white; border-radius: 6px; padding: 16px; margin-bottom: 12px;">
            <p style="margin: 0 0 8px 0; color: #666;">链接：</p>
            <a href="https://pan.baidu.com/s/1XdHDpjY1RX31048fnbZbWQ?pwd=utr7" target="_blank" style="color: #1976d2; text-decoration: none; word-break: break-all;">https://pan.baidu.com/s/1XdHDpjY1RX31048fnbZbWQ?pwd=utr7</a>
        </div>
        <div style="background: #fff9e6; border-radius: 6px; padding: 12px;">
            <p style="margin: 0; color: #f57c00;"><strong>提取码：</strong><span style="font-size: 18px; font-weight: bold; margin-left: 8px;">utr7</span></p>
        </div>
    </div>

    <div style="background: #e8f5e9; border-left: 4px solid #4caf50; padding: 16px; margin: 24px 0; border-radius: 4px;">
        <h3 style="color: #2e7d32; margin: 0 0 8px 0;">💡 使用提示</h3>
        <p style="margin: 0; color: #555; line-height: 1.8;">这份资源适合想要在小红书平台开展业务、寻找合作博主或学习创业内容的用户。建议结合自己的业务需求，筛选出最匹配的博主进行深入研究。</p>
    </div>
</div>
'''

tool, created = Tool.objects.update_or_create(
    slug='xiaohongshu-blogger-database',
    defaults={
        'name': '小红书博主信息数据库',
        'short_description': '14000位赚钱、创业、副业相关小红书博主信息Excel表格，含账号、粉丝等数据',
        'full_description': full_content,
        'website_url': 'https://pan.baidu.com/s/1XdHDpjY1RX31048fnbZbWQ?pwd=utr7',
        'category': category,
        'is_featured': True,
        'is_published': True,
    }
)

print('✓ 已添加：小红书博主信息数据库' if created else '✓ 已更新：小红书博主信息数据库')
