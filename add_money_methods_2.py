#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

category = Category.objects.get(name='赚钱技巧')

tools_data = [
    {
        'name': 'AI祈福漫画变现法',
        'short_description': '春节等节点制作祈福漫画，通过公众号赞赏和流量主变现',
        'full_description': '''**操作方法：**
1. 选择时机：春节、中秋等传统节日
2. 目标人群：中老年群体（情感共鸣强）
3. 制作流程：
   - 使用Nano Banana Pro生成温馨漫画风格图片
   - 添加祝福语和吉祥元素
   - 制作成图文或短视频形式
4. 发布平台：公众号、视频号
5. 变现方式：
   - 公众号赞赏
   - 流量主广告收益
   - 引流私域售卖周边

**关键要点：**
- 内容要温馨感人，触动情感
- 针对中老年人审美和价值观
- 节日前1-2周开始预热''',
        'website_url': 'http://ai-tool.indevs.in/',
        'category': category
    },
    {
        'name': 'AI爆款漫剧制作变现',
        'short_description': 'AI漫剧低成本产出，获得超10亿播放，商单+流量激励变现',
        'full_description': '''**操作方法：**
1. 选题策划：选择热门小说或原创剧本
2. 制作工具：
   - Seedance 2.0：解决人物一致性和运镜
   - Kling/Vidu：图转视频
   - Suno/MiniMax：配乐配音
3. 制作流程：
   - 分镜脚本设计
   - AI生成角色和场景
   - 视频剪辑和配音
   - 精细化调整（非一句话直出）
4. 发布平台：抖音、快手、B站
5. 变现方式：
   - 商单广告
   - 平台流量激励
   - IP授权和定制

**成功案例：**
《斩仙台下》通过精细化AI视频制作，获得超10亿播放量

**关键要点：**
- 精细化制作，不要低质量直出
- 保持人物一致性
- 剧情要有吸引力和悬念''',
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

print('\n第二批赚钱技巧完成！')
