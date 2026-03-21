#!/usr/bin/env python3
import os
import django
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

# 创建分类
categories = {
    'ai_models': Category.objects.get_or_create(
        name='AI大模型平台',
        defaults={'slug': slugify('AI大模型平台', allow_unicode=True), 'description': '综合AI大模型与对话平台'}
    )[0],
    'image_video': Category.objects.get_or_create(
        name='AI图像视频',
        defaults={'slug': slugify('AI图像视频', allow_unicode=True), 'description': '图像与视频生成工具'}
    )[0],
    'coding': Category.objects.get_or_create(
        name='AI编程开发',
        defaults={'slug': slugify('AI编程开发', allow_unicode=True), 'description': '编程与开发工具'}
    )[0],
    'office': Category.objects.get_or_create(
        name='办公效率',
        defaults={'slug': slugify('办公效率', allow_unicode=True), 'description': '办公与效率工具'}
    )[0],
    'research': Category.objects.get_or_create(
        name='科研文档',
        defaults={'slug': slugify('科研文档', allow_unicode=True), 'description': '科研与文档处理工具'}
    )[0],
    'audio': Category.objects.get_or_create(
        name='AI音频',
        defaults={'slug': slugify('AI音频', allow_unicode=True), 'description': '音频与声音工具'}
    )[0],
}

print('✓ 创建分类完成')

# 一、AI大模型平台
ai_models = [
    {'name': 'DeepSeek深度求索', 'url': 'https://www.deepseek.com/', 'desc': '开源免费大模型，可本地部署，成本极低。SiliconFlow注册送2000万Tokens'},
    {'name': 'Google Gemini', 'url': 'https://gemini.google.com/', 'desc': '免费版可用，支持Imagen 3绘图，OpenRouter提供免费Gemini 2.0 Flash Thinking'},
    {'name': 'Grok 3', 'url': 'https://grok.x.ai/', 'desc': 'xAI推出，每日免费测试额度，扩大测试范围'},
    {'name': 'CTO.NEW', 'url': 'https://cto.new/', 'desc': '永久免费，提供GPT-5.2、Claude 4.5、Gemini 2.5 Pro等顶级模型'},
    {'name': 'Juchats Labs', 'url': 'https://juchats.com/', 'desc': '每天10次免费，可使用o1-preview模型'},
]

for tool_data in ai_models:
    Tool.objects.get_or_create(
        name=tool_data['name'],
        defaults={
            'slug': slugify(tool_data['name'], allow_unicode=True),
            'short_description': tool_data['desc'][:100],
            'full_description': tool_data['desc'],
            'website_url': tool_data['url'],
            'category': categories['ai_models'],
            'is_published': True,
            'is_featured': True
        }
    )
    print(f"✓ {tool_data['name']}")

print('✓ AI大模型平台添加完成')

# 二、图像与视频生成工具
image_video_tools = [
    {'name': 'Wuli.art', 'url': 'https://wuli.art/', 'desc': '完全免费无限制，集成Qwen Image、Seedream 4.5、万相2.6、可灵Q1等，支持4K生图和1080p视频'},
    {'name': '即梦AI', 'url': 'https://jimeng.jianying.com/', 'desc': '字节跳动旗下，每日签到送积分，支持图像生成、视频生成、老照片修复'},
    {'name': 'Nano Banana Pro', 'url': 'https://www.nanobanana.pro/', 'desc': '通过Google Gemini Enterprise试用免费，强大生图能力，适合手办设计、电商图'},
    {'name': '海螺AI', 'url': 'https://hailuoai.com/', 'desc': '新用户赠送积分，视频生成，支持首尾帧控制'},
    {'name': '腾讯混元3D', 'url': 'https://3d.hunyuan.tencent.com/', 'desc': '每天免费20次，照片生成3D角色、小游戏动画'},
    {'name': 'Mokker AI', 'url': 'https://mokker.ai/', 'desc': '免费使用无需魔法，电商产品主图生成、背景替换'},
    {'name': 'Recraft', 'url': 'https://www.recraft.ai/', 'desc': '注册送250张生成额度，专业AI设计，擅长矢量图和胶片感图片'},
    {'name': 'Lovart', 'url': 'https://lovart.ai/', 'desc': '注册赠送积分，邀请可获额外积分，AI设计和绘图'},
]

for tool_data in image_video_tools:
    Tool.objects.get_or_create(
        name=tool_data['name'],
        defaults={
            'slug': slugify(tool_data['name'], allow_unicode=True),
            'short_description': tool_data['desc'][:100],
            'full_description': tool_data['desc'],
            'website_url': tool_data['url'],
            'category': categories['image_video'],
            'is_published': True,
            'is_featured': True
        }
    )
    print(f"✓ {tool_data['name']}")

print('✓ 图像视频工具添加完成')

# 三、编程与开发工具
coding_tools = [
    {'name': 'Trae', 'url': 'https://trae.ai/', 'desc': '字节跳动AI IDE，国际版免费，智能编程核心开源，支持自然语言修Bug、写代码，支持Claude 3.7和GPT-4.1'},
    {'name': 'CodeFlying', 'url': 'https://codeflying.com/', 'desc': '基础版免费，文生软件平台，一键生成微信小程序、APP、网页应用，无代码基础可用'},
    {'name': '百度秒哒', 'url': 'https://miaoda.baidu.com/', 'desc': '免费使用，无代码生成完整网站或应用，自动部署服务器'},
    {'name': 'CodeBuddy IDE', 'url': 'https://codebuddy.tencent.com/', 'desc': '腾讯出品免费，自动思考和部署能力强，网页设计能力不错'},
    {'name': 'Windsurf', 'url': 'https://codeium.com/windsurf', 'desc': '限时免费活动，曾提供GPT-4.1免费使用'},
]

for tool_data in coding_tools:
    Tool.objects.get_or_create(
        name=tool_data['name'],
        defaults={
            'slug': slugify(tool_data['name'], allow_unicode=True),
            'short_description': tool_data['desc'][:100],
            'full_description': tool_data['desc'],
            'website_url': tool_data['url'],
            'category': categories['coding'],
            'is_published': True,
            'is_featured': True
        }
    )
    print(f"✓ {tool_data['name']}")

print('✓ 编程开发工具添加完成')

# 四、办公与效率工具
office_tools = [
    {'name': 'NotebookLM', 'url': 'https://notebooklm.google.com/', 'desc': 'Google出品完全免费，高效整合信息，上传PDF生成思维导图、摘要、音频概览，处理知识库问答最好用'},
    {'name': 'ChatExcel', 'url': 'https://chatexcel.com/', 'desc': '免费，对话处理Excel表格，支持数据运算、分析和图表生成'},
    {'name': 'ChatPPT', 'url': 'https://chat-ppt.com/', 'desc': '接入DeepSeek，在WPS和Office中免费，对话式生成PPT文档'},
    {'name': 'AutoGLM沉思版', 'url': 'https://chatglm.cn/', 'desc': '智谱出品完全免费，浏览器Agent，自动操作浏览器进行全网信息检索、整理，Manus的免费平替'},
    {'name': 'Whimsical', 'url': 'https://whimsical.com/', 'desc': '同一账号免费使用AI 100次，AI辅助生成思维导图、流程图'},
    {'name': 'Diagramming AI', 'url': 'https://www.diagramming.ai/', 'desc': '免费无需魔法，输入文本生成流程图、甘特图等图表'},
    {'name': 'Get笔记', 'url': 'https://www.getquicker.net/', 'desc': '免费，语音AI笔记功能完全够用，支持flomo和微信读书笔记导入'},
    {'name': '秘塔输入法', 'url': 'https://metaso.cn/', 'desc': '免费AI语音输入法，目前只有桌面端'},
]

for tool_data in office_tools:
    Tool.objects.get_or_create(
        name=tool_data['name'],
        defaults={
            'slug': slugify(tool_data['name'], allow_unicode=True),
            'short_description': tool_data['desc'][:100],
            'full_description': tool_data['desc'],
            'website_url': tool_data['url'],
            'category': categories['office'],
            'is_published': True,
            'is_featured': True
        }
    )
    print(f"✓ {tool_data['name']}")

print('✓ 办公效率工具添加完成')

# 五、科研与文档处理工具
research_tools = [
    {'name': 'Kimi Researcher', 'url': 'https://kimi.moonshot.cn/', 'desc': '内测阶段免费需申请，深度调研功能'},
    {'name': 'Felo.ai', 'url': 'https://felo.ai/', 'desc': '免费AI智能搜索引擎，支持多语言搜索和深度挖掘'},
    {'name': 'MinerU', 'url': 'https://github.com/opendatalab/MinerU', 'desc': 'OpenDataLab开源免费，高质量PDF转Markdown，支持本地部署'},
    {'name': 'Auto-Deep-Research', 'url': 'https://github.com/hkust-nlp/Auto-Deep-Research', 'desc': '港大开源免费，自动化深度调研，OpenAI Deep Research的替代方案'},
]

for tool_data in research_tools:
    Tool.objects.get_or_create(
        name=tool_data['name'],
        defaults={
            'slug': slugify(tool_data['name'], allow_unicode=True),
            'short_description': tool_data['desc'][:100],
            'full_description': tool_data['desc'],
            'website_url': tool_data['url'],
            'category': categories['research'],
            'is_published': True,
            'is_featured': True
        }
    )
    print(f"✓ {tool_data['name']}")

print('✓ 科研文档工具添加完成')

# 六、音频与声音工具
audio_tools = [
    {'name': 'Suno', 'url': 'https://suno.ai/', 'desc': '每日赠送免费积分，AI音乐生成'},
    {'name': 'RVC', 'url': 'https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI', 'desc': '开源免费，声音克隆与转换，用于AI翻唱或影视解说配音'},
]

for tool_data in audio_tools:
    Tool.objects.get_or_create(
        name=tool_data['name'],
        defaults={
            'slug': slugify(tool_data['name'], allow_unicode=True),
            'short_description': tool_data['desc'][:100],
            'full_description': tool_data['desc'],
            'website_url': tool_data['url'],
            'category': categories['audio'],
            'is_published': True,
            'is_featured': True
        }
    )
    print(f"✓ {tool_data['name']}")

print('✓ 音频工具添加完成')
print(f'\n🎉 所有工具添加完成！共添加 {len(ai_models) + len(image_video_tools) + len(coding_tools) + len(office_tools) + len(research_tools) + len(audio_tools)} 个工具')
