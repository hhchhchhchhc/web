#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Tool, Category

# Get AI开发平台 category
category = Category.objects.get(id=692)

# Tool data
tool_data = {
    'name': 'Open Lovable - AI驱动的React应用构建器',
    'slug': 'open-lovable-react-builder',
    'short_description': '开源的AI驱动React应用构建器，通过聊天界面快速构建Web应用',
    'full_description': '''Open Lovable是一个开源的AI驱动React应用构建器，让你通过自然语言对话快速构建Web应用。

**核心功能：**
- 🤖 AI聊天界面：通过对话方式描述你想要的应用
- 🎨 实时预览：即时查看应用构建效果
- 🔧 多LLM支持：支持OpenAI、Anthropic Claude、Groq等多个AI模型
- 🌐 网页抓取：集成Firecrawl，可以从现有网站学习设计
- 💾 本地优先：所有数据存储在本地，保护隐私
- 🚀 快速部署：一键部署到生产环境

**技术栈：**
- 前端：React + TypeScript + Vite
- 后端：Python + FastAPI
- AI集成：支持多个LLM提供商
- 网页抓取：Firecrawl API

**适用场景：**
- 快速原型开发
- 学习React开发
- AI辅助编程
- 低代码开发

**开源免费：**完全开源，可自行部署，支持本地运行。''',
    'website_url': 'https://github.com/firecrawl/open-lovable',
    'category': category,
    'is_featured': False,
}

# Check if already exists
if Tool.objects.filter(slug=tool_data['slug']).exists():
    print(f"工具 '{tool_data['name']}' 已存在，跳过")
else:
    tool = Tool.objects.create(**tool_data)
    print(f"✅ 成功添加工具: {tool.name}")
    print(f"   分类: {category.name}")
    print(f"   网址: {tool.website_url}")
