"""
Configuration Parser for Universal Project Organizer

This module provides functionality to read, parse, and validate
.claude/project.yaml configuration files.

Usage:
    from skill.scripts.config_parser import load_config, ConfigError

    try:
        config = load_config("/path/to/project")
        print(f"Project type: {config['project_type']}")
    except ConfigError as e:
        print(f"Configuration error: {e}")
"""

import yaml
from pathlib import Path
from typing import Dict, Any, List, Optional, Union


class ConfigError(Exception):
    """Exception raised for configuration-related errors."""
    pass


class ConfigParser:
    """Parser for project configuration files."""

    # Required fields in configuration
    REQUIRED_FIELDS = ['project_type', 'language', 'structure']

    # Supported project types
    SUPPORTED_PROJECT_TYPES = [
        'spring-boot', 'maven', 'django', 'flask', 'fastapi',
        'react', 'nextjs', 'vue', 'express', 'go'
    ]

    # Supported languages
    SUPPORTED_LANGUAGES = [
        'java', 'python', 'javascript', 'typescript', 'go'
    ]

    # Supported template variables
    SUPPORTED_VARIABLES = ['{Name}', '{name}', '{package}', '{app}']

    def __init__(self, project_root: Path):
        """
        Initialize the configuration parser.

        Args:
            project_root: Path to the project root directory
        """
        self.project_root = Path(project_root)
        self.config_path = self.project_root / ".claude" / "project.yaml"

    def load(self) -> Dict[str, Any]:
        """
        Load and parse the configuration file.

        Returns:
            Parsed configuration as a dictionary

        Raises:
            ConfigError: If configuration file is missing, invalid, or malformed
        """
        # Check if configuration file exists
        if not self.config_path.exists():
            raise ConfigError(
                f"Configuration file not found: {self.config_path}\n\n"
                f"Please initialize the project with a template:\n"
                f"  python skill/scripts/init_project.py --template <template-name>\n\n"
                f"Available templates: {', '.join(self.SUPPORTED_PROJECT_TYPES)}"
            )

        # Read and parse YAML file
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise ConfigError(
                f"Invalid YAML syntax in {self.config_path}\n\n"
                f"Error: {str(e)}\n\n"
                f"Common YAML issues:\n"
                f"  - Incorrect indentation (use spaces, not tabs)\n"
                f"  - Missing colon after key\n"
                f"  - Unquoted strings with special characters"
            )
        except Exception as e:
            raise ConfigError(
                f"Failed to read configuration file: {self.config_path}\n"
                f"Error: {str(e)}"
            )

        # Validate configuration
        self.validate(config)

        return config

    def validate(self, config: Dict[str, Any]) -> None:
        """
        Validate the configuration structure and content.

        Args:
            config: Configuration dictionary to validate

        Raises:
            ConfigError: If validation fails
        """
        if config is None:
            raise ConfigError("Configuration file is empty")

        # Check required fields
        missing_fields = [
            field for field in self.REQUIRED_FIELDS
            if field not in config
        ]

        if missing_fields:
            raise ConfigError(
                f"Missing required field(s): {', '.join(missing_fields)}\n\n"
                f"Required fields:\n" +
                '\n'.join(f"  - {field}" for field in self.REQUIRED_FIELDS) +
                f"\n\nPlease add the missing fields to {self.config_path}"
            )

        # Validate project_type
        project_type = config.get('project_type')
        if project_type not in self.SUPPORTED_PROJECT_TYPES:
            raise ConfigError(
                f"Unsupported project_type: '{project_type}'\n\n"
                f"Supported project types:\n" +
                '\n'.join(f"  - {pt}" for pt in self.SUPPORTED_PROJECT_TYPES)
            )

        # Validate language
        language = config.get('language')
        if language not in self.SUPPORTED_LANGUAGES:
            raise ConfigError(
                f"Unsupported language: '{language}'\n\n"
                f"Supported languages:\n" +
                '\n'.join(f"  - {lang}" for lang in self.SUPPORTED_LANGUAGES)
            )

        # Validate structure
        structure = config.get('structure')
        if not isinstance(structure, dict):
            raise ConfigError(
                f"'structure' must be an object/dictionary\n"
                f"Got: {type(structure).__name__}"
            )

        if not structure:
            raise ConfigError(
                "structure' cannot be empty\n"
                f"Please define at least one file type structure"
            )

        # Validate each structure entry
        for file_type, file_config in structure.items():
            self._validate_structure_entry(file_type, file_config)

    def _validate_structure_entry(
        self,
        file_type: str,
        file_config: Dict[str, Any]
    ) -> None:
        """
        Validate a single structure entry.

        Args:
            file_type: Name of the file type (e.g., 'service', 'controller')
            file_config: Configuration for this file type

        Raises:
            ConfigError: If validation fails
        """
        if not isinstance(file_config, dict):
            raise ConfigError(
                f"structure.{file_type} must be an object/dictionary\n"
                f"Got: {type(file_config).__name__}"
            )

        # Check required fields in structure entry
        if 'path' not in file_config:
            raise ConfigError(
                f"structure.{file_type} is missing required field 'path'"
            )

        if 'naming' not in file_config:
            raise ConfigError(
                f"structure.{file_type} is missing required field 'naming'"
            )

        # Validate path template
        path = file_config['path']
        if not isinstance(path, str) or not path.strip():
            raise ConfigError(
                f"structure.{file_type}.path must be a non-empty string"
            )

        # Validate naming template
        naming = file_config['naming']
        if not isinstance(naming, str) or not naming.strip():
            raise ConfigError(
                f"structure.{file_type}.naming must be a non-empty string"
            )

        # Check if naming template includes at least one variable
        has_variable = any(var in naming for var in self.SUPPORTED_VARIABLES)
        if not has_variable:
            # Warning, not error - some cases might not need variables
            pass

        # Validate optional fields
        if 'generate_test' in file_config:
            if not isinstance(file_config['generate_test'], bool):
                raise ConfigError(
                    f"structure.{file_type}.generate_test must be a boolean (true/false)"
                )

        if 'additional_files' in file_config:
            if not isinstance(file_config['additional_files'], list):
                raise ConfigError(
                    f"structure.{file_type}.additional_files must be a list"
                )

    def get_file_type_config(
        self,
        config: Dict[str, Any],
        file_type: str
    ) -> Optional[Dict[str, Any]]:
        """
        Get configuration for a specific file type.

        Args:
            config: Full configuration dictionary
            file_type: Name of the file type (e.g., 'service', 'controller')

        Returns:
            Configuration for the file type, or None if not found
        """
        return config.get('structure', {}).get(file_type)

    def list_file_types(self, config: Dict[str, Any]) -> List[str]:
        """
        List all file types defined in the configuration.

        Args:
            config: Full configuration dictionary

        Returns:
            List of file type names
        """
        return list(config.get('structure', {}).keys())


def load_config(project_root: Union[str, Path]) -> Dict[str, Any]:
    """
    Load and parse project configuration.

    This is a convenience function that creates a ConfigParser
    and loads the configuration.

    Args:
        project_root: Path to the project root directory

    Returns:
        Parsed configuration dictionary

    Raises:
        ConfigError: If configuration is missing, invalid, or malformed

    Example:
        >>> config = load_config("/path/to/project")
        >>> print(config['project_type'])
        'spring-boot'
    """
    parser = ConfigParser(Path(project_root))
    return parser.load()


def validate_config(project_root: Union[str, Path]) -> None:
    """
    Validate project configuration without loading it into memory.

    Args:
        project_root: Path to the project root directory

    Raises:
        ConfigError: If validation fails

    Example:
        >>> try:
        ...     validate_config("/path/to/project")
        ...     print("✓ Configuration is valid")
        ... except ConfigError as e:
        ...     print(f"✗ {e}")
    """
    parser = ConfigParser(Path(project_root))
    parser.load()  # Load performs validation


if __name__ == "__main__":
    # Simple CLI for testing
    import sys

    if len(sys.argv) > 1:
        project_path = sys.argv[1]
    else:
        project_path = "."

    try:
        config = load_config(project_path)
        print("✓ Configuration loaded successfully")
        print(f"\nProject type: {config['project_type']}")
        print(f"Language: {config['language']}")
        print(f"File types: {', '.join(config['structure'].keys())}")
    except ConfigError as e:
        print(f"✗ Configuration Error:\n{e}")
        sys.exit(1)