# HTML to PDF Pipeline

Convert JavaGuide VuePress HTML articles to clean Markdown, then to print-ready LaTeX PDFs with Chinese support.

## Overview

```
HTML (VuePress SSR)  →  Markdown (clean)  →  LaTeX (.tex)  →  PDF
       │                      │                    │               │
  BeautifulSoup        remove TOC          md_to_latex()    xelatex ×2
  markdownify          escape_latex        fix_image_format  ctexart
```

## Prerequisites

```bash
# Python packages
pip install beautifulsoup4 markdownify cairosvg Pillow

# LaTeX (with Chinese support)
# TeX Live with ctex, xelatex, ctexart, tabularx, listings

# CJK fonts (for SVG→PDF/PNG conversion)
# Install to ~/.local/share/fonts/ and run fc-cache -f
# Example: Source Han Sans SC OTF files
```

## Phase 1: HTML → Markdown

### Extraction
- Target: `<main class="vp-page">` element
- Remove: navbar, sidebar, toc, footer, breadcrumbs, page-nav, meta, header-anchors, copy-code-buttons
- Strip `href` from `javaguide.cn` links (keep text), unwrap `<a>` tags
- Remove `mermaid-lazy-container` and "图表加载中" placeholders

### Code language recovery (`code_language_callback`)
- **Problem**: Shiki puts the `language-xxx` class on the wrapping `<div class="language-json">` and the `<code class="language-json">`, NOT on `<pre>` (which is `class="shiki"`). Without recovery every fence becomes a bare ```` ``` ````  → no highlighting downstream.
- **Fix**: pass `code_language_callback` to `markdownify`. The callback (receives `<pre>`) checks, in order: `<code>` child class → `<pre>` class → parent `<div>` class / `data-ext`.
- `NORMALIZE_LANG` maps `text`/`plaintext`/`markdown`/`md` → `""` (bare fence); real langs (`json`, `java`, `http`, `sql`, `yaml`, `bash`, …) pass through.

### Image handling
- Initial paths: `./ArticleName _ JavaGuide_files/xxx.png`
- Convert to relative: `../../../HTML/ArticleName _ JavaGuide_files/xxx.png`
- Skip chrome images: `logo.*`, `interview-guide-banner.*`, `favicon.*`
- `fix_image_path` leaves already-resolved `../` paths untouched (used by extracted Mermaid diagrams).

### Inline Mermaid diagram extraction (`save_mermaid_svgs`, `mermaid_to_standalone`)
- **Problem**: Mermaid diagrams are client-side rendered into the SSR HTML as **inline `<svg>`** (identified by `class="flowchart"` or `role="graphics-document document"`, wrapped in `.mermaid-content`/`.mermaid-wrapper`). markdownify flattens them to plain text → diagrams vanish.
- **Fix**: before markdownify, scan the raw HTML for these `<svg id="v-N" …>` blocks, clean each, write a standalone `.svg`, and replace the inline `<svg>` in the soup with an `<img>` ref. Decorative icon SVGs (`width="1em"`, iconify) are decomposed.
- **Output location**: `HTML/_mermaid/<ArticleName _ JavaGuide_files>/mermaid-<id>.svg`. Do NOT write next to the saved page assets — that `_files/` dir is often **root-owned/read-only**, which also breaks SVG→PDF conversion (which writes siblings). `HTML/_mermaid/` is tool-owned/writable.
- **Reference**: img `src` is set to the final relative path `../../HTML/_mermaid/…/mermaid-<id>.svg` (resolves correctly from both `markdown/<cat>/` and `latex/<cat>/`).

#### foreignObject → text (`_foreignobject_to_text`)
Mermaid node/edge labels are HTML inside `<foreignobject>` (lowercased in serialized HTML), which **cairosvg cannot render** → boxes with no text. Convert each label to a real SVG `<text>`:
- Extract text from inner `<p>`/`<span>` (unescape entities, `<br>` → line break).
- Size font to the foreignObject box (`fontsize ≈ lineHeight*0.72`, clamped 9–15px); multi-line wrap via `_wrap_units` (CJK counts as 2 ascii units); center at box mid with per-line `<tspan>` y.
- Use an **inline `style="fill:#1f2937;font-family:'Source Han Sans SC',sans-serif;font-size:Npx"`** — inline style beats Mermaid's embedded id-selector CSS (e.g. `#v-3{fill:#ccc;font-family:trebuchet ms}`) which would otherwise hide the label / break CJK glyphs.
- Empty labels (`width="0"`) are dropped.
- Caveat: `fix_svg_content` strips `marker-*` refs (draw.io workaround), so Mermaid edge **arrowheads are lost** — connecting lines/boxes/labels remain.

### TOC removal
- The VuePress TOC is a `- bullet list` between h1 title and first body paragraph
- `remove_toc()` strips all lines starting with `- ` or `  - ` after h1

## Phase 2: Markdown → LaTeX

### Document template (`LATEX_PREAMBLE`)
```latex
\documentclass[10pt,a4paper]{ctexart}
\usepackage[top=1.5cm, bottom=1.5cm, left=1.8cm, right=1.8cm]{geometry}
\usepackage{tabularx}        % auto-width tables
\usepackage{longtable}       % multi-page tables
\usepackage{listings}        % code blocks
\usepackage{enumitem}        % compact lists
\usepackage{titlesec}        % numbered headings
```

### Code syntax highlighting (`listings`)
Self-contained (no `-shell-escape`, no `minted`/`latexminted`).
- Colors: `codekw` (keywords, blue bold), `codecomment` (green italic), `codestring` (dark red), plus `codenum`/`codepunct`. Set via `keywordstyle`/`commentstyle`/`stringstyle` in `\lstset`.
- Built-in listings languages used: `Java`, `SQL`, `bash`, `Python`, `XML`, `HTML`, `CSS`.
- **Custom** `\lstdefinelanguage` for `json`, `yaml`, `http` (listings has no built-ins). JSON: `morekeywords={true,false,null}` + `morestring=[b]"`.
- `LANG_MAP` translates fence lang → listings lang. **Gotcha**: `json`/`yaml` must NOT map to `Java` (old bug); `text`/`markdown`/`diff`/`ebnf`/`mermaid` → `""` (plain).
- Keep the global `\lstset` CJK `literate` (full-width punctuation) and `breaklines`; custom langs deliberately omit their own `literate` to avoid overriding it.

### Heading mapping
| Markdown | LaTeX | Numbering |
|----------|-------|-----------|
| `#` (doc title) | `\title{...} \maketitle` | none |
| `##` | `\section{...}` | 1, 2, 3... |
| `###` | `\subsection{...}` | 1.1, 1.2... |
| `####` | `\subsubsection{...}` | 1.1.1... |

### Inline formatting (`process_inline`)
**Critical ordering** to avoid LaTeX escape conflicts:
1. Save `` `code` `` → `IMCODE1IMC` markers
2. Save `**bold**` → `IMB1IMB` markers
3. Save `*italic*` → `IMI1IMI` markers
4. Save `[text](url)` → `IML1IML` markers
5. `escape_latex_light()` on remaining plain text (no `#` escaping!)
6. Restore markers → `\textbf{...}`, `\texttt{...}`, `\href{...}{...}`

### Table rendering (`render_table`)
- Short tables (≤25 rows): `tabularx` with `X` columns, auto-wrap to `\textwidth`
- Long tables (>25 rows): `longtable` with `p{proportional_width}` columns
- All tables use `\footnotesize` font
- Column widths calculated proportionally from max cell length

### Escaping rules

| Function | Used for | Escapes `#`? | Escapes `_`? |
|----------|----------|-------------|-------------|
| `escape_latex()` | headings, code content, table cells | Yes (via `\#`) | Yes (via `\(?<!\\\)_` regex) |
| `escape_latex_light()` | paragraph body after markers | **No** (markers use `#`) | Yes |
| `escape_tex_cell()` | table cell preliminary | No | No (only `&` and `%`) |

**Key rule**: `escape_latex_light` MUST NOT escape `#`, or the `IMCODE`, `IMB`, etc. markers will be corrupted to `\#\#\#IMB...` and never replaced.

## Phase 3: Image Pipeline

### Flow
```
Image reference in markdown
        │
        ▼
\ includegraphics[width=0.85\textwidth]{path}
        │
        ▼
fix_image_format() resolves and converts path
        │
        ├── .svg  → convert_svg_to_pdf() → .pdf or .png
        ├── .webp → convert_webp_to_png() → .png
        └── .png  → convert to .jpg (xelatex compatibility fallback)
```

### SVG conversion (`convert_svg_to_pdf`)
1. Delete stale .pdf / .png outputs
2. Run `fix_svg_content()` to patch source
3. Try `cairosvg.svg2pdf()` → if >2KB, use .pdf
4. Fallback: `cairosvg.svg2png(dpi=150)` → use .png

Outputs go beside the source SVG, unless that dir is read-only — then `_writable_output()` redirects to `HTML/_converted/<dirname>/` (same for WebP→PNG and PNG→JPG). The returned `\includegraphics` path is absolute, so the redirect is transparent.

### SVG pre-processing (`fix_svg_content`)
**Problem**: JavaGuide's draw.io SVGs contain CSS that cairosvg can't parse.

| Issue | Fix |
|-------|-----|
| `light-dark(rgb(...), rgb(...))` nested parens | `_strip_light_dark()` — bracket-counting parser, keeps first arg |
| `var(--name, fallback)` nested parens | `_strip_var()` — bracket-counting parser, keeps fallback |
| ANY `font-family` (`system-ui`, `Helvetica`, `PingFang SC`, `monospace`, …) | Force to `'Source Han Sans SC', sans-serif` — in `<style>` CSS blocks, `style=""` attrs, AND `font-family=""` attrs |
| `<foreignObject>` HTML text | Remove entirely (rely on `<text>` fallback elements) |
| `<switch>` wrappers | Unwrap (expose inner `<text>`) |
| `filter="url(#...)"` references | Remove (unsupported filter effects) |
| `marker-end="url(#...)"` references | Remove |
| `style=""` with `background-color` | Strip background-color property |
| `xmlns:xxx` namespace prefixes | Remove |

### Font requirements for SVG rendering
- cairosvg uses fontconfig and has **NO per-glyph fallback**: it selects the *first* family in the `font-family` list; if that font lacks a glyph, you get tofu (□) — it will NOT fall back to a later family or a CJK font.
- Therefore `fix_svg_content` **forces** `'Source Han Sans SC', sans-serif` on every `font-family`, in three places:
  1. `<style>` CSS blocks — e.g. draw.io's `text{font-family:system-ui,-apple-system,"PingFang SC",...}` (declared once, inherited by all `<text>`; the most common tofu cause and easy to miss).
  2. `style="..."` presentation-style attributes.
  3. standalone `font-family="..."` attributes.
- The listed macOS/Windows families (`PingFang SC`, `Microsoft YaHei`) are NOT installed on Linux, so they don't help — replacement is mandatory, not a fallback.
- Font install: `cp *.otf ~/.local/share/fonts/ && fc-cache -f`; verify with `fc-list :lang=zh family`.
- Quick check: render CJK to PNG with the family vs `DejaVu Sans`, composite over white, compare dark-pixel counts (real glyphs ≫ tofu boxes).

### WebP conversion (`convert_webp_to_png`)
- xelatex cannot read WebP → convert to PNG with Pillow
- `Image.open().save(format='PNG')`

## Phase 4: TeX → PDF

```bash
xelatex -interaction=nonstopmode -output-directory=<pdf_dir> <tex_file>
# Run twice for cross-references
```

- Use `ctexart` documentclass (handles CJK via xeCJK + Fandol fonts)
- `\includegraphics` can handle: PDF, PNG, JPEG (NOT SVG, NOT WebP)
- Compile from `latex/<lang>/<category>/` so relative `../../../HTML/` paths resolve
- `build_pdfs.py` walks each top-level tree under `markdown/` (`java`, `python`, `typescript`), skips `README.md`, and emits `latex/<lang>/…` + `pdf/<lang>/…`
- `convert.py [java|python|typescript]` selects the target tree (default `java`); localization of code samples to Python/TypeScript is a separate manual/LLM step

## Common Issues & Fixes

| Symptom | Root Cause | Fix |
|---------|-----------|-----|
| `\#\#\#B\#\#\#` appearing in output | `escape_latex_light` escapes `#` → markers broken | Don't escape `#` in `escape_latex_light` |
| Chinese text as tofu (□) in SVG images | cairosvg has no glyph fallback; SVG `font-family` (often in a `<style>` block like `text{font-family:system-ui,…}`) resolves to a non-CJK font | Force `'Source Han Sans SC', sans-serif` on every `font-family` — **including inside `<style>` blocks**, not just `style=`/attrs |
| SVG conversion fails: `invalid literal for int() with base 16: 'ig'` | `light-dark()` CSS function not parsed | `_strip_light_dark()` with bracket-counting |
| SVG conversion fails: `could not convert string to float: ' rgb(255'` | Malformed `style` value after light-dark removal | Strip `background-color` from style; remove entire style if needed |
| Table overflows page width | `|l|l|l|` columns don't wrap | Use `tabularx{|X|X|X|}` with `\footnotesize` |
| `Missing $ inserted` | Bare `_` not in math mode | Escape `_` → `\_` via `re.sub(r'(?<!\\)_(?!\{)', r'\\_', text)` |
| `Unable to load picture` for .png | xelatex can't read some PNGs (path encoding issue) | Convert PNG→JPG as fallback in `fix_image_format` |
| `Cannot determine size of graphic` for .svg | xelatex can't read SVG natively | SVG must be converted to PDF or PNG first |
| Images too wide | `natwidth=1000,natheight=1000` forces wrong aspect ratio | Remove natwidth (only needed for raw SVG which we don't use) |
| Missing images | Original PNG/WebP deleted by cleanup | `fix_image_format` checks .jpg/.png/.pdf alternatives if original gone |
| Code blocks not highlighted | fence has no language (Shiki class on `<div>`/`<code>`, not `<pre>`) | `code_language_callback` recovers lang; add colors + custom json/yaml/http langs |
| `json`/`yaml` rendered as Java keywords | `LANG_MAP` mapped them to `Java` | map `json→json`, `yaml→yaml`, add `http` |
| Mermaid diagram becomes plain text | client-rendered inline `<svg>` flattened by markdownify | `save_mermaid_svgs` extracts to standalone `.svg` + `<img>` ref |
| Mermaid diagram renders as empty boxes | labels are HTML in `<foreignobject>`; cairosvg can't render | `_foreignobject_to_text` converts labels to SVG `<text>` |
| Mermaid label invisible (light gray) or CJK tofu | Mermaid `#id{fill:#ccc;font-family:trebuchet ms}` beats attrs | set label color/font via **inline `style=`** (beats stylesheet, non-`!important`) |
| `Permission denied` / `CAIRO_STATUS_WRITE_ERROR` writing next to a saved asset | the saved-page `_files/` dir is root-owned/read-only, so converted siblings can't be written | `_writable_output()` redirects conversions to writable `HTML/_converted/`; generated Mermaid SVGs go to `HTML/_mermaid/` |
| `ModuleNotFoundError: bs4` under WSL | default `wsl` user is `root`; deps live in `zhang`'s user site | run pipeline as `wsl -d Ubuntu-20.04 -u zhang` |

## File Layout

```
Agent知识/
├── HTML/                    # Source: saved VuePress pages
│   ├── ArticleName.html
│   ├── ArticleName _ JavaGuide_files/   # saved assets (may be root-owned/RO)
│   │   ├── diagram.svg
│   │   ├── screenshot.png
│   │   └── photo.webp
│   ├── _mermaid/            # tool-generated standalone Mermaid SVGs (writable)
│   │   └── ArticleName _ JavaGuide_files/
│   │       └── mermaid-v-3.svg
│   └── _converted/          # cache for image conversions when _files/ is read-only
│       └── ArticleName _ JavaGuide_files/
│           └── diagram.pdf
├── markdown/                # Output: cleaned markdown, one tree per language
│   ├── README.md            # index + learning path
│   ├── java/                # original Java-ecosystem version (convert.py default)
│   │   └── <Category>/
│   │       └── NN-ShortName.md
│   ├── python/              # Python version (localized code samples)
│   └── typescript/          # TypeScript version
├── latex/                   # Generated: LaTeX source
│   └── <lang>/<Category>/
│       └── NN-ShortName.tex
├── pdf/                     # Final: compiled PDFs
│   └── <lang>/<Category>/
│       └── NN-ShortName.pdf
├── build_pdfs.py            # Full pipeline script (walks markdown/<lang>/ trees)
├── convert.py               # HTML→MD (+ lang recovery, Mermaid extraction)
└── .opencode/
    └── skills/
        └── html-to-pdf.md   # This skill
```

Categories: `00-概念与术语`, `01-LLM基础`, `02-Agent`, `03-RAG`, `04-工程实践`, `05-评测与质量`, `06-安全与治理`, `07-系统设计`, `08-应用与案例`, `09-生态与前沿`.
Markdown image refs are `../../../HTML/…` (one level deeper than before) so they resolve from
both `markdown/<lang>/<cat>/` and `latex/<lang>/<cat>/`.

## Running the pipeline

```bash
# Must run as user 'zhang' (Python deps + TeX Live live under /home/zhang)
cd /path/to/ai-agent-knowledge && python3 convert.py && python3 build_pdfs.py
```
- `convert.py` regenerates ALL markdown from HTML (deterministic; also (re)extracts Mermaid SVGs).
- `build_pdfs.py` cleans TOC, generates `.tex`, converts images, runs `xelatex ×2`.
- Add a new article to `CATEGORY_MAP` in `convert.py` (keyword → category dir) before running, else it lands in `06-其他`.
