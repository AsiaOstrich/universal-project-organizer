#!/usr/bin/env python3
"""
Path Resolver for Universal Project Organizer

Resolves file paths and names based on templates and user input.
Handles template variable substitution and path normalization.
"""

import re
from pathlib import Path
from typing import Dict, Any, Optional, Tuple


class PathResolutionError(Exception):
    """Exception raised for path resolution errors."""
    pass


class PathResolver:
    """
    Resolves file paths and names using template configuration.

    Supports template variables:
    - {Name}: PascalCase name (e.g., UserService)
    - {name}: snake_case name (e.g., user_service)
    - {package}: Package path (e.g., com/example/demo)
    - {app}: Django app name (e.g., users)
    """

    SUPPORTED_VARIABLES = ['{Name}', '{name}', '{package}', '{app}']

    def __init__(self, config: Dict[str, Any], project_root: Optional[Path] = None):
        """
        Initialize PathResolver.

        Args:
            config: Project configuration dictionary
            project_root: Root directory of the project (default: current directory)
        """
        self.config = config
        self.project_root = project_root or Path.cwd()
        self.base_package = config.get('base_package', '')
        self.language = config.get('language', '')

    def resolve_path(
        self,
        file_type: str,
        name: str,
        app: Optional[str] = None,
        test: bool = False
    ) -> Path:
        """
        Resolve the full file path for a given file type and name.

        Args:
            file_type: Type of file (e.g., 'service', 'controller')
            name: Name for the file (can be PascalCase or snake_case)
            app: Django app name (optional, for Django projects)
            test: Whether to generate test file path

        Returns:
            Resolved absolute path

        Raises:
            PathResolutionError: If file type not found or path cannot be resolved
        """
        # Get file type configuration
        structure = self.config.get('structure', {})
        if file_type not in structure:
            available = ', '.join(structure.keys())
            raise PathResolutionError(
                f"File type '{file_type}' not found in configuration.\n"
                f"Available types: {available}"
            )

        file_config = structure[file_type]

        # Get path template
        if test:
            if 'test_path' not in file_config:
                raise PathResolutionError(
                    f"File type '{file_type}' does not support test file generation.\n"
                    f"Missing 'test_path' in configuration."
                )
            path_template = file_config['test_path']
        else:
            if 'path' not in file_config:
                raise PathResolutionError(
                    f"File type '{file_type}' is missing 'path' in configuration."
                )
            path_template = file_config['path']

        # Resolve path with variable substitution
        resolved_path = self._substitute_variables(
            path_template,
            name=name,
            app=app
        )

        # Return absolute path
        return self.project_root / resolved_path

    def resolve_filename(
        self,
        file_type: str,
        name: str,
        test: bool = False
    ) -> str:
        """
        Resolve the filename for a given file type and name.

        Args:
            file_type: Type of file (e.g., 'service', 'controller')
            name: Name for the file (can be PascalCase or snake_case)
            test: Whether to generate test filename

        Returns:
            Resolved filename

        Raises:
            PathResolutionError: If file type not found or naming pattern invalid
        """
        # Get file type configuration
        structure = self.config.get('structure', {})
        if file_type not in structure:
            raise PathResolutionError(f"File type '{file_type}' not found in configuration.")

        file_config = structure[file_type]

        # Get naming template
        if test:
            # Generate test filename based on main filename
            if 'naming' not in file_config:
                raise PathResolutionError(
                    f"File type '{file_type}' is missing 'naming' in configuration."
                )
            naming_template = file_config['naming']

            # Convert main filename to test filename
            # e.g., UserService.java -> UserServiceTest.java
            filename = self._substitute_variables(naming_template, name=name)
            filename = self._convert_to_test_filename(filename)
        else:
            if 'naming' not in file_config:
                raise PathResolutionError(
                    f"File type '{file_type}' is missing 'naming' in configuration."
                )
            naming_template = file_config['naming']
            filename = self._substitute_variables(naming_template, name=name)

        return filename

    def resolve_full_path(
        self,
        file_type: str,
        name: str,
        app: Optional[str] = None,
        test: bool = False
    ) -> Path:
        """
        Resolve the complete file path including directory and filename.

        Args:
            file_type: Type of file (e.g., 'service', 'controller')
            name: Name for the file (can be PascalCase or snake_case)
            app: Django app name (optional, for Django projects)
            test: Whether to generate test file path

        Returns:
            Complete absolute path including filename

        Raises:
            PathResolutionError: If path cannot be resolved
        """
        directory = self.resolve_path(file_type, name, app, test)
        filename = self.resolve_filename(file_type, name, test)
        return directory / filename

    def get_additional_files(
        self,
        file_type: str,
        name: str,
        directory: Path
    ) -> list[Path]:
        """
        Get additional files that should be created with the main file.

        Args:
            file_type: Type of file
            name: Name for the file
            directory: Directory where files will be created

        Returns:
            List of additional file paths
        """
        structure = self.config.get('structure', {})
        if file_type not in structure:
            return []

        file_config = structure[file_type]
        additional = file_config.get('additional_files', [])

        result = []
        for file_template in additional:
            filename = self._substitute_variables(file_template, name=name)
            result.append(directory / filename)

        return result

    def should_generate_test(self, file_type: str) -> bool:
        """
        Check if test file should be auto-generated for this file type.

        Args:
            file_type: Type of file

        Returns:
            True if test should be generated
        """
        structure = self.config.get('structure', {})
        if file_type not in structure:
            return False

        file_config = structure[file_type]
        return file_config.get('generate_test', False)

    def _substitute_variables(
        self,
        template: str,
        name: str,
        app: Optional[str] = None
    ) -> str:
        """
        Substitute template variables with actual values.

        Args:
            template: Template string with variables
            name: Name value (will be converted to PascalCase and snake_case)
            app: Optional app name for Django projects

        Returns:
            String with variables substituted
        """
        result = template

        # Convert name to different cases
        pascal_name = self._to_pascal_case(name)
        snake_name = self._to_snake_case(name)

        # Substitute {Name} - PascalCase
        result = result.replace('{Name}', pascal_name)

        # Substitute {name} - snake_case
        result = result.replace('{name}', snake_name)

        # Substitute {package} - convert dots to slashes
        if '{package}' in result:
            if not self.base_package:
                raise PathResolutionError(
                    "Template uses {package} variable but 'base_package' not configured."
                )
            package_path = self.base_package.replace('.', '/')
            result = result.replace('{package}', package_path)

        # Substitute {app} - Django app name
        if '{app}' in result:
            if not app:
                raise PathResolutionError(
                    "Template uses {app} variable but app name not provided."
                )
            result = result.replace('{app}', app)

        return result

    def _to_pascal_case(self, name: str) -> str:
        """
        Convert name to PascalCase.

        Handles:
        - snake_case: user_service -> UserService
        - kebab-case: user-service -> UserService
        - Already PascalCase: UserService -> UserService
        - camelCase: userService -> UserService
        """
        # Remove file extensions if present
        name = name.split('.')[0]

        # If contains underscore or hyphen, split and capitalize
        if '_' in name or '-' in name:
            parts = re.split(r'[_\-]', name)
            return ''.join(word.capitalize() for word in parts if word)

        # If already PascalCase, return as is
        if name and name[0].isupper():
            return name

        # If camelCase, capitalize first letter
        if name:
            return name[0].upper() + name[1:]

        return name

    def _to_snake_case(self, name: str) -> str:
        """
        Convert name to snake_case.

        Handles:
        - PascalCase: UserService -> user_service
        - camelCase: userService -> user_service
        - Already snake_case: user_service -> user_service
        """
        # Remove file extensions if present
        name = name.split('.')[0]

        # If already snake_case or kebab-case, convert to snake_case
        if '_' in name or '-' in name:
            return name.replace('-', '_').lower()

        # Convert PascalCase/camelCase to snake_case
        # Insert underscore before uppercase letters
        result = re.sub(r'(?<!^)(?=[A-Z])', '_', name)
        return result.lower()

    def _convert_to_test_filename(self, filename: str) -> str:
        """
        Convert a filename to its test equivalent.

        Examples:
        - UserService.java -> UserServiceTest.java
        - user_service.py -> test_user_service.py
        - UserComponent.jsx -> UserComponent.test.jsx
        """
        # Get file extension
        parts = filename.rsplit('.', 1)
        if len(parts) == 1:
            name, ext = filename, ''
        else:
            name, ext = parts

        # Language-specific test naming conventions
        if self.language == 'java':
            # Java: UserService.java -> UserServiceTest.java
            test_name = f"{name}Test"
        elif self.language == 'python':
            # Python: user_service.py -> test_user_service.py
            if not name.startswith('test_'):
                test_name = f"test_{name}"
            else:
                test_name = name
        elif self.language in ['javascript', 'typescript']:
            # JavaScript: UserComponent.jsx -> UserComponent.test.jsx
            if not '.test' in name and not '.spec' in name:
                test_name = f"{name}.test"
            else:
                test_name = name
        else:
            # Default: append Test
            test_name = f"{name}Test"

        # Reconstruct filename
        if ext:
            return f"{test_name}.{ext}"
        return test_name


def resolve_path(
    config: Dict[str, Any],
    file_type: str,
    name: str,
    project_root: Optional[Path] = None,
    app: Optional[str] = None,
    test: bool = False
) -> Path:
    """
    Convenience function to resolve a file path.

    Args:
        config: Project configuration dictionary
        file_type: Type of file
        name: Name for the file
        project_root: Root directory of the project
        app: Django app name (optional)
        test: Whether to generate test file path

    Returns:
        Resolved absolute path including filename
    """
    resolver = PathResolver(config, project_root)
    return resolver.resolve_full_path(file_type, name, app, test)


# CLI for testing
if __name__ == '__main__':
    import sys
    from config_parser import load_config

    if len(sys.argv) < 4:
        print("Usage: python path_resolver.py <project_root> <file_type> <name> [--app app_name] [--test]")
        print("\nExample:")
        print("  python path_resolver.py skill/examples/example-spring-boot service UserService")
        print("  python path_resolver.py skill/examples/example-spring-boot service UserService --test")
        sys.exit(1)

    project_root = Path(sys.argv[1])
    file_type = sys.argv[2]
    name = sys.argv[3]

    # Parse optional arguments
    app_name = None
    is_test = False

    for i, arg in enumerate(sys.argv[4:], start=4):
        if arg == '--app' and i + 1 < len(sys.argv):
            app_name = sys.argv[i + 1]
        elif arg == '--test':
            is_test = True

    try:
        # Load configuration
        config = load_config(project_root)

        # Create resolver
        resolver = PathResolver(config, project_root)

        # Resolve paths
        print(f"\nPath Resolution for: {name}")
        print("=" * 60)

        # Main file
        full_path = resolver.resolve_full_path(file_type, name, app_name, test=is_test)
        directory = resolver.resolve_path(file_type, name, app_name, test=is_test)
        filename = resolver.resolve_filename(file_type, name, test=is_test)

        print(f"File type: {file_type}")
        print(f"Name: {name}")
        if app_name:
            print(f"App: {app_name}")
        print(f"Test: {is_test}")
        print()
        print(f"Directory: {directory}")
        print(f"Filename: {filename}")
        print(f"Full path: {full_path}")

        # Additional files
        if not is_test:
            additional = resolver.get_additional_files(file_type, name, directory)
            if additional:
                print(f"\nAdditional files:")
                for path in additional:
                    print(f"  - {path}")

            # Test file
            if resolver.should_generate_test(file_type):
                test_path = resolver.resolve_full_path(file_type, name, app_name, test=True)
                print(f"\nTest file: {test_path}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)