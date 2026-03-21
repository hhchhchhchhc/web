#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Tool, Category

category = Category.objects.get(id=706)

tools_data = [
    {
        'name': 'Google Cloud Vertex AI - $300免费额度',
        'slug': 'google-vertex-ai-300-credit',
        'short_description': 'Google Cloud官方支持Claude，新用户$300免费额度（90天），稳定性极高，支持Claude全系列模型',
        'full_description': '''Google Cloud Vertex AI - $300免费额度

✅ 推荐指数：⭐⭐⭐⭐⭐

免费额度：新用户$300，有效期90天
支持模型：Claude 3.5 Sonnet、Claude 3 Opus、Claude 3 Haiku
特点：Google Cloud官方支持，稳定性极高

使用方法：
1. 注册Google Cloud账号（需要信用卡验证，但不会扣费）
2. 激活$300免费试用额度（90天有效期）
3. 在Vertex AI中启用Claude模型
4. 创建服务账号并获取API密钥
5. 通过Vertex AI API调用Claude模型

优势：
• $300额度非常充足，可以使用数月
• Google Cloud基础设施，稳定性和速度极佳
• 支持Claude全系列模型
• 企业级安全保障
• 详细的使用文档和技术支持

⚠️ 注意事项
• 需要国际信用卡验证（不会扣费）
• 90天后需要升级为付费账户或停止使用
• 部分地区可能需要科学上网
• 注意监控使用量，避免超出免费额度''',
        'website_url': 'https://cloud.google.com/vertex-ai',
    },
    {
        'name': 'AWS Bedrock - 12个月免费套餐',
        'slug': 'aws-bedrock-free-tier',
        'short_description': 'AWS官方支持Claude，新用户12个月免费套餐，与AWS生态深度集成，企业级安全',
        'full_description': '''AWS Bedrock - 12个月免费套餐

✅ 推荐指数：⭐⭐⭐⭐⭐

免费额度：新用户12个月免费套餐，包含一定量的Claude调用
支持模型：Claude 3.5 Sonnet、Claude 3 Opus、Claude 3 Haiku、Claude 3 Sonnet
特点：AWS官方支持，与AWS生态深度集成

使用方法：
1. 注册AWS账号（需要信用卡验证）
2. 激活12个月免费套餐
3. 在AWS Bedrock中启用Claude模型访问权限
4. 创建IAM用户并配置访问密钥
5. 通过AWS SDK或API调用Claude模型

优势：
• 12个月免费期，时间充足
• AWS全球基础设施，速度快
• 与AWS其他服务无缝集成（Lambda、S3等）
• 企业级安全和合规性
• 支持多个Claude模型版本

⚠️ 注意事项
• 需要国际信用卡验证
• 免费套餐有使用量限制，超出部分按量付费
• 需要申请模型访问权限（通常1-2个工作日）
• 注意AWS区域选择，部分区域可能不支持Claude''',
        'website_url': 'https://aws.amazon.com/bedrock',
    },
]

print(f'准备添加 {len(tools_data)} 个云服务提供商工具\n')

for tool_data in tools_data:
    existing = Tool.objects.filter(slug=tool_data['slug']).first()
    if existing:
        print(f'⏭️  跳过已存在: {tool_data["name"]}')
        continue

    tool = Tool.objects.create(**{**tool_data, 'category': category, 'is_featured': True, 'is_published': True})
    print(f'✅ 成功添加: {tool.name}')

print('\n完成云服务提供商工具添加！')
