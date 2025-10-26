# Universal Project Organizer Skill

A Claude Skill that helps developers automatically place generated files in the correct project locations.

## Overview

This skill enables Claude to understand project structures and automatically determine the correct location for generated files based on project type and configuration.

## How It Works

1. **Read Project Configuration**: The skill reads `.claude/project.yaml` in the project root
2. **Understand File Type**: Determines what type of file needs to be created (service, controller, model, etc.)
3. **Apply Rules**: Uses the configuration rules to determine the correct path
4. **Generate File**: Creates the file at the correct location with proper structure

## Usage

### Initialize a Project

When setting up a new project:

```
User: "Please initialize this project for Spring Boot"
Claude: [Reads project structure]
        [Detects Spring Boot project]
        [Generates .claude/project.yaml with Spring Boot template]
```

### Generate Files

Once configured, simply ask Claude to create files:

```
User: "Create a UserService class"
Claude: [Reads .claude/project.yaml]
        [Finds service configuration]
        [Creates file at: src/main/java/com/example/app/service/UserService.java]
        [Optionally creates test file]
```

## Configuration Format

The `.claude/project.yaml` file defines project structure:

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

## Supported Project Types

Currently supports:
- **Java**: Spring Boot, Maven, Gradle
- **Python**: Django, FastAPI, Flask
- **JavaScript/TypeScript**: React, Next.js, Vue, Express
- **Go**: Standard project layout

## Commands

### Initialize Project

```
User: "Initialize this as a [project-type] project"
```

Examples:
- "Initialize this as a Spring Boot project"
- "Initialize this as a Django project"
- "Initialize this as a React project"

### Create Files

```
User: "Create a [type] called [name]"
```

Examples:
- "Create a service called UserService"
- "Create a controller called AuthController"
- "Create a component called LoginForm"

### Validate Configuration

```
User: "Validate the project configuration"
```

Claude will check if `.claude/project.yaml` is valid and paths exist.

### Update Configuration

```
User: "Update the configuration to use [custom-path] for [file-type]"
```

## Skill Behavior Guidelines

### When to Read Configuration

**ALWAYS** read `.claude/project.yaml` before generating files. This ensures:
- Files are placed in correct locations
- Naming conventions are followed
- Related files (like tests) are generated if configured

### File Generation Process

1. **Check Configuration**: Read `.claude/project.yaml`
2. **Identify File Type**: Determine what kind of file to create
3. **Apply Path Template**: Use the path from configuration
4. **Apply Naming Convention**: Use the naming pattern from configuration
5. **Generate Content**: Create file with appropriate content
6. **Generate Related Files**: Create tests or other related files if configured

### Error Handling

If `.claude/project.yaml` doesn't exist:
1. Offer to initialize the project
2. Suggest available templates
3. Or ask user for project type

If configuration is invalid:
1. Identify the issue
2. Suggest corrections
3. Offer to fix it

### Best Practices

1. **Always Use Configuration**: Don't guess file locations
2. **Follow Naming Conventions**: Use the configured naming patterns
3. **Generate Complete Files**: Include imports, package declarations, etc.
4. **Create Related Files**: Generate tests if configured
5. **Validate Paths**: Ensure directories exist before creating files

## Development Phase: MVP

This skill is currently in MVP phase. Focus areas:

1. ✅ Configuration file format
2. 🚧 Basic file generation logic
3. 🚧 3-5 project templates
4. 🚧 Path resolution
5. 🚧 Error handling

## Extension Points

This skill can be extended to support:
- Custom file templates
- Custom validation rules
- Team-specific conventions
- Project detection automation

## Examples

### Example 1: Spring Boot Service

**Input**:
```
User: "Create a UserService with CRUD operations"
```

**Process**:
1. Read `.claude/project.yaml`
2. Find `structure.service` configuration
3. Resolve path: `src/main/java/com/example/myapp/service/UserService.java`
4. Generate service class with Spring annotations
5. Generate test file if `generate_test: true`

**Output**:
- `src/main/java/com/example/myapp/service/UserService.java` (created)
- `src/test/java/com/example/myapp/service/UserServiceTest.java` (created)

### Example 2: React Component

**Input**:
```
User: "Create a LoginForm component"
```

**Process**:
1. Read `.claude/project.yaml`
2. Find `structure.component` configuration
3. Resolve path: `src/components/LoginForm/LoginForm.jsx`
4. Generate component file
5. Generate related files (CSS, test) if configured

**Output**:
- `src/components/LoginForm/LoginForm.jsx` (created)
- `src/components/LoginForm/LoginForm.module.css` (created)
- `src/components/LoginForm/LoginForm.test.jsx` (created)

### Example 3: Django Model

**Input**:
```
User: "Create a User model in the accounts app"
```

**Process**:
1. Read `.claude/project.yaml`
2. Find `structure.model` configuration
3. Resolve path using app variable: `accounts/models.py`
4. Generate or update models.py with User class

**Output**:
- `accounts/models.py` (updated with User model)

## Troubleshooting

### Configuration Not Found

**Problem**: `.claude/project.yaml` doesn't exist

**Solution**:
```
User: "Initialize project configuration"
Claude: "What type of project is this? (spring-boot, django, react, etc.)"
User: "Spring Boot"
Claude: [Creates .claude/project.yaml from template]
```

### Wrong File Location

**Problem**: File created in wrong location

**Solution**:
1. Check `.claude/project.yaml` structure definition
2. Verify path templates are correct
3. Update configuration if needed

### Template Not Found

**Problem**: No template for project type

**Solution**:
1. Use generic template
2. Customize manually
3. Or request template addition

## Contributing

To add support for new project types:

1. Create template in `skill/templates/[language]/[type].yaml`
2. Add detection logic in `skill/scripts/detect_structure.py`
3. Test with example project
4. Document in README

## Resources

- [Project Specification](../docs/project-spec.md)
- [Configuration Guide](../docs/configuration.md) (Coming soon)
- [Template Reference](../docs/templates.md) (Coming soon)

---

**Version**: 0.1.0-alpha
**Status**: MVP Development
**Last Updated**: 2025-10-27