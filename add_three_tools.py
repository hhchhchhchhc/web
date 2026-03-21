#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

# CodeFlying - 文生软件平台
ai_dev_category = Category.objects.get(name='AI开发平台')
codeflying_data = {
    'name': 'CodeFlying - 国内首发文生软件平台',
    'short_description': '一键生成微信小程序、手机APP、网页应用，全程不写代码，基础版免费',
    'full_description': '''**平台特色：**
CodeFlying 是国内首发的文生软件平台，支持用中文描述直接生成完整应用。

**支持生成：**
- 微信小程序
- 手机APP
- 网页应用

**核心优势：**
- 全程不用写代码
- 不用搭建开发环境
- 不需要懂前后端技术
- 只需用中文描述需求

**使用示例：**
输入："我想做一个旅行日记小程序"
系统就能直接生成完整的小程序

**价格：**
基础版完全免费

**使用方式：**
访问 www.codeflying.net 注册账号即可开始使用''',
    'website_url': 'https://www.codeflying.net',
    'category': ai_dev_category
}

tool1, created1 = Tool.objects.get_or_create(
    name=codeflying_data['name'],
    defaults=codeflying_data
)
print(f'{"✓ 已添加" if created1 else "- 已存在"}: {tool1.name}')

# Same.new - 网站克隆工具
ai_coding_category = Category.objects.get(name='AI编程工具')
samenew_data = {
    'name': 'Same.new - AI网站克隆神器',
    'short_description': '估值1亿美金，一键克隆任何网站，自动生成代码并部署，新用户送5万Token',
    'full_description': '''**平台亮点：**
Same.new 是国外最近很火的AI工具，估值1亿美金，核心功能是网站克隆。

**核心功能：**
- 一键克隆任何网站
- 自动生成代码、样式、交互
- 自动修复Bug
- 自动部署上线
- 平台内预览和体验成品

**技术优势：**
把从0到1的开发直接跳过，几分钟内完整复制网站

**价格方案：**
- Pro版：每月25美元，500万Token
- 新注册账号送5万Token
- 免费额度可开发3-4个简单网站

**适用场景：**
- 快速原型开发
- 网站模仿学习
- 创意落地验证''',
    'website_url': 'https://same.new',
    'category': ai_coding_category
}

tool2, created2 = Tool.objects.get_or_create(
    name=samenew_data['name'],
    defaults=samenew_data
)
print(f'{"✓ 已添加" if created2 else "- 已存在"}: {tool2.name}')

# FLUX.1 Kontext - 人物一致性图像生成
ai_image_category = Category.objects.get(name='AI图像工具')
flux_data = {
    'name': 'FLUX.1 Kontext - 史上最强人物一致性',
    'short_description': '超精准P图和局部编辑，人物一致性极高，送200积分可生成50张图',
    'full_description': '''**模型特色：**
FLUX.1 Kontext 是史上最强的人物一致性AI图像模型。

**核心优势：**
- 人物一致性极高（连续生成、多轮编辑都保持一致）
- 超精准P图能力
- 支持局部编辑
- 精准理解想改和想保留的内容

**免费额度：**
- 每个账户送200积分
- 可免费生成50张图
- 支持国内邮箱注册，非常方便

**适用场景：**
- 角色设计和迭代
- 连续故事创作
- 精细图像编辑
- 人物形象保持''',
    'website_url': 'https://playground.bfl.ai/',
    'category': ai_image_category
}

tool3, created3 = Tool.objects.get_or_create(
    name=flux_data['name'],
    defaults=flux_data
)
print(f'{"✓ 已添加" if created3 else "- 已存在"}: {tool3.name}')

print('\n三个工具添加完成！')
