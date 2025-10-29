"""
Template Loader for Universal Project Organizer

This module provides functionality to discover, load, and manage
project templates.

Usage:
    from skill.scripts.template_loader import TemplateLoader, TemplateError

    loader = TemplateLoader()
    templates = loader.list_templates()
    template = loader.load_template("spring-boot")
"""

import yaml
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional


class TemplateError(Exception):
    """Exception raised for template-related errors."""
    pass


class TemplateLoader:
    """Loader for project templates."""

    def __init__(self, templates_dir: Optional[Path] = None):
        """
        Initialize the template loader.

        Args:
            templates_dir: Path to the templates directory.
                          If None, uses skill/templates relative to this file.
        """
        if templates_dir is None:
            # Default to skill/templates directory
            script_dir = Path(__file__).parent
            self.templates_dir = script_dir.parent / "templates"
        else:
            self.templates_dir = Path(templates_dir)

        if not self.templates_dir.exists():
            raise TemplateError(
                f"Templates directory not found: {self.templates_dir}"
            )

    def list_templates(self) -> List[Tuple[str, str, str]]:
        """
        List all available templates.

        Returns:
            List of tuples: (template_id, language, framework)
            For example: [("spring-boot", "java", "Spring Boot"), ...]
        """
        templates = []

        # Scan each language directory
        for lang_dir in self.templates_dir.iterdir():
            if not lang_dir.is_dir():
                continue

            language = lang_dir.name

            # Scan for template files in the language directory
            for template_file in lang_dir.glob("*.yaml"):
                template_id = template_file.stem  # filename without extension

                # Try to load template to get its display name
                try:
                    template_data = self._load_template_file(template_file)
                    project_type = template_data.get('project_type', template_id)
                    templates.append((template_id, language, project_type))
                except Exception:
                    # If template can't be loaded, skip it
                    continue

        return sorted(templates)

    def load_template(self, template_id: str) -> Dict[str, Any]:
        """
        Load a template by its ID.

        Args:
            template_id: Template identifier (e.g., "spring-boot", "django", "react")

        Returns:
            Template configuration dictionary

        Raises:
            TemplateError: If template not found or invalid
        """
        # Find the template file
        template_path = self._find_template_path(template_id)

        if not template_path:
            available = [t[0] for t in self.list_templates()]
            raise TemplateError(
                f"Template '{template_id}' not found.\n\n"
                f"Available templates:\n" +
                '\n'.join(f"  - {t}" for t in available)
            )

        # Load and validate the template
        template_data = self._load_template_file(template_path)
        self._validate_template(template_data, template_id)

        return template_data

    def get_template_info(self, template_id: str) -> Dict[str, Any]:
        """
        Get information about a template without fully loading it.

        Args:
            template_id: Template identifier

        Returns:
            Dictionary with template metadata
        """
        template_data = self.load_template(template_id)

        return {
            'template_id': template_id,
            'project_type': template_data.get('project_type'),
            'language': template_data.get('language'),
            'version': template_data.get('version', '1.0'),
            'file_types': list(template_data.get('structure', {}).keys()),
            'description': template_data.get('notes', '').split('\n')[0] if 'notes' in template_data else None
        }

    def _find_template_path(self, template_id: str) -> Optional[Path]:
        """
        Find the path to a template file.

        Args:
            template_id: Template identifier

        Returns:
            Path to template file, or None if not found
        """
        # Search in all language directories
        for lang_dir in self.templates_dir.iterdir():
            if not lang_dir.is_dir():
                continue

            template_file = lang_dir / f"{template_id}.yaml"
            if template_file.exists():
                return template_file

        return None

    def _load_template_file(self, template_path: Path) -> Dict[str, Any]:
        """
        Load a template file and parse its YAML content.

        Args:
            template_path: Path to template file

        Returns:
            Parsed template data

        Raises:
            TemplateError: If file can't be read or parsed
        """
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                template_data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise TemplateError(
                f"Invalid YAML in template {template_path.name}:\n{str(e)}"
            )
        except Exception as e:
            raise TemplateError(
                f"Failed to read template {template_path.name}:\n{str(e)}"
            )

        if template_data is None:
            raise TemplateError(f"Template {template_path.name} is empty")

        return template_data

    def _validate_template(self, template_data: Dict[str, Any], template_id: str) -> None:
        """
        Validate template structure.

        Args:
            template_data: Template configuration dictionary
            template_id: Template identifier for error messages

        Raises:
            TemplateError: If template is invalid
        """
        # Check required fields
        required_fields = ['project_type', 'language', 'structure']
        missing = [f for f in required_fields if f not in template_data]

        if missing:
            raise TemplateError(
                f"Template '{template_id}' is missing required fields: {', '.join(missing)}"
            )

        # Validate structure
        structure = template_data.get('structure')
        if not isinstance(structure, dict) or not structure:
            raise TemplateError(
                f"Template '{template_id}' has invalid or empty structure"
            )

        # Validate each structure entry
        for file_type, config in structure.items():
            if not isinstance(config, dict):
                raise TemplateError(
                    f"Template '{template_id}': structure.{file_type} must be a dictionary"
                )

            if 'path' not in config:
                raise TemplateError(
                    f"Template '{template_id}': structure.{file_type} missing 'path'"
                )

            if 'naming' not in config:
                raise TemplateError(
                    f"Template '{template_id}': structure.{file_type} missing 'naming'"
                )

    def customize_template(
        self,
        template_data: Dict[str, Any],
        custom_values: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        Customize a template with user-provided values.

        Args:
            template_data: Original template data
            custom_values: Dictionary of custom values (e.g., {'base_package': 'com.mycompany.app'})

        Returns:
            Customized template data
        """
        import copy
        customized = copy.deepcopy(template_data)

        # Apply custom values
        for key, value in custom_values.items():
            if key in customized:
                customized[key] = value

        # If base_package is customized, update paths in structure
        if 'base_package' in custom_values and 'structure' in customized:
            old_package = template_data.get('base_package', '')
            new_package = custom_values['base_package']

            for file_type, config in customized['structure'].items():
                if 'path' in config and old_package:
                    # Replace package in paths
                    old_path = old_package.replace('.', '/')
                    new_path = new_package.replace('.', '/')
                    config['path'] = config['path'].replace(old_path, new_path)

                if 'test_path' in config and old_package:
                    old_path = old_package.replace('.', '/')
                    new_path = new_package.replace('.', '/')
                    config['test_path'] = config['test_path'].replace(old_path, new_path)

        return customized


def list_available_templates(templates_dir: Optional[Path] = None) -> List[Tuple[str, str, str]]:
    """
    List all available templates.

    This is a convenience function.

    Args:
        templates_dir: Optional custom templates directory

    Returns:
        List of tuples: (template_id, language, framework)
    """
    loader = TemplateLoader(templates_dir)
    return loader.list_templates()


def load_template(template_id: str, templates_dir: Optional[Path] = None) -> Dict[str, Any]:
    """
    Load a template by ID.

    This is a convenience function.

    Args:
        template_id: Template identifier
        templates_dir: Optional custom templates directory

    Returns:
        Template configuration dictionary
    """
    loader = TemplateLoader(templates_dir)
    return loader.load_template(template_id)


if __name__ == "__main__":
    # Simple CLI for testing
    import sys

    loader = TemplateLoader()

    print("Available Templates:")
    print("=" * 60)

    templates = loader.list_templates()
    for template_id, language, project_type in templates:
        print(f"  {template_id:<20} ({language})")

        # Show brief info
        try:
            info = loader.get_template_info(template_id)
            file_types = info['file_types']
            print(f"    File types: {', '.join(file_types[:5])}")
            if len(file_types) > 5:
                print(f"                ... and {len(file_types) - 5} more")
        except Exception as e:
            print(f"    Error: {e}")

        print()

    # If template ID provided, show details
    if len(sys.argv) > 1:
        template_id = sys.argv[1]
        print("\n" + "=" * 60)
        print(f"Template Details: {template_id}")
        print("=" * 60)

        try:
            template = loader.load_template(template_id)
            print(f"Project type: {template['project_type']}")
            print(f"Language: {template['language']}")
            print(f"Version: {template.get('version', 'N/A')}")
            print(f"\nFile types ({len(template['structure'])}):")
            for ft in sorted(template['structure'].keys()):
                print(f"  - {ft}")
        except TemplateError as e:
            print(f"Error: {e}")
            sys.exit(1)