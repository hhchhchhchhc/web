#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

category = Category.objects.get(name='赚钱技巧')

tools_data = [
    {
        'name': '经典IP二创变现法',
        'short_description': 'AI复刻热门动画或小说名场面，起号后接广告或卖号变现',
        'full_description': '''**操作方法：**
1. 选择IP：热门动画、小说的经典场景
2. 制作工具：
   - Nano Banana Pro：生成角色和场景
   - Seedance 2.0/Kling：制作视频
3. 制作流程：
   - 选择经典名场面或热门片段
   - AI重新演绎（画风、角色可调整）
   - 添加字幕和配音
4. 发布平台：抖音、B站、小红书
5. 变现方式：
   - 账号涨粉后接广告
   - 直接卖号（粉丝量达标）
   - 引流到私域售卖周边

**关键要点：**
- 选择有情怀的经典IP
- 保持原作精神和质量
- 避免侵权，做好二创标注''',
        'website_url': 'http://ai-tool.indevs.in/',
        'category': category
    },
    {
        'name': 'AI原创玩偶手办变现',
        'short_description': 'AI生成玩偶形象并3D打印实物，或为万物制作手办风格图定制',
        'full_description': '''**操作方法：**
1. 设计阶段：
   - 使用Nano Banana Pro生成手办风格角色
   - 调整细节和配色
2. 实物制作：
   - 3D建模（可用AI辅助）
   - 3D打印或找工厂生产
3. 定制服务：
   - 为客户的宠物、照片制作手办风格图
   - 提供实物手办定制
4. 销售渠道：
   - 小红书、闲鱼售卖
   - 淘宝开店
   - 线下展会摆摊
5. 定价：虚拟图19.9-49.9元，实物手办99-299元

**关键要点：**
- 建立个人IP和品牌
- 注重细节和质量
- 可先卖虚拟图测试市场''',
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

print('\n第三批赚钱技巧完成！')
