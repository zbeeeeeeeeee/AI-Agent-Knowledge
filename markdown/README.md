# AI Agent 知识手册（Markdown 版）

> 由 JavaGuide 的 AI 系列文章整理而成的 AI Agent / LLM / RAG 知识手册，按 **Java / Python / TypeScript** 三种语言生态提供代码示例。

本目录下每个子目录是一套**完整且独立**的语言版本，结构完全一致：

| 版本 | 目录 | 代码技术栈 |
| --- | --- | --- |
| Java | [`java/`](java/) | Spring AI Alibaba Graph、Jackson + JSON Schema Validator |
| Python | [`python/`](python/) | LangGraph、jsonschema + dataclass、pydantic、FastAPI、asyncio |
| TypeScript | [`typescript/`](typescript/) | LangGraph.js、Zod、AsyncIterable / ReadableStream、Hono / Express |

> 三套版本正文一致；纯概念类文档内容相同，含代码的文档按各自语言生态重写。
> 原 Java 版文档完整保留在 [`java/`](java/)，未做删改。

## 目录结构与学习路径

| 模块 | 主题 | 说明 |
| --- | --- | --- |
| `01-LLM基础` | LLM 运行机制、结构化输出与 Function Calling | 入门：先搞懂 Token、上下文窗口、采样参数，再学会让模型输出可靠 JSON |
| `02-Agent` | Agent 核心概念、记忆系统 | 核心：Agent Loop、Tools、MCP、短期/长期记忆与记忆演化 |
| `03-RAG` | RAG 基础概念、向量索引与向量数据库 | 检索：RAG 全流程、Embedding、向量索引算法、向量数据库选型 |
| `04-工程实践` | Workflow/Graph/Loop、Loop Engineering、Harness Engineering、大模型网关 | 进阶：从框架到生产实践的工程能力 |
| `05-系统设计` | AI 应用系统设计（Prompt Demo → 生产级架构） | 架构：分层设计、网关、Prompt 版本化、可观测与评测 |
| `06-面试` | 6 份面试题 + 模拟题库 | 冲刺：Agent / RAG / 系统设计 / 应用开发面试 + 带难度分级的模拟面试 |

**推荐阅读顺序**：`01-LLM基础` → `02-Agent` → `03-RAG` → `04-工程实践` → `05-系统设计`，面试前刷 `06-面试`。

## 文档清单（17 篇）

| # | 文档 | 模块 | 语言化代码 |
| --- | --- | --- | --- |
| 1 | `01-LLM基础/01-LLM运行机制.md` | LLM 基础 | — |
| 2 | `01-LLM基础/02-大模型结构化输出.md` | LLM 基础 | ✅ 工具调用分发器 |
| 3 | `02-Agent/01-Agent核心概念.md` | Agent | — |
| 4 | `02-Agent/02-Agent记忆系统.md` | Agent | — |
| 5 | `03-RAG/01-RAG基础概念.md` | RAG | — |
| 6 | `03-RAG/02-RAG向量索引与向量数据库.md` | RAG | — |
| 7 | `04-工程实践/01-Workflow-Graph与Loop.md` | 工程实践 | ✅ 文章审核工作流（Graph 完整实现） |
| 8 | `04-工程实践/02-Loop工程.md` | 工程实践 | — |
| 9 | `04-工程实践/03-Harness工程.md` | 工程实践 | — |
| 10 | `04-工程实践/04-大模型网关.md` | 工程实践 | ✅ 网关接口 / 规则路由 / Token 预算 |
| 11 | `05-系统设计/01-AI应用系统设计.md` | 系统设计 | ✅ 分层架构接口定义（8 处） |
| 12 | `06-面试/01-AI-Agent面试题.md` | 面试 | — |
| 13 | `06-面试/02-RAG面试题.md` | 面试 | — |
| 14 | `06-面试/03-AI系统设计面试题.md` | 面试 | — |
| 15 | `06-面试/04-AI应用开发面试指南.md` | 面试 | — |
| 16 | `06-面试/05-大模型基础面试题.md` | 面试 | — |
| 17 | `06-面试/06-模拟面试题库.md` | 面试 | — |

## 构建说明

- **Markdown 源**：`../HTML/` 下的 JavaGuide 网页存档由 [`../convert.py`](../convert.py) 转换为 Markdown。
- **LaTeX / PDF**：由 [`../build_pdfs.py`](../build_pdfs.py) 一键生成 `../latex/<语言>/` 与 `../pdf/<语言>/`（ctexart 双栏 + xelatex，支持 SVG/WebP 图片转换、代码高亮、难度徽章）。
