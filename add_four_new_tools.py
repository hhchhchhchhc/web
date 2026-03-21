#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

# 1. Google Gemini 2.5 Pro免费试用
free_model_category = Category.objects.get(name='免费用最高级大模型')
gemini_pro_data = {
    'name': 'Google Gemini 2.5 Pro - 免费200万Token',
    'short_description': '免费试用Gemini 2.5 Pro，最大200万token上下文',
    'full_description': '''**平台特色：**
Google Gemini 2.5 Pro 提供免费试用，拥有超大上下文窗口。

**核心优势：**
- 最大200万token上下文
- 上下文长度足够上传整部网文小说
- Google最新Pro级模型

**使用方式：**
访问官网即可免费试用

**适用场景：**
- 长文本处理
- 小说创作和分析
- 大规模文档处理
- 代码库分析''',
    'website_url': 'https://deepmind.google/technologies/gemini/pro/',
    'category': free_model_category
}

tool1, created1 = Tool.objects.get_or_create(
    name=gemini_pro_data['name'],
    defaults=gemini_pro_data
)
print(f'{"✓ 已添加" if created1 else "- 已存在"}: {tool1.name}')

# 2. AI漫画生成变现法
money_category = Category.objects.get(name='赚钱技巧')
comic_data = {
    'name': 'AI小说转漫画变现法',
    'short_description': '一键生成漫画，撸百家号收益月入3000+，免费软件和教程',
    'full_description': '''**变现方式：**
使用AI全自动漫画生成脚本，将小说转换为漫画图片，发布到百家号获取收益。

**收益数据：**
月入3000+

**制作工具：**
- Stable Diffusion
- AI全自动漫画生成脚本插件
- 免费软件和使用教程

**操作流程：**
1. 准备小说文本内容
2. 使用AI脚本一键生成漫画图片
3. 发布到百家号平台
4. 获取平台流量收益

**教程资源：**
B站有完整的免费教程和软件分享

**适用场景：**
- 动漫解说
- 小说漫画化
- 百家号内容创作''',
    'website_url': 'https://b23.tv/brOhkXw',
    'category': money_category
}

tool2, created2 = Tool.objects.get_or_create(
    name=comic_data['name'],
    defaults=comic_data
)
print(f'{"✓ 已添加" if created2 else "- 已存在"}: {tool2.name}')

# 3. 哪吒2电影票引流方法
nezha_data = {
    'name': '哪吒2电影票引流变现法',
    'short_description': '借势哪吒2票房热度，凭电影票根免费送PPT引流，双赢模式',
    'full_description': '''**引流策略：**
借助哪吒2冲击全球票房的热度，通过电影票根活动进行精准引流。

**操作方法：**
1. 发布哪吒2相关内容
2. 文案示例："助力【哪吒2】，全力冲击全球票房榜，2.21起凭电影票根，免费获得哪吒开学PPT一套"
3. 用户凭电影票根领取免费PPT
4. 引流到私域进行后续转化

**优势特点：**
- 双赢模式：帮助电影宣传，自己获得精准流量
- 目标用户精准：观影用户消费能力强
- 成本低：PPT制作成本几乎为零
- 热度高：借势热门电影话题

**变现方式：**
- 引流到私域后续转化
- 售卖其他相关产品
- 建立粉丝社群

**关键要点：**
- 选择热门电影进行借势
- 赠品要有吸引力且成本低
- 及时跟进热点''',
    'website_url': 'http://ai-tool.indevs.in/',
    'category': money_category
}

tool3, created3 = Tool.objects.get_or_create(
    name=nezha_data['name'],
    defaults=nezha_data
)
print(f'{"✓ 已添加" if created3 else "- 已存在"}: {tool3.name}')

# 4. 卖DeepSeek资料淘宝开店
deepseek_data = {
    'name': '淘宝卖DeepSeek资料变现法',
    'short_description': '淘宝开店卖DeepSeek资料，随便就出单，附完整开店流程',
    'full_description': '''**变现方式：**
在淘宝开店售卖DeepSeek相关资料，操作简单容易出单。

**淘宝开店流程：**
1. 账号注册与认证：
   - 淘宝->设置->商家入驻->淘宝开店
   - 选择个人店铺
   - 完成支付宝实名认证（需身份证正反面+人脸识别）

2. 发布商品：
   - 下载卡牛app
   - 登录淘宝账号后点击"管理商品"
   - 点击"发布商品"
   - 图片参考其他卖家的优质图片
   - 标题：使用PPT名称或资料名称
   - 类目：商务/设计服务/设计素材/源文件
   - 直接上架

**产品示例：**
清华版DeepSeek资料、教程、PPT等

**关键要点：**
- 选择热门AI工具相关资料
- 参考同行优质商品页面
- 定价合理（通常9.9-29.9元）
- 及时更新热门资料''',
    'website_url': 'https://articles.zsxq.com/id_1bcuf9nz8u87.html',
    'category': money_category
}

tool4, created4 = Tool.objects.get_or_create(
    name=deepseek_data['name'],
    defaults=deepseek_data
)
print(f'{"✓ 已添加" if created4 else "- 已存在"}: {tool4.name}')

print('\n四个工具添加完成！')
