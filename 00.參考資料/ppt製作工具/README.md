# HTML 簡報 Starter Kit（數感實驗室・自適應版）

用 AI 快速產出有質感的 HTML 簡報。**一個 HTML 檔＝一份完整簡報**，瀏覽器雙擊即開、可投影、可列印成 PDF，不需要 PowerPoint。

本範本底層採用**自適應**設計（任何螢幕都不裁切、不漂移），新配色＋內嵌 logo，並內建規劃模式、總覽模式、體檢 linter、截圖驗收等工具。內附三項實用資源：

> 1. **check_deck.py `--measure`** — 用 Chrome 實際渲染量版面溢位，區分「真破版」(超出 slide) 與「裁切」(內文被切)。
> 2. **svg-patterns.md** — 結構圖配方庫（流程、對照、立體圖、折線圖…可直接複製）。
> 3. **all-layouts-demo.html**（根目錄）— 全版型各一頁、附用途說明與 plan-note 的速查 demo。

> ⚠️ **相容性提醒**：若團隊另有人用 **starter-kit_20260613**（vw＋JS 縮放版），它和本範本（純 CSS 自適應）的「16:9 機制」不相容——同一份簡報換底層會跑版。**團隊定案（2026-06-16）：以本版（CSS 自適應）為準，舊 vw/JS 版 deprecated。** 差異原理與舊檔轉換步驟見 `migrating-vw-to-css.md`。

---

## 一、本範本特性（對比一般 vw 範本）

| 項目 | 一般 vw 範本 | 本範本（自適應版） |
|------|-------|--------------|
| 尺寸單位 | `vw`（隨螢幕漂移） | **自適應 `--u`（`1cqw`）＋鎖 16:9 舞台**，任何螢幕不裁切 |
| 配色 | 深綠 `#0E5E3F` | **亮綠 `#379C39` / 深綠 `#004B24` / 米白 `#FEF4E8`** |
| Logo | `<img>` 圖檔（會破圖） | **內嵌 SVG `<use>`**，靠 CSS 染色、不破圖、免圖檔 |
| 內容安全框 | 無 | **`.slide-frame`** 內容框死不溢出（按 `g` 看安全線） |
| 舞台外補色 | 無 | **底色延伸（bleed）**：letterbox 跟著該頁底色延伸 |
| 溢出偵測 | 無 | **slide-audit.js**（console 跑 `auditSlides()`） |
| 規劃模式 P / 總覽模式 O | 有 | **保留**（規劃面板已為新舞台改寫） |
| check_deck / shot | 有 | **保留**（check_deck 已能認得自適應單位） |

---

## 二、快速開始（搭配 AI 使用）

1. **複製整個 numeracy-deck-kit 資料夾**到你的工作位置。
2. 開一個能讀檔的 AI 對話（如 Claude Code）。
3. **讓 AI 讀規範**：`slide-system.md`（必讀，開頭第 ⓪ 節是自適應單位規範）＋`content-style.md`。要配圖再給 `image-sourcing.md`、要畫結構圖再給 `svg-patterns.md`。
4. **給 AI 你的內容**，用下面的起手 prompt。
5. AI 產出的 `xxx.html` 放在**跟 `base.css`、`presenter.js` 同一層**，瀏覽器打開就能用。
6. 跑 `check_deck.py` 體檢（見第五節），0 FAIL 就完成。

### 給 AI 的起手 prompt（可直接複製）

```
請讀這個資料夾裡的 slide-system.md 和 content-style.md，
依照裡面的版型系統和文案規範，幫我把以下內容做成 HTML 簡報：

【內容】（貼上你的文章／大綱／講稿）
【場合與時間】例如：教師研習 60 分鐘（演講約 2 分鐘/頁）
【要求】
- 從 decks/starter.html（極簡、3 頁）起手，要某版型的正典寫法看 layouts/<name>.html（一型一檔）；引用同層的 base.css 和 presenter.js
- 尺寸一律用 calc(N*var(--u))，禁用 vw；內容字 ≥ calc(2*var(--u))
- 每頁內容包進 <div class="slide-frame">（封面/章節/呼吸頁/收尾例外）
- 每頁 <aside class="plan-note"> 放該頁對應的逐字原文（這就是講稿）
- 底色延伸：把 base.css 裡 body:has(.slide.active.probe-X) 的 class 換成你各頁的 class
- 做完用 check_deck.py 體檢，給我 0 FAIL 的版本
```

> 只想先看效果？直接打開 `all-layouts-demo.html`（全版型一次看，由 layouts/ 組裝；它和 base.css、presenter.js 已在同一層）。單看某一型則開 `layouts/<name>.html`。

---

## 三、檔案說明

| 檔案 | 給誰 | 做什麼 |
|------|------|--------|
| README.md | 人 | 本檔 |
| CHANGELOG.md | 人 | kit 的變更與決策紀錄 |
| **slide-system.md** | **AI（必讀）** | 主規範：第 ⓪ 節自適應單位規範＋十種版型＋進階技巧＋防雷 checklist |
| **template-spec.md** | **AI（必讀）** | 版型紀律：何時用哪型、正典間距/邊框值、字級與顏色紀律、擴充守則 |
| content-style.md | AI／人 | 文案風格：投影片語言、避免 AI 痕跡 |
| narrative-guide.md | 人 | 敘事結構：命題怎麼定、頁序怎麼排 |
| image-sourcing.md | AI | 配圖：抓圖、版權標示、AI 生圖 |
| svg-patterns.md | AI | 結構圖配方庫 Pattern A–N |
| migrating-vw-to-css.md | 人 | 舊 vw/JS 版檔案轉本版（CSS 自適應）的差異說明與步驟 |
| base.css | 程式 | 自適應底層：tokens＋16:9 舞台＋安全框＋底色延伸＋規劃層＋列印 |
| presenter.js | 程式 | 翻頁＋規劃模式(P)＋總覽模式(O)＋安全線(g) |
| slide-audit.js | 程式 | 內容溢出偵測（選配，console 跑 `auditSlides()`） |
| autocol.js | 程式（選配） | 長清單自動分欄塞框（保字級）；容器加 `data-autocol="N"`。見 slide-system §五三階策略 |
| autofit.js | 程式（選配） | 內容縮放塞框的最後手段（可能 <2vw、不鼓勵，不可取代砍字） |
| check_deck.py | 程式 | 簡報體檢 linter（詳見第五節） |
| shot.sh | 程式 | headless Chrome 逐頁截圖驗收 |
| decks/starter.html | 人／AI | **極簡起手檔**：封面＋1 內容＋收尾、內含完整 logo。做新簡報從這個起手最輕 |
| layouts/<name>.html | 人／AI | **版型單一真相**：13 型各一檔、雙擊就開，正典 markup＋CSS。改版型改這裡 |
| all-layouts-demo.html | 人／AI | 全版型一次看（由 build_layouts.py 從 layouts/ 組裝，勿手改）；兼 check_deck 整合測試 |
| build_layouts.py | 程式 | 從 layouts/ 組裝 all-layouts-demo.html（組裝合約的可執行版） |
| logo-symbol.html | 人／AI | logo SVG symbol 片段（17 path）；貼進 deck `<body>` 最前，每份一份。**不要手抄**（殘缺會 FAIL） |

---

## 四、簡報操作（打開 HTML 後）

| 操作 | 效果 |
|------|------|
| ← →、空白鍵、點畫面左/右側 | 翻頁 |
| Home／End | 第一頁／最後一頁 |
| 網址加 `#頁碼` | 直接跳該頁（如 `xxx.html#8`） |
| **P** | **規劃模式**：投影片下方展開「對應原文＋設計說明」——對應原文就是上台念的稿 |
| **O** | **總覽模式**：全部頁面縮圖，點哪頁跳哪頁；Esc 關閉 |
| **g** | **安全線**：切換 `.slide-frame` 安全框紅虛線 |
| 觸控左右滑 | 翻頁（平板） |

**自適應**：把視窗拉超寬或超扁，畫面都維持 16:9 置中、不變形不裁切，舞台外補色跟著該頁底色延伸。

**列印成 PDF**：瀏覽器列印（或 headless Chrome `--print-to-pdf`），規劃層自動隱藏，每頁一張 1920×1080。

---

## 五、品質檢查（交件前必跑）

```bash
# 體檢：頁碼、缺圖、字級≥2（vw 或 calc(N*var(--u)) 都認）、emoji、重複 CSS、規劃層、原文覆蓋
python3 check_deck.py 你的簡報.html 文章.md     # 第二參數選配：多檢「逐字覆蓋」
python3 check_deck.py 你的簡報.html --fix-css   # 合併手改累積的重複 CSS（先自動備份 .bak）
python3 check_deck.py 你的簡報.html --measure   # 用 Chrome 實際渲染量爆框：真破版=FAIL、裁切=提示

# 逐頁截圖驗收（改完版面一定要親眼看）
./shot.sh 你的簡報.html 1-11 /tmp/out --contact   # 範圍＋自動拼縮圖總覽

# 內容溢出偵測（瀏覽器 console）
auditSlides()                                     # 印出每頁爆框量；按 g 可同時看安全線
```

目標：**0 FAIL**。WARN 是提醒（例如圖內小字、模板尚未補的 plan-note），需目視判斷。

---

## 六、環境需求

- **看簡報 / 做簡報**：任何現代瀏覽器（建議 Chrome）。字型走 Google Fonts（Noto Sans TC），離線退回系統字型。**這部分跨平台都一樣，Windows/Mac 皆可。**
- **check_deck.py**：python3（內建模組就夠）。靜態體檢跨平台通用。
- **check_deck.py --measure / shot.sh**：需要 Google Chrome。內建的是 **macOS/Linux 的 Chrome 路徑**；**Windows 使用者**請改檔案開頭的 Chrome 路徑（如 `C:\Program Files\Google\Chrome\Application\chrome.exe`）。`--contact` 另需 python3＋Pillow（`pip3 install Pillow`）。
- 註：`--measure` 和 `shot.sh` 只是「驗收工具」，不影響簡報本身顯示；沒裝 Chrome 也能正常做與播簡報。

---

## 七、設計鐵則（給 AI 也給人，完整版在 slide-system.md 第 ⓪ 節）

- 每頁 `<section class="slide" style="background:#色碼;">`——背景用 inline style，**禁用 `slide--white` 類 class**。
- 版型 CSS（`.probe-*`）寫在該檔的 inline `<style>`；共用底層由 `base.css` 提供。
- **所有尺寸用 `calc(N*var(--u))`，禁用 `vw`**（列印區塊除外）。
- **觀眾要讀的字一律 ≥ `calc(2*var(--u))`**；只有頁碼、出處等微標註可更小。放不下就砍字，不是縮字。
- 內容包進 `.slide-frame`（封面/章節/呼吸頁/收尾例外）；底色延伸 `body:has()` 的 class 換成你各頁的。
- 檔名一律英文 kebab-case，避免路徑問題。
- 強調用「」或螢光黃 `.hi`（整份 ≤ 3 處），不用 Markdown 粗體符號；不用 emoji。

---

## 常見問題

| 問題 | 解法 |
|------|------|
| 打開全白／版面跑掉 | 確認 HTML 跟 `base.css`、`presenter.js` 的相對路徑對（`layouts/` 與 `decks/` 在子層，用 `../base.css`；`all-layouts-demo.html` 在根層，用 `base.css`） |
| 圖片破圖 | `assets/` 要跟 HTML 同層；檔名必須英文 |
| 投影字太小 | 違反 2vw 鐵則——跑 `check_deck.py` 揪出來 |
| 想改品牌色 | 動 `base.css` 開頭的 `:root` token 即可全局生效 |
| 按 P 規劃面板跑版 | 確認用本版 base.css（規劃層已為 16:9 舞台改寫） |
| 簡報要給別人 | 把 HTML＋base.css＋presenter.js＋assets/ 一起打包；或列印成 PDF |
