# Configuration Schema Documentation

This document defines the schema for `.claude/project.yaml` configuration files.

## Overview

The configuration file defines how the Universal Project Organizer should generate and place files in your project.

## Location

The configuration file MUST be located at:
```
<project-root>/.claude/project.yaml
```

## Schema Definition

### Required Fields

#### `project_type` (string)
Identifies the framework or project type.

**Supported values**:
- `"spring-boot"` - Spring Boot Java applications
- `"django"` - Django Python applications
- `"react"` - React JavaScript/TypeScript applications
- `"maven"` - Generic Maven Java projects
- `"flask"` - Flask Python applications
- `"nextjs"` - Next.js applications
- `"vue"` - Vue.js applications
- `"express"` - Express.js applications
- `"go"` - Go projects with standard layout

**Example**:
```yaml
project_type: spring-boot
```

#### `language` (string)
Primary programming language of the project.

**Supported values**:
- `"java"` - Java projects
- `"python"` - Python projects
- `"javascript"` - JavaScript projects
- `"typescript"` - TypeScript projects
- `"go"` - Go projects

**Example**:
```yaml
language: java
```

#### `structure` (object)
Maps file types to their path templates and naming conventions.

**Format**:
```yaml
structure:
  <file-type>:
    path: "<path-template>"
    naming: "<name-template>"
    test_path: "<test-path-template>"  # Optional
    generate_test: <boolean>            # Optional
    additional_files: [<list>]          # Optional
```

**Example**:
```yaml
structure:
  service:
    path: "src/main/java/com/example/app/service"
    naming: "{Name}Service.java"
    test_path: "src/test/java/com/example/app/service"
    generate_test: true
```

### Optional Fields

#### `base_package` (string)
Root package name for Java projects.

**Example**:
```yaml
base_package: com.example.myapp
```

**Usage**: Used in path templates with `{package}` variable.

#### `version` (string)
Configuration file version for future compatibility.

**Default**: `"1.0"`

**Example**:
```yaml
version: "1.0"
```

#### `naming_conventions` (object)
Code style naming conventions.

**Format**:
```yaml
naming_conventions:
  class: "PascalCase"      # or "camelCase", "snake_case", "kebab-case"
  method: "camelCase"
  constant: "UPPER_SNAKE_CASE"
  package: "lowercase"
```

#### `auto_generate` (object)
Flags for automatic file generation.

**Format**:
```yaml
auto_generate:
  test_files: true           # Auto-generate test files
  import_statements: true    # Auto-add imports
  package_declaration: true  # Auto-add package declarations
```

## Template Variables

Path and naming templates can use variables that will be substituted during file generation.

### Supported Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `{Name}` | User-provided name (PascalCase) | `User` |
| `{name}` | User-provided name (lowercase) | `user` |
| `{package}` | Base package converted to path | `com/example/app` |
| `{app}` | Django app name | `accounts` |

### Variable Examples

**Template**:
```yaml
path: "src/main/java/{package}/service"
naming: "{Name}Service.java"
```

**With values**:
- `{package}` = `com.example.myapp` (from `base_package`)
- `{Name}` = `User` (from user request)

**Result**:
```
src/main/java/com/example/myapp/service/UserService.java
```

## Complete Examples

### Spring Boot Project

```yaml
project_type: spring-boot
language: java
version: "1.0"
base_package: com.example.myapp

structure:
  service:
    path: "src/main/java/{package}/service"
    naming: "{Name}Service.java"
    test_path: "src/test/java/{package}/service"
    generate_test: true

  controller:
    path: "src/main/java/{package}/controller"
    naming: "{Name}Controller.java"
    test_path: "src/test/java/{package}/controller"
    generate_test: true

  repository:
    path: "src/main/java/{package}/repository"
    naming: "{Name}Repository.java"

  model:
    path: "src/main/java/{package}/model"
    naming: "{Name}.java"

  config:
    path: "src/main/java/{package}/config"
    naming: "{Name}Config.java"

naming_conventions:
  class: "PascalCase"
  method: "camelCase"
  constant: "UPPER_SNAKE_CASE"
  package: "lowercase"

auto_generate:
  test_files: true
  import_statements: true
  package_declaration: true
```

### Django Project

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

naming_conventions:
  class: "PascalCase"
  function: "snake_case"
  constant: "UPPER_SNAKE_CASE"
```

### React Project

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

naming_conventions:
  component: "PascalCase"
  function: "camelCase"
  constant: "UPPER_SNAKE_CASE"
```

## Validation Rules

### Required Field Validation

All of these fields MUST be present:
- `project_type`
- `language`
- `structure`

### Structure Validation

Each file type in `structure` MUST have:
- `path` - Cannot be empty
- `naming` - Cannot be empty

Optional fields for each file type:
- `test_path` - Test file location
- `generate_test` - Boolean flag
- `additional_files` - Array of related files

### Path Template Validation

Path templates:
- MUST NOT start with `/` (unless absolute path intended)
- CAN use variables in `{variable}` format
- SHOULD use forward slashes `/` (converted automatically on Windows)

### Naming Template Validation

Naming templates:
- MUST include at least one variable (typically `{Name}`)
- MUST include file extension if applicable

## Error Messages

The configuration parser provides clear error messages:

### Missing Required Field
```
❌ Configuration Error: Missing required field 'project_type'

Required fields:
  - project_type
  - language
  - structure

Please add the missing field to your .claude/project.yaml file.
```

### Invalid YAML Syntax
```
❌ Configuration Error: Invalid YAML syntax

File: .claude/project.yaml
Line: 5
Error: mapping values are not allowed here

Please check your YAML syntax. Common issues:
  - Incorrect indentation (use spaces, not tabs)
  - Missing colon after key
  - Unquoted strings with special characters
```

### Invalid Path Template
```
❌ Configuration Error: Invalid path template in structure.service.path

Path: "src/main/java/{invalid variable}/service"

Variables must use format: {VariableName}
Supported variables: {Name}, {name}, {package}, {app}
```

## Best Practices

1. **Use relative paths** - Easier to move projects around
2. **Keep structure simple** - Only define file types you actually use
3. **Use meaningful file type names** - Clear names like `service`, `controller`, not `type1`, `type2`
4. **Include comments** - Help team members understand custom configurations
5. **Version control** - Commit `.claude/project.yaml` to your repository
6. **Validate before use** - Run validation utility after changes

## Migration Guide

When upgrading configuration versions, refer to the migration guide in the documentation.

## See Also

- [Template System Documentation](../openspec/changes/add-mvp-core-features/specs/template-system/spec.md)
- [File Generation Documentation](../openspec/changes/add-mvp-core-features/specs/file-generation/spec.md)
- [Project Examples](../skill/examples/)

---

**Version**: 1.0
**Last Updated**: 2025-10-29