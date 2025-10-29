# Configuration System Specification

## ADDED Requirements

### Requirement: Configuration File Format

The system SHALL support YAML-based configuration files located at `.claude/project.yaml` in the target project root.

#### Scenario: Valid configuration file is read

- **WHEN** a `.claude/project.yaml` file exists with valid YAML syntax
- **THEN** the system SHALL parse the file successfully
- **AND** the system SHALL return a structured configuration object

#### Scenario: Missing configuration file

- **WHEN** no `.claude/project.yaml` file exists in the project
- **THEN** the system SHALL provide a clear error message
- **AND** the system SHALL suggest initializing the project with a template

#### Scenario: Invalid YAML syntax

- **WHEN** the configuration file contains invalid YAML syntax
- **THEN** the system SHALL provide a clear error message indicating the syntax error
- **AND** the system SHALL include the line number and description of the error

### Requirement: Configuration Schema

The configuration file SHALL include the following required fields:
- `project_type` (string): Identifies the framework (e.g., "spring-boot", "django", "react")
- `language` (string): Primary programming language (e.g., "java", "python", "javascript")
- `structure` (object): Maps file types to path templates and naming conventions

#### Scenario: Complete configuration with all required fields

- **WHEN** a configuration file includes project_type, language, and structure
- **THEN** the system SHALL accept the configuration as valid
- **AND** the system SHALL make all fields available for file generation

#### Scenario: Missing required field

- **WHEN** a configuration file is missing a required field
- **THEN** the system SHALL reject the configuration
- **AND** the system SHALL specify which required field is missing

#### Scenario: Optional fields are present

- **WHEN** a configuration includes optional fields like naming_conventions or auto_generate
- **THEN** the system SHALL parse and apply these optional settings
- **AND** the system SHALL use sensible defaults when optional fields are absent

### Requirement: Path Template Validation

The system SHALL validate that path templates in the structure section are well-formed and use supported variable syntax.

#### Scenario: Valid path template with variables

- **WHEN** a path template includes valid variables like `{Name}`, `{package}`, or `{app}`
- **THEN** the system SHALL accept the template
- **AND** the system SHALL be able to substitute variables during file generation

#### Scenario: Invalid path template syntax

- **WHEN** a path template contains unsupported syntax or malformed variables
- **THEN** the system SHALL reject the configuration
- **AND** the system SHALL provide guidance on correct variable syntax

#### Scenario: Absolute and relative paths

- **WHEN** a path template uses either absolute or relative paths
- **THEN** the system SHALL normalize the path appropriately
- **AND** the system SHALL resolve relative paths from the project root

### Requirement: Configuration Validation Utility

The system SHALL provide a standalone validation utility that can check configuration files for correctness.

#### Scenario: Validate command on valid configuration

- **WHEN** the validation utility is run on a valid configuration file
- **THEN** the utility SHALL report success
- **AND** the utility SHALL display a summary of the configuration

#### Scenario: Validate command on invalid configuration

- **WHEN** the validation utility is run on an invalid configuration file
- **THEN** the utility SHALL report all validation errors
- **AND** the utility SHALL provide actionable guidance for fixing each error

#### Scenario: Validate command with missing file

- **WHEN** the validation utility is run but no configuration file exists
- **THEN** the utility SHALL report the missing file
- **AND** the utility SHALL suggest initialization steps

### Requirement: Cross-Platform Path Support

The system SHALL handle file paths correctly on both Unix-like systems and Windows.

#### Scenario: Unix-style paths

- **WHEN** configuration is used on a Unix-like system (Linux, macOS)
- **THEN** the system SHALL use forward slashes for path separators
- **AND** the system SHALL generate valid Unix paths

#### Scenario: Windows-style paths

- **WHEN** configuration is used on a Windows system
- **THEN** the system SHALL use backslashes for path separators
- **AND** the system SHALL generate valid Windows paths

#### Scenario: Path normalization

- **WHEN** a configuration mixes path separator styles
- **THEN** the system SHALL normalize paths to the current platform's convention
- **AND** the system SHALL not break on mixed separators

### Requirement: Error Handling and User Feedback

The system SHALL provide clear, actionable error messages when configuration issues are encountered.

#### Scenario: Helpful error for common mistakes

- **WHEN** the configuration has a common mistake (e.g., wrong indentation, typo in field name)
- **THEN** the system SHALL identify the specific issue
- **AND** the system SHALL suggest the correct format or field name
- **AND** the system SHALL include an example of correct usage

#### Scenario: Error context information

- **WHEN** any configuration error occurs
- **THEN** the error message SHALL include the file path
- **AND** the error message SHALL include the relevant section or line number
- **AND** the error message SHALL avoid technical jargon when possible