---
name: thc-gitcommit
description: 依專案的 commit 規範建立 git commit，規範來源依序為 .cz.toml、其他規範檔、git log 既有慣例；可為已暫存 (staged) 的變更產生單一 commit，或掃描所有變更並依主題拆分為多個 commit。使用者要求提交變更或撰寫 commit message 時使用。觸發語句如「幫我 commit」「提交變更」「寫 commit message」「拆分 commit」「分成多個 commit」，以及英文 "commit this"、"write a commit message"、"split commits"。只在使用者明確要求時觸發，不主動建議；只是檢視 diff、解釋變更內容或詢問 git 用法時不觸發。
---

# THC Git Commit: 依專案規範建立 commit

本技能依專案的 commit 規範產生 commit message，並在使用者確認後提交。

| 模式 | 處理範圍 | 產出 |
| --- | --- | --- |
| 模式 A: 單一 commit | 已暫存 (staged) 的變更 | 一個 commit |
| 模式 B: 自動拆分 | 所有變更，含未暫存與未追蹤的檔案 | 依主題拆分的多個 commit |

判斷模式：使用者訊息含「拆分」「分成多個」「掃描剩餘變更」「怎麼拆 commit」或 "split commits" 時採模式 B，其他情境採模式 A。

## 內建寫作規範

本技能的產出與對話回應都遵循以下規範。若環境已安裝 `thc-zhtw-style`，以其完整規範為準。

- 語氣：正式、中性、精簡，一句一概念；不使用口語、情緒化或行銷式修辭。表格與清單允許短語體。
- 事實與推論分開：優先陳述可驗證的事實與觀察；推論標示「可能」「推測原因」或「建議確認」；避免「一定」「絕對」「完全沒有問題」等絕對語氣。
- 用字：使用台灣繁體中文與台灣資訊產業慣用語，例如程式、資料、預設、伺服器、最佳化。
- 識別字：指令、路徑、檔名、參數、分支名稱一律以反引號標記，逐字保留。
- 標點：中文句讀用全形 `，。、；：「」`；問號、驚嘆號與夾注括號用半形，左右括號必須同為半形；冒號前一個字元不是中文字時用半形 `: `；中文與英文、數字之間加一個半形空格。
- 禁用符號：`→`、`—`、`…`、`～`、`✓` 等特殊符號，改用 `->`、「至」、冒號或逗號分句、`...`、「是」「否」。
- 讀者：技術內容須讓工程師可理解、客戶可接受。

## 共用步驟 1: 確定 commit 規範

依下列順序尋找規範，採用第一個找到的來源，並在呈現 commit message 時註明依據。

1. 專案根目錄的 `.cz.toml`，或 `pyproject.toml` 的 `[tool.commitizen]`: 讀取允許的 `change_type`、`scope` 清單、`message_template` 與 `schema_pattern`。type 與 scope 一律以設定檔為準，不得自行增減。
2. 其他規範檔：`commitlint.config.*`、`.commitlintrc*`、`.gitmessage`，或 `CONTRIBUTING*` 中的 commit 章節。
3. 以上皆無：以 `git log --oneline -20` 推斷既有慣例，包含是否使用 `type(scope):` 前綴、使用的語言與用詞習慣，並沿用該慣例。
4. 既無設定檔，git log 也沒有一致慣例，例如新建立的儲存庫：提議採用 Conventional Commits 的 type，即 `feat`、`fix`、`docs`、`refactor`、`test`、`perf`、`build`、`ci`、`chore`，先徵得使用者同意再使用。

`message_template` 若含 issue 欄位，例如 `[<issue>]`，僅在使用者明確提供 issue 編號時填入，否則省略該欄位。

## 共用步驟 2: 敏感內容檢查

兩種模式都必須執行。檢查即將提交的內容是否含有不應入庫的檔案或片段：模式 A 檢查已暫存內容，模式 B 檢查所有變更。

| 類別 | 範例 |
| --- | --- |
| 暫存檔與產物 | `tmp_*`、`*.tmp`、`*.log`、`nohup.out`、個人筆記、中間產物 |
| 機敏設定 | `.env`、`credentials.json`、`*_secret.*`、`*.pem`、`id_rsa*` |
| 機敏字串 | diff 中的 Webhook URL、API 金鑰、存取權杖、密碼 |

發現疑慮時，列出檔案與理由並建議處理方式：刪除、加入 `.gitignore`、執行 `git rm --cached`，或在模式 A 以 `git restore --staged <file>` 移出暫存區。等待使用者決定，不得直接 commit。

## 模式 A: 單一 commit

### 步驟 A1: 分析已暫存的變更

執行 `git diff --cached --stat` 與 `git diff --cached`。

- 只分析已暫存內容，忽略未暫存與未追蹤的檔案。
- 沒有已暫存變更時，告知使用者「請先執行 `git add`」並結束，不得自動執行 `git add`。
- 接著執行共用步驟 2。

### 步驟 A2: 擬定 commit message

- 標題：依共用步驟 1 的格式撰寫，例如 `<type>(<scope>): <subject>`。subject 使用繁體中文，50 字以內，不加句號。
- 內文 (選填): 條列式，每項以 `- ` 開頭，描述「做了什麼」，而非「改了哪個檔案」。變更涉及多個面向時才寫，單純改動可以省略。
- 標題與內文的用字、標點遵循本技能的內建寫作規範。

### 步驟 A3: 呈現給使用者審查 (人工確認點)

完整呈現 commit message 與所依據的規範來源，詢問「是否可以提交?」，等待明確同意後才執行。

### 步驟 A4: 執行 commit

```bash
git commit -m "$(cat <<'EOF'
<標題>

<內文>
EOF
)"
```

完成後執行 `git status` 確認結果。

## 模式 B: 自動拆分

### 步驟 B1: 掃描所有變更

並行執行 `git status --short`、`git diff --stat`、`git diff --cached --stat`，並列出未追蹤的檔案。

### 步驟 B2: 依主題分類

依邏輯目的分類，不依檔案位置分類。type 與 scope 的實際取值以共用步驟 1 的規範為準，下表僅為示意。

| 主題 | 示意 type | 範例 |
| --- | --- | --- |
| 純格式化 | 規範中對應格式化的 type | Ruff 或 Prettier 統一引號、import 排序 |
| 新功能或新檔案 | `feat` | 新增 API 欄位、新腳本 |
| 設定檔調整 | 規範中對應設定的 type | 多台主機的共同屬性調整 |
| 測試 | `test` | 新增測試檔、修正既有測試 |
| 錯誤修正 | `fix` | 修正程式錯誤 |
| 文件 | `docs` | README、使用說明 |

判斷技巧：

- 抽樣檢視各檔 diff 的前 50 至 100 行即可歸類。
- 多個檔案出現相同的變更模式，歸為同一主題。
- 單一檔案混合多個主題時，須拆分 hunk (變更區塊)【暫譯】，做法見步驟 B6。
- 超過 100 行的 diff 常含多個主題，須仔細檢視。

### 步驟 B3: 敏感內容檢查

針對所有變更，包含未追蹤的檔案，執行共用步驟 2。

### 步驟 B4: 擬定拆分方案

以表格呈現主題與檔案的對應：

```markdown
| 主題 | 檔案 | 檔案數 |
| --- | --- | --- |
| A. <主題> | <檔案清單> | N |
| B. <主題> | <檔案清單> | M |
```

單一檔案混合多個主題時，提供兩種方案供使用者選擇：

| 方案 | 做法 | 取捨 |
| --- | --- | --- |
| 方案 1: 精細 | 拆分 hunk，每個主題一個 commit | 歷史較乾淨，工作量較大 |
| 方案 2: 簡單 | 整個檔案歸入一個主要 commit | 較快，commit 內文須涵蓋各面向 |

為每個 commit 草擬標題與內文，標明使用的格式與規範來源。敏感檔案另列「事前清理」步驟。

### 步驟 B5: 取得使用者確認 (人工確認點)

完整呈現拆分方案，詢問採用哪個方案、敏感檔案如何處理，等待明確同意後才執行。

### 步驟 B6: 執行拆分

若環境提供任務追蹤工具，以其記錄每個 commit 的進度。開始前若已有暫存內容，先確認其所屬主題；必要時以 `git restore --staged <file>` 移出，讓每個 commit 只包含當下主題的內容。

**多個檔案、單一主題**：執行 `git add <files>` 後 commit。

**單一檔案、多個主題**：以 patch 只寫入暫存區，全程不修改工作區檔案，避免任何步驟失敗時遺失變更。

1. 建立備份並確認成功。`<flat-name>` 是把路徑中的 `/` 換成 `__` 的檔名，例如 `src/a.py` 對應 `src__a.py`，避免備份路徑的子目錄不存在。

   ```bash
   mkdir -p "$(git rev-parse --git-dir)/thc-split"
   git diff HEAD -- <file> > "$(git rev-parse --git-dir)/thc-split/<flat-name>.full.patch"
   cp -- <file> "$(git rev-parse --git-dir)/thc-split/<flat-name>.final"
   ```

   兩個備份檔都存在且非空才繼續；任一失敗即停止並回報。
2. 對每個主題依序執行：
   - 從 `full.patch` 複製出只含該主題 hunk 的 `<flat-name>.<topic>.patch`，保留 `diff --git`、`---`、`+++` 檔頭。
   - 執行 `git apply --cached --recount <topic.patch>`，只套用到暫存區。
   - 以 `git diff --cached -- <file>` 確認暫存內容正確，再以當前主題的 message 執行 `git commit`。
3. 全部主題完成後驗證：
   - `git diff HEAD -- <file>` 無輸出，代表所有 hunk 皆已提交。
   - `cmp <file> "$(git rev-parse --git-dir)/thc-split/<flat-name>.final"` 無輸出，代表工作區未被更動。
4. 驗證通過後刪除 `thc-split` 備份目錄；驗證失敗則保留備份並回報差異。

未追蹤的新檔案預設整檔歸入單一主題。使用者要求拆分時，先以 `git add -N <file>` 讓檔案出現在 `git diff` 中，再依上述流程處理。

### 步驟 B7: 完成後驗證

- `git status`: 確認工作目錄乾淨，或只剩使用者決定保留的檔案。
- `git log --oneline -N`: 列出所有新 commit。
- 向使用者回報拆分結果，每行一個 commit，內容為 hash 與標題。

## 重要規則

- 必須遵循本技能的內建寫作規範；commit 標題與內文維持精簡，不套用「觀察、影響與風險、建議行動」的分段結構。
- 必須依共用步驟 1 確定規範；有設定檔時遵守其 type、scope 與 `schema_pattern`，不得使用清單外的值。
- 兩種模式都必須執行共用步驟 2 的敏感內容檢查。
- 禁止加入 AI 署名，例如 `Co-Authored-By`、`Generated by`。
- 禁止加入 issue 編號，除非使用者明確指定。
- 禁止未經使用者確認就執行 `git commit`。
- 禁止未經使用者確認就執行 `git add`；模式 B 在拆分方案獲得核准後可以自動暫存。
- 禁止以 `git commit --amend` 修改既有 commit。commit 內容有誤時先向使用者說明，經同意後以 `git reset --soft HEAD~1` 撤回該 commit，變更會保留在暫存區，再重新提交；讓每次改寫都是明確且經確認的動作。
- 拆分 hunk 期間禁止以 `git checkout` 或 `git restore` 還原工作區檔案。
- subject 與內文必須使用繁體中文，除非專案規範或既有慣例另有規定。
- pre-commit hook 失敗時 commit 並未建立：修正問題後重新執行 `git add` 並建立新的 commit，不得使用 amend。
