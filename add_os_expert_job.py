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

    <h2 style="color: #667eea; margin-top: 32px; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 2px solid #667eea;">🏢 关于公司</h2>

    <div style="background: #fff; border: 1px solid #e0e0e0; border-radius: 8px; padding: 20px; margin-bottom: 24px;">
        <p style="margin: 0 0 12px 0;"><strong style="color: #667eea;">Mercor</strong></p>
        <p style="margin: 0; color: #555; line-height: 1.8;">Mercor 与领先的 AI 实验室和企业合作，利用人类专业知识训练前沿模型。您将参与专注于训练和增强 AI 系统的项目，获得有竞争力的报酬，与顶尖研究人员合作，并帮助塑造您专业领域的下一代 AI 系统。</p>
        <p style="margin: 12px 0 0 0;"><a href="https://mercor.com" target="_blank" style="color: #667eea; text-decoration: none;">🔗 mercor.com</a></p>
    </div>

    <h2 style="color: #667eea; margin-top: 32px; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 2px solid #667eea;">🎯 项目背景</h2>

    <div style="background: #fff; border: 1px solid #e0e0e0; border-radius: 8px; padding: 20px; margin-bottom: 24px;">
        <p style="color: #555; line-height: 1.8; margin-bottom: 12px;">Mercor 正在支持一项高优先级的数据收集计划，旨在改进 AI 系统对复杂软件界面和真实多步骤工作流程的理解。当前数据集缺乏反映真实专业软件使用所需的保真度和专家基础。</p>
        <p style="color: #555; line-height: 1.8;">该项目通过收集由经验丰富的领域专家在真实数字环境中执行的高质量屏幕标注和屏幕录制来解决这一差距。</p>
    </div>

    <h2 style="color: #667eea; margin-top: 32px; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 2px solid #667eea;">📋 工作内容</h2>

    <div style="background: #f8f9fa; border-radius: 8px; padding: 20px; margin-bottom: 24px;">
        <p style="color: #555; margin-bottom: 12px;">根据任务阶段，您可能需要完成以下一项或两项工作：</p>
        <ul style="line-height: 2; margin: 0; padding-left: 24px; color: #555;">
            <li>录制演示特定任务的屏幕会话，并配以清晰的口头解说，解释每个步骤</li>
            <li>通过在相关 UI 元素周围绘制精确的边界框来标注专业软件的屏幕截图</li>
            <li>按照提供的准备说明在录制前设置特定的 UI 状态</li>
            <li>使用自定义捕获工具准确一致地录制工作流程</li>
            <li>严格遵守任务指南以确保数据质量和可用性</li>
        </ul>
    </div>

    <h2 style="color: #667eea; margin-top: 32px; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 2px solid #667eea;">✅ 任职要求</h2>

    <div style="background: #fff; border: 1px solid #e0e0e0; border-radius: 8px; padding: 20px; margin-bottom: 24px;">
        <p style="color: #555; margin-bottom: 12px;"><strong>必备技能：</strong></p>
        <ul style="line-height: 2; margin: 0 0 16px 0; padding-left: 24px; color: #555;">
            <li>熟悉专业软件工具，包括：<strong>Windows、MacOS、Linux</strong></li>
            <li>注重细节，能够遵循精确的指令</li>
            <li>能够独立工作并满足紧迫的截止日期</li>
            <li>拥有物理 Mac 设备，并能在需要时创建新的 macOS 用户配置文件</li>
        </ul>
        <p style="color: #555; margin-bottom: 12px;"><strong>加分项：</strong></p>
        <ul style="line-height: 2; margin: 0; padding-left: 24px; color: #555;">
            <li>有数据收集、标注或 QA 工作经验</li>
            <li>有录制或记录工作流程的经验</li>
            <li>熟悉使用新工具和准备环境</li>
        </ul>
    </div>

    <h2 style="color: #667eea; margin-top: 32px; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 2px solid #667eea;">🎯 成功标准</h2>

    <div style="background: #e8f5e9; border-radius: 8px; padding: 20px; margin-bottom: 24px;">
        <ul style="line-height: 2; margin: 0; padding-left: 24px; color: #2e7d32;">
            <li>屏幕标注精确、一致且符合指南</li>
            <li>屏幕录制准确捕获真实的专家工作流程</li>
            <li>在保持高质量的同时高效完成任务</li>
            <li>收集的数据可用于下游 AI 研究和开发</li>
        </ul>
    </div>

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
        <p style="color: #2e7d32; line-height: 1.8; margin-bottom: 12px;"><strong>通过推荐赚取高达 $400</strong></p>
        <p style="color: #555; line-height: 1.8; margin-bottom: 12px;">分享下面的推荐链接，每成功推荐一人即可赚取高达 $400。您可以推荐的人数没有限制。可能适用限制条件。</p>
        <div style="background: white; border-radius: 6px; padding: 12px; margin-top: 12px;">
            <a href="https://t.mercor.com/BzQSY" target="_blank" style="color: #667eea; text-decoration: none; word-break: break-all;">https://t.mercor.com/BzQSY</a>
        </div>
    </div>

    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 8px; padding: 20px; text-align: center; margin-top: 32px;">
        <h3 style="color: white; margin: 0 0 12px 0;">💡 为什么选择这个职位？</h3>
        <ul style="list-style: none; padding: 0; margin: 0; line-height: 2;">
            <li>💰 灵活时薪：$0-$100/小时</li>
            <li>🌍 完全远程，自由安排时间</li>
            <li>🔥 本月已招聘141人，机会真实可靠</li>
            <li>🤖 参与前沿 AI 训练数据收集</li>
            <li>🎁 推荐奖励高达 $400/人</li>
        </ul>
    </div>
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
