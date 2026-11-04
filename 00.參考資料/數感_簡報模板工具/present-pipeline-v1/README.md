# 數感簡報 pipeline（present-pipeline-v1）

> 🤖 **要用 AI 做簡報？先看 [AI-START-HERE.md](AI-START-HERE.md)** —— 單一入口，把那份丟給 AI 就能開始動手（硬規則、動畫 class、驗收指令、常見陷阱都在裡面）。

把「做簡報／溝通材料」拆成三個可獨立、也可串接的 Claude Code skill，外加 present 依賴的公司模板包。

- **frame** — 想清楚要講什麼（產敘事骨架）
- **present** — 對齊模板、切頁排版（產 deck，過 check_deck）
- **humanize** — 把文字改得像人（去 AI 味）

完整「何時用哪個」見 [使用說明.md](使用說明.md)。

---

## 資料夾結構

```
present-pipeline-v1/
├── README.md              ← 你在這
├── AI-START-HERE.md       ← 🤖 給 AI 的單一入口（用 AI 做簡報先讀這份）
├── 使用說明.md             ← 何時用哪個 skill（先看這）
├── skills/                ← 三個 skill 的原始碼（可讀、可改）
│   ├── frame/  present/  humanize/
├── skills-install/        ← 一鍵安裝檔（.skill）
├── deck-kit_數感實驗室/           ← present 依賴的模板包（版型、QA、紀律）
└── design-docs/           ← 設計與決策史（想深入才看，非必讀）
```

---

## 安裝

**Skills**（二選一）：
- 簡單：把 `skills-install/` 裡的 `*.skill` 在 Claude Code 安裝。
- 或：把 `skills/` 底下 `frame`、`present`、`humanize` 三個資料夾複製到 `~/.claude/skills/`。

**模板包**：把 `deck-kit_數感實驗室/` 放到一個固定位置（present 會用到）。

---

## ⚠ 必做：設定 present 的 kit 路徑

`frame` 和 `humanize` 自含、裝了就能用。**只有 `present` 需要知道 deck-kit_數感實驗室 在哪。**

安裝後，編輯 `present/SKILL.md` 的「前置」段——把「kit 位置」那行改成你實際放 `deck-kit_數感實驗室/` 的路徑。不設的話，present 會找不到版型與 check_deck。

---

## Windows 注意

跑 kit 的 `check_deck.py`（QA linter）時，主控台是 cp950 會因中文/符號 crash。一律加環境變數：

```
PYTHONUTF8=1 PYTHONIOENCODING=utf-8 python check_deck.py <deck.html>
```

---

## 快速上手

1. 開 Claude Code，把想講的東西丟給它、打 `/frame` → 得敘事骨架。
2. 「把這份骨架做成投影片」→ `/present` → 得 deck（求 check_deck 0 FAIL）。
3. 覺得文案很 AI → 主動打 `/humanize` 潤稿。

（humanize 多半要主動叫——它刻意設計成嚴苛、不會自己亂跳出來。）

---

## 版本

present-pipeline-v1（2026-06-23）。三 skill 皆 v1：frame/humanize 較穩；present 為「薄草稿」，會隨真實使用回饋持續迭代。模板包見 `deck-kit_數感實驗室/CHANGELOG.md`。
