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

# 添加AI复刻技术教程
tool, created = Tool.objects.get_or_create(
    name='AI复刻技术短视频变现教程',
    defaults={
        'short_description': '零门槛AI换脸技术，一张照片轻松制作高级感短视频',
        'full_description': '''2026年短视频新变现：AI复刻技术教程

【什么是AI复刻技术】
利用人工智能算法将图片中的人物形象无缝融合到指定视频中，实现精准换脸，同步更换服装、背景、手持物品等元素。堪称"升级版AI数字人"，让每个人都能成为短视频主角。

【核心优势】
• 高效率：几分钟完成一条高质量短视频
• 低门槛：无需拍摄、剪辑技能
• 个性化强：结合个人形象与优质内容模板
• 应用场景广：知识分享、商品展示、情景短剧、个人品牌塑造

【推荐平台】
众馨AI智能体平台，支持电脑与手机双端操作

【操作步骤】
1. 准备个人形象素材
   - 使用日常照片或"星绘"等AI艺术照软件生成
   - 确保人物面部清晰、无遮挡

2. 选择原视频素材
   - 在抖音等平台搜索行业关键词
   - 关键点：原视频第一帧必须有人物正面出镜，脸部无遮挡

3. 提交指令与生成
   - 输入指令："帮我把视频中的人物替换成图片中的人物"
   - 支持视频时长最长30秒
   - 可同步完成换脸、换装等操作

【电脑端操作】
访问 https://ai.zhongxinkeji.shop/home/
使用微信扫码登录（需提前开通账号并获得授权）

【手机端操作】
通过微信公众号"众馨"进入，点击左下角菜单栏"AI换人"功能

【实用技巧】
• 素材选择：原视频光线充足、人物动作清晰效果更佳
• 内容定位：结合自身行业选择原视频，保持内容垂直度
• 效果优化：如效果不理想，可调整图片角度或尝试不同原视频
• 视频制作时长：10分钟足矣
• 下载方式：电脑端直接下载，手机端需复制链接用QQ浏览器下载

【注意事项】
请遵守平台规则与社会公序良俗，尊重他人肖像权与版权，创作积极健康的内容。''',
        'website_url': 'https://articles.zsxq.com/id_c12w1zgz3t11.html',
        'category': category,
        'is_published': True,
    }
)

if created:
    print(f'✅ 已添加: {tool.name}')
else:
    print(f'⚠️  已存在: {tool.name}')
