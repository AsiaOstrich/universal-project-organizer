#!/usr/bin/env python3
"""
Configuration Resolver for Universal Project Organizer

Handles hierarchical configuration lookup with inheritance and override rules.
Resolves configuration conflicts based on priority order.
"""

from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
import yaml


class ConfigurationError(Exception):
    """Exception raised for configuration resolution errors."""
    pass


class ConfigResolver:
    """
    Resolves project configuration with hierarchical lookup.

    Priority order (highest to lowest):
    1. Current directory .claude/project.yaml
    2. Parent directory .claude/project.yaml
    3. Grandparent directory .claude/project.yaml
    ... (continue up the tree)
    N. Project root .claude/project.yaml
    N+1. Default template configuration

    Rules:
    - Child configs inherit from parent configs
    - Child configs can override parent settings
    - Specific settings override general settings
    - Structure definitions are merged (not replaced)
    """

    CONFIG_FILENAME = '.claude/project.yaml'

    def __init__(self, start_path: Path):
        """
        Initialize ConfigResolver.

        Args:
            start_path: Starting directory for configuration lookup
        """
        self.start_path = Path(start_path).resolve()
        self.config_chain: List[Tuple[Path, Dict[str, Any]]] = []

    def resolve(self) -> Dict[str, Any]:
        """
        Resolve configuration with hierarchical lookup and merging.

        Returns:
            Merged configuration dictionary

        Raises:
            ConfigurationError: If no configuration found or invalid config
        """
        # Build configuration chain from current directory up
        self._build_config_chain()

        if not self.config_chain:
            raise ConfigurationError(
                f"No configuration file found in {self.start_path} or parent directories.\n"
                f"Expected: .claude/project.yaml"
            )

        # Merge configurations from top (root) to bottom (current)
        merged_config = self._merge_configs()

        # Validate final configuration
        self._validate_config(merged_config)

        return merged_config

    def _build_config_chain(self) -> None:
        """
        Build the configuration chain by walking up the directory tree.

        Stores configs in order from root (lowest priority) to current (highest priority).
        """
        current = self.start_path
        configs_found = []

        # Walk up the directory tree
        while True:
            config_path = current / self.CONFIG_FILENAME

            if config_path.exists():
                try:
                    config_data = yaml.safe_load(config_path.read_text(encoding='utf-8'))
                    configs_found.append((current, config_data))
                except yaml.YAMLError as e:
                    raise ConfigurationError(
                        f"Invalid YAML in {config_path}: {e}"
                    )

            # Check if we've reached the root or a project boundary
            parent = current.parent
            if parent == current:  # Reached filesystem root
                break

            # Stop at git root or when we find a marker file
            if (current / '.git').exists():
                break

            current = parent

        # Reverse to get root-to-current order (lowest to highest priority)
        self.config_chain = list(reversed(configs_found))

    def _merge_configs(self) -> Dict[str, Any]:
        """
        Merge configuration chain with proper override rules.

        Merging strategy:
        - Scalar values: child overrides parent
        - Lists: child extends parent (with option to replace)
        - Dicts: recursive merge (child adds/overrides keys)
        - Structure: merge file types (child can add new types)
        """
        if not self.config_chain:
            return {}

        # Start with the root (lowest priority) config
        merged = self._deep_copy(self.config_chain[0][1])

        # Add metadata about config source
        merged['_config_sources'] = [str(self.config_chain[0][0])]

        # Merge each subsequent config
        for path, config in self.config_chain[1:]:
            merged = self._merge_dict(merged, config)
            merged['_config_sources'].append(str(path))

        return merged

    def _merge_dict(self, base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        """
        Recursively merge two dictionaries.

        Rules:
        - Override wins for scalar values
        - Lists are extended (unless _replace: true)
        - Dicts are recursively merged
        - Special handling for 'structure' to merge file types
        """
        result = self._deep_copy(base)

        for key, value in override.items():
            if key not in result:
                # New key from override
                result[key] = self._deep_copy(value)
            elif key == 'structure':
                # Special handling: merge file type definitions
                result[key] = self._merge_structure(result[key], value)
            elif isinstance(value, dict) and isinstance(result[key], dict):
                # Recursive merge for nested dicts
                result[key] = self._merge_dict(result[key], value)
            elif isinstance(value, list) and isinstance(result[key], list):
                # Extend lists (unless marked for replacement)
                if override.get(f'{key}_replace', False):
                    result[key] = self._deep_copy(value)
                else:
                    result[key] = result[key] + value
            else:
                # Override scalar values
                result[key] = self._deep_copy(value)

        return result

    def _merge_structure(
        self,
        base_structure: Dict[str, Any],
        override_structure: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Merge structure definitions (file types).

        Rules:
        - Child can add new file types
        - Child can override specific file type settings
        - Existing file types are merged, not replaced
        """
        result = self._deep_copy(base_structure)

        for file_type, config in override_structure.items():
            if file_type in result:
                # Merge existing file type config
                result[file_type] = self._merge_dict(result[file_type], config)
            else:
                # Add new file type
                result[file_type] = self._deep_copy(config)

        return result

    def _deep_copy(self, obj: Any) -> Any:
        """Deep copy an object (dict, list, or scalar)."""
        if isinstance(obj, dict):
            return {k: self._deep_copy(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._deep_copy(item) for item in obj]
        else:
            return obj

    def _validate_config(self, config: Dict[str, Any]) -> None:
        """
        Validate the final merged configuration.

        Checks:
        - Required fields present
        - Valid values
        - No conflicts
        """
        # Check required fields
        required_fields = ['language', 'structure']
        missing = [f for f in required_fields if f not in config]

        if missing:
            raise ConfigurationError(
                f"Missing required fields in merged configuration: {', '.join(missing)}\n"
                f"Config sources: {config.get('_config_sources', [])}"
            )

        # Validate structure
        if not config['structure']:
            raise ConfigurationError(
                "Configuration has empty 'structure'. At least one file type must be defined."
            )

        # Validate each file type
        for file_type, file_config in config['structure'].items():
            if 'path' not in file_config:
                raise ConfigurationError(
                    f"File type '{file_type}' missing 'path' field"
                )
            if 'naming' not in file_config:
                raise ConfigurationError(
                    f"File type '{file_type}' missing 'naming' field"
                )

    def get_config_source(self, key: str) -> Optional[str]:
        """
        Get the source (file path) of a specific configuration key.

        Useful for debugging: "Where did this setting come from?"
        """
        # Walk the chain backwards (highest to lowest priority)
        for path, config in reversed(self.config_chain):
            if key in config:
                return str(path)
        return None

    def show_resolution_order(self) -> str:
        """
        Show the configuration resolution order for debugging.

        Returns:
            Human-readable description of config resolution
        """
        if not self.config_chain:
            return "No configuration found"

        lines = ["Configuration Resolution Order:"]
        lines.append("=" * 60)

        for i, (path, config) in enumerate(self.config_chain, 1):
            priority = "HIGHEST" if i == len(self.config_chain) else f"Level {i}"
            lines.append(f"{i}. {priority}: {path}")
            lines.append(f"   project_type: {config.get('project_type', 'N/A')}")
            lines.append(f"   language: {config.get('language', 'N/A')}")

            if 'structure' in config:
                file_types = ', '.join(config['structure'].keys())
                lines.append(f"   file_types: {file_types}")
            lines.append("")

        return "\n".join(lines)


def resolve_config(project_path: Path) -> Dict[str, Any]:
    """
    Convenience function to resolve configuration.

    Args:
        project_path: Project directory to start lookup from

    Returns:
        Resolved configuration dictionary
    """
    resolver = ConfigResolver(project_path)
    return resolver.resolve()


# CLI for testing
if __name__ == '__main__':
    import sys
    import json

    if len(sys.argv) < 2:
        print("Usage: python config_resolver.py <project_path> [--show-order]")
        print("\nExample:")
        print("  python config_resolver.py /path/to/project")
        print("  python config_resolver.py /path/to/project --show-order")
        sys.exit(1)

    project_path = Path(sys.argv[1])
    show_order = '--show-order' in sys.argv

    try:
        resolver = ConfigResolver(project_path)
        config = resolver.resolve()

        if show_order:
            print(resolver.show_resolution_order())
            print("\nFinal Merged Configuration:")
            print("=" * 60)

        # Pretty print config (excluding internal fields)
        display_config = {k: v for k, v in config.items() if not k.startswith('_')}
        print(json.dumps(display_config, indent=2))

        if '_config_sources' in config:
            print("\nConfiguration Sources:")
            for i, source in enumerate(config['_config_sources'], 1):
                print(f"  {i}. {source}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)