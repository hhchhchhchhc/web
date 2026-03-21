#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

# 创建或获取分类
category, _ = Category.objects.get_or_create(
    name='电商运营工具',
    defaults={
        'description': '电商平台运营与营销工具',
        'order': 60
    }
)

# 完整的HTML内容
full_content = '''
<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', sans-serif; line-height: 1.8; color: #333;">
    <div style="background: linear-gradient(135deg, #e4002b 0%, #ff6b6b 100%); color: white; padding: 24px; margin-bottom: 24px; border-radius: 8px; text-align: center;">
        <h2 style="color: white; margin-bottom: 12px; font-size: 24px;">🎁 京东官方免费数字人直播</h2>
        <p style="font-size: 16px; opacity: 0.95;">限时福利：免费获得1年数字人直播权益</p>
    </div>

    <div style="background: #fff3e0; border-left: 4px solid #ff9800; padding: 16px; margin-bottom: 24px; border-radius: 4px;">
        <h3 style="color: #e65100; margin: 0 0 12px 0;">🎉 限时福利</h3>
        <p style="margin: 0; color: #666; line-height: 1.8; font-size: 16px;">京东官方现在免费赠送<strong style="color: #e4002b;">数字人直播权益1年</strong>，有店铺的商家可以免费领取使用！</p>
    </div>

    <h2 style="color: #e4002b; margin-top: 32px; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 2px solid #e4002b;">📋 如何领取</h2>

    <div style="background: #fff; border: 1px solid #e0e0e0; border-radius: 8px; padding: 20px; margin-bottom: 24px;">
        <ol style="line-height: 2.2; margin: 0; padding-left: 24px; color: #555;">
            <li style="margin-bottom: 12px;">
                <strong>登录京麦服务市场</strong><br>
                <span style="color: #666;">访问：</span>
                <a href="https://fw.jd.com/market/new/index" target="_blank" style="color: #e4002b; text-decoration: none;">https://fw.jd.com/market/new/index</a>
            </li>
            <li style="margin-bottom: 12px;">
                <strong>找到数字人直播服务</strong><br>
                <span style="color: #666;">在服务市场中搜索或浏览数字人直播相关服务</span>
            </li>
            <li>
                <strong>领取免费权益</strong><br>
                <span style="color: #666;">按照页面提示领取1年免费使用权</span>
            </li>
        </ol>
    </div>

    <h2 style="color: #e4002b; margin-top: 32px; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 2px solid #e4002b;">✨ 数字人直播优势</h2>

    <div style="display: grid; gap: 16px; margin-bottom: 24px;">
        <div style="background: #f8f9fa; border-left: 4px solid #28a745; padding: 16px; border-radius: 4px;">
            <h3 style="color: #28a745; margin: 0 0 8px 0; font-size: 18px;">⏰ 24小时不间断</h3>
            <p style="margin: 0; color: #555;">数字人可以全天候直播，无需休息，覆盖更多时段</p>
        </div>

        <div style="background: #f8f9fa; border-left: 4px solid #007bff; padding: 16px; border-radius: 4px;">
            <h3 style="color: #007bff; margin: 0 0 8px 0; font-size: 18px;">💰 降低成本</h3>
            <p style="margin: 0; color: #555;">相比真人主播，数字人直播大幅降低人力成本</p>
        </div>

        <div style="background: #f8f9fa; border-left: 4px solid #dc3545; padding: 16px; border-radius: 4px;">
            <h3 style="color: #dc3545; margin: 0 0 8px 0; font-size: 18px;">🎯 标准化输出</h3>
            <p style="margin: 0; color: #555;">确保每次直播内容的一致性和专业性</p>
        </div>

        <div style="background: #f8f9fa; border-left: 4px solid #ffc107; padding: 16px; border-radius: 4px;">
            <h3 style="color: #f57c00; margin: 0 0 8px 0; font-size: 18px;">🚀 快速上线</h3>
            <p style="margin: 0; color: #555;">无需培训主播，配置好即可立即开播</p>
        </div>
    </div>

    <h2 style="color: #e4002b; margin-top: 32px; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 2px solid #e4002b;">🎯 适用场景</h2>

    <div style="background: #fff; border: 1px solid #e0e0e0; border-radius: 8px; padding: 20px; margin-bottom: 24px;">
        <ul style="line-height: 2; margin: 0; padding-left: 24px; color: #555;">
            <li>📦 <strong>商品展示</strong> - 持续展示店铺商品特点和优势</li>
            <li>🎁 <strong>促销活动</strong> - 24小时不间断宣传促销信息</li>
            <li>💬 <strong>客户互动</strong> - 自动回答常见问题，引导下单</li>
            <li>🏪 <strong>店铺引流</strong> - 增加店铺曝光度和流量</li>
            <li>🌙 <strong>夜间直播</strong> - 覆盖夜间购物人群</li>
        </ul>
    </div>

    <div style="background: #e8f5e9; border-left: 4px solid #4caf50; padding: 16px; margin: 24px 0; border-radius: 4px;">
        <h3 style="color: #2e7d32; margin: 0 0 8px 0;">💡 温馨提示</h3>
        <p style="margin: 0; color: #555; line-height: 1.8;">此福利仅限京东商家使用，需要先在京东开设店铺。数字人直播可以作为真人直播的补充，在非高峰时段或夜间使用，帮助店铺保持持续曝光。</p>
    </div>

    <div style="background: #fff9e6; border-left: 4px solid #ffc107; padding: 16px; margin: 24px 0; border-radius: 4px;">
        <h3 style="color: #f57c00; margin: 0 0 8px 0;">⚠️ 注意事项</h3>
        <ul style="margin: 8px 0 0 0; padding-left: 24px; color: #666; line-height: 1.8;">
            <li>免费权益为限时活动，建议尽快领取</li>
            <li>需要登录京麦商家后台才能访问服务市场</li>
            <li>具体使用规则以京东官方说明为准</li>
        </ul>
    </div>
</div>
'''

# 创建或更新工具
tool, created = Tool.objects.update_or_create(
    slug='jd-digital-human-live',
    defaults={
        'name': '京东数字人直播',
        'short_description': '京东官方免费提供1年数字人直播权益，24小时不间断直播，降低运营成本',
        'full_description': full_content,
        'website_url': 'https://fw.jd.com/market/new/index',
        'category': category,
        'is_featured': True,
        'is_published': True,
    }
)

if created:
    print('✓ 已添加：京东数字人直播')
else:
    print('✓ 已更新：京东数字人直播')
