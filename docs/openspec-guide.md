# OpenSpec 使用指南

本專案使用 [OpenSpec](https://github.com/Fission-AI/OpenSpec) 進行規格驅動開發（Spec-Driven Development）。

## 什麼是 OpenSpec？

OpenSpec 是一個 AI 驅動的軟體規格管理系統，專為與 Claude Code 等 AI 助手協同工作而設計。

### 主要優點

- 📝 **版本控制的規格文件** - 所有規格都是 Markdown 文件，可以用 Git 追蹤
- 🔄 **變更提案系統** - 先提案、審查、再實作的工作流程
- 🤖 **AI 友好** - 與 Claude Code 無縫整合，支援 slash commands
- ✅ **自動驗證** - 自動檢查規格格式和完整性
- 🗂️ **結構化管理** - 清晰的目錄結構和命名規範

## 安裝

### 前置需求

- Node.js >= 20.19.0
- npm (通常隨 Node.js 一起安裝)

### 安裝步驟

OpenSpec 已經在本專案中安裝完成。如果需要在其他專案中使用：

```bash
# 本地安裝（推薦）
npm install @fission-ai/openspec --save-dev

# 初始化 OpenSpec
npx openspec init --tools claude
```

## 目錄結構

OpenSpec 初始化後會建立以下結構：

```
openspec/
├── project.md              # 專案上下文和開發慣例
├── AGENTS.md              # AI 助手使用說明（詳細工作流程）
├── specs/                  # 當前規格（source of truth）
│   └── [capability]/       # 單一功能領域
│       ├── spec.md         # 功能需求和場景
│       └── design.md       # 技術設計文件（可選）
├── changes/                # 變更提案（待實作）
│   └── [change-name]/
│       ├── proposal.md     # 變更說明（為什麼、改什麼、影響）
│       ├── tasks.md        # 實作清單
│       ├── design.md       # 技術決策（可選）
│       └── specs/          # 規格變更（delta）
│           └── [capability]/
│               └── spec.md # ADDED/MODIFIED/REMOVED
└── archive/                # 已完成並歸檔的變更
    └── YYYY-MM-DD-[change-name]/
```

### 關鍵文件說明

#### `project.md`
- **用途**：記錄專案的整體資訊
- **內容**：技術棧、程式碼風格、架構模式、測試策略等
- **何時更新**：專案初期設定，之後隨著慣例變更而更新

#### `specs/[capability]/spec.md`
- **用途**：當前已實作功能的規格（source of truth）
- **格式**：需求 + 場景
- **何時更新**：完成變更提案並歸檔時

#### `changes/[change-name]/`
- **用途**：提議的變更
- **生命週期**：提案 → 審查 → 實作 → 歸檔
- **何時建立**：新增功能、重大修改、架構變更時

## 工作流程

### 階段 1: 建立變更提案

#### 何時需要建立提案？

**需要提案的情況**：
- ✅ 新增功能或能力
- ✅ 破壞性變更（API、資料結構）
- ✅ 架構變更
- ✅ 效能優化（改變行為）
- ✅ 安全性模式更新

**不需要提案的情況**：
- ❌ Bug 修復（恢復原有規格的行為）
- ❌ 錯字、格式、註解
- ❌ 依賴更新（非破壞性）
- ❌ 配置變更
- ❌ 為現有行為新增測試

#### 建立提案的步驟

1. **選擇變更 ID**
   - 使用 kebab-case
   - 動詞開頭：`add-`, `update-`, `remove-`, `refactor-`
   - 描述性且唯一：`add-user-authentication`, `refactor-file-generation`

2. **建立目錄結構**
   ```bash
   mkdir -p openspec/changes/[change-id]/specs/[capability]
   ```

3. **撰寫 proposal.md**
   ```markdown
   ## Why
   [1-2 句話說明問題或機會]

   ## What Changes
   - [變更項目列表]
   - [用 **BREAKING** 標記破壞性變更]

   ## Impact
   - Affected specs: [受影響的功能]
   - Affected code: [主要檔案/系統]
   ```

4. **撰寫 tasks.md**
   ```markdown
   ## 1. Implementation
   - [ ] 1.1 建立資料庫 schema
   - [ ] 1.2 實作 API endpoint
   - [ ] 1.3 新增前端元件
   - [ ] 1.4 撰寫測試
   ```

5. **建立規格 delta（`specs/[capability]/spec.md`）**
   ```markdown
   ## ADDED Requirements
   ### Requirement: 新功能
   系統必須提供...

   #### Scenario: 成功情況
   - **WHEN** 用戶執行動作
   - **THEN** 預期結果

   ## MODIFIED Requirements
   ### Requirement: 現有功能
   [完整的修改後需求]

   ## REMOVED Requirements
   ### Requirement: 舊功能
   **Reason**: [為何移除]
   **Migration**: [如何處理]
   ```

6. **驗證提案**
   ```bash
   npx openspec validate [change-id] --strict
   ```

### 階段 2: 實作變更

1. **閱讀提案文件**
   - `proposal.md` - 理解要做什麼
   - `design.md` - 了解技術決策（如果有）
   - `tasks.md` - 取得實作清單

2. **按順序實作任務**
   - 一次完成一個任務
   - 完成後勾選 `- [x]`

3. **等待審查批准**
   - 在開始實作前，確保提案已被審查和批准

### 階段 3: 歸檔變更

功能完成並部署後：

```bash
# 歸檔變更並更新主規格
npx openspec archive <change-id> --yes

# 如果只是工具相關變更（不影響功能規格）
npx openspec archive <change-id> --skip-specs --yes

# 驗證歸檔後的規格
npx openspec validate --strict
```

歸檔後：
- 變更會移至 `archive/YYYY-MM-DD-[change-name]/`
- 規格 delta 會合併到 `specs/[capability]/spec.md`

## 常用命令

### 查看命令

```bash
# 列出所有活躍的變更提案
npx openspec list

# 列出所有規格
npx openspec list --specs

# 查看特定變更或規格的詳情
npx openspec show [item-name]

# 以 JSON 格式查看（用於程式處理）
npx openspec show [item-name] --json
```

### 驗證命令

```bash
# 驗證特定變更
npx openspec validate [change-name]

# 嚴格模式驗證（推薦）
npx openspec validate [change-name] --strict

# 互動式批量驗證
npx openspec validate
```

### 管理命令

```bash
# 歸檔已完成的變更
npx openspec archive <change-id> --yes

# 更新 OpenSpec 指令檔案
npx openspec update

# 互動式儀表板
npx openspec view
```

## 規格撰寫格式

### 需求格式

```markdown
### Requirement: 需求標題
系統必須（SHALL/MUST）...

#### Scenario: 場景名稱
- **WHEN** 條件
- **THEN** 預期結果
- **AND** 額外條件（可選）
```

### 重要格式規則

1. **場景必須使用四個 # 號**
   ```markdown
   #### Scenario: 正確格式 ✅
   ### Scenario: 錯誤格式 ❌
   - **Scenario**: 錯誤格式 ❌
   ```

2. **每個需求至少要有一個場景**

3. **使用 SHALL/MUST 表示強制需求**

4. **MODIFIED 需求要包含完整內容**
   - 從 `specs/` 複製整個需求區塊
   - 修改後貼到 delta 中
   - 不要只寫差異部分

### Delta 操作類型

- `## ADDED Requirements` - 新增的功能
- `## MODIFIED Requirements` - 修改的行為
- `## REMOVED Requirements` - 移除的功能
- `## RENAMED Requirements` - 重新命名

#### ADDED vs MODIFIED 的選擇

- **ADDED**: 引入新的獨立需求或子功能
  - 例如：新增「兩因素認證」功能

- **MODIFIED**: 改變現有需求的行為、範圍或驗收條件
  - 必須包含完整的更新後內容
  - 例如：修改「登入驗證」的行為

## 與 Claude Code 整合

### Slash Commands

OpenSpec 已經為 Claude Code 配置了 slash commands（在 `.claude/commands/openspec/` 目錄）。

### 自動觸發

Claude Code 會在以下情況自動參考 OpenSpec：
- 提到「proposal」、「spec」、「change」、「plan」等關鍵字
- 引入新功能、破壞性變更、架構調整
- 請求不明確，需要查看權威規格

### 使用建議

與 Claude 對話時：
```
"請為新增用戶認證功能建立 OpenSpec 變更提案"
"查看 OpenSpec 中的認證規格"
"驗證當前的 OpenSpec 變更提案"
```

## 常見問題

### Q: 何時該建立 design.md？

建立 `design.md` 的時機：
- 跨模組/服務的變更或新架構模式
- 引入新的外部依賴或重大資料模型變更
- 涉及安全性、效能或遷移的複雜性
- 有技術決策需要在編碼前釐清

否則可以省略 `design.md`。

### Q: 變更提案需要多詳細？

原則：**剛好足夠讓團隊理解和實作**
- 提案：1-2 段落說明「為什麼」和「改什麼」
- 任務：具體的實作步驟清單
- 規格 delta：明確的需求和場景

### Q: 可以同時有多個活躍的變更嗎？

可以，但要注意：
- 檢查是否有衝突（使用 `npx openspec list`）
- 確保不同變更不會修改相同的規格
- 團隊協調避免重複工作

### Q: 如何處理驗證錯誤？

```bash
# 1. 執行嚴格驗證查看詳細錯誤
npx openspec validate [change-id] --strict

# 2. 檢查 JSON 輸出了解詳情
npx openspec show [change-id] --json --deltas-only

# 3. 常見錯誤：
# - 場景格式錯誤：確保使用 #### Scenario:
# - 缺少場景：每個需求至少要有一個場景
# - 缺少 delta：確保有 ## ADDED/MODIFIED/REMOVED
```

## 最佳實踐

### 1. 簡單優先
- 預設變更應該 < 100 行新程式碼
- 單檔案實作，直到證明需要更複雜的結構
- 避免不必要的框架和抽象
- 選擇簡單、經過驗證的模式

### 2. 明確的參考
- 使用 `file.ts:42` 格式標記程式碼位置
- 引用規格時使用 `specs/auth/spec.md`
- 連結相關的變更和 PR

### 3. Capability 命名
- 使用動詞-名詞：`user-auth`, `payment-capture`
- 單一目的
- 10 分鐘可理解性規則
- 如果描述需要「AND」，就該拆分

### 4. 保持同步
- 實作完成後立即歸檔變更
- 不要讓 `changes/` 累積過期提案
- 定期檢視和清理

## 進階使用

### 搜尋技巧

```bash
# 列舉所有規格
npx openspec spec list --long

# 以 JSON 格式輸出（用於腳本）
npx openspec list --specs --json

# 全文搜尋（使用 ripgrep）
rg -n "Requirement:|Scenario:" openspec/specs
rg -n "^#|Requirement:" openspec/changes
```

### 腳本自動化

```bash
# Happy path script
CHANGE=add-two-factor-auth

# 1. 探索當前狀態
npx openspec spec list --long
npx openspec list

# 2. 建立變更結構
mkdir -p openspec/changes/$CHANGE/specs/auth
cat > openspec/changes/$CHANGE/proposal.md << 'EOF'
## Why
...
EOF

# 3. 建立規格 delta
cat > openspec/changes/$CHANGE/specs/auth/spec.md << 'EOF'
## ADDED Requirements
### Requirement: Two-Factor Authentication
...
EOF

# 4. 驗證
npx openspec validate $CHANGE --strict
```

## 更新 OpenSpec

當 OpenSpec 套件更新後：

```bash
# 更新套件
npm install @fission-ai/openspec@latest --save-dev

# 更新專案中的 OpenSpec 指令
npx openspec update
```

## 參考資源

- [OpenSpec GitHub](https://github.com/Fission-AI/OpenSpec)
- [OpenSpec AGENTS.md](../openspec/AGENTS.md) - 完整的工作流程指南
- [專案規格文件](project-spec.md) - 本專案的技術規格

---

**最後更新**: 2025-10-29
**OpenSpec 版本**: latest