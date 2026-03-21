#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tools.models import Tool

new_description = """Anthropic「Claude Cowork」最强免费替代品：全面调研（2026-02）

结论先行：如果你要的是"像 Cowork 一样把任务交给一个能动手改文件、跑脚本、自动化浏览器的 AI 同事"，且希望"软件本身免费 + 可做到接近 0 成本运行"，目前最接近 Cowork 体验、综合能力最强的路线是：

Open Interpreter（开源） + 本地模型（Ollama / LM Studio 等） +（可选）browser-use 做更强的网页自动化。

这一套在"文件/脚本执行 + 多步任务 + 人类确认 + 可本地部署"维度上与 Cowork 高度同构；差距主要在"成品级桌面 UI、企业治理能力、官方模板化技能/插件生态整合度"。

1. 你说的 Cowork 是什么？（确认指代）

Anthropic 在 2026 年 1 月发布了 Cowork（研究预览），定位为"把 Claude Code 的 agentic 执行能力带到桌面端、给非开发者用"。官方描述与产品页核心点包括：

• 本地文件访问：给 Claude 选择一个文件夹后，它可以读取/编辑/创建文件（如整理下载目录、把截图变成表格、从散乱笔记生成报告）。
• 多步任务与更强自主性：你描述目标，它拆解步骤执行，并在关键操作前征求确认。
• 与工具/连接器结合：支持 Connectors（基于 MCP 生态）、与浏览器能力结合（Claude in Chrome），以及插件（Plugins）把技能/连接器/子代理/命令打包。
• 安全边界：官方强调 Cowork 在隔离的 VM 环境运行，你可控制可见文件夹/网络 allowlist，且重大动作前会询问。

2. 替代品要"最强且免费"，需要先定义"免费"的边界

在 AI agent 领域，"免费"通常有两种：
• 软件/框架免费（开源或免费使用）：但模型调用可能要钱（OpenAI/Anthropic/Google 等计费）。
• 端到端几乎 0 成本：需要本地模型推理（Ollama / LM Studio / llama.cpp 等）+ 本地执行环境；代价从现金变成算力与时间。

3. Cowork 的能力拆解（用于对标）

从官方资料可把 Cowork 能力拆成 6 个模块：
• 本地工作区权限模型：选择文件夹 → 读/写/改/删（关键动作前确认）
• 执行工具链：能跑脚本/命令、调用系统工具（转换、压缩、抽取数据等）
• 文档/表格/幻灯片"技能"：对 docx/xlsx/pptx/pdf 的更可靠处理（官方称 Skills）
• 网页自动化：配合浏览器扩展完成检索、表单填写、抓取信息等
• 连接器生态（MCP）：把外部应用/数据库/工具变成可调用的"工具"
• 更高级的可复用封装：插件（Plugins）把技能/连接器/子代理/命令打包成岗位专家

4. 候选"免费替代品"清单（按与 Cowork 相似度分层）

A. 最接近 Cowork 的"能动手干活"路线（推荐优先）

1) Open Interpreter（开源，终端/程序化使用为主）
• 项目：https://github.com/OpenInterpreter/open-interpreter
• 核心能力：让 LLM 在本地执行 Python/JavaScript/Shell 等代码；强调"会要求你批准后再运行代码"（更安全）；可连接本地推理服务（LM Studio / Ollama 等）实现低成本或离线。
• 对标 Cowork：✅ 本地文件操作/批处理 ✅ 多步任务 ✅ "关键动作前确认" ⚠️ 缺少成品级桌面 UI

2) browser-use（MIT 开源，专注网页自动化）
• 项目：https://github.com/browser-use/browser-use
• 核心能力："Make websites accessible for AI agents"，提供 Python 库与 CLI，可让 agent 在浏览器里点击、输入、跨页面完成任务。
• 对标 Cowork：✅ Cowork 的"Claude in Chrome"定位 ⚠️ 不负责本地文件整理/文档生成

3) OpenHands（MIT 为主的开源平台，偏"开发/工程代理"，有本地 GUI）
• 项目：https://github.com/All-Hands-AI/OpenHands
• 核心能力：提供 SDK、CLI、Local GUI；更像"可自建的 Devin/Jules 类工作台"。
• 对标 Cowork：✅ 有 GUI 与 agent 执行环境 ⚠️ 更偏软件工程/开发者场景

B. "搭建你自己的 Cowork"（编排框架 + 工具）
• LangGraph（MIT）：https://github.com/langchain-ai/langgraph
• CrewAI（开源编排框架）：https://docs.crewai.com/en/introduction
• AutoGen Studio（有 GUI 的编排/实验平台）

C. "更像一个可自建的 Claude.ai（带插件/流水线）"
• Open WebUI Pipelines：https://docs.openwebui.com/features/pipelines/

5. 结论：最强免费替代品 = 一套组合拳（而不是单一产品）

推荐冠军方案：Open Interpreter + 本地模型 +（可选）browser-use

为什么它最像 Cowork？
• Cowork 的本质是：给 AI 一个受控工作区 + 一套"能执行"的工具（脚本/命令/浏览器）+ 任务规划与人类确认。
• Open Interpreter 在 README 里明确把定位写成"自然语言接口控制电脑、执行代码"，并强调执行前确认；同时也支持对接本地推理服务。
• browser-use 则在网页自动化这块补齐 Cowork + Chrome 的能力，并且是 MIT 许可、明确"可免费使用"。

7. 落地建议：3 条"从今天就能用"的路线

路线 A（最省钱）：本地模型 + Open Interpreter
适合：你主要做本地文件、数据、报告、批处理，偶尔需要网页抓取/登录。

路线 B（最像 Cowork）：Open Interpreter + browser-use
适合：你经常要做网页上的"点击/填表/搬运数据"类任务。

路线 C（想要可视化工作台）：OpenHands Local GUI
适合：你希望接近 Devin/Jules/Cowork 的"工作台式体验"，并愿意接受更工程化的上手成本。

8. 重要风险与注意事项
• 权限最小化：只给工作区文件夹，不要给整个磁盘；分项目/分客户隔离。
• 永远保留回滚：任何批量重命名/删除/覆盖前先备份或用 Git 管理。
• 防提示注入：Cowork 官方也专门提 prompt injection 风险（尤其是网页内容会"诱导 agent"）。
• 许可证合规：Open Interpreter 是 AGPL-3.0，若你要把它"改造后对外提供网络服务/商业分发"，会触发更严格的开源合规要求。"""

tool = Tool.objects.get(name='Claude Cowork最强免费替代品全面调研')
tool.full_description = new_description
tool.save()

print(f'✓ 已更新工具描述: {tool.name}')
print(f'  描述长度: {len(new_description)} 字符')
