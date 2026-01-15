"""Register the materialize_shell_command plugin with Pants."""

from jose.materialize_shell_command import rules as rules_module
from jose.materialize_shell_command import target_types as target_types_module


def target_types():
    """Register target types."""
    return [target_types_module.MaterializeShellCommand]


def rules():
    """Register rules."""
    return rules_module.rules()
