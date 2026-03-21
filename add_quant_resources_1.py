import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

# 获取网盘资源分类
category, _ = Category.objects.get_or_create(
    name='网盘资源',
    defaults={'description': '优质网盘资源和资料分享', 'order': 16}
)

# 添加人工智能量化交易研报
tool1, created1 = Tool.objects.get_or_create(
    name='人工智能量化交易研报',
    defaults={
        'short_description': 'AI量化交易研究报告合集，深度解析人工智能在量化交易中的应用',
        'full_description': '''人工智能量化交易研报资源包：

【资源内容】
专业的AI量化交易研究报告合集，涵盖人工智能技术在量化交易领域的最新应用和研究成果。

【适合人群】
• 量化交易从业者
• 金融科技研究人员
• AI算法工程师
• 投资策略研究员
• 金融学习者

【资源价值】
深度解析AI技术如何赋能量化交易，包括机器学习模型、深度学习算法在交易策略中的实际应用案例和研究分析。

百度网盘提取码: v2nu''',
        'website_url': 'https://pan.baidu.com/s/1OifV3QIiTM_Oi8daiGFNpA?pwd=v2nu',
        'category': category,
        'is_published': True,
    }
)

if created1:
    print(f'✅ 已添加: {tool1.name}')
else:
    print(f'⚠️  已存在: {tool1.name}')
