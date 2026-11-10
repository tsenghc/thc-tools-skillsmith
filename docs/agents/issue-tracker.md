# Issue tracker: 本機 Markdown

本儲存庫的 issue 與規格書 (spec) 以 Markdown 檔記錄在 `.scratch/` 目錄。

## 慣例

- 一個功能一個目錄：`.scratch/<feature-slug>/`。
- 規格書為 `.scratch/<feature-slug>/spec.md`。
- 實作 issue 一張票一個檔案，路徑為 `.scratch/<feature-slug>/issues/<NN>-<slug>.md`，編號從 `01` 起算；不得把多張票合併在單一檔案。
- triage 狀態記錄在每個 issue 檔開頭附近的 `Status:` 行，取值見 `triage-labels.md`。
- 留言與討論紀錄附加在檔案底部的 `## Comments` 標題下。

## 技能要求「發佈到 issue tracker」時

在 `.scratch/<feature-slug>/` 下建立新檔案，目錄不存在時一併建立。

## 技能要求「取得相關的票」時

讀取指定路徑的檔案。使用者通常會直接提供路徑或 issue 編號。

## Wayfinding 操作

供 `/wayfinder` 使用。map 是一個檔案，每張票各有一個 child 檔案。

| 項目 | 規則 |
| --- | --- |
| Map | `.scratch/<effort>/map.md`，內容為 `Notes`、`Decisions-so-far`、`Fog` 三段 |
| Child ticket | `.scratch/<effort>/issues/NN-<slug>.md`，編號從 `01` 起算，內文寫問題本身。`Type:` 行記錄票的類型 (`research`、`prototype`、`grilling`、`task`)；`Status:` 行記錄 `claimed` 或 `resolved` |
| Blocking | 檔案開頭附近的 `Blocked by: NN, NN` 行。所列檔案全部為 `resolved` 時，該票即解除阻擋 |
| Frontier | 掃描 `.scratch/<effort>/issues/`，找出未完成、未被阻擋且未被認領的檔案，編號最小者優先 |
| Claim | 開始任何工作前，先設定 `Status: claimed` 並存檔 |
| Resolve | 在 `## Answer` 標題下附上答案，設定 `Status: resolved`，再把脈絡指引 (摘要加連結) 附加到 `map.md` 的 `Decisions-so-far` 段落 |
