#!/usr/bin/env python3
"""
Master script: clean TOC from markdown files, then convert to LaTeX + compile PDF.
Uses ctexart for Chinese support, xelatex for compilation.
Converts SVG images to PDF before LaTeX compilation.
"""

import os
import re
import sys
import subprocess
from pathlib import Path

try:
    import cairosvg
    HAS_CAIROSVG = True
except ImportError:
    HAS_CAIROSVG = False

BASE_DIR = Path("/home/zhang/demos/latex_demos/Agent知识")
MD_DIR = BASE_DIR / "markdown"
TEX_DIR = BASE_DIR / "latex"
PDF_DIR = BASE_DIR / "pdf"
HTML_DIR = BASE_DIR / "HTML"
TEXLIVE_BIN = "/home/zhang/texlive/bin/x86_64-linux"
os.environ["PATH"] = f"{TEXLIVE_BIN}:{os.environ.get('PATH', '')}"

LATEX_PREAMBLE = r"""\documentclass[10pt,a4paper]{ctexart}

% --- Packages ---
\usepackage[top=1.5cm, bottom=1.5cm, left=1.8cm, right=1.8cm]{geometry}
\usepackage{hyperref}
\usepackage{graphicx}
\usepackage{float}
\usepackage{longtable}
\usepackage{tabularx}
\usepackage{booktabs}
\usepackage{enumitem}
\usepackage{xcolor}
\usepackage{fancyhdr}
\usepackage{listings}
\usepackage{fontspec}
\usepackage{titlesec}
\usepackage{caption}

% --- Code block styling ---
\definecolor{codebg}{RGB}{245,245,245}
\definecolor{codeframe}{RGB}{220,220,220}
\definecolor{codekw}{RGB}{0,0,192}
\definecolor{codecomment}{RGB}{0,128,0}
\definecolor{codestring}{RGB}{163,21,21}
\definecolor{codenum}{RGB}{128,0,128}
\definecolor{codepunct}{RGB}{90,90,90}

\lstset{
  basicstyle=\ttfamily\footnotesize,
  keywordstyle=\color{codekw}\bfseries,
  commentstyle=\color{codecomment}\itshape,
  stringstyle=\color{codestring},
  backgroundcolor=\color{codebg},
  frame=single,
  rulecolor=\color{codeframe},
  breaklines=true,
  breakatwhitespace=false,
  breakindent=0pt,
  postbreak=\mbox{\textcolor{red}{$\hookrightarrow$}\space},
  numbers=left,
  numberstyle=\tiny\color{gray},
  columns=flexible,
  keepspaces=true,
  showstringspaces=false,
  tabsize=2,
  aboveskip=4pt,
  belowskip=4pt,
  extendedchars=true,
  literate={，}{{，}}1 {；}{{；}}1 {！}{{！}}1 {？}{{？}}1 {“}{{“}}1 {”}{{”}}1 {（}{{（}}1 {）}{{）}}1 {《}{{《}}1 {》}{{》}}1,
}

% --- Extra language definitions (no built-in listings support) ---
\lstdefinelanguage{json}{
  morekeywords={true,false,null},
  sensitive=true,
  morestring=[b]",
  comment=[l]{//},
  morecomment=[s]{/*}{*/},
}
\lstdefinelanguage{yaml}{
  morekeywords={true,false,null,yes,no,on,off},
  sensitive=false,
  morecomment=[l]{\#},
  morestring=[b]",
  morestring=[d]',
}
\lstdefinelanguage{http}{
  morekeywords={GET,POST,PUT,DELETE,PATCH,HEAD,OPTIONS,HTTP,Host,Accept,Authorization,Content-Type,Content-Length,User-Agent},
  sensitive=true,
  morecomment=[l]{\#},
  morestring=[b]",
}

% --- Compact spacing ---
\linespread{1.0}
\setlength{\parskip}{2pt plus 1pt minus 1pt}
\setlength{\parindent}{0pt}

% --- Table styling ---
\renewcommand{\arraystretch}{1.1}

% --- Heading styling (numbered) ---
\titleformat{\section}{\large\bfseries}{\thesection\quad}{0em}{}
\titlespacing{\section}{0pt}{10pt}{5pt}
\titleformat{\subsection}{\normalsize\bfseries}{\thesubsection\quad}{0em}{}
\titlespacing{\subsection}{0pt}{8pt}{4pt}
\titleformat{\subsubsection}{\normalsize\bfseries}{\thesubsubsection\quad}{0em}{}
\titlespacing{\subsubsection}{0pt}{6pt}{3pt}

% --- Page style ---
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\small\emph{Agent 知识整理}}
\fancyhead[R]{\small\thepage}
\renewcommand{\headrulewidth}{0.4pt}

% --- Hyperref setup ---
\hypersetup{
  colorlinks=true,
  linkcolor=blue,
  urlcolor=blue,
  citecolor=blue,
}

% --- Caption format ---
\DeclareCaptionFormat{myformat}{\small\bfseries #1#2#3}
\captionsetup{format=myformat}

\begin{document}
"""

LATEX_POSTAMBLE = r"""
\end{document}
"""


# ============================================================
# Image Conversion
# ============================================================

def _writable_output(src_path, suffix):
    """Return an output path (with `suffix`) in a writable location.

    Saved-page asset dirs (``*_files/``) are sometimes root-owned/read-only,
    so writing a converted sibling (e.g. ``.pdf`` next to ``.svg``) fails. In
    that case redirect the output to ``HTML/_converted/<dirname>/``.
    """
    src_path = Path(src_path)
    parent = src_path.parent
    if os.access(str(parent), os.W_OK):
        return src_path.with_suffix(suffix)
    cache = HTML_DIR / "_converted" / parent.name
    cache.mkdir(parents=True, exist_ok=True)
    return cache / (src_path.stem + suffix)


def convert_svg_to_pdf(svg_path):
    """Convert an SVG file. Always fixes content first, then tries PDF→PNG fallback."""
    pdf_path = _writable_output(svg_path, '.pdf')
    png_path = _writable_output(svg_path, '.png')

    for p in [pdf_path, png_path]:
        if p.exists():
            p.unlink()

    # Always fix SVG content first for font/CSS compatibility
    fixed = fix_svg_content(svg_path)

    # Try PDF first
    try:
        cairosvg.svg2pdf(bytestring=fixed, write_to=str(pdf_path))
        if pdf_path.stat().st_size > 2000:
            return str(pdf_path)
    except Exception:
        pass

    # Fallback to PNG
    try:
        cairosvg.svg2png(bytestring=fixed, write_to=str(png_path), dpi=150)
        if png_path.stat().st_size > 2000:
            return str(png_path)
    except Exception as e:
        print(f"    Warning: SVG conversion failed for {svg_path.name}: {e}")

    return None


def _strip_light_dark(text):
    """Replace light-dark(X, Y) with X, handling nested parens."""
    result = []
    i = 0
    while i < len(text):
        if text[i:i+11] == 'light-dark(':
            i += 11
            depth = 1
            start = i
            while i < len(text) and depth > 0:
                if text[i] == '(': depth += 1
                elif text[i] == ')': depth -= 1
                i += 1
            inner = text[start:i-1]
            comma_pos = -1
            d = 0
            for j, c in enumerate(inner):
                if c == '(': d += 1
                elif c == ')': d -= 1
                elif c == ',' and d == 0:
                    comma_pos = j
                    break
            if comma_pos > 0:
                result.append(inner[:comma_pos].strip())
        else:
            result.append(text[i])
            i += 1
    return ''.join(result)


def _strip_var(text):
    """Replace var(--name, fallback) with fallback, handling nested parens."""
    result = []
    i = 0
    while i < len(text):
        if text[i:i+4] == 'var(':
            i += 4
            depth = 1
            start = i
            while i < len(text) and depth > 0:
                if text[i] == '(': depth += 1
                elif text[i] == ')': depth -= 1
                i += 1
            inner = text[start:i-1]
            last_comma = -1
            d = 0
            for j, c in enumerate(inner):
                if c == '(': d += 1
                elif c == ')': d -= 1
                elif c == ',' and d == 0:
                    last_comma = j
            if last_comma > 0:
                result.append(inner[last_comma+1:].strip())
            else:
                result.append('black')
        else:
            result.append(text[i])
            i += 1
    return ''.join(result)


def fix_svg_content(svg_path):
    """Strip unsupported features and fix fonts for CJK rendering."""
    with open(svg_path, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    # 1. CSS functions cairosvg can't parse (handle nested parens)
    content = _strip_light_dark(content)
    content = _strip_var(content)

    # 2. foreignObject blocks (HTML text, cairosvg can't render)
    content = re.sub(r'<foreignObject[^>]*>.*?</foreignObject>', '', content, flags=re.DOTALL)

    # 3. Unwrap <switch> to expose <text> fallbacks
    content = content.replace('<switch>', '').replace('</switch>', '')

    # 4. Strip unsupported filter/marker references
    content = re.sub(r'\s+filter="[^"]*"', '', content)
    content = re.sub(r'\s+marker-(?:start|end|mid)="[^"]*"', '', content)

    # 4b. Force a CJK-capable font on every font-family declared inside a
    #     <style> CSS block. cairosvg has no per-glyph font fallback, so a
    #     family like `system-ui`/`Helvetica`/`PingFang SC` (unavailable on
    #     Linux) renders Chinese as tofu (□). draw.io SVGs declare the font
    #     once here (e.g. `text{font-family:system-ui,...}`), inherited by all
    #     <text> elements, and this is NOT covered by the style="" fixes below.
    def fix_style_block(m):
        css = re.sub(r'font-family\s*:\s*[^;}]+',
                     "font-family:'Source Han Sans SC', sans-serif", m.group(2))
        return m.group(1) + css + m.group(3)

    content = re.sub(r'(<style[^>]*>)(.*?)(</style>)', fix_style_block,
                     content, flags=re.DOTALL)

    # 5. Fix style attributes: remove problematic values, fix CJK fonts
    def fix_style(m):
        inner = m.group(1)
        # Remove color-scheme
        inner = re.sub(r'\bcolor-scheme\s*:\s*[^;]+;?', '', inner)
        # Remove background-color (cairosvg sometimes chokes on it)
        inner = re.sub(r'\bbackground-color\s*:\s*[^;]+;?', '', inner)
        # Remove background (can have complex values)
        inner = re.sub(r'\bbackground\s*:\s*[^;"]+;?', '', inner)
        # Force a CJK-capable font for ANY declared family
        inner = re.sub(r'font-family\s*:\s*[^;]+',
                       "font-family:'Source Han Sans SC', sans-serif", inner)
        # Clean up empty/malformed properties
        inner = re.sub(r';\s*;', ';', inner)
        inner = re.sub(r';\s*$', '', inner)
        inner = inner.strip()
        if not inner:
            return ''
        return f'style="{inner}"'

    content = re.sub(r'style="([^"]*)"', fix_style, content)

    # 6. Fix font-family in standalone attributes (text elements)
    content = re.sub(
        r'''font-family\s*=\s*(['"]).*?\1''',
        '''font-family="'Source Han Sans SC', sans-serif"''',
        content
    )

    # 7. Strip namespace prefixes
    content = re.sub(r'\s*xmlns:\w+="[^"]*"', '', content)

    return content.encode('utf-8')


def convert_webp_to_png(webp_path):
    """Convert a WebP image to PNG. Returns PNG path or None."""
    png_path = _writable_output(webp_path, '.png')
    if png_path.exists() and png_path.stat().st_mtime > webp_path.stat().st_mtime:
        return str(png_path)
    try:
        from PIL import Image
        img = Image.open(str(webp_path))
        img.save(str(png_path), 'PNG')
        return str(png_path)
    except Exception as e:
        print(f"    Warning: WebP→PNG failed for {webp_path.name}: {e}")
        return None


# ============================================================
# Data
# ============================================================

def fix_image_references(tex_content, tex_dir):
    """Find all image references in tex content, convert problematic formats,
    and update the references."""
    return fix_image_format(tex_content, tex_dir)


def fix_image_format(tex_content, tex_dir):
    """Replace SVG→PDF/PNG, WebP→PNG, and handle problematic image paths."""
    def replace_img(m):
        opts = m.group(1) or ''
        fname = m.group(2)
        ext = Path(fname).suffix.lower()
        img_path = (tex_dir / fname).resolve()

        if not img_path.exists():
            # Try JPG/PNG/PDF alternatives if original missing
            for alt_ext in ['.jpg', '.png', '.pdf']:
                alt = img_path.with_suffix(alt_ext)
                if alt.exists():
                    return f'\\includegraphics[{opts}]{{{alt}}}'
            return m.group(0)

        if ext == '.svg' and HAS_CAIROSVG:
            new_path = convert_svg_to_pdf(img_path)
            if new_path:
                return f'\\includegraphics[{opts}]{{{new_path}}}'
        elif ext == '.webp':
            new_path = convert_webp_to_png(img_path)
            if new_path:
                return f'\\includegraphics[{opts}]{{{new_path}}}'
        elif ext in ('.png', '.jpeg', '.jpg', '.gif', '.bmp'):
            jpg_path = _writable_output(img_path, '.jpg')
            if not jpg_path.exists() or jpg_path.stat().st_mtime < img_path.stat().st_mtime:
                try:
                    from PIL import Image
                    img = Image.open(str(img_path))
                    if img.mode in ('RGBA', 'P', 'LA'):
                        img = img.convert('RGB')
                    img.save(str(jpg_path), 'JPEG', quality=95)
                except Exception:
                    pass
            if jpg_path.exists():
                return f'\\includegraphics[{opts}]{{{jpg_path}}}'

        return m.group(0)

    return re.sub(
        r'\\includegraphics(?:\[([^\]]*)\])?\{([^}]+)\}',
        replace_img,
        tex_content
    )

# Languages that map to lstlisting language names
LANG_MAP = {
    "python": "Python",
    "py": "Python",
    "java": "Java",
    "javascript": "Java",
    "js": "Java",
    "typescript": "Java",
    "ts": "Java",
    "json": "json",
    "yaml": "yaml",
    "yml": "yaml",
    "http": "http",
    "xml": "XML",
    "html": "HTML",
    "css": "CSS",
    "sql": "SQL",
    "bash": "bash",
    "sh": "bash",
    "shell": "bash",
    "text": "",  # no language
    "": "",
    "markdown": "",
    "md": "",
    "diff": "",
    "ebnf": "",
    "mermaid": "",
}

def remove_toc(text):
    """Remove the TOC bullet list between H1 title and first real content."""
    lines = text.split('\n')
    result = []
    state = 'before_h1'
    h1_found = False
    toc_start = None
    toc_end = None

    for i, line in enumerate(lines):
        if not h1_found and re.match(r'^#\s', line):
            h1_found = True
            state = 'after_h1'
            result.append(line)
            continue

        if state == 'after_h1':
            stripped = line.strip()
            if stripped == '':
                result.append(line)
                continue
            if stripped.startswith('- '):
                # This is TOC
                state = 'in_toc'
                continue
            else:
                # Not TOC - this is real content
                state = 'in_content'
                result.append(line)
                continue

        if state == 'in_toc':
            stripped = line.strip()
            if stripped.startswith('- ') or stripped.startswith('  - ') or stripped.startswith('- - '):
                continue
            elif stripped == '':
                continue
            else:
                state = 'in_content'
                result.append(line)
                continue

        if state == 'in_content':
            result.append(line)

    # Remove leading blank lines from result (after H1, before content)
    # Find H1 position
    h1_idx = None
    for i, line in enumerate(result):
        if re.match(r'^#\s', line):
            h1_idx = i
            break

    if h1_idx is not None:
        # Remove excessive blank lines after H1
        clean = result[:h1_idx+1]
        tail = result[h1_idx+1:]
        # Skip blank lines until first content
        content_start = 0
        for j, line in enumerate(tail):
            if line.strip() != '':
                content_start = j
                break
        clean.append('')
        clean.extend(tail[content_start:])
        result = clean

    return '\n'.join(result)


def escape_latex(text):
    """Escape LaTeX special characters in running text."""
    text = text.replace('\\', '\\textbackslash{}')
    text = text.replace('&', '\\&')
    text = text.replace('%', '\\%')
    text = text.replace('$', '\\$')
    text = text.replace('#', '\\#')
    text = re.sub(r'(?<!\\)_(?!\{)', r'\\_', text)
    text = text.replace('{', '\\{')
    text = text.replace('}', '\\}')
    text = text.replace('~', '\\textasciitilde{}')
    text = text.replace('^', '\\textasciicircum{}')
    return text


def process_inline(text):
    """Process inline markdown: bold, italic, code, links. Return LaTeX-safe text."""
    # Step 1: Save inline code to markers (protect from all processing)
    codes = {}
    code_counter = [0]
    def save_code(m):
        code_counter[0] += 1
        codes[code_counter[0]] = m.group(1)
        return f'###IC{code_counter[0]}###'
    text = re.sub(r'`([^`]+)`', save_code, text)

    # Step 2: Convert standalone images to figure
    text = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)',
                  lambda m: (
                      '\n\n\\begin{figure}[H]\n\\centering\n'
                      '\\includegraphics[width=0.85\\textwidth]'
                      f'{{{m.group(2)}}}\n\\end{{figure}}\n\n'
                  ),
                  text)

    # Step 3: Markdown → LaTeX formatting
    text = re.sub(r'\*\*(.+?)\*\*', r'###B###\1###BE###', text)
    text = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'###I###\1###IE###', text)

    # Step 4: Links
    text = re.sub(r'\[([^\]]*)\]\(([^)]+)\)',
                  lambda m: f'###LINK###{m.group(2)}###LTEXT###{escape_latex(m.group(1))}###LEND###' if m.group(1) else f'\\url{{{m.group(2)}}}',
                  text)

    # Step 5: Escape remaining literal LaTeX special chars
    text = escape_latex_light(text)

    # Step 6: Restore formatting markers to actual LaTeX
    text = text.replace('###B###', '\\textbf{')
    text = text.replace('###BE###', '}')
    text = text.replace('###I###', '\\textit{')
    text = text.replace('###IE###', '}')
    # Links: ###LINK###url###LTEXT###text###LEND### → \href{url}{text}
    text = re.sub(r'###LINK###([^#]+)###LTEXT###(.*?)###LEND###', r'\\href{\1}{\2}', text)

    # Step 7: Restore inline code (already LaTeX-safe)
    for idx in sorted(codes.keys(), reverse=True):
        code_text = escape_latex(codes[idx])
        text = text.replace(f'###IC{idx}###', f'\\texttt{{{code_text}}}')

    return text


def escape_latex_light(text):
    """Escape LaTeX special chars in plain text.
    Does NOT escape # (used as marker delimiter)."""
    text = text.replace('&', '\\&')
    text = text.replace('%', '\\%')
    text = text.replace('$', '\\$')
    text = re.sub(r'(?<!\\)_(?!\{)', r'\\_', text)
    text = text.replace('~', '\\textasciitilde{}')
    text = text.replace('^', '\\textasciicircum{}')
    text = text.replace('{', '\\{')
    text = text.replace('}', '\\}')
    return text


def fix_image_paths(text, tex_filename):
    """Fix image paths to be relative to the tex output directory."""
    # Images are referenced as ../../HTML/xxx_files/yyy.png
    # When .tex is in latex/category/xxx.tex, we need to point to HTML/xxx_files/yyy.png
    # But .tex file path is TEX_DIR/category/file.tex, so: ../../HTML/... works from that dir too
    # Actually we need to be careful. When xelatex compiles from the tex file's directory,
    # the path ../../HTML/... should work from latex/category/
    # Let's verify: latex/01-Agent核心/xxx.tex -> ../../HTML/ = python 知识/HTML/
    return text


def md_to_latex(text, title):
    """Convert markdown text to LaTeX body."""
    lines = text.split('\n')
    output = []
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Skip empty lines at start
        if not output and stripped == '':
            i += 1
            continue

        # H1 - extra heading in body (rare), use section*
        if stripped.startswith('# ') and output:
            heading = stripped[2:].strip()
            output.append(f'\n\\section*{{{escape_latex(heading)}}}')
            i += 1
            continue

        # H2 → \section
        if re.match(r'^##\s', stripped):
            heading = re.sub(r'^##\s+', '', stripped).strip()
            heading = re.sub(r'\s*\{#[^}]*\}\s*$', '', heading)
            output.append(f'\n\\section{{{escape_latex(heading)}}}')
            i += 1
            continue

        # H3 → \subsection
        if re.match(r'^###\s', stripped):
            heading = re.sub(r'^###\s+', '', stripped).strip()
            heading = re.sub(r'\s*\{#[^}]*\}\s*$', '', heading)
            output.append(f'\n\\subsection{{{escape_latex(heading)}}}')
            i += 1
            continue

        # H4 → \subsubsection
        if re.match(r'^####\s', stripped):
            heading = re.sub(r'^####\s+', '', stripped).strip()
            heading = re.sub(r'\s*\{#[^}]*\}\s*$', '', heading)
            output.append(f'\n\\subsubsection{{{escape_latex(heading)}}}')
            i += 1
            continue

        # Code block start
        if stripped.startswith('```'):
            lang = stripped[3:].strip().lower()
            lst_lang = LANG_MAP.get(lang, '')
            i += 1
            code_lines = []
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code_lines.append(lines[i])
                i += 1
            i += 1  # skip closing ```

            code_text = '\n'.join(code_lines)
            if lst_lang:
                output.append(f'\n\\begin{{lstlisting}}[language={lst_lang}]\n{code_text}\n\\end{{lstlisting}}\n')
            else:
                output.append(f'\n\\begin{{lstlisting}}\n{code_text}\n\\end{{lstlisting}}\n')
            continue

        # Image (standalone)
        if re.match(r'^!\[([^\]]*)\]\(([^)]+)\)', stripped):
            m = re.match(r'^!\[([^\]]*)\]\(([^)]+)\)', stripped)
            img_path = m.group(2)
            alt = m.group(1)
            output.append('')
            output.append('\\begin{figure}[H]')
            output.append('\\centering')
            output.append(f'\\includegraphics[width=0.85\\textwidth]{{{img_path}}}')
            if alt:
                output.append(f'\\caption*{{{escape_latex(alt)}}}')
            output.append('\\end{figure}')
            output.append('')
            i += 1
            continue

        # Horizontal rule
        if re.match(r'^---+\s*$', stripped) or re.match(r'^\* \* \*+\s*$', stripped):
            output.append('\n\\medskip\n\\hrule\n\\medskip\n')
            i += 1
            continue

        # Empty line
        if stripped == '':
            output.append('')
            i += 1
            continue

        # Table
        if stripped.startswith('|') and stripped.endswith('|'):
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                table_lines.append(lines[i].strip())
                i += 1

            output.extend(render_table(table_lines))
            continue

        # Unordered list
        if re.match(r'^-\s', stripped):
            list_items = []
            while i < len(lines):
                s = lines[i].strip()
                if re.match(r'^-\s', s):
                    item = re.sub(r'^-\s+', '', s)
                    item = process_inline(item)
                    list_items.append(item)
                    i += 1
                elif s == '' and i + 1 < len(lines) and re.match(r'^-\s', lines[i+1].strip()):
                    i += 1  # skip blank within list
                else:
                    break
            if list_items:
                output.append('\\begin{itemize}[itemsep=2pt, topsep=4pt]')
                for item in list_items:
                    output.append(f'  \\item {item}')
                output.append('\\end{itemize}')
            continue

        # Ordered list
        if re.match(r'^\d+\.\s', stripped):
            list_items = []
            while i < len(lines):
                s = lines[i].strip()
                if re.match(r'^\d+\.\s', s):
                    item = re.sub(r'^\d+\.\s+', '', s)
                    item = process_inline(item)
                    list_items.append(item)
                    i += 1
                elif s == '' and i + 1 < len(lines) and re.match(r'^\d+\.\s', lines[i+1].strip()):
                    i += 1
                else:
                    break
            if list_items:
                output.append('\\begin{enumerate}[itemsep=2pt, topsep=4pt]')
                for item in list_items:
                    output.append(f'  \\item {item}')
                output.append('\\end{enumerate}')
            continue

        # Blockquote
        if stripped.startswith('>'):
            quote_lines = []
            while i < len(lines) and lines[i].strip().startswith('>'):
                q = re.sub(r'^>\s?', '', lines[i].strip())
                quote_lines.append(q)
                i += 1
            quote_text = ' '.join(quote_lines)
            quote_text = process_inline(quote_text)
            output.append(f'\n\\begin{{quote}}\n{quote_text}\n\\end{{quote}}\n')
            continue

        # Plain paragraph
        para_lines = []
        while i < len(lines) and lines[i].strip() != '':
            s = lines[i].strip()
            # Stop if we hit a special line (heading, code, list, table, etc.)
            if re.match(r'^(#{1,4}\s|```|!\[|---+|\* \* \*|^\|.*\|$|^-\s|^\d+\.\s|^>\s)', s):
                break
            para_lines.append(s)
            i += 1
        if para_lines:
            para = ' '.join(para_lines)
            para = process_inline(para)
            output.append(f'\n{para}\n')
        else:
            i += 1

    return '\n'.join(output)


def render_table(table_lines):
    """Render a markdown table to LaTeX with controlled column widths."""
    if len(table_lines) < 2:
        return []

    header = [c.strip() for c in table_lines[0].strip('|').split('|')]
    if len(table_lines) < 3:
        return []

    rows = []
    for tl in table_lines[2:]:
        rows.append([c.strip() for c in tl.strip('|').split('|')])

    num_cols = len(header)

    # Estimate column widths: find max text length per column
    col_max_chars = [0] * num_cols
    all_text = [list(header)]
    for row in rows:
        # Pad to match header
        while len(row) < num_cols:
            row.append('')
        all_text.append(row[:num_cols])
    for r in all_text:
        for ci, cell in enumerate(r):
            col_max_chars[ci] = max(col_max_chars[ci], len(cell) if cell else 0)

    # Calculate width fractions based on text length
    total_chars = sum(col_max_chars)
    if total_chars == 0:
        total_chars = 1
    # Use p{} for precise width control; tabularx X for auto-wrap
    is_long = len(rows) > 25

    result = []
    if is_long:
        # Longtable: use p{width} columns
        col_defs = '|' + '|'.join(
            f'p{{\\dimexpr {col_max_chars[i]/total_chars:0.3f}\\textwidth-2\\tabcolsep\\relax}}'
            for i in range(num_cols)
        ) + '|'
        result.append('{\\footnotesize')
        result.append(f'\\begin{{longtable}}{{{col_defs}}}')
    else:
        # Tabularx: use X columns for auto-wrapping
        col_defs = '|' + '|'.join(['X'] * num_cols) + '|'
        result.append('{\\footnotesize')
        result.append(f'\\begin{{tabularx}}{{\\textwidth}}{{{col_defs}}}')

    result.append('\\hline')

    # Header
    hdr_cells = [f'\\textbf{{{escape_tex_cell(h)}}}' for h in header]
    result.append(' & '.join(hdr_cells) + ' \\\\')
    result.append('\\hline')

    if is_long:
        result.append('\\endhead')
        result.append('\\hline')
        result.append('\\endfoot')

    # Rows
    for row in rows:
        while len(row) < num_cols:
            row.append('')
        row[:] = row[:num_cols]
        escaped = [process_inline(escape_tex_cell(c)) for c in row]
        result.append(' & '.join(escaped) + ' \\\\')
        result.append('\\hline')

    if is_long:
        result.append('\\end{longtable}')
    else:
        result.append('\\end{tabularx}')
    result.append('}')
    result.append('')

    return result


def escape_tex_cell(text):
    """Escape text for use inside a table cell (preliminary, will be further processed by process_inline)."""
    # Only escape & and % early; the rest will be handled by process_inline
    text = text.replace('&', '\\&')
    text = text.replace('%', '\\%')
    return text


def process_file(md_path, cat_name, md_filename_base):
    """Process one markdown file: clean TOC, generate tex, compile PDF."""
    with open(md_path, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    # Set the working directory for relative path resolution
    md_path_obj = Path(md_path)

    # Step 1: Clean TOC
    cleaned = remove_toc(content)

    # Write cleaned markdown back
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(cleaned)

    # Step 2: Extract title from first H1
    title_match = re.search(r'^#\s+(.+)', cleaned, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else md_filename_base

    # Get body (without H1 title line)
    body_lines = cleaned.split('\n')
    body_start = 0
    for j, line in enumerate(body_lines):
        if re.match(r'^#\s+', line):
            body_start = j + 1
            # Skip blank lines after title
            while body_start < len(body_lines) and body_lines[body_start].strip() == '':
                body_start += 1
            break
    body = '\n'.join(body_lines[body_start:])

    # Step 3: Convert body to LaTeX
    latex_body = md_to_latex(body, title)

    # Step 4: Assemble full LaTeX
    tex_content = LATEX_PREAMBLE + f'\n\\title{{{escape_latex(title)}}}\n\\date{{}}\n\\maketitle\n' + latex_body + LATEX_POSTAMBLE

    # Write .tex file
    tex_subdir = TEX_DIR / cat_name
    tex_subdir.mkdir(parents=True, exist_ok=True)
    tex_filename = md_filename_base + '.tex'
    tex_path = tex_subdir / tex_filename

    # Step 5: Convert any referenced SVG/WebP images and update paths
    tex_content = fix_image_references(tex_content, tex_subdir)

    with open(tex_path, 'w', encoding='utf-8') as f:
        f.write(tex_content)

    return tex_path, title


def compile_tex(tex_path, cat_name, tex_basename):
    """Compile a .tex file to PDF using xelatex."""
    tex_dir = tex_path.parent
    stem = tex_basename.replace('.tex', '')

    pdf_subdir = PDF_DIR / cat_name
    pdf_subdir.mkdir(parents=True, exist_ok=True)

    # Run xelatex twice for TOC/cross-refs
    for run in range(2):
        result = subprocess.run(
            ['xelatex', '-interaction=nonstopmode', '-output-directory',
             str(pdf_subdir), tex_path.name],
            cwd=str(tex_dir),
            capture_output=True,
            timeout=120,
        )
        if result.returncode != 0:
            stderr_text = result.stderr.decode('utf-8', errors='replace')[-500:]
            stdout_text = result.stdout.decode('utf-8', errors='replace')
            return False, stdout_text[-500:]

    pdf_path = pdf_subdir / f'{stem}.pdf'
    return pdf_path.exists(), ''


def main():
    print("=" * 60)
    print("Markdown → LaTeX + PDF Pipeline")
    print("=" * 60)

    success_md = 0
    success_tex = 0
    success_pdf = 0
    results = []

    for md_root, dirs, files in os.walk(MD_DIR):
        cat_name = os.path.relpath(md_root, MD_DIR)
        if cat_name == '.':
            continue

        for f in sorted(files):
            if not f.endswith('.md'):
                continue

            md_path = os.path.join(md_root, f)
            base_name = f.replace('.md', '')
            short_name = f[:50] + ('...' if len(f) > 50 else '')

            print(f"\n--- {cat_name}/{short_name} ---")

            # Process (clean TOC + generate tex)
            try:
                tex_path, title = process_file(md_path, cat_name, base_name)
                print(f"  ✓ MD cleaned: {md_path}")
                print(f"  ✓ TEX generated: {tex_path}")
                success_md += 1
                success_tex += 1
            except Exception as e:
                print(f"  ✗ MD/TEX ERROR: {e}")
                continue

            # Compile PDF
            try:
                ok, err = compile_tex(tex_path, cat_name, os.path.basename(str(tex_path)))
                if ok:
                    pdf_path = PDF_DIR / cat_name / f'{base_name}.pdf'
                    size_kb = os.path.getsize(str(pdf_path)) / 1024
                    print(f"  ✓ PDF compiled: {pdf_path} ({size_kb:.0f} KB)")
                    success_pdf += 1
                    results.append((cat_name, base_name, 'OK', size_kb))
                else:
                    print(f"  ✗ PDF compile FAILED")
                    # Show last part of log
                    log_path = PDF_DIR / cat_name / f'{base_name}.log'
                    if log_path.exists():
                        with open(log_path, 'r') as lf:
                            log_tail = lf.read()[-1000:]
                        # Find error messages
                        errors = re.findall(r'^!(.*)', log_tail, re.MULTILINE)
                        for err_line in errors[-5:]:
                            print(f"    Error: {err_line[:120]}")
                    results.append((cat_name, base_name, 'PDF FAILED', 0))
            except Exception as e:
                print(f"  ✗ PDF ERROR: {e}")
                results.append((cat_name, base_name, f'ERROR: {e}', 0))

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"  Markdown files cleaned: {success_md}")
    print(f"  LaTeX files generated: {success_tex}")
    print(f"  PDF files compiled: {success_pdf}")

    for cat, name, status, size in results:
        icon = "✓" if status == 'OK' else "✗"
        size_str = f" ({size:.0f} KB)" if size else ""
        print(f"  {icon} [{cat}] {name}{size_str}  {status}")


if __name__ == "__main__":
    main()
