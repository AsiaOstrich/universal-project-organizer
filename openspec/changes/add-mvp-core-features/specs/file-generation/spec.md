# File Generation Specification

## ADDED Requirements

### Requirement: Path Resolution

The system SHALL resolve file paths by substituting template variables with actual values based on user input and configuration.

#### Scenario: Substitute Name variable

- **WHEN** a path template contains `{Name}` and the user requests a file named "User"
- **THEN** the system SHALL substitute {Name} with "User" in the path
- **AND** the system SHALL preserve the case as provided by the user

#### Scenario: Substitute package variable

- **WHEN** a path template contains `{package}` for a Java project with base_package "com.example.app"
- **THEN** the system SHALL substitute {package} with "com/example/app"
- **AND** the system SHALL convert dots to path separators

#### Scenario: Substitute app variable

- **WHEN** a path template contains `{app}` for a Django project
- **THEN** the system SHALL prompt the user for the app name if not provided
- **AND** the system SHALL substitute {app} with the user-provided app name

#### Scenario: Multiple variables in one path

- **WHEN** a path template contains multiple variables (e.g., "{app}/models/{Name}.py")
- **THEN** the system SHALL substitute all variables in the correct order
- **AND** the system SHALL handle missing variables by prompting the user or using defaults

#### Scenario: Relative path resolution

- **WHEN** a path template is relative (e.g., "src/main/java/{package}/service")
- **THEN** the system SHALL resolve the path from the project root directory
- **AND** the system SHALL create the full absolute path

### Requirement: File Type Detection

The system SHALL identify the type of file to generate based on user requests and configuration.

#### Scenario: Explicit file type from user request

- **WHEN** the user says "Create a service called UserService"
- **THEN** the system SHALL identify the file type as "service"
- **AND** the system SHALL look up the service structure in the configuration

#### Scenario: Implicit file type from naming

- **WHEN** the user says "Create UserController" and the name ends with "Controller"
- **THEN** the system SHALL infer the file type as "controller"
- **AND** the system SHALL verify this type exists in the configuration

#### Scenario: Ambiguous file type

- **WHEN** the user request does not clearly specify a file type
- **THEN** the system SHALL ask the user to clarify the intended file type
- **AND** the system SHALL list available file types from the configuration

#### Scenario: Unknown file type

- **WHEN** the user requests a file type not defined in the configuration
- **THEN** the system SHALL inform the user the type is not configured
- **AND** the system SHALL suggest adding it to the configuration or using a different type

### Requirement: File Content Generation

The system SHALL generate appropriate file content based on the project type, file type, and naming conventions.

#### Scenario: Generate Java class with package declaration

- **WHEN** generating a Java file in a Spring Boot project
- **THEN** the file SHALL include the correct package declaration based on the path
- **AND** the file SHALL include a basic class definition with the correct name
- **AND** the file SHALL use proper Java naming conventions (PascalCase for classes)

#### Scenario: Generate with framework-specific annotations

- **WHEN** generating a Spring Boot service
- **THEN** the file SHALL include `@Service` annotation
- **WHEN** generating a Spring Boot controller
- **THEN** the file SHALL include `@RestController` annotation
- **AND** common imports for the framework SHALL be included

#### Scenario: Generate Python class file

- **WHEN** generating a Python file for Django
- **THEN** the file SHALL include appropriate imports (e.g., from django.db import models)
- **AND** the file SHALL include a basic class definition following Python conventions
- **AND** the file SHALL use proper indentation (4 spaces)

#### Scenario: Generate React component file

- **WHEN** generating a React component
- **THEN** the file SHALL include a functional component template
- **AND** the file SHALL include necessary imports (React)
- **AND** the file SHALL export the component as default

### Requirement: Related File Generation

The system SHALL generate related files (such as test files) when configured to do so.

#### Scenario: Generate test file for Java service

- **WHEN** generating a service file and generate_test is true in configuration
- **THEN** the system SHALL also generate a corresponding test file
- **AND** the test file SHALL be placed in the test path specified in configuration
- **AND** the test file SHALL include basic test structure with correct naming

#### Scenario: Generate multiple related files for React component

- **WHEN** generating a React component with additional_files configured
- **THEN** the system SHALL generate the main component file
- **AND** the system SHALL generate the CSS module file
- **AND** the system SHALL generate the test file
- **AND** all files SHALL be placed in the component directory

#### Scenario: Skip related file generation when disabled

- **WHEN** generate_test is false or not specified in configuration
- **THEN** the system SHALL only generate the main file
- **AND** the system SHALL not generate test files

### Requirement: File System Operations

The system SHALL perform file system operations safely and with proper error handling.

#### Scenario: Create directories as needed

- **WHEN** generating a file in a path where parent directories do not exist
- **THEN** the system SHALL create all necessary parent directories
- **AND** the system SHALL set appropriate permissions on created directories

#### Scenario: Check for existing files

- **WHEN** generating a file that already exists at the target path
- **THEN** the system SHALL detect the existing file
- **AND** the system SHALL ask the user whether to overwrite, skip, or rename
- **AND** the system SHALL not overwrite without explicit user confirmation

#### Scenario: Handle permission errors

- **WHEN** attempting to write to a location without proper permissions
- **THEN** the system SHALL catch the permission error
- **AND** the system SHALL provide a clear error message
- **AND** the system SHALL suggest checking file permissions or using a different location

#### Scenario: Atomic file writes

- **WHEN** writing file content
- **THEN** the system SHALL write to a temporary file first
- **AND** the system SHALL move the temporary file to the final location only on success
- **AND** the system SHALL handle failures without leaving corrupted or partial files

### Requirement: Cross-Platform File Operations

The system SHALL generate files correctly on different operating systems.

#### Scenario: Normalize path separators

- **WHEN** generating files on Windows
- **THEN** the system SHALL use backslash path separators
- **WHEN** generating files on Unix-like systems
- **THEN** the system SHALL use forward slash path separators

#### Scenario: Handle file encoding

- **WHEN** writing file content
- **THEN** the system SHALL use UTF-8 encoding by default
- **AND** the system SHALL handle Unicode characters correctly
- **AND** the system SHALL respect platform-specific line endings

### Requirement: User Feedback During Generation

The system SHALL provide clear feedback about file generation progress and results.

#### Scenario: Success feedback

- **WHEN** a file is successfully generated
- **THEN** the system SHALL display a success message
- **AND** the message SHALL include the full path of the created file
- **AND** the message SHALL list any related files that were also created

#### Scenario: Failure feedback

- **WHEN** file generation fails
- **THEN** the system SHALL display a clear error message
- **AND** the message SHALL explain why the generation failed
- **AND** the message SHALL suggest corrective actions

#### Scenario: Dry-run mode

- **WHEN** the user requests a dry-run (preview mode)
- **THEN** the system SHALL show what files would be created
- **AND** the system SHALL display the paths and basic structure
- **AND** the system SHALL not actually create any files

### Requirement: Naming Convention Application

The system SHALL apply configured naming conventions when generating files.

#### Scenario: Apply case transformation

- **WHEN** a naming convention specifies PascalCase
- **THEN** the system SHALL convert the provided name to PascalCase (e.g., "user service" → "UserService")
- **WHEN** a naming convention specifies snake_case
- **THEN** the system SHALL convert the name to snake_case (e.g., "UserService" → "user_service")

#### Scenario: Apply prefix/suffix patterns

- **WHEN** a naming convention specifies a pattern like "{Name}Service.java"
- **THEN** the system SHALL append "Service" suffix to the name
- **AND** the system SHALL add ".java" file extension
- **AND** the system SHALL not duplicate suffixes if the user already included them

#### Scenario: Respect user-provided exact names

- **WHEN** the user provides a name that already follows conventions
- **THEN** the system SHALL use the name as-is without modification
- **AND** the system SHALL not force unnecessary transformations