# skillsmith

作者自用後公開分享的 [Claude Code](https://code.claude.com) plugin marketplace，收錄以繁體中文撰寫的開發流程技能：依規範建立 commit、對話交接、接手專案前的探查，以及繁中技術文件的風格與結構規範。

歡迎自由使用與修改。本儲存庫以作者自身需求為主，不保證回應 issue 或提供支援。

## 使用前提

- [Claude Code](https://code.claude.com)
- 執行 `thc-zhtw-style` 的檢查腳本時需要 Python 3；腳本只使用標準函式庫，不需另外安裝套件。

## Plugin 一覽

| Plugin | 包含的技能 | 用途 |
| --- | --- | --- |
| `thc-gitcommit` | `thc-gitcommit` | 依專案 commit 規範建立 commit，規範來源依序為 `.cz.toml`、其他規範檔、git log 慣例。模式 A 處理已暫存的變更，模式 B 依主題自動拆分為多個 commit |
| `thc-handoff` | `thc-handoff` | 將工作脈絡存成 `HANDOFF.md`，納入 git 追蹤並標示最後更新時間；新對話接手時先求證、回報，再等待確認 |
| `thc-onboarding` | `thc-onboarding` | 動手前唯讀探查專案，以繁體中文呈現精簡的專案概況後停下等待指示 |
| `thc-docs` | `thc-zhtw-style`、`thc-techdoc` | 繁中技術文件：風格規範與檢查腳本 `check_zhtw.py`，以及把素材整理成分層技術文件的結構規範 |

各 plugin 互相獨立，可以只安裝需要的幾個。`thc-gitcommit`、`thc-handoff`、`thc-onboarding` 各自內建精簡的寫作規範；同時安裝 `thc-docs` 時，改以完整的風格規範為準。

## 安裝

```bash
# 1. 註冊 marketplace
/plugin marketplace add tsenghc/thc-tools-skillsmith

# 2. 安裝需要的 plugin
/plugin install thc-gitcommit@skillsmith
/plugin install thc-handoff@skillsmith
/plugin install thc-onboarding@skillsmith
/plugin install thc-docs@skillsmith
```

## 更新

本儲存庫發佈新版本後，執行下列指令取得更新：

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

在新對話中說「繼續上次的工作」時，專案根目錄有 `HANDOFF.md` 則由 `thc-handoff` 接手，沒有則由 `thc-onboarding` 探查專案。

所有技能在提交、執行具副作用的指令或開始實作前，都會停在人工確認點，等使用者明確同意後才繼續。

## 修改技能

如果要依自己的需求修改技能，以下檔案可以作為參考：

- `GLOSSARY.md`: 本儲存庫的用語定義與譯名約定。
- `docs/adr/`: 設計決策與其原因。
- `AGENTS.md`: AI agent 在本儲存庫工作時遵循的規範。

本儲存庫的文件與技能遵循 `thc-zhtw-style` 風格規範。修改後執行檢查腳本，結束代碼為 0 代表沒有錯誤：

```bash
python3 plugins/thc-docs/skills/thc-zhtw-style/scripts/check_zhtw.py README.md AGENTS.md GLOSSARY.md docs/agents/*.md docs/adr/*.md plugins/*/skills/*/SKILL.md plugins/*/skills/*/references/*.md
```

## 目錄結構

```text
AGENTS.md                           # agent 設定與專案規範
GLOSSARY.md                         # 專案用語定義
LICENSE                             # MIT 授權條款
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

## 授權

本儲存庫以 [MIT 授權條款](LICENSE) 釋出。
