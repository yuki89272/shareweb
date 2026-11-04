# 永續能源說課簡報 × numeracy-deck-kit 整合診斷報告

> 對象：`主題課/永續能源/sustainable-energy-lesson-pitch.html`，底層 `numeracy-deck-kit`（CSS 自適應版）
> 日期：2026-06-16

## 結論摘要（TL;DR）
- **設計語言沒有不同**：deck 用的 `base.css`／`presenter.js` 與 numeracy-deck-kit 原版**逐位元組相同**，所有外觀差異 100% 都在 deck 自己的 inline `<style>`＋內容裡。
- 三個外觀差異各有根因：**logo＝打包脆弱＋手抄失誤**、**顏色＝規格缺口逼出即興**、**版型細節＝驅動方式（inline 擴充）但缺 template-spec**。
- **CSS 版（0616）與 JS 版（老師的 _20260613）16:9 機制不相容**：正 16:9 看起來一樣，非 16:9 混用會跑版；舊 JS 檔需轉換。
- deck 本身是純 CSS 0616、無混用，`check_deck --measure` 0 FAIL／0 溢位，可獨立正常播放。

---

## 一、共用資產驗證
| 檔案 | 與 numeracy-deck-kit 原版比對 |
|---|---|
| base.css | 逐位元組相同 |
| presenter.js | 逐位元組相同 |

→ 字體、配色 token、16:9 機制、bleed 規則的「源頭」一致。差異不是換了設計語言，而是 deck 內的三個動作造成。

## 二、三個外觀差異與根因

### 1. Logo 跑掉（確定，最該先修）
- 現象：每頁 brand-footer／封面／收尾的 logo 縮在左邊、右邊一大塊空白。
- 量到：deck 的 `<symbol id="nl-logo">` 只有 **1 條 `<path>`，原版有 17 條**。只貼了左邊那顆抽象 mark，沒貼完整「數感實驗室 NUMERACY LAB」字標；但 viewBox 仍是完整字標的寬比（162.16×45.83）→ mark 被塞進為整個字標開的框裡。
- 根因：**打包脆弱 ＋ 手抄失誤**。logo 是唯一塞不進 base.css 的東西（SVG path 資料），只能以 inline `<symbol>` 放 template.html、每份 deck 手抄 → 容易抄錯。
- 修法：把 template.html 完整 17-path symbol 整段換回。

### 2. 顏色不一樣（確定）
- deck 用到、但不在 numeracy-deck-kit 調色盤的色：
  - **紅 `#BE2026`（8 處）**：避開欄框線／圓點／標籤、L4「結尾埋種子」標、P2 淘汰主軸的 ×。
  - 淺綠 `#E0EFE7`（封面 SVG）、米色 `#E8E0D2`（P6 註解框線）。
- numeracy-deck-kit 品牌色只有：綠 `#379C39`／深綠 `#004B24`／米白 `#FEF4E8`／螢光黃 `#E8FF3A`／墨黑 `#0A0A0A`／灰——**沒有紅、也沒有語意（負面）色**。
- 根因：**規格缺口逼出即興**。要表達「避開↔著重」「淘汰」，系統沒有負面色 token、也沒規定否定怎麼呈現，於是自抓了紅。
- 待確認：團隊「避開／否定」的慣例（用灰？墨黑？不上色？），定了再統一改，避免再自創。

### 3. 版型細節不一樣（推斷）
- deck 自寫了約 8 個版型（probe-q／line／arch／energy／compare／rows 的 kicker+intro／split 的 note），而非用 numeracy-deck-kit 的 10 個標準版型。
- 字體、綠標題線、米白卡都沿用設計語言（故「看起來類似」），但這些自訂版型的**間距、邊框粗細、圓角**是自定的 → 細節飄。
- 根因：**驅動方式**。kit 本就設計成「inline 擴充」（自寫 probe-* 是預期用法），但**缺 template-spec**（哪種內容對應哪個標準版型、間距/邊框正典值），擴充就只能重定 → 飄移。

## 三、設計語言 / 打包 / 驅動 的歸納
| 症狀 | 設計語言 | 打包 | 驅動方式 |
|---|---|---|---|
| Logo | 同 | 脆弱（無法走 CSS 共用） | 手抄抄錯 |
| 顏色 | 同 | 缺負面色/規格 | 即興補色 |
| 版型細節 | 同 | 缺 template-spec | inline 擴充 |

> 不是設計語言問題，也不是 base.css 打包錯；是「手抄 logo＋inline 擴充」這個驅動方式，撞上兩個打包/規格缺口（logo 無法 CSS 共用、缺負面色與 template-spec），讓照規範做也會在這三點飄。

## 四、CSS 版 vs JS 版的 16:9 機制分岔
> 限制：本工作區只有 0616（CSS）與一個無日期 vw 版；老師的「vw＋JS 縮放」版（_20260613）不在此，JS 端細節依 0616 README ＋原理推得。

| | 老師（JS 版） | 0616（CSS 版，本 deck） |
|---|---|---|
| 單位 | `Nvw` | `calc(N*var(--u))`，`--u=1cqw` |
| 1 單位＝ | 視窗寬 1%（viewport） | `.deck` 容器寬 1%（16:9 舞台，`container-type:inline-size`） |
| 鎖 16:9 | JS 算尺寸/縮放 | 純 CSS：`min(100vw,177.7778vh)＋aspect-ratio:16/9` |
| 左右延伸底 bleed | JS 各自處理 | `body:has(.deck .slide.active.probe-X)`＋接縫 `calc(50vw-0.12*min(...))` |

**為何「看起來類似、混用跑版」**
- 正 16:9 螢幕：`1vw == 1cqw`，數字等值 → 乍看一樣。
- 非 16:9：
  - vw 版頁 → CSS 引擎：`vw` 對視窗量，但舞台已被 `min()` 縮成 16:9，視窗寬 ≠ 舞台寬 → 相對舞台過大/小 → 溢位。
  - `var(--u)` 版頁 → 無 `container-type` 的 JS deck：`cqw` 無查詢容器 → 退回亂抓 → 塌掉。
  - bleed 接縫綁 CSS 舞台幾何，JS letterbox 不同 → 底色對不齊。

## 五、舊檔轉換（JS/vw → CSS/0616）
因 16:9 下數字 1:1，多為機械式：
1. 換引擎：改用 0616 `base.css`＋`presenter.js`，移除舊 JS 縮放器。
2. 單位：inline `<style>` 內 `Nvw` → `calc(N*var(--u))`。**保留** `@media print` 與 `min(100vw,…)` 舞台算式的 vw/viewport，不可盲 replace。
3. 重設 bleed：每頁 `body:has(.deck .slide.active.<該頁class>)` 補對底色、章節接縫 class 對上。
4. 內容包進 `.slide-frame`（舊版若無安全框）。
5. 跑 `check_deck --measure` 抓溢位。
> 第 2 步可寫小腳本自動化（跳過 print 區塊），其餘人工確認。

## 六、建議
1. **全隊統一引擎**（0616 README 已要求）。CSS 版更穩（零 JS、任何螢幕自適應、且已含 bleed）→ 建議收斂到 CSS/0616，舊 JS 檔照第五節轉。
2. **把 logo 改成防呆**：保留單檔 inline symbol 的前提下，於 `check_deck.py` 加一條「logo symbol 完整性」檢查（path 數/關鍵 d 值），手抄殘缺即 FAIL。
3. **補 template-spec**（哪種內容用哪個版型＋間距/邊框正典值）＋**定義語意色**（至少一個「負面/避開」色或慣例），消除即興與細節漂移。
4. Windows 跑工具的眉角：`check_deck.py` 要 `PYTHONIOENCODING=utf-8`；`--measure` 的 Chrome 清單要加 Edge 路徑。

## 七、待確認
- 老師 JS 版（_20260613）實檔未取得，JS 端細節待對檔確認。
- 「避開/否定」的團隊配色慣例。
- template-spec 是否要做（對應 present-system PLANNING 開放問題 #1）。
