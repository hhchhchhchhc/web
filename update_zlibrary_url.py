import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Tool

tool = Tool.objects.get(slug='z-library永久访问指南')
tool.website_url = 'http://zlib.re'
tool.save()
print(f'Updated {tool.name} website URL to {tool.website_url}')
