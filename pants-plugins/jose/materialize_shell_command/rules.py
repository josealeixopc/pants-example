"""Rules for materialize_shell_command."""

import logging
import os

from pants.core.util_rules.system_binaries import BashBinary
from pants.engine.console import Console
from pants.engine.env_vars import EnvironmentVars, EnvironmentVarsRequest
from pants.engine.fs import Workspace
from pants.engine.goal import Goal, GoalSubsystem
from pants.engine.intrinsics import run_interactive_process
from pants.engine.process import InteractiveProcess
from pants.engine.rules import Get, collect_rules, goal_rule
from pants.engine.target import Targets

from .target_types import (
    MaterializeShellCommand,
    MaterializeShellCommandCommandField,
    MaterializeShellCommandExecutionDependenciesField,
    MaterializeShellCommandExtraEnvVarsField,
    MaterializeShellCommandLogOutputField,
    MaterializeShellCommandOutputDirectoriesField,
    MaterializeShellCommandOutputFilesField,
    MaterializeShellCommandTimeoutField,
    MaterializeShellCommandToolsField,
)

logger = logging.getLogger(__name__)


class MaterializeSubsystem(GoalSubsystem):
    """Materialize generated files to the workspace."""

    name = "materialize"
    help = "Run materialize_shell_command targets to generate files directly in the workspace."


class Materialize(Goal):
    """Goal for materializing files to workspace."""

    subsystem_cls = MaterializeSubsystem
    environment_behavior = Goal.EnvironmentBehavior.LOCAL_ONLY


@goal_rule
async def materialize_workspace_files(
    targets: Targets,
    console: Console,
    bash: BashBinary,
    workspace: Workspace,
) -> Materialize:
    """Materialize files from materialize_shell_command targets to workspace."""

    # Filter for materialize_shell_command targets
    materialize_targets = [
        tgt for tgt in targets if tgt.has_field(MaterializeShellCommandCommandField)
    ]

    if not materialize_targets:
        console.print_stderr("No materialize_shell_command targets found.")
        return Materialize(exit_code=0)

    console.print_stdout(f"Materializing {len(materialize_targets)} target(s)...")

    for target in materialize_targets:
        # Access fields directly from target
        command_field = target[MaterializeShellCommandCommandField]
        execution_deps_field = target[MaterializeShellCommandExecutionDependenciesField]
        output_files_field = target[MaterializeShellCommandOutputFilesField]
        output_dirs_field = target[MaterializeShellCommandOutputDirectoriesField]
        timeout_field = target[MaterializeShellCommandTimeoutField]
        tools_field = target[MaterializeShellCommandToolsField]
        extra_env_vars_field = target[MaterializeShellCommandExtraEnvVarsField]
        log_output_field = target[MaterializeShellCommandLogOutputField]

        # Get environment variables
        extra_env_vars = extra_env_vars_field.value or ()
        env_var_names = []
        explicit_env_vars = {}

        for env_var in extra_env_vars:
            if "=" in env_var:
                key, value = env_var.split("=", 1)
                explicit_env_vars[key] = value
            else:
                env_var_names.append(env_var)

        env_vars = await Get(EnvironmentVars, EnvironmentVarsRequest(env_var_names))
        all_env_vars = {**env_vars, **explicit_env_vars}

        # Get the directory containing the BUILD file (relative to repo root)
        target_dir = os.path.dirname(target.address.spec_path)

        # The working directory is relative to the current directory
        # InteractiveProcess with run_in_workspace=True runs from the repo root
        full_workdir = target_dir if target_dir else "."

        log_output = log_output_field.value
        command = command_field.value

        if log_output:
            console.print_stdout(f"Running {target.address}: {command}")
            console.print_stdout(f"  Working directory: {full_workdir}")

        # Create an interactive process that runs in the workspace
        interactive_process = InteractiveProcess(
            argv=[bash.path, "-c", f"cd '{full_workdir}' && {command}"],
            env=all_env_vars,
            run_in_workspace=True,
        )

        # Execute the process using the recommended intrinsic
        result = await run_interactive_process(interactive_process)

        if result.exit_code != 0:
            console.print_stderr(
                f"Command failed for {target.address} with exit code {result.exit_code}"
            )
            return Materialize(exit_code=result.exit_code)

        # Log the generated files and directories
        output_files = output_files_field.value or ()
        output_directories = output_dirs_field.value or ()

        if log_output or output_files or output_directories:
            for output_file in output_files:
                file_path = os.path.join(target_dir, output_file) if target_dir else output_file
                console.print_stdout(f"  Generated file: {file_path}")

            for output_dir in output_directories:
                dir_path = os.path.join(target_dir, output_dir) if target_dir else output_dir
                console.print_stdout(f"  Generated directory: {dir_path}")

    console.print_stdout(f"✓ Successfully materialized {len(materialize_targets)} target(s)")
    return Materialize(exit_code=0)


def rules():
    """Return all rules for materialize_shell_command."""
    return collect_rules()
