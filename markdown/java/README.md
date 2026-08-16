# Java 版 AI Agent 知识手册（原版）

> 本目录是知识手册的 **Java** 语言版本，即最初从 JavaGuide 整理的原版文档，完整保留未做删改。
> 与 `../python/`、`../typescript/` 结构完全一致，方便跨语言对照阅读。

## 代码技术栈

| 场景 | 使用的库 / 写法 |
| --- | --- |
| 工作流（Workflow/Graph/Loop） | [Spring AI Alibaba Graph](https://java2ai.com/docs/frameworks/graph-core/quick-start/)（`StateGraph`、`NodeAction`、`KeyStrategyFactory`、`MemorySaver`） |
| 结构化输出与工具调用 | Jackson + [JSON Schema Validator](https://github.com/networknt/json-schema-validator)（networknt） |
| 接口定义（网关 / 服务层） | `record` + `interface` |
| 流式输出 | WebFlux `Flux`（`Flux<LLMChunk>`、`Flux<ModelStreamEvent>`） |
| 并发控制 | `Semaphore`、Resilience4j（熔断/限流） |

## 语言化文档（4 篇，与 Python / TS 版对应）

| 文档 | 内容 |
| --- | --- |
| `01-LLM基础/02-大模型结构化输出.md` | Java 服务端校验与分发：`ToolCallDispatcher`（Jackson + JSON Schema Validator） |
| `04-工程实践/01-Workflow-Graph与Loop.md` | Spring AI Alibaba Graph 文章审核工作流（状态策略、四个节点、条件边、`MemorySaver`） |
| `04-工程实践/04-大模型网关.md` | `LLMRequest`/`LLMResponse` record、`ProviderClient`/`LLMGateway`、`RuleBasedModelRouter`、`TokenBudget` + `LLMRateLimiter` |
| `05-系统设计/01-AI应用系统设计.md` | 分层架构接口（`AiRequest`、`PromptService`、`AiTool`、`ToolRiskLevel`、`ModelGateway` 等 8 处） |

## 学习路径

1. `01-LLM基础`：LLM 运行机制 → 大模型结构化输出（Java 服务端校验与分发）
2. `02-Agent`：Agent 核心概念 → 记忆系统
3. `03-RAG`：RAG 基础概念 → 向量索引与向量数据库
4. `04-工程实践`：Workflow/Graph/Loop（Spring AI Alibaba 实战）→ Loop Engineering → Harness Engineering → 大模型网关
5. `05-系统设计`：AI 应用系统设计（Java 后端落地建议）
6. `06-面试`：六份面试题 + 模拟题库

> PDF 版见 `../../pdf/java/`，由 `../../build_pdfs.py` 编译生成。
