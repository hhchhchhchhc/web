#!/usr/bin/env python3
import os
import django
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

# 创建推广分类
promo_cat, _ = Category.objects.get_or_create(
    name='🎁 限时福利',
    defaults={
        'slug': 'limited-time-benefits',
        'description': '知识星球会员专属福利'
    }
)

promo_content = """
## 🎁 加入「财富自由之路」知识星球获取超值福利

**入群福利（星球票价199元）：**
- 一年2核2G VPS服务器（价值200-800元）
- 永久免费下载知网、万方、维普等学术论文
- 无限使用Claude Opus 4.6的多种方法

**联系方式：** 微信 a13479004101 或 dreamsjtuai

**单独购买：** 2核2G VPS 100元/年

---

### 📚 核心技术资源与源码
- **DecompGRU深度学习量化模型**：端到端时序+截面模型源码
- **聚宽9大策略源码** + 600+优质量化策略
- **Meme币交易策略**构建源码（价值数千元）
- **Crypto高频训练营**代码（价值4.425万元以上）

### 📊 数据与API服务
- **Tardis数据免费代下**：合约+现货数据（单次限2T）
- **Tushare Pro API**高级版访问权限（原购入价8500元）
- **Google Pro账号**（Gemini Pro）
- **Claude Opus 4.6**无限使用（antigravity2api反代）

### 💻 硬件与服务器福利
- 2月7日后加入送一年2核2G VPS（价值200-800元）
- 单独购买100元/年

### 📈 券商开户福利
**国企券商客户经理：** lsrhuarui（备注：好运莲莲渠道）

**开户福利：**
- 更低佣金 + QMT/PTrade技术支持
- 量化专业讨论群 + 软件资料
- 入金10万送QMT软件

**额外奖励（开户+3个月内入金10万）：**
- 一年谷歌Pro共享账号
- 一个月免费88核16GB内存120GB硬盘Windows云电脑
- Tushare Pro API
- 2399元期权知识星球全部内容（年化200%回撤18%策略）

### 💰 Tardis API数据服务
**当前档位：** Solo 1200美元/月（年付14400美元）
- 现货、期货、期权数据全覆盖
- 代下载：249元/T，单次最低99元
- **联系微信：** a13479004101

### 🌟 致富证券开户（美港股）
**总价值HK$8,800奖励：**
1. 开户送HK$200现金券+交易券
2. 入金最高返HK$1,300 + NVIDIA股票
3. 转仓最高回赠HK$7,000
4. 推荐好友每人得HK$300（上不封顶）

**邀请码：** XC6774
**二维码：** https://image2url.com/r2/default/images/1770021823559-f8b6c7cb-d63d-4b01-9ead-48455da15c08.png

**入金要求：** 开户7天内入金1万港币等值

**致富证券APP下载：**
链接: https://pan.baidu.com/s/1gpI4JSYY6MwZqP8Ywor9Tw?pwd=hmec
提取码: hmec

---

**知识星球链接：** https://t.zsxq.com/Fed8e
**联系微信：** a13479004101 / dreamsjtuai
"""

# 删除旧的推广工具（如果存在）
Tool.objects.filter(name__contains='知识星球').delete()
Tool.objects.filter(name__contains='限时福利').delete()

# 创建新的推广工具
Tool.objects.create(
    name='🎁 知识星球限时福利 - 免费VPS+学术论文+Opus 4.6',
    slug='knowledge-planet-benefits',
    short_description='加入知识星球获取：免费VPS、学术论文下载、Opus 4.6无限用、量化策略源码、Tardis数据等超值福利',
    full_description=promo_content,
    website_url='https://t.zsxq.com/Fed8e',
    category=promo_cat,
    is_published=True,
    is_featured=True
)

print('✓ 创建推广内容')
print('✓ 分类：🎁 限时福利')
print('✓ 已标记为精选（is_featured=True）')
print('\n推广内容将在网站显眼位置展示')
