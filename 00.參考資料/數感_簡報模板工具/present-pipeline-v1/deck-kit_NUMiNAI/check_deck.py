#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_deck.py — 數感 HTML 簡報通用體檢 linter
=================================================
一鍵檢查任何用 deck-kit_數感實驗室 做的 deck，擋住常見回歸。

用法：
    python3 check_deck.py <deck.html>                # 體檢（預設含 measure：用 Chrome 量版面溢位/重疊/超框）
    python3 check_deck.py <deck.html> <article.md>   # 多檢「對應原文逐字覆蓋」
    python3 check_deck.py <deck.html> --fix-css      # 順手合併 <style> 內重複 selector（會先備份 .bak）
                                                    #   @keyframes/@media/@supports/@font-face 整段保留不動；
                                                    #   合併前後會比對動畫指紋，不一致就放棄修改。
    python3 check_deck.py <deck.html> --no-measure   # 只跑靜態檢查、不開 Chrome（CI 無瀏覽器時用）
    python3 check_deck.py <deck.html> --measure      # （相容保留；measure 現為預設，加不加同效）

檢查項目：
  1. page-label__num == 該 section 在全 deck 的位置（封面/章節隔頁/收尾不顯示號，但仍佔位）
  2. 所有 <img src="assets/..."> 圖檔存在
  3. 內容字級 ≥ 2vw（--fs-content-min）；同時認 `Nvw` 與自適應的
     「calc(N*var(--u))」（16:9 下 1cqw=1vw，門檻一致）；列出所有 <2 供人工判斷
  4. 可見區（規劃層以外）無 emoji
  5. inline <style> 無重複定義的 selector（手改累積的 override cruft）
  6. 每個內容頁都有 <aside class="plan-note"> 且含 plan-note__source
  7. 不得使用 slide--white class（已知 bug）；每個 section 都有 inline background
  8. （選配，給 article.md）各頁對應原文接起來 ≈ 文章逐字（有序、全覆蓋）
  9. （measure，預設開；需 Chrome）實際渲染量版面：超出 slide 邊界 / 超出 .slide-frame 安全框 /
     頁內有底色或邊框的盒子互相重疊（含 <span> 膠囊）→ FAIL；內文被自身 overflow 裁切 → WARN
     編輯後檢查（2026-09-14）：內容覆蓋 <45%／色塊內容 <40%／最小字 <1.25u → WARN（老師刪字後版面要不要放大、補圖）

退出碼：0 全過；1 有 FAIL。WARN 不影響退出碼。
"""
import sys, os, re
from collections import Counter, OrderedDict

# ---- 內容類 class（字級應 ≥2vw）。其餘視為微標註，可小 ----
CONTENT_FS_CLASSES = (
    'probe-statement__sub', 'probe-split__body', 'probe-compare__col-body',
    'probe-compare__col-label', 'probe-three__col-label', 'probe-three__col-body',
    'probe-points', 'probe-cap', 'probe-question__text', 'probe-conditions__label',
    'probe-conditions__path', 'probe-kpi__label', 'probe-kpi__desc',
    'probe-steps__step-label', 'probe-steps__caption', 'probe-vmul__steps',
    'probe-thanks__body', 'probe-compare__col-title',
)
# 允許 <2vw 的微標註 class（定位用、不影響理解）
MICRO_FS_CLASSES = (
    'img-cite', 'probe-kpi__cite', 'page-label', 'probe-statement__tag',
    'probe-steps__step-num', 'probe-vmul__step-num', 'probe-cover__subtitle',
    'probe-chapter__label', 'brand-footer', 'progress', 'plan-note', 'src-key',
    'mode-hint', 'probe-vmul__carry',
)
# 行內手刻 font-size 的「微標註」class 片段（class 含這些＝定位/出處/徽章，可 <2vw 不算 FAIL）
MICRO_FS_INLINE_RE = re.compile(
    r'__num|__tag|__label|__cite|__caption|__step-num|__carry|__subtitle'
    r'|eyebrow|page-label|brand|img-cite|progress|plan-note|mode-hint|src-key'
)
# 不承載文字、不該套 2vw 內文門檻的標籤（行內 font-size 檢查略過）
NO_TEXT_TAGS = frozenset((
    'img', 'svg', 'path', 'polygon', 'polyline', 'use', 'source', 'video',
    'track', 'br', 'hr', 'input', 'image', 'symbol', 'g', 'rect', 'circle',
    'line', 'ellipse', 'defs',
))
# 語意上即「說明/標註」的標籤：圖說、引用、細則——天生小字，不套 2vw 內文門檻
MICRO_TEXT_TAGS = frozenset(('figcaption', 'caption', 'cite', 'small'))
EMOJI_RE = re.compile(
    '[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F000-\U0001F0FF\U00002B00-\U00002BFF️]'
)

def sections(html):
    """切出每個 <section ...>...</section>，回傳 (start, body) list。"""
    html = re.sub(r'<!--.*?-->', '', html, flags=re.S)   # 先去 HTML 註解，避免註解內字面 <section> 被誤算成一頁
    out = []
    for m in re.finditer(r'<section\b[^>]*>', html):
        s = m.start()
        e = html.find('</section>', s)
        out.append(html[s:e + 10] if e >= 0 else html[s:])
    return out

def section_kind(blk):
    if 'probe-cover' in blk: return 'cover'
    if 'probe-photo' in blk: return 'cover'   # 滿版圖封面＝結構頁（同 cover：免 page-num／plan-note）
    if 'probe-chapter' in blk: return 'chapter'
    if 'probe-thanks' in blk: return 'thanks'
    return 'content'

def _skip_ws_comments(s, i):
    while i < len(s):
        if s[i].isspace():
            i += 1
        elif s.startswith('/*', i):
            j = s.find('*/', i + 2)
            i = len(s) if j < 0 else j + 2
        else:
            break
    return i

def split_style_blocks(style):
    """把 <style> 內容依原順序切成：
         ('at',   原文)          → @keyframes / @media / @supports / @font-face，整段保留不解析
         ('rule', selector, decl) → 頂層一般規則
       @ 區塊裡的 from/to/0%/100% 不是 selector，切開才不會被誤判成重複定義。"""
    out, i, n = [], 0, len(style)
    while True:
        i = _skip_ws_comments(style, i)
        if i >= n:
            break
        start = i
        brace = style.find('{', i)
        if brace < 0:
            break
        head = style[start:brace].strip()
        if head.startswith('@'):
            depth, j = 0, brace
            while j < n:
                if style[j] == '{':
                    depth += 1
                elif style[j] == '}':
                    depth -= 1
                    if depth == 0:
                        break
                j += 1
            out.append(('at', style[start:j + 1]))
            i = j + 1
        else:
            end = style.find('}', brace)
            if end < 0:
                break
            out.append(('rule', head, style[brace + 1:end].strip()))
            i = end + 1
    return out

def parse_style_rules(style):
    """把 CSS 拆成有序 [(selector, decl_str)]；@ 區塊整段跳過（見 split_style_blocks）。"""
    return [(b[1], b[2]) for b in split_style_blocks(style) if b[0] == 'rule']

_KF_RE   = re.compile(r'@keyframes\s+([A-Za-z0-9_-]+)')
_ANIM_RE = re.compile(r'\banimation(?:-name)?\s*:')
def anim_fingerprint(css):
    """動畫指紋：@keyframes 名單＋animation 宣告數。--fix-css 前後必須一致。"""
    return (sorted(_KF_RE.findall(css)), len(_ANIM_RE.findall(css)))

# ---- 字級擷取：同時支援 `Nvw` 與自適應的「calc(N*var(--u))」----
#   16:9 螢幕下 1cqw（=1*--u）= 1vw，故門檻一致，皆換算成 vw 當量比較。
_FS_VW = re.compile(r'font-size:\s*([0-9.]+)vw')
_FS_U  = re.compile(r'font-size:\s*calc\(\s*([0-9.]+)\s*\*\s*var\(--u\)\s*\)')
def fs_vw_equiv(decl):
    """從一段宣告抓 font-size 的 vw 當量；抓不到回 None。"""
    m = _FS_VW.search(decl) or _FS_U.search(decl)
    return float(m.group(1)) if m else None

def decls_to_dict(decl):
    d = OrderedDict()
    for part in decl.split(';'):
        if ':' in part:
            k, v = part.split(':', 1)
            d[k.strip()] = v.strip()
    return d

def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    flags = [a for a in sys.argv[1:] if a.startswith('--')]
    if not args:
        print(__doc__); sys.exit(2)
    deck = args[0]
    article = args[1] if len(args) > 1 else None
    fix_css = '--fix-css' in flags
    deck_dir = os.path.dirname(os.path.abspath(deck))
    html = open(deck, encoding='utf-8').read()

    fails, warns = [], []
    def FAIL(m): fails.append(m)
    def WARN(m): warns.append(m)

    secs = sections(html)

    # 1. page-num == 位置
    for i, blk in enumerate(secs, 1):
        m = re.search(r'page-label__num">(\d+)</span>', blk)
        if m and int(m.group(1)) != i:
            FAIL(f'[頁碼] 第 {i} 個 section 的 page-num={m.group(1)}（應為 {i}）')
        if section_kind(blk) == 'content' and not m:
            WARN(f'[頁碼] 第 {i} 個內容頁沒有 page-label__num')

    # 2. 圖檔存在
    for src in sorted(set(re.findall(r'<img[^>]*src="([^"]+)"', html))):
        if src.startswith(('http://', 'https://', 'data:')):
            continue
        if not os.path.exists(os.path.join(deck_dir, src)):
            FAIL(f'[圖檔] 缺少 {src}')

    # 3. 字級——用 cascade 後的「有效」font-size（同 class 後者覆蓋前者，含群組規則）
    style_m = re.search(r'<style>(.*?)</style>', html, re.S)
    style = style_m.group(1) if style_m else ''
    rules_all = parse_style_rules(style)
    fs_rules = []
    for sel, decl in rules_all:
        fv = fs_vw_equiv(decl)              # 認 Nvw 也認 calc(N*var(--u))
        if fv is not None:
            fs_rules.append((sel, fv))
    for cls in CONTENT_FS_CLASSES:
        eff = None
        for sel, fs in fs_rules:            # 依序掃，最後一個命中的即有效值
            if ('.' + cls) in sel:
                eff = fs
        if eff is not None and eff < 2.0:
            FAIL(f'[字級] 內容類 .{cls} 有效字級 {eff}vw（當量）< 2vw')
    small_vw = re.findall(r'font-size:\s*([01](?:\.\d+)?)vw', html)
    small_u  = re.findall(r'font-size:\s*calc\(\s*([01](?:\.\d+)?)\s*\*\s*var\(--u\)\s*\)', html)
    n_small = len([s for s in (small_vw + small_u) if float(s) < 2.0])
    if n_small:
        WARN(f'[字級] 行內 <2vw 出現 {n_small} 次（多為圖內/微標註，請目視確認非觀眾要讀的句子）')

    # 3b. 手刻 inline style="font-size:…" 的「內容元素」< 2vw → FAIL
    #     （上面 CONTENT_FS_CLASSES 只掃硬編 class；手刻 inline font-size 整個繞過、只剩弱 WARN）
    #     排除：不承載文字/圖說語意標籤、微標註 class、有字距的 eyebrow/kicker、
    #           position:absolute/fixed 的頁角浮層（註腳/出處/徽章）
    body_only = re.sub(r'<style\b[^>]*>.*?</style>', '', html, flags=re.S)
    body_only = re.sub(r'<!--.*?-->', '', body_only, flags=re.S)
    for mt in re.finditer(r'<([a-zA-Z][\w-]*)\b([^>]*\bstyle\s*=\s*"([^"]*)"[^>]*)>', body_only):
        tag, attrs, sval = mt.group(1).lower(), mt.group(2), mt.group(3)
        if tag in NO_TEXT_TAGS or tag in MICRO_TEXT_TAGS:
            continue
        fv = fs_vw_equiv(sval)
        if fv is None or fv >= 2.0:
            continue
        if re.search(r'position\s*:\s*(?:absolute|fixed)', sval):
            continue                                   # 頁角浮層＝刻意微標註，非觀眾主文
        if 'letter-spacing' in sval:
            continue                                   # 有字距＝eyebrow/kicker 小標，非觀眾主文
        cm = re.search(r'class\s*=\s*"([^"]*)"', attrs)
        cls = cm.group(1) if cm else ''
        if MICRO_FS_INLINE_RE.search(cls):
            continue
        peek = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', body_only[mt.end():mt.end() + 24])).strip()
        FAIL(f'[字級] 內容元素手刻 inline font-size {fv}vw（當量）< 2vw：<{tag} class="{cls}">「{peek}…」')

    # 4. emoji（規劃層以外）
    visible = re.sub(r'<aside class="plan-note">.*?</aside>', '', html, flags=re.S)
    emos = EMOJI_RE.findall(re.sub(r'<style>.*?</style>', '', visible, flags=re.S))
    if emos:
        FAIL(f'[emoji] 可見區出現 emoji：{Counter(emos)}')

    # 5. 重複 selector
    rules = parse_style_rules(style)
    dup = {s: c for s, c in Counter(sel for sel, _ in rules).items() if c > 1}
    if dup:
        WARN(f'[CSS] {len(dup)} 個 selector 重複定義（override cruft）：' +
             ', '.join(f'{s}×{c}' for s, c in list(dup.items())[:8]) +
             ('' if len(dup) <= 8 else ' …') + '（可加 --fix-css 合併）')

    # 6. plan-note
    for i, blk in enumerate(secs, 1):
        if section_kind(blk) == 'content':
            if '<aside class="plan-note">' not in blk:
                WARN(f'[規劃層] 第 {i} 頁無 plan-note')
            elif 'plan-note__source' not in blk:
                WARN(f'[規劃層] 第 {i} 頁 plan-note 缺 source')

    # 7. slide--white / inline bg
    if 'slide--white' in html:
        FAIL('[技術] 出現 slide--white class（已知 bug，請改 inline background）')
    for i, blk in enumerate(secs, 1):
        if 'style=' not in blk.split('>', 1)[0] or 'background' not in blk.split('>', 1)[0]:
            WARN(f'[技術] 第 {i} 個 section 開頭 tag 沒設 inline background')

    # 7b. logo symbol 完整性（防手抄殘缺：完整 nl-logo 應有 17 條 path）
    if 'href="#nl-logo"' in html or "href='#nl-logo'" in html:
        m_logo = re.search(r'<symbol id="nl-logo".*?</symbol>', html, re.S)
        if not m_logo:
            FAIL('[logo] 有用 <use href="#nl-logo"> 但找不到 symbol 定義（請從 template.html 整段複製）')
        else:
            n_path = m_logo.group(0).count('<path')
            if n_path < 10:
                FAIL(f'[logo] nl-logo symbol 只有 {n_path} 條 path（完整應為 17），疑似手抄殘缺')

    # 8. 對應原文逐字覆蓋（選配）
    if article and os.path.exists(article):
        srcs = re.findall(r'plan-note__source">(.*?)</div>', html, re.S)
        def clean(t):
            t = re.sub(r'<b>.*?</b>', '', t, flags=re.S)   # 去掉「📄 對應原文…」標
            t = re.sub(r'<[^>]+>', '', t)                  # 去標籤
            return re.sub(r'\s+', '', t)
        deck_text = ''.join(clean(s) for s in srcs)
        art = re.sub(r'\s+', '', re.sub(r'<[^>]+>', '', open(article, encoding='utf-8').read()))
        art = re.sub(r'^.*?\n', '', art)  # 粗略；僅比字數量級
        ratio = len(deck_text) / max(1, len(art))
        if not (0.8 <= ratio <= 1.15):
            WARN(f'[原文] 對應原文總字數 {len(deck_text)} vs 文章 {len(art)}（比 {ratio:.2f}，偏離 1.0，可能漏段/重複）')
        else:
            print(f'  · 對應原文覆蓋比 {ratio:.2f}（接近 1 = 逐字全覆蓋）')

    # ---- --fix-css ----
    if fix_css and dup:
        blocks = split_style_blocks(style)
        # 先算出每個重複 selector 合併後的宣告；只在「第一次出現的位置」輸出，其餘刪除。
        merged = OrderedDict()
        for b in blocks:
            if b[0] != 'rule':
                continue
            sel, decl = b[1], b[2]
            if sel in merged:
                merged[sel].update(decls_to_dict(decl))
            else:
                merged[sel] = decls_to_dict(decl)
        emitted = set()
        parts = []
        for b in blocks:
            if b[0] == 'at':
                parts.append(b[1] + '\n')          # @keyframes/@media… 原封不動、原位保留
                continue
            sel = b[1]
            if sel in emitted:
                continue                           # 後面的重複定義已併進第一次出現處
            emitted.add(sel)
            props = merged[sel]
            parts.append(sel + '{' + ';'.join(f'{k}:{v}' for k, v in props.items()) + '}\n')
        new_style = ''.join(parts)
        html2 = html[:style_m.start(1)] + new_style + html[style_m.end(1):]

        # 自我驗證：動畫指紋一旦改變就整個放棄，寧可不修也不弄壞動畫
        if anim_fingerprint(html2) != anim_fingerprint(html):
            FAIL('[--fix-css] 合併後動畫指紋改變（@keyframes 或 animation 數量不符），已放棄修改、原檔未動')
        else:
            bak = deck + '.bak'
            open(bak, 'w', encoding='utf-8').write(html)
            open(deck, 'w', encoding='utf-8').write(html2)
            kf = len(_KF_RE.findall(new_style))
            print(f'  ✎ --fix-css：{len(dup)} 個重複 selector 已合併（{len(style)}→{len(new_style)} 字元）；'
                  f'{kf} 個 @keyframes 原樣保留。原檔備份於 {os.path.basename(bak)}')
        print('    ⚠ 請務必逐頁截圖驗收（同 selector 合併安全，但極少數跨 selector 順序敏感情況需目視）')

    # ---- 報告 ----
    print()
    print(f'==== {os.path.basename(deck)}：{len(secs)} 頁 ====')
    for m in fails: print('  ✗ ' + m)
    for m in warns: print('  ⚠ ' + m)
    if not fails and not warns:
        print('  ✓ 全部通過')
    print(f'\n結果：{len(fails)} FAIL · {len(warns)} WARN')

    # ---- measure：用 headless Chrome 實際渲染量版面（預設開；--no-measure 關閉）----
    do_measure = '--no-measure' not in flags
    ov = measure(deck) if do_measure else 0
    sys.exit(1 if (fails or ov) else 0)


# =================================================================
# measure：用 headless Chrome 實際渲染，量「超出 slide / 超出 .slide-frame / 元素重疊 / 內文被裁切」
# （字級/重複selector等靜態檢查抓不到版面溢位，這個補上）
# 預設開啟（不加旗標即跑）；CI 無瀏覽器可加 --no-measure 關閉。
# =================================================================
def measure(deck):
    import subprocess, tempfile, json as _json, os as _os
    chrome = None
    for c in ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
              '/Applications/Chromium.app/Contents/MacOS/Chromium',
              '/usr/bin/google-chrome', '/usr/bin/chromium', '/usr/bin/chromium-browser',
              r'C:\Program Files\Google\Chrome\Application\chrome.exe',
              r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
              r'C:\Program Files\Microsoft\Edge\Application\msedge.exe',
              r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe']:
        if _os.path.exists(c): chrome = c; break
    if not chrome:
        print('  · --measure 需要 Google Chrome，找不到，略過'); return 0
    html = open(deck, encoding='utf-8').read()
    # 探針（四類，render @1600×900）：
    #   beyond  = 元素超出整張 slide 邊界（硬性，真破版）→ FAIL
    #   frame   = .slide-frame 內的內容超出安全框（更嚴）→ FAIL
    #             ＊只查 .slide-frame 的子孫；頁角 chrome／註腳／出處（.slide 直屬、刻意放框外）天生不算
    #   overlap = 頁內兩個「有底色或邊框的盒子」互相重疊（含 <span> 膠囊）→ FAIL；排除父子包含
    #   clip    = 元素自身 overflow 把內文裁掉（常為刻意，如影片框）→ WARN
    #   容差：beyond/clip 沿用原值；frame ±6px（吸收 line-box/次像素）；overlap 雙軸交集需 >4px。
    #   排除 IMG/SVG 與裝飾類（chapter 大數字、cover 滿版圖、__num）以免誤報。
    probe = r'''<script>(function(){
function tg(el){var c=(el.getAttribute&&el.getAttribute('class'))||'';return el.tagName.toLowerCase()+(c?'.'+c.split(/\s+/)[0]:'');}
var SKIP=/chapter|cover__visual|__num|probe-fb__img|rvz__cover/;
var CHROME=/brand-footer|page-label|progress|plan-note/;
function clsOf(el){return (el.getAttribute&&el.getAttribute('class'))||'';}
function inChrome(el){var n=el;while(n&&n.nodeType===1&&n!==document.body){if(CHROME.test(clsOf(n)))return true;n=n.parentElement;}return false;}
function isMedia(t){t=t.toUpperCase();return t==='IMG'||t==='SVG'||t==='PATH'||t==='POLYGON'||t==='POLYLINE'||t==='USE'||t==='G'||t==='CIRCLE'||t==='RECT'||t==='LINE'||t==='ELLIPSE'||t==='DEFS'||t==='SYMBOL';}
function hasBox(el){var cs=getComputedStyle(el);var bg=cs.backgroundColor||'';
var clear=(bg===''||bg==='transparent'||bg==='rgba(0, 0, 0, 0)'||/,\s*0\)\s*$/.test(bg));
if(!clear)return true;
var bw=Math.max(parseFloat(cs.borderTopWidth)||0,parseFloat(cs.borderRightWidth)||0,parseFloat(cs.borderBottomWidth)||0,parseFloat(cs.borderLeftWidth)||0);
return bw>0;}
function run(){var out=[];[].forEach.call(document.querySelectorAll('.slide'),function(s,i){var p=i+1;var sr=s.getBoundingClientRect();
[].forEach.call(s.querySelectorAll('*'),function(el){var t=el.tagName;if(isMedia(t))return;var nm=tg(el);if(SKIP.test(nm))return;var r=el.getBoundingClientRect();if(!r.width||!r.height)return;
if(r.right>sr.right+3||r.left<sr.left-3||r.bottom>sr.bottom+3||r.top<sr.top-3){out.push({p:p,t:nm,k:'beyond'});}
var cs=getComputedStyle(el);if(cs.overflow!=='visible'&&(el.textContent||'').trim().length>0&&(el.scrollHeight>el.clientHeight+4||el.scrollWidth>el.clientWidth+4)){out.push({p:p,t:nm,k:'clip'});}});
var frame=s.querySelector('.slide-frame');if(frame){var fr=frame.getBoundingClientRect();
[].forEach.call(frame.querySelectorAll('*'),function(el){var t=el.tagName;if(isMedia(t))return;var nm=tg(el);if(SKIP.test(nm))return;if(inChrome(el))return;var r=el.getBoundingClientRect();if(!r.width||!r.height)return;
if(r.right>fr.right+6||r.left<fr.left-6||r.bottom>fr.bottom+6||r.top<fr.top-6){out.push({p:p,t:nm,k:'frame'});}});}
var boxes=[];[].forEach.call(s.querySelectorAll('*'),function(el){var t=el.tagName;if(isMedia(t))return;var nm=tg(el);if(SKIP.test(nm))return;if(!hasBox(el))return;var r=el.getBoundingClientRect();if(r.width<=0||r.height<=0)return;boxes.push({el:el,r:r,nm:nm});});
for(var a=0;a<boxes.length;a++)for(var b=a+1;b<boxes.length;b++){var A=boxes[a],B=boxes[b];if(A.el.contains(B.el)||B.el.contains(A.el))continue;
var ox=Math.min(A.r.right,B.r.right)-Math.max(A.r.left,B.r.left);var oy=Math.min(A.r.bottom,B.r.bottom)-Math.max(A.r.top,B.r.top);
if(ox>4&&oy>4){out.push({p:p,t:A.nm+' × '+B.nm,k:'overlap'});}}});
// ── 編輯後檢查（2026-09-14）：留白比／最小字級／色塊字佔比，低於門檻列 WARN ──
var CARD_SKIP=/hero|msask|band|page-hero|__title|probe-cover|chapter/;
function txtNode(el){return [].some.call(el.childNodes,function(n){return n.nodeType===3&&n.textContent.trim().length>=2;});}
function cover(root,rect,gw,gh){var g=new Uint8Array(gw*gh);var els=[root].concat([].slice.call(root.querySelectorAll('*')));els.forEach(function(el){if(el===root&&!txtNode(el))return;if(inChrome(el)||el.closest('.plan-note'))return;var t=el.tagName.toUpperCase();var ok=txtNode(el)||t==='IMG'||t==='SVG';if(!ok)return;var cs=getComputedStyle(el);if(cs.display==='none')return;var r=el.getBoundingClientRect();if(r.width<2||r.height<2)return;
var x0=Math.max(0,Math.floor((r.left-rect.left)/rect.width*gw)),x1=Math.min(gw,Math.ceil((r.right-rect.left)/rect.width*gw)),y0=Math.max(0,Math.floor((r.top-rect.top)/rect.height*gh)),y1=Math.min(gh,Math.ceil((r.bottom-rect.top)/rect.height*gh));for(var y=y0;y<y1;y++)for(var x=x0;x<x1;x++)g[y*gw+x]=1;});var f=0;for(var i=0;i<g.length;i++)f+=g[i];return f/g.length;}
[].forEach.call(document.querySelectorAll('.slide'),function(s,i){var p=i+1;var frame=s.querySelector('.slide-frame');if(!frame)return;if(/chapter|cover|breather|thanks/.test(clsOf(s)))return;var fr=frame.getBoundingClientRect();if(fr.width<10)return;var sw=s.getBoundingClientRect().width;var u=sw/100;
var cov=cover(frame,fr,160,90);if(cov<0.45)out.push({p:p,t:'內容只覆蓋 '+Math.round(cov*100)+'%（字刪少了？考慮放大或補圖）',k:'sparse'});
var minFs=999,minTxt='';[].forEach.call(frame.querySelectorAll('*'),function(el){if(inChrome(el)||el.closest('svg')||el.closest('.plan-note')||!txtNode(el))return;var cs=getComputedStyle(el);if(cs.display==='none')return;var fs=parseFloat(cs.fontSize);if(fs<minFs){minFs=fs;minTxt=el.textContent.trim().slice(0,10);}});
if(minFs<1.25*u)out.push({p:p,t:'最小字 '+(minFs/u).toFixed(2)+'u「'+minTxt+'」',k:'small'});
[].forEach.call(frame.querySelectorAll('*'),function(el){if(inChrome(el)||el.closest('svg')||!hasBox(el))return;var nm=tg(el);if(CARD_SKIP.test(nm))return;var r=el.getBoundingClientRect();if(r.width*r.height<fr.width*fr.height*0.08)return;var f=cover(el,r,40,24);if(f<0.4)out.push({p:p,t:nm+' 只有 '+Math.round(f*100)+'% 是內容',k:'hollow'});});});
var seen={},uniq=[];out.forEach(function(o){var k=o.p+'|'+o.t+'|'+o.k;if(!seen[k]){seen[k]=1;uniq.push(o);}});
var e=document.createElement('script');e.type='application/json';e.id='__ovf';e.textContent=JSON.stringify(uniq.slice(0,200));document.body.appendChild(e);}
if(document.fonts&&document.fonts.ready){document.fonts.ready.then(run);setTimeout(run,1500);}else{run();}})();</script>'''
    tmp = deck + '.__measure.html'
    open(tmp, 'w', encoding='utf-8').write(html.replace('</body>', probe + '</body>', 1))
    try:
        dom = subprocess.run([chrome, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--force-prefers-reduced-motion',
                              '--virtual-time-budget=5000', '--window-size=1600,900', '--dump-dom',
                              'file://' + _os.path.abspath(tmp)], capture_output=True, text=True, timeout=60).stdout
    finally:
        _os.path.exists(tmp) and _os.remove(tmp)
    m = re.search(r'id="__ovf"[^>]*>(.*?)</script>', dom, re.S)
    if not m:
        print('  · measure：探針未回報（字型/載入逾時？可重試）'); return 0
    items = _json.loads(m.group(1) or '[]')
    beyond  = [o for o in items if o['k'] == 'beyond']
    overlap = [o for o in items if o['k'] == 'overlap']
    frame   = [o for o in items if o['k'] == 'frame']
    clip    = [o for o in items if o['k'] == 'clip']
    sparse  = [o for o in items if o['k'] == 'sparse']
    hollow  = [o for o in items if o['k'] == 'hollow']
    small   = [o for o in items if o['k'] == 'small']
    from collections import defaultdict as _dd
    if not (beyond or overlap or frame or clip):
        print('  · measure：✓ 無版面溢位／重疊／超框（@1600×900）')
        _edit_report(sparse, hollow, small)
        return 0
    def _grp(rows, mark, head):
        g = _dd(list)
        for o in rows: g[o['p']].append(o['t'])
        print('  ' + mark + ' ' + head)
        for p in sorted(g): print('      P' + str(p) + ': ' + '、'.join(sorted(set(g[p]))[:5]))
    if beyond:  _grp(beyond,  '✗', '[版面] ' + str(len(beyond))  + ' 處「超出 slide 邊界」（真破版，render @1600×900）：')
    if overlap: _grp(overlap, '✗', '[版面] ' + str(len(overlap)) + ' 處「頁內元素重疊」（兩個有底色/邊框的盒子相疊）：')
    if frame:   _grp(frame,   '✗', '[版面] ' + str(len(frame))   + ' 處「超出 .slide-frame 安全框」（內容溢出安全區）：')
    if clip:    _grp(clip,    '⚠', '[版面] ' + str(len(clip))    + ' 處「內文被裁切」（可能刻意、請目視）：')
    _edit_report(sparse, hollow, small)
    return len(beyond) + len(overlap) + len(frame)   # beyond/overlap/frame 算 FAIL；裁切僅 WARN


def _edit_report(sparse, hollow, small):
    """編輯後檢查（2026-09-14）：老師刪字之後版面會不會太空、字會不會太小。只列 WARN，請人眼決定要放大、換版還是補圖。"""
    if not (sparse or hollow or small):
        print('  · 編輯後檢查：✓ 沒有偏空的頁（覆蓋 ≥45%、色塊內容 ≥40%、最小字 ≥1.25u）'); return
    from collections import defaultdict as _dd
    def _g(rows, head):
        g = _dd(list)
        for o in rows: g[o['p']].append(o['t'])
        print('  ⚠ ' + head)
        for p in sorted(g): print('      P' + str(p) + ': ' + '、'.join(sorted(set(g[p]))[:4]))
    if sparse: _g(sparse, '[編輯後] ' + str(len(sparse)) + ' 頁「內容偏少」（章節／封面不算）：')
    if hollow: _g(hollow, '[編輯後] ' + str(len(hollow)) + ' 個「色塊裡字太少」（卡片變空）：')
    if small:  _g(small,  '[編輯後] ' + str(len(small))  + ' 頁「最小字 <1.25u」（標籤／註解以外要放大）：')


if __name__ == '__main__':
    main()
