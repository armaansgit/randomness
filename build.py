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

        if re.match(r'^---+\s*$', line) or re.match(r'^\*\*\*+\s*$', line):
            out.append(close_list())
            out.append('<hr>\n')
            i += 1
            continue

        m = re.match(r'^(#{1,6})\s+(.*)', line)
        if m:
            out.append(close_list())
            level = len(m.group(1))
            text = inline(m.group(2))
            out.append(f'<h{level}>{text}</h{level}>\n')
            i += 1
            continue

        m = re.match(r'^[\-\*]\s+(.*)', line)
        if m:
            if not in_ul:
                out.append(close_list())
                in_ul = True
                out.append('<ul>\n')
            out.append(f'<li>{inline(m.group(1))}</li>\n')
            i += 1
            continue

        m = re.match(r'^\d+\.\s+(.*)', line)
        if m:
            if not in_ol:
                out.append(close_list())
                in_ol = True
                out.append('<ol>\n')
            out.append(f'<li>{inline(m.group(1))}</li>\n')
            i += 1
            continue

        m = re.match(r'^>\s*(.*)', line)
        if m:
            out.append(close_list())
            out.append(f'<blockquote>{inline(m.group(1))}</blockquote>\n')
            i += 1
            continue

        if line.strip() == '':
            out.append(close_list())
            i += 1
            continue

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
    text = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', r'<img src="\2" alt="\1">', text)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'__(.+?)__', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    text = re.sub(r'_(.+?)_', r'<em>\1</em>', text)
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
    background:#8ECAE6;
    color:#8B1A1A;
    font-family:'Departure Mono',monospace;
    font-size:14px;
    line-height:1.6;
    min-height:100vh;
    transition:background 0.3s,color 0.3s;
}}
#grain-overlay{{
    position:fixed;top:0;left:0;width:100%;height:100%;
    pointer-events:none;z-index:998;opacity:0;
    background-repeat:repeat;background-size:200px 200px;
    transition:opacity 0.2s;
}}
header{{
    position:sticky;top:0;
    background:rgba(142,202,230,0.92);
    padding:6px 8px;
    backdrop-filter:blur(8px);
    display:flex;justify-content:space-between;align-items:baseline;
    z-index:100;
    transition:background 0.3s;
}}
header .name{{font-weight:bold;font-size:14px}}
main{{padding:8px}}
h1{{font-size:16px;margin:20px 0 6px 0}}
h1:first-child{{margin-top:0}}
h2{{font-size:14px;margin:16px 0 4px 0}}
h3{{font-size:14px;margin:12px 0 4px 0}}
p{{margin-bottom:8px}}
a{{color:inherit;opacity:0.7;text-decoration:underline}}
a:hover{{opacity:1}}
strong{{font-weight:bold}}
hr{{border:none;height:1px;background:currentColor;opacity:0.15;margin:20px 0}}
ul,ol{{margin:0 0 8px 18px}}
li{{margin-bottom:2px}}
blockquote{{border-left:2px solid currentColor;opacity:0.6;padding-left:8px;font-style:italic;margin:8px 0}}
code{{background:rgba(128,128,128,0.15);padding:1px 3px;font-family:'Departure Mono',monospace;font-size:14px}}
pre{{background:rgba(128,128,128,0.12);border:1px solid rgba(128,128,128,0.2);padding:8px;margin:8px 0;overflow-x:auto}}
pre code{{background:none;padding:0}}
img{{max-width:100%;margin:8px 0}}

/* palette button */
#pal-btn{{
    position:fixed;bottom:16px;right:16px;
    width:34px;height:34px;border-radius:50%;
    border:1px solid rgba(128,128,128,0.25);
    background:rgba(200,200,200,0.15);
    backdrop-filter:blur(10px);
    cursor:pointer;font-size:17px;z-index:1001;
    display:flex;align-items:center;justify-content:center;
    font-family:'Departure Mono',monospace;
    transition:transform 0.2s,background 0.2s;
    color:inherit;
}}
#pal-btn:hover{{transform:scale(1.12);background:rgba(200,200,200,0.28)}}

/* palette panel */
#pal{{
    position:fixed;bottom:60px;right:16px;
    background:rgba(18,18,18,0.95);
    color:#e0e0e0;
    border-radius:14px;
    padding:16px;width:196px;
    font-family:'Departure Mono',monospace;
    font-size:11px;z-index:1000;
    backdrop-filter:blur(24px);
    border:1px solid rgba(255,255,255,0.07);
    display:none;
    box-shadow:0 8px 32px rgba(0,0,0,0.4);
}}
#pal.open{{display:block}}
.pl{{
    color:#666;font-size:10px;
    letter-spacing:0.12em;
    margin-bottom:8px;margin-top:14px;
}}
.pl:first-child{{margin-top:0}}
.pm{{display:flex;gap:5px}}
.pm button{{
    flex:1;padding:5px 0;
    border:1px solid rgba(255,255,255,0.1);
    background:transparent;color:#999;
    border-radius:7px;cursor:pointer;
    font-family:'Departure Mono',monospace;font-size:11px;
    transition:all 0.15s;
}}
.pm button:hover{{color:#fff;border-color:rgba(255,255,255,0.25)}}
.pm button.active{{
    background:rgba(255,255,255,0.15);
    color:#fff;border-color:rgba(255,255,255,0.3);
}}
.pc{{display:flex;gap:7px;flex-wrap:wrap}}
.sw{{
    width:26px;height:26px;border-radius:50%;
    cursor:pointer;
    box-shadow:inset 0 0 0 2px rgba(255,255,255,0);
    outline:2px solid transparent;
    outline-offset:2px;
    transition:transform 0.15s,outline-color 0.15s;
}}
.sw:hover{{transform:scale(1.18)}}
.sw.active{{outline-color:rgba(255,255,255,0.8)}}
#gr{{
    width:100%;margin-top:8px;
    accent-color:#888;
    cursor:pointer;height:4px;
}}
</style>
</head>
<body>
<div id="grain-overlay"></div>
<header>
<span class="name">яaид0mnэss</span>
</header>
<main>
{content}
</main>

<button id="pal-btn" onclick="document.getElementById('pal').classList.toggle('open')" title="Theme">◑</button>

<div id="pal">
  <div class="pl">MODE</div>
  <div class="pm">
    <button id="m-l" onclick="setMode('light')">light</button>
    <button id="m-d" onclick="setMode('dark')">dark</button>
  </div>
  <div class="pl">COLOR</div>
  <div class="pc">
    <span class="sw" data-color="#F5F0E8" style="background:#F5F0E8" onclick="setBg(this.dataset.color)"></span>
    <span class="sw" data-color="#8ECAE6" style="background:#8ECAE6" onclick="setBg(this.dataset.color)"></span>
    <span class="sw" data-color="#B5C4D6" style="background:#B5C4D6" onclick="setBg(this.dataset.color)"></span>
    <span class="sw" data-color="#D4B5B5" style="background:#D4B5B5" onclick="setBg(this.dataset.color)"></span>
    <span class="sw" data-color="#E8D5B7" style="background:#E8D5B7" onclick="setBg(this.dataset.color)"></span>
    <span class="sw" data-color="#1C1C1C" style="background:#1C1C1C" onclick="setBg(this.dataset.color)"></span>
  </div>
  <div class="pl">GRAIN</div>
  <input type="range" id="gr" min="0" max="100" value="0" oninput="setGrain(this.value)">
</div>

<script>
(function() {{
  var grainSVG = "<svg xmlns='http://www.w3.org/2000/svg' width='200' height='200'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.75' numOctaves='4' stitchTiles='stitch'/><feColorMatrix type='saturate' values='0'/></filter><rect width='200' height='200' filter='url(#n)' opacity='1'/></svg>";
  var grainURL = 'data:image/svg+xml;base64,' + btoa(grainSVG);
  var overlay = document.getElementById('grain-overlay');
  overlay.style.backgroundImage = 'url("' + grainURL + '")';

  var defaults = {{"mode":"light","bg":"#8ECAE6","grain":0}};
  var state;
  try {{ state = JSON.parse(localStorage.getItem('rnd_pal')) || defaults; }}
  catch(e) {{ state = defaults; }}

  function hexToRgb(hex) {{
    var r = parseInt(hex.slice(1,3),16);
    var g = parseInt(hex.slice(3,5),16);
    var b = parseInt(hex.slice(5,7),16);
    return r+','+g+','+b;
  }}

  function apply() {{
    var isDark = state.mode === 'dark';
    document.body.style.background = state.bg;
    document.body.style.color = isDark ? '#e8e8e8' : '#8B1A1A';
    var rgb = hexToRgb(state.bg);
    document.querySelector('header').style.background = isDark
      ? 'rgba(0,0,0,0.88)'
      : 'rgba('+rgb+',0.92)';
    overlay.style.opacity = (state.grain / 100) * 0.55;
    document.getElementById('gr').value = state.grain;

    document.querySelectorAll('.pm button').forEach(function(b) {{ b.classList.remove('active'); }});
    var mb = document.getElementById(isDark ? 'm-d' : 'm-l');
    if (mb) mb.classList.add('active');

    document.querySelectorAll('.sw').forEach(function(s) {{
      s.classList.toggle('active', s.dataset.color === state.bg);
    }});

    try {{ localStorage.setItem('rnd_pal', JSON.stringify(state)); }} catch(e) {{}}
  }}

  window.setMode = function(m) {{ state.mode = m; apply(); }};
  window.setBg   = function(c) {{ state.bg = c; apply(); }};
  window.setGrain= function(v) {{ state.grain = parseInt(v); apply(); }};

  apply();
}})();
</script>
</body>
</html>'''

    with open('index.html', 'w') as f:
        f.write(page)

    print('done. everything.md → index.html')


if __name__ == '__main__':
    build()
