<map version="1.0.1">
<node TEXT="AI Agent 知识总索引">
  <node TEXT="00 阅读入口" LINK="markdown/README.md">
    <node TEXT="按角色阅读">
      <node TEXT="🟡 新手入门 ≡" LINK="markdown/java/README.md"/>
      <node TEXT="🟡 后端工程师 ≡" LINK="markdown/java/README.md"/>
      <node TEXT="🟡 算法工程师 ≡" LINK="markdown/java/02-Agent/01-Agent核心概念.md"/>
      <node TEXT="🟡 架构师 ≡" LINK="markdown/java/07-系统设计/01-AI应用系统设计.md"/>
    </node>
    <node TEXT="按生命周期">
      <node TEXT="🟢 概念入门 ≡" LINK="markdown/java/README.md"/>
      <node TEXT="🟢 系统开发 ≡" LINK="markdown/java/04-工程实践/01-Workflow-Graph与Loop.md"/>
      <node TEXT="🟡 评测上线 ≡" LINK="markdown/java/07-系统设计/01-AI应用系统设计.md"/>
      <node TEXT="🟡 运营治理 ≡" LINK="markdown/java/04-工程实践/04-大模型网关.md"/>
    </node>
    <node TEXT="按语言阅读">
      <node TEXT="Java 版">
        <node TEXT="🟢 Java 全部文档" LINK="markdown/java/README.md"/>
        <node TEXT="🟢 Java PDF 版" LINK="pdf/java"/>
      </node>
      <node TEXT="Python 版">
        <node TEXT="🟢 Python 全部文档" LINK="markdown/python/README.md"/>
        <node TEXT="🟢 Python PDF 版" LINK="pdf/python"/>
      </node>
      <node TEXT="TypeScript 版">
        <node TEXT="🟢 TypeScript 全部文档" LINK="markdown/typescript/README.md"/>
        <node TEXT="🟢 TypeScript PDF 版" LINK="pdf/typescript"/>
      </node>
    </node>
  </node>
  <node TEXT="🟡 01 概念与分类 ≡" LINK="markdown/java/02-Agent/01-Agent核心概念.md">
    <node TEXT="🟡 Agent 定义与边界 ≡" LINK="markdown/java/02-Agent/01-Agent核心概念.md">
      <node TEXT="🟢 Agent 是什么 ≡" LINK="markdown/java/02-Agent/01-Agent核心概念.md"/>
      <node TEXT="🟢 Agent vs Chatbot ≡" LINK="markdown/java/00-概念与术语/01-Agent术语表与概念边界.md"/>
      <node TEXT="🟢 Agent vs Workflow ≡" LINK="markdown/java/02-Agent/01-Agent核心概念.md"/>
      <node TEXT="🟡 Agent vs RAG ≡" LINK="markdown/java/02-Agent/02-Agent记忆系统.md"/>
    </node>
    <node TEXT="🟢 自主性分级 ≡" LINK="markdown/java/00-概念与术语/02-Agent自主性分级.md"/>
    <node TEXT="🟡 分类体系与范式 ≡" LINK="markdown/java/02-Agent/01-Agent核心概念.md">
      <node TEXT="🟢 ReAct ≡" LINK="markdown/java/02-Agent/01-Agent核心概念.md"/>
      <node TEXT="🟢 Plan-and-Execute ≡" LINK="markdown/java/02-Agent/01-Agent核心概念.md"/>
      <node TEXT="🟡 Reflection ≡" LINK="markdown/java/02-Agent/01-Agent核心概念.md"/>
      <node TEXT="🟡 Multi-Agent ≡" LINK="markdown/java/02-Agent/01-Agent核心概念.md"/>
      <node TEXT="🟢 Agentic Workflows ≡" LINK="markdown/java/02-Agent/01-Agent核心概念.md"/>
      <node TEXT="🟡 A2A 协议 ≡" LINK="markdown/java/02-Agent/01-Agent核心概念.md"/>
      <node TEXT="🟢 各范式选型 ≡" LINK="markdown/java/02-Agent/01-Agent核心概念.md"/>
    </node>
    <node TEXT="🟢 术语表 ≡" LINK="markdown/java/00-概念与术语/01-Agent术语表与概念边界.md"/>
  </node>
  <node TEXT="🟡 02 能力模型 ≡" LINK="markdown/java/02-Agent/01-Agent核心概念.md">
    <node TEXT="🟡 感知与输入 ≡" LINK="markdown/java/01-LLM基础/01-LLM运行机制.md">
      <node TEXT="🟡 多模态 Token 化 ≡" LINK="markdown/java/01-LLM基础/01-LLM运行机制.md"/>
      <node TEXT="🟢 上下文窗口边界 ≡" LINK="markdown/java/01-LLM基础/01-LLM运行机制.md"/>
    </node>
    <node TEXT="🟢 记忆系统 ≡" LINK="markdown/java/02-Agent/02-Agent记忆系统.md">
      <node TEXT="🟢 短期记忆 ≡" LINK="markdown/java/02-Agent/02-Agent记忆系统.md"/>
      <node TEXT="🟢 长期记忆 ≡" LINK="markdown/java/02-Agent/02-Agent记忆系统.md"/>
      <node TEXT="🟢 记忆生命周期 ≡" LINK="markdown/java/02-Agent/02-Agent记忆系统.md"/>
      <node TEXT="🟢 记忆检索优化 ≡" LINK="markdown/java/02-Agent/02-Agent记忆系统.md"/>
      <node TEXT="🟢 Markdown 记忆 ≡" LINK="markdown/java/02-Agent/02-Agent记忆系统.md"/>
    </node>
    <node TEXT="🟡 规划与决策 ≡" LINK="markdown/java/02-Agent/01-Agent核心概念.md">
      <node TEXT="🟢 任务分解 ≡" LINK="markdown/java/02-Agent/01-Agent核心概念.md"/>
      <node TEXT="🟡 反思与自评 ≡" LINK="markdown/java/02-Agent/01-Agent核心概念.md"/>
      <node TEXT="🟡 成本约束决策 ≡" LINK="markdown/java/04-工程实践/02-Loop工程.md"/>
    </node>
    <node TEXT="🟢 工具使用与行动 ≡" LINK="markdown/java/01-LLM基础/02-大模型结构化输出.md">
      <node TEXT="🟢 Function Calling ≡" LINK="markdown/java/01-LLM基础/02-大模型结构化输出.md"/>
      <node TEXT="🟢 Tools 注册与 Schema ≡" LINK="markdown/java/02-Agent/01-Agent核心概念.md"/>
      <node TEXT="🟡 MCP 工具接入 ≡" LINK="markdown/java/02-Agent/01-Agent核心概念.md"/>
      <node TEXT="🟡 Agent Skills ≡" LINK="markdown/java/02-Agent/01-Agent核心概念.md"/>
    </node>
    <node TEXT="🟡 协作与沟通 ≡" LINK="markdown/java/02-Agent/01-Agent核心概念.md">
      <node TEXT="🟢 多智能体协作 ≡" LINK="markdown/java/02-Agent/03-多智能体编排.md"/>
      <node TEXT="🟡 A2A 通信 ≡" LINK="markdown/java/02-Agent/01-Agent核心概念.md"/>
    </node>
  </node>
  <node TEXT="🟡 03 架构与运行机制 ≡" LINK="markdown/java/02-Agent/01-Agent核心概念.md">
    <node TEXT="🟢 单 Agent 运行循环 ≡" LINK="markdown/java/02-Agent/01-Agent核心概念.md">
      <node TEXT="🟢 Agent Loop ≡" LINK="markdown/java/02-Agent/01-Agent核心概念.md"/>
      <node TEXT="🟢 最小三层架构 ≡" LINK="markdown/java/02-Agent/01-Agent核心概念.md"/>
    </node>
    <node TEXT="🟡 上下文与提示词架构 ≡" LINK="markdown/java/04-工程实践/03-Harness工程.md">
      <node TEXT="🟢 Prompt Engineering ≡" LINK="markdown/java/02-Agent/01-Agent核心概念.md"/>
      <node TEXT="🟢 Context Engineering ≡" LINK="markdown/java/02-Agent/01-Agent核心概念.md"/>
      <node TEXT="🟢 上下文利用 40% 现象 ≡" LINK="markdown/java/04-工程实践/03-Harness工程.md"/>
    </node>
    <node TEXT="🟢 工作流编排 ≡" LINK="markdown/java/04-工程实践/01-Workflow-Graph与Loop.md">
      <node TEXT="🟢 Workflow ≡" LINK="markdown/java/04-工程实践/01-Workflow-Graph与Loop.md"/>
      <node TEXT="🟢 Graph ≡" LINK="markdown/java/04-工程实践/01-Workflow-Graph与Loop.md"/>
      <node TEXT="🟢 Loop ≡" LINK="markdown/java/04-工程实践/01-Workflow-Graph与Loop.md"/>
      <node TEXT="🟢 框架概念对照 ≡" LINK="markdown/java/04-工程实践/01-Workflow-Graph与Loop.md"/>
      <node TEXT="Workflow 三语言实现">
        <node TEXT="🟢 Workflow 三语言实现 · Java 实现" LINK="markdown/java/04-工程实践/01-Workflow-Graph与Loop.md"/>
        <node TEXT="🟢 Workflow 三语言实现 · Python 实现" LINK="markdown/python/04-工程实践/01-Workflow-Graph与Loop.md"/>
        <node TEXT="🟢 Workflow 三语言实现 · TypeScript 实现" LINK="markdown/typescript/04-工程实践/01-Workflow-Graph与Loop.md"/>
      </node>
    </node>
    <node TEXT="🟢 模型接入层 ≡" LINK="markdown/java/04-工程实践/04-大模型网关.md">
      <node TEXT="🟢 LLM 运行机制 ≡" LINK="markdown/java/01-LLM基础/01-LLM运行机制.md"/>
      <node TEXT="结构化输出">
        <node TEXT="🟢 结构化输出 · Java 实现" LINK="markdown/java/01-LLM基础/02-大模型结构化输出.md"/>
        <node TEXT="🟢 结构化输出 · Python 实现" LINK="markdown/python/01-LLM基础/02-大模型结构化输出.md"/>
        <node TEXT="🟢 结构化输出 · TypeScript 实现" LINK="markdown/typescript/01-LLM基础/02-大模型结构化输出.md"/>
      </node>
      <node TEXT="🟢 大模型网关 ≡" LINK="markdown/java/04-工程实践/04-大模型网关.md"/>
      <node TEXT="🟢 路由与 Fallback ≡" LINK="markdown/java/04-工程实践/04-大模型网关.md"/>
    </node>
    <node TEXT="🟢 检索架构 RAG ≡" LINK="markdown/java/03-RAG/01-RAG基础概念.md">
      <node TEXT="🟢 RAG 基础 ≡" LINK="markdown/java/03-RAG/01-RAG基础概念.md"/>
      <node TEXT="🟢 Embedding ≡" LINK="markdown/java/03-RAG/01-RAG基础概念.md"/>
      <node TEXT="🟢 向量索引算法 ≡" LINK="markdown/java/03-RAG/02-RAG向量索引与向量数据库.md"/>
      <node TEXT="🟢 向量数据库选型 ≡" LINK="markdown/java/03-RAG/02-RAG向量索引与向量数据库.md"/>
      <node TEXT="🟢 混合检索与 RRF ≡" LINK="markdown/java/03-RAG/03-RAG高级检索.md"/>
      <node TEXT="🟢 Rerank 精排 ≡" LINK="markdown/java/03-RAG/03-RAG高级检索.md"/>
      <node TEXT="🟢 查询改写 ≡" LINK="markdown/java/03-RAG/03-RAG高级检索.md"/>
      <node TEXT="🟡 GraphRAG ≡" LINK="markdown/java/03-RAG/03-RAG高级检索.md"/>
      <node TEXT="三语言检索实现">
        <node TEXT="🟢 三语言检索实现 · Java 实现" LINK="markdown/java/03-RAG/03-RAG高级检索.md"/>
        <node TEXT="🟢 三语言检索实现 · Python 实现" LINK="markdown/python/03-RAG/03-RAG高级检索.md"/>
        <node TEXT="🟢 三语言检索实现 · TypeScript 实现" LINK="markdown/typescript/03-RAG/03-RAG高级检索.md"/>
      </node>
    </node>
    <node TEXT="🟢 Harness 工程 ≡" LINK="markdown/java/04-工程实践/03-Harness工程.md">
      <node TEXT="🟢 六层架构 ≡" LINK="markdown/java/04-工程实践/03-Harness工程.md"/>
      <node TEXT="🟢 一线团队案例 ≡" LINK="markdown/java/04-工程实践/03-Harness工程.md"/>
    </node>
    <node TEXT="🟢 多智能体编排 ≡" LINK="markdown/java/02-Agent/03-多智能体编排.md">
      <node TEXT="🟢 编排模式 ≡" LINK="markdown/java/02-Agent/03-多智能体编排.md"/>
      <node TEXT="🟡 通信协议 ≡" LINK="markdown/java/02-Agent/03-多智能体编排.md"/>
    </node>
  </node>
  <node TEXT="🟡 04 开发与工程化 ≡" LINK="markdown/java/07-系统设计/01-AI应用系统设计.md">
    <node TEXT="🟡 技术选型与框架 ≡" LINK="markdown/java/README.md">
      <node TEXT="🟢 Java 技术栈" LINK="markdown/java/README.md"/>
      <node TEXT="🟢 Python 技术栈" LINK="markdown/python/README.md"/>
      <node TEXT="🟢 TypeScript 技术栈" LINK="markdown/typescript/README.md"/>
      <node TEXT="🟢 框架与平台对比 ≡" LINK="markdown/java/04-工程实践/07-Agent框架选型对比.md"/>
    </node>
    <node TEXT="🟢 设计模式与范式 ≡" LINK="markdown/java/04-工程实践/01-Workflow-Graph与Loop.md">
      <node TEXT="🟢 Workflow Graph Loop ≡" LINK="markdown/java/04-工程实践/01-Workflow-Graph与Loop.md"/>
      <node TEXT="🟢 Loop Engineering ≡" LINK="markdown/java/04-工程实践/02-Loop工程.md"/>
      <node TEXT="🟢 Harness Engineering ≡" LINK="markdown/java/04-工程实践/03-Harness工程.md"/>
    </node>
    <node TEXT="🟢 上下文工程 ≡" LINK="markdown/java/04-工程实践/08-上下文工程.md">
      <node TEXT="🟢 Prompt 版本化 ≡" LINK="markdown/java/04-工程实践/08-上下文工程.md"/>
      <node TEXT="🟢 RAG 与 Memory 边界 ≡" LINK="markdown/java/02-Agent/02-Agent记忆系统.md"/>
      <node TEXT="🟢 Token 预算与上下文压缩 ≡" LINK="markdown/java/04-工程实践/08-上下文工程.md"/>
      <node TEXT="三语言上下文组装器">
        <node TEXT="🟢 三语言上下文组装器 · Java 实现" LINK="markdown/java/04-工程实践/08-上下文工程.md"/>
        <node TEXT="🟢 三语言上下文组装器 · Python 实现" LINK="markdown/python/04-工程实践/08-上下文工程.md"/>
        <node TEXT="🟢 三语言上下文组装器 · TypeScript 实现" LINK="markdown/typescript/04-工程实践/08-上下文工程.md"/>
      </node>
    </node>
    <node TEXT="🟢 成本与性能优化 ≡" LINK="markdown/java/04-工程实践/09-成本与性能优化.md">
      <node TEXT="🟢 成本归因 ≡" LINK="markdown/java/04-工程实践/09-成本与性能优化.md"/>
      <node TEXT="🟢 模型分级与缓存 ≡" LINK="markdown/java/04-工程实践/09-成本与性能优化.md"/>
      <node TEXT="🟢 限流与并发 ≡" LINK="markdown/java/04-工程实践/09-成本与性能优化.md"/>
      <node TEXT="三语言成本限流示例">
        <node TEXT="🟢 三语言成本限流示例 · Java 实现" LINK="markdown/java/04-工程实践/09-成本与性能优化.md"/>
        <node TEXT="🟢 三语言成本限流示例 · Python 实现" LINK="markdown/python/04-工程实践/09-成本与性能优化.md"/>
        <node TEXT="🟢 三语言成本限流示例 · TypeScript 实现" LINK="markdown/typescript/04-工程实践/09-成本与性能优化.md"/>
      </node>
    </node>
    <node TEXT="🟢 系统设计 ≡" LINK="markdown/java/07-系统设计/01-AI应用系统设计.md">
      <node TEXT="🟢 生产级分层架构 ≡" LINK="markdown/java/07-系统设计/01-AI应用系统设计.md"/>
      <node TEXT="🟢 同步 流式 异步模式 ≡" LINK="markdown/java/07-系统设计/01-AI应用系统设计.md"/>
      <node TEXT="🟢 工具调用与权限模型 ≡" LINK="markdown/java/07-系统设计/01-AI应用系统设计.md"/>
      <node TEXT="系统设计三语言接口实现">
        <node TEXT="🟢 系统设计三语言接口实现 · Java 实现" LINK="markdown/java/07-系统设计/01-AI应用系统设计.md"/>
        <node TEXT="🟢 系统设计三语言接口实现 · Python 实现" LINK="markdown/python/07-系统设计/01-AI应用系统设计.md"/>
        <node TEXT="🟢 系统设计三语言接口实现 · TypeScript 实现" LINK="markdown/typescript/07-系统设计/01-AI应用系统设计.md"/>
      </node>
    </node>
    <node TEXT="🟢 网关与基础设施 ≡" LINK="markdown/java/04-工程实践/04-大模型网关.md">
      <node TEXT="🟢 多模型统一接入 ≡" LINK="markdown/java/04-工程实践/04-大模型网关.md"/>
      <node TEXT="🟢 限流与配额 ≡" LINK="markdown/java/04-工程实践/04-大模型网关.md"/>
      <node TEXT="🟢 成本统计与预算 ≡" LINK="markdown/java/04-工程实践/04-大模型网关.md"/>
      <node TEXT="🟡 缓存与语义缓存 ≡" LINK="markdown/java/04-工程实践/04-大模型网关.md"/>
      <node TEXT="网关三语言实现">
        <node TEXT="🟢 网关三语言实现 · Java 实现" LINK="markdown/java/04-工程实践/04-大模型网关.md"/>
        <node TEXT="🟢 网关三语言实现 · Python 实现" LINK="markdown/python/04-工程实践/04-大模型网关.md"/>
        <node TEXT="🟢 网关三语言实现 · TypeScript 实现" LINK="markdown/typescript/04-工程实践/04-大模型网关.md"/>
      </node>
    </node>
    <node TEXT="🟢 部署与发布 ≡" LINK="markdown/java/04-工程实践/06-Agent部署与发布.md">
      <node TEXT="🟢 部署形态 ≡" LINK="markdown/java/04-工程实践/06-Agent部署与发布.md"/>
      <node TEXT="🟢 版本与回滚 ≡" LINK="markdown/java/04-工程实践/06-Agent部署与发布.md"/>
      <node TEXT="🟡 容量与扩展 ≡" LINK="markdown/java/04-工程实践/06-Agent部署与发布.md"/>
      <node TEXT="三语言部署示例">
        <node TEXT="🟢 三语言部署示例 · Java 实现" LINK="markdown/java/04-工程实践/06-Agent部署与发布.md"/>
        <node TEXT="🟢 三语言部署示例 · Python 实现" LINK="markdown/python/04-工程实践/06-Agent部署与发布.md"/>
        <node TEXT="🟢 三语言部署示例 · TypeScript 实现" LINK="markdown/typescript/04-工程实践/06-Agent部署与发布.md"/>
      </node>
    </node>
    <node TEXT="🟢 可观测与调试 ≡" LINK="markdown/java/04-工程实践/05-Agent可观测与追踪.md">
      <node TEXT="🟢 Trace 记录 ≡" LINK="markdown/java/04-工程实践/05-Agent可观测与追踪.md"/>
      <node TEXT="🟢 日志与回放 ≡" LINK="markdown/java/04-工程实践/05-Agent可观测与追踪.md"/>
      <node TEXT="🟡 调试工具链 ≡" LINK="markdown/java/04-工程实践/05-Agent可观测与追踪.md"/>
      <node TEXT="三语言采集器">
        <node TEXT="🟢 三语言采集器 · Java 实现" LINK="markdown/java/04-工程实践/05-Agent可观测与追踪.md"/>
        <node TEXT="🟢 三语言采集器 · Python 实现" LINK="markdown/python/04-工程实践/05-Agent可观测与追踪.md"/>
        <node TEXT="🟢 三语言采集器 · TypeScript 实现" LINK="markdown/typescript/04-工程实践/05-Agent可观测与追踪.md"/>
      </node>
    </node>
  </node>
  <node TEXT="🟡 05 评测与质量 ≡" LINK="markdown/java/05-评测与质量/01-Agent评测体系.md">
    <node TEXT="🟢 指标体系 ≡" LINK="markdown/java/05-评测与质量/01-Agent评测体系.md">
      <node TEXT="🟢 任务成功率 ≡" LINK="markdown/java/05-评测与质量/01-Agent评测体系.md"/>
      <node TEXT="🟢 轨迹质量 ≡" LINK="markdown/java/05-评测与质量/01-Agent评测体系.md"/>
      <node TEXT="🟢 工具调用准确率 ≡" LINK="markdown/java/05-评测与质量/01-Agent评测体系.md"/>
      <node TEXT="🟢 延迟与成本 ≡" LINK="markdown/java/05-评测与质量/01-Agent评测体系.md"/>
    </node>
    <node TEXT="🟡 评测方法 ≡" LINK="markdown/java/05-评测与质量/01-Agent评测体系.md">
      <node TEXT="🟢 离线评测集 ≡" LINK="markdown/java/05-评测与质量/01-Agent评测体系.md"/>
      <node TEXT="🟢 人工评测 ≡" LINK="markdown/java/05-评测与质量/01-Agent评测体系.md"/>
      <node TEXT="🟡 在线 A B 实验 ≡" LINK="markdown/java/05-评测与质量/01-Agent评测体系.md"/>
      <node TEXT="🟢 LLM-as-Judge ≡" LINK="markdown/java/05-评测与质量/01-Agent评测体系.md"/>
      <node TEXT="三语言评测脚本">
        <node TEXT="🟢 三语言评测脚本 · Java 实现" LINK="markdown/java/05-评测与质量/01-Agent评测体系.md"/>
        <node TEXT="🟢 三语言评测脚本 · Python 实现" LINK="markdown/python/05-评测与质量/01-Agent评测体系.md"/>
        <node TEXT="🟢 三语言评测脚本 · TypeScript 实现" LINK="markdown/typescript/05-评测与质量/01-Agent评测体系.md"/>
      </node>
    </node>
    <node TEXT="🟡 评测基座与回归 ≡" LINK="markdown/java/05-评测与质量/01-Agent评测体系.md">
      <node TEXT="🟢 评测集构建 ≡" LINK="markdown/java/05-评测与质量/01-Agent评测体系.md"/>
      <node TEXT="🔴 基准与榜单"/>
      <node TEXT="🟢 回归与 CI ≡" LINK="markdown/java/05-评测与质量/01-Agent评测体系.md"/>
    </node>
    <node TEXT="🟡 持续改进 ≡" LINK="markdown/java/04-工程实践/03-Harness工程.md">
      <node TEXT="🟡 Human-in-the-Loop ≡" LINK="markdown/java/07-系统设计/01-AI应用系统设计.md"/>
      <node TEXT="🟢 反馈闭环 ≡" LINK="markdown/java/05-评测与质量/01-Agent评测体系.md"/>
    </node>
  </node>
  <node TEXT="🟡 06 安全与治理 ≡" LINK="markdown/java/06-安全与治理/01-Agent安全护栏清单.md">
    <node TEXT="🟢 风险分类 ≡" LINK="markdown/java/06-安全与治理/01-Agent安全护栏清单.md">
      <node TEXT="🟢 模型风险 ≡" LINK="markdown/java/06-安全与治理/01-Agent安全护栏清单.md"/>
      <node TEXT="🟢 工具风险 ≡" LINK="markdown/java/06-安全与治理/01-Agent安全护栏清单.md"/>
      <node TEXT="🟢 数据风险 ≡" LINK="markdown/java/06-安全与治理/01-Agent安全护栏清单.md"/>
    </node>
    <node TEXT="🟡 护栏机制 ≡" LINK="markdown/java/06-安全与治理/01-Agent安全护栏清单.md">
      <node TEXT="🟢 权限最小化 ≡" LINK="markdown/java/06-安全与治理/01-Agent安全护栏清单.md"/>
      <node TEXT="🟡 沙箱执行 ≡" LINK="markdown/java/06-安全与治理/01-Agent安全护栏清单.md"/>
      <node TEXT="🟢 Prompt 注入防护 ≡" LINK="markdown/java/06-安全与治理/01-Agent安全护栏清单.md"/>
      <node TEXT="🟡 内容安全 ≡" LINK="markdown/java/06-安全与治理/01-Agent安全护栏清单.md"/>
      <node TEXT="三语言工具风控实现">
        <node TEXT="🟢 三语言工具风控实现 · Java 实现" LINK="markdown/java/06-安全与治理/01-Agent安全护栏清单.md"/>
        <node TEXT="🟢 三语言工具风控实现 · Python 实现" LINK="markdown/python/06-安全与治理/01-Agent安全护栏清单.md"/>
        <node TEXT="🟢 三语言工具风控实现 · TypeScript 实现" LINK="markdown/typescript/06-安全与治理/01-Agent安全护栏清单.md"/>
      </node>
    </node>
    <node TEXT="🟡 合规与审计 ≡" LINK="markdown/java/06-安全与治理/01-Agent安全护栏清单.md">
      <node TEXT="🟡 隐私与数据边界 ≡" LINK="markdown/java/07-系统设计/01-AI应用系统设计.md"/>
      <node TEXT="🟢 审计日志 ≡" LINK="markdown/java/06-安全与治理/01-Agent安全护栏清单.md"/>
      <node TEXT="🟡 第三方模型数据边界 ≡" LINK="markdown/java/07-系统设计/01-AI应用系统设计.md"/>
    </node>
    <node TEXT="🟡 责任与流程 ≡" LINK="markdown/java/06-安全与治理/01-Agent安全护栏清单.md">
      <node TEXT="🟢 审批流程 ≡" LINK="markdown/java/06-安全与治理/01-Agent安全护栏清单.md"/>
      <node TEXT="🟡 责任归属 ≡" LINK="markdown/java/06-安全与治理/01-Agent安全护栏清单.md"/>
    </node>
  </node>
  <node TEXT="🟡 07 应用与案例 ≡" LINK="markdown/java/04-工程实践/03-Harness工程.md">
    <node TEXT="🟡 选型决策 ≡" LINK="markdown/java/02-Agent/01-Agent核心概念.md">
      <node TEXT="🟡 是否用 Agent 决策树 ≡" LINK="markdown/java/02-Agent/01-Agent核心概念.md"/>
      <node TEXT="🟢 Workflow vs Agent ≡" LINK="markdown/java/02-Agent/01-Agent核心概念.md"/>
    </node>
    <node TEXT="🟡 场景模式库 ≡" LINK="markdown/java/04-工程实践/03-Harness工程.md">
      <node TEXT="🟡 编码 Agent ≡" LINK="markdown/java/04-工程实践/03-Harness工程.md"/>
      <node TEXT="🔴 客服 Agent"/>
      <node TEXT="🔴 数据分析 Agent"/>
      <node TEXT="🔴 办公自动化 Agent"/>
    </node>
    <node TEXT="🟢 行业解决方案 ≡" LINK="markdown/java/08-应用与案例/02-行业场景方案.md">
      <node TEXT="🟢 金融 ≡" LINK="markdown/java/08-应用与案例/02-行业场景方案.md"/>
      <node TEXT="🟢 医疗 ≡" LINK="markdown/java/08-应用与案例/02-行业场景方案.md"/>
      <node TEXT="🟢 电商 ≡" LINK="markdown/java/08-应用与案例/02-行业场景方案.md"/>
      <node TEXT="🟢 企业服务 ≡" LINK="markdown/java/08-应用与案例/02-行业场景方案.md"/>
    </node>
    <node TEXT="🟢 案例库 ≡" LINK="markdown/java/08-应用与案例/01-案例库与反模式索引.md">
      <node TEXT="🟢 案例索引 ≡" LINK="markdown/java/08-应用与案例/01-案例库与反模式索引.md"/>
      <node TEXT="🟢 可复用模式 ≡" LINK="markdown/java/08-应用与案例/01-案例库与反模式索引.md"/>
      <node TEXT="🟢 OpenAI 三人团队 ≡" LINK="markdown/java/04-工程实践/03-Harness工程.md"/>
      <node TEXT="🟢 Anthropic 三智能体 ≡" LINK="markdown/java/04-工程实践/03-Harness工程.md"/>
      <node TEXT="🟢 Stripe 每周 1300 PR ≡" LINK="markdown/java/04-工程实践/03-Harness工程.md"/>
      <node TEXT="🟢 失败案例与反模式 ≡" LINK="markdown/java/08-应用与案例/01-案例库与反模式索引.md"/>
    </node>
  </node>
  <node TEXT="🟡 08 生态与前沿 ≡" LINK="markdown/java/09-生态与前沿/01-Agent技术雷达.md">
    <node TEXT="🟡 协议与标准 ≡" LINK="markdown/java/09-生态与前沿/01-Agent技术雷达.md">
      <node TEXT="🟢 MCP 标准 ≡" LINK="markdown/java/09-生态与前沿/01-Agent技术雷达.md"/>
      <node TEXT="🟡 A2A 标准 ≡" LINK="markdown/java/09-生态与前沿/01-Agent技术雷达.md"/>
      <node TEXT="🟢 Skills 标准 ≡" LINK="markdown/java/09-生态与前沿/01-Agent技术雷达.md"/>
    </node>
    <node TEXT="🟢 技术雷达 ≡" LINK="markdown/java/09-生态与前沿/01-Agent技术雷达.md">
      <node TEXT="🟢 论文清单 ≡" LINK="markdown/java/09-生态与前沿/02-论文精读清单.md"/>
      <node TEXT="🟢 框架动态 ≡" LINK="markdown/java/09-生态与前沿/01-Agent技术雷达.md"/>
      <node TEXT="🟢 产品平台动态 ≡" LINK="markdown/java/09-生态与前沿/01-Agent技术雷达.md"/>
    </node>
    <node TEXT="🟡 趋势判断 ≡" LINK="markdown/java/09-生态与前沿/01-Agent技术雷达.md">
      <node TEXT="🟢 Harness 趋势 ≡" LINK="markdown/java/04-工程实践/03-Harness工程.md"/>
      <node TEXT="🟡 多智能体趋势 ≡" LINK="markdown/java/09-生态与前沿/01-Agent技术雷达.md"/>
      <node TEXT="🟢 评测与治理趋势 ≡" LINK="markdown/java/09-生态与前沿/01-Agent技术雷达.md"/>
    </node>
  </node>
</node>
</map>
