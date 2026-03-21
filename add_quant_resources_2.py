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

# 添加深度学习量化路演和研报
tool, created = Tool.objects.get_or_create(
    name='深度学习量化路演和研报',
    defaults={
        'short_description': '深度学习在量化交易中的应用路演和研究报告',
        'full_description': '''深度学习量化路演和研报资源包：

【资源内容】
深度学习技术在量化交易领域的路演材料和研究报告，系统介绍深度学习模型在金融市场预测和交易策略中的应用。

【适合人群】
• 量化交易研究员
• 深度学习工程师
• 金融科技从业者
• 算法交易开发者
• 投资机构研究人员

【资源价值】
包含深度学习量化策略的实战案例、模型设计思路、回测结果分析等专业内容，帮助理解深度学习如何提升量化交易效果。

百度网盘提取码: d32n''',
        'website_url': 'https://pan.baidu.com/s/1mvG7DmOzMymGMhb1g-yh8w?pwd=d32n',
        'category': category,
        'is_published': True,
    }
)

if created:
    print(f'✅ 已添加: {tool.name}')
else:
    print(f'⚠️  已存在: {tool.name}')
