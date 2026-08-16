# AI Agent 知识手册（Markdown 版）

> 由 JavaGuide 的 AI 系列文章整理而成的 AI Agent / LLM / RAG 知识手册，按 **Java / Python / TypeScript** 三种语言生态提供代码示例。
> 最外层入口见仓库根目录的 [`README.md`](../README.md) 和 [`知识地图总索引.md`](../知识地图总索引.md)。

本目录下每个子目录是一套**完整且独立**的语言版本，结构完全一致：

| 版本 | 目录 | 代码技术栈 |
| --- | --- | --- |
| Java | [`java/`](java/) | Spring AI Alibaba Graph、Jackson + JSON Schema Validator |
| Python | [`python/`](python/) | LangGraph、jsonschema + dataclass、pydantic、FastAPI、asyncio |
| TypeScript | [`typescript/`](typescript/) | LangGraph.js、Zod、AsyncIterable / ReadableStream、Hono / Express |

> 三套版本正文一致；纯概念类文档内容相同，含代码的文档按各自语言生态重写。
> 原 Java 版文档完整保留在 [`java/`](java/)，并作为概念文档的 canonical 版本。

## 目录结构与学习路径

| 模块 | 主题 | 状态 |
| --- | --- | --- |
| `00-概念与术语` | 术语表、概念边界、自主性分级 | 🟢 第一迭代已补 |
| `01-LLM基础` | LLM 运行机制、结构化输出与 Function Calling | 🟢 完整 |
| `02-Agent` | Agent 核心概念、记忆系统、多智能体编排 | 🟢 第一迭代已补多智能体 |
| `03-RAG` | RAG 基础概念、向量索引与向量数据库 | 🟢 完整 |
| `04-工程实践` | Workflow/Graph/Loop、Loop Engineering、Harness Engineering、大模型网关、可观测与追踪、部署与发布 | 🟢 完整 |
| `05-评测与质量` | Agent 评测体系 | 🟢 第二迭代已补 |
| `06-安全与治理` | Agent 安全护栏清单 | 🟢 第二迭代已补 |
| `07-系统设计` | AI 应用系统设计（Prompt Demo → 生产级架构） | 🟢 完整 |
| `08-应用与案例` | 案例库、反模式、行业方案 | 🔴 待补全 |
| `09-生态与前沿` | 技术雷达、协议与趋势 | 🔴 待补全 |
| `10-面试` | 6 份面试题 + 模拟题库 | 🟢 完整 |

**推荐阅读顺序**：`00-概念与术语` → `01-LLM基础` → `02-Agent` → `03-RAG` → `04-工程实践` → `05-评测与质量` → `06-安全与治理` → `07-系统设计`，面试前刷 `10-面试`。

## 文档清单（24 篇）

| # | 文档 | 模块 | 语言化代码 |
| --- | --- | --- | --- |
| 1 | `00-概念与术语/01-Agent术语表与概念边界.md` | 概念与术语 | — |
| 2 | `00-概念与术语/02-Agent自主性分级.md` | 概念与术语 | — |
| 3 | `01-LLM基础/01-LLM运行机制.md` | LLM 基础 | — |
| 4 | `01-LLM基础/02-大模型结构化输出.md` | LLM 基础 | ✅ 工具调用分发器 |
| 5 | `02-Agent/01-Agent核心概念.md` | Agent | — |
| 6 | `02-Agent/02-Agent记忆系统.md` | Agent | — |
| 7 | `02-Agent/03-多智能体编排.md` | Agent | — |
| 8 | `03-RAG/01-RAG基础概念.md` | RAG | — |
| 9 | `03-RAG/02-RAG向量索引与向量数据库.md` | RAG | — |
| 10 | `04-工程实践/01-Workflow-Graph与Loop.md` | 工程实践 | ✅ 文章审核工作流（Graph 完整实现） |
| 11 | `04-工程实践/02-Loop工程.md` | 工程实践 | — |
| 12 | `04-工程实践/03-Harness工程.md` | 工程实践 | — |
| 13 | `04-工程实践/04-大模型网关.md` | 工程实践 | ✅ 网关接口 / 规则路由 / Token 预算 |
| 14 | `04-工程实践/05-Agent可观测与追踪.md` | 工程实践 | ✅ 三语言 Trace / 指标采集器 |
| 15 | `04-工程实践/06-Agent部署与发布.md` | 工程实践 | ✅ 三语言服务骨架 / 容器化 |
| 16 | `05-评测与质量/01-Agent评测体系.md` | 评测与质量 | ✅ 三语言评测执行器 |
| 17 | `06-安全与治理/01-Agent安全护栏清单.md` | 安全与治理 | ✅ 三语言工具风控实现 |
| 18 | `07-系统设计/01-AI应用系统设计.md` | 系统设计 | ✅ 分层架构接口定义（8 处） |
| 19 | `10-面试/01-AI-Agent面试题.md` | 面试 | — |
| 20 | `10-面试/02-RAG面试题.md` | 面试 | — |
| 21 | `10-面试/03-AI系统设计面试题.md` | 面试 | — |
| 22 | `10-面试/04-AI应用开发面试指南.md` | 面试 | — |
| 23 | `10-面试/05-大模型基础面试题.md` | 面试 | — |
| 24 | `10-面试/06-模拟面试题库.md` | 面试 | — |

## 构建说明

- **Markdown 源**：`../HTML/` 下的 JavaGuide 网页存档由 [`../convert.py`](../convert.py) 转换为 Markdown。
- **LaTeX / PDF**：由 [`../build_pdfs.py`](../build_pdfs.py) 一键生成 `../latex/<语言>/` 与 `../pdf/<语言>/`（ctexart 双栏 + xelatex，支持 SVG/WebP 图片转换、代码高亮、难度徽章）。
- **知识地图**：由根目录 [`build_knowledge_map.py`](../build_knowledge_map.py) 生成。
