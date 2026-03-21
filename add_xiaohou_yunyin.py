import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

# 获取副业赚钱分类
category, _ = Category.objects.get_or_create(
    name='副业赚钱',
    defaults={'description': '正规无门槛的副业和赚钱方法', 'order': 15}
)

# 添加小猴云印推广
tool, created = Tool.objects.get_or_create(
    name='小猴云印推广',
    defaults={
        'short_description': '靠资料打印实现"睡后收益"的零成本玩法',
        'full_description': '''小猴云印推广——零成本睡后收益玩法：

【平台介绍】
小猴云印是线上打印服务平台，用户可以在线打印文档资料并快递到家。

【收益模式】
上传有价值的资料（学习资料、考试真题、工作模板等），用户打印你的资料时获得佣金分成，实现睡后收益。

<thinking>
The user wants me to add the 小猴云印 content as a separate tool. I'm creating a script that adds it to the "副业赚钱" category. I need to include the key information about how it works as a passive income method through document printing.

Let me continue with the full description covering the operation steps and benefits.
</thinking>

【操作流程】
1. 注册小猴云印账号
2. 上传高需求资料（教育类、职场类、考试类）
3. 设置合理价格
4. 分享资料链接到各平台
5. 用户打印即可获得收益

【适合资料类型】
• 学习资料：课程笔记、知识总结
• 考试真题：各类考试题库
• 工作模板：简历模板、PPT模板、合同模板
• 生活实用：菜谱、手工教程

【收益特点】
• 零成本启动，无需囤货
• 一次上传，持续收益
• 自动化运营，真正的睡后收入
• 适合长期积累

【推广渠道】
知乎、小红书、豆瓣、百度贴吧、微信群等需求场景。''',
        'website_url': 'https://www.xiaohouyunyin.com',
        'category': category,
        'is_published': True,
    }
)

if created:
    print(f'✅ 已添加: {tool.name}')
else:
    print(f'⚠️  已存在: {tool.name}')
