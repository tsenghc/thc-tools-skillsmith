# AGENTS.md

本檔提供 AI agent 在本儲存庫工作時的設定與指引。

## Agent skills

### Issue tracker

Issue 以 Markdown 檔記錄在本儲存庫內的 `.scratch/` 目錄。詳見 `docs/agents/issue-tracker.md`。

### Triage labels

使用五個預設的 triage 標籤，標籤字串與角色名稱相同。詳見 `docs/agents/triage-labels.md`。

### Domain docs

採 single-context 結構：根目錄一份 `GLOSSARY.md`，加上 `docs/adr/`。詳見 `docs/agents/domain.md`。

## 專案規範

- 本儲存庫的文件與技能遵循 `thc-zhtw-style` 風格規範。修改 Markdown 後執行下列指令，結束代碼必須為 0 才算通過。

  ```bash
  python3 plugins/thc-docs/skills/thc-zhtw-style/scripts/check_zhtw.py README.md AGENTS.md GLOSSARY.md docs/agents/*.md docs/adr/*.md plugins/*/skills/*/SKILL.md plugins/*/skills/*/references/*.md
  ```

- 修改風格規範時，必須一併同步 `thc-gitcommit`、`thc-handoff`、`thc-onboarding` 的內建寫作規範，原因見 `docs/adr/0001-skills-embed-writing-guide-summary.md`。
- 技能的 front matter 必須寫成單行，多行區塊會在換行處產生空格。
- 用語依 `GLOSSARY.md`。
