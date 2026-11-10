# skillsmith

個人用的 [Claude Code](https://code.claude.com) plugin marketplace，集中管理自製的技能，並可安裝到任何裝置上。

## Plugin 一覽

| Plugin | 包含的技能 | 用途 |
| --- | --- | --- |
| `thc-gitcommit` | `thc-gitcommit` | 依專案 commit 規範建立 commit，規範來源依序為 `.cz.toml`、其他規範檔、git log 慣例。模式 A 處理已暫存的變更，模式 B 依主題自動拆分為多個 commit |
| `thc-handoff` | `thc-handoff` | 將工作脈絡存成 `HANDOFF.md`，納入 git 追蹤並標示最後更新時間；新對話接手時先求證、回報，再等待確認 |
| `thc-onboarding` | `thc-onboarding` | 動手前唯讀探查專案，以繁體中文呈現精簡的專案概況後停下等待指示 |
| `thc-docs` | `thc-zhtw-style`、`thc-techdoc` | 繁中技術文件：風格規範與檢查腳本 `check_zhtw.py`，以及把素材整理成分層技術文件的結構規範 |

## 安裝

本儲存庫為私有，各裝置須先具備存取權限：在 GitHub 帳號加入 SSH 金鑰，或執行 `gh auth login`。

```bash
# 1. 註冊 marketplace (私有儲存庫可使用 SSH 位址)
/plugin marketplace add git@github.com:tsenghc/thc-tools-skillsmith.git

# 2. 安裝 plugin
/plugin install thc-gitcommit@skillsmith
/plugin install thc-handoff@skillsmith
/plugin install thc-onboarding@skillsmith
/plugin install thc-docs@skillsmith
```

## 更新

推送變更後，在各裝置執行：

```bash
/plugin marketplace update skillsmith
/plugin update thc-gitcommit@skillsmith
/plugin update thc-handoff@skillsmith
/plugin update thc-onboarding@skillsmith
/plugin update thc-docs@skillsmith
```

## 使用方式

| 技能 | 觸發語句範例 | 行為 |
| --- | --- | --- |
| `thc-gitcommit` | 「幫我 commit」、"commit this" | 為已暫存的變更產生單一 commit |
| `thc-gitcommit` | 「拆分 commit」、"split commits" | 掃描所有變更並依主題拆分 |
| `thc-handoff` | 「存交接檔」、"save this conversation" | 寫入 `HANDOFF.md` |
| `thc-handoff` | 「從交接檔接手」、"resume from the handoff" | 求證、回報，再等待確認 |
| `thc-onboarding` | 「熟悉一下這個專案」、"onboard me" | 唯讀探查後呈現專案概況並停下 |
| `thc-techdoc` | 「整理成技術文件」、「寫 SOP」 | 判定文件型態後停下確認，再產出分層文件 |
| `thc-zhtw-style` | 「校稿」、「潤稿」 | 套用繁中風格規範並附修改摘要 |

## 文件風格檢查

本儲存庫的技能與文件皆遵循 `thc-zhtw-style` 風格規範。修改後執行檢查腳本，結束代碼為 0 代表沒有錯誤：

```bash
python3 plugins/thc-docs/skills/thc-zhtw-style/scripts/check_zhtw.py README.md AGENTS.md GLOSSARY.md docs/agents/*.md docs/adr/*.md plugins/*/skills/*/SKILL.md plugins/*/skills/*/references/*.md
```

## 目錄結構

```text
AGENTS.md                           # agent 設定與專案規範
GLOSSARY.md                         # 專案用語定義
docs/agents/                        # mattpocock 技能的設定
docs/adr/                           # 架構決策紀錄 (ADR)
.claude-plugin/marketplace.json     # marketplace 清單，列出所有 plugin
plugins/thc-gitcommit/
  .claude-plugin/plugin.json        # plugin 清單
  skills/thc-gitcommit/SKILL.md     # 技能本體
plugins/thc-handoff/
  .claude-plugin/plugin.json
  skills/thc-handoff/SKILL.md
plugins/thc-onboarding/
  .claude-plugin/plugin.json
  skills/thc-onboarding/SKILL.md
plugins/thc-docs/
  .claude-plugin/plugin.json
  skills/thc-zhtw-style/            # 風格規範：SKILL.md、references/、scripts/check_zhtw.py
  skills/thc-techdoc/               # 結構規範：SKILL.md、references/layers.md
```

## 隱私說明

本儲存庫只包含技能指示文字與檢查腳本，不含任何私人媒體檔案，例如照片、縮圖總覽或影片。可以維持私有，也可以公開。
