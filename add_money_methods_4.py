#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

category = Category.objects.get(name='赚钱技巧')

tools_data = [
    {
        'name': 'AI带货矩阵变现法',
        'short_description': 'AI生成逼真美女或商品背景图进行带货，抖音图文销量榜热门模式',
        'full_description': '''**操作方法：**
1. 账号矩阵：批量注册多个抖音账号
2. 内容制作：
   - 使用Nano Banana Pro生成逼真的美女形象
   - 或为商品生成精美背景图
   - 制作图文带货内容
3. 选品策略：
   - 高佣金产品（服装、美妆、家居）
   - 应季热销商品
4. 发布策略：
   - 每天定时发布3-5条
   - 多账号交替发布
5. 变现方式：
   - 抖音小店佣金
   - 橱窗带货分成

**成功数据：**
抖音图文销量榜上已有大量账号采用此模式

**关键要点：**
- AI生成图片要逼真自然
- 选品要精准匹配目标人群
- 持续优化爆款内容''',
        'website_url': 'http://ai-tool.indevs.in/',
        'category': category
    },
    {
        'name': 'AI工具教程售卖变现',
        'short_description': '在闲鱼卖AI工具部署与安装教程，需求量极大',
        'full_description': '''**操作方法：**
1. 选择热门工具：
   - Claude Code、Clawdbot部署教程
   - OpenClaw安装使用教程
   - 免费GPU平台使用指南
2. 制作教程：
   - 录制详细视频教程
   - 编写图文安装文档
   - 提供常见问题解答
3. 销售平台：
   - 闲鱼（主推）
   - 淘宝
   - 小红书私信
4. 定价策略：9.9-29.9元
5. 增值服务：
   - 提供远程协助（加价）
   - 售后答疑群

**市场需求：**
AI工具部署教程需求量极大，尤其是技术门槛较高的工具

**关键要点：**
- 教程要详细易懂
- 及时更新版本
- 提供良好售后服务''',
        'website_url': 'http://ai-tool.indevs.in/',
        'category': category
    },
]

for tool_data in tools_data:
    tool, created = Tool.objects.get_or_create(
        name=tool_data['name'],
        defaults=tool_data
    )

    if created:
        print(f'✓ 已添加: {tool.name}')
    else:
        print(f'- 已存在: {tool.name}')

print('\n第四批赚钱技巧完成！')
