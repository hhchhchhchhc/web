#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

tools_data = [
    {
        'name': '九天·毕昇平台',
        'short_description': '中国移动AI算力平台，注册送1000-3000算力豆，提供V100显卡',
        'full_description': '九天·毕昇是中国移动推出的AI算力平台，注册即送1000-3000算力豆。提供V100显卡（32GB显存），支持Jupyter/VSCode环境，终端有root权限，适合深度学习训练。',
        'website_url': 'https://jiutian.10086.cn/',
        'category_name': '云算力平台'
    },
    {
        'name': '阿里天池实验室',
        'short_description': '阿里云提供60小时免费GPU时长，支持V100/P100/T4显卡',
        'full_description': '阿里天池实验室提供60小时免费GPU时长，配备V100/P100/T4显卡，支持Notebook在线调试。单次最长8小时，适合短期训练和竞赛项目。',
        'website_url': 'https://tianchi.aliyun.com/',
        'category_name': '云算力平台'
    },
    {
        'name': '百度AI Studio',
        'short_description': '每周免费GPU算力，Tesla V100显卡，内置丰富数据集和教程',
        'full_description': '百度AI Studio每周提供数十小时免费GPU算力，配备Tesla V100显卡，内置丰富数据集和教程。主要支持PaddlePaddle框架，适合百度生态用户。',
        'website_url': 'https://aistudio.baidu.com/',
        'category_name': '云算力平台'
    },
    {
        'name': 'OpenI启智社区',
        'short_description': '集成代码管理与算力资源，提供免费GPU实例（16GB+显存）',
        'full_description': 'OpenI启智社区集成代码管理与算力资源，提供免费GPU实例（16GB+显存），支持多种深度学习框架，适合学术研究和开源项目。',
        'website_url': 'https://openi.pcl.ac.cn/',
        'category_name': '云算力平台'
    },
    {
        'name': '腾讯云Cloud Studio',
        'short_description': '每月5万分钟免费时长，T4显卡+8核CPU+32G内存',
        'full_description': '腾讯云Cloud Studio每月提供5万分钟免费时长，配备T4显卡（16G显存）、8核CPU和32G内存，在线VSCode开发环境，适合AI应用部署。',
        'website_url': 'https://cloudstudio.net/',
        'category_name': '云算力平台'
    },
    {
        'name': 'Kaggle',
        'short_description': '每周30小时免费GPU时长，支持多种深度学习框架',
        'full_description': 'Kaggle提供每周30小时免费GPU时长，CPU内存29GB，单次训练最长12小时。支持主流深度学习框架，适合数据科学竞赛和模型训练。',
        'website_url': 'https://www.kaggle.com/',
        'category_name': '云算力平台'
    },
    {
        'name': 'Google Colab',
        'short_description': '免费GPU云端Jupyter环境，支持T4/P100/V100显卡',
        'full_description': 'Google Colab提供免费GPU云端Jupyter环境，动态分配T4/P100/V100显卡，显存15-16GB。免费版单次最长12小时，支持CUDA加速，适合快速实验和学习。',
        'website_url': 'https://colab.research.google.com/',
        'category_name': '云算力平台'
    }
]

for tool_data in tools_data:
    category_name = tool_data.pop('category_name')
    category = Category.objects.get(name=category_name)

    tool, created = Tool.objects.get_or_create(
        name=tool_data['name'],
        defaults={
            **tool_data,
            'category': category
        }
    )

    if created:
        print(f'✓ 已添加: {tool.name} → {category.name}')
    else:
        print(f'- 已存在: {tool.name}')

print('\n完成！')
