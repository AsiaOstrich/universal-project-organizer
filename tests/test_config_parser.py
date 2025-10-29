#!/usr/bin/env python3
"""
Unit tests for config_parser.py
"""

import unittest
import tempfile
import shutil
from pathlib import Path
import sys

# Add skill/scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'skill' / 'scripts'))

from config_parser import ConfigParser, ConfigError, load_config


class TestConfigParser(unittest.TestCase):
    """Test ConfigParser class"""

    def setUp(self):
        """Create temporary directory for test configs"""
        self.test_dir = Path(tempfile.mkdtemp())
        self.claude_dir = self.test_dir / '.claude'
        self.claude_dir.mkdir()

    def tearDown(self):
        """Clean up temporary directory"""
        shutil.rmtree(self.test_dir)

    def test_valid_config(self):
        """Test loading valid configuration"""
        config_file = self.claude_dir / 'project.yaml'
        config_file.write_text("""
project_type: spring-boot
language: java
base_package: com.example.demo

structure:
  service:
    path: "src/main/java/{package}/service"
    naming: "{Name}Service.java"
    generate_test: true
""")

        parser = ConfigParser(self.test_dir)
        config = parser.load()

        self.assertEqual(config['project_type'], 'spring-boot')
        self.assertEqual(config['language'], 'java')
        self.assertEqual(config['base_package'], 'com.example.demo')
        self.assertIn('service', config['structure'])

    def test_missing_required_fields(self):
        """Test configuration missing required fields"""
        config_file = self.claude_dir / 'project.yaml'
        config_file.write_text("""
project_type: spring-boot
# Missing language and structure
""")

        parser = ConfigParser(self.test_dir)
        with self.assertRaises(ConfigError) as cm:
            parser.load()

        self.assertIn('Missing required field', str(cm.exception))

    def test_invalid_project_type(self):
        """Test invalid project type"""
        config_file = self.claude_dir / 'project.yaml'
        config_file.write_text("""
project_type: invalid-type
language: java
structure:
  service:
    path: "src/service"
    naming: "{Name}.java"
""")

        parser = ConfigParser(self.test_dir)
        with self.assertRaises(ConfigError) as cm:
            parser.load()

        self.assertIn('Unsupported project_type', str(cm.exception))

    def test_invalid_language(self):
        """Test invalid language"""
        config_file = self.claude_dir / 'project.yaml'
        config_file.write_text("""
project_type: spring-boot
language: cobol
structure:
  service:
    path: "src/service"
    naming: "{Name}.java"
""")

        parser = ConfigParser(self.test_dir)
        with self.assertRaises(ConfigError) as cm:
            parser.load()

        self.assertIn('Unsupported language', str(cm.exception))

    def test_empty_structure(self):
        """Test configuration with empty structure"""
        config_file = self.claude_dir / 'project.yaml'
        config_file.write_text("""
project_type: spring-boot
language: java
structure: {}
""")

        parser = ConfigParser(self.test_dir)
        with self.assertRaises(ConfigError) as cm:
            parser.load()

        self.assertIn('cannot be empty', str(cm.exception))

    def test_structure_missing_path(self):
        """Test structure entry missing path"""
        config_file = self.claude_dir / 'project.yaml'
        config_file.write_text("""
project_type: spring-boot
language: java
structure:
  service:
    naming: "{Name}Service.java"
    # Missing path
""")

        parser = ConfigParser(self.test_dir)
        with self.assertRaises(ConfigError) as cm:
            parser.load()

        self.assertIn("missing required field", str(cm.exception))

    def test_structure_missing_naming(self):
        """Test structure entry missing naming"""
        config_file = self.claude_dir / 'project.yaml'
        config_file.write_text("""
project_type: spring-boot
language: java
structure:
  service:
    path: "src/service"
    # Missing naming
""")

        parser = ConfigParser(self.test_dir)
        with self.assertRaises(ConfigError) as cm:
            parser.load()

        self.assertIn("missing required field", str(cm.exception))

    def test_config_not_found(self):
        """Test missing configuration file"""
        parser = ConfigParser(self.test_dir / 'nonexistent')
        with self.assertRaises(ConfigError) as cm:
            parser.load()

        self.assertIn('not found', str(cm.exception))

    def test_invalid_yaml(self):
        """Test invalid YAML syntax"""
        config_file = self.claude_dir / 'project.yaml'
        config_file.write_text("""
project_type: spring-boot
language: java
structure:
  service:
    path: "unclosed string
""")

        parser = ConfigParser(self.test_dir)
        with self.assertRaises(ConfigError) as cm:
            parser.load()

        self.assertIn('Invalid YAML', str(cm.exception))

    def test_load_config_convenience_function(self):
        """Test load_config convenience function"""
        config_file = self.claude_dir / 'project.yaml'
        config_file.write_text("""
project_type: django
language: python
structure:
  model:
    path: "{app}/models.py"
    naming: "class {Name}(models.Model)"
""")

        config = load_config(self.test_dir)

        self.assertEqual(config['project_type'], 'django')
        self.assertEqual(config['language'], 'python')

    def test_optional_fields(self):
        """Test configuration with optional fields"""
        config_file = self.claude_dir / 'project.yaml'
        config_file.write_text("""
project_type: react
language: javascript
version: "2.0"
description: "My React app"

structure:
  component:
    path: "src/components"
    naming: "{Name}.jsx"

naming_conventions:
  class: "PascalCase"
  method: "camelCase"

auto_generate:
  test_files: true
""")

        parser = ConfigParser(self.test_dir)
        config = parser.load()

        self.assertEqual(config['version'], '2.0')
        self.assertEqual(config['description'], 'My React app')
        self.assertIn('naming_conventions', config)
        self.assertIn('auto_generate', config)


if __name__ == '__main__':
    unittest.main()