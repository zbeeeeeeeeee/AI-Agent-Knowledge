# AI Agent 知识库

> 最外层入口：先看[**知识地图总索引**](知识地图总索引.md)，再进入具体文档。
> 当前版本：**知识地图三语言版 v0.3**（第一迭代已完成；地图已支持 Java / Python / TypeScript 三语言视图）。

## 快速导航

| 入口 | 作用 |
| --- | --- |
| [知识地图总索引.md](知识地图总索引.md) | 🧭 最外层思维导图：Mermaid 图 + 三语言可点击索引 + 语言覆盖矩阵 + 角色阅读路径 |
| [Agent知识地图.xmind](Agent知识地图.xmind) | XMind 版脑图，可直接打开评审 |
| [Agent知识地图.mm](Agent知识地图.mm) | FreeMind 版脑图，可导入 XMind / FreeMind，便于 diff |
| [知识地图-内容映射与成熟度.md](知识地图-内容映射与成熟度.md) | 现有内容 → 地图节点的映射与成熟度评分 |
| [知识地图-缺口与补全计划.md](知识地图-缺口与补全计划.md) | 🔴/🟡 缺口清单、P0/P1/P2 补全计划、治理规则 |
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
3. `知识地图总索引.md` 的可点击索引提供 **Java / Python / TypeScript 三列直达链接**，并附 **20 篇 × 3 语言覆盖矩阵**。
4. XMind / FreeMind / Mermaid 中，4 篇语言化代码文档已展开为三个语言叶子；共享文档链接 Java canonical。
5. 新增文档必须先声明语言策略：`shared`（三份同文）或 `code`（三套实现）。

## 当前快照

- 主题数：**20 篇 × 3 语言版本**；含代码文档按 Java / Python / TypeScript 分别实现。
- 第一迭代新增：Agent 术语表与概念边界、Agent 自主性分级、多智能体编排。
- 目录结构已重排为：`00-概念与术语` → `01-LLM基础` → `02-Agent` → `03-RAG` → `04-工程实践` → `05-评测与质量` → `06-安全与治理` → `07-系统设计` → `08-应用与案例` → `09-生态与前沿` → `10-面试`。
- 地图覆盖：134 个叶子节点，🟢 62 / 🟡 39 / 🔴 33，加权覆盖率约 **61%**。
- 最强板块：架构与运行机制（98%）、能力模型（81%）、概念与分类（81%）。
- 最弱板块：评测与质量（12%）、生态与前沿（22%）、安全与治理（29%）。

## 备份与版本

| 标签 | 说明 |
| --- | --- |
| `backup-before-knowledge-map-20260816-081135` | 构建地图前的完整备份 |
| `knowledge-map-review-v0.1` | 知识地图审核版 v0.1 |
| `iteration-1-start` | 第一迭代开始前的标记 |
| `iteration-1-complete` | 第一迭代完成后的标记 |
| `map-language-aware-v0.3.1` | 三语言地图升级完成（含语言叶子归属精修） |

> 远程推送需要本机配置 Gitee 凭证，命令：`git push origin master --tags`。
