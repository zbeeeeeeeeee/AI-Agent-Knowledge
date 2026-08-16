#!/usr/bin/env python3
"""
Convert JavaGuide VuePress HTML files to clean Markdown.
Extracts .vp-page content, removes navigation/sidebar chrome,
preserves tables, code blocks, images.
"""

import os
import re
import sys
from html import unescape
from pathlib import Path
from bs4 import BeautifulSoup, Tag
from markdownify import markdownify as md


BASE_DIR = Path("/home/zhang/demos/latex_demos/Agent知识")
HTML_DIR = BASE_DIR / "HTML"
OUTPUT_DIR = BASE_DIR / "markdown"

# Category mapping: filename keyword -> category dir
CATEGORY_MAP = [
    ("01-LLM基础", [
        "LLM 运行机制",
        "大模型结构化输出",
    ]),
    ("02-Agent", [
        "AI Agent 核心概念",
        "AI Agent 记忆系统",
    ]),
    ("03-RAG", [
        "RAG 基础概念",
        "RAG 向量索引算法",
    ]),
    ("04-工程实践", [
        "Loop Engineering",
        "Harness Engineering",
        "大模型网关",
        "AI 工作流中的 Workflow",
    ]),
    ("05-系统设计", [
        "AI 应用系统设计",
        "AI 系统设计面试题",
    ]),
    ("06-面试", [
        "AI Agent 面试题",
        "RAG 面试题",
        "大模型基础面试题",
        "AI 应用开发面试指南",
    ]),
]

# Site chrome selectors to remove (element AND all its content)
REMOVE_SELECTORS = [
    ".vp-skip-link",
    ".vp-navbar",
    ".vp-sidebar",
    ".vp-toc",
    ".vp-footer",
    ".page-meta",
    ".page-info",
    ".breadcrumb",
    ".edit-link",
    ".prev-next",
    ".vp-copy-code-button",
    "button.vp-copy-code-button",
    "style",
    "script",
    "link",
    ".vp-project-home",
    ".iconify-icon",
]

# Links to strip href from but keep text content
STRIP_HREF_PATTERNS = [
    "javaguide.cn",
    "zhuanlan.zhihu.com",
    "xiaobot.net",
    "mp.weixin.qq.com",
]

# Images to skip (site chrome, not article content)
SKIP_IMG_PATTERNS = [
    r"logo\.(png|svg|webp)",
    r"interview-guide-banner",
    r"favicon",
    r"icon-",
]


def get_output_filename(html_filename):
    """Derive clean markdown filename from HTML filename."""
    name = html_filename.replace(".html", "").strip()
    # Remove trailing " _ JavaGuide" etc.
    name = re.sub(r"\s*_\s*JavaGuide$", "", name)
    return name + ".md"


def get_category(html_filename):
    for cat_dir, keywords in CATEGORY_MAP:
        for kw in keywords:
            if kw in html_filename:
                return cat_dir
    return "06-其他"


def fix_image_path(img_src, html_filename, html_dir):
    """Convert image src to relative path from markdown output dir."""
    if not img_src or img_src.startswith("data:") or img_src.startswith("http"):
        return img_src

    # Already a resolved relative path (e.g. generated Mermaid diagrams).
    if img_src.startswith("../"):
        return img_src

    # Clean up leading ./ or /
    img_src = img_src.lstrip("./")

    # The image is relative to HTML_DIR
    # markdown file will be in OUTPUT_DIR/<lang>/category/xxx.md
    # So path should be: ../../../HTML/xxx.jpg
    return f"../../../HTML/{img_src}"


def should_skip_image(img_src):
    for pattern in SKIP_IMG_PATTERNS:
        if re.search(pattern, img_src, re.IGNORECASE):
            return True
    return False


def clean_element(elem):
    """Remove unwanted child elements from a BeautifulSoup element."""
    if elem is None:
        return

    # Step 1: Remove unwanted elements entirely (BEFORE stripping links)
    for selector in REMOVE_SELECTORS:
        selector_simple = selector.split("[")[0].lstrip(".")
        if selector.startswith("."):
            for child in elem.find_all(class_=selector_simple):
                child.decompose()

    # Also remove page-info, page-meta, breadcrumb, page-nav, hint
    for cls_name in ["page-info", "page-meta", "breadcrumb", "vp-page-nav", "vp-meta-item", "git-info", "hint"]:
        for child in elem.find_all(class_=cls_name):
            child.decompose()

    # Step 2: Strip href from external/self-referencing links, keep the text
    for a in elem.find_all("a", href=True):
        href = a.get("href", "")
        for pattern in STRIP_HREF_PATTERNS:
            if pattern in href:
                a.unwrap()
                break

    # Remove header anchors
    for child in elem.find_all(class_="header-anchor"):
        child.decompose()
    for child in elem.find_all("button", class_="vp-copy-code-button"):
        child.decompose()
    # Remove line-numbers divs from code blocks
    for child in elem.find_all(class_="line-numbers"):
        child.decompose()
    # Remove styles and scripts inside content
    for tag_name in ["style", "script", "link"]:
        for child in elem.find_all(tag_name):
            child.decompose()
    # Remove empty elements
    for child in elem.find_all():
        if child.name not in ("img", "br", "hr", "input") and not child.get_text(strip=True) and not child.find_all("img"):
            if child.find_parent() is not None:
                child.decompose()


# Languages that should become a bare code fence (no highlighting)
NORMALIZE_LANG = {
    "text": "",
    "plaintext": "",
    "plain": "",
    "markdown": "",
    "md": "",
    "": "",
}


def code_language_callback(pre_el):
    """Recover the code language for markdownify.

    JavaGuide/VuePress (Shiki) put the ``language-xxx`` class on the wrapping
    ``<div class="language-json">`` and the ``<code class="language-json">``,
    while ``<pre>`` only carries ``class="shiki"``. Inspect all of them.
    """
    candidates = []
    code = pre_el.find("code")
    if code is not None:
        candidates.append(code)
    candidates.append(pre_el)
    if pre_el.parent is not None:
        candidates.append(pre_el.parent)

    for el in candidates:
        for cls in (el.get("class") or []):
            if cls.startswith("language-"):
                lang = cls[len("language-"):].strip().lower()
                return NORMALIZE_LANG.get(lang, lang)

    parent = pre_el.parent
    if parent is not None and parent.get("data-ext"):
        lang = parent.get("data-ext").strip().lower()
        return NORMALIZE_LANG.get(lang, lang)

    return ""


def _xml_escape(text):
    return (text.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;"))


def _text_units(s):
    """Rough visual width in 'ascii units' (CJK counts as 2)."""
    return sum(2 if ord(c) > 0x2E7F else 1 for c in s)


def _wrap_units(text, budget):
    """Greedy word/char wrap so each line fits within `budget` ascii units."""
    lines = []
    cur = ""
    for word in text.split(" "):
        cand = (cur + " " + word).strip() if cur else word
        if cur and _text_units(cand) > budget:
            lines.append(cur)
            cur = word
        else:
            cur = cand
        while _text_units(cur) > budget and len(cur) > 1:
            acc = 0
            idx = 0
            for i, c in enumerate(cur):
                acc += 2 if ord(c) > 0x2E7F else 1
                if acc > budget:
                    idx = i
                    break
            if idx <= 0:
                break
            lines.append(cur[:idx])
            cur = cur[idx:]
    if cur:
        lines.append(cur)
    return lines or [""]


def _foreignobject_to_text(match):
    """Convert a Mermaid <foreignobject> HTML label into an SVG <text> element.

    cairosvg cannot render foreignObject/HTML, so labels vanish. We recover the
    text, size the font to the label box and center it (multi-line aware).
    """
    try:
        w = float(match.group(1) or 0)
        h = float(match.group(2) or 0)
    except ValueError:
        return ""
    inner = match.group(3)
    inner = re.sub(r"<br\s*/?>", "\n", inner, flags=re.IGNORECASE)
    paras = re.findall(r"<p\b[^>]*>(.*?)</p>", inner, re.DOTALL)
    raw = "\n".join(paras) if paras else inner
    text = unescape(re.sub(r"<[^>]+>", "", raw)).strip()
    if not text or w <= 0 or h <= 0:
        return ""

    segments = [s for s in text.split("\n") if s.strip()]
    if len(segments) > 1:
        lines = segments
    else:
        nlines = max(1, int(round(h / 25.6)))
        if nlines == 1:
            lines = [text]
        else:
            budget = max(4, _text_units(text) / nlines + 1)
            lines = _wrap_units(text, budget)

    n = len(lines)
    lineheight = h / n if n else h
    fontsize = max(9.0, min(15.0, lineheight * 0.72))
    cx = w / 2.0
    top = h / 2.0 - (n - 1) * lineheight / 2.0
    tspans = "".join(
        '<tspan x="%.2f" y="%.2f">%s</tspan>' % (cx, top + i * lineheight, _xml_escape(ln))
        for i, ln in enumerate(lines)
    )
    # Use an inline style so it beats Mermaid's embedded id-selector CSS
    # (e.g. "#v-3{fill:#ccc;font-family:trebuchet ms}") which would otherwise
    # win over presentation attributes and hide the label / break CJK glyphs.
    style = ("fill:#1f2937;font-family:'Source Han Sans SC',sans-serif;"
             "font-size:%.1fpx" % fontsize)
    return (
        '<text text-anchor="middle" dominant-baseline="central" '
        'style="%s">%s</text>' % (style, tspans)
    )


def mermaid_to_standalone(svg_raw):
    """Turn an inline Mermaid <svg> into a standalone, cairosvg-friendly SVG."""
    svg = re.sub(
        r'<foreignobject\b[^>]*?width="([^"]*)"[^>]*?height="([^"]*)"[^>]*>(.*?)</foreignobject>',
        _foreignobject_to_text,
        svg_raw,
        flags=re.DOTALL | re.IGNORECASE,
    )
    # Drop any remaining foreignObject (empty edge labels etc.)
    svg = re.sub(r"<foreignobject\b[^>]*>.*?</foreignobject>", "", svg,
                 flags=re.DOTALL | re.IGNORECASE)
    return svg


def save_mermaid_svgs(html_content, files_dir_name):
    """Extract inline Mermaid diagrams, write standalone .svg files.

    Files are written under ``HTML/_mermaid/<files_dir_name>/`` (a writable,
    tool-generated location) rather than next to the read-only saved page
    assets. Returns a mapping of svg id -> saved filename.
    """
    result = {}
    for m in re.finditer(r"<svg\b[^>]*>", html_content):
        open_tag = m.group(0)
        if "graphics-document" not in open_tag and "flowchart" not in open_tag:
            continue
        id_m = re.search(r'id="([^"]+)"', open_tag)
        if not id_m:
            continue
        sid = id_m.group(1)
        end = html_content.find("</svg>", m.end())
        if end == -1:
            continue
        end += len("</svg>")
        svg_clean = mermaid_to_standalone(html_content[m.start():end])
        fname = f"mermaid-{sid}.svg"
        out_path = HTML_DIR / "_mermaid" / files_dir_name / fname
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(svg_clean)
        result[sid] = fname
    return result


def process_html_file(html_path, html_filename):
    """Process a single HTML file and return markdown text."""
    with open(html_path, "r", encoding="utf-8", errors="replace") as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, "html.parser")

    # Find the main content area (<main class="vp-page">)
    vp_page = soup.find("main", class_="vp-page")
    if vp_page is None:
        # Fallback: try div
        vp_page = soup.find("div", class_="vp-page")
    if vp_page is None:
        print(f"  WARNING: No .vp-page found in {html_filename}")
        return None

    # Remove Skip Link if at top
    skip_link = vp_page.find("a", class_="vp-skip-link")
    if skip_link:
        skip_link.decompose()

    # Clean up unwanted elements
    clean_element(vp_page)

    # Extract inline Mermaid diagrams to standalone .svg files and replace the
    # inline <svg> (which markdownify would flatten to text) with an <img> ref.
    files_dir_name = html_filename[:-5] + "_files"  # strip trailing ".html"
    mermaid_map = save_mermaid_svgs(html_content, files_dir_name)
    for svg_tag in vp_page.find_all("svg"):
        classes = svg_tag.get("class") or []
        sid = svg_tag.get("id")
        is_diagram = ("flowchart" in classes) or (svg_tag.get("role") == "graphics-document document")
        fname = mermaid_map.get(sid) if sid else None
        if is_diagram and fname:
            img_tag = soup.new_tag("img")
            img_tag["src"] = f"../../HTML/_mermaid/{files_dir_name}/{fname}"
            img_tag["alt"] = "流程图"
            svg_tag.replace_with(img_tag)
        else:
            # decorative icon SVGs -> drop to avoid stray text
            svg_tag.decompose()

    # Get the page title
    title_elem = vp_page.find("h1")
    if title_elem is None:
        # Try vp-page-title
        title_container = vp_page.find("div", class_="vp-page-title")
        if title_container:
            title_elem = title_container.find("h1")

    # Remove the title from vp_page to avoid duplication, we'll add it manually
    if title_elem:
        title_text = title_elem.get_text(strip=True)
        title_elem.decompose()
    else:
        title_text = os.path.splitext(html_filename)[0].split(" _ ")[0]

    # Remove remaining vp-page-title container
    title_container = vp_page.find("div", class_="vp-page-title")
    if title_container:
        title_container.decompose()

    # Update image paths: fix relative paths
    for img in vp_page.find_all("img"):
        src = img.get("src", "")
        if src:
            # Check if should skip
            if should_skip_image(src):
                # Replace with empty string or just remove the image
                img.decompose()
                continue
            new_src = fix_image_path(src, html_filename, HTML_DIR)
            img["src"] = new_src

        # Remove loading="lazy" and data attributes
        for attr in list(img.attrs.keys()):
            if attr.startswith("data-") or attr in ("loading", "decoding"):
                del img[attr]

    # Preserve code blocks - convert pre/code to markdown-friendly format
    for pre in vp_page.find_all("pre"):
        # Get language from class
        lang = ""
        if pre.get("class"):
            for cls in pre.get("class", []):
                if cls.startswith("language-"):
                    lang = cls.replace("language-", "")
        # Mark the language for markdownify
        if lang:
            pre["data-lang"] = lang

    # Convert to markdown
    markdown_body = md(
        str(vp_page),
        heading_style="ATX",
        bullets="-",
        strip=["script", "style", "link"],
        code_language_callback=code_language_callback,
    )

    # Clean up the markdown
    markdown_body = cleanup_markdown(markdown_body)

    # Assemble final markdown
    final_md = f"# {title_text}\n\n{markdown_body.strip()}\n"

    return final_md


def cleanup_markdown(text):
    """Clean up markdown output artifacts."""
    # Remove "此页内容" TOC header line (VuePress artifact)
    text = re.sub(r'^此页内容\s*\n+', '', text, flags=re.MULTILINE)

    # Remove "图表加载中" Mermaid placeholder lines
    text = re.sub(r'^图表加载中\s*\n+', '', text, flags=re.MULTILINE)

    # Remove excessive blank lines (more than 2 consecutive)
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Fix code block language annotations from our custom data-lang
    def fix_code_block(match):
        lang = match.group(1) or ""
        code = match.group(2)
        if lang:
            return f"```{lang}\n{code.strip()}\n```"
        return f"```\n{code.strip()}\n```"

    # Fix pre-formatted code that markdownify might mishandle
    # Remove extra whitespace at line starts
    lines = text.split("\n")
    result_lines = []
    for line in lines:
        result_lines.append(line.rstrip())
    text = "\n".join(result_lines)

    # Fix image paths that might have been double-encoded
    text = re.sub(r"!\[\]\(\./[^)]+\)", lambda m: m.group(0).replace("./", ""), text)

    return text


def main():
    print("=" * 60)
    print("JavaGuide HTML → Markdown Converter")
    print("=" * 60)

    # Target language tree: java (default) / python / typescript.
    # Language localization (code samples) is a separate step afterwards.
    lang = "java"
    if len(sys.argv) > 1 and sys.argv[1] in ("java", "python", "typescript"):
        lang = sys.argv[1]
    out_base = OUTPUT_DIR / lang

    # Find all HTML files
    html_files = sorted([
        f for f in os.listdir(HTML_DIR)
        if f.endswith(".html") and not f.endswith("Zone.Identifier")
    ])

    print(f"\nFound {len(html_files)} HTML files.")
    print(f"Output tree: {out_base}\n")

    success_count = 0
    fail_count = 0

    for html_file in html_files:
        html_path = HTML_DIR / html_file
        category = get_category(html_file)
        out_filename = get_output_filename(html_file)
        out_dir = out_base / category
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / out_filename

        print(f"Processing: {html_file}")
        print(f"  → Category: {category}")
        print(f"  → Output:   {out_filename}")

        try:
            markdown_text = process_html_file(html_path, html_file)
            if markdown_text:
                with open(out_path, "w", encoding="utf-8") as f:
                    f.write(markdown_text)
                # Count some stats
                line_count = markdown_text.count("\n")
                char_count = len(markdown_text)
                img_count = markdown_text.count("![")
                print(f"  ✓ OK | {line_count} lines | {char_count} chars | {img_count} images")
                success_count += 1
            else:
                print(f"  ✗ FAILED - no content extracted")
                fail_count += 1
        except Exception as e:
            print(f"  ✗ ERROR: {e}")
            fail_count += 1

        print()

    print("=" * 60)
    print(f"Done: {success_count} success, {fail_count} failed")
    print(f"Output tree: {out_base}")
    print("=" * 60)


if __name__ == "__main__":
    main()
