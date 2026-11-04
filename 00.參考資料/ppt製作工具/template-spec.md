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
- **內容垂直置中**：內容頁主內容容器用 `flex:1;min-height:0` 撐滿安全框、再加 `justify-content`／`align-content:safe center`——內容少時置中填滿、內容多時 `safe` 自動退回頂端對齊不裁切（`grid/cards/kpi/rows/split/stats/steps/flow` 皆已內建）。

---

*相關：`slide-system.md`（版型骨架）、`content-style.md`（文案去 AI 感）、`migrating-vw-to-css.md`（舊 JS/vw 檔轉本版）。*
