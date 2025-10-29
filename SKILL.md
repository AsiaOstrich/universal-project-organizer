# Universal Project Organizer

A Claude skill for automatically organizing and generating project files in the correct locations.

## What This Skill Does

When users ask you to create code files (services, controllers, components, etc.), this skill:

1. **Reads project configuration** (`.claude/project.yaml`) to understand the project structure
2. **Determines correct file paths** based on project type and naming conventions
3. **Generates boilerplate code** with proper imports, annotations, and structure
4. **Creates test files** automatically when configured
5. **Places files in the right locations** following project conventions

## When to Use This Skill

Use this skill when the user requests:

- ✅ "Create a UserService"
- ✅ "Generate a ProductController"
- ✅ "Add a User model to the users app"
- ✅ "Create a UserProfile component"
- ✅ "Generate repository for Order"
- ✅ "Add a custom hook for authentication"

Do NOT use for:
- ❌ Modifying existing files (use standard editing)
- ❌ Reading files (use standard reading)
- ❌ General coding questions (answer directly)
- ❌ Refactoring existing code (use standard tools)

## How to Use This Skill

### Step 1: Understand the User's Request

Parse the request to extract:
- **File type**: service, controller, component, model, etc.
- **Name**: User, Product, Order, etc.
- **Additional context**: app name (for Django), custom options

Examples:
```
"Create a UserService"
  → Type: service
  → Name: User

"Add a User model to the users app"
  → Type: model
  → Name: User
  → App: users

"Generate a ProductController with tests"
  → Type: controller
  → Name: Product
  → Note: Tests will be auto-generated if configured
```

### Step 2: Locate and Load Configuration

Use the configuration resolver to find and load project configuration:

```python
from pathlib import Path
from skill.scripts.config_resolver import resolve_config

# Resolve configuration (handles hierarchical configs)
project_root = Path.cwd()
config = resolve_config(project_root)
```

**What this does**:
- Searches for `.claude/project.yaml` in current and parent directories
- Merges hierarchical configurations (child overrides parent)
- Returns complete configuration with all settings

**If no configuration found**:
```python
# Guide user to create configuration
print("No project configuration found.")
print("Please create .claude/project.yaml with your project structure.")
print("\nExample for Spring Boot:")
print("  project_type: spring-boot")
print("  language: java")
print("  base_package: com.example.demo")
```

### Step 3: Generate Files

Use the file generator to create files:

```python
from skill.scripts.file_generator import generate_file

# Generate files (includes main file + tests + additional files)
generated_files = generate_file(
    config=config,
    file_type='service',      # From user request
    name='User',              # From user request
    project_root=project_root,
    app='users',              # Optional, for Django
    dry_run=False             # Set to True to preview
)

# Report what was created
for file in generated_files:
    test_marker = "[TEST]" if file.is_test else ""
    print(f"✓ Created {test_marker} {file.path}")
```

**What this generates**:
- Main file with boilerplate code
- Test file (if `generate_test: true`)
- Additional files (CSS, types, etc.)

### Step 4: Inform the User

Provide clear feedback about what was created:

```python
# Good response format:
print(f"\n✓ Created {file_type}: {name}")
print(f"\nGenerated {len(generated_files)} file(s):")
for file in generated_files:
    relative_path = file.path.relative_to(project_root)
    if file.is_test:
        print(f"  ✓ [TEST] {relative_path}")
    else:
        print(f"  ✓ {relative_path}")

# Show file content if helpful
if len(generated_files) <= 2:  # Only for simple cases
    main_file = generated_files[0]
    print(f"\n{main_file.path.name}:")
    print("```" + config['language'])
    print(main_file.content)
    print("```")
```

## Complete Workflow Example

### Example 1: Spring Boot Service

**User**: "Create a UserService"

**Your Response**:

```python
from pathlib import Path
from skill.scripts.config_resolver import resolve_config
from skill.scripts.file_generator import generate_file

# 1. Load configuration
project_root = Path.cwd()
config = resolve_config(project_root)

# 2. Generate files
generated_files = generate_file(
    config=config,
    file_type='service',
    name='User',
    project_root=project_root
)

# 3. Report results
print("✓ Created service: User\n")
print(f"Generated {len(generated_files)} file(s):")
for file in generated_files:
    relative_path = file.path.relative_to(project_root)
    marker = "[TEST]" if file.is_test else ""
    print(f"  ✓ {marker} {relative_path}")

# Show the generated code
main_file = generated_files[0]
print(f"\n{main_file.path.name}:")
print(f"```java")
print(main_file.content)
print("```")
```

**Output**:
```
✓ Created service: User

Generated 2 file(s):
  ✓ src/main/java/com/example/demo/service/UserService.java
  ✓ [TEST] src/test/java/com/example/demo/service/UserServiceTest.java

UserService.java:
```java
package com.example.demo.service;

import org.springframework.stereotype.Service;
import org.springframework.beans.factory.annotation.Autowired;

@Service
public class UserService {

    // TODO: Implement business logic

}
```
```

### Example 2: Django Model

**User**: "Add a User model to the users app"

**Your Response**:

```python
from pathlib import Path
from skill.scripts.config_resolver import resolve_config
from skill.scripts.file_generator import generate_file

# 1. Load configuration
project_root = Path.cwd()
config = resolve_config(project_root)

# 2. Generate files (note the 'app' parameter for Django)
generated_files = generate_file(
    config=config,
    file_type='model',
    name='User',
    project_root=project_root,
    app='users'  # Django requires app name
)

# 3. Report results
print("✓ Created model: User in users app\n")
for file in generated_files:
    print(f"  ✓ {file.path.relative_to(project_root)}")

print(f"\nGenerated code:")
print("```python")
print(generated_files[0].content)
print("```")
```

### Example 3: React Component

**User**: "Create a UserProfile component"

**Your Response**:

```python
from pathlib import Path
from skill.scripts.config_resolver import resolve_config
from skill.scripts.file_generator import generate_file

# 1. Load configuration
project_root = Path.cwd()
config = resolve_config(project_root)

# 2. Generate files (React creates multiple files)
generated_files = generate_file(
    config=config,
    file_type='component',
    name='UserProfile',
    project_root=project_root
)

# 3. Report results
print("✓ Created component: UserProfile\n")
print(f"Generated {len(generated_files)} file(s):")
for file in generated_files:
    print(f"  ✓ {file.path.relative_to(project_root)}")

print("\nComponent structure created with:")
print("  - UserProfile.jsx (main component)")
print("  - UserProfile.module.css (styles)")
print("  - UserProfile.test.jsx (tests)")
```

## Error Handling

### Configuration Not Found

```python
from skill.scripts.config_resolver import ConfigurationError

try:
    config = resolve_config(project_root)
except ConfigurationError as e:
    print(f"❌ Configuration error: {e}")
    print("\nTo fix this:")
    print("1. Create .claude/project.yaml in your project root")
    print("2. Specify your project type and structure")
    print("\nExample:")
    print("```yaml")
    print("project_type: spring-boot")
    print("language: java")
    print("base_package: com.example.demo")
    print("```")
    print("\nSee available templates:")
    print("  python skill/scripts/template_loader.py")
    return
```

### File Type Not Found

```python
from skill.scripts.file_generator import FileGenerationError

try:
    generated_files = generate_file(...)
except FileGenerationError as e:
    print(f"❌ Generation error: {e}")

    # Show available file types
    structure = config.get('structure', {})
    print("\nAvailable file types in this project:")
    for file_type in structure.keys():
        print(f"  - {file_type}")
    return
```

### File Already Exists

```python
try:
    generated_files = generate_file(config, 'service', 'User', project_root)
except FileGenerationError as e:
    if "already exists" in str(e):
        print(f"❌ {e}")
        print("\nOptions:")
        print("1. Use a different name")
        print("2. Delete the existing file first")
        print("3. Edit the existing file instead")
    else:
        raise
```

### Missing Required Parameter (Django)

```python
# Django models require 'app' parameter
if config.get('project_type') == 'django' and file_type == 'model':
    if not app:
        print("❌ Django models require an app name.")
        print("\nUsage: 'Create a User model in the users app'")
        print("Or specify: --app users")
        return
```

## Best Practices

### 1. Confirm Before Creating

For complex operations, confirm with user:

```python
# Preview with dry-run
preview = generate_file(..., dry_run=True)

print(f"This will create {len(preview)} file(s):")
for file in preview:
    print(f"  - {file.path.relative_to(project_root)}")

# Ask for confirmation in your response
print("\nShould I proceed? (yes/no)")
```

### 2. Show Configuration Source

Help users understand which config is being used:

```python
from skill.scripts.config_resolver import ConfigResolver

resolver = ConfigResolver(project_root)
config = resolver.resolve()

print("Using configuration from:")
for source in config.get('_config_sources', []):
    print(f"  - {source}")
```

### 3. Validate File Type

Check if requested file type exists:

```python
structure = config.get('structure', {})
if file_type not in structure:
    available = ', '.join(structure.keys())
    print(f"❌ File type '{file_type}' not found.")
    print(f"\nAvailable types: {available}")
    print("\nDid you mean one of these?")
    # Suggest similar types
    import difflib
    suggestions = difflib.get_close_matches(file_type, structure.keys(), n=3)
    for suggestion in suggestions:
        print(f"  - {suggestion}")
    return
```

### 4. Handle Multiple Configs

For projects with hierarchical configs:

```python
resolver = ConfigResolver(project_root)

# Show resolution order
print("Configuration resolution order:")
print(resolver.show_resolution_order())

# This helps users understand why certain settings are active
```

### 5. Suggest Related Actions

After creating files, suggest next steps:

```python
print("\n✓ Files created successfully!")
print("\nNext steps:")
print("  1. Implement business logic in UserService")
print("  2. Add tests in UserServiceTest")
print("  3. Run tests: mvn test")

if config.get('project_type') == 'spring-boot':
    print("  4. Inject service in controllers with @Autowired")
```

## Advanced Features

### Preview Mode (Dry Run)

```python
# Generate without writing files
preview = generate_file(..., dry_run=True)

print("Preview mode - no files will be created:")
for file in preview:
    print(f"\nFile: {file.path}")
    print("Content preview:")
    print(file.content[:200] + "..." if len(file.content) > 200 else file.content)
```

### Custom Content

```python
# User provides specific code
custom_code = """
@Service
public class UserService {
    @Autowired
    private UserRepository repository;

    public User findById(Long id) {
        return repository.findById(id).orElse(null);
    }
}
"""

generated_files = generate_file(
    config=config,
    file_type='service',
    name='User',
    project_root=project_root,
    custom_content=custom_code  # Use custom instead of boilerplate
)
```

### Batch Generation

```python
# Create multiple related files
entities = ['User', 'Product', 'Order']

for entity in entities:
    try:
        files = generate_file(config, 'service', entity, project_root)
        print(f"✓ Created {entity}Service")
    except Exception as e:
        print(f"❌ Failed to create {entity}Service: {e}")
```

## Debugging

### Show Configuration Details

```python
import json

print("Current configuration:")
print(json.dumps(config, indent=2))
```

### Test Path Resolution

```python
from skill.scripts.path_resolver import PathResolver

resolver = PathResolver(config, project_root)

# Test path resolution
full_path = resolver.resolve_full_path('service', 'User')
print(f"Service 'User' will be created at: {full_path}")

# Test with different names
for name in ['User', 'user_service', 'UserService']:
    path = resolver.resolve_full_path('service', name)
    print(f"  {name:20} → {path}")
```

### List Available Templates

```python
from skill.scripts.template_loader import TemplateLoader

loader = TemplateLoader()
templates = loader.list_templates()

print("Available templates:")
for template_id, language, project_type in templates:
    print(f"  - {template_id:15} ({language:10}) - {project_type}")
```

## Common Scenarios

### Scenario 1: New Project Setup

**User**: "I want to set up a Spring Boot project for file organization"

**Your Response**:
1. Check if `.claude/` directory exists
2. If not, offer to create it
3. Suggest using a template or creating custom config
4. Guide them through the setup

### Scenario 2: Unknown File Type

**User**: "Create a UserHelper"

**Your Response**:
1. Check if "helper" file type exists in config
2. If not, suggest similar types (util, component, service)
3. Ask user to clarify or add to config

### Scenario 3: Multi-Module Project

**User**: "Create a UserService in the backend module"

**Your Response**:
1. Navigate to backend/ directory
2. Use hierarchical config resolution
3. Generate files in correct module

### Scenario 4: Custom Requirements

**User**: "Create a UserService but use UserBusinessService as the class name"

**Your Response**:
1. Explain that naming comes from template
2. Offer to generate with custom content
3. Or suggest updating the template

## Tool Reference

### Configuration Tools

```python
# config_resolver.py
from skill.scripts.config_resolver import (
    resolve_config,           # Main function
    ConfigResolver,           # Class for advanced usage
    ConfigurationError        # Exception type
)

# config_parser.py (single config)
from skill.scripts.config_parser import (
    load_config,             # Load single config
    ConfigParser,            # Parser class
    ConfigError              # Exception type
)
```

### Generation Tools

```python
# file_generator.py
from skill.scripts.file_generator import (
    generate_file,           # Main function
    FileGenerator,           # Generator class
    FileGenerationError,     # Exception type
    GeneratedFile            # Dataclass for results
)

# path_resolver.py
from skill.scripts.path_resolver import (
    resolve_path,            # Convenience function
    PathResolver,            # Resolver class
    PathResolutionError      # Exception type
)
```

### Template Tools

```python
# template_loader.py
from skill.scripts.template_loader import (
    TemplateLoader,          # Loader class
    TemplateError            # Exception type
)

loader = TemplateLoader()
templates = loader.list_templates()           # List all
template = loader.load_template('spring-boot') # Load specific
info = loader.get_template_info('spring-boot') # Get metadata
```

## Summary

This skill enables you to:

1. ✅ **Understand** project structure from `.claude/project.yaml`
2. ✅ **Generate** files with correct paths, names, and content
3. ✅ **Support** multiple project types (Spring Boot, Django, React)
4. ✅ **Handle** hierarchical configurations (monorepos, multi-module)
5. ✅ **Create** test files automatically
6. ✅ **Apply** framework-specific annotations and imports
7. ✅ **Provide** clear feedback and error messages

When in doubt:
- Use dry-run mode to preview
- Show available file types
- Check configuration sources
- Suggest corrections for errors

Always prioritize clear communication with the user about what you're creating and where it will be placed.