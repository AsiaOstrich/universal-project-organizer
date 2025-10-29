# Template System Specification

## ADDED Requirements

### Requirement: Template File Structure

The system SHALL provide pre-built YAML template files for common project types stored in `skill/templates/{language}/{framework}.yaml`.

#### Scenario: Template files are organized by language and framework

- **WHEN** templates are stored in the templates directory
- **THEN** templates SHALL be organized in subdirectories by language (java, python, javascript, go)
- **AND** each template file SHALL be named after the framework (spring-boot.yaml, django.yaml, react.yaml)

#### Scenario: Template discovery

- **WHEN** the system needs to list available templates
- **THEN** the system SHALL scan the templates directory structure
- **AND** the system SHALL return a list of available language/framework combinations

### Requirement: Spring Boot Template

The system SHALL provide a Spring Boot template with structure definitions for common Java file types.

#### Scenario: Spring Boot service file structure

- **WHEN** a Spring Boot template is loaded
- **THEN** the template SHALL define paths for service classes (src/main/java/{package}/service)
- **AND** the template SHALL define naming convention ({Name}Service.java)
- **AND** the template SHALL specify test file generation in src/test/java/{package}/service

#### Scenario: Spring Boot controller file structure

- **WHEN** a Spring Boot template is loaded
- **THEN** the template SHALL define paths for REST controllers (src/main/java/{package}/controller)
- **AND** the template SHALL define naming convention ({Name}Controller.java)
- **AND** the template SHALL include common Spring annotations in the structure

#### Scenario: Spring Boot repository and model structures

- **WHEN** a Spring Boot template is loaded
- **THEN** the template SHALL define repository paths (src/main/java/{package}/repository)
- **AND** the template SHALL define model/entity paths (src/main/java/{package}/model)
- **AND** the template SHALL include appropriate naming conventions for each

### Requirement: Django Template

The system SHALL provide a Django template with structure definitions for Django app-based organization.

#### Scenario: Django model file structure

- **WHEN** a Django template is loaded
- **THEN** the template SHALL define model paths using the pattern `{app}/models.py`
- **AND** the template SHALL support adding classes to existing files
- **AND** the template SHALL use Python naming conventions (PascalCase for classes)

#### Scenario: Django view file structure

- **WHEN** a Django template is loaded
- **THEN** the template SHALL define view paths ({app}/views.py)
- **AND** the template SHALL define serializer paths ({app}/serializers.py)
- **AND** the template SHALL support function-based and class-based views

#### Scenario: Django test structure

- **WHEN** a Django template is loaded
- **THEN** the template SHALL define test paths ({app}/tests/test_{module}.py)
- **AND** the template SHALL use Django test case naming conventions

### Requirement: React Template

The system SHALL provide a React template with structure definitions for component-based architecture.

#### Scenario: React component file structure

- **WHEN** a React template is loaded
- **THEN** the template SHALL define component paths (src/components/{Name})
- **AND** the template SHALL define main file naming ({Name}.jsx or {Name}.tsx)
- **AND** the template SHALL support related files (CSS modules, tests)

#### Scenario: React additional file generation

- **WHEN** a React component is generated
- **THEN** the template SHALL specify related files to create
- **AND** the system SHALL generate {Name}.module.css for styles
- **AND** the system SHALL generate {Name}.test.jsx for tests

#### Scenario: React hooks and pages

- **WHEN** a React template is loaded
- **THEN** the template SHALL define hook paths (src/hooks) with use{Name}.js naming
- **AND** the template SHALL define page paths (src/pages/{Name})
- **AND** the template SHALL define utility paths (src/utils)

### Requirement: Template Loading and Parsing

The system SHALL load and parse template files into usable configuration objects.

#### Scenario: Load template by project type

- **WHEN** given a project_type identifier (e.g., "spring-boot")
- **THEN** the system SHALL locate the corresponding template file
- **AND** the system SHALL parse the YAML content
- **AND** the system SHALL return a structured template object

#### Scenario: Template not found

- **WHEN** a requested template does not exist
- **THEN** the system SHALL provide a clear error message
- **AND** the system SHALL list available templates
- **AND** the system SHALL suggest the closest matching template if applicable

#### Scenario: Invalid template format

- **WHEN** a template file has invalid YAML or missing required fields
- **THEN** the system SHALL report the template as invalid
- **AND** the system SHALL specify what is wrong with the template
- **AND** the system SHALL prevent the template from being used

### Requirement: Template Application

The system SHALL apply templates to initialize project configurations.

#### Scenario: Initialize project with template

- **WHEN** a user initializes a project with a specific template
- **THEN** the system SHALL copy the template structure to `.claude/project.yaml`
- **AND** the system SHALL substitute project-specific values (e.g., package names)
- **AND** the system SHALL preserve all file type definitions from the template

#### Scenario: Customize template during initialization

- **WHEN** a user provides custom values during initialization (e.g., base package)
- **THEN** the system SHALL substitute these values in the template
- **AND** the system SHALL validate the customized configuration
- **AND** the system SHALL save the customized configuration to the project

#### Scenario: Template reuse

- **WHEN** multiple projects use the same template
- **THEN** each project SHALL have an independent configuration file
- **AND** changes to one project's configuration SHALL NOT affect others
- **AND** the original template SHALL remain unmodified

### Requirement: Template Validation

The system SHALL validate that templates conform to the expected structure and conventions.

#### Scenario: Valid template structure

- **WHEN** a template is validated
- **THEN** the system SHALL check for required fields (project_type, language, structure)
- **AND** the system SHALL verify path templates use valid variable syntax
- **AND** the system SHALL confirm naming conventions are present

#### Scenario: Template with missing structure definitions

- **WHEN** a template is missing key structure definitions for the project type
- **THEN** the system SHALL warn about incomplete template
- **AND** the system SHALL list the recommended structure types for that project type
- **AND** the system SHALL still allow the template to be used if minimally valid

### Requirement: Template Documentation

Each template SHALL include inline documentation explaining its structure and usage.

#### Scenario: Template with usage comments

- **WHEN** a template file is viewed
- **THEN** the template SHALL include comments explaining each structure section
- **AND** the template SHALL provide examples of variable usage
- **AND** the template SHALL document optional vs required sections

#### Scenario: Template examples

- **WHEN** a user needs to understand a template
- **THEN** the system SHALL provide example usage in the template file itself
- **AND** the system SHALL include sample values for common customizations
- **AND** the system SHALL reference documentation for complex scenarios