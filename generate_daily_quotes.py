#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
from datetime import datetime

# 人民日报风格金句库
QUOTES = [
    {"quote": "奋斗是青春最亮丽的底色", "context": "新时代的青年，要在奋斗中释放青春激情、追逐青春理想"},
    {"quote": "幸福都是奋斗出来的", "context": "只有奋斗的人生才称得上幸福的人生"},
    {"quote": "时代是出卷人，我们是答卷人，人民是阅卷人", "context": "不忘初心，牢记使命，永远奋斗"},
    {"quote": "撸起袖子加油干", "context": "空谈误国，实干兴邦"},
    {"quote": "人民对美好生活的向往，就是我们的奋斗目标", "context": "始终把人民放在心中最高位置"},
    {"quote": "绿水青山就是金山银山", "context": "保护生态环境就是保护生产力"},
    {"quote": "打铁必须自身硬", "context": "全面从严治党永远在路上"},
    {"quote": "不驰于空想，不骛于虚声", "context": "一步一个脚印，踏踏实实干好工作"},
    {"quote": "天下之本在国，国之本在家", "context": "家庭是社会的基本细胞"},
    {"quote": "功成不必在我，功成必定有我", "context": "以钉钉子精神做实做细做好各项工作"},
    {"quote": "志不求易者成，事不避难者进", "context": "越是艰险越向前"},
    {"quote": "征途漫漫，惟有奋斗", "context": "新征程上，我们必须更加坚定信心"},
    {"quote": "江山就是人民，人民就是江山", "context": "始终同人民想在一起、干在一起"},
    {"quote": "行百里者半九十", "context": "越到紧要关头，越要坚定必胜信念"},
    {"quote": "千磨万击还坚劲，任尔东西南北风", "context": "保持战略定力，增强发展信心"},
]

def generate_article():
    # 随机选择3-5条金句
    selected_quotes = random.sample(QUOTES, random.randint(3, 5))

    today = datetime.now().strftime("%Y年%m月%d日")

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>人民日报每日金句 | {today}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            line-height: 1.8;
        }}

        .container {{
            max-width: 680px;
            margin: 0 auto;
            background: white;
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }}

        .header {{
            background: linear-gradient(135deg, #d32f2f 0%, #c62828 100%);
            color: white;
            padding: 40px 30px;
            text-align: center;
        }}

        .header h1 {{
            font-size: 28px;
            font-weight: bold;
            margin-bottom: 10px;
            letter-spacing: 2px;
        }}

        .header .date {{
            font-size: 14px;
            opacity: 0.9;
        }}

        .content {{
            padding: 30px;
        }}

        .intro {{
            text-align: center;
            color: #666;
            font-size: 15px;
            margin-bottom: 30px;
            line-height: 1.8;
        }}

        .quote-card {{
            background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
            border-radius: 12px;
            padding: 25px;
            margin-bottom: 20px;
            position: relative;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }}

        .quote-card:nth-child(even) {{
            background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        }}

        .quote-number {{
            position: absolute;
            top: -10px;
            left: 20px;
            background: #d32f2f;
            color: white;
            width: 32px;
            height: 32px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 16px;
            box-shadow: 0 2px 8px rgba(211, 47, 47, 0.4);
        }}

        .quote-text {{
            font-size: 20px;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 15px;
            padding-left: 20px;
            border-left: 4px solid #d32f2f;
            line-height: 1.6;
        }}

        .quote-context {{
            font-size: 15px;
            color: #555;
            line-height: 1.8;
            padding-left: 10px;
        }}

        .footer {{
            background: #f5f5f5;
            padding: 25px;
            text-align: center;
            color: #666;
            font-size: 14px;
        }}

        .footer .motto {{
            font-size: 16px;
            color: #d32f2f;
            font-weight: bold;
            margin-bottom: 10px;
        }}

        .divider {{
            height: 2px;
            background: linear-gradient(to right, transparent, #d32f2f, transparent);
            margin: 30px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📰 人民日报每日金句</h1>
            <div class="date">{today} 星期{['一', '二', '三', '四', '五', '六', '日'][datetime.now().weekday()]}</div>
        </div>

        <div class="content">
            <div class="intro">
                ✨ 每天一句正能量，点亮奋斗新征程 ✨<br>
                让我们一起学习人民日报的金句智慧，汲取前行的力量！
            </div>

            <div class="divider"></div>
"""

    # 添加金句卡片
    for idx, item in enumerate(selected_quotes, 1):
        html += f"""
            <div class="quote-card">
                <div class="quote-number">{idx}</div>
                <div class="quote-text">"{item['quote']}"</div>
                <div class="quote-context">💡 {item['context']}</div>
            </div>
"""

    html += """
            <div class="divider"></div>
        </div>

        <div class="footer">
            <div class="motto">🌟 不忘初心 · 砥砺前行 🌟</div>
            <div>每日金句，与您共勉</div>
            <div style="margin-top: 10px; font-size: 12px; color: #999;">
                关注我们，每天获取更多正能量
            </div>
        </div>
    </div>
</body>
</html>
"""

    return html

if __name__ == "__main__":
    article_html = generate_article()

    # 保存文件
    filename = f"daily_quotes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(article_html)

    print(f"✅ 文章已生成: {filename}")
    print(f"📝 包含 {article_html.count('quote-card')} 条金句")
