#!/usr/bin/env python3
"""
Configuration Validation Utility for Universal Project Organizer

This utility validates .claude/project.yaml configuration files and
provides detailed feedback about any issues.

Usage:
    python skill/scripts/validate_config.py [project-path]

    If no path is provided, validates the current directory.

Examples:
    # Validate current directory
    python skill/scripts/validate_config.py

    # Validate specific project
    python skill/scripts/validate_config.py /path/to/project

    # Validate with detailed output
    python skill/scripts/validate_config.py --verbose
"""

import sys
import argparse
from pathlib import Path
from typing import Dict, Any, List

# Import the config parser
try:
    from config_parser import ConfigParser, ConfigError, load_config
except ImportError:
    # Try relative import if running as part of package
    from .config_parser import ConfigParser, ConfigError, load_config


def format_success(message: str) -> str:
    """Format a success message with color."""
    return f"✓ {message}"


def format_error(message: str) -> str:
    """Format an error message with color."""
    return f"✗ {message}"


def format_warning(message: str) -> str:
    """Format a warning message."""
    return f"⚠ {message}"


def format_info(message: str) -> str:
    """Format an info message."""
    return f"ℹ {message}"


def validate_project(project_root: Path, verbose: bool = False) -> bool:
    """
    Validate a project's configuration.

    Args:
        project_root: Path to the project root
        verbose: Whether to print verbose output

    Returns:
        True if validation passed, False otherwise
    """
    parser = ConfigParser(project_root)

    print(f"\nValidating configuration for: {project_root.absolute()}")
    print("─" * 60)

    # Check if config file exists
    if not parser.config_path.exists():
        print(format_error(f"Configuration file not found"))
        print(f"\nExpected location: {parser.config_path}")
        print(f"\n{format_info('To initialize:')}")
        print("  python skill/scripts/init_project.py --template <template-name>")
        print(f"\nAvailable templates: {', '.join(parser.SUPPORTED_PROJECT_TYPES)}")
        return False

    # Try to load and validate
    try:
        config = parser.load()
        print(format_success("Configuration is valid"))

        # Print configuration summary
        print("\n" + "─" * 60)
        print("Configuration Summary:")
        print("─" * 60)
        print(f"Project type:    {config['project_type']}")
        print(f"Language:        {config['language']}")

        if 'base_package' in config:
            print(f"Base package:    {config['base_package']}")

        if 'version' in config:
            print(f"Config version:  {config['version']}")

        # List file types
        structure = config.get('structure', {})
        print(f"\nDefined file types ({len(structure)}):")
        for file_type in sorted(structure.keys()):
            print(f"  • {file_type}")

        # Verbose output
        if verbose:
            print("\n" + "─" * 60)
            print("Detailed Structure:")
            print("─" * 60)

            for file_type, file_config in structure.items():
                print(f"\n{file_type}:")
                print(f"  Path:   {file_config.get('path', 'N/A')}")
                print(f"  Naming: {file_config.get('naming', 'N/A')}")

                if 'test_path' in file_config:
                    print(f"  Test:   {file_config['test_path']}")

                if 'generate_test' in file_config:
                    print(f"  Auto-generate tests: {file_config['generate_test']}")

                if 'additional_files' in file_config:
                    files = ', '.join(file_config['additional_files'])
                    print(f"  Additional files: {files}")

        # Check for common issues (warnings, not errors)
        warnings = check_common_issues(config)
        if warnings:
            print("\n" + "─" * 60)
            print("Warnings:")
            print("─" * 60)
            for warning in warnings:
                print(format_warning(warning))

        print("\n" + "─" * 60)
        return True

    except ConfigError as e:
        print(format_error("Validation failed"))
        print(f"\n{e}")
        return False


def check_common_issues(config: Dict[str, Any]) -> List[str]:
    """
    Check for common configuration issues that aren't errors but might be problems.

    Args:
        config: Configuration dictionary

    Returns:
        List of warning messages
    """
    warnings = []
    structure = config.get('structure', {})

    # Check if there are very few file types defined
    if len(structure) < 2:
        warnings.append(
            f"Only {len(structure)} file type(s) defined. "
            f"Consider adding more common types for your project."
        )

    # Check if any file types don't have test configuration
    for file_type, file_config in structure.items():
        if 'generate_test' not in file_config and 'test_path' not in file_config:
            warnings.append(
                f"File type '{file_type}' has no test configuration. "
                f"Consider adding test_path or generate_test."
            )

    # Check if naming templates don't include {Name} variable
    for file_type, file_config in structure.items():
        naming = file_config.get('naming', '')
        if '{Name}' not in naming and '{name}' not in naming:
            warnings.append(
                f"File type '{file_type}' naming template doesn't include {{Name}} or {{name}}. "
                f"This might cause issues with file generation."
            )

    return warnings


def validate_multiple_projects(projects: List[Path], verbose: bool = False) -> None:
    """
    Validate multiple projects and provide a summary.

    Args:
        projects: List of project paths to validate
        verbose: Whether to print verbose output
    """
    results = []

    for project in projects:
        success = validate_project(project, verbose)
        results.append((project, success))

    # Print summary if multiple projects
    if len(projects) > 1:
        print("\n" + "=" * 60)
        print("Validation Summary:")
        print("=" * 60)

        passed = sum(1 for _, success in results if success)
        failed = len(results) - passed

        print(f"Total projects:  {len(results)}")
        print(f"Passed:          {passed}")
        print(f"Failed:          {failed}")

        if failed > 0:
            print("\nFailed projects:")
            for project, success in results:
                if not success:
                    print(f"  ✗ {project}")


def main():
    """Main entry point for the validation utility."""
    parser = argparse.ArgumentParser(
        description="Validate Universal Project Organizer configuration files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Validate current directory
  %(prog)s

  # Validate specific project
  %(prog)s /path/to/project

  # Validate with detailed output
  %(prog)s --verbose

  # Validate multiple projects
  %(prog)s project1/ project2/ project3/
        """
    )

    parser.add_argument(
        'projects',
        nargs='*',
        default=['.'],
        help='Project path(s) to validate (default: current directory)'
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Show detailed configuration information'
    )

    parser.add_argument(
        '--version',
        action='version',
        version='Universal Project Organizer Config Validator 1.0'
    )

    args = parser.parse_args()

    # Convert project paths to Path objects
    project_paths = [Path(p) for p in args.projects]

    # Validate projects
    if len(project_paths) == 1:
        success = validate_project(project_paths[0], args.verbose)
        sys.exit(0 if success else 1)
    else:
        validate_multiple_projects(project_paths, args.verbose)
        # Exit with error if any validation failed
        sys.exit(0)


if __name__ == "__main__":
    main()