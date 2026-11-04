# HTML 簡報設計系統 — AI Context 文件（自適應版）

> 本文件用於指導 AI 產出 HTML 簡報。讀完後你應該能：
> 1. 用十種基礎版型組裝一份完整簡報
> 2. 在改版面時避開已知的坑
> 3. 維持一致的視覺語言

---

## ⓪ 自適應單位規範（務必先讀）

本版底層改成**自適應**：舞台鎖 16:9 雙向置中，尺寸單位由 `vw` 改為 `--u`，
任何螢幕（超寬、超扁、投影機）都不裁切、不漂移。

- **單位**：`--u`（定義在 base.css，`--u: 1cqw` = 舞台寬的 1%）。所有尺寸寫成
  `calc(N * var(--u))`，**禁用 `vw` / `vh`**（列印 `@media print` 區塊除外）。
- **換算**：本文件以下各版型的「關鍵 CSS」仍以舊的 `Nvw` 寫法呈現作為比例參考；
  套用時一律寫成 **`calc(N * var(--u))`**（一般 vw 範本的 `Nvw` 對應於此）。16:9 螢幕下兩者等值，
  所以「內容字 ≥ 2vw」鐵則 = **`≥ calc(2 * var(--u))`**。
- **優先用語意 token**：base.css 已備好 `--fs-hero`、`--fs-card-title`、`--fs-body`、
  `--fs-sub`、`--fs-small` 等，能用 token 就別寫死數字。
- **內容安全框**：每頁內容包進 `<div class="slide-frame">`（滿版例外：封面/章節/呼吸頁/收尾），
  連 `absolute` 也跑不出安全範圍；放映按 `g` 顯示安全線。
- **底色延伸（bleed）**：舞台外 letterbox 跟著該頁底色（白/米白/深綠；章節頁左綠右米白）。
  靠 base.css 的 `body:has(.slide.active.probe-X)` 規則——做自己的 deck 時，把那些
  `probe-X` 換成你各頁的 class。
- **配色**：`--green-primary:#379C39`、`--green-dark:#004B24`、`--paper-warm:#FEF4E8`。
- **logo**：內嵌 SVG `<symbol id="nl-logo">`（放 body 最前），三處用 `<use href="#nl-logo">`
  引用，靠 CSS `color` 染色，不再用 `<img>` 圖檔。
- **版型單一真相：`layouts/<name>.html`（一型一檔，雙擊就開）**。13 型：cover / chapter / hero / grid / cards / spotlight / rows / split / kpi / stats / breather / flow / thanks。要某版型的正典 markup＋CSS，直接看那一檔；改版型也改那一檔。
- 全版型一次看：`all-layouts-demo.html`（由 `build_layouts.py` 從 layouts/ 自動組裝，**勿手改**）。它也是 check_deck 的整合測試標的。

> 單位一律用 `calc(N*var(--u))`；其餘版型骨架、防雷 checklist 見下。

---

## 一、技術架構

- 單一 HTML 檔。**版型 CSS（`.probe-*` 區塊）寫在 inline `<style>` 內**，方便單檔分享
- 全域 token、`.slide` 容器骨架、共用元素（`.page-label`、`.brand-footer`、`.hi`、`.progress`）由 `base.css` 提供，HTML 開頭 `<link rel="stylesheet" href="base.css">` 引用即可（也可整段抄進 inline `<style>` 做完全獨立檔）
- `presenter.js` 處理鍵盤 / 滑鼠 / 觸控翻頁（按 `P` 切換規劃模式）
- 每一頁是一個 `<section class="slide">`，用 `.active` class 控制顯示

### 組裝合約（把多個版型組成一份 deck）

版型真相在 `layouts/`（一型一檔）。把選好的版型組成一份完整 deck 時，照這套規則（`build_layouts.py` 是它的可執行版）：

1. **一個 `<head>`**：`<link rel="stylesheet" href="base.css">`，再把用到的各版型 CSS（來自各 `layouts/<name>.html` 的 `<style>`）合併進一個 inline `<style>`；**共用的 `.ph`／`.spec` 只留一份**（依 selector 去重）。
2. **logo `<symbol id="nl-logo">` 只放一份**，擺 `<body>` 最前。
3. **各版型的 `<section>` 依序串接**進 `<div class="deck">`；**page-label 頁碼重新編號**＝該頁在 deck 的順位（`page-label__num` ≠ 順位會被 check_deck 擋）。
4. **bleed 底色 class** 放對頁（章節/呼吸頁/流程/收尾各自的 `probe-*`，base.css 的 `:has()` 規則才會補對底色）。
5. **腳本擺結尾**：`presenter.js`、`slide-audit.js`。
6. 做完跑 `check_deck.py` 求 0 FAIL。

> present 階段組裝 deck 時照同一套合約。改完任一版型，重跑 `python build_layouts.py` 再 `python check_deck.py all-layouts-demo.html`（0 FAIL）當回歸測試。
- **規劃層（合併規劃與成品）**：每頁可在 `<section class="slide">` 內加一個 `<aside class="plan-note">`（永遠隱藏，當資料來源）；按 `P` 進規劃模式，投影片維持 16:9 置頂、不被遮，規劃面板**往下展開**接在投影片下方（要往下捲才看完），內容＝該頁對應的**完整逐字原文**（也就是上台念的稿）＋一條小設計資訊。**一個檔同時是規劃稿、成品、與演講者備註**，不會像「MD 規劃＋另一個 HTML」兩邊不同步。CSS 見 base.css「規劃層」段；產出流程見 `40H_文章轉HTML簡報指南`。authoring：

  ```html
  <section class="slide" style="background:#FFFFFF;"> … 成品內容 …
    <aside class="plan-note">
      <!-- 主體：該頁對應的「完整逐字原文」。結構頁標「（結構頁，無對應段落）」 -->
      <div class="plan-note__source"><b>📄 對應原文（一字不漏）</b>今天我想來討論一個問題：許多大人過去不好的數學學習經驗就是「我好像機器人，被訓練成要背一堆公式…超無聊。」的確，例如 17 × 9：7×9=63 進6；9×1=9；9+6=15；結果等於 153。這種標準化的程序，計算機做的就好，21世紀都有 AI 了，幹嘛還要人來做、來學？</div>
      <div class="plan-note__meta"><b>說明</b>這頁造成什麼　｜　<span class="stop">⛔</span>不放什麼　｜　<b>版型</b>svg-A 直式　｜　<b>素材</b>OK</div>
    </aside>
  </section>
  ```

  > **對應原文＝完整逐字、一對一、依序、全覆蓋**：內容頁與文章是「有序分割」——把各頁 `plan-note__source` 接起來＝**一字不漏的整篇文章**，不漏字、不跳序、不重疊；一段可拆多頁、結構頁（封面/隔頁/收尾）標無對應。**原文本身就是上台念的稿，不另設講稿欄。**
  >
  > **萃取標記**：原文中「被提煉成這頁投影片重點」的句子，用 `<u class="src-key">……</u>` 標**黃色底線**——讓人一眼看見「原文哪一句 → 變成投影片上的哪句話」。投影片放精煉一句（賴以威句型：短、常用「不是A而是B／不只A更是B／A比B重要」對仗），黃底線句則是它在原文的出處。
- 16:9 比例，所有尺寸用 `vw` 單位（投影時等比縮放）
- 字型：Noto Sans TC（Google Fonts）

---

## 二、視覺規範速查

### 配色 Token

```css
:root {
  --green-primary: #0E5E3F;   /* 主色：深綠 */
  --green-dark:    #073B27;   /* 深綠底（呼吸頁用） */
  --ink:           #0A0A0A;   /* 正文純黑 */
  --hi-yellow:     #E8FF3A;   /* 螢光黃跳色 */
  --paper:         #FFFFFF;   /* 主要白底 */
  --paper-warm:    #FAF7F0;   /* 米白底（封面/收尾用） */
  --mid-gray:      #686968;   /* 副標、說明文 */
  --label-gray:    #757070;   /* 頁碼標籤 */
}
```

### 字級對照（同步 `base.css` 內 token）

新版型優先使用 token；舊版型內的硬編碼 vw 值維持不動。

| 用途 | Token | 值 | 字重 |
|------|-------|----|------|
| 封面主標 | `--fs-cover-title` | 5.2vw | 900 |
| Chapter 隔頁主標 | `--fs-chapter-title` | 5vw | 900 |
| Chapter 隔頁背景數字 | `--fs-chapter-num` | 22vw | 900 |
| 頁面主標 | `--fs-hero` | 3.2vw | 900 |
| 卡片主標 | `--fs-card-title` | 2.2vw | 900 |
| KPI 大數字 | `--fs-kpi` | 7.5vw | 900 |
| 副標 | `--fs-sub` | 1.45vw | 500 |
| 正文 | `--fs-body` | 1.55vw | 500 |
| 說明 / list item | `--fs-small` | 1.15vw | 400 |
| 大寫 Label / letter-spacing | `--fs-label` | 1.05vw | 700 |

**底線（`--fs-min`：0.9vw）。** 投影時 0.9vw 已經是極限，再小看不到。

### Highlight（螢光黃）

整份簡報**最多 3 處**。只用在最該被記住的詞，不是整句。

```css
.hi {
  background-image: linear-gradient(180deg,
    transparent 12%, var(--hi-yellow) 12%,
    var(--hi-yellow) 88%, transparent 88%);
  padding: 0 0.15em;
  box-decoration-break: clone;
  -webkit-box-decoration-break: clone;
}
```

不要用 `background-color + padding` — 多行時上下行會互蓋。

### 底色變體

| 底色 | 用途 | 寫法 |
|------|------|------|
| 白 `#FFFFFF` | 大多數內容頁 | `style="background:#FFFFFF;"` |
| 米白 `#FAF7F0` | 封面、收尾 | `style="background:#FAF7F0;"` |
| 深綠 `#073B27` | 呼吸頁（數據/轉場） | `style="background:#073B27;"` |

**重要：不要用 `slide--white` class，已知會造成頁面空白 bug。一律用 inline style 設定背景色。**

### 共用元素

每頁左上角 page-label + 右下角 brand-footer：

```html
<div class="page-label">
  <span class="page-label__num">02</span>
  <span class="page-label__bar"></span>
  <span>頁面名稱</span>
</div>
<div class="brand-footer">數感實驗室 NUMERACY LAB</div>
```

標題上方的綠色細線是視覺錨點：`border-top: 3px solid var(--green-primary); padding-top: 1.5vw;`

---

## 三、十種基礎版型骨架

每種版型提供可複製的 HTML。`<!-- 替換：XXX -->` 標記需要改的地方。

### 1. 封面（Cover）

上圖下文。圖片滿版裁切，下方左標題右副標。

```html
<section class="slide probe-cover" style="background:#FFFFFF;">
  <div class="brand-footer">數感實驗室 NUMERACY LAB</div>
  <div class="probe-cover__visual">
    <img src="<!-- 替換：主視覺圖片路徑 -->" alt="主視覺">
  </div>
  <div class="probe-cover__bottom">
    <div class="probe-cover__title">
      <!-- 替換：主標題（一行，不換行） -->
    </div>
    <div class="probe-cover__subtitle">
      <!-- 替換：副標（可用 <br> 換行） -->
    </div>
  </div>
</section>
```

關鍵 CSS：
```css
.probe-cover { padding: 0 7vw 5vw; }
.probe-cover__visual {
  flex: 1; margin: 0 -7vw; overflow: hidden;
}
.probe-cover__visual img {
  width: 100%; height: 100%; object-fit: cover;
}
.probe-cover__bottom {
  padding-top: 2.5vw;
  display: flex; justify-content: space-between; align-items: flex-end;
}
.probe-cover__title {
  font-size: 4.5vw; font-weight: 900; color: var(--ink);
  line-height: 1.2; border-top: 3px solid var(--green-primary);
  padding-top: 1.5vw;
}
.probe-cover__subtitle {
  font-size: 1.1vw; font-weight: 500; color: var(--ink);
  text-align: right; line-height: 1.8;
}
```

### 2. 全圖隔頁（Chapter Divider）

左側深綠色塊放超大半透明編號，右側 CHAPTER 標 + 主標 + 副標。用於章節分隔，比 hero 頁更安靜。

```html
<section class="slide probe-chapter" style="background:#FAF7F0;">
  <div class="probe-chapter__left">
    <div class="probe-chapter__num"><!-- 替換：01 --></div>
  </div>
  <div class="probe-chapter__right">
    <div class="brand-footer"><img src="assets/logo-horizontal.png" alt=""></div>
    <div class="probe-chapter__label">CHAPTER <!-- 替換：01 --></div>
    <div class="probe-chapter__title"><!-- 替換：公司現況 --></div>
    <div class="probe-chapter__sub"><!-- 替換：副標（可省略） --></div>
  </div>
</section>
```

關鍵 CSS：
```css
.probe-chapter { padding: 0; flex-direction: row; }
.probe-chapter__left {
  width: 38%;
  background: var(--green-primary);
  display: flex; align-items: flex-end; justify-content: flex-end;
  padding: 5vw;
  position: relative;
  overflow: hidden;
}
.probe-chapter__num {
  font-size: var(--fs-chapter-num);          /* 22vw */
  font-weight: 900;
  color: rgba(255,255,255,0.18);
  line-height: 0.82; letter-spacing: -0.04em;
  user-select: none;
}
.probe-chapter__right {
  flex: 1;
  display: flex; flex-direction: column;
  justify-content: center;
  padding: 5vw 7vw 5vw 6vw;
}
.probe-chapter__label {
  font-size: var(--fs-label);                /* 1.05vw */
  font-weight: 700; letter-spacing: 0.3em;
  color: var(--green-primary);
  margin-bottom: 1vw;
}
.probe-chapter__title {
  font-size: var(--fs-chapter-title);        /* 5vw */
  font-weight: 900; color: var(--ink);
  border-top: 3px solid var(--green-primary);
  padding-top: 1.8vw;
}
.probe-chapter__sub {
  font-size: var(--fs-sub);
  font-weight: 500; color: var(--mid-gray);
  margin-top: 1.5vw;
}
```

副標可省略；只用 label + title 視覺更穩。

### 3. Hero 宣言（Hero Statement）

一句大字 + 視覺元素 + 說明段。用於核心命題、價值主張。

```html
<section class="slide probe-hero" style="background:#FFFFFF;">
  <div class="page-label">
    <span class="page-label__num"><!-- 替換：02 --></span>
    <span class="page-label__bar"></span>
    <span><!-- 替換：核心命題 --></span>
  </div>
  <div class="brand-footer">數感實驗室 NUMERACY LAB</div>

  <div class="probe-hero__headline">
    <!-- 替換：主標題 -->
  </div>

  <div class="probe-hero__middle">
    <!-- 替換：視覺區域（圓形圖組、單張大圖、或留白） -->
    <div class="probe-hero__circles">
      <div class="probe-hero__circle"><img src="圖片路徑" alt=""></div>
      <div class="probe-hero__circle"><img src="圖片路徑" alt=""></div>
      <div class="probe-hero__circle"><img src="圖片路徑" alt=""></div>
    </div>
    <div class="probe-hero__bubble"><!-- 替換：關鍵詞標籤 --></div>
  </div>

  <div class="probe-hero__desc">
    <!-- 替換：一段說明文，<strong> 標記重點詞，<span class="hi"> 標記唯一金句 -->
  </div>
</section>
```

關鍵 CSS：
```css
.probe-hero { padding: 7vw 7vw 5vw; align-items: center; }
.probe-hero__headline {
  font-size: 3.2vw; font-weight: 900; color: var(--ink);
  border-top: 3px solid var(--green-primary); padding-top: 1.5vw;
  align-self: flex-start;
}
.probe-hero__circle { width: 18vw; height: 18vw; border-radius: 50%; overflow: hidden; }
.probe-hero__circle img { width: 100%; height: 100%; object-fit: cover; }
.probe-hero__bubble {
  font-size: 1.4vw; font-weight: 700;
  background: var(--hi-yellow); padding: 0.6vw 2vw; border-radius: 100vw;
}
.probe-hero__desc { font-size: 1.8vw; font-weight: 500; text-align: center; max-width: 75%; }
```

### 4. 多欄卡片 — 純文字（Info Grid）

標題 + N 欄卡片（2–4 欄）。用於定位、比較、流程。

```html
<section class="slide" style="background:#FFFFFF;">
  <div class="page-label">
    <span class="page-label__num"><!-- 替換 --></span>
    <span class="page-label__bar"></span>
    <span><!-- 替換 --></span>
  </div>
  <div class="brand-footer">數感實驗室 NUMERACY LAB</div>

  <div class="probe-grid__hero"><!-- 替換：頁面主標 --></div>

  <div class="probe-grid__grid">
    <!-- 重複 N 次（改 grid-template-columns 控制欄數） -->
    <div class="probe-grid__card">
      <div class="probe-grid__label"><!-- 替換：標籤 --></div>
      <div class="probe-grid__title"><!-- 替換：卡片標題 --></div>
      <div class="probe-grid__body"><!-- 替換：內容 --></div>
    </div>
  </div>
</section>
```

關鍵 CSS：
```css
.probe-grid__hero {
  font-size: 3.2vw; font-weight: 900; color: var(--ink);
  border-top: 3px solid var(--green-primary); padding-top: 1.5vw;
  margin-bottom: 4vw;
}
.probe-grid__grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 3vw; }
.probe-grid__card { border-top: 3px solid var(--green-primary); padding-top: 1.5vw; }
.probe-grid__label { font-size: 0.9vw; font-weight: 700; letter-spacing: 0.3em; color: var(--green-primary); }
.probe-grid__title { font-size: 2.2vw; font-weight: 900; color: var(--ink); }
.probe-grid__body { font-size: 1.1vw; line-height: 1.8; }
```

欄數調整：改 `grid-template-columns: repeat(N, 1fr);`

> **欄標籤分兩種，字級別搞混：**
> - **純定位標籤**（`CHAPTER 01`、`A／B／C` 這種只用來標位置的大寫小標）→ 維持小字（0.9–1.05vw）+ 大 letter-spacing。
> - **承載內容的類別標籤**（對比兩端的「事前準備／臨機應變」、多欄解法的「標準／拆解／顛倒」、方法名、品項名）→ **它就是這頁的主角**，屬「內容字」，套**內容字基準（≥ 2vw、字重 900、letter-spacing 收到 .04em）**，不能用最小的綠字。
>
> 判準：聽眾若得「先讀這個標籤才看得懂這欄在講什麼」，它就是內容、要 ≥ 2vw；若拿掉它照樣懂（只是定位，如 CHAPTER／A·B·C），才維持小字。
> 〔來源：L05 P10（compare 兩欄）、P11（three 三欄）手改；字級併入下方「內容字最小 2vw」基準〕

### 5. 多欄卡片 — 含圖（Card with Image）

跟純文字版結構類似，但每張卡片上方有裁切圖片。

```html
<section class="slide" style="background:#FFFFFF;">
  <div class="page-label">...</div>
  <div class="brand-footer">數感實驗室 NUMERACY LAB</div>

  <div class="probe-cards__hero"><!-- 替換：頁面主標 --></div>

  <div class="probe-cards__cards">
    <div class="probe-cards__card">
      <div class="probe-cards__img">
        <img src="<!-- 替換：圖片路徑 -->" alt="">
      </div>
      <div class="probe-cards__name"><!-- 替換：卡片名稱 --></div>
      <div class="probe-cards__detail">
        <strong>Hook：</strong><!-- 替換 --><br>
        <strong>互動：</strong><!-- 替換 -->
      </div>
    </div>
    <!-- 重複第二張卡片 -->
  </div>
</section>
```

關鍵 CSS：
```css
.probe-cards__cards { display: grid; grid-template-columns: 1fr 1fr; gap: 3vw; flex: 1; }
.probe-cards__img {
  border-radius: 1.5vw; height: 20vw; overflow: hidden;
}
.probe-cards__img img { width: 100%; height: 100%; object-fit: cover; }
.probe-cards__name { font-size: 1.8vw; font-weight: 900; }
.probe-cards__detail { font-size: 1.25vw; line-height: 1.8; }
```

### 6. 左文右圖（Text + Image Split）

左側文字說明 + 右側大圖。可左右互換。

```html
<section class="slide probe-split" style="background:#FFFFFF;">
  <div class="page-label">...</div>
  <div class="brand-footer">數感實驗室 NUMERACY LAB</div>

  <div class="probe-split__hero"><!-- 替換：主標 --></div>

  <div class="probe-split__grid">
    <div class="probe-split__visual">
      <img src="<!-- 替換 -->" alt="" style="width:100%;height:100%;object-fit:cover;">
    </div>
    <div class="probe-split__body">
      <div class="probe-split__desc"><!-- 替換：說明文 --></div>
      <div class="probe-split__list-label"><!-- 替換：清單標題 --></div>
      <ul class="probe-split__list">
        <li><!-- 替換：項目 --></li>
      </ul>
    </div>
  </div>
</section>
```

關鍵 CSS：
```css
.probe-split__grid { display: grid; grid-template-columns: 1.1fr 1fr; gap: 4vw; flex: 1; }
.probe-split__visual { border-radius: 1.5vw; overflow: hidden; }
.probe-split__desc { font-size: 1.3vw; line-height: 1.9; }
```

左右互換：把 `grid-template-columns` 改為 `1fr 1.1fr`，HTML 裡 visual 和 body 的 div 對調。

### 7. 大數字 / KPI（Big Numbers）

數字橫排突出，用於成果、規模。可做橫條式或圓圈式。

**橫條式（KPI）：**
```html
<section class="slide probe-kpi" style="background:#FFFFFF;">
  <div class="page-label">...</div>
  <div class="brand-footer">數感實驗室 NUMERACY LAB</div>

  <div class="probe-kpi__headline"><!-- 替換：主標 --></div>

  <div class="probe-kpi__bars">
    <div class="probe-kpi__bar">
      <div class="probe-kpi__bar-num"><!-- 替換：>70% --></div>
      <div class="probe-kpi__bar-text">
        <strong><!-- 替換：指標名 --></strong> <!-- 替換：說明 -->
      </div>
    </div>
    <!-- 重複更多 bar -->
  </div>
</section>
```

**大數字式（規模數據）：**
```html
<section class="slide probe-stats" style="background:#073B27;">
  <div class="page-label">...</div>
  <div class="brand-footer">數感實驗室 NUMERACY LAB</div>

  <div class="probe-stats__headline"><!-- 替換 --></div>

  <div class="probe-stats__row">
    <div class="probe-stats__item">
      <div class="probe-stats__num">73<span class="unit">個</span></div>
      <div class="probe-stats__label"><!-- 替換 --></div>
      <div class="probe-stats__desc"><!-- 替換 --></div>
    </div>
    <!-- 重複 -->
  </div>
</section>
```

### 8. 呼吸頁（Breather）

深色底 + 少量內容，用於節奏轉換。可以是大數字頁（版型 7 的深綠底版），也可以是一句話 + 留白。

核心概念：這頁的目的是「讓聽眾喘口氣」。不要塞太多資訊。

深綠底時，所有文字改白色，highlight 改螢光黃，page-label 也要覆寫：

```css
.probe-stats .page-label, .probe-stats .page-label__num { color: rgba(255,255,255,0.6); }
.probe-stats .page-label__num { background: rgba(255,255,255,0.2); color: #fff; }
.probe-stats .page-label__bar { background: rgba(255,255,255,0.3); }
.probe-stats .brand-footer { color: rgba(255,255,255,0.25); }
```

### 9. 收尾（Thanks / CTA）

```html
<section class="slide probe-thanks" style="background:#FAF7F0;">
  <div class="brand-footer">數感實驗室 NUMERACY LAB</div>
  <div class="probe-thanks__title"><!-- 替換：收尾大字 --></div>
  <div class="probe-thanks__body"><!-- 替換：一句說明 --></div>
  <div class="probe-thanks__meta"><!-- 替換：聯絡資訊 --></div>
</section>
```

關鍵 CSS：
```css
.probe-thanks {
  justify-content: center; align-items: center; text-align: center;
}
.probe-thanks__title { font-size: 4.5vw; font-weight: 900; color: var(--ink); }
.probe-thanks__body { font-size: 1.4vw; color: var(--mid-gray); max-width: 60%; margin-top: 2.5vw; }
```

### 10. 三節點橫排流程圖（Flow）

三個方框 + 兩段直箭頭 + 底部弧形回流線。用於概念循環、生態系、A→B→C→A 的論述。配合上方三段 caption 對應 01/02/03，視覺跟文字一一對應。

```html
<section class="slide probe-flow-page" style="background-color:#FAF7F0;">
  <div class="page-label">...</div>
  <div class="brand-footer">...</div>

  <div class="probe-flow-wrap__hero"><!-- 替換：頁面主標 --></div>

  <!-- caption 排在 SVG 上方，跟下方三框由左到右對應 -->
  <div class="probe-flow__captions">
    <div class="probe-flow__caption">
      <div class="probe-flow__caption-num">01</div>
      <div>
        <div class="probe-flow__caption-title">節點 A <span class="hi">關鍵動作</span></div>
        <div class="probe-flow__caption-desc">說明這段做什麼</div>
      </div>
    </div>
    <div class="probe-flow__caption">
      <div class="probe-flow__caption-num">02</div>
      <div>
        <div class="probe-flow__caption-title">節點 B 動作</div>
        <div class="probe-flow__caption-desc">說明</div>
      </div>
    </div>
    <div class="probe-flow__caption">
      <div class="probe-flow__caption-num">03</div>
      <div>
        <div class="probe-flow__caption-title">節點 C 動作</div>
        <div class="probe-flow__caption-desc">說明</div>
      </div>
    </div>
  </div>

  <div class="probe-flow">
    <svg class="probe-flow__svg" viewBox="0 0 1000 400" preserveAspectRatio="xMidYMid meet">
      <defs>
        <!-- marker 自動沿路徑切線旋轉箭頭，弧形末端不用手算三角形 -->
        <marker id="flow-arrow-red" viewBox="0 0 12 12" refX="11" refY="6"
                markerWidth="10" markerHeight="10" orient="auto-start-reverse">
          <path d="M 0 0 L 12 6 L 0 12 Z" fill="#BE2026" opacity="0.65"/>
        </marker>
      </defs>

      <!-- 紅色直箭頭：A → B -->
      <line x1="278" y1="125" x2="362" y2="125" stroke="#BE2026" stroke-width="4"/>
      <path d="M 362 113 L 384 125 L 362 137 Z" fill="#BE2026"/>

      <!-- 綠色直箭頭：B → C -->
      <line x1="628" y1="125" x2="712" y2="125" stroke="#0E5E3F" stroke-width="4"/>
      <path d="M 712 113 L 734 125 L 712 137 Z" fill="#0E5E3F"/>

      <!-- 虛線弧：A → C（marker 自動轉向） -->
      <path d="M 140 235 Q 500 360, 860 235"
            stroke="#BE2026" stroke-width="3"
            stroke-dasharray="11,9" fill="none" opacity="0.6"
            marker-end="url(#flow-arrow-red)"/>
    </svg>

    <!-- 三段文字標籤 -->
    <div class="probe-flow__label probe-flow__label--top">標籤 A→B</div>
    <div class="probe-flow__label probe-flow__label--diag">標籤 B→C</div>
    <div class="probe-flow__label probe-flow__label--side">標籤 A→C（虛線弧）</div>

    <!-- 三個 node -->
    <div class="probe-flow__node probe-flow__node--ntu">
      <div class="probe-flow__node-icon"><!-- SVG pictogram --></div>
      <div class="probe-flow__node-role">ROLE A</div>
      <div class="probe-flow__node-name">節點 A</div>
      <div class="probe-flow__node-desc">短描述</div>
    </div>
    <div class="probe-flow__node probe-flow__node--industry">...</div>
    <div class="probe-flow__node probe-flow__node--public">...</div>
  </div>
</section>
```

關鍵 CSS：
```css
.probe-flow-page { padding: 7vw 7vw 5vw; }
.probe-flow-wrap__hero {
  font-size: var(--fs-hero); font-weight: 900;
  border-top: 3px solid var(--green-primary); padding-top: 1.5vw;
}

.probe-flow {
  width: 92%;
  aspect-ratio: 1000 / 400;   /* SVG viewBox 同比例 */
  margin: 1.2vw auto 0;
  position: relative;
  order: 2;                   /* caption 在上方 → 用 order 排到 SVG 之下 */
}
.probe-flow__svg { position: absolute; inset: 0; width: 100%; height: 100%; z-index: 0; }
.probe-flow__node {
  position: absolute;
  width: 22%; height: 50%;
  background: var(--paper-warm);
  border-radius: var(--radius-md);
  border-top: 4px solid var(--green-primary);
  padding: 1.2vw 1.4vw;
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  gap: 0.4vw;
  z-index: 2;
  box-shadow: var(--shadow-card);
}
.probe-flow__node--ntu      { top: 6%; left: 4%; }
.probe-flow__node--industry { top: 6%; left: 39%; }
.probe-flow__node--public   { top: 6%; left: 74%; }

.probe-flow__captions {
  display: grid; grid-template-columns: repeat(3, 1fr);
  gap: 3vw;
  margin: 2vw auto 0;
  width: 95%;
  order: 1;                   /* 跟 .probe-flow 配合排在 SVG 上方 */
}
```

設計重點：
- **三節點橫排**比「兩上一下」三角形排列更直觀，caption 01/02/03 跟 left/mid/right 一對一
- 用 `flex order` 不重排 HTML，照樣讓 caption 出現在 SVG 上方
- 弧形回流線用 `<marker orient="auto-start-reverse">` 讓箭頭跟著路徑切線旋轉 — 弧度可隨意調，箭頭方向自動對齊

---

## 三之二、通用版型（資料密集型・可活用）

這幾種是給「產品比較、案例彙整、研究資料」這類圖文密集內容用的通用骨架。**命名中性、不綁特定主題**：同一個版型能套產品、方法、案例、人物、選項…只要是「圖＋結構化說明」「單一主角深入」「項目→對應」的情境都能用。完整可複製 HTML 見 `layouts/cards.html`／`layouts/spotlight.html`／`layouts/rows.html`。

**共同圖片原則**：物件／產品／文件類圖片一律放在**米白卡片（`var(--paper-warm)`）上、用 `object-fit:contain`**——完整顯示不裁切，留白也是米白、不露突兀灰底。情境照才用 `cover` 滿版。

### A. 圖文卡 grid（`.probe-cards`）
N 張並列卡片，每張 = 完整圖 + 標題（可右側加標籤／價格）+ `.spec` 結構化說明。改 `grid-template-columns` 控張數（2–4 張）。
```html
<div class="probe-cards__cards">
  <div class="probe-cards__card">
    <div class="probe-cards__img"><img src="assets/xxx.png" alt=""></div>
    <div class="probe-cards__info">
      <div class="probe-cards__name">項目名 <span class="probe-cards__tag">標籤／價格</span></div>
      <dl class="spec"><dt>類別</dt><dd>…</dd><dt>內容</dt><dd>…</dd><dt>特色</dt><dd>…</dd></dl>
    </div>
  </div>
  <!-- 重複更多卡片 -->
</div>
```

### B. 聚焦 spotlight（`.probe-spotlight`）
單一主角深入介紹：左側主圖大，右側標題＋`.spec`重點＋下方三張縮圖。用於「想把一個東西講透」。
```html
<div class="probe-spotlight__grid">
  <div class="probe-spotlight__main"><img src="assets/main.png" alt=""></div>
  <div class="probe-spotlight__side">
    <div class="probe-spotlight__name">主角名 <span class="probe-spotlight__tag">標籤</span></div>
    <dl class="spec">…</dl>
    <div class="probe-spotlight__thumbs">
      <div class="probe-spotlight__thumb"><img src="assets/t1.png" alt=""></div>
      <!-- 共三張 -->
    </div>
  </div>
</div>
```

### C. 對照列 rows（`.probe-rows`）
多列「左項目 →（箭頭）右對應」，可加分組標籤。活用：問題→對策、條件→結果、前→後、項目→說明。
```html
<div class="probe-rows">
  <div class="probe-rows__row">
    <span class="probe-rows__tag">分組</span>
    <span class="probe-rows__item">左：問題／條件／前</span>
    <span class="probe-rows__arrow">→</span>
    <span class="probe-rows__to">右：對策／結果／後（輔助說明，字較小）</span>
  </div>
  <!-- 重複更多列 -->
</div>
```

### D. `.spec` 結構化清單（元件，非版型）
`<dl class="spec"><dt>標籤</dt><dd>內容</dd>…</dl>`：左標籤（綠、不換行）右內容的兩欄定義列。可塞進上面任何版型，把「材質／內容物／特色／規格」排得整齊。

---

## 四、進階版面技巧（實戰 Pattern）

這幾招都是修 bug 修出來的，非顯而易見但解決常見痛點。

> **延伸**：要做 PowerPoint 風格的結構圖（房間+門+人、計算分解、多條件對比、流程節點等向量圖示），看 `svg-patterns.md`。要找/抓配圖，看 `image-sourcing.md`。

### Pattern 1：Subgrid 對齊多欄 baseline

**場景**：KPI 頁有 3 個欄，各包含「大數字 / 標籤 / 說明」。如果某欄說明文字較長，會把那欄的「大數字」往上推，三個大數字 baseline 對不齊。

**症狀**：每個欄各自垂直居中 → 內容多寡不同 → 大數字位置高低不一。

**修法**：用 CSS Subgrid 讓三欄共用 parent 的 row baseline。

```css
.probe-stats__row {
  display: grid;
  grid-template-columns: 1.3fr 1fr 1.4fr;
  grid-template-rows: auto auto auto;   /* num / label / desc */
  gap: 0.7vw 3vw;
  align-content: center;                /* 三 row 整組在 slide 內居中 */
}
.probe-stats__item {
  display: grid;
  grid-template-rows: subgrid;          /* 共用 parent 的 row */
  grid-row: span 3;
}
.probe-stats__num { align-self: end; }  /* 大數字對齊 row 1 底部 → 三欄 baseline 統一 */
```

不論哪欄 desc 多長都不會把 num 推開。Chrome 117+ / Safari 16+ 已支援，可直接用。

### Pattern 2：SVG `<marker>` 弧形箭頭自動轉向

**場景**：流程圖底部要畫一條弧形虛線從 A 繞到 C，弧線末端切線是斜的，手算箭頭三角形角度很麻煩，做出來方向還常常不對。

**修法**：用 SVG `<marker orient="auto-start-reverse">`，瀏覽器自動沿路徑切線旋轉箭頭。

```html
<svg viewBox="0 0 1000 400">
  <defs>
    <marker id="arrow" viewBox="0 0 12 12" refX="11" refY="6"
            markerWidth="10" markerHeight="10" orient="auto-start-reverse">
      <path d="M 0 0 L 12 6 L 0 12 Z" fill="#BE2026"/>
    </marker>
  </defs>
  <path d="M 140 235 Q 500 360, 860 235"
        stroke="#BE2026" stroke-width="3"
        fill="none" marker-end="url(#arrow)"/>
</svg>
```

- `orient="auto"` 跟著正向切線
- `orient="auto-start-reverse"` 比較通用 — 如果改成 `marker-start`，三角形會自動反向，不用重畫
- `refX/refY` 是 marker 的「錨點」，調這兩個值控制箭頭尖端剛好落在路徑端點

### Pattern 3：半透明卡片在背景圖上

**場景**：頁面有滿版背景照片（校門、團隊照、場景圖），上面要放卡片或文字塊。卡片如果用純白底會「擋掉照片」，全透明又難讀。

**修法**：半透明白底 + `backdrop-filter` 微模糊。

```css
.card-on-photo {
  background: rgba(255, 255, 255, 0.88);
  backdrop-filter: blur(2px);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-elevated);
}
```

- `0.88` 是甜蜜點：紋理透出但字仍清楚。深底用 `0.82–0.85`，淺底用 `0.88–0.92`
- `blur(2px)` 讓卡片下方的背景柔化，避免複雜紋理跟卡片邊界打架
- 配合 `linear-gradient(rgba(...) 0%, rgba(...) 100%), url(...)` 給整頁加一層 vertical overlay，控制照片上明下暗，照片頂部展示主體（如校門匾額），卡片區域更暗讓字更穩

範例（P18 校門合作提案頁）：
```css
.probe-ask {
  background-color: #FAF7F0;
  background-image: linear-gradient(
    to bottom,
    rgba(250,247,240,0.72) 0%,
    rgba(250,247,240,0.85) 50%,
    rgba(250,247,240,0.93) 100%
  ), url('assets/nthu_gate.jpg');
  background-size: cover;
  background-position: center 30%;
}
```

### Pattern 4：直幅／文件圖貼合框（框寬 auto，免 letterbox）

**場景**：左文右圖（split）放的是**直幅照片或整張文件**（手寫計算紙、講義、直拍照），而圖框是橫的。`object-fit:contain` 會在左右補空白（letterbox），`cover` 又會裁掉內容——文件要看「整張」不能裁。

**修法**：不要固定圖框長寬，讓**框寬 `auto`、圖以高度撐滿**，框就會緊貼圖、零空白。

```css
/* grid 讓圖欄收成內容寬 */
.split { display: grid; grid-template-columns: 1.2fr auto; align-items: center; }
.split__visual { background: transparent; overflow: visible; }
.split__visual img {
  height: 40vw;          /* 用高度撐滿（接近版面可用高）*/
  width: auto;           /* 寬度跟著長寬比 → 框＝圖，無 letterbox */
  max-width: 100%;
  object-fit: contain;
  display: block;
}
```

- 想再放大：把 `height` 推到接近「内容區高 − page-hero」的上限；或把 page-hero 收進左欄、讓圖佔滿整頁高。
- 要在圖上加圈註（標出某段內容）：外層 `position:relative`，圈用 `position:absolute` 的 `%` 定位（隨圖縮放自動跟著走）。
- 一般情境/氛圍 AI 圖仍走「滿版版型」（`probe-fb`，整頁 16:9 背景）；本 pattern 只給「要看整張」的直幅文件/照片。
- 〔來源：L05 S22 手寫計算紙〕

---

## 五、防雷 Checklist

產出或修改簡報時，逐條檢查：

### [全局] 結構與技術

- [ ] 每個 `<section>` 都有 `class="slide"` + `style="background:#色碼;"`，不要用 `slide--white` class
- [ ] 圖片容器要設固定高度或用 `flex: 1` 填滿（否則會塌成 0 高度）
- [ ] CSS 寫在 `<style>` 裡，不要外連（方便單檔分享）
- [ ] 不要用 `slide--white`、`slide--beige` 等 class 設定背景（已知 bug）
- [ ] assets 內檔名一律英文 kebab-case，禁中文、禁空格（URL 編碼會出意外）

### [全局] 字級與排版

- [ ] **投影片正文（觀眾要讀的句子）≥ `--fs-content-min`（2vw）**——演講實測底線，比這小投影看起來就太小。內容字＝主標／副標／卡片標題與標籤／清單項／說明句／計算式／條件名等「要讀來理解」的文字，一律 ≥ 2vw。只有**定位用微標註**可低於：頁碼、圖片與論文出處（cite）、規劃層、封面日期小字、Hero kicker（eyebrow，如 CORE CLAIM）、STEP／直式步驟序號、直式中的進位數字。判準：拿掉它仍看得懂＝可小；要讀它才懂＝內容、≥ 2vw
- [ ] **欄/卡片的「類別標籤」若承載內容（方法名、對比端點）＝內容字，套 ≥ 2vw/900**——它是這欄的主角，不可用 0.9vw 微標。只有純定位用的大寫小標（CHAPTER、A/B/C、STEP 序號）才維持小字
- [ ] 同階層標題字級一致（同為 `--fs-hero` / 同為卡片標題），不要某頁突然變大或變小
- [ ] 一頁不要超過兩種字重（通常 900 + 500）
- [ ] **整段中文不要設 `white-space: nowrap`**，長句會撞出邊界。要鎖 2–4 字詞組防止「最後一字落單」時，用 `.nowrap` / `.no-orphan` class 包該詞組即可
- [ ] 落單字檢查：每頁瀏覽一遍，desc / body 結尾若出現「最後一行只剩 1 字」就要處理（精簡文字 / `<br>` 強制斷行 / `.nowrap` 鎖詞）。`text-wrap: pretty` 已自動修一部分但不保證

### [改版面時] 佈局

- [ ] **圖框不要有灰/白 letterbox**（圖長寬 ≠ 框長寬時補的空白）。三種處理：
  - **照片放 split 圖框** → `object-fit: cover` 填滿（可接受輕微裁切），框底色設白
  - **情境/氛圍/AI 插畫** → 用「滿版版型」：整頁 16:9 背景圖 `cover` 鋪滿＋深色漸層＋標題壓字；AI 圖**直接以 16:9（1536×1024）生成**，不要用方圖（1024²）塞長框
  - **圖表/含字/需看清全圖** → 用 `contain`，並把**圖框做成該圖的長寬比**（讓 contain 也不留邊）
- [ ] 圖片容器必須 `min-height: 0`（在 flex/grid 子元素中），否則上方文字會把圖擠到看不完整
- [ ] 封面的圖文配置用「上圖下文」，不要左右切（不自然）
- [ ] 圓形圖片（`border-radius: 50%`）要夠大（至少 18vw），太小提案時講不到內容
- [ ] 多欄 grid 超過 4 欄會太擠，考慮分上下排
- [ ] flex 容器裡的元素如果沒有內容，要給 `min-height` 防止塌陷
- [ ] icon / 裝飾圖不要跟文字擠在同一行，用 `position: absolute` 浮動到卡片角落

### [內容塞不下時] 三階策略

爆框（內容超出 `.slide-frame`）時**依序**處理，不要直接跳到縮字：

1. **砍字（首選，也是紀律）**：放不下＝內容太多。精簡文字、拆頁，維持 ≥2vw 可讀。`check_deck.py --measure` 會抓爆框逼你面對。
2. **`autocol.js` — 長清單自動分欄**：清單型內容用掉橫向空白、**字級不變、可讀性保住**。容器加 `data-autocol="4"`（上限欄數），HTML 末載入 `<script src="../autocol.js"></script>`；1 欄塞不下就自動加到 2、3… 欄。
3. **`autofit.js` — 內容縮放塞框（最後手段，不鼓勵）**：把 `.slide-frame` 內容 `transform:scale(<1)` 縮到塞得下。⚠️ **會讓字級低於 2vw 可讀底線**——只在「真的不能砍、又必須一頁呈現」時當安全網，**不可當塞太多的藉口**。載入 `<script src="../autofit.js"></script>`（放 presenter.js 之後；與 autocol 並用時 autocol 先跑）。

> 一句話：**能砍就砍 → 清單就分欄（autocol）→ 真的沒辦法才縮（autofit）**。autocol 保可讀、autofit 犧牲可讀。兩者皆選配；不載入則維持「偵測＋砍字」紀律。

### [寫文案時] AI 痕跡檢查

- [ ] 「從 X 到 Y」整份最多用一次
- [ ] 沒有「翻轉」「重新定義」「情緒旅程」等抽象動詞
- [ ] 沒有破折號 + 三段排比（GPT 招牌句型）
- [ ] 驚嘆號整份 ≤ 5 個
- [ ] 「讓⋯⋯」開頭句 ≤ 2 次
- [ ] 結尾句不要用英文語法的中文（如「讓它變成好的」）
- [ ] 金句整份最多 3 個（封面、命題、結尾各一）
- [ ] 命題 vs 手段分清楚——命題是觀察（「每個人都有數學記憶」），手段是做法（「把記憶變好玩」）

---

## 六、presenter.js 使用說明

把以下 script 放在 `</body>` 前：

```html
<script>
// 完整內容見 presenter.js
// 功能：← → 翻頁、空白鍵下一頁、Home/End 首尾頁
// 點擊左 1/3 上一頁、右 2/3 下一頁
// 支援觸控滑動
// 左下角自動顯示「N / 總數」（避開右下 brand-footer）
// P＝規劃模式（下方展開對應原文）
// O＝總覽模式（全頁縮圖格狀、點擊跳頁、Esc 關）
</script>
```

如果要從特定頁開始，URL 加 `#頁碼`（如 `index.html#5`）。

### 選配腳本（內容自適應，與「偵測爆框」互補）

放在 `presenter.js` 之後、`</body>` 前，**按需載入**：

- `<script src="../autocol.js"></script>`：長清單自動分欄（保字級）。容器標 `data-autocol="N"`。
- `<script src="../autofit.js"></script>`：內容縮放塞框的最後手段（可能 <2vw，不鼓勵）。

策略順序與取捨見 §五「[內容塞不下時] 三階策略」。不載入則維持「偵測＋砍字」的預設紀律。
