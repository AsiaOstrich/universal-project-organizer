# Universal Project Organizer

> A Claude Skill that helps developers automatically place generated files in the correct project locations.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status](https://img.shields.io/badge/Status-In%20Development-orange.svg)]()

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

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/universal-project-organizer.git

# Navigate to the project
cd universal-project-organizer

# Install dependencies
pip install -r requirements.txt
```

### Usage

1. **Initialize your project** (one-time setup per project)
   ```bash
   # Auto-detect project type
   python scripts/init_project.py
   
   # Or use a template
   python scripts/init_project.py --template spring-boot
   ```

2. **Use with Claude**
   ```
   User: "Create a UserService class"
   Claude: [reads .claude/project.yaml]
           [generates file at correct location]
   ```

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

- [📋 Project Specification](docs/project-spec.md) - Detailed technical specification
- [⚖️ License Guide](docs/license-guide.md) - Information about the MIT License
- [🔧 Configuration Guide](docs/configuration.md) - How to configure your project (Coming soon)
- [🎨 Templates](docs/templates.md) - Available project templates (Coming soon)

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
pytest tests/
```

### Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines. (Coming soon)

## 🗺️ Roadmap

### Phase 1: MVP (Current)
- [x] Project specification
- [ ] Basic SKILL.md structure
- [ ] Configuration file parser
- [ ] 3 basic templates (Spring Boot, Django, React)
- [ ] File generation logic

### Phase 2: Enhancement
- [ ] Auto-detection system
- [ ] More project templates
- [ ] Configuration validation
- [ ] Comprehensive documentation
- [ ] Test coverage

### Phase 3: Advanced Features
- [ ] Custom rule engine
- [ ] VS Code integration
- [ ] Team configuration sharing
- [ ] MCP server version (optional)

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
