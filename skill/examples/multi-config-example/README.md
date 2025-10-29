# Multi-Configuration Example

This example demonstrates **hierarchical configuration** with priority order and conflict resolution.

## Directory Structure

```
multi-config-example/
├── .claude/
│   └── project.yaml          ← Level 1: Root config (Lowest Priority)
├── backend/
│   ├── .claude/
│   │   └── project.yaml      ← Level 2: Backend config (Medium Priority)
│   └── user-service/
│       └── .claude/
│           └── project.yaml  ← Level 3: Service config (Highest Priority)
└── README.md
```

## Configuration Priority Order

### Rule: **Child Overrides Parent**

When working in `backend/user-service/`:

```
Priority (Highest to Lowest):
1. user-service/.claude/project.yaml  ← WINS conflicts
2. backend/.claude/project.yaml       ← Overridden by #1
3. .claude/project.yaml (root)        ← Overridden by #1 and #2
```

## How Configuration Merging Works

### Example 1: Scalar Values (Simple Override)

**Root config** (Level 1):
```yaml
base_package: com.example.app
```

**Backend config** (Level 2):
```yaml
base_package: com.example.backend  # Overrides root
```

**User-service config** (Level 3):
```yaml
base_package: com.example.backend.user  # Overrides backend
```

**Result**: `base_package = "com.example.backend.user"` ✅

---

### Example 2: Structure Merging (Additive)

**Root config** (Level 1):
```yaml
structure:
  config:
    path: "config"
    naming: "{name}.yaml"
```

**Backend config** (Level 2):
```yaml
structure:
  service:
    path: "src/main/java/{package}/service"
    naming: "{Name}Service.java"
  controller:
    path: "src/main/java/{package}/controller"
    naming: "{Name}Controller.java"
```

**User-service config** (Level 3):
```yaml
structure:
  event_handler:
    path: "src/main/java/{package}/handler"
    naming: "{Name}Handler.java"
  dto:
    path: "src/main/java/{package}/dto"
    naming: "{Name}DTO.java"
```

**Result**: All file types are **merged** ✅
```yaml
structure:
  config:         # From root
  service:        # From backend
  controller:     # From backend
  event_handler:  # From user-service
  dto:            # From user-service
```

---

### Example 3: Structure Override (Same Key)

**Backend config** (Level 2):
```yaml
structure:
  service:
    path: "src/main/java/{package}/service"
    naming: "{Name}Service.java"
    generate_test: true
```

**User-service config** (Level 3):
```yaml
structure:
  service:
    path: "src/main/java/{package}/services"  # Different path!
    custom_annotation: "@UserService"
```

**Result**: Fields are **merged**, child wins conflicts ✅
```yaml
structure:
  service:
    path: "src/main/java/{package}/services"  # Overridden by child
    naming: "{Name}Service.java"              # Inherited from parent
    generate_test: true                       # Inherited from parent
    custom_annotation: "@UserService"         # Added by child
```

---

### Example 4: Annotations/Imports (Additive)

**Backend config** (Level 2):
```yaml
annotations:
  service:
    - "@Service"
imports:
  service:
    - "org.springframework.stereotype.Service"
```

**User-service config** (Level 3):
```yaml
annotations:
  event_handler:
    - "@Component"
    - "@EventListener"
imports:
  event_handler:
    - "org.springframework.stereotype.Component"
```

**Result**: **Merged** by file type ✅
```yaml
annotations:
  service:         # From backend
    - "@Service"
  event_handler:   # From user-service
    - "@Component"
    - "@EventListener"

imports:
  service:                                    # From backend
    - "org.springframework.stereotype.Service"
  event_handler:                              # From user-service
    - "org.springframework.stereotype.Component"
```

## Testing Configuration Resolution

### View Configuration Resolution Order

```bash
python skill/scripts/config_resolver.py \
  skill/examples/multi-config-example/backend/user-service \
  --show-order
```

Output:
```
Configuration Resolution Order:
============================================================
1. Level 1: .../multi-config-example
   project_type: N/A
   language: java
   file_types: config

2. Level 2: .../multi-config-example/backend
   project_type: spring-boot
   language: java
   file_types: service, controller, repository

3. HIGHEST: .../multi-config-example/backend/user-service
   project_type: N/A
   language: N/A
   file_types: event_handler, dto
```

### View Final Merged Configuration

```bash
python skill/scripts/config_resolver.py \
  skill/examples/multi-config-example/backend/user-service
```

## Conflict Resolution Rules

### Rule 1: Child Wins Scalar Values
```yaml
# Parent
base_package: com.example.parent

# Child
base_package: com.example.child

# Result
base_package: com.example.child  ✅ Child wins
```

### Rule 2: Merge Dictionaries Recursively
```yaml
# Parent
structure:
  service:
    path: "src/service"

# Child
structure:
  service:
    naming: "{Name}.java"

# Result
structure:
  service:
    path: "src/service"      # From parent
    naming: "{Name}.java"    # From child
```

### Rule 3: Add New Keys
```yaml
# Parent
structure:
  service: {...}

# Child
structure:
  controller: {...}

# Result
structure:
  service: {...}      # From parent
  controller: {...}   # Added by child
```

### Rule 4: Extend Lists (Default)
```yaml
# Parent
tags: ["backend", "java"]

# Child
tags: ["microservice"]

# Result
tags: ["backend", "java", "microservice"]  ✅ Extended
```

### Rule 5: Replace Lists (Explicit)
```yaml
# Child with _replace flag
tags: ["microservice"]
tags_replace: true

# Result
tags: ["microservice"]  ✅ Replaced, not extended
```

## Use Cases

### Use Case 1: Monorepo with Multiple Services

```
monorepo/
├── .claude/project.yaml           # Shared conventions
├── service-a/.claude/project.yaml # Service A specifics
├── service-b/.claude/project.yaml # Service B specifics
└── service-c/.claude/project.yaml # Service C specifics
```

### Use Case 2: Layered Configuration

```
project/
├── .claude/project.yaml              # Organization standards
└── backend/
    ├── .claude/project.yaml          # Backend team standards
    └── user-module/
        └── .claude/project.yaml      # User module specifics
```

### Use Case 3: Development vs Production

```
project/
├── .claude/project.yaml              # Base config
├── dev/.claude/project.yaml          # Dev environment overrides
└── prod/.claude/project.yaml         # Prod environment overrides
```

## Best Practices

### 1. ✅ Define Common Settings at Root

Put shared conventions in the root config:
```yaml
# Root .claude/project.yaml
naming_conventions:
  class: "PascalCase"
  method: "camelCase"

defaults:
  generate_test: true
```

### 2. ✅ Override Only What Changes

Child configs should only define differences:
```yaml
# Child .claude/project.yaml
base_package: com.example.child  # Override
# naming_conventions inherited (no need to repeat)
```

### 3. ✅ Document Override Reasons

Add comments explaining why you override:
```yaml
# User service uses a different package structure
# because it's deployed as a separate microservice
base_package: com.example.backend.user
```

### 4. ✅ Use Git Boundaries

Stop config lookup at `.git` directory (project root):
```
my-project/
├── .git/                  ← Config lookup stops here
├── .claude/project.yaml   ← Root config
└── backend/
    └── .claude/project.yaml
```

### 5. ❌ Avoid Deep Nesting

Don't create unnecessary config levels:
```
❌ BAD:
project/.claude/
  backend/.claude/
    services/.claude/
      user/.claude/
        api/.claude/          ← Too deep!

✅ GOOD:
project/.claude/
  backend/.claude/
    user-service/.claude/     ← Reasonable depth
```

## Debugging Configuration Issues

### Check Which Config is Being Used

```bash
python skill/scripts/config_resolver.py <path> --show-order
```

### Find Where a Setting Comes From

```python
from config_resolver import ConfigResolver

resolver = ConfigResolver(Path('backend/user-service'))
source = resolver.get_config_source('base_package')
print(f"base_package comes from: {source}")
# Output: base_package comes from: /path/to/backend/user-service/.claude/project.yaml
```

### Common Issues

**Issue**: "Configuration not found"
- **Cause**: No `.claude/project.yaml` in current or parent directories
- **Solution**: Create a config file or check your working directory

**Issue**: "Unexpected configuration value"
- **Cause**: Parent config is overriding your changes
- **Solution**: Use `--show-order` to see resolution order

**Issue**: "Missing file type"
- **Cause**: Child config doesn't inherit parent's structure
- **Solution**: Check for YAML syntax errors preventing merge

## Summary

### Configuration Resolution = Child Overrides Parent

1. **Start** from current directory
2. **Walk up** to parent directories
3. **Collect** all `.claude/project.yaml` files
4. **Merge** from root (lowest priority) to current (highest priority)
5. **Child wins** conflicts on scalar values
6. **Merge** dictionaries and structures
7. **Extend** lists (unless marked for replacement)

### Key Benefits

✅ **DRY**: Define common settings once at root
✅ **Flexible**: Override specific settings per module
✅ **Clear**: Explicit priority order (child wins)
✅ **Composable**: Build complex configs from simple parts
✅ **Debuggable**: See exactly where each setting comes from