# AI 請先讀這份（數感 HTML 簡報系統）

> **給人類使用者**：把這份檔案（或整個資料夾）丟給你的 AI，跟它說「照 AI-START-HERE.md 做」，它就知道怎麼做出符合規範的簡報。
> **給 AI**：這份是唯一入口。讀完這份，你就能開始動手；需要細節時，再照下面的「什麼時候讀哪一份」去查。**不要**一開始就把所有文件讀完，會浪費 context。

---

## 0. 這是什麼

一套用 **HTML 做簡報**的系統。**一個 .html 檔＝一份完整簡報**，瀏覽器打開就能投影，不需要 PowerPoint。

- 舞台鎖 16:9，任何螢幕都不裁切、不漂移
- 內建：規劃模式（講稿）、總覽模式、動畫、體檢 linter、截圖驗收
- 尺寸單位是 `--u`（＝舞台寬的 1%），**不是 vw**

---

## 1. 最短路徑（照做就對）

**先選一套 kit**——下文所有 `deck-kit_*/` 就是你選的那一套。三套的版型系統、規則、指令完全相同，只差品牌層與底板：

| kit | 什麼場合 |
|---|---|
| `deck-kit_數感實驗室` | 數感實驗室對外簡報的預設款（綠） |
| `deck-kit_NUMiNAI` | NUMiNAI 平台相關（綠松；吉祥物素材在該 kit 的 `assets/`） |
| `deck-kit_AI數感盃` | AI數感盃競賽、教師研習，以及任何想要「清爽藍白科技感」的場合（藍白＋CSS 畫的底板） |

一份 deck 只吃一套 `base.css`；三套的語意 token 同名，所以換 kit ＝換掉同層的 `base.css`（＋ logo symbol），內容不用重排。**選了 `deck-kit_AI數感盃` 要多讀它的 `README.md` 第三、四節**（底板 class `nx-steps`／`nx-dark`／`nx-bare` 與 `.nx-rule`／`.nx-num`，那套專有）。

```
1. 複製你選的 deck-kit_*/ 到工作資料夾
2. 讀 deck-kit_*/slide-system.md（必讀）＋ content-style.md（文案規範）
3. 從 decks/starter.html 複製起手；要某個版型的正典寫法就看 layouts/<name>.html
4. 新的 .html 必須跟 base.css、presenter.js 放在「同一層」；圖片放 assets/
5. 寫完跑：python3 check_deck.py <deck.html>   → 要 0 FAIL
6. 逐頁看過：./shot.sh <deck.html> 1-10 /tmp/shots  → 用讀圖能力逐張確認
```

**要重建一份別人已經在瀏覽器裡改過字的 deck，先跑 `python3 keep_edits.py 舊.html 新.html`**，不然他改的字會被蓋掉（細節見 §4b）。

**交件標準：`check_deck.py` 0 FAIL，而且你真的看過截圖。** 只跑 linter 不看圖，會漏掉「沒爆框但很醜」的頁。

---

## 2. 什麼時候讀哪一份

| 檔案 | 何時讀 | 內容 |
|---|---|---|
| `deck-kit_*/slide-system.md` | **一定要讀** | 版型系統、單位規範（第 ⓪ 節）、版面高度預算、進階技巧、防雷清單 |
| `deck-kit_*/content-style.md` | **一定要讀** | 文案規範、每頁字數、出處（cite）紀律 |
| `deck-kit_*/decks/starter.html` | 起手時 | 極簡 3 頁範本，直接複製 |
| `deck-kit_*/layouts/<name>.html` | 要用某版型時 | 一型一檔的正典寫法（cover / hero / stats / spotlight / photo-cover…） |
| `deck-kit_*/all-layouts-demo.html` | 想一次看全部版型 | 全版型各一頁的速查 demo |
| `deck-kit_*/image-sourcing.md` | 要配圖 / AI 生圖時 | 圖片來源、版權、生圖 prompt 規則、方圖裁切怎麼救 |
| `deck-kit_*/svg-patterns.md` | 要畫結構圖時 | 流程、對照、折線圖…可直接複製的 SVG 配方 |
| `deck-kit_*/template-spec.md` | 要新增版型時 | 版型規格與陷阱 |
| `deck-kit_*/README.md` | 用 `deck-kit_AI數感盃` 時要讀 | 該套的色票、底板 class、`.nx-*` 工具 class（另兩套不必讀） |
| `deck-kit_*/README_編輯與儲存.md` | **交件時附給簡報的主人** | 簡報主人怎麼自己改字、儲存、備份；改字後自動重排；舊分頁存檔保護 |
| `deck-kit_*/CHANGELOG.md` | 想知道最近改了什麼 | 版本紀錄 |
| `design-docs/` | **通常不用讀** | 設計決策史 |

---

## 3. 硬規則（違反就是 FAIL，不要例外）

1. **尺寸一律 `calc(N*var(--u))`，禁用 `vw`。** `--u` ＝舞台寬 1%；16:9 下 1u ＝ 1vw，但 vw 會隨螢幕漂移。
2. **給觀眾讀的內容字 ≥ `calc(2*var(--u))`。** 只有頁碼、出處、微標註可以更小。
3. **每頁內容包進 `<div class="slide-frame">`**（封面、章節隔頁、滿版圖、收尾頁例外）。
4. **`page-label__num` ＝該頁在整份 deck 的實際位置**（沒有頁碼的滿版頁也佔一個號碼）。搬動任何一頁都要全部重編。
5. **每個內容頁都要有 `<aside class="plan-note">`**，裡面放該頁的逐字講稿（`plan-note__source`）＋設計說明（`plan-note__meta`）。這就是簡報者上台念的稿。
6. **可見區不准出現 emoji**（規劃層裡可以）。要圖示用 inline SVG。**注意 `✓ ✔ ✗ ✕ ★ ✦` 會被判定成 emoji 而 FAIL**；實測安全的符號只有 `× → ↓ ▼ ▶ ●`，打勾一定要用 inline SVG。
7. **每個 `<section class="slide">` 的開頭 tag 要有 inline `background`。** 不要用 `slide--white`（已知 bug）。
8. **logo 用 `<use href="#nl-logo">`**，symbol 整段從 `logo-symbol.html` 複製（完整是 17 條 path，手抄殘缺會被 linter 抓）。
9. **cite 只列頁面上真的看得到的數據來源。** 刪掉資料就要同步刪出處。
10. **每頁可見中文字 ≤ 80（硬上限 140）。** 投影片只放「標籤＋一句話」，說明交給圖片和講者，完整的話寫進 `plan-note`。詳見 `deck-kit_*/content-style.md` §八。
11. **動畫要節制：每頁 1–2 組，全場平均不超過 2 組／頁**（見下方 §4）。做完要先按 `M` 關掉動畫確認「不播也看得懂」，再打開確認有掛上。
    - 一頁掛到五、六個進場動畫就會變吵。**只給最該被看見的那一兩個東西**：主標一個、資料型動畫（長條長出來、線畫出來）算內容不算裝飾，可以留。
    - **`anim-stagger` 最吵**（一次帶動整組子元素），除非那一組本身就是重點，否則不要用。
    - **要「一個一個出現」，優先做成互動（點擊），不要做成計時**。計時的問題是講者控制不了節奏，而且觀眾還沒想完答案就跑出來了。做法見 `slide-system.md` §四 Pattern 10。

---

## 4. 動畫：加 class 就好，不要自己寫 keyframes

| class | 效果 |
|---|---|
| `anim-bar` | 長條從左長出來（scaleX） |
| `anim-bar-w` | 長條長出來（width 版）——**條裡面有文字時用這個**，字不會被壓扁 |
| `anim-up` | 淡入＋往上浮（最泛用） |
| `anim-fade` | 單純淡入 |
| `anim-pop` | 彈出放大（圓點、徽章） |
| `anim-drop` | 從上落下（年份卡、大數字） |
| `anim-slam` | 放大砸下（揭曉、結果） |
| `anim-left` / `anim-right` | 左右滑入（兩欄對比） |
| `anim-stamp` | 蓋章（帶旋轉的彈跳） |
| `anim-draw` | SVG 線條畫出來，需 `style="--anim-draw-len:560"`（≈路徑長度） |
| `anim-stagger` | **加在容器上**，子項自動依序浮上來（最多 8 個） |
| `anim-bar-v` | 直條從底線長上去（scaleY；SVG rect 直條圖用） |
| `anim-rows` | 表格逐列浮上 |
| `data-anim="in-y"` | 沿自己的 y 軸滑入（箭頭往內指用） |
| `data-anim="draw-rev"` | SVG 線條從尾端往回畫 |

- 微調：`style="--anim-delay:.4s"`（延遲）、`style="--anim-dur:.8s"`（時長）
- 動畫只在 `.slide.active`（目前這頁）觸發，翻回來會重播
- **翻牌頁**：包在 `.rvz` 裡的元素會自動變成「翻開（`.is-open`）才播」，不用換 class
- 使用者按 **M** 可以一鍵關掉全部動畫；系統開了「減少動態效果」時預設關閉
- **不要用 `id` 綁動畫**（總覽模式會複製節點，id 會重複）
- **沒手動掛 anim-* 的頁，`presenter.js` 會自動配**（見 §4b）：標題、軸線、標籤、有框方塊、頁尾不動，只動長條、折線、圓點、圓餅塊、表格逐列、KPI 數字、卡片依序、帶子最後。手動掛的 anim-* 優先，`<section data-anim="none">` 整頁關。

---

## 4b. 編輯、重排、揭曉（2026-09-14 起 kit 內建；做 deck 只要照三條規則標）

簡報的主人會在瀏覽器裡按 `E` 直接改字、按「儲存」寫回同一個檔（`serve.py`＋雙擊 `開啟簡報.command`）；`presenter.js` 會在改字後**自動重排**（清空的方塊收起、色塊跟著縮、卡片重新分欄、空位給圖表；字變少時把剩下的放大「補回」）並**自動配進場動畫**（骨架不動、論點動；每頁最多按一下揭曉）。做 deck 時只需要：

1. **圖表照慣例畫，動畫才認得**：長條圖的 `<rect>` 同一條基準線（直條）或同一左緣（橫條）；折線／連線用有 `stroke`、沒有 `fill` 的 `<path>`／`<polyline>`；圓點用 `<circle>`；填色形狀（圓餅塊）用有 `fill` 的 `<path>`。座標軸用 `<line>`、標籤用 `<text>`，它們會當骨架不動。
2. **講述有先後的頁標順序**：圖上看不出先後的（例如「先我們在哪、再往哪長」），在元素或 `<g>` 上寫 `data-seq="1,2,3…"`，同一步一起出、每步隔 0.38 秒；沒標的當底圖先出。
3. **有「現況 → 轉折」的頁標揭曉，會被刪字的區塊標補回**：進頁只看骨架＋現況、按一下才出論點的元素加 `data-reveal`（每頁最多一次，通常是圖表後半段、結論卡、小結帶；帶子會等其他動畫跑完最後出）；會被刪字的主文字區（卡片、欄位、文字欄）加 `data-grow`，kit 版型已為它們定義放大階段（`template-spec.md` §九）。

另外三件事：

- **`<head>` 寫 `<meta name="deck-build" content="YYYYMMDD-HHMMSS">`**（每次重建換值）。`serve.py` 靠它擋掉舊分頁的儲存（回 409、提示重新整理），不然舊分頁一存就把新版面蓋回去。
- **重建前必跑 `python3 keep_edits.py 舊.html 新.html`**，把 `<script id="deck-edits">` 裡的修改搬到新檔。修改是用「頁:第 N 個有字的元素」定位的，所以重排版時不要增減或調換該頁帶字的元素（只改 CSS、只加沒有字的包裝層才安全）；某頁結構重做就清掉該頁舊修改並把 `rev` 加一。
- **全幅圖要鋪進上下留白**：滿版 `<img>`（`position:absolute;inset:0;object-fit:cover`）加 `data-bleed="50 50"`（＝object-position 百分比），螢幕不是 16:9 時留白帶會是圖的延伸，頁碼那一帶也在圖上；沒加的頁只補該頁底色。

QA 除了 0 FAIL，還要看 `check_deck.py --measure` 的「編輯後檢查」三個 WARN（內容偏少／色塊字太少／最小字）；交件時把 `README_編輯與儲存.md`、`開啟簡報.command`、`serve.py`、`keep_edits.py` 跟 deck 放同一層。

---

## 5. 驗收指令

```bash
# 體檢（預設會開 Chrome 實際量版面：溢位／重疊／超框）
python3 check_deck.py <deck.html>

# 沒有瀏覽器的環境
python3 check_deck.py <deck.html> --no-measure

# 逐頁截圖（第 6 到 12 頁），再用讀圖能力逐張看過
./shot.sh <deck.html> 6-12 /tmp/shots
```

`check_deck.py` 會檢查：頁碼＝位置、圖檔存在、字級 ≥2u、可見區無 emoji、CSS 重複定義、每頁有 plan-note、inline background、logo 完整性，以及實際渲染的版面溢位／頁內重疊。**退出碼 0 ＝全過。**

**linter 抓不到、一定要自己量的兩件事**：

```bash
# 每頁可見中文字（不含 plan-note）——目標 ≤80、硬上限 140
python3 - <<'EOF'
import re, statistics as st
s=open('<deck.html>',encoding='utf8').read()
secs=re.split(r'(?=<section class="slide)',s)[1:]
n=[len(re.findall(r'[一-鿿]', re.sub(r'<[^>]+>',' ', x.split('<aside')[0]))) for x in secs]
print('平均%.0f 中位數%.0f 最大%d｜超過120字的頁：%d/%d'%(st.mean(n),st.median(n),max(n),sum(1 for v in n if v>120),len(n)))
for i,v in sorted(enumerate(n,1),key=lambda x:-x[1])[:8]: print(f'  P{i}: {v}字')
EOF

# 動畫用量——0 就是沒做
grep -o 'anim-[a-z]*' <deck.html> | sort | uniq -c | sort -rn
```

**動畫的驗收陷阱**：`shot.sh` 截的是靜態畫面，動畫可能還沒播完就被截到，看起來像破版。QA 要跑兩次——先確認「不播動畫時版面也是完整的」，再確認動畫真的掛上了。**不可以做出「非得等動畫跑完才看得懂」的簡報。**

> ⚠️ **關動畫不能靠在 `<html>` 加 `no-motion` class**——`presenter.js` 開場會依 `localStorage` 把它覆寫掉，你以為關了其實沒關，驗出來的 0 FAIL 是假的。正確做法是**注入 CSS**：
>
> ```python
> s = open(deck, encoding='utf8').read().replace(
>     '</head>',
>     '<style>*,*::before,*::after{animation:none!important;transition:none!important;}</style>\n</head>')
> open('_nomotion.html','w',encoding='utf8').write(s)   # 對這個檔跑 check_deck 與 shot.sh
> ```
>
> 手動操作時按 `M` 是有效的（那會同時寫 localStorage）；只有「程式化注入 class」這條路不通。

**確認動畫真的掛上了**（不要只看 grep 到幾個 class，要看瀏覽器認不認）：headless 跑 `document.getAnimations()`，逐頁確認 `.slide.active` 底下有動畫實體。

**判讀提醒**：`[版面] 頁內元素重疊` 有兩種常見誤判——翻牌頁的遮罩（`.rvz__cover` 本來就該蓋住答案）、以及兩個盒子邊緣剛好相碰。看到要先截圖確認，不要盲目改版面。

---

## 6. 六個最容易踩的坑（詳細版在 slide-system.md）

1. **版面高度預算**：舞台高 56.25u −上下安全邊 12u ＝ `.slide-frame` 可用 **44.25u**；再扣 page-hero（約 8.2u）與 cite（約 2.4u／行），主內容區只剩 **約 33.5u**。**排版前先加總，不要排完才發現爆框。**
2. **grid 欄裡的圖片不要用 `height:100%`**：row 是 `auto` 時解析不到確定值，`<img>` 會用內在比例把整頁撐爆（方圖最慘）。要給確定高度 `height:calc(28*var(--u))` ＋ `object-fit:cover`。
3. **滿版圖轉場頁遇到淺色照片，要自訂 scrim**：預設漸層在 30% 高度只剩 0.42 不透明度，白字會糊掉。該頁 inline 覆寫一組更厚的漸層，不要去改共用規則。
4. **AI 生圖是方形（1024×1024）**，放進橫長框置中裁切會切掉人的腳。用 `object-position:center 65%~72%` 往下挪。生圖 prompt 一律加「不要出現任何文字、字母、數字」（中文會變亂碼）。
5. **搬動頁序**：切 section 要用 `re.split(r'(?=<section class="slide)', html)`——檔案裡會出現 `</section><section` 直接相接，用「換行＋縮排」切會把兩頁黏成一頁。切完先斷言頁數，搬完要逐頁依位置重編頁碼（**不能全域搜尋取代，會改到內文數字**）。
6. **出處要跟頁面上的數據一致**，而且並列比較的數字要對齊口徑（性別／年齡帶／時點／分母定義），不然會被台下當場抓包。

---

## 7. 起手 prompt（人類可以直接複製給 AI）

把 `deck-kit_*` 換成你選的那一套（`deck-kit_數感實驗室`／`deck-kit_NUMiNAI`／`deck-kit_AI數感盃`）；選 AI數感盃 就再加一句「並讀 README.md 第三、四節，封面／章節頁加 nx-steps、深底頁加 nx-dark」。

```
請讀 deck-kit_*/slide-system.md 和 content-style.md，
依照裡面的版型系統和文案規範，幫我把以下內容做成 HTML 簡報：

【內容】（貼上你的文章／大綱／講稿）
【場合與時間】例如：教師研習 60 分鐘（演講約 2 分鐘／頁）
【要求】
- 從 decks/starter.html 起手；要某版型的正典寫法看 layouts/<name>.html
- 產出的 .html 放在跟 base.css、presenter.js 同一層
- 尺寸一律 calc(N*var(--u))，禁用 vw；內容字 ≥ calc(2*var(--u))
- 每頁內容包進 <div class="slide-frame">
- 每頁 <aside class="plan-note"> 放該頁的逐字講稿
- 需要動畫時用 anim-* class，不要自己寫 keyframes
- 做完跑 check_deck.py 給我 0 FAIL 的版本，並逐頁截圖確認
```

---

## 8. 簡報操作（給上台的人）

| 按鍵 | 功能 |
|---|---|
| `←` `→` `空白` | 翻頁（也可以點畫面左 1/3 ／右 2/3、觸控左右滑） |
| `P` | 規劃模式：投影片下方展開該頁的逐字講稿 |
| `O` | 總覽模式：所有頁縮圖，點哪頁跳哪頁 |
| `g` | 顯示內容安全框（驗收用） |
| `M` | 開／關所有動畫（設定會記住） |
| `E` | 編輯模式：文字點一下就改，SVG 字跳小輸入框；工具列「儲存」寫回同一個檔（要用 `開啟簡報.command` 開） |
| `→`（頁碼旁有黃點時） | 先揭曉這頁的論點，再按才翻頁；`←` 一律回上一頁 |

列印或輸出 PDF 時，規劃層自動隱藏、動畫不執行（直接是最終狀態），講義不會缺東西。

---

## 9. 絕對不要做的事

- ❌ 不要改 `base.css` 的共用規則來解決單頁問題——單頁問題用該頁 inline 覆寫
- ❌ 不要用 `vw`、不要用 `id` 綁動畫、不要在可見區放 emoji
- ❌ 不要把 .html 跟 `base.css`／`presenter.js` 放在不同層
- ❌ 不要只跑 linter 就交件——一定要看截圖
- ⚠ `check_deck.py --fix-css` 會合併重複 selector。它已經改成保留 `@keyframes`／`@media` 並在改壞時自動放棄，但**沒事不要跑**；那行「可加 --fix-css 合併」的提示可以無視。
