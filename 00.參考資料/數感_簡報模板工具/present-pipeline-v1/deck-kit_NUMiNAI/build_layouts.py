# -*- coding: utf-8 -*-
"""build_layouts.py — 從 layouts/ 組裝出 all-layouts-demo.html。

這支腳本是「組裝合約」的可執行版（人讀版見 slide-system.md「組裝合約」一節）：
present 把選好的版型組成一份 deck 時，照同一套規則做。

單一真相＝layouts/<name>.html（一型一檔，手改這裡）。
本檔把它們按正典順序組成一份完整 deck：
  ‧ 一個 <head>：連 base.css + 合併各版型 CSS（依 selector 去重，共用的 .ph/.spec 只留一份）
  ‧ logo <symbol> 只放一份
  ‧ 各版型的 <section> 依序串接，page-label 頁碼重新編號（01,02,...）
  ‧ 腳本擺結尾（presenter.js / slide-audit.js）

用途：present 的組裝範例 ＋ check_deck 整合測試（改完任一版型後跑
  `PYTHONUTF8=1 PYTHONIOENCODING=utf-8 python check_deck.py all-layouts-demo.html`
  應 0 FAIL，證明 13 版型仍能組成合法 deck）。

用法：python build_layouts.py
"""
import re, os, sys

KIT = os.path.dirname(os.path.abspath(__file__))
LAYOUTS = os.path.join(KIT, "layouts")
OUT = os.path.join(KIT, "all-layouts-demo.html")

# 正典版型順序（＝組裝後的頁序）
ORDER = ["cover","photo-cover","chapter","hero","grid","cards","spotlight","rows","split",
         "kpi","stats","breather","flow","steps","video-poster","thanks"]

def read_layout(name):
    p = os.path.join(LAYOUTS, f"{name}.html")
    if not os.path.exists(p):
        print(f"  [warn] 缺 layouts/{name}.html，跳過"); return None
    return open(p, encoding="utf-8").read()

def style_of(html):
    m = re.search(r"<style>(.*?)</style>", html, re.S)
    return m.group(1).strip() if m else ""

def section_of(html):
    m = re.search(r"(<section\b.*?</section>)", html, re.S)
    return m.group(1) if m else ""

def symbol_of(html):
    m = re.search(r"(<svg width=\"0\".*?</svg>)", html, re.S)
    return m.group(1) if m else ""

def rules_of(style):
    """切成 (selector, body) 規則清單（這套 CSS 無巢狀大括號、無 @-rule）。"""
    return [(s.strip(), b.strip()) for s, b in re.findall(r"([^{}]+)\{([^{}]*)\}", style)]

def main():
    merged_rules = {}       # selector -> body（去重：共用 .ph/.spec 只留一份）
    order_rules = []        # 保順序的 selector 清單
    sections = []
    symbol = ""
    for name in ORDER:
        html = read_layout(name)
        if not html: continue
        if not symbol:
            symbol = symbol_of(html)
        for sel, body in rules_of(style_of(html)):
            if sel not in merged_rules:
                merged_rules[sel] = body
                order_rules.append(sel)
        sections.append(section_of(html))

    # 頁碼重新編號：每個 section 的第一個 page-label__num → 序號
    renumbered = []
    for i, sec in enumerate(sections, start=1):
        sec = re.sub(r'(<span class="page-label__num">)\d+(</span>)',
                     rf'\g<1>{i:02d}\g<2>', sec, count=1)
        renumbered.append(sec)

    css = "\n".join(f"{sel} {{{merged_rules[sel]}}}" for sel in order_rules)
    body_sections = "\n\n".join(renumbered)

    out = f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>全版型展示 — 數感實驗室簡報系統（由 layouts/ 組裝・勿手改）</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="base.css">
<style>
/* ⚠ 本檔由 build_layouts.py 從 layouts/ 自動組裝，請勿手改；改版型請改 layouts/<name>.html 再重跑。 */
{css}
</style>
</head>
<body>
{symbol}
<div class="deck">

{body_sections}

</div>
<script src="presenter.js"></script>
<script src="slide-audit.js"></script>
</body>
</html>
"""
    open(OUT, "w", encoding="utf-8").write(out)
    print(f"DONE: 組裝 {len(sections)} 版型 → {os.path.basename(OUT)}（{len(order_rules)} 條 CSS 規則）")

if __name__ == "__main__":
    main()
