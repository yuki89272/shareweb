# SVG / Shape 結構圖庫 — AI Context 文件

> 本文件補強 `slide-system.md` 第三節「十種基礎版型」之外的「結構圖元件」。
> 用途：當你要表達**過程、比對、流程、結構關係**時，純文字或單張圖都不夠——
> 需要用 SVG 或純 CSS shape 拼出可編輯的向量圖示。

PowerPoint 用 AUTO_SHAPE/GROUP 拼出來的那種乾淨向量圖（如房間+門+人、流程節點+箭頭、條件對比圖），HTML 也可以做，且更好維護（可改文字、可改色、可重排）。

---

## 收錄原則

收進這個庫的 pattern 必須：
1. **重用機率 ≥ 3 次**（演講、課程、簡報跨主題會用到）
2. **純 HTML/CSS 或行內 SVG**（不依賴外部圖片）
3. **可改色、可改文字、可調大小**（用 vw + CSS variable）
4. **附完整可貼上的 HTML + CSS 樣板**

---

## Pattern A：直式乘法 grid（計算分解）

**用途**：示範一道計算題的步驟拆解。常用於講「執行多步驟有多累」、「自動化能省多少力」。

**視覺**：
- 4 欄 grid（千/百/十/個），上下對齊
- 上方紅字 = 進位（superscript）
- 中間是被乘數、乘號、乘數
- 下方綠色橫線
- 結果用主色

```
       6
     1 7
   ×   9
   ─────
   1 5 3
```

**HTML**：

```html
<div class="probe-vmul">
  <span></span><span></span>
  <span class="probe-vmul__carry">6</span>
  <span></span>

  <span></span><span></span>
  <span>1</span><span>7</span>

  <span class="probe-vmul__op">×</span>
  <span></span><span></span>
  <span>9</span>

  <div class="probe-vmul__rule"></div>

  <span></span>
  <span class="probe-vmul__result">1</span>
  <span class="probe-vmul__result">5</span>
  <span class="probe-vmul__result">3</span>
</div>
```

**CSS**：

```css
.probe-vmul {
  display: inline-grid;
  grid-template-columns: 1fr 1fr 1fr 1fr;
  font-family: 'Noto Sans TC', 'Courier New', monospace;
  font-weight: 900;
  font-size: 4.5vw;
  line-height: 1.15;
  text-align: center;
  letter-spacing: 0.02em;
  font-feature-settings: 'tnum';
}
.probe-vmul > span { padding: 0 0.3vw; }
.probe-vmul__carry {
  font-size: 1.6vw;
  color: #BE2026;
  align-self: end;
  padding-bottom: 0.4vw;
}
.probe-vmul__op { color: var(--green-primary); }
.probe-vmul__rule {
  grid-column: 1 / -1;
  border-top: 0.25vw solid var(--ink);
  margin: 0.4vw 0;
}
.probe-vmul__result { color: var(--green-primary); }
```

**擴充**：兩位數 × 兩位數時，需 partial product 兩列；加 column 數即可。

---

## Pattern B：多條件對比圖（房間+門+移動 + 右側長條）

**用途**：展示 N 個實驗條件、N 個方案優劣對比。**長條圖讓量級差異一眼可見**——光看數字「11%/14%/16%/20%」缺乏衝擊，加上等比例長條後「20% 幾乎是 11% 兩倍」立刻有感。

**視覺**：每行一個條件，3 欄 grid
- 左 11vw：條件標籤（左側色邊）
- 中 flex：房間圖示（圓角矩形 + 字母/圓點 + 箭頭/門）
- 右 16vw：錯誤率數字 + 等比長條

**配色梯度**：條件越糟，色越熱
- A 主綠 `#0E5E3F` → B 橘 `#E89A3F` → C 紅 `#BE2026` → D 暗紅 `#8B1A1A`

用 `style="--c:#XXX;"` 在每 row 設定本行主色，內部所有元素都用 `var(--c)`。

**HTML（4 條件完整範例）**：

```html
<div class="probe-conditions">

  <!-- A：同房間 -->
  <div class="probe-conditions__row" style="--c:#0E5E3F;">
    <div class="probe-conditions__label">條件 A<span>同房間移動</span></div>
    <div class="probe-conditions__viz">
      <div class="probe-room probe-room--wide">
        <div class="probe-letter">起 ●</div>
        <div class="probe-arrow-h">─ ─ ─ →</div>
        <div class="probe-letter">● 終</div>
      </div>
    </div>
    <div class="probe-conditions__stat">
      <div>
        <div class="probe-conditions__pct-label">錯誤率</div>
        <div class="probe-conditions__pct">11%</div>
      </div>
      <div class="probe-conditions__bar-wrap">
        <div class="probe-conditions__bar" style="width:55%;"></div>
      </div>
    </div>
  </div>

  <!-- B：穿 1 道門 -->
  <div class="probe-conditions__row" style="--c:#E89A3F;">
    <div class="probe-conditions__label">條件 B<span>穿過一道門</span></div>
    <div class="probe-conditions__viz">
      <div class="probe-room probe-room--flex"><div class="probe-letter">A ●</div></div>
      <div class="probe-door-mini"><div>門</div><div>→</div></div>
      <div class="probe-room probe-room--flex"><div class="probe-letter">B ●</div></div>
    </div>
    <div class="probe-conditions__stat">
      <div>
        <div class="probe-conditions__pct-label">錯誤率</div>
        <div class="probe-conditions__pct">14%</div>
      </div>
      <div class="probe-conditions__bar-wrap">
        <div class="probe-conditions__bar" style="width:70%;"></div>
      </div>
    </div>
  </div>

  <!-- C：回到原房間（雙向箭頭） -->
  <div class="probe-conditions__row" style="--c:#BE2026;">
    <div class="probe-conditions__label">條件 C<span>回到原房間</span></div>
    <div class="probe-conditions__viz">
      <div class="probe-room probe-room--flex">
        <div class="probe-letter probe-letter--with-sub">A<small>起→回</small></div>
      </div>
      <div class="probe-arrows-stack"><div>→</div><div>←</div></div>
      <div class="probe-room probe-room--flex"><div class="probe-letter">B</div></div>
    </div>
    <div class="probe-conditions__stat">
      <div>
        <div class="probe-conditions__pct-label">錯誤率</div>
        <div class="probe-conditions__pct">16%</div>
      </div>
      <div class="probe-conditions__bar-wrap">
        <div class="probe-conditions__bar" style="width:80%;"></div>
      </div>
    </div>
  </div>

  <!-- D：連續換兩房 -->
  <div class="probe-conditions__row" style="--c:#8B1A1A;">
    <div class="probe-conditions__label">條件 D<span>連續換兩個房間</span></div>
    <div class="probe-conditions__viz">
      <div class="probe-room probe-room--flex"><div class="probe-letter">A</div></div>
      <div class="probe-arrow-h">→</div>
      <div class="probe-room probe-room--flex"><div class="probe-letter">B</div></div>
      <div class="probe-arrow-h">→</div>
      <div class="probe-room probe-room--flex"><div class="probe-letter">C</div></div>
    </div>
    <div class="probe-conditions__stat">
      <div>
        <div class="probe-conditions__pct-label">錯誤率</div>
        <div class="probe-conditions__pct">20%</div>
      </div>
      <div class="probe-conditions__bar-wrap">
        <div class="probe-conditions__bar" style="width:100%;"></div>
      </div>
    </div>
  </div>

</div>
```

**CSS**：

```css
.probe-conditions {
  flex: 1; display: flex; flex-direction: column;
  gap: 1.2vw; min-height: 0;
}
.probe-conditions__row {
  display: grid;
  grid-template-columns: 11vw 1fr 16vw;
  gap: 2vw; align-items: center;
}
.probe-conditions__label {
  font-size: 1.2vw; font-weight: 700; line-height: 1.4;
  border-left: 4px solid var(--c); padding-left: 1vw;
  color: var(--c);
}
.probe-conditions__label span {
  display: block; font-size: 0.95vw; font-weight: 500; color: var(--c);
  margin-top: 0.2vw;
}
.probe-conditions__viz { display: flex; align-items: center; gap: 0.6vw; }
.probe-room {
  height: 4.8vw; background: #F4F4F2;
  border-top: 4px solid var(--c); border-radius: 0.6vw;
  display: flex; align-items: center; justify-content: center;
  gap: 0.7vw; padding: 0 1vw; min-width: 4vw;
}
.probe-room--flex { flex: 1; }
.probe-room--wide { flex: 1; min-width: 24vw; }
.probe-letter { font-size: 1.4vw; font-weight: 900; color: var(--c); }
.probe-letter--with-sub { display: flex; flex-direction: column; align-items: center; gap: 0.1vw; }
.probe-letter--with-sub small { font-size: 0.75vw; font-weight: 500; }
.probe-arrow-h {
  font-size: 1.4vw; color: var(--c);
  font-weight: 900; letter-spacing: 0.05em;
}
.probe-arrows-stack {
  display: flex; flex-direction: column;
  font-size: 1.2vw; color: var(--c); font-weight: 900;
  align-items: center; gap: 0.3vw;
}
.probe-door-mini {
  display: flex; flex-direction: column; align-items: center;
  font-size: 0.8vw; color: var(--c); padding: 0 0.3vw;
}
.probe-door-mini div:first-child { font-size: 0.95vw; font-weight: 700; }
.probe-conditions__stat { display: flex; align-items: center; gap: 0.8vw; }
.probe-conditions__pct-label {
  font-size: 0.75vw; font-weight: 700; color: var(--c);
  letter-spacing: 0.2em; margin-bottom: 0.2vw;
}
.probe-conditions__pct {
  font-size: 2.3vw; font-weight: 900; color: var(--c);
  font-feature-settings: 'tnum'; flex: 0 0 4.8vw; line-height: 1;
}
.probe-conditions__bar-wrap { flex: 1; }
.probe-conditions__bar { height: 1.3vw; background: var(--c); border-radius: 0.2vw; }
```

**長條寬度計算**：以最大值為 100%，其他按比例。
- 例：max = 20%，則 11→55%、14→70%、16→80%、20→100%
- 一律 `width: NN%;` inline style 即可

**簡化變體**：
- 不要長條：刪掉 `.probe-conditions__bar-wrap`，3 欄改 2 欄（label / viz / pct）
- 只兩個條件：grid `grid-template-columns: 12vw 1fr 16vw` 維持，行數減
- 房間內顯示其他內容：把 `.probe-letter` 換成任何子元素

**對應 PPT 出處**：L05 PowerPoint S17（門口效應 4 條件示意圖）。
**已在 L05 HTML v1 套用**：P21（穿過幾扇門，記憶就掉多少）。

---

## Pattern C：鋸齒切換流程（1A2B 任務示意）

**待新增**。視覺：上下兩條軌道 + Z 字型連線 + 節點數字/字母交錯。
對應 PPT 出處：L05 S15（1A2B 切換成本實驗）。
未做完前可暫時用「三欄對比卡」（slide-system.md 版型 4 加 alert 色）替代。

---

## Pattern D：4 道門 + 紙條墜落（穿門掉記憶）

**已實作（L05 P29，深綠底版）**。視覺：一排 4 個白線門框（圓角矩形＋內框＋黃點門把、上方 ①–④ 編號），門與門的間隙各 2 張小紙條（圓角小矩形、旋轉 ±12–26°、黃 #E8FF3A 與米白交錯、內畫兩條短橫線當字跡）＋向下的點狀虛線墜落軌跡（q 曲線、rgba 黃 .45）。
技法：單一 inline SVG（viewBox 1000×268），door()/slip() 兩個生成函式各帶位置參數。深底用白描邊＋低透明度填色；淺底版改 --green-primary 描邊即可。
是 Pattern F（編號流程版型）的「損耗」變體。

---

## Pattern E：多解法對比卡（5+18 三種看法）

**用途**：同一道題的不同解法，並列比較流程。

**視覺**：3 欄綠色頂線卡片
- 上：解法名稱（標籤）
- 中：解法標題
- 下：步驟列表 + 結果

實作見 `slide-system.md` 版型 4「多欄卡片 — 純文字」，配色用 `--green-primary`。本 pattern 是版型 4 的特化用法，不另寫 HTML。

---

## Pattern F：編號流程版型（步驟／階段序列）

**用途**：有序步驟、階段、流程（Polya 四步、實驗 N 步、解題階段）。
**視覺**：一排圓角方塊（編號①②…＋圖示＋標籤），方塊間 `→`；「關鍵步驟」用實心綠變體、「常被跳過/出錯」步驟用螢光黃；下方一條虛線弧箭頭表「跳關」，再配 1–2 條 takeaway 色帶總結。
**關鍵技法**：方塊用 flex row + `justify-content:center`，加 `--key`(綠)/`--jump`(黃) 變體。跳關虛線弧用**獨立 SVG、viewBox 比例＝顯示比例**＋ `<marker orient="auto-start-reverse">`。
**坑**：跳關 SVG 用 `preserveAspectRatio="none"` 撐滿寬會把箭頭三角拉歪——**一定等比＋marker**。
**出處**：L05 S27（完整碼 `.p27diag`）。Pattern D（門+紙條）是它的「掉記憶」變體。

---

## Pattern G：前後對照空間圖（隔間 → 打通）

**用途**：部分→整體、隔閡消失（小房間打通成大廳、切換成本消失）。
**視覺**：左＝N 個被牆隔開的格子＋之字虛線路徑逐格穿門（門標①②③）＋「每道門＝一次成本」；中＝螢光黃「打通」箭頭；右＝同範圍變一個大框、一條直線箭頭暢通穿過。
**關鍵技法**：CSS grid/絕對定位畫格子即可，不需複雜 SVG；之字路徑一條 `<path>` dasharray。
**出處**：L05 S29（`.pP29diag`）。

---

## Pattern H：拆位匯流（位值規律）

**用途**：兩位數×11、拆位規律（某位＝兩數和）。
**視覺**：左＝來源數字框（十位/個位）；中＝SVG 連線（兩數各落到對應位，另兩條斜線匯流到中間位、黃圈標「＋」）；右＝結果三格（中間位黃底「＝它們的和」）；下方同構小例證（35×11→3 (3+5) 5＝385）。
**出處**：L05 S32（`.pP32diag`）。是 Pattern E 的「規律可視化」延伸。

---

## Pattern I：階梯方塊＋差值橋（數列規律）

**用途**：數列相鄰差規律（平方差＝兩底數和、等差）。
**視覺**：一排數值方塊；相鄰塊間向上小弧（橋），橋上黃 chip 標差（+21）、橋下小字拆解（21=10+11）；下方獨立公式帶；旁邊遞增小長條輔助「每次多 2」；可接「觀察→猜想→驗證」三節點。
**關鍵技法**：橋＝cubic `<path>` + marker；方塊等距。
**坑**：差值的分解式（10+11）**不要放在橋弧下方**——會和弧線/箭頭重疊。把它併進橋上的黃色 chip（兩行：上「+21」、下「10+11」），chip 不透明、壓在弧頂，乾淨。
**出處**：L05 S39（`.pP37diag`）。

---

## Pattern J：容量堆疊容器（部分-整體、此消彼長）

**用途**：固定總量被幾種成分瓜分、彼此擠壓（工作記憶＝內在＋外在＋增生負荷）。
**視覺**：代表「上限」的方框容器，內部堆疊長條切成數段（各一色）；「該消除」的段加刪除斜線＋叉；旁邊放兩個對照容器（成分大→另一段被擠掉 vs 消除後→有空間）。
**關鍵技法**：純 SVG `<rect>` 堆疊；色用 灰(中性)/紅(該消除 #C8302B)/綠(要保留)。
**出處**：L05 S42（`.pP42diag`）。

---

## Pattern K：頭尾配對弧（配對求和）

**用途**：配對結構（高斯 1+100、首尾相加都相等）。
**視覺**：水平數線，左端 1,2,3… 右端 …98,99,100；半圓 `<path>` 弧連 1↔100、2↔99…、弧上標和；中段「…」省略、標「第 N 組」；下方「N 組 × 和 ＝ 總」＋黃底答案。
**關鍵技法**：弧＝`A`(arc) 或 cubic；端點放小圓點。
**出處**：L05 S44（`.pP44diag`）。

---

## Pattern L：斜投影立體（擠出剖面，如 U 形溝渠）★最值得重用

**用途**：立體幾何題（U 形溝渠、L 形、中空柱）——前面剖面、往深度擠出，比平面圖好懂。
**關鍵技法（cabinet 斜投影）**：
- 前面照實畫剖面多邊形（座標好算）；深度方向＝每個頂點加固定位移 `dz=(+dx,−dy)`（往右上）得「後面」頂點。
- 可見面＝前後對應頂點組成的四邊形：頂面、側面、（透過缺口看到的）凹槽內壁與槽底。
- **畫的順序（painter's algorithm）**：先畫後方/頂部/內壁/槽底，**最後畫前剖面**（前剖面是凹的 U 多邊形、缺口不填→透出後方槽內）。
- 同綠色系不同明度區分面（頂亮/側中/槽底暗），統一 `stroke:#0E5E3F`。
**坑**：尺寸標籤放形體外緣、別和面內字疊；直書標籤離形體遠一點。
**出處**：L05 S31（完整頂點/面在該頁 SVG）。

---

## Pattern M：框算式（標出子值來源）

**用途**：一條完整算式，標出「停在哪/漏了哪會得到哪個錯答案」。
**視覺**：完整算式當主角（大字），**巢狀色框**框住子段：內框＝某中間值、外框（虛線、另一色）＝含更多項的值；「容易漏的項」用第三色標「漏掉→X」；正解黃底；下方配色圖例（哪框＝哪值＋為何錯）。
**關鍵技法**：inline-block 巢狀 `<span>` 加 border（依內容自動撐大、免算座標）；框上數字標籤用 `::before` 絕對定位＋白底遮線，避免壓到外框虛線。
**出處**：L05 S18（`.box447/.box397/.minus50`）。

---

## Pattern N：多線軌跡圖（論文折線圖）

**用途**：論文數據、跨時間多條軌跡（成長斜率、黃金交叉）。
**視覺**：座標軸＋格線＋N 條 `<polyline>`；交叉點黃色 highlight 圓＋標籤；legend 框列各線（色塊＋名稱＋數值）。
**關鍵技法**：
- 在 **Python 算好各點像素座標**（`y=top+(max−v)/range*H`）再吐 polyline，免手算。
- **Y 軸標題直書**（每字一個 `<tspan x=固定 dy=行距>`），不要 `rotate`（旋轉中文不好讀）。
- 圖內字級可 <2vw（圖表附屬標註是正文 2vw 底線的例外），但要塞得進 legend 框。
**坑**：圖「太扁」→ viewBox 改高、字改小；legend 超框 → 縮短標籤＋加寬框。
**出處**：L05 S43（`.p43chart`）。

---

## 何時新增 Pattern

當你做完一份簡報，發現有結構圖**重用機率 ≥ 3 次**，就抽出到這裡。寫法：

1. 取一個 `probe-xxx` class 命名
2. 列「用途」、「視覺」描述
3. 貼可複製 HTML + CSS
4. 標明對應 PPT/原始來源（如「對應 L05 S17」）

未實作的 pattern 也可以先列「待新增」+ 出處，避免之後重做時找不到。
