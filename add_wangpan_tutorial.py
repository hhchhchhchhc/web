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

# 添加网盘搬运副业教程
tool, created = Tool.objects.get_or_create(
    name='网盘搬运副业保姆级教程',
    defaults={
        'short_description': '零成本副业，通过网盘拉新和资料分享赚零花钱，日赚100+',
        'full_description': '''零成本网盘搬运副业保姆级教程：

【核心收益模式】
1. 拉新奖励：每邀请新用户5-50元（夸克最高12元）
2. 转存收益：用户转存资料获得分成
3. 会员分成：用户开通会员持续获得30-40%分成

【推荐平台】
• 任推邦：聚合阿里、百度等大厂网盘项目，无需押金
• 小猴云印：线上打印服务，上传资料赚佣金

【适合人群】
宝妈、大学生、职场兼职人群，0成本启动、时间地点全自由

【操作流程】
1. 注册夸克网盘和任推邦平台
2. 申请网盘推广权限
3. 准备高需求资源（教育、影视、工具类）
4. 多渠道分发（知乎、小红书、B站等）

【收益案例】
• 地推团队单日120单，收益超1300元
• 资料链接30天带来1384元收益
• 新手1-2周可稳定日赚100+

详细教程包含注册、申请、推广全流程。''',
        'website_url': 'https://dt.bd.cn',
        'category': category,
        'is_published': True,
    }
)

if created:
    print(f'✅ 已添加: {tool.name}')
else:
    print(f'⚠️  已存在: {tool.name}')
