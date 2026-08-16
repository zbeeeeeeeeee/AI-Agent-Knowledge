# TypeScript 版 AI Agent 知识手册

> 本目录是知识手册的 **TypeScript** 语言版本（与 `../java/`、`../python/` 结构完全一致）。
> 4 篇含代码的文档已按 TypeScript 生态重写，其余文档为语言无关的概念/面试内容，与 Java 版一致。

## 代码技术栈映射

| 场景 | 使用的库 / 写法 |
| --- | --- |
| 工作流（Workflow/Graph/Loop） | [LangGraph.js](https://langchain-ai.github.io/langgraphjs/)（`Annotation.Root` + reducer、`StateGraph`、`MemorySaver`、`addConditionalEdges`） |
| 结构化输出与工具调用 | [Zod](https://zod.dev/)（`z.object` 契约校验 + 类型推导 `z.infer`） |
| 接口定义（网关 / 服务层） | `interface` + `type`（结构化类型）+ 构造器依赖注入 |
| 流式输出 | `AsyncIterable` / `ReadableStream`（异步流式） |
| 服务端 Web 框架 | Hono / Express（网关、编排服务） |
| 并发控制 | `p-limit`、`opossum`（熔断器） |

## 语言化文档（4 篇）

| 文档 | 原文（Java） | TypeScript 版 |
| --- | --- | --- |
| `01-LLM基础/02-大模型结构化输出.md` | Jackson + JSON Schema Validator 的 `ToolCallDispatcher` | Zod `ToolCallDispatcher`（`safeParse` 校验 + async 分发 → 鉴权 → 执行 → 审计） |
| `04-工程实践/01-Workflow-Graph与Loop.md` | Spring AI Alibaba Graph 文章审核工作流 | LangGraph.js 完整实现（状态 Annotation、四个节点、条件边路由、`MemorySaver` 持久化） |
| `04-工程实践/04-大模型网关.md` | Java record / 接口 | `interface` 请求响应 + `ProviderClient`/`LLMGateway` 适配器 + 规则路由 + Token 预算限流 |
| `07-系统设计/01-AI应用系统设计.md` | Java 分层接口（8 处） | `interface`（`AiRequest` 等）+ union type（风险等级）+ 网关/RAG/评测接口（含 `AsyncIterable` 流式） |

## 目录结构

| 模块 | 说明 |
| --- | --- |
| `00-概念与术语` | 术语表与概念边界、自主性分级 |
| `01-LLM基础` | LLM 运行机制、结构化输出 |
| `02-Agent` | Agent 核心概念、记忆系统、多智能体编排 |
| `03-RAG` | RAG 基础、向量索引与向量数据库 |
| `04-工程实践` | Workflow/Graph/Loop、Loop Engineering、Harness Engineering、大模型网关、可观测与追踪、部署与发布 |
| `05-评测与质量` | Agent 评测体系 |
| `06-安全与治理` | Agent 安全护栏清单 |
| `07-系统设计` | AI 应用系统设计 |
| `08-应用与案例` | 待补全 |
| `09-生态与前沿` | 待补全 |
| `10-面试` | 6 份面试题 + 模拟题库 |

## 学习路径

1. `00-概念与术语`：先统一术语边界与自主性分级
2. `01-LLM基础`：LLM 运行机制 → 大模型结构化输出（TypeScript 服务端校验与分发）
3. `02-Agent`：Agent 核心概念 → 记忆系统 → 多智能体编排
4. `03-RAG`：RAG 基础概念 → 向量索引与向量数据库
5. `04-工程实践`：Workflow/Graph/Loop（LangGraph.js 实战）→ Loop Engineering → Harness Engineering → 大模型网关 → 可观测与追踪 → 部署与发布
6. `05-评测与质量`：Agent 评测体系（TypeScript 评测执行器）
7. `06-安全与治理`：Agent 安全护栏清单（TypeScript 工具风控实现）
8. `07-系统设计`：AI 应用系统设计（TypeScript 后端落地建议）
9. `10-面试`：六份面试题 + 模拟题库

> PDF 版见 `../../pdf/typescript/`，由 `../../build_pdfs.py` 编译生成。
