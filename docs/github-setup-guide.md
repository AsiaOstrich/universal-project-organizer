# GitHub Repository 建立指南

## 快速建立步驟（推薦）

### 方法 1：使用 GitHub CLI (gh)

如果您有安裝 GitHub CLI：

```bash
# 1. 建立本地專案目錄
mkdir universal-project-organizer
cd universal-project-organizer

# 2. 初始化 Git
git init

# 3. 建立 GitHub repo（會自動在 GitHub 上創建）
gh repo create universal-project-organizer \
  --public \
  --description "A Claude Skill that helps developers automatically place generated files in the correct project locations" \
  --clone

# 4. 設定基本檔案
touch README.md
touch LICENSE
touch .gitignore

# 5. 第一次 commit
git add .
git commit -m "Initial commit"
git push -u origin main
```

### 方法 2：在 GitHub 網站上建立（最簡單）

1. **前往 GitHub**
   - 訪問：https://github.com/new

2. **填寫資訊**
   ```
   Repository name: universal-project-organizer
   Description: A Claude Skill that helps developers automatically place generated files in the correct project locations
   Public: ✅ 選擇 Public
   
   初始化選項：
   ✅ Add a README file
   ✅ Add .gitignore (選擇 Python)
   ✅ Choose a license (選擇 MIT)
   ```

3. **點擊 Create repository**

4. **Clone 到本地**
   ```bash
   git clone https://github.com/你的帳號/universal-project-organizer.git
   cd universal-project-organizer
   ```

### 方法 3：先本地開發，後推送到 GitHub

```bash
# 1. 建立本地專案
mkdir universal-project-organizer
cd universal-project-organizer
git init

# 2. 建立基本檔案（我已經幫你準備好了）
# - 複製 project-spec.md
# - 複製 LICENSE
# - 建立 README.md
# - 建立 .gitignore

# 3. 第一次 commit
git add .
git commit -m "Initial commit: Project specification and license"

# 4. 在 GitHub 上手動建立空的 repo（不要初始化）

# 5. 連接並推送
git remote add origin https://github.com/你的帳號/universal-project-organizer.git
git branch -M main
git push -u origin main
```

---

## 📋 建議的初始檔案

### .gitignore (Python 專案)

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
env/
ENV/
.venv

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/

# OS
.DS_Store
Thumbs.db

# Project specific
.claude/  # 不要提交用戶的專案配置範例
*.log
```

### README.md (初稿)

```markdown
# Universal Project Organizer

A Claude Skill that helps developers automatically place generated files in the correct project locations.

## 🎯 Features

- 📂 Automatically detect project type and structure
- ⚡ Fast file placement using project configuration files
- 🎨 Support for multiple project types (Spring Boot, Django, React, etc.)
- 📝 Customizable project templates
- 👥 Team-friendly (configuration can be version controlled)

## 🚀 Quick Start

Coming soon...

## 📖 Documentation

See [project-spec.md](docs/project-spec.md) for detailed specification.

## 🛠️ Development Status

🚧 **Work in Progress** - Currently in early development phase.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📬 Contact

- GitHub Issues: [Create an issue](https://github.com/你的帳號/universal-project-organizer/issues)
```

---

## 🏷️ 建議的 GitHub 設定

### Repository Topics (標籤)

在 repo 設定中加入這些 topics：

```
claude
claude-ai
skill
claude-skill
project-management
developer-tools
file-organization
code-generation
automation
productivity
python
yaml
```

### Repository Description

```
A Claude Skill that helps developers automatically place generated files in the correct project locations
```

### Repository Settings

- ✅ Issues: Enabled
- ✅ Discussions: Optional (如果想要社群討論)
- ✅ Wiki: Optional
- ✅ Projects: Optional (用於專案管理)

---

## 📦 完整建立流程（推薦）

### Step 1: 在 GitHub 網站建立 repo

1. 訪問 https://github.com/new
2. 填寫資訊並選擇 MIT License
3. 點擊 Create repository

### Step 2: Clone 到本地

```bash
git clone https://github.com/你的帳號/universal-project-organizer.git
cd universal-project-organizer
```

### Step 3: 複製準備好的檔案

```bash
# 把這些檔案複製進去：
# - project-spec.md → docs/project-spec.md
# - license-guide.md → docs/license-guide.md
# - LICENSE (如果 GitHub 沒自動生成)
```

### Step 4: 建立基本結構

```bash
mkdir -p skill/{scripts,templates,examples}
mkdir -p tests
mkdir -p docs

# 移動檔案
mv project-spec.md docs/
mv license-guide.md docs/
```

### Step 5: Commit 並推送

```bash
git add .
git commit -m "docs: Add project specification and license guide"
git push
```

### Step 6: 用 Claude Code 繼續開發

```bash
# 在專案目錄
code .  # 開啟 VS Code

# 在 VS Code 終端
claude code

# 然後對 Claude Code 說：
"請根據 docs/project-spec.md 開始建立專案結構"
```

---

## ✅ 檢查清單

建立完成後確認：

- [ ] README.md 存在且內容正確
- [ ] LICENSE 檔案存在 (MIT)
- [ ] .gitignore 適合 Python 專案
- [ ] docs/project-spec.md 已加入
- [ ] 基本目錄結構已建立
- [ ] GitHub Topics 已設定
- [ ] Repository 設定正確
- [ ] 可以正常 clone

---

## 🎓 後續步驟

1. ✅ 建立 GitHub repo
2. 📝 設定基本檔案
3. 💻 用 VS Code + Claude Code 開始開發
4. 🧪 建立測試
5. 📚 撰寫文檔
6. 🚀 發布第一版

---

## 💡 提示

### 如果要使用 GitHub CLI

```bash
# 安裝 GitHub CLI (如果沒有)
# macOS
brew install gh

# Windows
winget install GitHub.cli

# Linux
# 參考：https://github.com/cli/cli#installation

# 登入
gh auth login
```

### 如果要在 Claude Code 中操作 Git

Claude Code 可以執行 git 指令，所以在 VS Code 環境中可以：

```bash
# Claude Code 可以幫你執行這些
git status
git add .
git commit -m "message"
git push
```

---

**選擇最適合您的方式開始吧！**
