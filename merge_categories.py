import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

# 获取两个分类
zhuanqian_jiqiao = Category.objects.get(name='赚钱技巧')
fuye_zhuanqian = Category.objects.get(name='副业赚钱')

print(f'将 "{zhuanqian_jiqiao.name}" 的工具迁移到 "{fuye_zhuanqian.name}"')

# 将所有工具从"赚钱技巧"移到"副业赚钱"
tools = Tool.objects.filter(category=zhuanqian_jiqiao)
count = tools.count()
tools.update(category=fuye_zhuanqian)

print(f'✅ 已迁移 {count} 个工具')

# 删除"赚钱技巧"分类
zhuanqian_jiqiao.delete()
print(f'✅ 已删除 "{zhuanqian_jiqiao.name}" 分类')

print(f'\n合并完成！现在 "{fuye_zhuanqian.name}" 分类共有 {Tool.objects.filter(category=fuye_zhuanqian).count()} 个工具')
