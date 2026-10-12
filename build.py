#!/usr/bin/env python3
"""
build.py — converts everything.md into index.html
usage: python3 build.py
"""

import re
import html

def md_to_html(md):
    """dead simple markdown to html. no libraries needed."""
    lines = md.split('\n')
    out = []
    in_code_block = False
    in_ul = False
    in_ol = False
    code_lines = []

    def close_list():
        nonlocal in_ul, in_ol
        result = ''
        if in_ul:
            result = '</ul>\n'
            in_ul = False
        if in_ol:
            result = '</ol>\n'
            in_ol = False
        return result

    i = 0
    while i < len(lines):
        line = lines[i]

        # fenced code blocks
        if line.strip().startswith('```'):
            if not in_code_block:
                out.append(close_list())
                in_code_block = True
                code_lines = []
            else:
                in_code_block = False
                code_content = html.escape('\n'.join(code_lines))
                out.append(f'<pre><code>{code_content}</code></pre>\n')
            i += 1
            continue

        if in_code_block:
            code_lines.append(line)
            i += 1
            continue

        # horizontal rule
        if re.match(r'^---+\s*$', line) or re.match(r'^\*\*\*+\s*$', line):
            out.append(close_list())
            out.append('<hr>\n')
            i += 1
            continue

        # headings
        m = re.match(r'^(#{1,6})\s+(.*)', line)
        if m:
            out.append(close_list())
            level = len(m.group(1))
            text = inline(m.group(2))
            out.append(f'<h{level}>{text}</h{level}>\n')
            i += 1
            continue

        # unordered list
        m = re.match(r'^[\-\*]\s+(.*)', line)
        if m:
            if not in_ul:
                out.append(close_list())
                in_ul = True
                out.append('<ul>\n')
            out.append(f'<li>{inline(m.group(1))}</li>\n')
            i += 1
            continue

        # ordered list
        m = re.match(r'^\d+\.\s+(.*)', line)
        if m:
            if not in_ol:
                out.append(close_list())
                in_ol = True
                out.append('<ol>\n')
            out.append(f'<li>{inline(m.group(1))}</li>\n')
            i += 1
            continue

        # blockquote
        m = re.match(r'^>\s*(.*)', line)
        if m:
            out.append(close_list())
            out.append(f'<blockquote>{inline(m.group(1))}</blockquote>\n')
            i += 1
            continue

        # blank line
        if line.strip() == '':
            out.append(close_list())
            i += 1
            continue

        # paragraph
        out.append(close_list())
        para_lines = []
        while i < len(lines) and lines[i].strip() != '' and not lines[i].startswith('#') and not lines[i].startswith('```') and not re.match(r'^---+\s*$', lines[i]) and not re.match(r'^[\-\*]\s+', lines[i]) and not re.match(r'^\d+\.\s+', lines[i]) and not re.match(r'^>\s', lines[i]):
            para_lines.append(lines[i])
            i += 1
        out.append(f'<p>{inline("<br>".join(para_lines))}</p>\n')
        continue

    out.append(close_list())
    return ''.join(out)


def inline(text):
    """handle inline markdown: bold, italic, code, links, images"""
    # images
    text = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', r'<img src="\2" alt="\1">', text)
    # links
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
    # bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'__(.+?)__', r'<strong>\1</strong>', text)
    # italic
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    text = re.sub(r'_(.+?)_', r'<em>\1</em>', text)
    # inline code
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    return text


def build():
    with open('everything.md', 'r') as f:
        md = f.read()

    content = md_to_html(md)

    page = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>яaид0mnэss</title>
<style>
@font-face {{
    font-family: 'Departure Mono';
    src: url('DepartureMono-Regular.woff2') format('woff2'),
         url('DepartureMono-Regular.otf') format('opentype');
    font-weight: normal;
    font-style: normal;
}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{
    background:#fff;
    color:#000;
    font-family:'Departure Mono',monospace;
    font-size:14px;
    line-height:1.6;
    min-height:100vh;
    position:relative;
}}
body::before {{
    content:"";
    position:fixed;
    top:0;
    left:0;
    width:100vw;
    height:100vh;
    background-image:url('bg.png');
    background-position:center;
    background-size:cover;
    background-repeat:no-repeat;
    opacity:0.35;
    z-index:-1;
    pointer-events:none;
}}
header{{
    position:sticky;
    top:0;
    background:rgba(255,255,255,0.85);
    padding:6px 8px;
    backdrop-filter:blur(8px);
    display:flex;
    justify-content:space-between;
    align-items:baseline;
}}
header .name{{font-weight:bold;font-size:14px}}
main{{padding:8px}}
h1{{font-size:16px;margin:20px 0 6px 0}}
h1:first-child{{margin-top:0}}
h2{{font-size:14px;margin:16px 0 4px 0}}
h3{{font-size:14px;margin:12px 0 4px 0}}
p{{margin-bottom:8px}}
a{{color:#0000ee}}
a:visited{{color:#551a8b}}
a:hover{{color:#0000ee}}
strong{{font-weight:bold}}
hr{{border:none;height:1px;background:rgba(0,0,0,0.2);margin:20px 0}}
ul,ol{{margin:0 0 8px 18px}}
li{{margin-bottom:2px}}
blockquote{{border-left:2px solid #ccc;padding-left:8px;color:#555;font-style:italic;margin:8px 0}}
code{{background:rgba(240,240,240,0.7);padding:1px 3px;font-family:'Departure Mono',monospace;font-size:14px}}
pre{{background:rgba(240,240,240,0.7);border:1px solid #ddd;padding:8px;margin:8px 0;overflow-x:auto}}
pre code{{background:none;padding:0}}
img{{max-width:100%;margin:8px 0}}
</style>
</head>
<body>
<header>
<span class="name">яaид0mnэss</span>
</header>
<main>
{content}
</main>
</body>
</html>'''

    with open('index.html', 'w') as f:
        f.write(page)

    print('done. everything.md → index.html')


if __name__ == '__main__':
    build()
