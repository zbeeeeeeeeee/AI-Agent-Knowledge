# AI Agent 知识库

> 最外层入口：先看[**知识地图总索引**](知识地图总索引.md)，再进入具体文档。
> 当前版本：**知识地图审核版 v0.1**（结构待审核，内容待按缺口计划补全）。

## 快速导航

| 入口 | 作用 |
| --- | --- |
| [知识地图总索引.md](知识地图总索引.md) | 🧭 最外层思维导图：Mermaid 图 + 可点击节点索引 + 角色阅读路径 |
| [Agent知识地图.xmind](Agent知识地图.xmind) | XMind 版脑图，可直接打开评审 |
| [Agent知识地图.mm](Agent知识地图.mm) | FreeMind 版脑图，可导入 XMind / FreeMind，便于 diff |
| [知识地图-内容映射与成熟度.md](知识地图-内容映射与成熟度.md) | 现有 17 篇内容 → 新地图节点的映射与成熟度评分 |
| [知识地图-缺口与补全计划.md](知识地图-缺口与补全计划.md) | 🔴/🟡 缺口清单、P0/P1/P2 补全计划、治理规则 |
| [build_knowledge_map.py](build_knowledge_map.py) | 脑图唯一数据源与生成器：修改结构只改这里 |

## 内容区

| 格式 | 目录 | 说明 |
| --- | --- | --- |
| Markdown 源 | [`markdown/`](markdown/) | Java / Python / TypeScript 三语言版本，Java 为 canonical 原版 |
| LaTeX 源 | [`latex/`](latex/) | 与 Markdown 对应的可编译版本 |
| PDF | [`pdf/`](pdf/) | 已编译 PDF |
| HTML 存档 | [`HTML/`](HTML/) | JavaGuide 原始网页存档与转换资源 |

## 当前快照

- 主题数：17 篇 × 3 语言版本；含代码文档按 Java / Python / TypeScript 分别实现。
- 地图覆盖：134 个叶子节点，🟢 58 / 🟡 40 / 🔴 36，加权覆盖率约 **58%**。
- 最强板块：架构与运行机制、工程实践、记忆与工具使用。
- 最弱板块：评测与质量（12%）、安全与治理（29%）、生态与前沿（22%）。

## 备份

- 构建地图前的备份提交：`9845e7a`
- 备份标签：`backup-before-knowledge-map-20260816-081135`
- 远程推送未执行成功（本机无 Gitee 凭证）；配置凭证后可执行 `git push origin master --tags`。
