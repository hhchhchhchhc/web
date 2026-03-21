import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Tool

tool = Tool.objects.get(slug='z-library永久访问指南')
print(f'Name: {tool.name}')
print(f'Slug: {tool.slug}')
print(f'Website URL: {tool.website_url}')
print(f'Category: {tool.category.name}')
print(f'Published: {tool.is_published}')
