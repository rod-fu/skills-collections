#!/usr/bin/env python3
import argparse
import html
import json
import re
import shutil
from pathlib import Path


def slugify(value, fallback):
    value = re.sub(r"[^a-zA-Z0-9\u4e00-\u9fff]+", "-", value).strip("-").lower()
    return value or fallback


def render_slide(slide, index, theme):
    title = html.escape(slide.get("title", f"Page {index}"))
    motif = html.escape(slide.get("motif", ""))
    layout = html.escape(slide.get("layout", ""))
    visual = html.escape(slide.get("visual", ""))
    notes = html.escape(slide.get("notes", ""))
    bullets = slide.get("bullets", [])
    bullet_html = "\n".join(f"<li>{html.escape(str(item))}</li>" for item in bullets[:5])
    accent = html.escape(theme.get("accent", "oklch(62% 0.12 245)"))
    bg = html.escape(theme.get("background", "oklch(96% 0.02 80)"))
    fg = html.escape(theme.get("foreground", "oklch(18% 0.03 250)"))
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <style>
    * {{ box-sizing: border-box; }}
    html, body {{ margin: 0; width: 100%; height: 100%; background: {bg}; color: {fg}; }}
    body {{ font-family: Inter, "Noto Sans SC", "Microsoft YaHei", sans-serif; text-wrap: pretty; }}
    .slide {{ width: 100vw; height: 100vh; aspect-ratio: 16 / 9; padding: 6vh 6vw; display: grid; grid-template-columns: 1.15fr .85fr; gap: 4vw; align-items: center; }}
    .kicker {{ font-size: clamp(14px, 1.2vw, 18px); letter-spacing: .08em; text-transform: uppercase; color: {accent}; font-weight: 700; }}
    h1 {{ margin: 2vh 0; font-size: clamp(52px, 6.6vw, 124px); line-height: .95; letter-spacing: 0; max-width: 11ch; }}
    ul {{ margin: 4vh 0 0; padding: 0; list-style: none; display: grid; gap: 1.2vh; }}
    li {{ font-size: clamp(20px, 2vw, 34px); line-height: 1.16; border-top: 1px solid color-mix(in oklch, {fg}, transparent 78%); padding-top: 1.1vh; }}
    .panel {{ border-left: 4px solid {accent}; padding-left: 2vw; display: grid; gap: 2.4vh; }}
    .label {{ font-size: clamp(14px, 1vw, 18px); color: color-mix(in oklch, {fg}, transparent 30%); }}
    .value {{ font-size: clamp(20px, 1.7vw, 30px); line-height: 1.25; }}
    .notes {{ position: fixed; left: 6vw; bottom: 3vh; right: 6vw; font-size: 13px; color: color-mix(in oklch, {fg}, transparent 52%); }}
  </style>
</head>
<body>
  <main class="slide">
    <section>
      <div class="kicker">Page {index:02d}</div>
      <h1>{title}</h1>
      <ul>{bullet_html}</ul>
    </section>
    <aside class="panel">
      <div><div class="label">视觉母题</div><div class="value">{motif}</div></div>
      <div><div class="label">版式方案</div><div class="value">{layout}</div></div>
      <div><div class="label">核心视觉/图表</div><div class="value">{visual}</div></div>
    </aside>
  </main>
  <div class="notes">{notes}</div>
</body>
</html>"""


def main():
    parser = argparse.ArgumentParser(description="Scaffold a multi-page HTML deck from JSON.")
    parser.add_argument("outline_json", help="JSON with title, theme, slides[]")
    parser.add_argument("output_dir")
    parser.add_argument("--asset-dir", default=str(Path(__file__).resolve().parents[1] / "assets"))
    args = parser.parse_args()

    outline = json.loads(Path(args.outline_json).read_text(encoding="utf-8"))
    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)

    theme = outline.get("theme", {})
    manifest = []
    for idx, slide in enumerate(outline.get("slides", []), start=1):
        name = f"{idx:02d}-{slugify(slide.get('title', ''), 'slide')}.html"
        (out / name).write_text(render_slide(slide, idx, theme), encoding="utf-8")
        manifest.append({"title": slide.get("title", f"Page {idx}"), "src": name})

    template = Path(args.asset_dir) / "deck_index.html"
    index = template.read_text(encoding="utf-8")
    index = index.replace("__DECK_TITLE__", html.escape(outline.get("title", "演示文稿")))
    index = index.replace("__MANIFEST_JSON__", json.dumps(manifest, ensure_ascii=False, indent=2))
    (out / "index.html").write_text(index, encoding="utf-8")
    shutil.copyfile(Path(args.asset_dir) / "animations.jsx", out / "animations.jsx")
    print(json.dumps({"output": str(out), "slides": len(manifest), "index": str(out / "index.html")}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
