#!/usr/bin/env node
import { mkdir } from "node:fs/promises";
import path from "node:path";
import { pathToFileURL } from "node:url";

async function loadPlaywright() {
  try {
    return await import("playwright");
  } catch (error) {
    throw new Error("缺少 playwright。请在可用的 Node 运行时中安装或加载 playwright 后再导出 PDF。");
  }
}

const input = process.argv[2];
const output = process.argv[3] || "deck.pdf";

if (!input) {
  console.error("用法: node export_deck_pdf.mjs <index.html|url> [output.pdf]");
  process.exit(1);
}

const { chromium } = await loadPlaywright();
await mkdir(path.dirname(path.resolve(output)), { recursive: true });
const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
const target = /^https?:\/\//.test(input) ? input : pathToFileURL(path.resolve(input)).href;
await page.goto(target, { waitUntil: "networkidle" });
await page.pdf({
  path: output,
  width: "1920px",
  height: "1080px",
  printBackground: true,
  preferCSSPageSize: false,
});
await browser.close();
console.log(JSON.stringify({ output: path.resolve(output) }, null, 2));
