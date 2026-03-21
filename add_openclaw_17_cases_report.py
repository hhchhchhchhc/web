from tools.models import Category, Tool

category, _ = Category.objects.get_or_create(
    name='openclaw使用方法',
    defaults={'description': 'OpenClaw AI工具使用教程和实践经验'}
)

name = '【方正金工】OpenClaw赋能金融投研：17个高效应用案例详解'
short_description = (
    '方正证券研究所发布的OpenClaw深度应用报告，系统梳理金融投研中的17个高效落地场景。'
)

full_description = '''
报告来源：方正证券研究所
分析师：曹春晓（S1220522030005）

核心结论：
OpenClaw通过“语言模型认知能力 + 本地执行能力”的融合，实现从对话到执行的跨越，
在金融投研中的信息检索、自动化执行、数据接口接入、策略研究与回测等环节表现出较高效率。

报告重点（17个应用案例）包括：
1. 浏览器自动化检索热点新闻
2. 自动检索并安装热门skills
3. 邮件收发与管理自动化
4. 本地文件管理与信息检索
5. 自动化任务提醒
6. 百度百科 + AI绘本生成
7. OpenClaw + Seedance视频生成
8. 调用深度研究Agent生成专题研究
9. “麦肯锡顾问”skill完成研究与PPT制作
10. 接管浏览器完成信息检索与报告生成
11. 自动配置同花顺API并提取公告数据
12. 自动配置米筐API并提取高频数据
13. 连接Wind API（含不同部署环境对比）
14. PB-ROE经典选股策略构建
15. “杯柄”形态选股策略构建
16. 安装股票分析skills进行个股深度分析
17. 全自动因子挖掘与回测

使用价值：
- 主动投研：显著减少重复劳动，提升信息处理与报告产出效率
- 量化研究：可辅助因子研究、策略复现、组合构建与回测流程

风险提示（报告原文）：
- 历史规律未来可能失效
- 案例仅供测试，不构成投资建议
- 大模型输出存在误差与不确定性

说明：
本文为报告精要整理，完整细节请以方正证券研究所原文为准。
'''.strip()

obj, created = Tool.objects.update_or_create(
    name=name,
    defaults={
        'short_description': short_description,
        'full_description': full_description,
        'website_url': 'https://www.foundersc.com/',
        'category': category,
        'is_featured': True,
        'is_published': True,
    }
)

print(('Created' if created else 'Updated') + f': {obj.name} | slug={obj.slug} | category={obj.category.name}')
