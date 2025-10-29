#!/usr/bin/env python3
"""
Unit tests for template_loader.py
"""

import unittest
from pathlib import Path
import sys

# Add skill/scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'skill' / 'scripts'))

from template_loader import TemplateLoader, TemplateError


class TestTemplateLoader(unittest.TestCase):
    """Test TemplateLoader class"""

    def setUp(self):
        """Set up template loader"""
        self.loader = TemplateLoader()

    def test_list_templates(self):
        """Test listing available templates"""
        templates = self.loader.list_templates()

        # Should have at least 3 templates
        self.assertGreaterEqual(len(templates), 3)

        # Check structure
        for template_id, language, project_type in templates:
            self.assertIsInstance(template_id, str)
            self.assertIsInstance(language, str)
            self.assertIsInstance(project_type, str)

    def test_load_spring_boot_template(self):
        """Test loading Spring Boot template"""
        template = self.loader.load_template('spring-boot')

        self.assertEqual(template['project_type'], 'spring-boot')
        self.assertEqual(template['language'], 'java')
        self.assertIn('structure', template)
        self.assertIn('service', template['structure'])
        self.assertIn('controller', template['structure'])

    def test_load_django_template(self):
        """Test loading Django template"""
        template = self.loader.load_template('django')

        self.assertEqual(template['project_type'], 'django')
        self.assertEqual(template['language'], 'python')
        self.assertIn('structure', template)
        self.assertIn('model', template['structure'])
        self.assertIn('view', template['structure'])

    def test_load_react_template(self):
        """Test loading React template"""
        template = self.loader.load_template('react')

        self.assertEqual(template['project_type'], 'react')
        self.assertEqual(template['language'], 'javascript')
        self.assertIn('structure', template)
        self.assertIn('component', template['structure'])
        self.assertIn('hook', template['structure'])

    def test_load_nonexistent_template(self):
        """Test loading non-existent template"""
        with self.assertRaises(TemplateError) as cm:
            self.loader.load_template('nonexistent')

        self.assertIn('not found', str(cm.exception))

    def test_get_template_info(self):
        """Test getting template metadata"""
        info = self.loader.get_template_info('spring-boot')

        self.assertEqual(info['template_id'], 'spring-boot')
        self.assertEqual(info['project_type'], 'spring-boot')
        self.assertEqual(info['language'], 'java')
        self.assertIn('file_types', info)
        self.assertGreater(len(info['file_types']), 0)

    def test_customize_template(self):
        """Test customizing template with custom values"""
        template = self.loader.load_template('spring-boot')

        custom_values = {
            'base_package': 'com.mycompany.myapp'
        }

        customized = self.loader.customize_template(template, custom_values)

        self.assertEqual(customized['base_package'], 'com.mycompany.myapp')
        # Original should not be modified
        self.assertNotEqual(template.get('base_package'), 'com.mycompany.myapp')

    def test_template_has_required_fields(self):
        """Test that templates have required fields"""
        for template_id, _, _ in self.loader.list_templates():
            template = self.loader.load_template(template_id)

            # Required fields
            self.assertIn('project_type', template)
            self.assertIn('language', template)
            self.assertIn('structure', template)

            # Structure should not be empty
            self.assertGreater(len(template['structure']), 0)

    def test_template_file_types_valid(self):
        """Test that all file types in templates are valid"""
        for template_id, _, _ in self.loader.list_templates():
            template = self.loader.load_template(template_id)

            for file_type, config in template['structure'].items():
                # Each file type must have path and naming
                self.assertIn('path', config,
                    f"Template {template_id}: file type '{file_type}' missing 'path'")
                self.assertIn('naming', config,
                    f"Template {template_id}: file type '{file_type}' missing 'naming'")


if __name__ == '__main__':
    unittest.main()