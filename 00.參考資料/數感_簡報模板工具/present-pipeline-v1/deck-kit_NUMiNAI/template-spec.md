# template-spec — 版型規格與紀律（AI／人共用）

> 搭配 `slide-system.md`（各版型「怎麼運作」）使用。本檔講「**何時用哪型、正典數值、不可漂移的紀律**」。
> 目的：讓「照規範做」的人也不會在顏色、間距、字級、logo 上飄掉。
> 單位一律 `calc(N*var(--u))`（見 slide-system.md ⓪）。

---

## 一、先選標準版型，不夠才擴充

做一頁前，先從下表挑最接近的標準版型。**能用標準型就別自寫**；真要自寫，照第六節「擴充守則」。

| 版型 class | 用途（何時用） | 欄數 | 關鍵正典值 |
|---|---|---|---|
| `probe-cover` | 封面 | — | 上圖下文；標題 `--fs-cover-title`；底色延伸補白 |
| `probe-photo` | 滿版圖封面／主視覺（圖即內容） | — | 滿版圖 `cover`/`center`＋內建可調深色漸層遮罩＋標題安全區；底色延伸補深；**section 勿加 `position:relative`（白屏陷阱）** |
| `probe-chapter` | 章節隔頁 | — | 左綠 38%＋右米白；背景數字 `--fs-chapter-num` |
| `probe-hero` | 單句核心命題／價值主張 | — | 一句大字＋中段視覺＋說明；金句用 `.hi`（全篇 ≤3） |
| `probe-grid` | 多欄純文字卡（定位／比較／要點） | 2–4 | 卡 `border-top:3px` 綠；subgrid 對齊；標題 `--fs-card-title` |
| `probe-cards` | 圖文卡（物件／案例／人物＋說明） | 2–4 | 米白卡 `border-top:4px`＋`--radius-md`＋`--shadow-card`；圖 `object-fit:contain` |
| `probe-spotlight` | 單一主角深入（一個東西講透） | — | 左主圖大＋右 `.spec`＋下三縮圖 |
| `probe-rows` | 左項目→右對應（問題→對策、線索→揭曉、條件→結果） | — | 列米白＋`border-left:3px` 綠；tag 綠底白字 |
| `probe-split` | 左文右圖（可左右互換） | — | grid 子項 `min-height:0`；圖框防 letterbox |
| `probe-kpi` | 橫條式大數字 | — | 數字 `calc(5*var(--u))` 綠；baseline 對齊 |
| `probe-stats` | 深綠呼吸頁・大數字 | — | 底 `--green-dark`；數字 `--fs-kpi` 螢光黃；chrome 反白 |
| `probe-breather` | 深綠呼吸頁・一句話 | — | 一句大字；不塞資訊 |
| `probe-flow-page` | 三節點橫排流程（A→B→C／**循環**） | 3 | SVG＋marker 弧線箭頭；caption 對 01/02/03 |
| `probe-steps` | 線性多步流程（A→B→C→…） | 3–5 | flex 橫排自動分配；節點卡＋→箭頭；STEP 序號 |
| `probe-video` | 影片頁（可點海報→開新分頁播放） | — | YouTube 海報縮圖＋置中「▶ 點擊播放」＋「在 YouTube 開啟」連結；16:9；**離線/`file://` 用海報式、勿用 iframe** |
| `probe-thanks` | 收尾／CTA | — | 置中大字＋一句＋logo |

> 表內每型的完整骨架與關鍵 CSS 見 `slide-system.md` 第三節。

## 二、內容 → 版型 對應指引

| 你的內容長這樣 | 用 |
|---|---|
| 一個核心提問／主張，要它有份量 | `probe-hero`（或 `probe-grid` 標題＋內文） |
| 「考慮過 A、B、C，淘汰理由各是…」 | `probe-rows`（左方案／右淘汰理由）或 `probe-grid` |
| 一條敘事線／流程的幾個階段（**線性** 3–5 步） | `probe-steps`（首選，自動分配 3–5 節點）；**循環**流程用 `probe-flow-page`（≤3）；步驟太多放不下退 `probe-grid` |
| N 個並列項目，各有「好／代價」「優點／說明」 | `probe-grid`（純文字）或 `probe-cards`（有圖） |
| 「線索→揭曉」「問題→現況」「動作→產出」 | `probe-rows` |
| 一個成品／物件要展示＋說明 | `probe-spotlight` 或 `probe-split` |
| 純數據規模 | `probe-kpi` / `probe-stats` |
| 節奏轉換、喘口氣 | `probe-breather` |
| 滿版照片當封面／主視覺，標題壓在圖上 | `probe-photo`（內建深色遮罩確保白字可讀） |
| 要播一段影片（YouTube） | `probe-video`（海報式：可點開新分頁；離線安全、免 iframe） |

> 多數內容頁是 `probe-grid` / `probe-cards` / `probe-rows` 三選一。先想「這是並列、還是對應、還是單一主角」。

## 三、字級紀律

- **觀眾要讀的句子一律 ≥ `calc(2*var(--u))`**（主標／副標／卡片標題與承載內容的標籤／清單項／說明句／計算式）。放不下就砍字，不縮字。
- 可低於 2 的**只有微標註**：頁碼、出處 cite、規劃層、封面日期、eyebrow（如 CHAPTER／L7 特別活動）、STEP 序號、直式進位數字。
- 承載內容的「類別標籤」（方法名、對比端點）＝內容字，要 ≥2vw／900，不可用 0.9vw 綠微標。
- `check_deck.py` 只對內建 `CONTENT_FS_CLASSES` 自動擋；**自訂 class 不在清單，<2vw 只會 WARN 不會 FAIL**——所以自寫版型時要自律，別把主文做小。

## 四、顏色紀律

**品牌色就這些，不要自己加色：**

| token | 值 | 用途 |
|---|---|---|
| `--green-primary` | `#379C39` | 標題線、強調框線、tag、icon |
| `--green-dark` | `#004B24` | 深綠呼吸頁底、重點深字 |
| `--paper-warm` | `#FEF4E8` | 卡片底、封面/收尾底 |
| `--ink` | `#0A0A0A` | 正文 |
| `--mid-gray` / `--label-gray` | `#686968` / `#757070` | 副說明、頁碼、次要（de-emphasize） |
| `--hi-yellow` | `#E8FF3A` | 螢光黃強調，**全篇 ≤3 處**，只標最該記的詞 |
| `--alert` / `--alert-soft` | `#BE2026` / `#FBEAE9` | **語意色：負面／避開／警示／危險**，少量用 |

**四種語意分清楚，不要混用：**
- **正面／著重 → 綠**（`--green-primary`）
- **負面／避開／警示 → 紅**（`--alert`）：框線、圓點、`×`、標籤等**少量**用，不做大面積填色；`--alert-soft` 給淡底／淡框。
- **強調（最該記的一個詞）→ 螢光黃**（`--hi-yellow`），全篇 ≤3 處。
- **次要／不重要 → 灰**（`--mid-gray`）。

> ⚠️ 別把「避開（紅）」做成「灰」——灰是「不重要」，紅是「要被看見的負面」，語意不同。
> 紅是語意訊號不是裝飾：整頁太多紅點就失去意義，克制使用。

### 落地對照（警示怎麼做，base.css 已備 `.alert` 修飾類，不要自己重發明）

掛 `.alert` 在標準版型上即變紅語意——不另立紅版型：

```html
<!-- 禁止／警示卡：紅上緣線＋紅 label，內文可加紅 × 標記 -->
<div class="probe-grid__card alert">
  <div class="probe-grid__label">禁止</div>
  <div class="probe-grid__title"><span class="alert-mark">×</span> 不能讓小孩單獨操作教具</div>
  <div class="probe-grid__body">全程有人在旁。</div>
</div>

<!-- 警示列：紅左線＋淡紅底（--alert-soft）＋紅 tag -->
<div class="probe-rows__row alert">
  <span class="probe-rows__tag">緊急</span>
  <span class="probe-rows__item">小孩走失</span><span class="probe-rows__arrow">→</span>
  <span class="probe-rows__to">安撫穩場 → 通報總負責人與服務台 → 廣播協尋</span>
</div>

<!-- 待填佔位（express／培訓常見：保留假設值、不編造）-->
報到時間 <span class="tbd">待填</span>
```

- 標記字元安全範圍：`×`(U+00D7)、`●`、`！` 等非 emoji 區字元可放可見區當警示符；`⛔`🚫 等 emoji 只能放 `plan-note`（可見區會被 check_deck 擋）。
- 克制：`.alert` 卡／列**少量**用；rows 連續多條淡紅底沒問題（`--alert-soft`），但別整頁實心紅。

## 五、間距・邊框・圓角 正典值（擴充時照抄）

| 用途 | 值 |
|---|---|
| 標題綠線 | `border-top:3px solid var(--green-primary)` ＋ `padding-top:calc(1.5*var(--u))` |
| 卡片上緣強調線 | `border-top:4px solid var(--green-primary)`（圖文卡）／`3px`（純文字卡） |
| 列／小卡左線 | `border-left:3px solid var(--green-primary)` |
| 卡片圓角 | `var(--radius-md)`（`1.2*u`）；小元件 `var(--radius-sm)`（`0.4*u`） |
| 卡片陰影 | `var(--shadow-card)` |
| 欄間距 | `var(--gap-lg)`（`3*u`）；欄內 `var(--gap-sm/md)` |
| 內容安全框 | 包進 `.slide-frame`（封面/章節/呼吸頁/收尾例外） |

> 自寫版型時，邊框寬、圓角、間距**一律取上表既有值**，不要憑感覺給新數字——這是「細節漂移」的主因。

## 六、新增版型流程（以後要加版型，照這條走）

版型的單一真相＝`layouts/<name>.html`（一型一檔）。新增一個版型＝新增一個 layout 檔並登錄，**不改既有版型、不改引擎**。步驟：

1. **先確認標準版型真的裝不下**（多數情況裝得下；先翻 §一/§二）。真的缺，才自寫。
2. **建 `layouts/<name>.html`**：複製一個最接近的現有 layout 當骨架，連 `../base.css`、用 logo-symbol（見 `logo-symbol.html`）、一個正典 section、`page-label__num` 設 `01`、結尾接 `../presenter.js`、`../slide-audit.js`。
3. **遵守版型紀律**：
   - class 命名 `probe-<name>__<part>`。
   - 字級用語意 token（`--fs-hero/-card-title/-body/-small/-label`）；**承載「觀眾要讀的內容」的字一律 ≥ `calc(2*var(--u))`——別套展示用的小字（如把主項做成 1.5u）**。間距/邊框/圓角取 §五正典值。
   - 顏色只用 §四 token。
   - **底色延伸**：非白底頁要在 base.css 補 `body:has(.deck .slide.active.<你的頁class>)`，或重用既有 `probe-*` 類名直接吃現成規則。
4. **登錄進目錄**：在 §一版型表加一列、§二「內容→版型」加對應指引——讓人/AI 知道何時用它。
5. **重建組裝 deck**：`python build_layouts.py`（把新版型納入 `all-layouts-demo.html`）。
6. **QA**：`check_deck.py --measure` 對該 layout 檔與 all-layouts-demo 都 0 FAIL／0 溢位，再人眼開檔確認。

> 這條流程＝「版型的可維護擴充點」。對應 frame 範本表的「複製這格」：版型也是複製一檔、登錄、重建，不動既有。

## 七、防呆對照（check_deck 會擋的）

- 頁碼 `page-label__num` ≠ section 順位 → FAIL
- 內建內容類 class <2vw → FAIL（自訂 class 只 WARN，靠本檔第三節自律）
- 可見區 emoji → FAIL
- `slide--white` class → FAIL
- 缺圖檔 → FAIL
- **logo symbol 不完整**（手抄殘缺）→ FAIL（見 `check_deck.py` 第 7b 檢查）

## 八、版型陷阱（check_deck 不一定擋，靠自律）

- **`<section>`（即 `.slide`）勿加 `position:relative`**：`.slide` 靠 base.css 的 `position:absolute;inset:0` 撐滿舞台；改成 `relative` 會讓它塌掉、整頁變白屏。`probe-photo` 的滿版圖、`probe-thanks` 的置中 logo 等需要絕對定位的子元素，直接用 `position:absolute` 即可——它們以撐滿的 `.slide` 為定位基準，不必、也不可在 section 上補 `relative`。
- **離線／本機（`file://`）播影片一律用 `probe-video` 海報式，勿用 `<iframe>`**：`file://` 開 YouTube iframe 會 `Error 153`／空白。海報式＝可點的 `<a target="_blank">` 包 `img.youtube.com/vi/<ID>/maxresdefault.jpg`＋置中「▶ 點擊播放」（`▶`＝U+25B6 非 emoji）＋「在 YouTube 開啟」連結，點了開新分頁播放，離線投影也安全。
- **grid 欄裡的圖片容器勿用 `height:100%`**：grid row 高度是 `auto` 時，`height:100%` 解析不到確定值，`<img>` 會退回用「圖片內在比例」撐開——1024×1024 方圖放進 42u 寬的欄就撐出 42u 高，整頁往下爆出安全框（每個元素單看都正常，最難抓）。圖框一律給**確定高度**、圖片填滿：

  ```css
  .xxx__img{ height:calc(28*var(--u)); min-height:0; overflow:hidden; }
  .xxx__img img{ width:100%; height:100%; object-fit:cover; display:block; }
  ```

  高度值從 `slide-system.md` §二「版面高度預算」推回來（主內容區約 33.5u），別憑感覺給。完整說明見 `slide-system.md` §四 Pattern 5。
- **全幅圖要鋪進上下留白**：滿版 `<img>`（`position:absolute;inset:0;object-fit:cover`）加 `data-bleed="50 50"`（兩個百分比＝`object-position`，要跟 CSS 寫的一樣）。presenter 換頁時會把同一張圖用同樣縮放鋪在 body 上，螢幕是 16:10 或更方時，上下的留白就是圖的延伸，頁碼所在的那一帶也在圖上；沒有這個屬性的頁面只補該頁底色。生圖時要求場景（地面／天空）鋪到畫面最底和最頂，不要在邊緣露出底色，延伸出去才不會斷。
- **滿版圖轉場頁遇淺色照片要自訂 scrim**：`.probe-fb__scrim` 預設漸層在 30% 高度只剩 `0.42` 不透明度，壓不住淺色底圖，白色小標會讀不到。該頁 inline 覆寫一組更厚的漸層即可（見 `slide-system.md` §四 Pattern 6），不要去改共用規則；更好的解法是生圖時就要求下三分之一留深色（`image-sourcing.md` §九）。
- **內容垂直置中**：內容頁主內容容器用 `flex:1;min-height:0` 撐滿安全框、再加 `justify-content`／`align-content:safe center`——內容少時置中填滿、內容多時 `safe` 自動退回頂端對齊不裁切（`grid/cards/kpi/rows/split/stats/steps/flow` 皆已內建）。

## 九、補回階段（編輯後：字刪少／卡片變少時，把剩下的放大）

老師在瀏覽器編輯模式（按 E）刪字之後，`presenter.js` 的 `reflow()` 只做「收」：清空的方塊收起、整塊空掉的容器收起、卡片列重新分欄。
「補回」是另一半——把剩下的內容放大填滿，由 **版型 CSS** 依兩個工具標記的屬性定義階段（`base.css` 檔尾 `/* ── 2026-09-14 補回階段` 那一段）。

### 三個屬性

| 屬性 | 誰寫的 | 意思 |
|---|---|---|
| `data-grow` | **layout 手動標**（`layouts/<name>.html` 裡） | 「會被刪字的主文字區」：卡片、欄位、文字欄、步驟說明、對照列。工具只量這些元素。標題（`.probe-*__title`／`__hero`）、eyebrow、頁尾**不掛** |
| `data-tier="s\|m\|l"` | presenter 自動標在每個 `[data-grow]` 上 | 該區可見字數 ≤45＝`s`、≤100＝`m`、更多＝`l`；每次改字重算；存檔時拿掉 |
| `data-n="N"` | presenter 自動標在每個 grid／flex 容器（原本 ≥2 子項） | 目前可見子項數；被清掉的子項仍在 DOM（`.is-cleared`），所以 CSS 用 `:has(> :nth-child(k))` 能分辨「原本幾張」 |

### 放大原則（寫階段時照這些）

- 尺寸一律 `calc(N*var(--u))`；**只比正典大、不超過該頁標題字級**；`s` 級約 1.3–1.5×、`m` 級約 1.15×；行距、內距、gap 一起調。
- **標題類跟整列走、內文類各自走**：同一列的卡片標題／名稱／大數字標籤只有在「每張都 ≤m」時放到 m、「每張都 s」時放到 s（清空的卡片字數 0＝s，不會擋）；內文／spec／說明則看自己那張。這樣同列標題永遠一樣大，被刪過的那張內文還是會補回。
- **清單型**（rows／kpi／flow captions）整列一起走，而且可見列 ≤4 才放大，列多時不擠。
- **卡片少**：用 `data-n` 分階段——4→3、3→2、→1；「原本幾張」靠 `:has(> :nth-child(k))`。→1 時變單張大卡置中（grid 64u、cards 60u、steps 56u）。
- 兩種補回同時發生（卡片少＋字少）取較大：字級寫成 `font-size:max(正典, var(--rb-t-*,0px), var(--rb-n-*,0px))`，tier 階段在 data-grow 元素／容器上設 `--rb-t-*`，n 階段在容器上設 `--rb-n-*`。
- 只有單一文字區的版型（hero、spotlight、split、flow）直接寫字級，不用變數。
- 沒掛 `data-grow`、沒被刪過的頁**完全不受影響**（n 階段只在可見數 < DOM 子項數時觸發）。
- ⚠ demo 裡的示範文字很短，所以 `all-layouts-demo.html` 一載入就會看到 s／m 階段（字比 layout 正典略大），不是 bug。
- ⚠ 若 deck 自己把某版型的正典字級改大，補回階段值要跟著抬，否則階段值可能比 deck 的還小。

### 各版型的階段（一行一版型；數字＝×u）

| 版型 | `data-grow` 掛在 | 字少（tier m → s） | 卡片少（`data-n`） |
|---|---|---|---|
| `probe-grid` | `.probe-grid__card` | 標題 2.4→2.6（整列）；內文 1.35→1.8（各自） | 4→3：標題 2.4／內文 1.35／欄距 4；3→2：2.8／1.8／5；→1：3.0／2.2、單卡 64u 置中 |
| `probe-cards` | `.probe-cards__info` | 名稱 2.4→2.6、標籤 1.3→1.45（整列）；spec 1.35→1.6（各自） | 4→3：2.4／1.3／1.3；3→2：2.6／1.45／1.5、gap 4；→1：2.9／1.6／1.7、單卡 60u 置中（2 張是正典，不算變少） |
| `probe-spotlight` | `.probe-spotlight__side` | 名稱 2.4→2.7、標籤 1.45→1.6、spec 1.35→1.6 | —（單一主角） |
| `probe-rows` | `.probe-rows__row` | 整列：項目 1.7→1.9、對應 1.35→1.5（可見 ≤4 列才放） | 4→3：1.7／1.35；3→2：2.0／1.6、tag 1.15；→1：2.4／1.9、tag 1.3；一列左或右清空，箭頭一起收 |
| `probe-split` | `.probe-split__body` | 段落 1.8→2.4、清單 1.35→1.7；s 時圖欄改 `1fr 1.3fr` | 文字欄整個清空 → 只剩圖（gap 0） |
| `probe-kpi` | `.probe-kpi__text` | 整列：說明 1.8→2.1（可見 ≤4 條才放） | 4→3：數字 5.6／說明 1.75；3→2：6.5／2.0；→1：8／2.4 |
| `probe-stats` | `.probe-stats__item` | 標籤 2.4→2.6（整列）；說明 1.35→1.6（各自） | 4→3：數字 8.5；3→2：9.5、標籤 2.6、說明 1.5；→1：11／3.0／1.8 |
| `probe-steps` | `.probe-steps__node` | 標題 2.4→2.6（整列）；說明 1.35→1.6（各自） | 剩 3（原 ≥4）：2.5／1.4；剩 2：2.8／1.7、箭頭 3；剩 1：3.0／2.0、單卡 56u；清空節點旁的箭頭一起收（兩個可見節點間永遠一支） |
| `probe-flow-page` | `.probe-flow__caption` | 整列：標題 1.35→1.5、說明 1.15→1.25 | —（三個節點固定在 SVG 圖上） |
| `probe-hero` | `.probe-hero__desc` | 2.1→2.5、寬 80%→85% | — |
| cover／chapter／breather／photo-cover／video-poster／thanks | 不掛 | — | —（純圖／章節／一句話頁） |

### 新增版型時，階段要一起寫（接在 §六 的步驟後面）

1. 在 `layouts/<name>.html` 的主文字區掛 `data-grow`（只加屬性，不改文字、不改結構）。
2. 在 `base.css` 補回段落加一節 `/* ▸ <name> */`，照上面三段寫：① 字少（tier）② 卡片少（n，只有卡片列才寫）③ 套用 `max()`。
3. 重跑 `python3 build_layouts.py`，`check_deck.py all-layouts-demo.html --measure` 要 0 FAIL、無溢位／重疊。
4. 做一次「刪字模擬」：開 demo 按 E，把那個版型的卡片字清到剩幾個字、再整張清空，確認放大後沒有超出 `.slide-frame`（按 g 看安全線），有超出就把該階段的字級調小。
5. 在本節的階段表加一列。

---

*相關：`slide-system.md`（版型骨架）、`content-style.md`（文案去 AI 感）、`migrating-vw-to-css.md`（舊 JS/vw 檔轉本版）。*
