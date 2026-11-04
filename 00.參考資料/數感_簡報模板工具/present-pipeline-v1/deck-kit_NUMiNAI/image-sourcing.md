# 配圖採購指南 — AI Context 文件

> 本文件指導 AI 為簡報主動抓配圖。讀完後你應該知道：
> 1. 該去哪裡找圖（優先序）
> 2. 怎麼驗證授權能用
> 3. 抓下來怎麼放、HTML 怎麼標 attribution
> 4. 沒找到時怎麼 fallback

---

## 一、來源優先序

依「真實性 ＞ 取得門檻 ＞ 視覺品質」排序：

| 優先 | 來源 | 何時用 | License |
|:-:|---|---|---|
| 1 | **Wikimedia Commons** | 人物、地標、論文圖、歷史照、公領域作品 | 多為 CC BY/BY-SA/PD |
| 2 | **論文/官方原圖** | 講某篇論文時，直接連到該論文 PDF 的原圖（用連結，不下載） | 學術合理使用 |
| 3 | **Unsplash / Pexels** | 情境照（廚房、課堂、書桌等中性場景） | 自家 license（免費商用） |
| 4 | **gen-image skill** | 抽象概念、卡通示意、特定構圖需求、找不到真實圖時 | 自有 |
| 5 | **`.img-ph` 占位** | 已知會替換、本輪不抓 | — |

> **演講簡報規則**（L05 試做累積）：論文圖 v1 用真貼圖讓老師判斷／中性場景多用網路公領域圖／AI 圖用 gen-image，不要無中生有編構圖。

---

## 二、Wikimedia Commons 抓圖流程（最常用）

### Step 1：搜索

```bash
curl -s "https://commons.wikimedia.org/w/api.php?action=query&format=json&list=search&srsearch=YOUR+KEYWORDS&srnamespace=6&srlimit=10"
```

- `srnamespace=6` 限定檔案 namespace
- 中性場景搜：用 Category 比較準
  ```bash
  curl -s "https://commons.wikimedia.org/w/api.php?action=query&format=json&list=categorymembers&cmtitle=Category:Kitchens&cmtype=file&cmlimit=50"
  ```
- 過濾 PDF、肖像、不相關名稱（cozy/holiday/with_woman 等可加可不加）

### Step 2：取得真正 URL + License

```bash
curl -s "https://commons.wikimedia.org/w/api.php?action=query&format=json&titles=File:FILENAME.jpg&prop=imageinfo&iiprop=url|extmetadata&iiurlwidth=1600"
```

從回傳 JSON 抓：
- `imageinfo[0].thumburl`：1600px 寬縮圖（簡報用這個尺寸剛好）
- `extmetadata.LicenseShortName.value`：CC BY 3.0 / CC BY-SA 4.0 / Public domain 等
- `extmetadata.Artist.value`：作者署名（CC BY 必須標）

### Step 3：下載（**一定要加 User-Agent**）

```bash
curl -sL -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
  -o "assets/kebab-name.jpg" \
  "<thumb-url-from-step-2>"
```

> ⚠️ **不加 User-Agent 會拿到 HTML 頁面**（Wikipedia 反爬機制）。記得 `file assets/foo.jpg` 驗證是真 JPEG/PNG。

### Step 4：驗證 + 重命名

```bash
file assets/kebab-name.jpg  # 確認 "JPEG image data" / "PNG image data"
```

檔名規則：英文 kebab-case，禁中文、禁空格、禁 URL 編碼。例：
- `honnold-el-capitan.jpg` ✓
- `Alex Honnold El Capitan.jpg` ✗（空格）
- `廚房.jpg` ✗（中文）

---

## 三、HTML 引用 + Attribution

### 引用

```html
<div class="probe-split__visual" style="position:relative;">
  <img src="assets/honnold-el-capitan.jpg" alt="Alex Honnold free solo on El Capitan">
  <div class="img-cite">Alex Honnold｜El Capitan｜Wikimedia CC BY 3.0</div>
</div>
```

### Attribution 樣式（建議放 base.css 或 inline）

```css
.img-cite {
  position: absolute;
  bottom: 0.6vw; right: 0.8vw;
  font-size: 0.7vw;
  color: #fff; background: rgba(0,0,0,0.5);
  padding: 0.2vw 0.6vw; border-radius: 0.3vw;
  letter-spacing: 0.05em;
}
```

### 標示內容

- **CC BY / CC BY-SA**：必標「作者｜來源｜license」
- **Public Domain / CC0**：建議標「來源｜PD」
- **論文圖**：用連結方式呈現（`<a href="DOI">圖在論文原連結</a>`），**不下載**

---

## 四、Unsplash / Pexels（情境照）

- Unsplash：搜尋 https://unsplash.com/s/photos/KEYWORD ，圖片頁有 download 按鈕
- Pexels：搜尋 https://www.pexels.com/search/KEYWORD/ ，類似
- 兩者都不要求標 attribution（但建議標）
- 不要用 `curl` 從 Unsplash 直接抓（需要 referer header），改用 unsplash.com 給的 download URL，或請使用者下載

---

## 五、版權安全速查表

| License | 可用 | 必標 attribution | 商用 OK |
|---|:-:|:-:|:-:|
| Public Domain / CC0 | ✓ | 建議 | ✓ |
| CC BY (任何版本) | ✓ | **必** | ✓ |
| CC BY-SA | ✓ | **必** | ✓ |
| CC BY-ND | ⚠️ 不可修改 | **必** | ✓ |
| CC BY-NC | ⚠️ 課程教學 OK，外部演講要小心 | **必** | ✗ |
| 沒授權標示 | ✗ | — | ✗ |
| Fair use / 學術合理使用 | ⚠️ 用連結方式呈現，不下載 | 必 | 看情境 |

---

## 六、Fallback：找不到圖

如果 3 個來源都搜不到合適的，**不要硬塞不相干的圖**。改用 `.img-ph` 灰底占位，並在 HTML comment 記錄要補什麼：

```html
<div class="probe-split__visual img-ph">
  Honnold 攀爬台北 101<br>（待補真實圖）
</div>
<!-- TODO: 找 Honnold + 101 合成圖，或請用戶 gen-image -->
```

`.img-ph` 樣式（已在 base 或範例 HTML 內定義）：
```css
.img-ph {
  background: #F4F4F2;
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  color: var(--mid-gray); font-size: 0.95vw;
  text-align: center; padding: 1vw; border-radius: 1vw;
}
.img-ph::before {
  content: "圖片占位"; font-size: 0.8vw;
  letter-spacing: 0.25em; margin-bottom: 0.5vw;
  color: var(--label-gray);
}
```

---

## 七、常見坑

| 坑 | 症狀 | 解法 |
|---|---|---|
| 沒加 User-Agent | 下載到 HTML 而非圖 | `-A "Mozilla/5.0..."` |
| 用 thumburl 但檔不存在 | 404 | 改用原始 `url`（不經 thumb） |
| 中文檔名 | 路徑解析失敗 | 一律英文 kebab-case |
| 圖太大（>5MB） | 簡報開啟慢 | 縮到 1600px 寬就夠 |
| Wikipedia thumb 路徑變動 | 缺圖 | 用 imageinfo API 拿正確 thumburl |
| Pexels/Unsplash 反 curl | 403 | 不要 curl，請用戶手動下載或用 gen-image |

---

## 八、檢核清單

抓完每張圖確認：

- [ ] `file assets/foo.jpg` 顯示真實圖片格式（不是 HTML）
- [ ] 檔名英文 kebab-case
- [ ] License 確認可用
- [ ] HTML `<img alt="...">` 有寫
- [ ] CC BY/SA 圖有附 attribution
- [ ] 圖片寬度不超過 1920px（避免簡報過肥）

---

## 九、gen-image（AI 生成插畫／情境圖）

找不到合適授權照片時，用 `/gen-image`（Codex CLI 走 ChatGPT 訂閱額度）生成。適用：收尾頁滿版情境圖、抽象概念示意（迷霧捷徑、思考結晶…）、教學插畫。

**必踩的坑：**

| 坑 | 解法 |
|---|---|
| **中文路徑會壞**（Codex 在含中文/空格的工作目錄會生不出來或落錯地方）| **一律在 ASCII 暫存路徑跑**（如 `/tmp/imgname/`），生完再 `cp` 到 deck 的 `assets/` |
| 多行 prompt 當 argv 傳 → `No prompt provided via stdin` | 用 heredoc 走 stdin：`cat <<'PROMPT' \| codex exec -C "$(pwd)" -s workspace-write --skip-git-repo-check` |
| 額度用完（生圖消耗比文字快 3–5×，週期制）| 等週期重置／升級帳號／設 `OPENAI_API_KEY` 走 API 計費 |
| 圖內中文字變亂碼 | prompt 明確 `NO text, no words, no letters`；要文字用 HTML 疊字，別讓 AI 畫 |

**滿版收尾圖規格**（搭 `probe-fb` 版型）：

- 直接生 **16:9（1536×1024）**，不要方圖塞長框（會 letterbox）。
- prompt 指定「**BOTTOM THIRD 留乾淨、較暗的空間**」——`probe-fb` 文字壓在下方，主體放上半／一側才不被字蓋到。
- 風格關鍵字：`warm, flat-design, cream (#FAF7F0) + deep forest-green (#0E5E3F), editorial` → 跟數感品牌一致。
- 生完用 headless Chrome 截該頁驗收主體不被字卡住（見 `shot.sh`）。
- 若拿到的是淺色調的圖、白字壓不住，該頁自訂一組更厚的 scrim 補救——見 `slide-system.md` §四 Pattern 6。

### 方圖塞橫框：用 `object-position` 救裁切

**症狀**：gen-image 給的是 1024×1024 方圖，放進橫長的圖框、用 `object-fit:cover`，結果人物的腳、招牌的下緣、桌面上的東西被切掉。

**根因**：`cover` 會把圖放大到填滿框、超出的部分裁掉，而且預設**從正中間裁**。方圖塞橫框＝上下各被裁一塊；但畫面重點（人站在地上、招牌掛在下方）通常偏下，被切掉的正好是要看的部分。

**做法**：把裁切視窗往下挪。

```css
.xxx__img img{ width:100%; height:100%; object-fit:cover; object-position:center 68%; }
```

`65%~72%` 是實測堪用區間（`50%` ＝置中，`100%` ＝貼齊圖片底部）。

**怎麼估**：

1. 先算**可見縱向比例** `f`：

   `f ＝ (框高 ÷ 框寬) × (圖寬 ÷ 圖高)`

   例：框 42u × 28u、圖 1024×1024 → `f ＝ (28/42) × 1 ＝ 0.67`，代表只看得到圖的 67% 高度，33% 會被裁掉。

2. 設 `object-position: center Y%` 之後，實際看到的縱向區間是 `[ Y×(1−f) , Y×(1−f)+f ]`。

   例：`Y=65%`、`f=0.67` → 看到圖的 `21.7% ~ 88.3%`，等於**只從上面裁**、底部幾乎全留，腳和招牌都保住。

3. 算出來 `f ≥ 1`，表示是相反情況（圖被左右裁），改調 `object-position` 的**橫向**值。

> 估完仍要用 `shot.sh` 截那一頁親眼看。公式只保證「沒把該看的裁掉」，不保證構圖好看。
> 更根本的解法：需要橫長框就**直接生 16:9（1536×1024）**，別讓方圖去塞（見上方滿版圖規格）。

### 生圖 prompt 的兩條硬規則

1. **不要出現任何文字**：prompt 寫明 `NO text, no words, no letters, no numbers, no signage text`。模型畫中文一定變亂碼（筆畫看起來像字但不是字），投影出來很傷。要有字就用 HTML 疊在圖上。
2. **留白給字**：講明哪一塊要留乾淨。滿版頁寫 `keep the BOTTOM THIRD dark and visually simple (empty space for overlaid text)`；一般配圖寫 `subject centered with generous margin around it`——主體周圍有餘裕，之後才有空間靠 `object-position` 調裁切。
