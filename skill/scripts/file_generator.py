#!/usr/bin/env python3
"""
File Generator for Universal Project Organizer

Generates code files based on templates and project configuration.
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass

from config_parser import load_config
from path_resolver import PathResolver, PathResolutionError


class FileGenerationError(Exception):
    """Exception raised for file generation errors."""
    pass


@dataclass
class GeneratedFile:
    """Represents a generated file."""
    path: Path
    content: str
    file_type: str
    is_test: bool = False


class FileGenerator:
    """
    Generates code files based on project templates.

    Supports:
    - Creating main files with boilerplate code
    - Auto-generating test files
    - Creating additional files (CSS, types, etc.)
    - Applying annotations and imports based on file type
    """

    def __init__(self, config: Dict[str, Any], project_root: Optional[Path] = None):
        """
        Initialize FileGenerator.

        Args:
            config: Project configuration dictionary
            project_root: Root directory of the project
        """
        self.config = config
        self.project_root = project_root or Path.cwd()
        self.resolver = PathResolver(config, project_root)
        self.language = config.get('language', '')
        self.project_type = config.get('project_type', '')

    def generate(
        self,
        file_type: str,
        name: str,
        app: Optional[str] = None,
        custom_content: Optional[str] = None,
        dry_run: bool = False
    ) -> List[GeneratedFile]:
        """
        Generate files for the given file type and name.

        Args:
            file_type: Type of file to generate
            name: Name for the file
            app: Django app name (optional)
            custom_content: Custom content to use instead of boilerplate
            dry_run: If True, don't write files (just return what would be generated)

        Returns:
            List of generated files

        Raises:
            FileGenerationError: If generation fails
        """
        generated_files = []

        try:
            # Generate main file
            main_file = self._generate_main_file(
                file_type, name, app, custom_content
            )
            generated_files.append(main_file)

            # Generate test file if configured
            if self.resolver.should_generate_test(file_type):
                test_file = self._generate_test_file(file_type, name, app)
                generated_files.append(test_file)

            # Generate additional files (CSS, types, etc.)
            directory = self.resolver.resolve_path(file_type, name, app)
            additional_paths = self.resolver.get_additional_files(
                file_type, name, directory
            )
            for path in additional_paths:
                additional_file = self._generate_additional_file(
                    path, file_type, name
                )
                generated_files.append(additional_file)

            # Write files to disk
            if not dry_run:
                for file in generated_files:
                    self._write_file(file)

            return generated_files

        except Exception as e:
            raise FileGenerationError(f"Failed to generate {file_type}: {e}") from e

    def _generate_main_file(
        self,
        file_type: str,
        name: str,
        app: Optional[str],
        custom_content: Optional[str]
    ) -> GeneratedFile:
        """Generate the main file."""
        path = self.resolver.resolve_full_path(file_type, name, app, test=False)

        if custom_content:
            content = custom_content
        else:
            content = self._generate_boilerplate(file_type, name, app)

        return GeneratedFile(
            path=path,
            content=content,
            file_type=file_type,
            is_test=False
        )

    def _generate_test_file(
        self,
        file_type: str,
        name: str,
        app: Optional[str]
    ) -> GeneratedFile:
        """Generate a test file."""
        path = self.resolver.resolve_full_path(file_type, name, app, test=True)
        content = self._generate_test_boilerplate(file_type, name, app)

        return GeneratedFile(
            path=path,
            content=content,
            file_type=file_type,
            is_test=True
        )

    def _generate_additional_file(
        self,
        path: Path,
        file_type: str,
        name: str
    ) -> GeneratedFile:
        """Generate an additional file (CSS, types, etc.)."""
        content = self._generate_additional_boilerplate(path, file_type, name)

        return GeneratedFile(
            path=path,
            content=content,
            file_type=file_type,
            is_test=False
        )

    def _generate_boilerplate(
        self,
        file_type: str,
        name: str,
        app: Optional[str]
    ) -> str:
        """
        Generate boilerplate code for a file.

        Creates language-specific code with:
        - Package/import declarations
        - Class/function definitions
        - Common annotations
        - Standard imports
        """
        pascal_name = self.resolver._to_pascal_case(name)
        snake_name = self.resolver._to_snake_case(name)

        if self.language == 'java':
            return self._generate_java_boilerplate(file_type, pascal_name)
        elif self.language == 'python':
            return self._generate_python_boilerplate(file_type, pascal_name, snake_name, app)
        elif self.language in ['javascript', 'typescript']:
            return self._generate_javascript_boilerplate(file_type, pascal_name)
        else:
            # Generic boilerplate
            return f"// {pascal_name}\n// TODO: Implement {file_type}\n"

    def _generate_java_boilerplate(self, file_type: str, name: str) -> str:
        """Generate Java boilerplate code."""
        package = self.config.get('base_package', 'com.example.demo')
        structure = self.config.get('structure', {})
        file_config = structure.get(file_type, {})

        # Get class name from naming pattern (e.g., "{Name}Service.java" -> "UserService")
        filename = self.resolver.resolve_filename(file_type, name, test=False)
        class_name = filename.replace('.java', '')

        # Package declaration
        lines = [f"package {package}.{file_type};", ""]

        # Imports (try both 'imports' and 'common_imports')
        imports = self.config.get('imports', {}).get(file_type, [])
        if not imports:
            imports = self.config.get('common_imports', {}).get(file_type, [])
        if imports:
            for imp in imports:
                lines.append(f"import {imp};")
            lines.append("")

        # Annotations
        annotations = self.config.get('annotations', {}).get(file_type, [])
        if annotations:
            for annotation in annotations:
                # Remove "(optional)" from annotations
                annotation = annotation.replace(" (optional)", "").strip()
                lines.append(annotation)
            lines.append("")

        # Class definition
        class_type = self._get_java_class_type(file_type)
        lines.append(f"public {class_type} {class_name} {{")
        lines.append("")
        lines.append("    // TODO: Implement business logic")
        lines.append("")
        lines.append("}")

        return "\n".join(lines)

    def _generate_python_boilerplate(
        self,
        file_type: str,
        pascal_name: str,
        snake_name: str,
        app: Optional[str]
    ) -> str:
        """Generate Python boilerplate code."""
        lines = []

        # Module docstring
        lines.append(f'"""')
        lines.append(f"{pascal_name} {file_type}")
        lines.append(f'"""')
        lines.append("")

        # Common imports
        common_imports = self.config.get('common_imports', {}).get(file_type, [])
        if common_imports:
            lines.extend(common_imports)
            lines.append("")

        # Generate code based on file type
        if file_type in ['model', 'serializer', 'view', 'form']:
            # Django class-based files
            base_class = self._get_python_base_class(file_type)
            lines.append(f"class {pascal_name}({base_class}):")
            lines.append('    """')
            lines.append(f"    {pascal_name} {file_type}")
            lines.append('    """')
            lines.append("    # TODO: Implement")
            lines.append("    pass")
        elif file_type == 'function_view':
            # Django function-based view
            lines.append(f"def {snake_name}(request):")
            lines.append('    """')
            lines.append(f"    {pascal_name} view")
            lines.append('    """')
            lines.append("    # TODO: Implement")
            lines.append("    pass")
        else:
            # Generic Python code
            lines.append(f"# {pascal_name}")
            lines.append("# TODO: Implement")

        lines.append("")
        return "\n".join(lines)

    def _generate_javascript_boilerplate(self, file_type: str, name: str) -> str:
        """Generate JavaScript/TypeScript boilerplate code."""
        lines = []

        if file_type == 'component':
            # React component
            lines.append(f"import React from 'react';")
            lines.append(f"import styles from './{name}.module.css';")
            lines.append("")
            lines.append(f"const {name} = () => {{")
            lines.append("  return (")
            lines.append(f"    <div className={{styles.container}}>")
            lines.append(f"      <h1>{name}</h1>")
            lines.append("      {/* TODO: Implement component */}")
            lines.append("    </div>")
            lines.append("  );")
            lines.append("};")
            lines.append("")
            lines.append(f"export default {name};")
        elif file_type == 'hook':
            # Custom React hook
            hook_name = f"use{name}"
            lines.append(f"import {{ useState, useEffect }} from 'react';")
            lines.append("")
            lines.append(f"const {hook_name} = () => {{")
            lines.append("  // TODO: Implement hook logic")
            lines.append("  return {};")
            lines.append("};")
            lines.append("")
            lines.append(f"export default {hook_name};")
        elif file_type == 'service':
            # API service
            lines.append(f"// {name} Service")
            lines.append("")
            lines.append(f"const {name}Service = {{")
            lines.append("  // TODO: Implement service methods")
            lines.append("};")
            lines.append("")
            lines.append(f"export default {name}Service;")
        else:
            # Generic JavaScript
            lines.append(f"// {name}")
            lines.append("// TODO: Implement")

        lines.append("")
        return "\n".join(lines)

    def _generate_test_boilerplate(
        self,
        file_type: str,
        name: str,
        app: Optional[str]
    ) -> str:
        """Generate test boilerplate code."""
        pascal_name = self.resolver._to_pascal_case(name)
        snake_name = self.resolver._to_snake_case(name)

        if self.language == 'java':
            return self._generate_java_test_boilerplate(file_type, pascal_name)
        elif self.language == 'python':
            return self._generate_python_test_boilerplate(file_type, pascal_name, snake_name)
        elif self.language in ['javascript', 'typescript']:
            return self._generate_javascript_test_boilerplate(file_type, pascal_name)
        else:
            return f"// Test for {pascal_name}\n// TODO: Implement tests\n"

    def _generate_java_test_boilerplate(self, file_type: str, name: str) -> str:
        """Generate Java test boilerplate."""
        package = self.config.get('base_package', 'com.example.demo')

        # Get test class name from naming pattern
        test_filename = self.resolver.resolve_filename(file_type, name, test=True)
        test_class = test_filename.replace('.java', '')

        # Get main class name for test method
        main_filename = self.resolver.resolve_filename(file_type, name, test=False)
        main_class = main_filename.replace('.java', '')

        lines = [
            f"package {package}.{file_type};",
            "",
            "import org.junit.jupiter.api.Test;",
            "import static org.junit.jupiter.api.Assertions.*;",
            "",
            f"class {test_class} {{",
            "",
            "    @Test",
            f"    void test{main_class}() {{",
            "        // TODO: Implement test",
            "    }",
            "",
            "}"
        ]

        return "\n".join(lines)

    def _generate_python_test_boilerplate(
        self,
        file_type: str,
        pascal_name: str,
        snake_name: str
    ) -> str:
        """Generate Python test boilerplate."""
        lines = [
            f'"""',
            f"Tests for {pascal_name}",
            f'"""',
            "",
            "import pytest",
            "",
            "",
            f"def test_{snake_name}():",
            '    """',
            f"    Test {pascal_name}",
            '    """',
            "    # TODO: Implement test",
            "    pass",
            ""
        ]

        return "\n".join(lines)

    def _generate_javascript_test_boilerplate(self, file_type: str, name: str) -> str:
        """Generate JavaScript test boilerplate."""
        lines = [
            f"import {{ render, screen }} from '@testing-library/react';",
            f"import {name} from './{name}';",
            "",
            f"describe('{name}', () => {{",
            f"  test('renders {name}', () => {{",
            "    // TODO: Implement test",
            "  });",
            "});",
            ""
        ]

        return "\n".join(lines)

    def _generate_additional_boilerplate(
        self,
        path: Path,
        file_type: str,
        name: str
    ) -> str:
        """Generate boilerplate for additional files."""
        filename = path.name

        if filename.endswith('.css') or filename.endswith('.module.css'):
            # CSS file
            return f"/* {name} styles */\n\n.container {{\n  /* TODO: Add styles */\n}}\n"
        elif filename.endswith('.ts') or filename.endswith('.d.ts'):
            # TypeScript type file
            return f"// {name} types\n\nexport interface {name}Props {{\n  // TODO: Define props\n}}\n"
        else:
            # Generic file
            return f"// {filename}\n// TODO: Implement\n"

    def _get_java_class_type(self, file_type: str) -> str:
        """Get Java class type (class, interface, enum)."""
        # Most types are classes, but some can be interfaces
        if file_type in ['repository']:
            return 'interface'
        return 'class'

    def _get_python_base_class(self, file_type: str) -> str:
        """Get Python base class for Django."""
        base_classes = {
            'model': 'models.Model',
            'serializer': 'serializers.ModelSerializer',
            'view': 'APIView',
            'form': 'forms.Form',
        }
        return base_classes.get(file_type, 'object')

    def _write_file(self, file: GeneratedFile) -> None:
        """
        Write a generated file to disk.

        Creates parent directories if they don't exist.
        """
        # Create parent directories
        file.path.parent.mkdir(parents=True, exist_ok=True)

        # Check if file already exists
        if file.path.exists():
            raise FileGenerationError(
                f"File already exists: {file.path}\n"
                f"Use --force to overwrite existing files."
            )

        # Write file
        file.path.write_text(file.content, encoding='utf-8')


def generate_file(
    config: Dict[str, Any],
    file_type: str,
    name: str,
    project_root: Optional[Path] = None,
    app: Optional[str] = None,
    custom_content: Optional[str] = None,
    dry_run: bool = False
) -> List[GeneratedFile]:
    """
    Convenience function to generate files.

    Args:
        config: Project configuration
        file_type: Type of file to generate
        name: Name for the file
        project_root: Root directory of the project
        app: Django app name (optional)
        custom_content: Custom content instead of boilerplate
        dry_run: Don't write files, just return what would be generated

    Returns:
        List of generated files
    """
    generator = FileGenerator(config, project_root)
    return generator.generate(file_type, name, app, custom_content, dry_run)


# CLI for testing
if __name__ == '__main__':
    import sys

    if len(sys.argv) < 4:
        print("Usage: python file_generator.py <project_root> <file_type> <name> [--app app_name] [--dry-run]")
        print("\nExample:")
        print("  python file_generator.py skill/examples/example-spring-boot service UserService")
        print("  python file_generator.py skill/examples/example-spring-boot service UserService --dry-run")
        sys.exit(1)

    project_root = Path(sys.argv[1])
    file_type = sys.argv[2]
    name = sys.argv[3]

    # Parse optional arguments
    app_name = None
    dry_run = False

    for i, arg in enumerate(sys.argv[4:], start=4):
        if arg == '--app' and i + 1 < len(sys.argv):
            app_name = sys.argv[i + 1]
        elif arg == '--dry-run':
            dry_run = True

    try:
        # Load configuration
        config = load_config(project_root)

        # Generate files
        print(f"\nGenerating {file_type}: {name}")
        print("=" * 60)

        generated_files = generate_file(
            config, file_type, name, project_root, app_name, dry_run=dry_run
        )

        print(f"\nGenerated {len(generated_files)} file(s):")
        for file in generated_files:
            status = "(dry-run)" if dry_run else "✓"
            test_marker = "[TEST]" if file.is_test else ""
            print(f"  {status} {test_marker} {file.path}")

        if not dry_run:
            print(f"\n✓ Files created successfully!")
        else:
            print(f"\n(Dry run - no files were created)")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)