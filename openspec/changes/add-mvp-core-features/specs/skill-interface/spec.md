# Skill Interface Specification

## ADDED Requirements

### Requirement: Skill File Structure

The skill SHALL be defined in `skill/SKILL.md` following the Claude Skills format.

#### Scenario: Skill metadata

- **WHEN** Claude loads the skill
- **THEN** the skill file SHALL include frontmatter with name, description, and license
- **AND** the name SHALL be "universal-project-organizer"
- **AND** the description SHALL explain when to use the skill

#### Scenario: Skill documentation

- **WHEN** a user or Claude reads the skill file
- **THEN** the skill SHALL include clear usage instructions
- **AND** the skill SHALL document supported project types
- **AND** the skill SHALL provide examples of common requests

### Requirement: Skill Invocation Patterns

The skill SHALL recognize and respond to natural language requests for file generation.

#### Scenario: Service creation request

- **WHEN** the user says "Create a UserService" or "Create a service called UserService"
- **THEN** the skill SHALL activate
- **AND** the skill SHALL identify the file type as "service"
- **AND** the skill SHALL proceed with file generation workflow

#### Scenario: Controller creation request

- **WHEN** the user says "Generate a UserController" or "Create a controller for users"
- **THEN** the skill SHALL activate
- **AND** the skill SHALL identify the file type as "controller"
- **AND** the skill SHALL extract the name "User" or "users"

#### Scenario: Component creation request

- **WHEN** the user says "Create a LoginForm component" or "Generate a component called LoginForm"
- **THEN** the skill SHALL activate
- **AND** the skill SHALL identify the file type as "component"
- **AND** the skill SHALL handle framework-specific component generation

#### Scenario: Model or entity creation request

- **WHEN** the user says "Create a User model" or "Generate an entity for products"
- **THEN** the skill SHALL activate
- **AND** the skill SHALL identify the file type as "model" or "entity"
- **AND** the skill SHALL handle database-related file generation

### Requirement: Configuration Loading Workflow

The skill SHALL load and validate the project configuration before generating files.

#### Scenario: Configuration exists and is valid

- **WHEN** the skill is invoked for file generation
- **THEN** the skill SHALL read `.claude/project.yaml` from the project root
- **AND** the skill SHALL validate the configuration structure
- **AND** the skill SHALL proceed with file generation using the configuration

#### Scenario: Configuration missing

- **WHEN** the skill is invoked but `.claude/project.yaml` does not exist
- **THEN** the skill SHALL inform the user the project is not initialized
- **AND** the skill SHALL offer to initialize the project with a template
- **AND** the skill SHALL list available templates (Spring Boot, Django, React)

#### Scenario: Configuration invalid

- **WHEN** the skill reads a configuration with errors
- **THEN** the skill SHALL report the validation errors
- **AND** the skill SHALL not proceed with file generation
- **AND** the skill SHALL suggest using the validation utility to fix errors

### Requirement: File Type Identification

The skill SHALL determine the correct file type from the user's request and match it to the configuration.

#### Scenario: Direct file type mention

- **WHEN** the user explicitly mentions a file type (e.g., "service", "controller")
- **THEN** the skill SHALL look up that file type in the configuration
- **AND** the skill SHALL use the corresponding structure definition

#### Scenario: Inferred file type from name

- **WHEN** the user provides a name that implies a file type (e.g., "UserController" implies controller)
- **THEN** the skill SHALL infer the file type from naming patterns
- **AND** the skill SHALL verify the inferred type exists in the configuration

#### Scenario: File type not found in configuration

- **WHEN** the identified file type is not defined in the project configuration
- **THEN** the skill SHALL inform the user that this file type is not configured
- **AND** the skill SHALL list the available file types from the configuration
- **AND** the skill SHALL suggest updating the configuration if needed

### Requirement: User Confirmation and Interaction

The skill SHALL interact with users to confirm actions and gather missing information.

#### Scenario: Confirm file creation

- **WHEN** the skill is ready to create a file
- **THEN** the skill SHALL show the user the target path
- **AND** the skill SHALL ask for confirmation before creating the file
- **AND** the skill SHALL only create the file if the user confirms

#### Scenario: Request missing information

- **WHEN** the skill needs information not provided in the request (e.g., app name for Django)
- **THEN** the skill SHALL ask the user for the missing information
- **AND** the skill SHALL provide context about why the information is needed
- **AND** the skill SHALL validate the provided information

#### Scenario: Handle existing files

- **WHEN** the target file already exists
- **THEN** the skill SHALL notify the user of the conflict
- **AND** the skill SHALL offer options: overwrite, skip, or rename
- **AND** the skill SHALL only proceed based on the user's choice

### Requirement: File Generation Orchestration

The skill SHALL orchestrate the complete file generation workflow from request to file creation.

#### Scenario: Complete file generation workflow

- **WHEN** all prerequisites are met (valid config, confirmed path, user approval)
- **THEN** the skill SHALL resolve the full file path
- **AND** the skill SHALL generate appropriate file content
- **AND** the skill SHALL create the file at the target location
- **AND** the skill SHALL generate any related files (tests, etc.)
- **AND** the skill SHALL report success with the created file paths

#### Scenario: Workflow with multiple files

- **WHEN** configuration specifies related files (e.g., component + CSS + test)
- **THEN** the skill SHALL generate all specified files
- **AND** the skill SHALL ensure all files are created successfully
- **AND** the skill SHALL report all created files to the user

#### Scenario: Workflow failure handling

- **WHEN** any step in the workflow fails
- **THEN** the skill SHALL stop further file generation
- **AND** the skill SHALL report the specific failure
- **AND** the skill SHALL not leave partial or incomplete files

### Requirement: Error Handling and Recovery

The skill SHALL handle errors gracefully and provide actionable guidance.

#### Scenario: Recoverable error with suggestion

- **WHEN** an error occurs that the user can fix (e.g., invalid configuration)
- **THEN** the skill SHALL explain the error clearly
- **AND** the skill SHALL suggest specific corrective actions
- **AND** the skill SHALL allow the user to retry after fixing the issue

#### Scenario: Unrecoverable error

- **WHEN** an error occurs that cannot be recovered (e.g., permission denied)
- **THEN** the skill SHALL explain the error and its cause
- **AND** the skill SHALL not attempt to continue the workflow
- **AND** the skill SHALL suggest alternative approaches if available

#### Scenario: Error logging

- **WHEN** any error occurs
- **THEN** the skill SHALL log sufficient details for debugging
- **AND** the skill SHALL include context (configuration path, requested file, etc.)
- **AND** the skill SHALL avoid exposing sensitive information in error messages

### Requirement: Project Initialization Support

The skill SHALL support initializing new projects with configuration templates.

#### Scenario: Initialize with template selection

- **WHEN** the user says "Initialize this as a Spring Boot project"
- **THEN** the skill SHALL load the Spring Boot template
- **AND** the skill SHALL ask for project-specific values (e.g., base package)
- **AND** the skill SHALL create `.claude/project.yaml` with the configured template

#### Scenario: Initialize with auto-detection

- **WHEN** the user says "Initialize this project" without specifying a type
- **THEN** the skill SHALL attempt to detect the project type (by checking for pom.xml, manage.py, package.json)
- **AND** the skill SHALL suggest the detected type to the user
- **AND** the skill SHALL allow the user to confirm or choose a different type

#### Scenario: Initialize existing configuration

- **WHEN** the user tries to initialize but `.claude/project.yaml` already exists
- **THEN** the skill SHALL inform the user that the project is already initialized
- **AND** the skill SHALL show the current configuration
- **AND** the skill SHALL offer to validate or update the existing configuration

### Requirement: Skill Tool Integration

The skill SHALL effectively use Claude Code tools (Read, Write, Glob, Grep) for file operations.

#### Scenario: Read configuration file

- **WHEN** the skill needs to load the configuration
- **THEN** the skill SHALL use the Read tool to read `.claude/project.yaml`
- **AND** the skill SHALL handle cases where the file does not exist

#### Scenario: Write generated files

- **WHEN** the skill generates a file
- **THEN** the skill SHALL use the Write tool to create the file
- **AND** the skill SHALL provide the full absolute path and content

#### Scenario: Check for existing files

- **WHEN** the skill needs to check if a file exists
- **THEN** the skill SHALL use the Glob tool to check for the file path
- **AND** the skill SHALL interpret the results correctly

#### Scenario: Search for project markers

- **WHEN** the skill needs to detect project type
- **THEN** the skill SHALL use the Glob tool to search for marker files (pom.xml, package.json, etc.)
- **AND** the skill SHALL identify the project type based on found markers

### Requirement: User Feedback and Reporting

The skill SHALL provide clear, helpful feedback throughout the workflow.

#### Scenario: Progress updates

- **WHEN** the skill is performing multi-step operations
- **THEN** the skill SHALL inform the user of progress
- **AND** the skill SHALL indicate which step is currently executing

#### Scenario: Success summary

- **WHEN** file generation completes successfully
- **THEN** the skill SHALL provide a summary of what was created
- **AND** the skill SHALL list all file paths with clickable links (if supported)
- **AND** the skill SHALL indicate any next steps or related actions

#### Scenario: Helpful guidance

- **WHEN** the user might need additional information
- **THEN** the skill SHALL proactively offer relevant tips
- **AND** the skill SHALL reference documentation when appropriate
- **AND** the skill SHALL avoid overwhelming the user with too much information