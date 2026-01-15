"""Register the package_v2_shell_command plugin with Pants."""

from jose.package_v2_shell_command import rules as rules_module
from jose.package_v2_shell_command import target_types as target_types_module


def target_types():
    """Register target types."""
    return [target_types_module.PackageV2ShellCommand]


def rules():
    """Register rules."""
    return rules_module.rules()
