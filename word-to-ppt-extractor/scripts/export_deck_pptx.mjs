#!/usr/bin/env node
import { readFile, mkdir } from "node:fs/promises";
import path from "node:path";

async function loadPptxGen() {
  try {
    const mod = await import("pptxgenjs");
    return mod.default || mod;
  } catch (error) {
    throw new Error("缺少 pptxgenjs。请在可用的 Node 运行时中安装或加载 pptxgenjs 后再导出 PPTX。");
  }
}

const input = process.argv[2];
const output = process.argv[3] || "deck.pptx";

if (!input) {
  console.error("用法: node export_deck_pptx.mjs <outline.json> [output.pptx]");
  process.exit(1);
}

const PptxGenJS = await loadPptxGen();
const outline = JSON.parse(await readFile(input, "utf-8"));
const pptx = new PptxGenJS();
pptx.layout = "LAYOUT_WIDE";
pptx.author = "Codex word-to-ppt-extractor";
pptx.subject = outline.title || "Huashu Design Deck";
pptx.title = outline.title || "Deck";
pptx.company = "Huashu Design";
pptx.lang = "zh-CN";
pptx.theme = {
  headFontFace: "Microsoft YaHei",
  bodyFontFace: "Microsoft YaHei",
  lang: "zh-CN",
};

const theme = outline.theme || {};
const bg = theme.backgroundHex || "F7F3EA";
const fg = theme.foregroundHex || "1B1B1F";
const accent = theme.accentHex || "2D5BFF";

for (const [i, item] of (outline.slides || []).entries()) {
  const slide = pptx.addSlide();
  slide.background = { color: bg };
  slide.addText(`Page ${String(i + 1).padStart(2, "0")}`, {
    x: 0.55, y: 0.35, w: 1.4, h: 0.25, fontSize: 10, bold: true, color: accent,
  });
  slide.addText(item.title || `Page ${i + 1}`, {
    x: 0.55, y: 0.9, w: 6.4, h: 1.6, fontSize: 34, bold: true, color: fg, margin: 0.03,
    fit: "shrink",
  });
  const bullets = (item.bullets || []).slice(0, 5).map((text) => ({ text: String(text), options: { bullet: { type: "ul" } } }));
  slide.addText(bullets, {
    x: 0.75, y: 2.85, w: 5.7, h: 2.1, fontSize: 18, color: fg, breakLine: false, fit: "shrink",
  });
  slide.addShape(pptx.ShapeType.line, { x: 7.1, y: 0.85, w: 0, h: 5.0, line: { color: accent, width: 2 } });
  slide.addText(`视觉母题\n${item.motif || ""}\n\n版式方案\n${item.layout || ""}\n\n核心视觉\n${item.visual || ""}`, {
    x: 7.35, y: 0.9, w: 5.2, h: 4.6, fontSize: 14, color: fg, valign: "mid", fit: "shrink",
  });
  if (item.notes) {
    slide.addNotes(String(item.notes));
  }
}

await mkdir(path.dirname(path.resolve(output)), { recursive: true });
await pptx.writeFile({ fileName: output });
console.log(JSON.stringify({ output: path.resolve(output) }, null, 2));
