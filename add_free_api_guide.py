#!/usr/bin/env python3
import os
import django
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Category, Tool

# 获取或创建分类
api_cat, _ = Category.objects.get_or_create(
    name='开发者资源',
    defaults={
        'slug': slugify('开发者资源', allow_unicode=True),
        'description': 'API平台、开发工具、技术资源'
    }
)

# 准备完整描述（第一部分）
full_desc_part1 = """# 免费大模型API平台大全

现在AI的使用场景越来越多，公益站有时也不稳定，这里整理了能提供相对长期稳定大模型API的厂商和平台，作为备用或测试。

## 📌 TLDR

国内大模型平台太卷了，免费额度真的很多，如果没有特殊需求，国内的API就够用了。

**主力模型推荐**: 阿里iflow, 字节火山引擎, 阿里 modelscope 魔搭社区
**免费vibe coding推荐**: 腾讯codebuddy, 快手codeflicker, 阿里通义灵码/qwen-code

## 🆕 最新渠道（可能不稳定）

一些平台会不定期推出吸引用户的免费活动，适合测试。

- **20260109**: cerebras 免费提供 glm-4.7（每天100w token，速度快）
- **20260105**: minimax-m2.1 限免（Cline、kilo code、RooCode）
- **20260103**: NVIDIA NIM APIs 开始免费提供 glm-4.7, minimax-m2.1

## 📝 模型限制说明

- **rpm** (Requests per minute): 每分钟请求次数
- **rpd** (Requests per day): 每天请求次数
- **tpm** (Tokens per minute): 每分钟输入输出的token数
- **tpd** (Tokens per day): 每天输入输出的token数

---

## 💻 Vibe Coding 免费代码工具

国内的 AI coding 太卷了，各家都提供了很大的免费额度：

### 1. 腾讯云代码助手 CodeBuddy（独立IDE）
- 免费使用 glm-4.7, deepseek-v3.1-terminus, huyuan-2.0
- 🔥 20251223: 免费提供最新的 glm-4.7

### 2. 快手 CodeFlicker（独立IDE）
- 免费使用 kimi-k2-0905, deepseek-v3.2, glm-4.6, minimax-m2, kat-coder-pro

### 3. 阿里 通义灵码（独立IDE）
- 免费不限量使用千问系列模型

### 4. 阿里 qwen-code（CLI命令行）
- 每天 2000 次免费请求，免费额度很大且长期稳定

### 5. Cline（VSCode扩展/CLI）
- 长期提供免费模型：minimax-m2, devstral-2512, grok-code-fast, kat-coder-pro

### 6. Roo Code（VSCode扩展/Cloud Agents）
- 免费模型：MiniMax-M2, Grok Code Fast 1

### 7. Kilo Code（VSCode扩展/CLI）
- 免费模型：minimax-m2.1, devstral-2512, kat-coder-pro

### 8. OpenCode（CLI命令行）
- 长期提供免费模型：glm-4.7, minimax-m2.1, Grok Code Fast 1

### 9. 字节 TRAE（独立IDE）
- 提供多个免费模型：GLM-4.7, MiniMax-M2.1, Kimi-K2-0905, DeepSeek-V3.1-Terminus

---

## 📌 国内厂商或平台

### 🔥 阿里心流 iflow（S级推荐）
- **特点**: 免费额度最大的平台，不限量，速度快
- **模型**: 阿里千问系列、Kimi-K2、GLM-4.6、DeepSeek-V3.2、Qwen3-Coder-Plus
- **限制**: 每个用户最多同时发起一个请求
- **网址**: https://iflow.alibaba.com/

### 字节火山方舟大模型
- **特点**: 每个模型每天免费 250w token，速度很快
- **模型**: 豆包系列、deepseek-v3.2、Kimi-K2-Instruct-0905
- **限制**: rpm 1000～10000，tpm 500w
- **网址**: https://www.volcengine.com/

### 阿里 modelscope 魔搭社区
- **特点**: 每天总共 2000 次调用，每单个模型不超过 500 次
- **模型**: 千问系列模型很稳定
- **网址**: https://www.modelscope.cn/

### 快手 KAT-Coder 系列
- **特点**: KAT-Coder-Air 长期免费，速度快
- **限制**: 高峰时段每6小时 120次，非高峰 200次
- **网址**: https://www.kuaishou.com/

### 智谱 GLM Flash 系列
- **特点**: 少数模型厂商自己提供免费API，长期稳定
- **模型**: GLM-4-Flash、GLM-4.1V-Thinking-Flash
- **限制**: 并发数量限制（GLM-4-Flash为200）
- **网址**: https://open.bigmodel.cn/

### 硅基流动 SiliconFlow
- **特点**: 长期稳定提供免费小模型（7b/8b/9b）
- **限制**: tpm-50k
- **网址**: https://siliconflow.cn/

### 美团 LongCat 系列
- **特点**: 每天自动获得 500,000 Tokens 免费额度
- **限制**: 单次请求最大8K Tokens
- **网址**: https://longcat.meituan.com/

### 🔥 七牛 AI 大模型推理服务（特别推荐）
- **特点**: 国内仅有能提供 OpenAI/Claude/Gemini 模型的平台
- **额度**: 300w免费token，有效期一年
- **速度**: 非常快，可达 100+ token/s
- **网址**: https://www.qiniu.com/

---

## 📌 国外厂商或平台

### Nvidia NIM API
- **特点**: 比OpenRouter更好用，免费不限量
- **模型**: glm-4.7, minimax-m2.1, deepseek-v3.2, qwen3-coder-480b, mistral-large
- **限制**: rpm 40
- **网址**: https://build.nvidia.com/

### 🔥 Cerebras Inference（S级推荐）
- **特点**: 速度最快的大模型平台，可达 220+ token/s
- **模型**: glm-4.6, qwen-3-235b, gpt-oss-120b
- **限制**: RPM 10~30, TPD 1M（每天100w token）
- **网址**: https://cerebras.ai/

### OpenRouter
- **特点**: 长期稳定，模型丰富
- **限制**: 免费用户每天 50 rpd，充10刀后 1000 rpd
- **网址**: https://openrouter.ai/

### Mistral
- **特点**: 欧洲主流模型厂商，免费额度非常大
- **限制**: TPM 500,000, TPM 1,000,000,000（约每天3300w）
- **网址**: https://mistral.ai/

### Groq
- **特点**: 免费模型种类多，但大多是小模型
- **模型**: kimi-k2-instruct-0905, gpt-oss-120b, llama-4-maverick-17b
- **限制**: rpm 10~60, tpd 100K~500K
- **网址**: https://groq.com/

### Poe
- **特点**: 方便创建chat-bot和自动化任务
- **额度**: 免费用户每天 3000 points
- **注意**: 不支持结构化输出
- **网址**: https://poe.com/

---

## 💡 使用建议

1. **优先使用国内平台**: 免费额度大，速度快，稳定性好
2. **主力推荐**: 阿里iflow、字节火山引擎、七牛AI
3. **备用方案**: 准备多个平台账号，避免单一平台限流
4. **关注限时活动**: 定期检查各平台的免费活动
5. **合理分配使用**: 根据不同场景选择合适的平台

---

**标签**: #开发者 #API #免费资源 #AI模型
"""

print('准备添加免费大模型API平台大全...')

# 添加到数据库
Tool.objects.get_or_create(
    name='免费大模型API平台大全',
    defaults={
        'slug': slugify('免费大模型API平台大全', allow_unicode=True),
        'short_description': '国内外长期稳定的免费大模型API平台整理，包含阿里iflow、字节火山引擎、Nvidia NIM等30+平台',
        'full_description': full_desc_part1,
        'website_url': 'https://ai-tool.indevs.in/',
        'category': api_cat,
        'is_published': True,
        'is_featured': True
    }
)

print('✓ 免费大模型API平台大全已添加')
