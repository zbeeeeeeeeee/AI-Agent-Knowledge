#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AI Agent 知识地图生成器（单一数据源 -> 多格式输出）。

输出：
  知识地图总索引.md     人工审阅版（Mermaid 图 + 可点击索引表 + 阅读路径）
  知识地图总索引.mmd     Mermaid 源码（VS Code / Obsidian 可直接渲染）
  Agent知识地图.mm       FreeMind 格式（可导入 XMind / FreeMind）
  Agent知识地图.xmind    XMind 工作簿（可直接打开）
"""
import json
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape, quoteattr

STATUS = {
    "nav": ("🧭", "入口/导航"),
    "full": ("🟢", "完整：有理论+方法+实践/案例"),
    "partial": ("🟡", "部分：有内容，但深度或闭环不足"),
    "gap": ("🔴", "空白：需要补全"),
    "later": ("⚪", "暂不建设"),
}

ROOT_TITLE = "AI Agent 知识总索引"


class Node:
    def __init__(self, title, status="nav", link=None, children=None, lang=None):
        self.title = title
        self.status = status
        self.link = link
        self.children = children or []
        self.lang = lang


def N(title, status="nav", link=None, children=None, lang=None):
    return Node(title, status, link, children, lang)


# 相对仓库根目录的权威入口。约定：概念/面试以 Java 版为 canonical，语言化代码按语言链接。
J = "markdown/java"
PY = "markdown/python"
TS = "markdown/typescript"
LANGS = ["java", "python", "typescript"]

# 三种语言策略：
#   shared = 三语言内容完全一致，Java 为 canonical，Python/TS 为同路径副本
#   code   = 同一主题有三套语言化实现，地图显式展开 Java/Python/TypeScript 三个叶子
#   single = 仓库级资源（如顶层 README）
DOC_INVENTORY = [
    ("Agent 术语表与概念边界", "00-概念与术语/01-Agent术语表与概念边界.md", "shared"),
    ("Agent 自主性分级", "00-概念与术语/02-Agent自主性分级.md", "shared"),
    ("LLM 运行机制", "01-LLM基础/01-LLM运行机制.md", "shared"),
    ("大模型结构化输出", "01-LLM基础/02-大模型结构化输出.md", "code"),
    ("Agent 核心概念", "02-Agent/01-Agent核心概念.md", "shared"),
    ("Agent 记忆系统", "02-Agent/02-Agent记忆系统.md", "shared"),
    ("多智能体编排", "02-Agent/03-多智能体编排.md", "shared"),
    ("RAG 基础概念", "03-RAG/01-RAG基础概念.md", "shared"),
    ("RAG 向量索引与向量数据库", "03-RAG/02-RAG向量索引与向量数据库.md", "shared"),
    ("Workflow、Graph 与 Loop", "04-工程实践/01-Workflow-Graph与Loop.md", "code"),
    ("Loop Engineering", "04-工程实践/02-Loop工程.md", "shared"),
    ("Harness Engineering", "04-工程实践/03-Harness工程.md", "shared"),
    ("大模型网关", "04-工程实践/04-大模型网关.md", "code"),
    ("AI 应用系统设计", "07-系统设计/01-AI应用系统设计.md", "code"),
    ("AI Agent 面试题", "10-面试/01-AI-Agent面试题.md", "shared"),
    ("RAG 面试题", "10-面试/02-RAG面试题.md", "shared"),
    ("AI 系统设计面试题", "10-面试/03-AI系统设计面试题.md", "shared"),
    ("AI 应用开发面试指南", "10-面试/04-AI应用开发面试指南.md", "shared"),
    ("大模型基础面试题", "10-面试/05-大模型基础面试题.md", "shared"),
    ("模拟面试题库", "10-面试/06-模拟面试题库.md", "shared"),
]
CODE_DOCS = {rel for _, rel, mode in DOC_INVENTORY if mode == "code"}


def LANG3(title, rel_path, status="full"):
    """为一个 code 类文档生成三个语言实现子节点（标题带主题前缀，保证脑图节点唯一）。"""
    return N(title, "nav", None, [
        N(f"{title} · Java 实现", status, f"{J}/{rel_path}", lang="java"),
        N(f"{title} · Python 实现", status, f"{PY}/{rel_path}", lang="python"),
        N(f"{title} · TypeScript 实现", status, f"{TS}/{rel_path}", lang="typescript"),
    ])


def lang_links(node):
    """返回节点在三种语言下的链接。shared 文档自动展开为三语言同路径链接。"""
    links = {lang: None for lang in LANGS}
    if not node.link:
        return links
    if node.lang == "java":
        return {"java": node.link, "python": None, "typescript": None}
    if node.lang == "python":
        return {"java": None, "python": node.link, "typescript": None}
    if node.lang == "typescript":
        return {"java": None, "python": None, "typescript": node.link}
    if node.link.startswith(f"{J}/"):
        rel = node.link[len(J) + 1:]
        links = {lang: f"markdown/{lang}/{rel}" for lang in LANGS}
    elif node.link.startswith(f"{PY}/"):
        rel = node.link[len(PY) + 1:]
        links = {"python": f"markdown/python/{rel}", "java": f"markdown/java/{rel}", "typescript": f"markdown/typescript/{rel}"}
    elif node.link.startswith(f"{TS}/"):
        rel = node.link[len(TS) + 1:]
        links = {"typescript": f"markdown/typescript/{rel}", "java": f"markdown/java/{rel}", "python": f"markdown/python/{rel}"}
    elif node.link.startswith("pdf/java"):
        links = {"java": "pdf/java", "python": None, "typescript": None}
    elif node.link.startswith("pdf/python"):
        links = {"java": None, "python": "pdf/python", "typescript": None}
    elif node.link.startswith("pdf/typescript"):
        links = {"java": None, "python": None, "typescript": "pdf/typescript"}
    else:
        links = {lang: None for lang in LANGS}
        links["java"] = node.link
    return links


TREE = Node(ROOT_TITLE, "nav", None, [
    N("00 阅读入口", "nav", "markdown/README.md", [
        N("按角色阅读", "nav", None, [
            N("新手入门", "partial", f"{J}/README.md"),
            N("后端工程师", "partial", f"{J}/README.md"),
            N("算法工程师", "partial", f"{J}/02-Agent/01-Agent核心概念.md"),
            N("架构师", "partial", f"{J}/07-系统设计/01-AI应用系统设计.md"),
            N("面试冲刺", "full", f"{J}/10-面试/04-AI应用开发面试指南.md"),
        ]),
        N("按生命周期", "nav", None, [
            N("概念入门", "full", f"{J}/README.md"),
            N("系统开发", "full", f"{J}/04-工程实践/01-Workflow-Graph与Loop.md"),
            N("评测上线", "partial", f"{J}/07-系统设计/01-AI应用系统设计.md"),
            N("运营治理", "partial", f"{J}/04-工程实践/04-大模型网关.md"),
        ]),
        N("按语言阅读", "nav", None, [
            N("Java 版", "nav", None, [
                N("Java 全部文档", "full", f"{J}/README.md", lang="java"),
                N("Java PDF 版", "full", "pdf/java", lang="java"),
            ]),
            N("Python 版", "nav", None, [
                N("Python 全部文档", "full", f"{PY}/README.md", lang="python"),
                N("Python PDF 版", "full", "pdf/python", lang="python"),
            ]),
            N("TypeScript 版", "nav", None, [
                N("TypeScript 全部文档", "full", f"{TS}/README.md", lang="typescript"),
                N("TypeScript PDF 版", "full", "pdf/typescript", lang="typescript"),
            ]),
        ]),
    ]),
    N("01 概念与分类", "partial", f"{J}/02-Agent/01-Agent核心概念.md", [
        N("Agent 定义与边界", "partial", f"{J}/02-Agent/01-Agent核心概念.md", [
            N("Agent 是什么", "full", f"{J}/02-Agent/01-Agent核心概念.md"),
            N("Agent vs Chatbot", "partial", f"{J}/10-面试/06-模拟面试题库.md"),
            N("Agent vs Workflow", "full", f"{J}/02-Agent/01-Agent核心概念.md"),
            N("Agent vs RAG", "partial", f"{J}/02-Agent/02-Agent记忆系统.md"),
        ]),
        N("自主性分级", "full", f"{J}/00-概念与术语/02-Agent自主性分级.md"),
        N("分类体系与范式", "partial", f"{J}/02-Agent/01-Agent核心概念.md", [
            N("ReAct", "full", f"{J}/02-Agent/01-Agent核心概念.md"),
            N("Plan-and-Execute", "full", f"{J}/02-Agent/01-Agent核心概念.md"),
            N("Reflection", "partial", f"{J}/02-Agent/01-Agent核心概念.md"),
            N("Multi-Agent", "partial", f"{J}/02-Agent/01-Agent核心概念.md"),
            N("Agentic Workflows", "full", f"{J}/02-Agent/01-Agent核心概念.md"),
            N("A2A 协议", "partial", f"{J}/02-Agent/01-Agent核心概念.md"),
            N("各范式选型", "full", f"{J}/02-Agent/01-Agent核心概念.md"),
        ]),
        N("术语表", "full", f"{J}/00-概念与术语/01-Agent术语表与概念边界.md"),
    ]),
    N("02 能力模型", "partial", f"{J}/02-Agent/01-Agent核心概念.md", [
        N("感知与输入", "partial", f"{J}/01-LLM基础/01-LLM运行机制.md", [
            N("多模态 Token 化", "partial", f"{J}/01-LLM基础/01-LLM运行机制.md"),
            N("上下文窗口边界", "full", f"{J}/01-LLM基础/01-LLM运行机制.md"),
        ]),
        N("记忆系统", "full", f"{J}/02-Agent/02-Agent记忆系统.md", [
            N("短期记忆", "full", f"{J}/02-Agent/02-Agent记忆系统.md"),
            N("长期记忆", "full", f"{J}/02-Agent/02-Agent记忆系统.md"),
            N("记忆生命周期", "full", f"{J}/02-Agent/02-Agent记忆系统.md"),
            N("记忆检索优化", "full", f"{J}/02-Agent/02-Agent记忆系统.md"),
            N("Markdown 记忆", "full", f"{J}/02-Agent/02-Agent记忆系统.md"),
        ]),
        N("规划与决策", "partial", f"{J}/02-Agent/01-Agent核心概念.md", [
            N("任务分解", "full", f"{J}/02-Agent/01-Agent核心概念.md"),
            N("反思与自评", "partial", f"{J}/02-Agent/01-Agent核心概念.md"),
            N("成本约束决策", "partial", f"{J}/04-工程实践/02-Loop工程.md"),
        ]),
        N("工具使用与行动", "full", f"{J}/01-LLM基础/02-大模型结构化输出.md", [
            N("Function Calling", "full", f"{J}/01-LLM基础/02-大模型结构化输出.md"),
            N("Tools 注册与 Schema", "full", f"{J}/02-Agent/01-Agent核心概念.md"),
            N("MCP 工具接入", "partial", f"{J}/02-Agent/01-Agent核心概念.md"),
            N("Agent Skills", "partial", f"{J}/02-Agent/01-Agent核心概念.md"),
        ]),
        N("协作与沟通", "partial", f"{J}/02-Agent/01-Agent核心概念.md", [
            N("多智能体协作", "full", f"{J}/02-Agent/03-多智能体编排.md"),
            N("A2A 通信", "partial", f"{J}/02-Agent/01-Agent核心概念.md"),
        ]),
    ]),
    N("03 架构与运行机制", "partial", f"{J}/02-Agent/01-Agent核心概念.md", [
        N("单 Agent 运行循环", "full", f"{J}/02-Agent/01-Agent核心概念.md", [
            N("Agent Loop", "full", f"{J}/02-Agent/01-Agent核心概念.md"),
            N("最小三层架构", "full", f"{J}/02-Agent/01-Agent核心概念.md"),
        ]),
        N("上下文与提示词架构", "partial", f"{J}/04-工程实践/03-Harness工程.md", [
            N("Prompt Engineering", "full", f"{J}/02-Agent/01-Agent核心概念.md"),
            N("Context Engineering", "full", f"{J}/02-Agent/01-Agent核心概念.md"),
            N("上下文利用 40% 现象", "full", f"{J}/04-工程实践/03-Harness工程.md"),
        ]),
        N("工作流编排", "full", f"{J}/04-工程实践/01-Workflow-Graph与Loop.md", [
            N("Workflow", "full", f"{J}/04-工程实践/01-Workflow-Graph与Loop.md"),
            N("Graph", "full", f"{J}/04-工程实践/01-Workflow-Graph与Loop.md"),
            N("Loop", "full", f"{J}/04-工程实践/01-Workflow-Graph与Loop.md"),
            N("框架概念对照", "full", f"{J}/04-工程实践/01-Workflow-Graph与Loop.md"),
            LANG3("Workflow 三语言实现", "04-工程实践/01-Workflow-Graph与Loop.md"),
        ]),
        N("模型接入层", "full", f"{J}/04-工程实践/04-大模型网关.md", [
            N("LLM 运行机制", "full", f"{J}/01-LLM基础/01-LLM运行机制.md"),
            LANG3("结构化输出", "01-LLM基础/02-大模型结构化输出.md"),
            N("大模型网关", "full", f"{J}/04-工程实践/04-大模型网关.md"),
            N("路由与 Fallback", "full", f"{J}/04-工程实践/04-大模型网关.md"),
        ]),
        N("检索架构 RAG", "full", f"{J}/03-RAG/01-RAG基础概念.md", [
            N("RAG 基础", "full", f"{J}/03-RAG/01-RAG基础概念.md"),
            N("Embedding", "full", f"{J}/03-RAG/01-RAG基础概念.md"),
            N("向量索引算法", "full", f"{J}/03-RAG/02-RAG向量索引与向量数据库.md"),
            N("向量数据库选型", "full", f"{J}/03-RAG/02-RAG向量索引与向量数据库.md"),
        ]),
        N("Harness 工程", "full", f"{J}/04-工程实践/03-Harness工程.md", [
            N("六层架构", "full", f"{J}/04-工程实践/03-Harness工程.md"),
            N("一线团队案例", "full", f"{J}/04-工程实践/03-Harness工程.md"),
        ]),
        N("多智能体编排", "full", f"{J}/02-Agent/03-多智能体编排.md", [
            N("编排模式", "full", f"{J}/02-Agent/03-多智能体编排.md"),
            N("通信协议", "partial", f"{J}/02-Agent/03-多智能体编排.md"),
        ]),
    ]),
    N("04 开发与工程化", "partial", f"{J}/07-系统设计/01-AI应用系统设计.md", [
        N("技术选型与框架", "partial", f"{J}/README.md", [
            N("Java 技术栈", "full", f"{J}/README.md", lang="java"),
            N("Python 技术栈", "full", f"{PY}/README.md", lang="python"),
            N("TypeScript 技术栈", "full", f"{TS}/README.md", lang="typescript"),
            N("框架与平台对比", "gap"),
        ]),
        N("设计模式与范式", "full", f"{J}/04-工程实践/01-Workflow-Graph与Loop.md", [
            N("Workflow Graph Loop", "full", f"{J}/04-工程实践/01-Workflow-Graph与Loop.md"),
            N("Loop Engineering", "full", f"{J}/04-工程实践/02-Loop工程.md"),
            N("Harness Engineering", "full", f"{J}/04-工程实践/03-Harness工程.md"),
        ]),
        N("上下文工程", "partial", f"{J}/07-系统设计/01-AI应用系统设计.md", [
            N("Prompt 版本化", "partial", f"{J}/07-系统设计/01-AI应用系统设计.md"),
            N("RAG 与 Memory 边界", "full", f"{J}/02-Agent/02-Agent记忆系统.md"),
            N("Token 预算与上下文压缩", "partial", f"{J}/07-系统设计/01-AI应用系统设计.md"),
        ]),
        N("系统设计", "full", f"{J}/07-系统设计/01-AI应用系统设计.md", [
            N("生产级分层架构", "full", f"{J}/07-系统设计/01-AI应用系统设计.md"),
            N("同步 流式 异步模式", "full", f"{J}/07-系统设计/01-AI应用系统设计.md"),
            N("工具调用与权限模型", "full", f"{J}/07-系统设计/01-AI应用系统设计.md"),
            LANG3("系统设计三语言接口实现", "07-系统设计/01-AI应用系统设计.md"),
        ]),
        N("网关与基础设施", "full", f"{J}/04-工程实践/04-大模型网关.md", [
            N("多模型统一接入", "full", f"{J}/04-工程实践/04-大模型网关.md"),
            N("限流与配额", "full", f"{J}/04-工程实践/04-大模型网关.md"),
            N("成本统计与预算", "full", f"{J}/04-工程实践/04-大模型网关.md"),
            N("缓存与语义缓存", "partial", f"{J}/04-工程实践/04-大模型网关.md"),
            LANG3("网关三语言实现", "04-工程实践/04-大模型网关.md"),
        ]),
        N("部署与发布", "gap", None, [
            N("部署形态", "gap"),
            N("版本与回滚", "gap"),
            N("容量与扩展", "gap"),
        ]),
        N("可观测与调试", "partial", f"{J}/04-工程实践/04-大模型网关.md", [
            N("Trace 记录", "partial", f"{J}/07-系统设计/01-AI应用系统设计.md"),
            N("日志与回放", "gap"),
            N("调试工具链", "gap"),
        ]),
    ]),
    N("05 评测与质量", "gap", f"{J}/07-系统设计/01-AI应用系统设计.md", [
        N("指标体系", "partial", f"{J}/07-系统设计/01-AI应用系统设计.md", [
            N("任务成功率", "gap"),
            N("轨迹质量", "gap"),
            N("工具调用准确率", "gap"),
            N("延迟与成本", "partial", f"{J}/04-工程实践/04-大模型网关.md"),
        ]),
        N("评测方法", "partial", f"{J}/07-系统设计/01-AI应用系统设计.md", [
            N("离线评测集", "gap"),
            N("人工评测", "gap"),
            N("在线 A B 实验", "gap"),
            N("LLM-as-Judge", "gap"),
        ]),
        N("评测基座与回归", "gap", None, [
            N("评测集构建", "gap"),
            N("基准与榜单", "gap"),
            N("回归与 CI", "gap"),
        ]),
        N("持续改进", "partial", f"{J}/04-工程实践/03-Harness工程.md", [
            N("Human-in-the-Loop", "partial", f"{J}/07-系统设计/01-AI应用系统设计.md"),
            N("反馈闭环", "partial", f"{J}/04-工程实践/03-Harness工程.md"),
        ]),
    ]),
    N("06 安全与治理", "partial", f"{J}/07-系统设计/01-AI应用系统设计.md", [
        N("风险分类", "partial", f"{J}/07-系统设计/01-AI应用系统设计.md", [
            N("模型风险", "partial", f"{J}/07-系统设计/01-AI应用系统设计.md"),
            N("工具风险", "partial", f"{J}/07-系统设计/01-AI应用系统设计.md"),
            N("数据风险", "partial", f"{J}/07-系统设计/01-AI应用系统设计.md"),
        ]),
        N("护栏机制", "partial", f"{J}/07-系统设计/01-AI应用系统设计.md", [
            N("权限最小化", "partial", f"{J}/07-系统设计/01-AI应用系统设计.md"),
            N("沙箱执行", "gap"),
            N("Prompt 注入防护", "gap"),
            N("内容安全", "gap"),
        ]),
        N("合规与审计", "partial", f"{J}/04-工程实践/04-大模型网关.md", [
            N("隐私与数据边界", "partial", f"{J}/07-系统设计/01-AI应用系统设计.md"),
            N("审计日志", "partial", f"{J}/04-工程实践/04-大模型网关.md"),
            N("第三方模型数据边界", "partial", f"{J}/07-系统设计/01-AI应用系统设计.md"),
        ]),
        N("责任与流程", "gap", None, [
            N("审批流程", "gap"),
            N("责任归属", "gap"),
        ]),
    ]),
    N("07 应用与案例", "partial", f"{J}/04-工程实践/03-Harness工程.md", [
        N("选型决策", "partial", f"{J}/02-Agent/01-Agent核心概念.md", [
            N("是否用 Agent 决策树", "partial", f"{J}/02-Agent/01-Agent核心概念.md"),
            N("Workflow vs Agent", "full", f"{J}/02-Agent/01-Agent核心概念.md"),
        ]),
        N("场景模式库", "partial", f"{J}/04-工程实践/03-Harness工程.md", [
            N("编码 Agent", "partial", f"{J}/04-工程实践/03-Harness工程.md"),
            N("客服 Agent", "gap"),
            N("数据分析 Agent", "gap"),
            N("办公自动化 Agent", "gap"),
        ]),
        N("行业解决方案", "gap", None, [
            N("金融", "gap"),
            N("医疗", "gap"),
            N("电商", "gap"),
            N("企业服务", "gap"),
        ]),
        N("案例库", "partial", f"{J}/04-工程实践/03-Harness工程.md", [
            N("OpenAI 三人团队", "full", f"{J}/04-工程实践/03-Harness工程.md"),
            N("Anthropic 三智能体", "full", f"{J}/04-工程实践/03-Harness工程.md"),
            N("Stripe 每周 1300 PR", "full", f"{J}/04-工程实践/03-Harness工程.md"),
            N("失败案例与反模式", "partial", f"{J}/04-工程实践/02-Loop工程.md"),
        ]),
    ]),
    N("08 生态与前沿", "gap", f"{J}/02-Agent/01-Agent核心概念.md", [
        N("协议与标准", "partial", f"{J}/02-Agent/01-Agent核心概念.md", [
            N("MCP 标准", "partial", f"{J}/02-Agent/01-Agent核心概念.md"),
            N("A2A 标准", "partial", f"{J}/02-Agent/01-Agent核心概念.md"),
            N("Skills 标准", "partial", f"{J}/02-Agent/01-Agent核心概念.md"),
        ]),
        N("技术雷达", "gap", None, [
            N("论文清单", "gap"),
            N("框架动态", "gap"),
            N("产品平台动态", "gap"),
        ]),
        N("趋势判断", "gap", None, [
            N("Harness 趋势", "partial", f"{J}/04-工程实践/03-Harness工程.md"),
            N("多智能体趋势", "gap"),
            N("评测与治理趋势", "gap"),
        ]),
    ]),
])


def display_title(node):
    if node.status == "nav":
        return node.title
    emoji = STATUS[node.status][0]
    title = f"{emoji} {node.title}"
    if node.link and node.link.startswith(f"{J}/") and node.lang is None:
        title += " ≡"
    return title


def iter_leaves(node, path=()):
    p = path + (node.title,)
    if node.children:
        for c in node.children:
            yield from iter_leaves(c, p)
    else:
        yield p, node


def render_mermaid():
    lines = ["mindmap", f"  root(({ROOT_TITLE}))"]

    def walk(node, depth):
        prefix = "  " * (depth + 1)
        title = display_title(node).replace("  ", " ")
        lines.append(prefix + title)
        for c in node.children:
            walk(c, depth + 1)

    for c in TREE.children:
        walk(c, 1)
    return "\n".join(lines) + "\n"


def render_freemind():
    def walk(node, depth):
        title = escape(display_title(node))
        attrs = f" TEXT={quoteattr(title)}"
        if node.link:
            attrs += f" LINK={quoteattr(node.link)}"
        indent = "  " * depth
        if node.children:
            lines.append(f"{indent}<node{attrs}>")
            for c in node.children:
                walk(c, depth + 1)
            lines.append(f"{indent}</node>")
        else:
            lines.append(f"{indent}<node{attrs}/>")

    lines = ['<map version="1.0.1">']
    lines.append(f'<node TEXT={quoteattr(ROOT_TITLE)}>')
    for c in TREE.children:
        walk(c, 1)
    lines.append("</node>")
    lines.append("</map>")
    return "\n".join(lines) + "\n"


def render_xmind_topics():
    uid = {"i": 0}

    def walk(node):
        uid["i"] += 1
        topic = {
            "id": f"topic-{uid['i']}",
            "class": "topic",
            "title": display_title(node),
        }
        if node.link:
            topic["href"] = node.link
        if node.children:
            topic["children"] = {"attached": [walk(c) for c in node.children]}
        return topic

    root = {
        "id": "topic-root",
        "class": "topic",
        "title": ROOT_TITLE,
        "children": {"attached": [walk(c) for c in TREE.children]},
    }
    return [{
        "id": "sheet-1",
        "class": "sheet",
        "title": ROOT_TITLE,
        "rootTopic": root,
    }]


def write_xmind(path):
    content = json.dumps(render_xmind_topics(), ensure_ascii=False, indent=2)
    metadata = json.dumps({"creator": {"name": "AI Agent Knowledge Base", "version": "0.3.0"}}, ensure_ascii=False, indent=2)
    manifest = json.dumps({"file-entries": {"content.json": {}, "metadata.json": {}}}, ensure_ascii=False, indent=2)
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("manifest.json", manifest)
        z.writestr("metadata.json", metadata)
        z.writestr("content.json", content)


def render_index_md():
    lines = []
    lines.append("# AI Agent 知识总索引（三语言版 v0.3）")
    lines.append("")
    lines.append("> 本文件是知识库的**最外层索引**：脑图负责导航，文档负责承载内容，状态标识负责暴露缺口，语言矩阵负责三语言直达。")
    lines.append("> 由 `build_knowledge_map.py` 生成；修改结构请改脚本后重新生成，避免图与文档漂移。")
    lines.append("")
    lines.append("## 0. 图例与语言策略")
    lines.append("")
    lines.append("| 标识 | 含义 |")
    lines.append("| --- | --- |")
    for key in ("full", "partial", "gap", "later", "nav"):
        emoji, desc = STATUS[key]
        lines.append(f"| {emoji} | {desc} |")
    lines.append("| ≡ | 三语言内容一致：Java 为 canonical，Python / TypeScript 为同路径副本，索引表中三列均可直达 |")
    lines.append("| Java / Python / TypeScript 实现 | 同一主题有 4 篇语言化代码文档，在地图中显式展开为三个语言叶子 |")
    lines.append("")
    lines.append("**语言组织原则**：知识地图按“知识主题”组织，不按语言复制整棵树。每个节点的语言策略只有三类：`shared` 三语言同文、`code` 三语言实现、`single` 仓库级资源。")
    lines.append("")
    lines.append("## 1. 思维导图总图")
    lines.append("")
    lines.append("```mermaid")
    lines.append(render_mermaid().rstrip())
    lines.append("```")
    lines.append("")
    lines.append("> 同一个脑图还提供：`Agent知识地图.xmind`（XMind 直接打开）、`Agent知识地图.mm`（FreeMind / XMind 导入）、`知识地图总索引.mmd`（Mermaid 源码）。")
    lines.append("")
    lines.append("## 2. 可点击索引（三语言链接）")
    lines.append("")
    lines.append("约定：Java 为 canonical；所有存在的语言副本均给出直接链接；`code` 类文档已在脑图中展开为三个实现节点。")
    lines.append("")
    lines.append("| 节点路径 | 状态 | Java | Python | TypeScript |")
    lines.append("| --- | --- | --- | --- | --- |")
    for path, node in iter_leaves(TREE):
        title = " / ".join(path)
        emoji, desc = STATUS[node.status]
        links = lang_links(node)
        cells = []
        for lang in LANGS:
            link = links.get(lang)
            lang_label = {"java": "Java", "python": "Python", "typescript": "TypeScript"}[lang]
            if link:
                cells.append(f"[{lang_label}]({link})")
            else:
                cells.append("—")
        lines.append(f"| {title} | {emoji} {desc} | " + " | ".join(cells) + " |")
    lines.append("")
    lines.append("## 3. 语言覆盖矩阵（20 篇 × 3 语言）")
    lines.append("")
    lines.append("| # | 文档 | 语言策略 | Java | Python | TypeScript |")
    lines.append("| --- | --- | --- | --- | --- | --- |")
    for i, (doc_title, rel, mode) in enumerate(DOC_INVENTORY, 1):
        if mode == "code":
            strategy = "code：三套语言化实现"
        else:
            strategy = "shared：三语言同文"
        links = [f"[{lang}](markdown/{lang}/{rel})" for lang in LANGS]
        lines.append(f"| {i} | {doc_title} | {strategy} | " + " | ".join(links) + " |")
    lines.append("")
    lines.append("> 使用建议：阅读概念看任意一版即可（推荐 Java canonical）；写代码直接点自己技术栈对应的列。")
    lines.append("")
    lines.append("## 4. 四类阅读入口")
    lines.append("")
    lines.append("| 角色 | 建议路径 | 终点 |")
    lines.append("| --- | --- | --- |")
    lines.append(f"| 新手入门 | [01-LLM基础]({J}/01-LLM基础/01-LLM运行机制.md) → [02-Agent]({J}/02-Agent/01-Agent核心概念.md) → [03-RAG]({J}/03-RAG/01-RAG基础概念.md) | 建立完整概念地图 |")
    lines.append(f"| 后端开发 | 新手路径 → [04-工程实践]({J}/04-工程实践/01-Workflow-Graph与Loop.md) → [07-系统设计]({J}/07-系统设计/01-AI应用系统设计.md) | 能落地生产级 Agent 服务 |")
    lines.append(f"| 架构师 | [03 架构与运行机制]({J}/02-Agent/01-Agent核心概念.md) → [04 网关]({J}/04-工程实践/04-大模型网关.md) → [07 系统设计]({J}/07-系统设计/01-AI应用系统设计.md) | 能设计、拆解、治理 AI 系统 |")
    lines.append(f"| 面试冲刺 | [AI 应用开发面试指南]({J}/10-面试/04-AI应用开发面试指南.md) → 6 份面试题 → [模拟题库]({J}/10-面试/06-模拟面试题库.md) | 能结构化答题 |")
    lines.append("")
    lines.append("## 5. 现状速览")
    lines.append("")
    lines.append("**已有强项**：LLM 运行机制、结构化输出、Agent Loop、记忆系统、RAG 基础与向量检索、Workflow/Graph/Loop、Harness、网关、系统设计。")
    lines.append("")
    lines.append("**本轮已补齐**：术语表、自主性分级、多智能体编排；地图已升级为三语言视图。\n\n**主要缺口**：部署与可观测专项、评测体系、安全护栏专项、行业案例库、生态技术雷达。")
    lines.append("")
    lines.append("详见 [`知识地图-内容映射与成熟度.md`](知识地图-内容映射与成熟度.md) 与 [`知识地图-缺口与补全计划.md`](知识地图-缺口与补全计划.md)。")
    return "\n".join(lines) + "\n"


def main():
    root = Path(__file__).resolve().parent
    (root / "知识地图总索引.md").write_text(render_index_md(), encoding="utf-8")
    (root / "知识地图总索引.mmd").write_text(render_mermaid(), encoding="utf-8")
    (root / "Agent知识地图.mm").write_text(render_freemind(), encoding="utf-8")
    write_xmind(root / "Agent知识地图.xmind")
    print("generated:")
    for name in ("知识地图总索引.md", "知识地图总索引.mmd", "Agent知识地图.mm", "Agent知识地图.xmind"):
        print(f"  {name}: { (root / name).stat().st_size } bytes")


if __name__ == "__main__":
    main()
