#!/usr/bin/env python3
"""
Generate a sleek, neofetch-style info card SVG with staggered line fade-ins.
Reads structured details and outputs info-card.svg.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "info-card.svg")

CANVAS_W = 560
CANVAS_H = 586
PAD = 26
TITLEBAR_H = 34

BG = "#0d1117"
BG2 = "#111722"
FRAME = "#30363d"
TITLE_TEXT = "#7d8590"
TEXT_MUTED = "#8b949e"
TEXT_MAIN = "#c9d1d9"
TEXT_WHITE = "#f0f6fc"

# Accent colors
CYAN = "#38bdf8"
GREEN = "#4ade80"
YELLOW = "#fbbf24"
PURPLE = "#c084fc"
PINK = "#f472b6"
BLUE = "#60a5fa"
ORANGE = "#fb923c"

lines = [
    ("title", "nirmal", "@", "reignofoptimus"),
    ("divider", "---------------------------------------------"),
    ("field", "OS", "Arch Linux x86_64 / Web / Cloud", CYAN),
    ("field", "Host", "B.Tech CS & Design @ FISAT (KTU)", PURPLE),
    ("field", "Now", "Chair @ IEEE Computer Society FISAT", GREEN),
    ("field", "Prev", "AI & ML Intern @ SRAI Smart Solutions", BLUE),
    ("field", "Stack", "Python, Java, C, JS, Three.js, React, MySQL", YELLOW),
    ("field", "Focus", "Full-Stack Dev, AI Systems & Creative UI", PINK),
    ("field", "Portfolio", "https://nirmalmadhu.vercel.app", ORANGE),
    ("field", "LinkedIn", "linkedin.com/in/nirmal-madhu-523642361", CYAN),
    ("field", "Contact", "nirmalmadhu2005@gmail.com", GREEN),
    ("field", "Status", "Open to collaborations & software roles", PURPLE),
]

# Color blocks like Neofetch
PALETTE_COLORS = [
    "#1f242c", "#ff5f56", "#27c93f", "#f1fa8c", "#bd93f9", "#ff79c6", "#8be9fd", "#f8f8f2"
]

LINE_HEIGHT = 28
START_Y = TITLEBAR_H + 34

css_rules = [
    "@keyframes lineFade {",
    "  0% { opacity: 0; transform: translateY(6px); }",
    "  100% { opacity: 1; transform: translateY(0); }",
    "}",
    ".term-line { opacity: 0; animation: lineFade 0.35s cubic-bezier(0.16, 1, 0.3, 1) forwards; }"
]

parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS_W}" height="{CANVAS_H}" '
    f'viewBox="0 0 {CANVAS_W} {CANVAS_H}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
    f'<style>{" ".join(css_rules)}</style>',
    '<defs>'
    f'<linearGradient id="card-bg" x1="0" y1="0" x2="0" y2="1">'
    f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/>'
    '</linearGradient></defs>',
    f'<rect width="{CANVAS_W}" height="{CANVAS_H}" rx="12" fill="url(#card-bg)"/>',
    f'<rect x="0.5" y="0.5" width="{CANVAS_W-1}" height="{CANVAS_H-1}" rx="12" '
    f'fill="none" stroke="{FRAME}" stroke-width="1"/>',
    f'<line x1="0" y1="{TITLEBAR_H}" x2="{CANVAS_W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>'
]

# Title bar dots
for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dotcol}"/>')
parts.append(f'<text x="{CANVAS_W/2}" y="{TITLEBAR_H/2 + 4}" fill="{TITLE_TEXT}" font-size="12" '
             f'text-anchor="middle">reignofoptimus@github: ~$ neofetch</text>')

# Render lines
curr_y = START_Y
delay = 0.15

for item in lines:
    delay_str = f"animation-delay: {delay:.2f}s;"
    delay += 0.08
    if item[0] == "title":
        _, user, at, host = item
        parts.append(
            f'<g class="term-line" style="{delay_str}">'
            f'<text x="{PAD}" y="{curr_y}" font-size="15" font-weight="700">'
            f'<tspan fill="{CYAN}">{user}</tspan>'
            f'<tspan fill="{TEXT_MUTED}">{at}</tspan>'
            f'<tspan fill="{PURPLE}">{host}</tspan>'
            f'</text></g>'
        )
    elif item[0] == "divider":
        _, text = item
        parts.append(
            f'<g class="term-line" style="{delay_str}">'
            f'<text x="{PAD}" y="{curr_y}" font-size="13" fill="{FRAME}">{text}</text></g>'
        )
    elif item[0] == "field":
        _, key, val, color = item
        parts.append(
            f'<g class="term-line" style="{delay_str}">'
            f'<text x="{PAD}" y="{curr_y}" font-size="13">'
            f'<tspan fill="{color}" font-weight="600">{key:<10}</tspan>'
            f'<tspan fill="{TEXT_MUTED}">:: </tspan>'
            f'<tspan fill="{TEXT_MAIN}">{val}</tspan>'
            f'</text></g>'
        )
    curr_y += LINE_HEIGHT

# Palette color blocks row
delay_str = f"animation-delay: {delay:.2f}s;"
block_w = 18
block_h = 14
parts.append(f'<g class="term-line" style="{delay_str}">')
palette_y = curr_y + 10
for i, color in enumerate(PALETTE_COLORS):
    bx = PAD + i * (block_w + 6)
    parts.append(f'<rect x="{bx}" y="{palette_y}" width="{block_w}" height="{block_h}" rx="3" fill="{color}"/>')
parts.append('</g>')

parts.append("</svg>")
svg = "".join(parts)
with open(OUT, "w", encoding="utf-8") as f:
    f.write(svg)
print(f"wrote {OUT} ({len(svg)} bytes)")
