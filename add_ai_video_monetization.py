import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

# 获取AI课程分类
category, _ = Category.objects.get_or_create(
    name='AI课程',
    defaults={'description': 'AI相关的学习课程和教程', 'order': 5}
)

# 添加AI视频变现教程
tool, created = Tool.objects.get_or_create(
    name='2026年AI视频变现全攻略',
    defaults={
        'short_description': '普通人用AI制作高级场景对话视频的完整教程，从提示词到变现',
        'full_description': '''2026年普通人AI视频变现全攻略——一节课解密高级场景对话视频制作全流程：

【核心理念】
无需专业摄影棚和演员，普通人只需掌握提示词和剪辑逻辑，就能快速生成用于品牌赋能、门店引流或知识分享的专业视频。

【四大核心板块】
1. 核心灵魂：提示词（Prompt）
2. 人物形象：男女主角照片（无需实拍）
3. 内容骨架：口播文案
4. 后期包装：视频精剪与修复

【第一步：精准提示词（最关键）】
高质量提示词必须包含6大要素：
• 分镜脚本设计：明确镜头编号、画面内容、景别
• 场景搭建规范：详细描述环境氛围
• 表演指导：指定人物情绪和动作
• 完整脚本文案：画面描述和配音文本对照
• 制作注意事项：隐晦加入画质要求（4k画质、电影感光影）
• 结尾必加指令：全程中文介绍，不显示文字

【第二步：工具实操】
• 视频生成工具：玫瑰AI / 小云雀（调用最火爆大模型）
• 人物形象准备：上传艺术照或用"星绘"制作数字照片
• 文案时长控制：
  - 小云雀：最长15秒
  - 玫瑰AI：最长8秒
  - 策略：拆分长文案为多个短句分别生成后拼接

【第三步：后期精剪】
使用"开拍工具"进行三维修缮：
1. 画质修复：超清化处理，提升高级感
2. 去水印与纠错：净化画面，去除乱码文字
3. 网感包装：添加动态字幕，专业自媒体效果

【完整行动清单】
1. 写文案：梳理专业知识或对话内容
2. 拆脚本：按8-15秒分段，撰写分镜提示词
3. 生素材：用玫瑰AI/小云雀生成视频片段
4. 做精修：用开拍工具修复画质、去水印、加字幕
5. 导出发布：合成完整视频，赋能行业

【适合人群】
品牌主、门店老板、知识博主、自媒体创作者''',
        'website_url': 'https://articles.zsxq.com/id_swrhdqmz5lq3.html',
        'category': category,
        'is_published': True,
    }
)

if created:
    print(f'✅ 已添加: {tool.name}')
else:
    print(f'⚠️  已存在: {tool.name}')
