# Universal Project Organizer

> A Claude Skill that helps developers automatically place generated files in the correct project locations.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status](https://img.shields.io/badge/Status-MVP%20Ready-brightgreen.svg)]()
[![Tests](https://img.shields.io/badge/Tests-34%20Passing-success.svg)]()
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)]()
[![Node](https://img.shields.io/badge/Node-20.19%2B-green.svg)]()

## 🎯 Overview

Ever asked Claude to generate a file and wondered where it should go? This skill solves that problem by understanding your project structure and automatically placing files in the correct locations.

### Key Features

- 📂 **Smart File Placement** - Automatically determines the correct location for generated files
- ⚡ **Fast & Efficient** - Uses configuration files to avoid repeated project scanning
- 🎨 **Multi-Framework Support** - Works with Spring Boot, Django, React, Next.js, and more
- 📝 **Customizable** - Define your own project structure rules
- 👥 **Team-Friendly** - Configuration files can be version controlled and shared
- 🔄 **Template System** - Quick setup with pre-built templates

## 🚀 Quick Start

### Prerequisites

- **Node.js** >= 20.19.0 (for OpenSpec)
- **Python** 3.8+ (for utility scripts)

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/universal-project-organizer.git

# Navigate to the project
cd universal-project-organizer

# Install Node.js dependencies (OpenSpec)
npm install

# Install Python dependencies (when available)
pip install -r requirements.txt
```

### OpenSpec Setup

This project uses [OpenSpec](https://github.com/Fission-AI/OpenSpec) for spec-driven development.

OpenSpec is already initialized in this project. You can use the following commands:

```bash
# List active change proposals
npx openspec list

# List specifications
npx openspec list --specs

# View a change or spec
npx openspec show [item-name]

# Validate changes
npx openspec validate [change-name] --strict

# Archive completed changes
npx openspec archive <change-name> --yes
```

For more details, see [OpenSpec documentation](openspec/AGENTS.md).

### Usage

#### 1. Set up your project configuration

Create `.claude/project.yaml` in your project root:

```yaml
project_type: spring-boot  # or django, react
language: java             # or python, javascript
base_package: com.example.demo

structure:
  service:
    path: "src/main/java/{package}/service"
    naming: "{Name}Service.java"
    generate_test: true
```

Or use a pre-built template:
```bash
# View available templates
python skill/scripts/template_loader.py

# Use a template (copy to your project)
cp skill/templates/java/spring-boot.yaml your-project/.claude/project.yaml
```

#### 2. Use with Claude

Simply ask Claude to create files:

```
You: "Create a UserService"

Claude: ✓ Created service: User

Generated 2 file(s):
  ✓ src/main/java/com/example/demo/service/UserService.java
  ✓ [TEST] src/test/java/com/example/demo/service/UserServiceTest.java
```

Claude will:
- Read your `.claude/project.yaml`
- Determine the correct file path
- Generate boilerplate code with annotations
- Create test files automatically

## 📖 How It Works

### Configuration-Based Approach

Each project maintains a `.claude/project.yaml` file that defines:
- Project type and language
- Directory structure rules
- File naming conventions
- Auto-generation preferences

Example configuration:
```yaml
project_type: spring-boot
language: java
base_package: com.example.myapp

structure:
  service:
    path: "src/main/java/com/example/myapp/service"
    naming: "{Name}Service.java"
    generate_test: true
```

### Workflow

1. Claude reads the project configuration
2. Determines the correct file path based on rules
3. Generates the file with appropriate structure
4. Optionally creates related files (tests, etc.)

## 🎨 Supported Project Types

### Currently Supported
- ☕ Java (Spring Boot, Maven, Gradle)
- 🐍 Python (Django, FastAPI, Flask)
- ⚛️ JavaScript/TypeScript (React, Next.js, Vue, Express)
- 🐹 Go (Standard project layout)

### Coming Soon
- Ruby on Rails
- .NET Core
- Rust
- PHP (Laravel, Symfony)

## 📚 Documentation

### Core Documentation
- [⚡ **SKILL.md**](SKILL.md) - **Complete skill interface guide for Claude**
- [📋 Project Specification](docs/project-spec.md) - Detailed technical specification
- [🔧 Configuration Schema](docs/config-schema.md) - YAML configuration reference
- [🎨 Available Templates](docs/available-templates.md) - 3 built-in templates (Spring Boot, Django, React)
- [📖 Templates Guide](docs/templates.md) - Template system documentation

### Advanced Features
- [🔀 Hierarchical Configuration](skill/examples/multi-config-example/README.md) - Priority rules and merging
- [📖 OpenSpec Guide](docs/openspec-guide.md) - Spec-driven development with OpenSpec
- [⚖️ License Guide](docs/license-guide.md) - MIT License information

### Examples
- [Spring Boot Example](skill/examples/example-spring-boot/) - Complete configuration example
- [Multi-Config Example](skill/examples/multi-config-example/) - Monorepo / multi-module setup

## 🛠️ Development

### Project Structure

```
universal-project-organizer/
├── skill/                  # Core skill implementation
│   ├── SKILL.md           # Main skill file for Claude
│   ├── scripts/           # Utility scripts
│   ├── templates/         # Project templates
│   └── examples/          # Example projects
├── tests/                 # Test suite
├── docs/                  # Documentation
└── README.md
```

### Running Tests

```bash
# Run all unit tests
python3 tests/test_config_parser.py
python3 tests/test_path_resolver.py
python3 tests/test_template_loader.py

# Run workflow tests
python3 skill/examples/skill-workflow-test.py
```

**Test Results**: ✅ 34/34 tests passing

### Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines. (Coming soon)

## 🗺️ Roadmap

### ✅ Phase 1: MVP (COMPLETE!)
- [x] Project specification & OpenSpec setup
- [x] Complete SKILL.md interface
- [x] Configuration parser (single & hierarchical)
- [x] 3 core templates (Spring Boot, Django, React)
- [x] File generation engine
- [x] Path resolution system
- [x] Template loader
- [x] Comprehensive testing (34 tests)
- [x] Full documentation

### 🚧 Phase 2: Enhancement (In Progress)
- [ ] Auto-detection system for project types
- [ ] More project templates (Maven, Flask, Next.js, Vue, etc.)
- [ ] VS Code extension
- [ ] Configuration migration tools
- [ ] Performance optimization

### 📅 Phase 3: Advanced Features
- [ ] Custom rule engine DSL
- [ ] Team configuration sharing platform
- [ ] MCP server version
- [ ] Real-time validation
- [ ] IDE plugins (JetBrains, VS Code)
- [ ] AI-powered template generation

## 💡 Why This Project?

When working with Claude to generate code, one of the most common pain points is:
1. Claude generates great code
2. But you have to manually place it in the right location
3. And remember your project's structure conventions

This skill automates that process, making Claude-assisted development faster and more seamless.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/YOUR_USERNAME/universal-project-organizer/issues).

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by the need for better file organization in Claude-assisted development
- Built with the Claude Skills framework
- Thanks to the open-source community

## 📬 Contact

- **GitHub Issues**: [Create an issue](https://github.com/YOUR_USERNAME/universal-project-organizer/issues)
- **Discussions**: [Join the discussion](https://github.com/YOUR_USERNAME/universal-project-organizer/discussions)

---

**Status**: 🚧 Work in Progress - Currently in active development

**Latest Update**: 2025-10-27
