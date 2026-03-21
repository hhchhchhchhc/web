#!/usr/bin/env python3
import os
import django
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

PREMIUM_TOOLS = [
    {
        'category': 'AI写作工具',
        'tools': [
            {'name': 'ChatGPT', 'url': 'https://chat.openai.com/', 'desc': 'OpenAI的对话式AI，擅长文本生成、研究综合和内容创意'},
            {'name': 'Jasper AI', 'url': 'https://www.jasper.ai/', 'desc': '营销专用AI写作平台，50+模板，品牌语调一致性'},
            {'name': 'Copy.ai', 'url': 'https://www.copy.ai/', 'desc': '快速生成社交媒体、广告文案和产品描述'},
            {'name': 'Writesonic', 'url': 'https://writesonic.com/', 'desc': '集成SEO、AI搜索可见性和内容创作自动化'},
            {'name': 'Grammarly', 'url': 'https://www.grammarly.com/', 'desc': '业界领先的语法检查和写作优化工具'},
            {'name': 'HubSpot AI', 'url': 'https://www.hubspot.com/', 'desc': '营销邮件、社交内容、CTA和内容创意生成'},
            {'name': 'Descript', 'url': 'https://www.descript.com/', 'desc': '将播客、访谈转换为博客文章和短视频'},
        ]
    },
    {
        'category': 'AI视频工具',
        'tools': [
            {'name': 'Synthesia', 'url': 'https://www.synthesia.io/', 'desc': '生成交互式AI视频和逼真AI头像，支持120+语言'},
            {'name': 'HeyGen', 'url': 'https://www.heygen.com/', 'desc': '生成引人入胜的AI视频'},
            {'name': 'Google Veo', 'url': 'https://deepmind.google/technologies/veo/', 'desc': '从文本或图像生成高质量电影级短视频'},
            {'name': 'Lumen5', 'url': 'https://lumen5.com/', 'desc': '将网络研讨会或播客转换为短视频和社交帖子'},
        ]
    },
    {
        'category': 'AI编程工具',
        'tools': [
            {'name': 'GitHub Copilot', 'url': 'https://github.com/features/copilot', 'desc': '行业领先的AI编程助手，支持多模型选择'},
            {'name': 'Cursor', 'url': 'https://cursor.sh/', 'desc': 'AI原生IDE，深度理解整个代码库，擅长大规模重构'},
            {'name': 'Windsurf', 'url': 'https://codeium.com/windsurf', 'desc': '强大的免费AI编程助手，支持多语言和IDE集成'},
            {'name': 'Claude Code', 'url': 'https://www.anthropic.com/', 'desc': '终端优先的AI代理，擅长复杂多步骤任务'},
            {'name': 'Tabnine', 'url': 'https://www.tabnine.com/', 'desc': '注重隐私和安全，支持本地部署和私有代码库训练'},
            {'name': 'Amazon Q Developer', 'url': 'https://aws.amazon.com/q/developer/', 'desc': 'AWS开发者专用，生成安全的云就绪代码'},
            {'name': 'Sourcegraph Cody', 'url': 'https://sourcegraph.com/cody', 'desc': '深度理解大型复杂代码库，适合monorepo'},
            {'name': 'Qodo', 'url': 'https://www.qodo.ai/', 'desc': '生成有意义的测试，提高代码质量，主动识别bug'},
            {'name': 'Replit Ghostwriter', 'url': 'https://replit.com/', 'desc': '云端协作IDE的实时AI编程助手'},
        ]
    },
    {
        'category': 'AI音频工具',
        'tools': [
            {'name': 'ElevenLabs', 'url': 'https://elevenlabs.io/', 'desc': '高质量自然语音生成，听起来像真人'},
            {'name': 'Otter.ai', 'url': 'https://otter.ai/', 'desc': '会议转录和摘要工具'},
        ]
    },
    {
        'category': 'AI搜索引擎',
        'tools': [
            {'name': 'Perplexity', 'url': 'https://www.perplexity.ai/', 'desc': 'AI驱动的研究工具，帮助工程师深入了解问题'},
            {'name': 'Gemini', 'url': 'https://gemini.google.com/', 'desc': 'Google多模态AI助手，擅长搜索、写作、编码'},
        ]
    },
    {
        'category': 'AI办公工具',
        'tools': [
            {'name': 'Notion AI', 'url': 'https://www.notion.so/product/ai', 'desc': '将笔记转换为任务，总结更新，自动化文档'},
            {'name': 'ClickUp', 'url': 'https://clickup.com/', 'desc': 'AI简化生产力，总结笔记，自动化任务'},
            {'name': 'Zapier', 'url': 'https://zapier.com/', 'desc': '连接数千个应用，自动化重复任务'},
            {'name': 'monday.com', 'url': 'https://monday.com/', 'desc': 'AI工作流自动化、资源规划和风险预警'},
        ]
    },
    {
        'category': 'AI设计工具',
        'tools': [
            {'name': 'Figma AI', 'url': 'https://www.figma.com/', 'desc': '生成UI布局，将提示转换为交互式原型'},
            {'name': 'Surfer AI', 'url': 'https://surferseo.com/', 'desc': '创建SEO优化内容，实时优化分数'},
        ]
    },
    {
        'category': 'AI开发平台',
        'tools': [
            {'name': 'n8n', 'url': 'https://n8n.io/', 'desc': '低代码开源工作流自动化工具，构建自定义AI代理'},
            {'name': 'Vercel AI SDK', 'url': 'https://sdk.vercel.ai/', 'desc': '构建自定义AI代理，跨模型灵活性'},
            {'name': 'Snyk', 'url': 'https://snyk.io/', 'desc': 'AI识别漏洞，增强CI/CD管道中的代码安全'},
            {'name': 'CodeRabbit', 'url': 'https://coderabbit.ai/', 'desc': '自动化代码审查，支持MCP集成'},
        ]
    },
]

print('添加优质工具...\n')

added = 0
skipped = 0

for cat_data in PREMIUM_TOOLS:
    cat_name = cat_data['category']
    cat, _ = Category.objects.get_or_create(
        name=cat_name,
        defaults={'slug': slugify(cat_name, allow_unicode=True)}
    )

    for tool_data in cat_data['tools']:
        # 检查是否已存在
        if Tool.objects.filter(name=tool_data['name']).exists():
            skipped += 1
            continue

        slug = slugify(tool_data['name'], allow_unicode=True) or f"tool-{added}"
        counter = 1
        while Tool.objects.filter(slug=slug).exists():
            slug = f"{slugify(tool_data['name'], allow_unicode=True)}-{counter}"
            counter += 1

        Tool.objects.create(
            name=tool_data['name'],
            slug=slug,
            short_description=tool_data['desc'],
            full_description=tool_data['desc'],
            website_url=tool_data['url'],
            category=cat,
            is_published=True,
            is_featured=True
        )
        added += 1
        print(f'✓ {tool_data["name"]}')

print(f'\n完成！')
print(f'新增: {added} 个')
print(f'跳过: {skipped} 个')
