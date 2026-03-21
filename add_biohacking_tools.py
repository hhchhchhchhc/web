import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

# 创建生物骇客分类
category, created = Category.objects.get_or_create(
    name='生物骇客',
    defaults={
        'description': '通过科学方法优化身体和大脑性能，包括饮食、运动、睡眠监测等',
        'order': 10
    }
)

tools_data = [
    {
        'name': 'Oura Ring',
        'short_description': '智能戒指，追踪睡眠质量、HRV心率变异性和身体恢复状态',
        'full_description': '''Oura Ring是一款智能戒指，可以精确追踪：
- 睡眠结构（深度睡眠/REM睡眠）
- 心率变异性（HRV）- 身体恢复的关键指标
- 体温变化
- 活动量和卡路里消耗

数据驱动的健康优化，帮助你了解酒精、压力、运动对身体的真实影响。''',
        'website_url': 'https://ouraring.com',
    },
    {
        'name': 'Zero - 间歇性禁食追踪',
        'short_description': '追踪间歇性禁食，提升BDNF脑源性神经营养因子',
        'full_description': '''Zero是最受欢迎的间歇性禁食追踪应用：
- 多种禁食方案（16:8、18:6、OMAD等）
- 追踪禁食时长和历史记录
- 科学研究支持的健康益处
- 提升BDNF，增强细胞自噬

间歇性禁食是最简单有效的生物骇客方法之一。''',
        'website_url': 'https://www.zerofasting.com',
    },
    {
        'name': 'Cronometer',
        'short_description': '精确的营养追踪工具，优化饮食避免精制糖和反式脂肪',
        'full_description': '''Cronometer是专业级营养追踪工具：
- 追踪微量营养素（维生素、矿物质）
- 识别营养缺口
- 避免精制糖、反式脂肪等有害成分
- 增加抗炎食物（深海鱼、彩色蔬菜、莓果）

数据驱动的饮食优化，让你真正了解吃进去的每一口食物。''',
        'website_url': 'https://cronometer.com',
    },
    {
        'name': 'Headspace',
        'short_description': '冥想和正念训练应用，压力管理的核心工具',
        'full_description': '''Headspace是全球领先的冥想应用：
- 引导式冥想课程
- 压力管理和焦虑缓解
- 改善睡眠质量
- 提升专注力

压力管理是生物骇客四大支柱之一，冥想是最有效的方法。''',
        'website_url': 'https://www.headspace.com',
    },
    {
        'name': 'Examine.com',
        'short_description': '基于科学研究的补充剂数据库，避免"聪明药"陷阱',
        'full_description': '''Examine.com提供独立、科学的补充剂信息：
- 超过600种补充剂的研究综述
- 基于临床研究的效果评估
- 避免营销炒作和"聪明药"陷阱
- 靶向补充剂推荐（Omega-3、苏糖酸镁等）

在尝试任何补充剂前，先查询科学证据。''',
        'website_url': 'https://examine.com',
    },
    {
        'name': 'Whoop',
        'short_description': '专业运动员使用的恢复追踪器，监测HRV和睡眠',
        'full_description': '''Whoop是专业级身体恢复追踪器：
- 24/7心率和HRV监测
- 睡眠质量分析
- 运动负荷和恢复建议
- 压力和疲劳评估

数据驱动的训练优化，避免过度训练和受伤。''',
        'website_url': 'https://www.whoop.com',
    },
]

for tool_data in tools_data:
    tool, created = Tool.objects.get_or_create(
        name=tool_data['name'],
        defaults={
            **tool_data,
            'category': category,
            'is_published': True,
        }
    )
    if created:
        print(f'✅ 已添加: {tool.name}')
    else:
        print(f'⚠️  已存在: {tool.name}')

print(f'\n✅ 完成！已添加生物骇客分类和{len(tools_data)}个工具')
