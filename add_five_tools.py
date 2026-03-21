#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

# 1. ASMR插画+白噪音变现法
money_category = Category.objects.get(name='赚钱技巧')
asmr_data = {
    'name': 'ASMR插画+白噪音变现法',
    'short_description': '制作动态插画配白噪音视频，受众广粘性强，可挂疗愈周边产品变现',
    'full_description': '''**市场背景：**
现在失眠的人很多，ASMR内容很火，这个赛道可以做插画+白噪音内容。

**内容制作：**
1. 动态插画场景：
   - 窗外雪景
   - 窗外暴雨
   - 其他疗愈场景
2. 视频动画效果
3. 配上14分半钟左右白噪音：
   - 舒缓的纯音乐
   - ASMR音乐
   - 雨声等自然声音

**制作工具：**
- 音乐制作：使用Suno AI音乐创作平台（https://suno.qihuiguan.cn/home/#/）
- 不需要魔法，有免费额度

**受众特点：**
- 受众群体广
- 用户粘性强
- 长期观看需求

**变现方式：**
- 挂疗愈周边产品
- 疗愈音乐售卖
- 午休抱枕等周边

**关键要点：**
- 内容制作相对简单
- 持续更新保持粘性
- 选择合适的疗愈场景''',
    'website_url': 'http://ai-tool.indevs.in/',
    'category': money_category
}

tool1, created1 = Tool.objects.get_or_create(
    name=asmr_data['name'],
    defaults=asmr_data
)
print(f'{"✓ 已添加" if created1 else "- 已存在"}: {tool1.name}')

# 2. 腾讯混元3D
ai_image_category = Category.objects.get(name='AI图像工具')
hunyuan3d_data = {
    'name': '腾讯混元3D - 照片变游戏角色',
    'short_description': '一张照片变游戏角色和动画，创作小游戏，每天免费生成20次',
    'full_description': '''**平台特色：**
腾讯最新的3D生成模型，已经有人用它创作小游戏动画。

**核心功能：**
- 一张照片变游戏角色
- 生成3D模型和动画
- 创作小游戏
- 角色动画制作

**免费额度：**
每个账号每天可免费生成20次模型，0成本试用

**适用场景：**
- 游戏角色设计
- 小游戏开发
- 3D动画创作
- 虚拟形象制作''',
    'website_url': 'https://3d.hunyuan.tencent.com/',
    'category': ai_image_category
}

tool2, created2 = Tool.objects.get_or_create(
    name=hunyuan3d_data['name'],
    defaults=hunyuan3d_data
)
print(f'{"✓ 已添加" if created2 else "- 已存在"}: {tool2.name}')

# 3. 闪播侠直播工具
video_category = Category.objects.get(name='视频工具')
shanboxia_data = {
    'name': '闪播侠 - 直播间互动工具',
    'short_description': '内置起名、生成头像、壁纸等直播功能，完全免费',
    'full_description': '''**平台特色：**
闪播侠是专为直播间设计的互动工具平台，内置各种常见直播间功能。

**核心功能：**
- 宝宝起名
- 名字头像生成
- 恶搞P图
- 壁纸生成
- 其他直播互动功能

**使用方式：**
1. 选择功能（如宝宝起名）
2. 点击立即开播
3. 用直播工具抓取显示区域
4. 在控制台输入内容（如姓氏）
5. 点击生成，左侧实时显示结果

**价格：**
完全免费

**适用场景：**
- 抖音直播间互动
- 快手直播间
- 其他直播平台''',
    'website_url': 'http://www.shanboxia.com/',
    'category': video_category
}

tool3, created3 = Tool.objects.get_or_create(
    name=shanboxia_data['name'],
    defaults=shanboxia_data
)
print(f'{"✓ 已添加" if created3 else "- 已存在"}: {tool3.name}')

# 4. Whimsical AI思维导图工具
office_category = Category.objects.get(name='AI办公工具')
whimsical_data = {
    'name': 'Whimsical - AI思维导图生成器',
    'short_description': '一分钟生成高质量思维导图和图表，免费使用AI 100次',
    'full_description': '''**平台特色：**
Whimsical是一个AI辅助的可视化工具，在需要快速生成高质量图表和思维导图的场景中表现不错。

**核心功能：**
- AI生成思维导图
- 自动分层级输出相关步骤
- 快速生成高质量图表
- 团队协作功能

**使用方式：**
1. 使用谷歌账号登录
2. 输入主题（如"怎么实现财富自由"）
3. 点击星星图标【generate additional ideas】
4. 系统按话题分层级输出相关步骤
5. 在二级结构中继续点击【generate ideas】生成完整思维导图

**免费额度：**
同一账号免费使用AI 100次

**适用场景：**
- 快速头脑风暴
- 项目规划
- 知识整理
- 演示文稿准备''',
    'website_url': 'https://whimsical.com/?by=history&from=kkframenew',
    'category': office_category
}

tool4, created4 = Tool.objects.get_or_create(
    name=whimsical_data['name'],
    defaults=whimsical_data
)
print(f'{"✓ 已添加" if created4 else "- 已存在"}: {tool4.name}')

print('\n四个工具添加完成！')
