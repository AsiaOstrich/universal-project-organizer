# Proposal: Add MVP Core Features

## Why

The Universal Project Organizer currently has documentation and OpenSpec setup, but lacks the core implementation needed to function as a Claude Skill. Users cannot yet use the skill to automatically place generated files in correct project locations.

This proposal establishes the foundational capabilities required for the MVP:
1. Configuration system to read and validate project structure definitions
2. Template system for common project types (Spring Boot, Django, React)
3. File generation logic to create files in correct locations
4. Skill interface to integrate with Claude Code

Without these core features, the project cannot deliver on its primary value proposition.

## What Changes

### New Capabilities
- **Configuration System** - Read, parse, and validate `.claude/project.yaml` files
- **Template System** - Pre-built templates for Spring Boot, Django, and React projects
- **File Generation** - Logic to generate files based on configuration and templates
- **Skill Interface** - Main `skill/SKILL.md` that orchestrates the workflow

### Implementation Components
- Configuration schema definition (YAML)
- Configuration parser and validator (Python)
- Template files for 3 project types
- File generation engine with path resolution
- Claude Skill orchestration logic
- Basic error handling and user feedback

### Non-Goals (Deferred to Later Phases)
- Auto-detection of project types
- More than 3 project templates
- Advanced validation and migration tools
- VS Code integration

## Impact

### Affected Specs
This proposal creates the initial specifications for:
- `configuration-system` - Configuration file management
- `template-system` - Project template handling
- `file-generation` - File creation and placement logic
- `skill-interface` - Claude Code integration

### Affected Code
New files to be created:
- `skill/SKILL.md` - Main skill file
- `skill/scripts/config_parser.py` - Configuration parsing
- `skill/scripts/file_generator.py` - File generation logic
- `skill/templates/java/spring-boot.yaml` - Spring Boot template
- `skill/templates/python/django.yaml` - Django template
- `skill/templates/javascript/react.yaml` - React template

### User Impact
After this change, users will be able to:
1. Initialize a project with a configuration file
2. Ask Claude to generate files (e.g., "Create a UserService")
3. Have files automatically placed in the correct location
4. Use pre-built templates for common project types

### Dependencies
- Python 3.8+ (already required)
- PyYAML library (to be added to requirements.txt)
- Existing Claude Code tools (Read, Write, Glob, etc.)

## Risks and Mitigations

### Risk: Configuration Schema Complexity
**Risk**: YAML schema might become too complex for users to understand
**Mitigation**: Keep schema simple, focus on essential fields only, provide clear examples

### Risk: Template Maintenance
**Risk**: Templates might become outdated as frameworks evolve
**Mitigation**: Start with 3 well-documented templates, version them clearly, document update process

### Risk: Path Resolution Edge Cases
**Risk**: Different operating systems and project structures might cause issues
**Mitigation**: Use pathlib for cross-platform compatibility, test on Unix and Windows paths, handle edge cases gracefully

## Success Criteria

- [ ] Configuration files can be read and validated
- [ ] All 3 templates can be applied to initialize a project
- [ ] Files can be generated in correct locations based on configuration
- [ ] Skill integrates with Claude Code and responds to user requests
- [ ] Basic error messages guide users when issues occur
- [ ] Manual testing confirms workflow works end-to-end