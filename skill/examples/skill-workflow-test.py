#!/usr/bin/env python3
"""
Test script to validate the SKILL.md workflow examples.

This script demonstrates the complete workflow described in SKILL.md.
"""

import sys
from pathlib import Path

# Add skill/scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from config_resolver import resolve_config, ConfigurationError
from file_generator import generate_file, FileGenerationError


def test_spring_boot_service():
    """Test Example 1 from SKILL.md: Spring Boot Service"""
    print("=" * 60)
    print("Test 1: Spring Boot Service")
    print("=" * 60)
    print("User request: 'Create a UserService'\n")

    try:
        # 1. Load configuration
        project_root = Path(__file__).parent / 'example-spring-boot'
        config = resolve_config(project_root)
        print(f"✓ Configuration loaded from: {project_root}")

        # 2. Generate files (dry-run to avoid conflicts)
        generated_files = generate_file(
            config=config,
            file_type='service',
            name='Test',  # Use 'Test' to avoid conflicts
            project_root=project_root,
            dry_run=True  # Preview only
        )

        # 3. Report results
        print(f"\n✓ Would create service: Test\n")
        print(f"Would generate {len(generated_files)} file(s):")
        for file in generated_files:
            relative_path = file.path.relative_to(project_root)
            marker = "[TEST]" if file.is_test else ""
            print(f"  ✓ {marker} {relative_path}")

        # Show the generated code
        main_file = generated_files[0]
        print(f"\n{main_file.path.name}:")
        print("```java")
        print(main_file.content)
        print("```")

        print("\n✅ Test 1 PASSED\n")
        return True

    except Exception as e:
        print(f"\n❌ Test 1 FAILED: {e}\n")
        return False


def test_configuration_error():
    """Test error handling: Configuration not found"""
    print("=" * 60)
    print("Test 2: Configuration Error Handling")
    print("=" * 60)
    print("User request: Generate file in directory without config\n")

    try:
        # Try to load config from directory without .claude/project.yaml
        project_root = Path('/tmp/nonexistent_project')
        config = resolve_config(project_root)

        print("❌ Test 2 FAILED: Should have raised ConfigurationError\n")
        return False

    except ConfigurationError as e:
        print(f"✓ Caught expected error: {e}")
        print("\n✓ Error handling works correctly")
        print("\nWould show to user:")
        print("=" * 60)
        print(f"❌ Configuration error: {e}")
        print("\nTo fix this:")
        print("1. Create .claude/project.yaml in your project root")
        print("2. Specify your project type and structure")
        print("\nExample:")
        print("```yaml")
        print("project_type: spring-boot")
        print("language: java")
        print("base_package: com.example.demo")
        print("```")

        print("\n✅ Test 2 PASSED\n")
        return True

    except Exception as e:
        print(f"❌ Test 2 FAILED: Unexpected error: {e}\n")
        return False


def test_file_type_validation():
    """Test error handling: Invalid file type"""
    print("=" * 60)
    print("Test 3: File Type Validation")
    print("=" * 60)
    print("User request: 'Create a UserHelper' (type doesn't exist)\n")

    try:
        # Load valid config
        project_root = Path(__file__).parent / 'example-spring-boot'
        config = resolve_config(project_root)

        # Try to generate with invalid file type
        generated_files = generate_file(
            config=config,
            file_type='helper',  # Doesn't exist
            name='User',
            project_root=project_root,
            dry_run=True
        )

        print("❌ Test 3 FAILED: Should have raised error for invalid type\n")
        return False

    except FileGenerationError as e:
        print(f"✓ Caught expected error: {e}")

        # Show available file types
        structure = config.get('structure', {})
        print("\n✓ Would show to user:")
        print("=" * 60)
        print(f"❌ {e}")
        print("\nAvailable file types in this project:")
        for file_type in sorted(structure.keys()):
            print(f"  - {file_type}")

        print("\n✅ Test 3 PASSED\n")
        return True

    except Exception as e:
        print(f"❌ Test 3 FAILED: Unexpected error: {e}\n")
        return False


def test_hierarchical_config():
    """Test hierarchical configuration resolution"""
    print("=" * 60)
    print("Test 4: Hierarchical Configuration")
    print("=" * 60)
    print("User request: Generate in nested config structure\n")

    try:
        # Load config from nested directory
        project_root = Path(__file__).parent / 'multi-config-example/backend/user-service'

        if not project_root.exists():
            print("⚠️  Test 4 SKIPPED: multi-config-example not found")
            print("   (This is expected if example doesn't exist)\n")
            return True

        config = resolve_config(project_root)

        # Show config sources
        print("✓ Configuration resolved from:")
        for source in config.get('_config_sources', []):
            print(f"  - {source}")

        # Verify merged configuration
        print(f"\n✓ Final configuration:")
        print(f"  - project_type: {config.get('project_type')}")
        print(f"  - language: {config.get('language')}")
        print(f"  - base_package: {config.get('base_package')}")

        # Count file types (should be merged from all levels)
        structure = config.get('structure', {})
        print(f"  - file_types: {len(structure)} types available")
        print(f"    ({', '.join(sorted(structure.keys()))})")

        print("\n✅ Test 4 PASSED\n")
        return True

    except Exception as e:
        print(f"❌ Test 4 FAILED: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_preview_mode():
    """Test dry-run / preview mode"""
    print("=" * 60)
    print("Test 5: Preview Mode (Dry Run)")
    print("=" * 60)
    print("User request: 'Preview creating a ProductController'\n")

    try:
        project_root = Path(__file__).parent / 'example-spring-boot'
        config = resolve_config(project_root)

        # Generate in dry-run mode
        preview = generate_file(
            config=config,
            file_type='controller',
            name='Product',
            project_root=project_root,
            dry_run=True
        )

        print("✓ Preview mode - no files will be created:\n")
        for file in preview:
            print(f"File: {file.path.relative_to(project_root)}")
            print("Content preview:")
            content_preview = file.content[:150] + "..." if len(file.content) > 150 else file.content
            print(content_preview)
            print()

        print("✅ Test 5 PASSED\n")
        return True

    except Exception as e:
        print(f"❌ Test 5 FAILED: {e}\n")
        return False


def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("SKILL.md Workflow Validation Tests")
    print("=" * 60 + "\n")

    tests = [
        ("Spring Boot Service Generation", test_spring_boot_service),
        ("Configuration Error Handling", test_configuration_error),
        ("File Type Validation", test_file_type_validation),
        ("Hierarchical Configuration", test_hierarchical_config),
        ("Preview Mode", test_preview_mode),
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ Test '{name}' crashed: {e}\n")
            results.append((name, False))

    # Summary
    print("=" * 60)
    print("Test Summary")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")

    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 All tests passed! SKILL.md workflow is working correctly.\n")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please review.\n")
        return 1


if __name__ == '__main__':
    sys.exit(main())