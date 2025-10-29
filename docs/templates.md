# Project Templates

Universal Project Organizer provides pre-built templates for common project types. Templates define standard file structures, naming conventions, and auto-generation settings.

## Available Templates

### Java Templates

#### spring-boot
Complete Spring Boot project template with standard MVC structure.

**File Types:**
- `service` - Business logic services
- `controller` - REST API controllers
- `repository` - Data access repositories
- `model` - Domain models/entities
- `entity` - JPA entities
- `dto` - Data Transfer Objects
- `config` - Configuration classes
- `exception` - Custom exceptions
- `util` - Utility classes
- `component` - Spring components

**Features:**
- Auto-generates test files for services and controllers
- Includes common Spring annotations
- Standard package structure: `{base_package}/{file_type}`
- Test path: `src/test/java/{base_package}/{file_type}`

**Example Configuration:**
```yaml
project_type: spring-boot
language: java
base_package: com.example.myapp
version: "1.0"
```

### Python Templates

#### django
Django web framework template with app-based structure.

**File Types:**
- `model` - Django models
- `view` - Class-based views
- `function_view` - Function-based views
- `serializer` - Django REST Framework serializers
- `form` - Django forms
- `admin` - Admin configurations
- `urls` - URL patterns
- `test` - Test cases
- `manager` - Custom model managers
- `signal` - Django signals
- `middleware` - Custom middleware
- `util` - Utility functions

**Features:**
- App-based structure using `{app}` variable
- Auto-generates test files
- Follows Django conventions (snake_case)
- Includes common Django imports

**Example Configuration:**
```yaml
project_type: django
language: python
version: "1.0"
```

### JavaScript Templates

#### react
Modern React application template with hooks and functional components.

**File Types:**
- `component` - React components (with CSS modules and tests)
- `page` - Page-level components
- `hook` - Custom React hooks
- `context` - React Context providers
- `util` - Utility functions
- `service` - API service modules
- `slice` - Redux Toolkit slices
- `reducer` - Redux reducers
- `action` - Redux actions
- `constant` - Constants
- `type` - TypeScript type definitions

**Features:**
- Component directories with CSS modules
- Auto-generates test files
- Supports both Redux and Context API patterns
- Modern React patterns (hooks, functional components)

**Example Configuration:**
```yaml
project_type: react
language: javascript
version: "1.0"
```

## Using Templates

### 1. Initialize a New Project

To initialize a project with a template:

```bash
python skill/scripts/init_project.py --template spring-boot
```

This creates `.claude/project.yaml` with the template configuration.

### 2. List Available Templates

```bash
python skill/scripts/template_loader.py
```

Output:
```
Available Templates:
============================================================
  spring-boot          (java)
  django               (python)
  react                (javascript)
```

### 3. View Template Details

```bash
python skill/scripts/template_loader.py spring-boot
```

### 4. Customize Templates

Templates can be customized by editing `.claude/project.yaml`:

```yaml
# Original template
project_type: spring-boot
language: java
base_package: com.example.demo

# Customize for your project
base_package: com.mycompany.myapp

# Override specific file type settings
structure:
  service:
    path: "src/main/java/com/mycompany/myapp/business"  # Custom path
    naming: "{Name}BusinessService.java"                # Custom naming
```

## Template Variables

All templates support these variables:

| Variable | Description | Example |
|----------|-------------|---------|
| `{Name}` | PascalCase name | `UserService` |
| `{name}` | snake_case name | `user_service` |
| `{package}` | Package path | `com/example/demo` |
| `{app}` | Django app name | `users` |

## Template Structure

Templates are YAML files located in `skill/templates/{language}/`:

```
skill/templates/
├── java/
│   ├── spring-boot.yaml
│   └── maven.yaml
├── python/
│   ├── django.yaml
│   ├── flask.yaml
│   └── fastapi.yaml
└── javascript/
    ├── react.yaml
    ├── nextjs.yaml
    └── vue.yaml
```

### Template Schema

```yaml
project_type: template-name
language: programming-language
version: "1.0"
base_package: com.example.demo  # Optional, Java projects

structure:
  file_type_name:
    path: "relative/path/{variable}"
    naming: "{Name}Suffix.ext"
    test_path: "test/path"        # Optional
    generate_test: true           # Optional
    additional_files:             # Optional
      - "file1.ext"
      - "file2.ext"

naming_conventions:               # Optional
  class: "PascalCase"
  method: "camelCase"
  constant: "UPPER_SNAKE_CASE"

auto_generate:                    # Optional
  test_files: true
  import_statements: true
  package_declaration: true

annotations:                      # Optional
  file_type_name:
    - "@Annotation1"
    - "@Annotation2"

common_imports:                   # Optional
  file_type_name:
    - "import statement 1"
    - "import statement 2"
```

## Creating Custom Templates

### 1. Create Template File

Create a new YAML file in the appropriate language directory:

```bash
touch skill/templates/python/fastapi.yaml
```

### 2. Define Template Structure

```yaml
project_type: fastapi
language: python
version: "1.0"

structure:
  router:
    path: "app/routers"
    naming: "{name}_router.py"
    generate_test: true
    test_path: "tests/routers"

  schema:
    path: "app/schemas"
    naming: "{name}_schema.py"

  crud:
    path: "app/crud"
    naming: "{name}_crud.py"
    generate_test: true
    test_path: "tests/crud"

naming_conventions:
  class: "PascalCase"
  function: "snake_case"
  constant: "UPPER_SNAKE_CASE"

auto_generate:
  test_files: true
  import_statements: true
```

### 3. Validate Template

```bash
python skill/scripts/init_project.py --template fastapi --validate-only
```

### 4. Test Template

Create a test project:

```bash
mkdir test-project
cd test-project
python ../skill/scripts/init_project.py --template fastapi
python ../skill/scripts/validate_config.py .
```

## Best Practices

### Template Design

1. **Include Common File Types**: Cover the most frequently used file types for the project type
2. **Sensible Defaults**: Use conventions from the framework/ecosystem
3. **Test Support**: Enable `generate_test` for file types that need testing
4. **Clear Naming**: Use descriptive file type names that match domain terminology
5. **Comprehensive Paths**: Use template variables for flexibility

### Using Templates

1. **Start with Template**: Initialize projects with appropriate template
2. **Customize as Needed**: Override specific settings in project.yaml
3. **Validate Configuration**: Run validation after customization
4. **Document Changes**: Comment custom settings in project.yaml

### Maintaining Templates

1. **Version Templates**: Use semantic versioning (1.0, 1.1, etc.)
2. **Document Changes**: Update this file when adding/modifying templates
3. **Test Templates**: Validate templates work with real projects
4. **Community Input**: Gather feedback from users for improvements

## Template Loading API

The `TemplateLoader` class provides programmatic access to templates:

```python
from skill.scripts.template_loader import TemplateLoader, TemplateError

# Initialize loader
loader = TemplateLoader()

# List all templates
templates = loader.list_templates()
# Returns: [('spring-boot', 'java', 'Spring Boot'), ...]

# Load a specific template
template = loader.load_template('spring-boot')
# Returns: Dictionary with template configuration

# Get template info
info = loader.get_template_info('spring-boot')
# Returns: {'template_id': 'spring-boot', 'project_type': 'spring-boot', ...}

# Customize template
custom_values = {'base_package': 'com.mycompany.app'}
customized = loader.customize_template(template, custom_values)
```

## Troubleshooting

### Template Not Found

**Error:**
```
Template 'xyz' not found.

Available templates:
  - spring-boot
  - django
  - react
```

**Solution:** Use one of the available template names.

### Invalid Template Structure

**Error:**
```
Template 'spring-boot' is missing required fields: structure
```

**Solution:** Ensure template YAML has `project_type`, `language`, and `structure` fields.

### Empty Structure

**Error:**
```
Template 'xyz' has invalid or empty structure
```

**Solution:** Define at least one file type in the `structure` section.

### Missing Path or Naming

**Error:**
```
Template 'xyz': structure.service missing 'path'
```

**Solution:** Each file type must have both `path` and `naming` fields.

## Future Templates

Planned templates for future releases:

- **Java**: Maven multi-module, Gradle, Quarkus
- **Python**: Flask, FastAPI, Pytest
- **JavaScript**: Next.js, Vue.js, Express.js
- **TypeScript**: NestJS, Angular
- **Go**: Standard Go project, Gin framework

## See Also

- [Configuration Schema](config-schema.md) - YAML configuration reference
- [Project Specification](../project-spec.md) - Overall project design
- [Examples](../skill/examples/) - Example projects using templates