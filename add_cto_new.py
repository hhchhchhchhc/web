#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

category, _ = Category.objects.get_or_create(
    name='AI对话助手',
    defaults={'description': 'AI对话和聊天助手工具', 'order': 5}
)

full_content = '''
<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', sans-serif; line-height: 1.8; color: #333;">
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 24px; margin-bottom: 24px; border-radius: 8px; text-align: center;">
        <h2 style="color: white; margin-bottom: 12px; font-size: 24px;">🚀 CTO.NEW</h2>
        <p style="font-size: 16px; opacity: 0.95;">永久免费使用顶级AI模型</p>
    </div>

    <div style="background: #e8f5e9; border-left: 4px solid #4caf50; padding: 16px; margin-bottom: 24px; border-radius: 4px;">
        <h3 style="color: #2e7d32; margin: 0 0 12px 0;">✨ 永久免费</h3>
        <p style="margin: 0; color: #555; line-height: 1.8; font-size: 16px;">CTO.NEW 提供<strong style="color: #2e7d32;">永久免费</strong>的AI模型访问服务，无需付费即可使用顶级模型。</p>
    </div>

    <h2 style="color: #667eea; margin-top: 32px; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 2px solid #667eea;">🤖 支持的顶级模型</h2>

    <div style="display: grid; gap: 16px; margin-bottom: 24px;">
        <div style="background: #f8f9fa; border-left: 4px solid #007bff; padding: 16px; border-radius: 4px;">
            <h3 style="color: #007bff; margin: 0 0 8px 0; font-size: 18px;">GPT-5.2</h3>
            <p style="margin: 0; color: #555;">OpenAI 最新一代语言模型</p>
        </div>

        <div style="background: #f8f9fa; border-left: 4px solid #dc3545; padding: 16px; border-radius: 4px;">
            <h3 style="color: #dc3545; margin: 0 0 8px 0; font-size: 18px;">Claude 4.5</h3>
            <p style="margin: 0; color: #555;">Anthropic 高性能对话模型</p>
        </div>

        <div style="background: #f8f9fa; border-left: 4px solid #ffc107; padding: 16px; border-radius: 4px;">
            <h3 style="color: #f57c00; margin: 0 0 8px 0; font-size: 18px;">Gemini 2.5 Pro</h3>
            <p style="margin: 0; color: #555;">Google 顶级多模态模型</p>
        </div>
    </div>

    <h2 style="color: #667eea; margin-top: 32px; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 2px solid #667eea;">💡 核心优势</h2>

    <div style="background: #fff; border: 1px solid #e0e0e0; border-radius: 8px; padding: 20px; margin-bottom: 24px;">
        <ul style="line-height: 2; margin: 0; padding-left: 24px; color: #555;">
            <li>💰 <strong>永久免费</strong> - 无需付费订阅</li>
            <li>🎯 <strong>顶级模型</strong> - 集成最新最强的AI模型</li>
            <li>🚀 <strong>快速访问</strong> - 无需复杂配置，即开即用</li>
            <li>🔄 <strong>多模型切换</strong> - 灵活选择最适合的模型</li>
        </ul>
    </div>

    <div style="background: #fff3e0; border-left: 4px solid #ff9800; padding: 16px; margin: 24px 0; border-radius: 4px;">
        <h3 style="color: #e65100; margin: 0 0 8px 0;">💡 使用提示</h3>
        <p style="margin: 0; color: #666; line-height: 1.8;">CTO.NEW 为用户提供了一个便捷的平台，可以免费体验和使用多个顶级AI模型，适合开发者、研究人员和AI爱好者使用。</p>
    </div>
</div>
'''

tool, created = Tool.objects.update_or_create(
    slug='cto-new',
    defaults={
        'name': 'CTO.NEW',
        'short_description': '永久免费使用GPT-5.2、Claude 4.5、Gemini 2.5 Pro等顶级AI模型',
        'full_description': full_content,
        'website_url': 'https://cto.new',
        'category': category,
        'is_featured': True,
        'is_published': True,
    }
)

print('✓ 已添加：CTO.NEW' if created else '✓ 已更新：CTO.NEW')
