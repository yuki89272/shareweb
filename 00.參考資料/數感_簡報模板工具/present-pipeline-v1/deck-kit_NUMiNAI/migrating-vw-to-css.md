# 從 vw／JS 版遷移到 CSS 自適應版（本版 0616）

> 為什麼會有這份：團隊曾有兩套鎖 16:9 的做法——**舊版用 `vw`＋JS 縮放**，**本版（0616）用純 CSS 自適應**（`--u = 1cqw` ＋ `aspect-ratio`）。兩套**不相容**，混用會跑版。本檔說明差異、為何不相容、以及怎麼把舊檔轉過來。

## 一、兩套差在「1 個單位是對誰量的」

| | 舊版（vw＋JS） | 本版 0616（CSS 自適應） |
|---|---|---|
| 作者單位 | `Nvw` | `calc(N*var(--u))`，`--u = 1cqw` |
| `1` 單位＝ | 視窗寬的 1%（**viewport**） | `.deck` 容器寬的 1%（**16:9 舞台**，靠 `container-type:inline-size`） |
| 鎖 16:9 | JS 計算尺寸／縮放 | 純 CSS：`.deck{width:min(100vw,177.7778vh);aspect-ratio:16/9}` |
| 左右延伸底 bleed | JS 各自處理 | `body:has(.deck .slide.active.probe-X)` ＋章節接縫 `calc(50vw-0.12*min(100vw,177.7778vh))` |

## 二、為何「看起來一樣、混用卻跑版」

- **正 16:9 螢幕**：舞台寬＝視窗寬，所以 `1vw == 1cqw`，兩版數字完全等值 → 乍看一模一樣。
- **非 16:9（超寬／偏方／偏高視窗）就分家**：
  - 把 **vw 版的頁**丟進 CSS 引擎：`vw` 是對視窗量的，但舞台已被 `min()` 縮成 16:9，視窗寬 ≠ 舞台寬 → 內容相對舞台過大或過小 → 溢位／跑版。
  - 把 **`var(--u)` 版的頁**丟進沒有 `container-type` 的 JS deck：`cqw` 找不到查詢容器 → 退回亂抓（常塌成極小）。
  - **bleed**：本版的 `body:has()` ＋接縫數學綁的是 CSS 舞台幾何；JS 版 letterbox 機制不同，混用底色會對不齊。

> **團隊定案（2026-06-16）：以 CSS 自適應版（本版 0616）為準**；舊 vw/JS 版 deprecated。理由：零 JS、任何螢幕自適應、內建 bleed。同一份簡報不能換底層，舊檔請依下方步驟轉成 CSS 版。

## 三、轉換步驟（舊 vw/JS → 本版 CSS）

因為 16:9 下數字 1:1 相等，多為機械式：

1. **換引擎**：HTML 改引用本版 `base.css`、`presenter.js`；移除舊的 JS 縮放器與其呼叫。
2. **換單位**：inline `<style>` 裡 `Nvw` → `calc(N*var(--u))`。
   - **保留 viewport 的兩處不要動**：`@media print` 區塊；`.deck` 的 `min(100vw,177.7778vh)` 舞台算式。
   - `check_deck.py` 字級檢查兩種寫法都認得。
3. **包安全框**：每頁內容包進 `<div class="slide-frame">`（封面/章節/呼吸頁/收尾例外）。
4. **重設 bleed**：每頁加／對好 `body:has(.deck .slide.active.<該頁class>)` 的底色；重用標準 `probe-*` 類名可直接吃現成規則。章節頁用左綠右米白接縫規則。
5. **驗收**：`python3 check_deck.py 檔.html --measure`，要 0 FAIL／0 溢位。

> 第 2 步可寫小腳本自動化（務必跳過 `@media print` 區塊與 `min(100vw…)`）；其餘人工確認。

## 四、怎麼判斷一份舊檔是哪一版

- 看 `<head>` 引用的 `base.css`：本版開頭有 `--u: 1cqw;`、`.deck{…aspect-ratio:16/9;container-type:inline-size}`。
- 看 `presenter.js`：舊版常有 `resize` 監聽＋`transform: scale()` 或設 `style.width/height` 的縮放邏輯；本版沒有（只處理翻頁）。
- 看 deck 內尺寸：滿是裸 `Nvw` ＝ 舊版；`calc(N*var(--u))` ＝ 本版。

---

*相關：`README.md`（相容性提醒）、`slide-system.md` ⓪（自適應單位規範）、`template-spec.md`（版型紀律）。*
