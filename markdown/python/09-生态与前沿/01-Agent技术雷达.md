# Agent 技术雷达

> 语言策略：shared（Java canonical，P/T 同文）

## 级别定义

- **Adopt**：知识库已有实践，默认采用；
- **Trial**：值得试点，但有前提；
- **Assess**：值得观察，暂不投入；
- **Hold**：当前不建议生产采用。

## 1. 协议与标准

| 项目 | 级别 | 说明 |
| --- | --- | --- |
| MCP | Adopt | 工具/资源/提示词接入标准，知识库已纳入工具层 |
| Agent Skills | Adopt | 经验包与延迟加载模式，适合团队知识沉淀 |
| A2A | Assess | 多智能体任务交换方向正确，生态仍在收敛 |
| OpenTelemetry GenAI | Trial | Trace 语义正在稳定，可用于供应商无关采集 |

## 2. 框架与库

| 项目 | 级别 | 说明 |
| --- | --- | --- |
| LangGraph | Adopt | Python 生产级 Graph + Agent 基线 |
| LangGraph.js | Adopt | TypeScript 生产级基线 |
| Spring AI Alibaba Graph | Adopt | Java 生态基线 |
| OpenAI Agents SDK | Trial | 原型快，注意供应商绑定 |
| AutoGen | Assess | 多智能体研究价值高，生产运维需自建 |
| CrewAI | Assess | 角色化流水线友好，复杂控制流要评估 |

## 3. 平台与产品

| 项目 | 级别 | 说明 |
| --- | --- | --- |
| Claude Code / Codex 类编码 Agent | Adopt | 已有 Harness/Loop 实践素材 |
| LangSmith / Langfuse 类观测平台 | Trial | 与自建 Trace 二选一，先定义 Span 模型 |
| 通用 Agent 托管平台 | Assess | 关注锁定、数据边界与单位成本 |
| 低代码 Agent 平台 | Hold | 复杂控制与可观测性不足时不要硬上 |

## 4. 研究趋势

| 趋势 | 级别 | 对工程的影响 |
| --- | --- | --- |
| Agentic Workflows | Adopt | 固定骨架 + 局部自主是当前生产主流 |
| Context Engineering | Adopt | 决定效果上限，优先于换模型 |
| Memory 分层 | Trial | 短期上下文 + 长期检索 + 项目记忆 |
| Multi-Agent | Assess | 只在单 Agent 证明不足后采用 |
| Agent 评测与安全 | Adopt | 没有回归门禁与护栏不允许上线 |
| GUI / Computer Use Agent | Assess | 观察沙箱与审计成熟度 |

## 5. 更新规则

1. 季度评审一次，更新级别和说明；
2. 每个项目必须有对应文档或实践记录，不允许只贴链接；
3. 从 Assess 升到 Trial 需要 PoC 记录；升到 Adopt 需要评测与回滚方案。

## 6. 延伸阅读

- [Agent 框架与平台横评](../04-工程实践/07-Agent框架选型对比.md)
- [论文精读清单](02-论文精读清单.md)
- [知识地图总索引](../../../知识地图总索引.md)
