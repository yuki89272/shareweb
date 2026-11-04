#!/usr/bin/env bash
# shot.sh — 用 headless Chrome 截 deck 的單頁或範圍，方便逐頁驗收
# 用法：
#   ./shot.sh <deck.html> <page>           單頁，輸出到 /tmp/shots/pNN.png
#   ./shot.sh <deck.html> 6-12             範圍
#   ./shot.sh <deck.html> 18 ./out         指定輸出目錄
# 依賴：Google Chrome 或 Edge（headless）。deck 用 presenter.js 的 #N 跳第 N 個 section。
set -euo pipefail

DECK="${1:?用法: shot.sh <deck.html> <page|a-b> [outdir]}"
SPEC="${2:?缺頁碼，例如 18 或 6-12}"
OUT="${3:-/tmp/shots}"
mkdir -p "$OUT"
OUT="$(cd "$OUT" && pwd)"   # 絕對化：headless Chrome/Edge 對相對輸出路徑不可靠（尤其 Windows）

# 找 Chrome
CHROME=""
for c in \
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  "/Applications/Chromium.app/Contents/MacOS/Chromium" \
  "$(command -v google-chrome 2>/dev/null || true)" \
  "$(command -v chromium 2>/dev/null || true)" \
  "/c/Program Files/Google/Chrome/Application/chrome.exe" \
  "/c/Program Files (x86)/Google/Chrome/Application/chrome.exe" \
  "/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe" \
  "/c/Program Files/Microsoft/Edge/Application/msedge.exe"; do
  [ -n "$c" ] && [ -x "$c" ] && CHROME="$c" && break
done
[ -z "$CHROME" ] && { echo "找不到 Chrome/Edge，請改路徑"; exit 1; }

# deck 絕對路徑（給 file:// 用）
ABS="$(cd "$(dirname "$DECK")" && pwd)/$(basename "$DECK")"
# file:// URL：Windows git-bash 的 /c/... 轉成 C:/... 否則 Chrome 認不得
case "$ABS" in
  /[a-zA-Z]/*) URL="file:///$(printf '%s' "$ABS" | sed -E 's#^/([a-zA-Z])/#\1:/#')" ;;
  *)           URL="file://$ABS" ;;
esac

# 解析範圍
if [[ "$SPEC" == *-* ]]; then
  A="${SPEC%-*}"; B="${SPEC#*-}"
else
  A="$SPEC"; B="$SPEC"
fi

for n in $(seq "$A" "$B"); do
  f="$OUT/p$(printf '%02d' "$n").png"
  "$CHROME" --headless=new --disable-gpu --hide-scrollbars \
    --window-size=1600,900 --virtual-time-budget=2800 \
    --screenshot="$f" "$URL#$n" >/dev/null 2>&1
  echo "  $f"
done
echo "完成：$OUT"

# --contact：把這批截圖拼成一張縮圖總覽（需要 python3 + PIL）
if [[ "${4:-}" == "--contact" || "${3:-}" == "--contact" ]]; then
  python3 - "$OUT" <<'PY'
import sys, glob, math
from PIL import Image, ImageDraw
out = sys.argv[1]
files = sorted(glob.glob(out + '/p*.png'))
if files:
    n = len(files)
    cols = min(5, n); rows = math.ceil(n / cols)
    tw, th = 480, 270
    sheet = Image.new('RGB', (cols * tw, rows * th), 'white')
    dr = ImageDraw.Draw(sheet)
    for i, fp in enumerate(files):
        im = Image.open(fp).convert('RGB').resize((tw - 4, th - 22))
        x = (i % cols) * tw; y = (i // cols) * th
        sheet.paste(im, (x + 2, y + 20))
        dr.text((x + 6, y + 4), fp.split('/')[-1][1:3], fill='black')
    sheet.save(out + '/contact.png')
    print('縮圖總覽：' + out + '/contact.png')
PY
fi
