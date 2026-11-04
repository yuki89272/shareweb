# deck-kit_NUMiNAI

NUMiNAI（數學 AI 精靈）專用的 HTML 簡報工具。
和隔壁 `deck-kit_數感實驗室`（數感實驗室綠）**版型完全相同、只換品牌層**：
同一套 `.slide` / `.slide-frame` / 版型 class / `check_deck.py` / `shot.sh`，
換掉的是 `:root` 的色票 token、字型，以及 `assets/` 的 logo 與吉祥物。

> 做 NUMiNAI 的簡報用這一份；做數感實驗室的簡報用 `deck-kit_數感實驗室`。
> 兩份的 `base.css` 是各自獨立的檔案，改一邊不會動到另一邊。

> **版型文件（`slide-system.md`／`content-style.md`／`template-spec.md`／`layouts/`／`svg-patterns.md`…）
> 與 `deck-kit_數感實驗室` 同源、內容相同**，這裡放的是副本，方便整包複製就能用。
> 要改版型規則請**兩份一起改**，不然會漂走。`all-layouts-demo.html` 打開會直接吃這裡的 `base.css`，
> 所以看到的是 NUMiNAI 配色。

---

## 一、色彩系統

資料來源：`Numina數學AI精靈 Brand Guideline`（顏色/主色 p10-11、輔助色 p12）＋ `Color Palette.pdf`。
兩份是**不同的東西**，別混用：

| | 是什麼 | 用在哪 |
|---|---|---|
| **Brand 主色**（Guideline p10 綠松、p11 藍） | Pantone 指定的品牌核心色。**logo 和吉祥物就是畫在這一組上** | 品牌識別、強調、圖表主色 |
| **Color Palette · Major** | 同一個色相家族，但**是另一組值**——一條降飽和的 9 階 UI 階梯 | 介面底色、卡片、大面積淡色 |

實際量過的差異（把兩份 PDF 都轉點陣取樣，並用已標示 hex 的 p10 反驗過管線準確）：

| | 主色 | Major 最接近的一階 |
|---|---|---|
| PANTONE 325c `#82D3C6`（品牌核心） | — | 落在 Major 500 `#95D1C6` 與 600 `#70C3B3` **之間**，不是階梯上的任何一階 |
| PANTONE 304c `#C0E9E2` | — | Major 300 `#BEE8E1`　**幾乎相同** |
| PANTONE 2397c `#0AACA3` | — | Major 700 `#4EA9A2`　R 差 68，主色鮮豔得多 |
| PANTONE 7712c `#097881` | — | Major 900 `#3B817C`　同上 |

**結論**：只有 304c 對得上。所以本 kit 的作法是
**品牌核心用主色、UI 階梯用 Major**，兩者並存不互相取代。

### token 一覽（`base.css` `:root`）

```
品牌主色（綠松）  --brand-teal-950 #06565C ← 7712c 的加深階，只給滿版深底
                --brand-teal-900 #097881   PANTONE 7712c
                --brand-teal-700 #0AACA3   PANTONE 2397c
                --brand-teal-500 #82D3C6   PANTONE 325c ← logo／吉祥物
                --brand-teal-300 #C0E9E2   PANTONE 304c
                --brand-teal-100 #ECF8F6   PANTONE 7457c
品牌副主色（藍）  --brand-blue-700 #0093B8 / -500 #00B1E0 / -300 #6DE2F3 / -100 #D9FFFF
UI 階梯          --major-100…900、--vermilion-*、--yellow-*、--indigo-*、--gray-100…1000
品牌輔助色        --acc-yellow #F3E43B、--acc-red #E83E48、--acc-orange #FF9600、--acc-blue #2B70C9
```

### 語意層（版型只認這幾個，換色只要改這裡）

```
--green-primary : brand-teal-900 #097881   規線／小標／章節底／logo
--green-dark    : brand-teal-950 #06565C   滿版深底頁
--paper-warm    : brand-teal-100 #ECF8F6   卡片與淡底
--ink           : gray-1000     #1E1E1E
--mid-gray      : gray-600      #636363
--alert         : acc-red       #E83E48
--hi-yellow     : acc-yellow    #F3E43B
```

> **為什麼 `--green-primary` 不是最漂亮的 `#0AACA3`？**
> 因為它同時當「白底上的小標文字」與「白字膠囊的底色」用。
> `#0AACA3` 對白只有約 2.6:1，小字會糊；`#097881` 約 4.9:1，過得了 AA。
> 想要亮一點的青綠當**填色**（長條、色塊）時直接用 `--brand-teal-700`。

---

## 二、字型

`Chiron GoRound TC`（Brand Guideline · Typography 指定），Google Fonts 有，直接 `@import`，
權重 200–900 全供應。後備 `Noto Sans TC`。

字級階梯（Typography.pdf）：Display 38 / H1 30 / H2 26 / H3 24 / H4 22 / H5 20 /
Body L 20 / Body M・Body 16 / Label 14 / Caption 12 / Overline 10。
簡報端仍以 deck-kit 的 `--fs-*` 為準（投影距離不同），Typography 那組是產品介面的。

---

## 三、吉祥物（NUMINAI）

`assets/` 內的 SVG 是從 Brand Guideline 的向量原稿抽出來重建的（非截圖）：

```
logo-wordmark.svg   NUMiNAI 字標
logo-lockup.svg     NUMiNAI ＋「數學 AI 精靈」橫式組合
mascot-full.svg     全身　　mascot-half.svg  半身
pose-*.svg          12 種肢體與表情：wave stand heart question pen crown
                    correct exclaim ring study peek think（已去掉原稿的淡綠底板）
```

**造型規則（Guideline 原文）**：身體＝筆劃工具、頭上是「π」、務必保持中分髮型；
扁平化、避免尖角；情緒配比＝身體 60%＋臉部 30%＋道具 10%。

**背景限制（Guideline p24，很重要）**：吉祥物可放的底色只有
**白、淡綠 `#ECF8F6`、黑、黃 `#F3E43B`、藍 `#2B70C9`**。
**不可**放在青綠系（`#0AACA3`）或淺藍系背景上——會糊掉。
→ 所以本 kit 的章節頁把吉祥物放在**右側米白區**，不是左側深綠塊。

---

## 四、踩過的坑

- **別給 `.probe-chapter` 加 `position:relative`**。`.slide` 本身是 `position:absolute; inset:0`，
  加了會蓋掉，章節頁會整頁掉出畫面（只有第一張看得到）。要當定位錨點直接用 `.slide` 就好。
- logo symbol 的 viewBox 是 `0 0 260 67`（數感那顆是 `162.16 45.83`），
  換 logo 時 `aspect-ratio` 與 `.brand-logo` 的寬高要一起改。
- 字標的青綠是寫死的 `#82D3C6`（品牌規範「請勿隨意改變色彩」），
  不吃 `currentColor`，所以深底頁上它仍是青綠，不會變白。

---

*建立：2026-08-21　來源：Numina數學AI精靈 Brand Guideline／Color Palette／Typography／VI*

## 老師自己改字、直接儲存、自動重排、動畫（2026-09-13 起）

- 雙擊 `開啟簡報.command` 開簡報 → 按 `E` 進編輯模式 → 點文字直接改（圖裡的字也可以）→ 按「儲存」直接寫回同一個 html，不跳視窗；舊版留在 `backups/`。完整說明見 `README_編輯與儲存.md`。
- 改完字版面會自動重排：整塊刪掉的方塊收起來、色塊縮小、卡片列重新分寬、圖片／圖表自動放大。
- 動畫依功能自動配（長條長出來、折線畫出來、數字跑上去、卡片依序浮上），按 `M` 整場關。想指定就在元素上寫 `data-anim="…"`。
- 每頁最多「按一下」：有標 `data-reveal` 的頁，進頁只看骨架和現況，按 → 一次演出論點，再按才翻頁（頁碼旁黃點＝還有一段）。
- 刪字之後會「補回」：字剩得少的區塊自動放大、卡片變少會變大（版型階段見 `template-spec.md` §九）；`check_deck.py` 會列出偏空的頁。
- **AI 重建 HTML 前必跑** `python3 keep_edits.py 舊.html 新.html`，老師的修改才不會被蓋掉。
