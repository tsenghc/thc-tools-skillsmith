# Domain docs

本檔說明工程類技能探查程式碼時，如何使用本儲存庫的領域文件。

## 探查前先讀取

- 根目錄的 `GLOSSARY.md`；或
- 根目錄的 `GLOSSARY-MAP.md` (若存在): 它指向各個 context 的 `GLOSSARY.md`，讀取與主題相關的每一份。
- `docs/adr/`: 讀取與即將修改的區域相關的 ADR (架構決策紀錄)。multi-context 的儲存庫還要檢查 `src/<context>/docs/adr/` 中屬於特定 context 的決策。

上述檔案不存在時，直接繼續，不提出也不建議預先建立。`/domain-modeling` 技能 (經由 `/grill-with-docs` 與 `/improve-codebase-architecture` 觸發) 會在名詞或決策實際定案時才建立這些檔案。

## 檔案結構

本儲存庫為 single-context: 

```text
/
├── GLOSSARY.md
├── docs/adr/
│   ├── 0001-event-sourced-orders.md
│   └── 0002-postgres-for-write-model.md
└── src/
```

multi-context 的儲存庫 (根目錄有 `GLOSSARY-MAP.md`): 

```text
/
├── GLOSSARY-MAP.md
├── docs/adr/                          ← 全系統層級的決策
└── src/
    ├── ordering/
    │   ├── GLOSSARY.md
    │   └── docs/adr/                  ← 特定 context 的決策
    └── billing/
        ├── GLOSSARY.md
        └── docs/adr/
```

## 使用名詞表的用語

產出中提到領域概念時，例如 issue 標題、重構提案、假設、測試名稱，使用 `GLOSSARY.md` 定義的名詞，不改用名詞表明確避免的同義詞。

需要的概念尚未收錄於名詞表時，代表兩種可能：正在發明專案未使用的用語，應重新考慮；或名詞表確實有缺口，記下來交給 `/domain-modeling` 處理。

## 標示與 ADR 的衝突

產出與既有 ADR 牴觸時，明確指出，不得默默推翻：

> _與 ADR-0007 (event-sourced orders) 牴觸，但值得重新討論，因為..._
