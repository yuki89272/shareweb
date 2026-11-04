# CHANGELOG — numeracy-deck-kit（數感簡報模板）（自適應版）

> 本檔記錄 kit 本身的變更與決策。最新在上。

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
