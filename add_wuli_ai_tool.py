#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

# 创建或获取分类
category, _ = Category.objects.get_or_create(
    name='AI图像视频生成',
    defaults={
        'description': 'AI图像和视频生成工具',
        'order': 10
    }
)

# 完整的HTML内容
full_content = '''
<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', sans-serif; line-height: 1.8; color: #333;">
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 24px; margin-bottom: 24px; border-radius: 8px; text-align: center;">
        <h2 style="color: white; margin-bottom: 12px; font-size: 24px;">🎨 呜哩AI - 一站式AIGC创意平台</h2>
        <p style="font-size: 16px; opacity: 0.95;">Qwen Image、Seedream 4.5、万相2.6、可灵 Q1 无限用，还免费！</p>
    </div>

    <h2 style="color: #667eea; margin-top: 32px; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 2px solid #667eea;">✨ 核心优势</h2>

    <div style="display: grid; gap: 16px; margin-bottom: 24px;">
        <div style="background: #f8f9fa; border-left: 4px solid #28a745; padding: 16px; border-radius: 4px;">
            <h3 style="color: #28a745; margin: 0 0 8px 0; font-size: 18px;">💰 完全免费</h3>
            <p style="margin: 0; color: #555;">目前所有功能都免费，没有次数限制</p>
        </div>

        <div style="background: #f8f9fa; border-left: 4px solid #007bff; padding: 16px; border-radius: 4px;">
            <h3 style="color: #007bff; margin: 0 0 8px 0; font-size: 18px;">🤖 模型丰富</h3>
            <p style="margin: 0; color: #555;">集成了通义、字节、可灵等多个顶级模型</p>
        </div>

        <div style="background: #f8f9fa; border-left: 4px solid #dc3545; padding: 16px; border-radius: 4px;">
            <h3 style="color: #dc3545; margin: 0 0 8px 0; font-size: 18px;">🎯 质量高</h3>
            <p style="margin: 0; color: #555;">生图能直出 4K，生视频能直出 1080p</p>
        </div>

        <div style="background: #f8f9fa; border-left: 4px solid #ffc107; padding: 16px; border-radius: 4px;">
            <h3 style="color: #f57c00; margin: 0 0 8px 0; font-size: 18px;">⚡ 速度快</h3>
            <p style="margin: 0; color: #555;">生图几秒钟，生视频 1-2 分钟</p>
        </div>
    </div>

    <h2 style="color: #667eea; margin-top: 32px; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 2px solid #667eea;">🛠️ 功能特性</h2>

    <div style="background: #fff; border: 1px solid #e0e0e0; border-radius: 8px; padding: 20px; margin-bottom: 24px;">
        <h3 style="color: #333; margin-top: 0; margin-bottom: 16px;">支持的模型</h3>
        <ul style="line-height: 2; margin: 0; padding-left: 24px; color: #555;">
            <li><strong>Qwen Image</strong> - 阿里通义千问图像生成模型</li>
            <li><strong>Seedream 4.5</strong> - 高质量图像生成</li>
            <li><strong>万相2.6</strong> - 多样化图像创作</li>
            <li><strong>可灵 Q1</strong> - 视频生成模型</li>
        </ul>
    </div>

    <div style="background: #fff; border: 1px solid #e0e0e0; border-radius: 8px; padding: 20px; margin-bottom: 24px;">
        <h3 style="color: #333; margin-top: 0; margin-bottom: 16px;">支持的功能</h3>
        <ul style="line-height: 2; margin: 0; padding-left: 24px; color: #555;">
            <li>📝 <strong>文生图</strong> - 通过文字描述生成图像</li>
            <li>🖼️ <strong>图生图</strong> - 基于参考图像生成新图像</li>
            <li>🎬 <strong>文生视频</strong> - 通过文字描述生成视频</li>
            <li>🎥 <strong>图生视频</strong> - 将静态图像转换为动态视频</li>
            <li>🔄 <strong>参考生成</strong> - 支持参考图生成图像和视频</li>
        </ul>
    </div>

    <h2 style="color: #667eea; margin-top: 32px; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 2px solid #667eea;">📊 输出质量</h2>

    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 24px;">
        <div style="background: #e3f2fd; padding: 20px; border-radius: 8px; text-align: center;">
            <div style="font-size: 36px; margin-bottom: 8px;">4K</div>
            <div style="color: #1976d2; font-weight: bold;">图像分辨率</div>
        </div>
        <div style="background: #f3e5f5; padding: 20px; border-radius: 8px; text-align: center;">
            <div style="font-size: 36px; margin-bottom: 8px;">1080p</div>
            <div style="color: #7b1fa2; font-weight: bold;">视频分辨率</div>
        </div>
    </div>

    <div style="background: #fff3e0; border-left: 4px solid #ff9800; padding: 16px; margin: 24px 0; border-radius: 4px;">
        <h3 style="color: #e65100; margin: 0 0 8px 0;">💡 使用提示</h3>
        <p style="margin: 0; color: #666; line-height: 1.8;">呜哩AI作为一站式AIGC创意平台，整合了多个顶级AI模型，让您无需在不同平台间切换，即可体验最新的图像和视频生成技术。完全免费且无次数限制，是创作者的理想选择。</p>
    </div>
</div>
'''

# 创建或更新工具
tool, created = Tool.objects.update_or_create(
    slug='wuli-ai',
    defaults={
        'name': '呜哩AI',
        'short_description': 'Qwen Image、Seedream 4.5、万相2.6、可灵 Q1无限用，完全免费的一站式AIGC创意平台',
        'full_description': full_content,
        'website_url': 'https://wuli.art/generate',
        'category': category,
        'is_featured': True,
        'is_published': True,
    }
)

if created:
    print('✓ 已添加：呜哩AI')
else:
    print('✓ 已更新：呜哩AI')
