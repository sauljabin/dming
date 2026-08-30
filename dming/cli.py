import click

from dming import __version__
from dming.commands import chance, convert, roll_command, rules
from dming.output import GlobalOptions, OutputFormat, format_option

_roll = roll_command


@click.group()
@format_option
@click.version_option(__version__)
@click.pass_context
def dming(context: click.Context, output_format: str | None) -> None:
    """Tools for running tabletop role-playing games."""
    selected = OutputFormat(output_format) if output_format is not None else None
    context.obj = GlobalOptions(output_format=selected)


dming.add_command(roll_command)
dming.add_command(chance)
dming.add_command(convert)
dming.add_command(rules)
