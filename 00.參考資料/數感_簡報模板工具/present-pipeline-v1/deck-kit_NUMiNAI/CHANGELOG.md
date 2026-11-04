# CHANGELOG — deck-kit_數感實驗室（數感簡報模板）（自適應版）

> 本檔記錄 kit 本身的變更與決策。最新在上。

## 2026-09-14

起因：年度主管會議 deck 第二輪 dogfood——老師大量刪字後版面要跟著「補回」，動畫要跟講述邏輯走，並要每頁可以按一下揭曉。

### 新增
- **補回階段**：`presenter.js` reflow 之後對 `data-grow` 元素依可見字數標 `data-tier="s|m|l"`（≤45／≤100／更多），對卡片列標可見張數 `data-n`；`base.css` 新增 16 個版型的放大階段（見 `template-spec.md` §九）。刪字只會收掉空位，補回才把剩下的放大填滿。
- **按一下揭曉**：元素加 `data-reveal` 進頁時藏著（佔位），按 →／點右邊一次演出來，再按才翻頁；右下角頁碼旁黃點＝這頁還有一段；←一律回上一頁；列印全顯示。
- **骨架不動、論點動**：自動動畫改成標題、軸線、標籤、有框方塊、頁尾不動，只動長條／折線／圓點／圓餅／表格逐列／數字跑／卡片依序／帶子最後；圖裡的字跟形狀一起出；`data-seq` 講述順序；新增 `in-y`、`draw-rev`。
- **check_deck 編輯後檢查**：measure 多量每頁內容覆蓋率、色塊內容佔比、最小字級，低於門檻列 WARN（不算 FAIL）。
- **全幅圖延伸進上下留白（2026-09-17）**：全幅 `<img>` 加 `data-bleed="X Y"`（百分比，對應 object-position，預設 50 50），`syncLetterbox()` 會把同一張圖用同樣的縮放與位置鋪在 body 上；螢幕不是 16:9 時，上下的留白就是圖的延伸，頁碼那一帶也在圖上，而不是一條色帶。視窗改變大小會重算。
- **全螢幕留白跟著頁面底色（2026-09-17）**：`syncLetterbox()` 換頁時把 body／html 底色設成該 section 的底色（章節頁沿用左綠右米白漸層）；離開一頁時揭曉的重設等淡出跑完再做。
- **舊分頁存檔保護（2026-09-17）**：build 在 `<head>` 寫 `<meta name="deck-build">`；`serve.py` 提供 `GET /__build`，`POST /save` 時比對戳記，分頁比磁碟舊就回 409 不寫；presenter 存檔前先查、被擋就提示重新整理，不退回下載。修改留在 localStorage，重新整理後自動回來。
- **deck-edits 版本號**：頁面結構重做時清掉該頁舊修改並把 `rev` 加一，瀏覽器看到 rev 不同就丟掉舊的本機快取。

### 修正
- `.is-cleared` 改為 `!important`，版型自己的 `display:flex／grid` 不會把收起的方塊再打開。
- 揭曉的 HTML 容器本身也藏起來（之前會剩空色塊）；數字跑上去只在自己出現時跑、不重跑。
- 標題不再進場動畫（一開始就在，不會有空白頁）。


## 2026-09-13

起因：年度主管會議簡報 dogfood。老師要在瀏覽器裡自己改字、直接存回同一個檔，而且改完版面要自己跟著重排；動畫要依功能自動配。

### 新增（編輯與儲存）
- **編輯模式（按 E）**：頁面上所有文字點一下就能改，SVG 圖裡的字點一下跳小輸入框（Enter 確定）。修改存在 `<script id="deck-edits">`（eid＝「頁:第幾個有字的元素」；SVG 字「頁:sN」），另存一份也在 localStorage。
- **儲存零對話框**：`serve.py`（本機 127.0.0.1:8765，`POST /save` 原子寫回、`backups/` 留 20 份）＋ `開啟簡報.command`（雙擊即開，預設開資料夾裡最新的 .html）。直接雙擊 html 開則走 Chrome File System Access（第一次選檔）。
- **存回原始 DOM**：儲存寫回 build 出來的原始內容＋修改清單，重開檔案時元素順序不會位移；修改內容會清掉 data-eid／contenteditable 等編輯屬性。
- **keep_edits.py**：重新產生 HTML 後把舊檔的 deck-edits 搬回新檔（AI 重建前必跑）。
- **自動重排 `reflow()`**：整塊文字刪掉 → 方塊收起（`.is-cleared`）、全空的容器一起收、卡片列網格重新分欄、`.slide-frame > [data-fill]／.chart` 吃掉空出來的空間。載入、每次輸入、SVG 改字後都跑。
- 右上角模式藥丸開場 5 秒後淡出，按任何鍵再顯示 3 秒。

### 新增（動畫 v2：依功能自動配）
- `presenter.js` 的 `autoAnim()`：標題浮上 → 圖表（同基準線的 rect＝直條 `anim-bar-v` 長上去、同左緣的＝橫條 `anim-bar`、折線／連線 `anim-draw` 畫出來（自動算 `--anim-draw-len`）、圓點與有填色的形狀 `anim-pop`、圖內文字最後浮上）→ 表格逐列（`anim-rows`）→ 卡片列依序浮上 → 帶子最後；KPI 數字（類名含 `__n`／`__big`／`kpi`）從 0 跑到目標值（`anim-count`）。整頁最晚 1.8 秒到齊。
- 任何元素可寫 `data-anim="up|fade|pop|drop|slam|left|right|stamp|bar|bar-v|draw|count|rows|none"` 指定；`<section data-anim="none">` 整頁關；作者自己掛的 anim-* 不會被覆蓋。
- `base.css` 新增 `.anim-bar-v`、`.anim-rows`，並給 SVG 的 bar／pop 補 `transform-box:fill-box`。
- **動畫要跟著講述邏輯（2026-09-14 補）**：任何元素（含 SVG 的 `<g>`）可寫 `data-seq="1,2,3…"`，同一步的元素一起出現、每步相隔 0.38 秒；沒標的元素當底圖先出。沒有 data-seq 的圖表：形狀先出，字跟著它所在的形狀一起出（不再「形狀全放好，字才跑進來」）。新增 `data-anim="in-y"`（沿自己的 y 軸滑入，箭頭往內指用）與 `draw-rev`（從尾端往回畫）。KPI 數字等到自己出現才開始跑。例：P13 三個外圈 → 三支往內的箭頭滑入 → 中心圓與字一起彈出；P12 座標 → 我們在這裡 → 授權框撐開 → 右欄 NUMiNAI 滑入 → 左上新服務。
- `shot.sh`／`check_deck.py` 的 Chrome 加 `--force-prefers-reduced-motion`：截圖與量測一律關動畫。
- `slide-audit.js` 只在 headless／`?audit` 時才把結果寫進 document.title（之前會把分頁標題蓋成 JSON）。


## 2026-08-15

起因：用本 kit 實做「啟動數感・財務課調整說明」簡報（dogfood），一輪實戰累積出動畫需求與六條版面／流程經驗。

### 新增（動畫）

- **通用進場動畫 class**：`.anim-bar`／`.anim-bar-w`（線條展開）、`.anim-up`／`.anim-fade`／`.anim-pop`／`.anim-drop`／`.anim-slam`／`.anim-left`／`.anim-right`／`.anim-stamp`／`.anim-draw`，以及容器用的 `.anim-stagger`（子元素依序進場）。掛 class 即用，不必每份 deck 各自重寫 keyframes。
  - 支援 `--anim-delay`、`--anim-dur` 兩個變數個別調時間。
  - 包在 `.rvz` 翻牌裡的動畫**自動改為「翻開才播」**，不會在牌還沒翻時就演完。
- **presenter.js：按 `M` 的動態總開關**。開關會在 `<html>` 加／移除 `.no-motion` 一次關掉全部動畫；設定記在 `localStorage`，換頁、重開檔都記得。系統層開了「減少動態效果」（prefers-reduced-motion）時**預設為關**。

### 修正（check_deck.py）

- CSS 解析改為**認得 `@` 區塊**：`@keyframes`／`@media`／`@supports`／`@font-face` 整段保留，不再被拆進頂層規則。消除 keyframes 裡的 `from`／`to` 被誤判成「重複 selector」的假警告。
- `--fix-css` **只合併頂層規則**，並加上**動畫指紋自我驗證**——合併前後比對動畫相關內容，不一致就中止，避免自動合併把動畫改壞。

### 文件（六條實戰經驗回灌）

- `slide-system.md`
  - §一 新增「**重排頁序（搬頁）的兩個陷阱**」：切頁要用 `re.split(r'(?=<section class="slide)')` 並先斷言頁數；頁碼＝實際位置（無標籤的滿版頁也佔號），搬完要逐 section 依位置重編、禁止全域取代，附三項搬完驗證。
  - §二 新增「**版面高度預算**」表：56.25u −12u 安全邊 ＝ 44.25u 可用；扣 page-hero（約 8.2u）與 cite（約 2.4u/行）後主內容區約 33.5u。排版前先加總，不要排完才發現爆框。
  - §四 新增 **Pattern 5**（grid 欄內圖片勿用 `height:100%`：row 為 `auto` 時解析不到，`<img>` 用內在比例撐爆整頁；改給確定高度＋`object-fit:cover`）、**Pattern 6**（滿版圖轉場頁遇淺色照片要 inline 覆寫更厚的 `.probe-fb__scrim`）。
  - §五 checklist 補：高度預算先加總、圖框勿 `height:100%`；新增「[改內容時] 出處一致」一組。
- `template-spec.md` §八 版型陷阱：補「grid 圖片勿 `height:100%`」與「淺色底圖要自訂 scrim」兩條（附可抄片段，細節指向 slide-system §四）。
- `image-sourcing.md` §九：新增「**方圖塞橫框：用 `object-position` 救裁切**」（`f ＝ (框高/框寬)×(圖寬/圖高)`、可見區間 `[Y×(1−f), Y×(1−f)+f]`、實測 `65%~72%`）與「**生圖 prompt 的兩條硬規則**」（禁一切文字／留白給字）。
- `content-style.md`：新增 §六「**出處（cite）紀律**」——cite 只列頁面上真的看得見的數據來源，刪資料要同步刪出處；原「自我檢查清單」順延為 §七並加第 6 條。

## 2026-06-23

起因：present pipeline 需要「版型單一真相」來對齊；舊 `decks/template.html` 是事實上的全版型大雜燴檔，present 對齊與維護都不穩。

### 決策
- **版型拆成 `layouts/<name>.html`（一型一檔、雙擊就開）＝單一真相。** 13 型：cover/chapter/hero/grid/cards/spotlight/rows/split/kpi/stats/breather/flow/thanks。每檔自帶該版型 CSS（版型 CSS 互不重疊，內嵌讓每檔自含、可獨立開），連 `../base.css`。
- **CSS 放哪**：選「每檔自帶」而非抽共用 layouts.css——延續「CSS 跟著 markup 走、複製即用」模型、不增 deck 依賴。
- **template.html 去留**：刪除（人用全版型起手檔；present 驅動後不需要，少數手動起手用 starter.html）。改以**生成的組裝 deck** 取代其「看整體」功能。

### 新增
- `layouts/*.html`（13 檔）：版型單一真相。每檔皆 check_deck 0 FAIL。
- `build_layouts.py`：從 layouts/ 組裝出 `all-layouts-demo.html`（**組裝合約的可執行版**）；present 組裝 deck 照同一套規則。
- `slide-system.md` §一新增「組裝合約」：合約的人讀版（一個 head／symbol 一份／section 串接重編頁碼／bleed class／腳本結尾／0 FAIL）。

### 修改
- `all-layouts-demo.html`：改為由 build_layouts.py 從 layouts/ 自動組裝（勿手改）；兼 check_deck 整合測試標的（13 頁 0 FAIL）。
- `slide-system.md`、`README.md`：版型參考指向 `layouts/` 與 `all-layouts-demo.html`，移除對 `decks/template.html` 的指引。

### 修正
- `layouts/stats.html`、`layouts/breather.html`：**改用 `.slide-frame` 包內容**，解決翻頁時 page-label/logo 位移飄動。
  - 根因：`.slide` 是 `container-type:size`、`--u=1cqw`（容器內容寬的 1%）。非框頁的水平 padding 會縮小內容寬 → `--u` 跟著縮 → 絕對定位的 page-label(左 7u)/brand-footer(右 7u) 連同所有內容一起位移縮放，與框內頁（padding:0、cqw=16px）對不齊。
  - 解法：包進 `.slide-frame` → 觸發 `.slide:has(.slide-frame){padding:0}` → cqw 回到 16px、chrome 與框內頁同位；內容靠絕對定位的 frame 內縮到安全邊距，不影響 cqw。這也是其他內容頁的標準做法（stats/breather 原本是漏接 frame 的兩個特例）。
  - 驗證：Playwright 量測三頁 page-label 皆 (112,48)、brand-footer 皆右 1488/底 868；check_deck 0 FAIL、--measure 0 溢位。

### 刪除
- `decks/template.html`（功能由 layouts/ ＋ all-layouts-demo.html 取代）。

### 後續（present 第一輪 dogfood 回灌）
- **新增版型 `probe-steps`**（`layouts/steps.html`）：線性多步流程，flex 自動分配 **3–5 節點**（A→B→C→…），節點卡＋→箭頭＋STEP 序號。補上 dogfood 暴出的「4+ 步流程無版型」缺口（既有 `probe-flow-page` 只吃 3 節點且為循環）。template-spec §一/§二、build_layouts.py ORDER 已登錄；all-layouts-demo 14 頁 0 FAIL/0 溢位。
- **新增 `logo-symbol.html`**：logo SVG symbol（17 path）獨立片段檔，貼進 deck `<body>` 用，免從 layout 摳、免手抄殘缺。
- **template-spec §六 改寫為「新增版型流程」**：複製最近 layout→改→登錄 §一/§二→`build_layouts.py` 重建→check_deck。確立「加版型＝複製一檔+登錄+重建，不動既有/引擎」的可維護擴充點；並把「承載內容字 ≥2u、別套展示用小字」寫進紀律。
- **已知保留（滾動修正）**：部分 layouts 字級為單頁展示調、低於 2u（如 `probe-hero__bubble`/`probe-rows__item`），承載內容時需個案上調；check_deck 對自訂 class 只 WARN。present skill 已加警告，暫不統一改值。
- **新增警示語意 `.alert` 修飾類（base.css）**＋ template-spec §四「落地對照」：第三輪 dogfood（培訓 SOP）暴出「§四只有紅色原則、無可抄手段，每個 SOP deck 各自重發明」。現在 `.probe-grid__card.alert`/`.probe-cards__card.alert`/`.probe-rows__row.alert`＋`.alert-mark`（紅 ×）＋`.tbd`（待填佔位）內建於 base.css，掛修飾類即用、不另立紅版型；§四附可抄片段與「`×`(U+00D7) 可當警示符、`⛔` 只能放 plan-note」。present skill 培訓行已指向此。

## 2026-06-16

起因：用本 kit 實做「永續能源說課簡報」當 dogfood，從整合痛點長出以下修正。

### 決策
- **16:9 機制定案：以 CSS 自適應版（本版）為準**，舊 `vw＋JS 縮放`版 deprecated。理由：零 JS、任何螢幕自適應、內建底色延伸（bleed）。
- **內容爆框策略定為三階**（選 option 3）：`砍字（紀律）→ autocol（分欄、保可讀）→ autofit（縮放、最後手段、可能 <2vw）`。三者並存但有先後，autofit 不可取代砍字。
- **語意色定案**：新增 `--alert`(`#BE2026`)／`--alert-soft`(`#FBEAE9`) token ＝負面／避開／警示（少量用）。釐清四語意分工：正面=綠、負面=紅、強調=螢光黃、次要=灰。base.css、template-spec §4 已更新；dogfood 簡報原即興的 `#BE2026` 已全改 `var(--alert)`。先沿用 svg-patterns 既有的 `#BE2026`，覺得跟暖底衝再調。

### 新增
- `template-spec.md`：版型紀律（何時用哪型、內容→版型對應、字級紀律、顏色紀律、間距/邊框/圓角正典值、擴充守則、防呆對照）。補上「template-spec 該不該做」這個長期開放問題。
- `migrating-vw-to-css.md`：舊 vw/JS 版 → 本版 CSS 的差異原理、為何混用跑版、轉換 5 步、版本辨識。
- `decks/starter.html`：**極簡起手檔**（封面＋1 內容＋收尾，內含完整 17-path logo）。降低起手門檻（template.html 是全 10 版型、偏重），也根治 logo 手抄。

### 修改
- `check_deck.py`：
  - 新增 **logo symbol 完整性檢查**——用了 `<use href="#nl-logo">` 卻找不到 symbol、或 path 數 <10（完整應 17）即 FAIL。起因：dogfood 簡報手抄 logo 只貼了 1/17 條 path，logo 跑掉。
  - `--measure` 的 Chrome 偵測清單**加入 Windows Chrome/Edge 路徑**（跨平台）。
  - `sections()` **先去 HTML 註解再偵測** `<section>`——避免註解裡寫到字面 `<section>` 被誤算成一頁、害頁碼錯位 FAIL（做 scaffold 時踩到）。
- `slide-system.md`：§五新增「[內容塞不下時] 三階策略」；§六新增「選配腳本」說明（autocol/autofit 載入與取捨）。**§三版型 class 名對齊 template.html**（`probe-p2/p3/concept/flagship/layers` → `hero/grid/split/cards/flow-page`，含子元素如 `__card-label`→`__label`），消除與 template/base.css 命名打架；template-spec 指向 §三 的連結因此對得上。
- `README.md`：相容性提醒改記「定案以 CSS 版為準」並指向 migrating 文件；檔案表補 `template-spec.md`、`migrating-vw-to-css.md`、`autocol.js`、`autofit.js`、`CHANGELOG.md`、`decks/starter.html`。
- `shot.sh`：**跨平台**——Chrome 偵測清單加入 Windows Chrome/Edge；`file://` URL 把 git-bash 的 `/c/...` 正規化成 `C:/...`；輸出目錄絕對化（headless 對相對輸出路徑不可靠）。已在 Windows 實測產圖成功。

### 收編原為「孤兒」的檔
- `autocol.js`、`autofit.js`：先前已寫好但無任何文件/HTML 引用、沒人知道存在。本次正式文件化並納入三階策略（見上）。

### 待辦（未完成）
- （目前無）本輪「完善擴充包」的項目皆已收尾。

### Windows 使用備忘
- 跑 `check_deck.py` 在 cp950 主控台印 `⚠` 會 crash → 用 `PYTHONIOENCODING=utf-8 PYTHONUTF8=1 python check_deck.py …`。

## 2026-09-06

起因：2027 AI 數感盃教師研習首版做完，實測**平均 132 字/頁、動畫用量 0**，老師退回並指定比照 `AI與教育／ai-education-math.html`（平均 66 字、中位數 47、動畫約 340 處）重做。追查發現這兩件事**在整套文件裡從來沒被寫成規則**——字數上限完全沒提，動畫只有目錄沒有「必須用」。

### 新增（同日第四輪：動畫節制＋互動元件）

老師看完回饋：「動畫太多，可以少一點。但可以做一些互動按鈕。」實測比對——本 deck 6.6 個動畫／頁、`ai-education-math.html` 4.3／頁，而老師指名參考的 `finance-course-2026.html` 是 **0 個進場動畫**：它的動態只出現在「點擊之後」。

- **`AI-START-HERE.md` 硬規則 #11 改寫**：從「每頁至少掛一組動畫」改成「**每頁 1–2 組、全場平均不超過 2 組／頁**」，並點名 `anim-stagger` 最吵；最重要的一句是「**要一個一個出現，優先做成互動（點擊），不要做成計時**」——計時的問題是講者控制不了節奏，觀眾還沒想完答案就跑出來了。
- **`slide-system.md` §四 Pattern 10「互動元件」**：三種模式（點擊揭曉／逐步點擊／選項按鈕）的完整 markup ＋ 三條共通規則（一定要 `event.stopPropagation()`；用 `opacity` 藏而不是 `animation` 藏，按 `M` 關動畫後互動照樣能用；`.optans` 用 `visibility` 佔位免得版面跳）。
- **`base.css` 內建這三組元件**（`.rvz__cover` / `.stepclick`＋`.stepitem`＋`.stepdone` / `.optbtn`＋`.optans`），以後直接掛 class 就有，不必每份 deck 重寫。
- **`check_deck.py` 的重疊偵測略過 `rvz__cover`**：蓋牌本來就是刻意疊在答案上，之前會誤報「真破版」。

> 驗收踩到的坑：headless Chrome 加 `--virtual-time-budget` 時，`getComputedStyle` 讀到的值不可靠——點擊後 class 明明加上了、`el.matches()` 也回 true，opacity 卻沒更新。**互動要用「點擊後截圖」驗收，不要用 computed style。**

### 新增（同日第三輪：章節頁）

同一份 deck 再補 12 頁章節頁（4 章頁＋7 小節頁＋1 講者頁），60 → 72 頁：

- **`slide-system.md` §四 Pattern 9「章節頁（兩級）」**：章頁＝全幅 gen-image、小節頁＝深綠清單，兩級並存。四條原則——章與第一小節合併（不要連兩張分隔頁）／編號用 1/2/3 不用 A/B/C（規劃文件要一起改）／小節頁只換 highlight、重播只讓那一行動／進度條用 `flex:<分鐘數>` 標比例、**不標絕對分鐘**（超時才不會打自己臉）。
- 同節補上兩個陷阱：**`.probe-breather` 是 `text-align:center`**，章節頁要自己覆寫成 left，否則大標會被推到照片最雜的那半邊；**插入既有 deck 後必須按 section 順序重編 `page-label__num`**，不可全域取代（`plan-note` 裡也有大量 `P<數字>`），換算規劃文件時要遮罩保護「別份簡報」的頁碼參照。
- 頁數預算寫清楚：章節頁不吃「頁數 ＝ 分鐘 ÷ 2」的內容頁預算，總頁 ＝ 內容頁 ＋ 節奏頁。

### 新增（同日第二輪：配圖）

同一份 deck 接著補了七張 gen-image（封面／算盤／簽名／牆洞／生活物件／打磨／收尾海景），過程踩到四個定位坑，全部寫回文件：

- **`slide-system.md` §四 Pattern 7「把一般內容頁改成滿版底圖」**：完整 markup ＋ CSS 配方，並列出三條紅線——section 不可加 `position:relative`（`.slide` 在 base.css 已是 `absolute;inset:0`）；`page-label`／`brand-footer`／`slide-frame` **只能加 `z-index`**，改 `position` 會掉回文件流直接衝出邊界。附「氣氛圖走滿版、焦點圖走側欄」的取捨原則，以及通用 `.aicap` AI 圖註樣式。
- **`slide-system.md` §四 Pattern 8「覆寫既有版型前先 grep」**：`grep` 要寫 `\.classname\s*\{`——`\s*` 不可省，否則會漏掉寫成 `.classname {` 的規則，誤以為沒人定義過而整條重寫。實際後果：覆蓋了 `left` 但原規則的 `transform:translateX(-50%)` 還在，整排 QR 被推出畫面。原則是**能只加一個屬性就別重寫整條**。
- **`slide-system.md` §五〔改版面時〕佈局**：補三條 checklist（先 grep 再覆寫／滿版底圖三紅線／AI 生圖每張都要掛「示意圖為 AI 生成」）。

### 新增
- **`AI-START-HERE.md` §3 硬規則 #10／#11**：每頁可見中文字 ≤ 80（硬上限 140）；每頁至少掛一組動畫。
- **`AI-START-HERE.md` §5**：補上 linter 抓不到、必須自己跑的兩段量測指令（字數統計、動畫用量），以及**動畫的驗收陷阱**——`shot.sh` 截靜態畫面，可能在動畫播完前截到；QA 要先掛 `no-motion` 確認「不播也看得懂」再打開確認有掛上。
- **`content-style.md` §八「每頁字數與頁面公式」**：實測基準表、頁面公式（page-hero → 2–3 個「標籤＋一句話」內容塊 → page-foot）、砍字五條紀律、圖片角色（隱喻照片最能省字，基準 1.3 張/頁）。
- **`slide-system.md` §五 新增「[每頁完成時] 字數與動畫」檢查段**，含互動頁的解法：問題與答案同頁時，答案掛 `--anim-delay:3s` 延遲浮現，比拆頁或翻牌都簡單。

### 同步
兩份 kit（`deck-kit_數感實驗室`／`deck-kit_NUMiNAI`）的 `content-style.md`、`slide-system.md` 已同步，md5 一致。
