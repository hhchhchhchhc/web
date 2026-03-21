import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

# 创建浏览器插件分类
category, _ = Category.objects.get_or_create(
    name='浏览器插件',
    defaults={'description': '提升浏览器使用体验的扩展插件', 'order': 8}
)

# 添加Cosmos Enhanced
tool, created = Tool.objects.get_or_create(
    name='Cosmos Enhanced',
    defaults={
        'short_description': '增强小宇宙播客网页端体验，支持下载、搜索和1-16倍速播放',
        'full_description': '''Cosmos Enhanced是小宇宙播客网页端增强插件：
- 下载功能：单集音频、封面原图、播客封面、主播头像
- 搜索增强：在ListenNotes搜索播客和单集
- 播放器增强：1-16倍速播放控制
- 提升播客收听体验
- Chrome浏览器扩展

让小宇宙网页端更好用。''',
        'website_url': 'https://chromewebstore.google.com/detail/cosmos-enhanced/bgjffbeeolcikmcpliaekbgdkflchakg',
        'category': category,
        'is_published': True,
    }
)

if created:
    print(f'✅ 已添加: {tool.name}')
else:
    print(f'⚠️  已存在: {tool.name}')
