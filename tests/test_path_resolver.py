#!/usr/bin/env python3
"""
Unit tests for path_resolver.py
"""

import unittest
from pathlib import Path
import sys

# Add skill/scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'skill' / 'scripts'))

from path_resolver import PathResolver, PathResolutionError


class TestPathResolver(unittest.TestCase):
    """Test PathResolver class"""

    def setUp(self):
        """Set up test configuration"""
        self.config = {
            'project_type': 'spring-boot',
            'language': 'java',
            'base_package': 'com.example.demo',
            'structure': {
                'service': {
                    'path': 'src/main/java/{package}/service',
                    'naming': '{Name}Service.java',
                    'test_path': 'src/test/java/{package}/service',
                    'generate_test': True
                },
                'controller': {
                    'path': 'src/main/java/{package}/controller',
                    'naming': '{Name}Controller.java',
                    'test_path': 'src/test/java/{package}/controller',
                    'generate_test': True
                }
            }
        }
        self.project_root = Path('/tmp/test-project')
        self.resolver = PathResolver(self.config, self.project_root)

    def test_resolve_path_service(self):
        """Test resolving service path"""
        path = self.resolver.resolve_path('service', 'User')

        expected = self.project_root / 'src/main/java/com/example/demo/service'
        self.assertEqual(path, expected)

    def test_resolve_filename_service(self):
        """Test resolving service filename"""
        filename = self.resolver.resolve_filename('service', 'User')

        self.assertEqual(filename, 'UserService.java')

    def test_resolve_full_path_service(self):
        """Test resolving complete service path"""
        full_path = self.resolver.resolve_full_path('service', 'User')

        expected = self.project_root / 'src/main/java/com/example/demo/service/UserService.java'
        self.assertEqual(full_path, expected)

    def test_resolve_test_path(self):
        """Test resolving test file path"""
        test_path = self.resolver.resolve_full_path('service', 'User', test=True)

        expected = self.project_root / 'src/test/java/com/example/demo/service/UserServiceTest.java'
        self.assertEqual(test_path, expected)

    def test_pascal_case_conversion(self):
        """Test PascalCase name conversion"""
        # Already PascalCase
        self.assertEqual(self.resolver._to_pascal_case('UserService'), 'UserService')

        # snake_case to PascalCase
        self.assertEqual(self.resolver._to_pascal_case('user_service'), 'UserService')

        # kebab-case to PascalCase
        self.assertEqual(self.resolver._to_pascal_case('user-service'), 'UserService')

        # camelCase to PascalCase
        self.assertEqual(self.resolver._to_pascal_case('userService'), 'UserService')

    def test_snake_case_conversion(self):
        """Test snake_case name conversion"""
        # PascalCase to snake_case
        self.assertEqual(self.resolver._to_snake_case('UserService'), 'user_service')

        # camelCase to snake_case
        self.assertEqual(self.resolver._to_snake_case('userService'), 'user_service')

        # Already snake_case
        self.assertEqual(self.resolver._to_snake_case('user_service'), 'user_service')

        # kebab-case to snake_case
        self.assertEqual(self.resolver._to_snake_case('user-service'), 'user_service')

    def test_file_type_not_found(self):
        """Test error when file type doesn't exist"""
        with self.assertRaises(PathResolutionError) as cm:
            self.resolver.resolve_path('helper', 'User')

        self.assertIn('not found', str(cm.exception))
        self.assertIn('Available types', str(cm.exception))

    def test_missing_base_package(self):
        """Test error when base_package required but missing"""
        config = {
            'language': 'java',
            'structure': {
                'service': {
                    'path': 'src/main/java/{package}/service',
                    'naming': '{Name}Service.java'
                }
            }
        }
        resolver = PathResolver(config, self.project_root)

        with self.assertRaises(PathResolutionError) as cm:
            resolver.resolve_path('service', 'User')

        self.assertIn('base_package', str(cm.exception))

    def test_should_generate_test(self):
        """Test checking if test should be generated"""
        self.assertTrue(self.resolver.should_generate_test('service'))
        self.assertTrue(self.resolver.should_generate_test('controller'))

    def test_test_filename_java(self):
        """Test Java test filename conversion"""
        filename = self.resolver._convert_to_test_filename('UserService.java')
        self.assertEqual(filename, 'UserServiceTest.java')

    def test_test_filename_python(self):
        """Test Python test filename conversion"""
        python_config = {
            'language': 'python',
            'structure': {
                'model': {
                    'path': 'models',
                    'naming': '{name}.py'
                }
            }
        }
        resolver = PathResolver(python_config, self.project_root)

        filename = resolver._convert_to_test_filename('user_service.py')
        self.assertEqual(filename, 'test_user_service.py')

    def test_test_filename_javascript(self):
        """Test JavaScript test filename conversion"""
        js_config = {
            'language': 'javascript',
            'structure': {
                'component': {
                    'path': 'src/components',
                    'naming': '{Name}.jsx'
                }
            }
        }
        resolver = PathResolver(js_config, self.project_root)

        filename = resolver._convert_to_test_filename('UserProfile.jsx')
        self.assertEqual(filename, 'UserProfile.test.jsx')

    def test_django_app_variable(self):
        """Test Django {app} variable substitution"""
        django_config = {
            'project_type': 'django',
            'language': 'python',
            'structure': {
                'model': {
                    'path': '{app}/models.py',
                    'naming': 'class {Name}(models.Model)'
                }
            }
        }
        resolver = PathResolver(django_config, self.project_root)

        path = resolver.resolve_path('model', 'User', app='users')
        expected = self.project_root / 'users/models.py'
        self.assertEqual(path, expected)

    def test_missing_app_parameter(self):
        """Test error when {app} variable used but app not provided"""
        django_config = {
            'language': 'python',
            'structure': {
                'model': {
                    'path': '{app}/models.py',
                    'naming': 'class {Name}(models.Model)'
                }
            }
        }
        resolver = PathResolver(django_config, self.project_root)

        with self.assertRaises(PathResolutionError) as cm:
            resolver.resolve_path('model', 'User')  # No app parameter

        self.assertIn('app name not provided', str(cm.exception))


if __name__ == '__main__':
    unittest.main()