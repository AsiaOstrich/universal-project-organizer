# Available Templates

Universal Project Organizer currently provides **3 built-in templates** for common project types.

## Quick Reference

| Template ID | Language | Project Type | File Types | Status |
|------------|----------|--------------|------------|--------|
| `spring-boot` | Java | Spring Boot | 10 types | ✅ Ready |
| `django` | Python | Django Web | 12 types | ✅ Ready |
| `react` | JavaScript | React App | 11 types | ✅ Ready |

---

## 1. Spring Boot Template

**Template ID**: `spring-boot`
**Language**: Java
**Version**: 1.0
**Use Case**: Spring Boot REST API / Microservices

### File Types (10)

| Type | Naming | Path | Auto Test | Description |
|------|--------|------|-----------|-------------|
| `service` | `{Name}Service.java` | `src/main/java/{package}/service` | ✅ | Business logic layer |
| `controller` | `{Name}Controller.java` | `src/main/java/{package}/controller` | ✅ | REST API endpoints |
| `repository` | `{Name}Repository.java` | `src/main/java/{package}/repository` | ❌ | Data access (JPA) |
| `model` | `{Name}.java` | `src/main/java/{package}/model` | ❌ | Domain models |
| `entity` | `{Name}.java` | `src/main/java/{package}/entity` | ❌ | JPA entities |
| `dto` | `{Name}DTO.java` | `src/main/java/{package}/dto` | ❌ | Data transfer objects |
| `config` | `{Name}Config.java` | `src/main/java/{package}/config` | ❌ | Configuration classes |
| `exception` | `{Name}Exception.java` | `src/main/java/{package}/exception` | ❌ | Custom exceptions |
| `util` | `{Name}Util.java` | `src/main/java/{package}/util` | ❌ | Utility classes |
| `component` | `{Name}Component.java` | `src/main/java/{package}/component` | ❌ | Spring components |

### Annotations & Imports

```yaml
service:
  annotations: ["@Service"]
  imports:
    - "org.springframework.stereotype.Service"
    - "org.springframework.beans.factory.annotation.Autowired"

controller:
  annotations: ["@RestController", "@RequestMapping"]
  imports:
    - "org.springframework.web.bind.annotation.*"
    - "org.springframework.http.ResponseEntity"

repository:
  annotations: ["@Repository"]
  imports:
    - "org.springframework.data.jpa.repository.JpaRepository"
    - "org.springframework.stereotype.Repository"

config:
  annotations: ["@Configuration"]

component:
  annotations: ["@Component"]
```

### Example Usage

```bash
# Initialize project with Spring Boot template
python skill/scripts/init_project.py --template spring-boot

# Generate a service
python skill/scripts/file_generator.py . service User
# → UserService.java + UserServiceTest.java

# Generate a controller
python skill/scripts/file_generator.py . controller Product
# → ProductController.java + ProductControllerTest.java
```

### Generated Code Example

**UserService.java**:
```java
package com.example.demo.service;

import org.springframework.stereotype.Service;
import org.springframework.beans.factory.annotation.Autowired;

@Service
public class UserService {

    // TODO: Implement business logic

}
```

---

## 2. Django Template

**Template ID**: `django`
**Language**: Python
**Version**: 1.0
**Use Case**: Django Web Application / REST API

### File Types (12)

| Type | Naming | Path | Auto Test | Description |
|------|--------|------|-----------|-------------|
| `model` | `class {Name}(models.Model)` | `{app}/models.py` | ✅ | Django ORM models |
| `view` | `class {Name}(APIView)` | `{app}/views.py` | ✅ | Class-based views |
| `function_view` | `def {name}(request)` | `{app}/views.py` | ✅ | Function-based views |
| `serializer` | `class {Name}Serializer` | `{app}/serializers.py` | ❌ | DRF serializers |
| `form` | `class {Name}Form` | `{app}/forms.py` | ❌ | Django forms |
| `admin` | `class {Name}Admin` | `{app}/admin.py` | ❌ | Admin panel config |
| `urls` | `urlpatterns = [...]` | `{app}/urls.py` | ❌ | URL routing |
| `test` | `class {Name}TestCase` | `{app}/tests.py` | N/A | Test cases |
| `manager` | `class {Name}Manager` | `{app}/managers.py` | ❌ | Custom managers |
| `signal` | `@receiver(...)` | `{app}/signals.py` | ❌ | Django signals |
| `middleware` | `class {Name}Middleware` | `{app}/middleware.py` | ❌ | Custom middleware |
| `util` | `def {name}(...)` | `{app}/utils.py` | ❌ | Utility functions |

### Common Imports

```yaml
model:
  imports: ["from django.db import models"]

serializer:
  imports: ["from rest_framework import serializers"]

view:
  imports: ["from rest_framework.views import APIView"]

form:
  imports: ["from django import forms"]
```

### Example Usage

```bash
# Initialize project with Django template
python skill/scripts/init_project.py --template django

# Generate a model (requires --app parameter)
python skill/scripts/file_generator.py . model User --app users
# → users/models.py with User model

# Generate a view
python skill/scripts/file_generator.py . view UserList --app users
# → users/views.py with UserList class
```

### Generated Code Example

**models.py**:
```python
"""
User model
"""

from django.db import models


class User(models.Model):
    """
    User model
    """
    # TODO: Implement
    pass
```

---

## 3. React Template

**Template ID**: `react`
**Language**: JavaScript
**Version**: 1.0
**Use Case**: React Single Page Application

### File Types (11)

| Type | Naming | Path | Auto Test | Additional Files | Description |
|------|--------|------|-----------|-----------------|-------------|
| `component` | `{Name}.jsx` | `src/components/{Name}` | ✅ | `.module.css`, `.test.jsx` | React components |
| `page` | `{Name}.jsx` | `src/pages` | ✅ | `.module.css`, `.test.jsx` | Page components |
| `hook` | `use{Name}.js` | `src/hooks` | ✅ | `.test.js` | Custom hooks |
| `context` | `{Name}Context.jsx` | `src/contexts` | ❌ | - | Context providers |
| `util` | `{name}.js` | `src/utils` | ✅ | `.test.js` | Utility functions |
| `service` | `{name}Service.js` | `src/services` | ✅ | `.test.js` | API services |
| `slice` | `{name}Slice.js` | `src/store/slices` | ✅ | `.test.js` | Redux slices |
| `reducer` | `{name}Reducer.js` | `src/store/reducers` | ❌ | - | Redux reducers |
| `action` | `{name}Actions.js` | `src/store/actions` | ❌ | - | Redux actions |
| `constant` | `{name}Constants.js` | `src/constants` | ❌ | - | Constants |
| `type` | `{name}.types.js` | `src/types` | ❌ | - | Type definitions |

### Example Usage

```bash
# Initialize project with React template
python skill/scripts/init_project.py --template react

# Generate a component (creates directory with component + CSS + test)
python skill/scripts/file_generator.py . component UserProfile
# → src/components/UserProfile/
#     UserProfile.jsx
#     UserProfile.module.css
#     UserProfile.test.jsx

# Generate a custom hook
python skill/scripts/file_generator.py . hook User
# → src/hooks/useUser.js
#   src/hooks/useUser.test.js

# Generate a service
python skill/scripts/file_generator.py . service api
# → src/services/apiService.js
#   src/services/apiService.test.js
```

### Generated Code Example

**UserProfile.jsx**:
```javascript
import React from 'react';
import styles from './UserProfile.module.css';

const UserProfile = () => {
  return (
    <div className={styles.container}>
      <h1>UserProfile</h1>
      {/* TODO: Implement component */}
    </div>
  );
};

export default UserProfile;
```

**UserProfile.module.css**:
```css
/* UserProfile styles */

.container {
  /* TODO: Add styles */
}
```

**UserProfile.test.jsx**:
```javascript
import { render, screen } from '@testing-library/react';
import UserProfile from './UserProfile';

describe('UserProfile', () => {
  test('renders UserProfile', () => {
    // TODO: Implement test
  });
});
```

---

## Template Comparison

### By Language

| Language | Templates | Total File Types |
|----------|-----------|------------------|
| Java | spring-boot | 10 |
| Python | django | 12 |
| JavaScript | react | 11 |

### By Features

| Feature | spring-boot | django | react |
|---------|-------------|--------|-------|
| Auto-generate tests | ✅ (service, controller) | ✅ (model, view) | ✅ (most types) |
| Annotations | ✅ Spring annotations | ❌ | ❌ |
| Additional files | ❌ | ❌ | ✅ CSS modules |
| Package structure | ✅ `{package}` variable | ✅ `{app}` variable | ✅ Component folders |
| Naming convention | PascalCase | PascalCase (classes) | PascalCase (components) |

### Auto-Test Support

| Template | File Types with Auto-Test |
|----------|---------------------------|
| `spring-boot` | service, controller (2/10) |
| `django` | model, view, function_view (3/12) |
| `react` | component, page, hook, util, service, slice (6/11) |

---

## Planned Templates

The following templates are documented but not yet implemented:

### Java Templates
- `maven` - Generic Maven project
- `gradle` - Generic Gradle project
- `quarkus` - Quarkus microservices

### Python Templates
- `flask` - Flask web framework
- `fastapi` - FastAPI REST framework
- `pytest` - Python testing project

### JavaScript/TypeScript Templates
- `nextjs` - Next.js framework
- `vue` - Vue.js framework
- `express` - Express.js backend
- `nestjs` - NestJS (TypeScript)

### Other Languages
- `go` - Go project structure
- `rust` - Rust project structure

See [docs/templates.md](templates.md) for details on future templates.

---

## Using Templates

### Method 1: Initialize New Project

```bash
# Create .claude/project.yaml from template
python skill/scripts/init_project.py --template spring-boot

# Customize base_package
python skill/scripts/init_project.py --template spring-boot \
  --base-package com.mycompany.myapp
```

### Method 2: Manual Configuration

Create `.claude/project.yaml`:

```yaml
project_type: spring-boot  # Or django, react
language: java              # Or python, javascript
version: "1.0"

# Load template structure
# Template will be loaded from skill/templates/java/spring-boot.yaml
```

### Method 3: Hierarchical Configuration

For multi-module projects:

```
my-project/
├── .claude/project.yaml          # Root: common settings
├── backend/
│   └── .claude/project.yaml      # Uses spring-boot template
└── frontend/
    └── .claude/project.yaml      # Uses react template
```

---

## Creating Custom Templates

### Template File Structure

Templates are YAML files in `skill/templates/{language}/`:

```yaml
project_type: my-template
language: java
version: "1.0"

structure:
  custom_type:
    path: "src/main/java/{package}/custom"
    naming: "{Name}Custom.java"
    test_path: "src/test/java/{package}/custom"
    generate_test: true

annotations:
  custom_type:
    - "@CustomAnnotation"

imports:
  custom_type:
    - "com.example.CustomClass"
```

### Example: Custom Spring Boot Template

Create `skill/templates/java/my-spring-boot.yaml`:

```yaml
project_type: my-spring-boot
language: java
version: "1.0"

# Custom package structure
structure:
  api_handler:
    path: "src/main/java/{package}/api/handler"
    naming: "{Name}Handler.java"
    test_path: "src/test/java/{package}/api/handler"
    generate_test: true

  domain_entity:
    path: "src/main/java/{package}/domain/entity"
    naming: "{Name}Entity.java"

# Custom annotations
annotations:
  api_handler:
    - "@ApiHandler"
    - "@Validated"

imports:
  api_handler:
    - "com.example.annotation.ApiHandler"
    - "org.springframework.validation.annotation.Validated"
```

Use it:
```bash
python skill/scripts/init_project.py --template my-spring-boot
```

---

## Template Validation

### Check Available Templates

```bash
python skill/scripts/template_loader.py
```

### Validate Template

```bash
python skill/scripts/template_loader.py spring-boot
```

### Validate Project Configuration

```bash
python skill/scripts/validate_config.py /path/to/project
```

---

## Summary

### Currently Available (3 templates)

✅ **spring-boot** - Java Spring Boot (10 file types)
✅ **django** - Python Django (12 file types)
✅ **react** - JavaScript React (11 file types)

### Template Capabilities

- ✅ Language-specific code generation
- ✅ Framework-specific annotations and imports
- ✅ Auto-generate test files
- ✅ Additional files (CSS, types, etc.)
- ✅ Template variables ({Name}, {name}, {package}, {app})
- ✅ Custom template creation support
- ✅ Hierarchical configuration (multiple templates per project)

### Next Steps

1. Choose a template for your project type
2. Initialize with `init_project.py --template <name>`
3. Customize `.claude/project.yaml` if needed
4. Generate files with `file_generator.py`

For detailed template documentation, see [docs/templates.md](templates.md).