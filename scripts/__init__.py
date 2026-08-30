import shlex
import subprocess
import sys
from collections.abc import Mapping, Sequence

from rich.console import Console


class CommandProcessor:
    def __init__(
        self,
        commands: Mapping[str, Sequence[str]],
        rollback: Mapping[str, Sequence[str]] | None = None,
    ) -> None:
        self.commands = commands
        self.rollback = rollback or {}
        self.console = Console()

    def run(self) -> str:
        output = ""
        for name, command in self.commands.items():
            result = self.execute_command(name, command)
            if result.returncode:
                display = shlex.join(command)
                self.console.print(
                    "\n[bold red]Error[/] when executing "
                    f'[bold blue]"{name}" ([bold yellow]{display}[/])[/]:exclamation::\n'
                    f"[red]{result.stdout}{result.stderr}[/]\n"
                )

                if self.rollback:
                    self.console.print("[bold yellow]Rolling back:[/]")
                    for rollback_name, rollback_command in self.rollback.items():
                        self.execute_command(rollback_name, rollback_command)

                sys.exit(result.returncode)
            else:
                output += result.stdout

        return output

    def execute_command(
        self,
        name: str,
        command: Sequence[str],
    ) -> subprocess.CompletedProcess[str]:
        self.console.print()
        self.console.print(f"[bold blue]{name.lower()}:")
        self.console.print(f"[bold yellow]{shlex.join(command)}[/]")
        return subprocess.run(command, capture_output=True, text=True, check=False)
