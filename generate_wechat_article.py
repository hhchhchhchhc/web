#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

# 获取所有分类和工具
categories = Category.objects.all().order_by('order', 'name')

html_content = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>全民效率神器 - AI工具大全</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
            line-height: 1.8;
            color: #333;
            background: #f5f5f5;
            padding: 20px 16px;
        }

        .container {
            max-width: 750px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        }

        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px 24px;
            text-align: center;
        }

        .header h1 {
            font-size: 28px;
            font-weight: bold;
            margin-bottom: 12px;
        }

        .header p {
            font-size: 15px;
            opacity: 0.95;
        }

        .content {
            padding: 24px;
        }

        .category {
            margin-bottom: 40px;
        }

        .category:last-child {
            margin-bottom: 0;
        }

        .category-title {
            font-size: 22px;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 20px;
            padding-bottom: 12px;
            border-bottom: 3px solid #667eea;
            display: flex;
            align-items: center;
        }

        .category-title::before {
            content: "📌";
            margin-right: 8px;
        }

        .tool-card {
            background: #fafafa;
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 16px;
            border-left: 4px solid #667eea;
        }

        .tool-name {
            font-size: 18px;
            font-weight: bold;
            color: #333;
            margin-bottom: 8px;
        }

        .tool-desc {
            font-size: 14px;
            color: #666;
            line-height: 1.6;
        }

        .tool-link {
            display: inline-block;
            margin-top: 8px;
            color: #667eea;
            font-size: 13px;
            text-decoration: none;
        }

        .footer {
            background: #f8f9fa;
            padding: 24px;
            text-align: center;
            color: #666;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 全民效率神器</h1>
            <p>精选AI工具大全 · 提升效率从这里开始</p>
        </div>
        <div class="content">
'''

# 遍历所有分类和工具
for category in categories:
    tools = Tool.objects.filter(category=category).order_by('-created_at')

    if tools.exists():
        html_content += f'''
            <div class="category">
                <div class="category-title">{category.name}</div>
'''

        for tool in tools:
            html_content += f'''
                <div class="tool-card">
                    <div class="tool-name">{tool.name}</div>
                    <div class="tool-desc">{tool.short_description}</div>
                    <a href="{tool.website_url}" class="tool-link">🔗 访问工具</a>
                </div>
'''

        html_content += '''
            </div>
'''

html_content += '''
        </div>
        <div class="footer">
            <p>💡 更多AI工具持续更新中</p>
            <p>访问 ai-tool.indevs.in 获取完整工具列表</p>
        </div>
    </div>
</body>
</html>
'''

# 保存HTML文件
output_file = 'wechat_article_all_tools.html'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f'✓ 公众号文章已生成: {output_file}')
print(f'✓ 共包含 {categories.count()} 个分类')
print(f'✓ 共包含 {Tool.objects.count()} 个工具')
