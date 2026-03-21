#!/usr/bin/env python3
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Tool

# 更新 Linux.do 工具描述
try:
    tool = Tool.objects.get(slug='linux-do')

    tool.short_description = 'AI和开发前沿技术的中文开源社区，提供免费AI模型和DeepLX翻译服务'
    tool.full_description = '''🌟 Linux.do - Where Possible Begins

🎯 核心定位：
• 成立于2024年1月17日的中文开源社区
• 专注AI和开发前沿技术交流
• 基于Discourse平台构建
• 口号："Where possible begins"
• 社区文化：真诚、友善、团结、专业

✨ 核心功能：
• **免费AI工具**：提供ChatGPT、GPT-4、Claude3.5等大模型免费访问
• **DeepLX API**：免费翻译服务，绕过DeepL官方限制
• **技术交流**：涵盖Linux、DevOps、容器化、自动化脚本等
• **知识沉淀**：精华帖和Wiki文档，形成可复用知识资产
• **项目式学习**："从做中学"文化，如"30天挑战搭建个人云"

🔧 特色服务：
• LinuxDo Scripts浏览器扩展（帖子收藏、AI总结等）
• Dify集成插件（用户认证、内容搜索、个性化推荐）
• 与GitHub、Obsidian、RSS等工具联动
• 无广告、无营销，纯粹社区体验

📊 社区规模：
• 超过30,000注册用户
• 日活IP超过7,000
• 需邀请码注册，确保社区质量

🎯 适用人群：
• AI和前沿技术爱好者
• 开发者和技术从业者
• 开源精神践行者
• 寻求高质量技术交流的人'''

    tool.save()
    print("✅ Linux.do 描述已更新！")

except Tool.DoesNotExist:
    print("❌ 未找到 Linux.do 工具记录")
