# Universal Project Organizer - 開發規格

## 專案概述

一個 Claude Skill，用於幫助開發者在生成檔案時自動放置到正確的專案位置。

### 核心功能
- 📂 根據專案類型自動識別正確的檔案位置
- ⚡ 使用配置檔系統避免重複掃描
- 🎯 支援多種常見專案類型（Spring Boot, Django, React, Next.js 等）
- 📝 可自訂配置以適應特殊專案結構
- 👥 團隊友好（配置檔可版本控制）

---

## 技術架構

### 方案：Skill + 專案配置檔系統

```
核心設計理念：
1. 每個專案有自己的配置檔（.claude/project.yaml）
2. Skill 讀取配置決定檔案位置
3. 無需外部服務（純 Skill 實作）
4. 配置檔可進版本控制
```

---

## 專案結構

```
universal-project-organizer/
├── README.md                    # 專案說明
├── LICENSE                      # 授權（建議 MIT）
├── .gitignore                   # Git 忽略規則
│
├── skill/                       # Skill 核心
│   ├── SKILL.md                # Claude Skill 主檔案
│   │
│   ├── scripts/                # 輔助腳本
│   │   ├── init_project.py    # 初始化專案配置
│   │   ├── detect_structure.py # 自動偵測專案結構
│   │   ├── validate_config.py  # 驗證配置正確性
│   │   └── generate_file.py    # 檔案生成邏輯
│   │
│   ├── templates/              # 專案配置模板
│   │   ├── java/
│   │   │   ├── spring-boot.yaml
│   │   │   └── maven-generic.yaml
│   │   ├── python/
│   │   │   ├── django.yaml
│   │   │   ├── fastapi.yaml
│   │   │   └── flask.yaml
│   │   ├── javascript/
│   │   │   ├── react.yaml
│   │   │   ├── nextjs.yaml
│   │   │   ├── vue.yaml
│   │   │   └── express.yaml
│   │   ├── go/
│   │   │   └── standard.yaml
│   │   └── generic.yaml        # 通用模板
│   │
│   └── examples/               # 範例專案
│       ├── example-spring-boot/
│       ├── example-django/
│       └── example-react/
│
├── tests/                      # 測試
│   ├── test_init.py
│   ├── test_detection.py
│   └── test_validation.py
│
└── docs/                       # 文檔
    ├── getting-started.md
    ├── configuration.md
    ├── templates.md
    └── customization.md
```

---

## 配置檔格式（YAML）

### 基本格式

```yaml
# .claude/project.yaml

# 專案元資訊
project_type: spring-boot  # 專案類型
language: java             # 主要語言
version: "1.0"            # 配置版本

# 基礎資訊
base_package: com.example.myapp  # Java 專案的 base package

# 目錄結構定義
structure:
  # 格式：
  # <檔案類型>:
  #   path: 主要檔案路徑
  #   test_path: 測試檔案路徑（可選）
  #   naming: 命名規則
  #   template: 檔案模板（可選）
  
  service:
    path: "src/main/java/com/example/myapp/service"
    test_path: "src/test/java/com/example/myapp/service"
    naming: "{Name}Service.java"
    generate_test: true
  
  controller:
    path: "src/main/java/com/example/myapp/controller"
    test_path: "src/test/java/com/example/myapp/controller"
    naming: "{Name}Controller.java"
    generate_test: true
  
  repository:
    path: "src/main/java/com/example/myapp/repository"
    naming: "{Name}Repository.java"
  
  model:
    path: "src/main/java/com/example/myapp/model"
    naming: "{Name}.java"
  
  config:
    path: "src/main/java/com/example/myapp/config"
    naming: "{Name}Config.java"

# 命名慣例（可選）
naming_conventions:
  class: "PascalCase"
  method: "camelCase"
  constant: "UPPER_SNAKE_CASE"
  package: "lowercase"

# 專案特定規則（可選）
custom_rules:
  - pattern: "**/*Service.java"
    requires: ["@Service annotation"]
  - pattern: "**/*Controller.java"
    requires: ["@RestController annotation"]

# 自動生成選項
auto_generate:
  test_files: true          # 自動生成測試檔案
  import_statements: true   # 自動加入 import
  package_declaration: true # 自動加入 package 聲明
```

### 不同專案類型的範例

#### Django 專案
```yaml
project_type: django
language: python
version: "1.0"

structure:
  model:
    path: "{app}/models.py"
    naming: "class {Name}(models.Model)"
  
  view:
    path: "{app}/views.py"
    naming: "class {Name}View"
  
  serializer:
    path: "{app}/serializers.py"
    naming: "class {Name}Serializer"
  
  test:
    path: "{app}/tests/test_{module}.py"
    naming: "class Test{Name}"
```

#### React 專案
```yaml
project_type: react
language: javascript
version: "1.0"

structure:
  component:
    path: "src/components/{Name}"
    naming: "{Name}.jsx"
    additional_files:
      - "{Name}.module.css"
      - "{Name}.test.jsx"
  
  page:
    path: "src/pages/{Name}"
    naming: "{Name}.jsx"
  
  hook:
    path: "src/hooks"
    naming: "use{Name}.js"
  
  util:
    path: "src/utils"
    naming: "{name}.js"
```

---

## 使用流程

### 初始設定（每個專案一次）

```bash
# 方式 1：自動偵測
使用者："請初始化這個專案"
Claude 讀取 SKILL → 執行 detect_structure.py
→ 自動識別專案類型（檢查 pom.xml, package.json 等）
→ 生成對應的 .claude/project.yaml

# 方式 2：使用模板
使用者："這是一個 Spring Boot 專案，請建立配置"
Claude 複製 templates/java/spring-boot.yaml → .claude/project.yaml
→ 根據實際專案調整路徑

# 方式 3：手動配置
使用者自己編寫 .claude/project.yaml
```

### 日常使用

```
使用者："幫我創建 UserService"

Claude 執行流程：
1. 讀取 .claude/project.yaml
2. 查找 structure.service 定義
3. 解析路徑模板和命名規則
4. 生成檔案到：src/main/java/com/example/myapp/service/UserService.java
5. 如果 generate_test: true，同時生成測試檔案
6. 根據規則加入必要的 annotations 和 imports
```

---

## 開發優先順序

### Phase 1: MVP（最小可行產品）
- [ ] 基礎 SKILL.md 結構
- [ ] 配置檔讀取邏輯
- [ ] 2-3 個基本模板（Spring Boot, Django, React）
- [ ] 簡單的檔案生成邏輯
- [ ] 基本的錯誤處理

### Phase 2: 完善功能
- [ ] 自動偵測專案類型
- [ ] 更多專案模板
- [ ] 配置驗證工具
- [ ] 詳細的文檔
- [ ] 測試覆蓋

### Phase 3: 進階功能
- [ ] 自訂規則引擎
- [ ] 配置檔遷移工具
- [ ] VS Code 整合（可選）
- [ ] 團隊配置分享

---

## 技術棧

### 開發語言
- Python 3.8+ （腳本開發）
- Node.js >= 20.19.0 （OpenSpec 規格管理）
- Bash（輔助腳本）

### 依賴

#### Node.js 依賴
```json
// package.json
{
  "devDependencies": {
    "@fission-ai/openspec": "latest"
  }
}
```

#### Python 依賴
```python
# requirements.txt
pyyaml>=6.0        # YAML 配置解析
pathlib>=1.0       # 路徑處理
jinja2>=3.0        # 模板引擎（檔案模板）
pytest>=7.0        # 測試框架
```

### 檔案格式
- YAML（配置檔）
- Markdown（文檔、OpenSpec 規格）
- Python（腳本）

### 規格管理工具

本專案使用 [OpenSpec](https://github.com/Fission-AI/OpenSpec) 進行規格驅動開發：

#### OpenSpec 簡介
- **用途**：AI 驅動的軟體規格管理系統
- **優點**：
  - 版本控制的規格文件
  - 變更提案追蹤（change proposals）
  - 與 Claude Code 無縫整合
  - 自動驗證規格格式

#### 安裝方式
```bash
# 本地安裝（已在專案中完成）
npm install @fission-ai/openspec --save-dev

# 使用 npx 執行命令
npx openspec list
```

#### 基本命令
```bash
# 列出活躍的變更提案
npx openspec list

# 列出現有規格
npx openspec list --specs

# 查看變更或規格詳情
npx openspec show [item-name]

# 驗證變更提案
npx openspec validate [change-name] --strict

# 歸檔完成的變更
npx openspec archive <change-name> --yes
```

#### OpenSpec 目錄結構
```
openspec/
├── project.md              # 專案上下文和慣例
├── specs/                  # 當前規格（已實作的功能）
│   └── [capability]/       # 單一功能領域
│       └── spec.md         # 需求和場景
├── changes/                # 變更提案（待實作的功能）
│   └── [change-name]/
│       ├── proposal.md     # 變更說明
│       ├── tasks.md        # 實作清單
│       ├── design.md       # 技術決策（可選）
│       └── specs/          # 規格變更
│           └── [capability]/
│               └── spec.md # ADDED/MODIFIED/REMOVED
└── archive/                # 已完成的變更
```

#### 工作流程
1. **建立變更提案**：當要新增功能或修改架構時
   ```bash
   # Claude 會自動建立 changes/[change-id]/ 目錄結構
   ```

2. **實作功能**：根據 tasks.md 逐步完成

3. **歸檔變更**：功能完成並部署後
   ```bash
   npx openspec archive <change-id> --yes
   ```

詳細使用方式請參考 [openspec/AGENTS.md](../openspec/AGENTS.md)。

---

## 測試策略

### 單元測試
```python
# tests/test_init.py
def test_detect_spring_boot_project():
    """測試 Spring Boot 專案偵測"""
    
def test_generate_config_from_template():
    """測試從模板生成配置"""

# tests/test_detection.py
def test_parse_pom_xml():
    """測試解析 pom.xml"""
    
def test_parse_package_json():
    """測試解析 package.json"""

# tests/test_validation.py
def test_validate_config_structure():
    """測試配置檔結構驗證"""
    
def test_validate_paths_exist():
    """測試路徑存在性驗證"""
```

### 整合測試
- 在範例專案上測試完整流程
- 測試不同專案類型的配置生成

---

## 文檔規劃

### README.md
- 專案介紹
- 快速開始
- 安裝方式
- 基本範例

### docs/getting-started.md
- 詳細安裝步驟
- 第一次使用教學
- 常見問題

### docs/configuration.md
- 配置檔完整說明
- 所有欄位解釋
- 進階配置範例

### docs/templates.md
- 內建模板列表
- 如何選擇模板
- 如何自訂模板

### docs/customization.md
- 進階自訂指南
- 自訂規則
- 擴展新專案類型

---

## 貢獻指南（未來）

### 社群參與
- Issue 模板
- PR 模板
- 貢獻者指南
- 行為準則

### 專案管理
- 使用 GitHub Projects
- Milestone 規劃
- Release 流程

---

## 授權

建議使用 **MIT License**
- 寬鬆開源
- 商業友好
- 社群接受度高

---

## 後續規劃

### 短期（1-2 個月）
- 完成 MVP
- 發布 v0.1.0
- 收集用戶反饋

### 中期（3-6 個月）
- 擴充模板庫
- 改善自動偵測
- 建立社群

### 長期（6+ 個月）
- 考慮 MCP 版本
- IDE 插件
- 視覺化配置編輯器

---

## 相關資源

### Claude Skills 文檔
- https://docs.claude.com/ (需查閱最新)
- Skill 創建最佳實踐
- 範例 Skills 參考

### 參考專案
- 研究其他 language servers
- 研究專案腳手架工具
- 研究 IDE 專案模板

---

## 開發環境建議

### 本地開發
```bash
# 建立虛擬環境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 安裝依賴
pip install -r requirements.txt
pip install -r requirements-dev.txt  # 開發依賴

# 執行測試
pytest tests/
```

### 使用 Claude Code
```bash
# 在專案根目錄
claude code

# Claude Code 可以幫助：
# - 實作腳本邏輯
# - 撰寫測試
# - 生成文檔
# - 重構程式碼
```

---

## 注意事項

### 避免的坑
- ❌ 不要過早優化（先做 MVP）
- ❌ 不要支援太多專案類型（先做好 3-5 個）
- ❌ 不要配置檔格式過於複雜
- ✅ 保持簡單，逐步迭代

### 設計原則
- **簡單優於複雜**：配置檔要易讀易寫
- **慣例優於配置**：提供合理的預設值
- **漸進式增強**：基本功能先完善
- **社群驅動**：聽取用戶反饋

---

## 聯絡方式（待補充）

- GitHub Issues: [待建立]
- 討論區: [待建立]
- 郵件: [待定]

---

**文件版本**: 1.0  
**最後更新**: 2025-10-27  
**狀態**: 規劃階段 → 準備開始開發
