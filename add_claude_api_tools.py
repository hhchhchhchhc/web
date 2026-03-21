#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Tool, Category

# 获取分类
category = Category.objects.get(id=706)  # 免费用最高级大模型

# 定义要添加的工具列表
tools_data = [
    {
        'name': 'Anthropic官方新用户$5免费额度',
        'slug': 'anthropic-free-5-credit',
        'short_description': '注册Anthropic官方账号即可获得$5免费额度，可调用约25万tokens，适合所有新用户',
        'full_description': '''Anthropic官方新用户$5免费额度

✅ 推荐指数：⭐⭐⭐⭐⭐

获取方式：注册Anthropic官方账号即可获得$5免费额度
使用期限：通常为1-3个月
适用人群：所有新用户

操作步骤：
1. 访问 console.anthropic.com 注册账号
2. 完成邮箱验证
3. 在API Keys页面创建密钥
4. 开始使用，$5额度可调用约25万tokens

⚠️ 注意事项
• 需要国际信用卡绑定（即使不扣费）
• 部分地区可能需要科学上网
• 额度用完后需付费续费''',
        'website_url': 'https://console.anthropic.com',
    },
    {
        'name': 'Anthropic学生计划$50免费额度',
        'slug': 'anthropic-student-50-credit',
        'short_description': '通过学生认证获得$50免费额度，有效期6-12个月，适合在校学生和教育工作者',
        'full_description': '''Anthropic学生计划$50免费额度

✅ 推荐指数：⭐⭐⭐⭐⭐

获取方式：通过学生认证获得$50免费额度
使用期限：6-12个月
适用人群：在校学生、教育工作者

申请条件：
• 拥有有效的学生邮箱（.edu或学校域名）
• 或提供学生证明文件
• 年满18岁

申请流程：
1. 访问Anthropic官网的教育计划页面
2. 填写申请表格，上传学生证明
3. 等待审核（通常1-3个工作日）
4. 审核通过后，$50额度自动充值到账户''',
        'website_url': 'https://console.anthropic.com',
    },
]

print(f'准备添加 {len(tools_data)} 个工具到分类：{category.name}\n')

# 添加工具
for tool_data in tools_data:
    # 检查工具是否已存在
    existing = Tool.objects.filter(slug=tool_data['slug']).first()
    if existing:
        print(f'⏭️  跳过已存在的工具: {tool_data["name"]}')
        continue

    # 创建新工具
    tool = Tool.objects.create(
        name=tool_data['name'],
        slug=tool_data['slug'],
        short_description=tool_data['short_description'],
        full_description=tool_data['full_description'],
        website_url=tool_data['website_url'],
        category=category,
        is_featured=True,
        is_published=True,
    )
    print(f'✅ 成功添加工具: {tool.name}')

print(f'\n完成！')
