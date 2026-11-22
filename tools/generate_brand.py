#!/usr/bin/env python3
"""Generate CASbench's organization identity from its existing matrix mark.

Run from any directory: python3 -I tools/generate_brand.py
Set RSVG_CONVERT to the path of rsvg-convert to also render PNG avatars.
"""
from pathlib import Path
import os
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "profile" / "assets"
INK = "#1E2329"
PAPER = "#F4F1EA"
STEEL = "#8A949E"
ACCENT = "#F2B705"
VERIFIED = "#2E9E5B"


def matrix(x, y, size):
    """The original three-by-three results matrix, at the requested scale."""
    cells = (("filled", "filled", "hollow"),
             ("filled", "empty", "filled"),
             ("hollow", "filled", "filled"))
    unit = size / 3
    parts = [f'<g transform="translate({x} {y})">',
             f'<rect x="0" y="0" width="{size}" height="{size}" rx="{size * .06:.2f}" '
             f'fill="none" stroke="{STEEL}" stroke-opacity=".7" stroke-width="{size * .025:.2f}"/>']
    for row, values in enumerate(cells):
        for col, kind in enumerate(values):
            if kind == "empty":
                continue
            cx, cy = (col + .5) * unit, (row + .5) * unit
            r = unit * .28
            paint = (f'fill="{VERIFIED}"' if kind == "filled" else
                     f'fill="none" stroke="{ACCENT}" stroke-width="{unit * .10:.2f}"')
            parts.append(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r:.2f}" {paint}/>')
    parts.append('</g>')
    return "\n".join(parts)


def logo(background):
    bg = f'<rect width="512" height="512" fill="{INK}"/>' if background else ""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512" role="img" aria-labelledby="title">
<title id="title">CASbench organization mark</title>
{bg}
{matrix(104, 104, 304)}
</svg>
'''


def banner():
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 300" width="1280" height="300" role="img" aria-labelledby="title desc">
<title id="title">CASbench</title>
<desc id="desc">Computer algebra benchmarks: reproducible, verified and dated.</desc>
<defs><pattern id="grid" width="8" height="8" patternUnits="userSpaceOnUse"><path d="M8 0H0V8" fill="none" stroke="{STEEL}" stroke-opacity=".13" stroke-width=".5"/></pattern></defs>
<rect width="1280" height="300" fill="{INK}"/>
<rect width="1280" height="300" fill="url(#grid)"/>
{matrix(66, 58, 184)}
<g font-family="IBM Plex Mono, JetBrains Mono, ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">
<text x="303" y="125" font-size="60" font-weight="700" fill="{PAPER}">CAS<tspan fill="{ACCENT}" font-weight="400">bench</tspan></text>
<text x="306" y="171" font-size="23" fill="{PAPER}">Computer algebra benchmarks</text>
<text x="306" y="210" font-size="19" fill="{STEEL}">reproducible · verified · dated</text>
</g>
</svg>
'''


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, svg in (("casbench-logo.svg", logo(True)),
                      ("casbench-logo-transparent.svg", logo(False)),
                      ("casbench-banner.svg", banner())):
        (OUT / name).write_text(svg, encoding="utf-8")
    renderer = os.environ.get("RSVG_CONVERT") or shutil.which("rsvg-convert")
    if renderer:
        for size in (512, 1024):
            subprocess.run([renderer, "--width", str(size), "--height", str(size), "--output",
                            str(OUT / f"casbench-avatar-{size}.png"), str(OUT / "casbench-logo.svg")], check=True)
    else:
        print("SVG files written; set RSVG_CONVERT to render the PNG avatars.")


if __name__ == "__main__":
    main()
