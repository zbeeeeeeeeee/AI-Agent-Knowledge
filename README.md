# AI Agent 知识库

> 最外层入口：先看[**知识地图总索引**](知识地图总索引.md)，再进入具体文档。
> 当前版本：**知识地图三语言版 v0.5**（第三迭代已完成：G08–G11）。

## 快速导航

| 入口 | 作用 |
| --- | --- |
| [知识地图总索引.md](知识地图总索引.md) | 🧭 最外层思维导图：Mermaid 图 + 三语言可点击索引 + 28 篇语言覆盖矩阵 + 角色阅读路径 |
| [Agent知识地图.xmind](Agent知识地图.xmind) | XMind 版脑图，可直接打开评审 |
| [Agent知识地图.mm](Agent知识地图.mm) | FreeMind 版脑图，可导入 XMind / FreeMind，便于 diff |
| [知识地图-内容映射与成熟度.md](知识地图-内容映射与成熟度.md) | 现有内容 → 地图节点的映射与成熟度评分 |
| [知识地图-缺口与补全计划.md](知识地图-缺口与补全计划.md) | 缺口清单、P0/P1/P2 补全计划、治理规则 |
| [build_knowledge_map.py](build_knowledge_map.py) | 脑图唯一数据源与生成器：修改结构只改这里 |

## 内容区

| 格式 | 目录 | 说明 |
| --- | --- | --- |
| Markdown 源 | [`markdown/`](markdown/) | Java / Python / TypeScript 三语言版本，Java 为 canonical 原版 |
| LaTeX 源 | [`latex/`](latex/) | 与 Markdown 对应的可编译版本 |
| PDF | [`pdf/`](pdf/) | 已编译 PDF |
| HTML 存档 | [`HTML/`](HTML/) | JavaGuide 原始网页存档与转换资源 |

## 三语言如何体现

1. **知识地图按知识主题组织，不按语言复制整棵树。**
2. 每个节点标注语言策略：`≡` 表示三语言同文（Java canonical，Python / TypeScript 同路径副本）；`Java / Python / TypeScript 实现` 表示语言化代码节点。
3. `知识地图总索引.md` 的可点击索引提供 **Java / Python / TypeScript 三列直达链接**，并附 **28 篇 × 3 语言覆盖矩阵**。
4. XMind / FreeMind / Mermaid 中，10 篇语言化代码文档已展开为三语言叶子；共享文档链接 Java canonical。
5. 新增文档必须先声明语言策略：`shared`（三份同文）或 `code`（三套实现）。

## 当前快照

- 主题数：**28 篇 × 3 语言版本**。
- 第三迭代新增：RAG 高级检索、案例库与反模式索引、Agent 框架选型对比、上下文工程。
- 地图覆盖：171 个叶子节点，🟢 123 / 🟡 35 / 🔴 13，加权覆盖率约 **82%**。
- 已补齐板块：开发与工程化（96%）、架构与运行机制（97%）、评测（88%）、安全（83%）。
- 剩余短板：生态与前沿（22%）、行业方案（待补）、在线 A/B 与基准榜单（待补）。

## 备份与版本

| 标签 | 说明 |
| --- | --- |
| `backup-before-knowledge-map-20260816-081135` | 构建地图前的完整备份 |
| `knowledge-map-review-v0.1` | 知识地图审核版 v0.1 |
| `iteration-1-start` / `iteration-1-complete` | 第一迭代标记 |
| `map-language-aware-v0.3.1` | 三语言地图升级完成 |
| `iteration-2-start` / `iteration-2-complete` | 第二迭代标记 |
| `iteration-3-start` / `iteration-3-complete` | 第三迭代标记 |
