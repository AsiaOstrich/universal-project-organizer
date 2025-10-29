# Project Context

## Purpose

Universal Project Organizer is a Claude Skill that helps developers automatically place generated files in the correct project locations based on project type and structure.

### Goals
- Enable Claude to understand project structures and automatically determine correct file locations
- Support multiple common project types (Spring Boot, Django, React, Next.js, etc.)
- Use configuration files to avoid repeated project scanning
- Provide a team-friendly solution with version-controlled configurations
- Offer template-based quick setup for common frameworks

### Target Users
- Developers using Claude Code to generate code files
- Teams that want consistent file organization across projects
- Projects with complex directory structures and naming conventions

## Tech Stack

### Core Technologies
- **Python 3.8+** - Utility scripts for project initialization and validation
- **Node.js >= 20.19.0** - OpenSpec for spec-driven development
- **YAML** - Configuration file format for project structure definitions
- **Markdown** - Documentation and OpenSpec specifications

### Development Tools
- **OpenSpec (@fission-ai/openspec)** - AI-native spec management system
- **pytest** - Testing framework for Python scripts (planned)
- **PyYAML** - YAML parsing library (planned)
- **Jinja2** - Template engine for file generation (planned)

### Supported Project Types
The skill targets these frameworks and project types:
- **Java**: Spring Boot, Maven, Gradle
- **Python**: Django, FastAPI, Flask
- **JavaScript/TypeScript**: React, Next.js, Vue, Express
- **Go**: Standard project layout

## Project Conventions

### Code Style

#### Python Scripts
- **Style Guide**: PEP 8
- **Line Length**: 100 characters maximum
- **Naming**:
  - Functions: `snake_case`
  - Classes: `PascalCase`
  - Constants: `UPPER_SNAKE_CASE`
  - Private members: prefix with `_`
- **Docstrings**: Use Google-style docstrings for all public functions and classes
- **Type Hints**: Use type hints for function parameters and return values

#### YAML Configuration Files
- **Indentation**: 2 spaces (no tabs)
- **Naming**: `kebab-case` for file names, `snake_case` for keys
- **Comments**: Use `#` for inline explanations of complex configurations
- **Structure**: Group related settings together with blank lines between sections

#### Markdown Documentation
- **Headers**: Use ATX-style headers (`#`, `##`, etc.)
- **Code Blocks**: Always specify language for syntax highlighting
- **Links**: Use reference-style links for repeated URLs
- **Line Length**: Soft limit of 120 characters for readability

### Architecture Patterns

#### Configuration-Driven Design
- Each target project has a `.claude/project.yaml` configuration file
- The Skill reads configuration to determine file locations
- No external services required - pure Skill implementation
- Configurations are version-controlled with the project

#### Template System
- Pre-built templates for common project types
- Templates stored in `skill/templates/{language}/{framework}.yaml`
- Template inheritance and composition for reusability
- User can override templates with custom configurations

#### File Generation Flow
1. Read `.claude/project.yaml` from target project
2. Identify file type from user request (service, controller, model, etc.)
3. Resolve path using configuration rules and templates
4. Apply naming conventions from configuration
5. Generate file with appropriate structure and imports
6. Optionally create related files (tests, etc.)

#### Separation of Concerns
- **skill/SKILL.md**: Main skill logic and instructions
- **skill/scripts/**: Standalone utility scripts (init, detect, validate)
- **skill/templates/**: Configuration templates
- **skill/examples/**: Reference implementations
- **docs/**: User-facing documentation

### Testing Strategy

#### Unit Tests (Planned)
- Test each script module independently
- Mock file system operations
- Test YAML parsing and validation
- Test path resolution logic
- Target: 80% code coverage

#### Integration Tests (Planned)
- Test complete workflow on example projects
- Verify correct file generation for each project type
- Test configuration detection and initialization
- Validate template application

#### Manual Testing
- Test with real Claude Code interactions
- Verify file placement in actual projects
- Test edge cases and error handling
- Validate documentation accuracy

### Git Workflow

#### Branching Strategy
- **master**: Stable, production-ready code
- **develop**: Integration branch for features (if needed)
- **feature/***: Feature development branches
- **fix/***: Bug fix branches

#### Commit Conventions
Follow Conventional Commits specification:
- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation changes
- `refactor:` - Code refactoring
- `test:` - Test additions or updates
- `chore:` - Build process or tool updates

Format: `<type>(<scope>): <description>`

Example: `feat(templates): add FastAPI project template`

#### Commit Requirements
- Clear, descriptive commit messages
- Reference related issues when applicable
- Include Claude Code co-authorship footer:
  ```
  🤖 Generated with [Claude Code](https://claude.com/claude-code)

  Co-Authored-By: Claude <noreply@anthropic.com>
  ```

## Domain Context

### Claude Skills Framework
- Skills are Markdown files that extend Claude's capabilities
- Skills can be project-specific or user-specific
- Skills read from `.claude/` directory in projects
- Skills can use tools like Read, Write, Glob, Grep

### File Organization Patterns
Understanding common project structure patterns:
- **Java/Maven**: `src/main/java/{package}/` and `src/test/java/{package}/`
- **Python/Django**: App-based structure with `{app}/models.py`, `{app}/views.py`
- **React**: Component-based with `src/components/{ComponentName}/`
- **Next.js**: Page-based routing in `pages/` or `app/` directory

### Configuration File Concepts
- **project_type**: Identifies the framework/stack (e.g., "spring-boot", "django")
- **structure**: Maps file types to path templates and naming rules
- **auto_generate**: Flags for automatic generation of related files (tests, etc.)
- **base_package**: Root package/namespace for the project

## Important Constraints

### Technical Constraints
- Must work without external APIs or services (offline-capable)
- Configuration files must be human-readable and easy to edit
- File paths must be platform-independent (Unix and Windows)
- Must handle existing files gracefully (no overwrites without confirmation)
- YAML configurations must validate against a schema

### Design Constraints
- Keep configurations simple - avoid over-engineering
- Prefer convention over configuration when possible
- Start with 3-5 well-supported project types, expand later
- Default to single-file implementations unless complexity demands more
- Follow "10-minute understandability" rule for all features

### Development Phase Constraints
- **MVP Phase**: Focus on core functionality, 3 basic templates
- **No premature optimization**: Implement features as needed
- **Simplicity first**: Avoid frameworks and abstractions until proven necessary
- **User feedback driven**: Iterate based on real usage patterns

## External Dependencies

### Claude Code
- Primary interface for the skill
- Provides tools: Read, Write, Edit, Glob, Grep, Bash
- Manages skill loading and execution
- Handles user interactions

### OpenSpec
- Repository: https://github.com/Fission-AI/OpenSpec
- Version: latest (@fission-ai/openspec)
- Purpose: Spec-driven development workflow
- Integration: Slash commands in `.claude/commands/openspec/`

### Python Standard Library
Used for utility scripts:
- `pathlib` - Path manipulation
- `os` - File system operations
- `json`, `yaml` - Configuration parsing

### Planned Dependencies
- **PyYAML** (>=6.0) - YAML configuration parsing
- **Jinja2** (>=3.0) - Template engine for file generation
- **pytest** (>=7.0) - Testing framework

### No External Services
- No API calls required
- No authentication needed
- No network dependencies for core functionality
- Fully offline-capable

## Project Status

- **Version**: 0.1.0-alpha
- **Phase**: MVP Development
- **License**: MIT
- **Repository**: (To be published)
- **Last Updated**: 2025-10-29
