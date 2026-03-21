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
        <h2 style="color: white; margin-bottom: 12px; font-size: 24px;">💼 Expert Equities Research Reviewer</h2>
        <div style="display: flex; gap: 16px; flex-wrap: wrap; margin-top: 16px;">
            <span style="background: rgba(255,255,255,0.2); padding: 6px 12px; border-radius: 4px;">⏰ Part-time</span>
            <span style="background: rgba(255,255,255,0.2); padding: 6px 12px; border-radius: 4px;">🌍 Remote</span>
            <span style="background: rgba(255,255,255,0.2); padding: 6px 12px; border-radius: 4px;">💰 $150-$180/hour</span>
        </div>
    </div>

    <h2 style="color: #667eea; margin-top: 32px; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 2px solid #667eea;">🎯 职位背景</h2>

    <div style="background: #fff; border: 1px solid #e0e0e0; border-radius: 8px; padding: 20px; margin-bottom: 24px;">
        <p style="color: #555; line-height: 1.8; margin-bottom: 12px;">Mercor代表一个正在构建自主AI驱动的公开股票深度研究系统的团队招聘专家股票研究审查员。该系统生成多来源投资研究报告，包括财务建模、估值分析、竞争定位、目标价格和结构化投资论点。</p>
        <p style="color: #555; line-height: 1.8;">在这个角色中，您将评估AI生成的报告的准确性、分析深度和实际投资效用——帮助校准和改进一个旨在达到机构研究标准的系统。这是一个适合经验丰富的投资专业人士的高判断力角色。</p>
    </div>

    <h2 style="color: #667eea; margin-top: 32px; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 2px solid #667eea;">📋 核心职责</h2>

    <div style="background: #f8f9fa; border-radius: 8px; padding: 20px; margin-bottom: 24px;">
        <ul style="line-height: 2; margin: 0; padding-left: 24px; color: #555;">
            <li>审查AI生成的股票研究报告的事实准确性、分析严谨性和逻辑连贯性</li>
            <li>评估投资论点、目标价格和买入/持有/卖出建议，识别不支持的假设或推理缺口</li>
            <li>验证财务指标和建模逻辑，包括：
                <ul style="margin-top: 8px;">
                    <li>收入增长和利润率结构</li>
                    <li>Rule of 40计算</li>
                    <li>TAM估算</li>
                    <li>估值倍数和DCF假设</li>
                </ul>
            </li>
            <li>评估结论是否反映当前市场现实并与公开信息一致</li>
            <li>提供跨关键质量维度的结构化书面反馈，包括：
                <ul style="margin-top: 8px;">
                    <li>来源可靠性</li>
                    <li>声明置信度校准</li>
                    <li>内部一致性</li>
                    <li>覆盖完整性</li>
                </ul>
            </li>
            <li>标记过时数据、误解的指标、有缺陷的估值逻辑或可能误导投资决策者的缺失背景因素</li>
            <li>评估多公司比较分析和行业级评估的方法论合理性和实际相关性</li>
        </ul>
    </div>

    <h2 style="color: #667eea; margin-top: 32px; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 2px solid #667eea;">✅ 任职要求</h2>

    <div style="background: #fff; border: 1px solid #e0e0e0; border-radius: 8px; padding: 20px; margin-bottom: 24px;">
        <p style="color: #555; margin-bottom: 12px;"><strong>必备条件：</strong></p>
        <ul style="line-height: 2; margin: 0 0 16px 0; padding-left: 24px; color: #555;">
            <li>在公开股票研究、投资组合管理或相关买方/卖方角色方面具有专业经验（对冲基金、资产管理、股票研究或投资银行）</li>
            <li>精通基本面分析，包括：
                <ul style="margin-top: 8px;">
                    <li>财务报表解读</li>
                    <li>DCF建模和估值方法</li>
                    <li>可比公司分析</li>
                    <li>基于盈利的预测</li>
                </ul>
            </li>
            <li>能够批判性评估投资论点并提供清晰、具体和可操作的书面反馈</li>
            <li>熟悉审查结构化研究文档（Markdown或PDF格式）</li>
            <li>出色的书面沟通能力——反馈必须精确、分析性强且具有建设性</li>
        </ul>
    </div>

    <h2 style="color: #667eea; margin-top: 32px; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 2px solid #667eea;">🎁 加分项</h2>

    <div style="background: #e8f5e9; border-radius: 8px; padding: 20px; margin-bottom: 24px;">
        <ul style="line-height: 2; margin: 0; padding-left: 24px; color: #2e7d32;">
            <li>CFA资格或正在积极准备中</li>
            <li>有构建或评估量化研究工具、筛选系统或系统化策略的经验</li>
            <li>熟悉AI/LLM在金融研究背景下的能力和局限性</li>
            <li>在科技领域之外的多个行业有覆盖经验</li>
        </ul>
    </div>

    <h2 style="color: #667eea; margin-top: 32px; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 2px solid #667eea;">💡 为什么加入</h2>

    <div style="background: #fff9e6; border-radius: 8px; padding: 20px; margin-bottom: 24px;">
        <ul style="line-height: 2; margin: 0; padding-left: 24px; color: #555;">
            <li>塑造在机构级研究水平运作的前沿AI系统的质量标准</li>
            <li>与构建多代理金融分析系统的工程师和AI研究人员合作</li>
            <li>直接影响AI生成的股票研究如何被验证、校准和改进</li>
            <li>加入为下一代AI辅助投资研究做出贡献的全球高级金融专业人士网络</li>
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
        <p style="color: #2e7d32; line-height: 1.8; margin-bottom: 12px;"><strong>通过推荐赚取高达 $720</strong></p>
        <p style="color: #555; line-height: 1.8; margin-bottom: 12px;">分享下面的推荐链接，每成功推荐一人即可赚取高达 $720。您可以推荐的人数没有限制。可能适用限制条件。</p>
        <div style="background: white; border-radius: 6px; padding: 12px; margin-top: 12px;">
            <a href="https://t.mercor.com/LwTJR" target="_blank" style="color: #667eea; text-decoration: none; word-break: break-all;">https://t.mercor.com/LwTJR</a>
        </div>
    </div>

    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 8px; padding: 20px; text-align: center; margin-top: 32px;">
        <h3 style="color: white; margin: 0 0 12px 0;">💡 为什么选择这个职位？</h3>
        <ul style="list-style: none; padding: 0; margin: 0; line-height: 2;">
            <li>💰 时薪：$150-$180/小时</li>
            <li>🌍 完全远程，灵活时间</li>
            <li>🤖 与前沿AI金融分析系统合作</li>
            <li>🎁 推荐奖励高达 $720/人</li>
            <li>📊 运用专业投资经验塑造AI研究系统</li>
            <li>🏆 加入全球高级金融专业人士网络</li>
        </ul>
    </div>
</div>
'''

tool, created = Tool.objects.update_or_create(
    slug='expert-equities-research-reviewer-mercor',
    defaults={
        'name': 'Expert Equities Research Reviewer - Mercor',
        'short_description': '远程股票研究审查专家，$150-$180/小时，评估AI生成的投资研究报告，需专业投资经验',
        'full_description': full_content,
        'website_url': 'https://t.mercor.com/LwTJR',
        'category': category,
        'is_featured': True,
        'is_published': True,
    }
)

print('✓ 已添加：Expert Equities Research Reviewer - Mercor' if created else '✓ 已更新：Expert Equities Research Reviewer - Mercor')
