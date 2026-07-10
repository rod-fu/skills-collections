#!/usr/bin/env bash
set -euo pipefail

deck_dir="${1:-.}"
bgm="${2:-}"
sfx="${3:-}"

if [[ ! -f "$deck_dir/index.html" ]]; then
  echo "未找到 $deck_dir/index.html" >&2
  exit 1
fi

if [[ -z "$bgm" && -z "$sfx" ]]; then
  echo "未提供音频文件，跳过注入。"
  exit 0
fi

python_bin="${PYTHON:-}"
if [[ -z "$python_bin" ]]; then
  if command -v python3 >/dev/null 2>&1; then
    python_bin="python3"
  elif command -v python >/dev/null 2>&1; then
    python_bin="python"
  else
    echo "未找到 python/python3，无法注入音频。" >&2
    exit 1
  fi
fi

"$python_bin" - "$deck_dir/index.html" "$bgm" "$sfx" <<'PY'
from pathlib import Path
import sys

index = Path(sys.argv[1])
bgm = sys.argv[2]
sfx = sys.argv[3]
html = index.read_text(encoding="utf-8")
snippet = "\n".join([
    f'<audio id="deck-bgm" src="{bgm}" preload="auto" loop></audio>' if bgm else "",
    f'<audio id="deck-sfx" src="{sfx}" preload="auto"></audio>' if sfx else "",
    "<script>window.playDeckSfx=()=>document.getElementById('deck-sfx')?.play?.().catch(()=>{});</script>",
])
if "deck-bgm" not in html and "deck-sfx" not in html:
    html = html.replace("</body>", snippet + "\n</body>")
index.write_text(html, encoding="utf-8")
print(f"已注入音频: {index}")
PY
