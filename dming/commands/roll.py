import click
from rich.console import Console
from rich.text import Text

from dming import __version__
from dming.dice import DiceGroup, InvalidDiceError, RollDetails, roll_details
from dming.output import OutputFormat, format_option, render_record, resolve_format

FILTER_LABELS = {
    "kh": "keep highest",
    "kl": "keep lowest",
    "dh": "drop highest",
    "dl": "drop lowest",
}


def _plain_line(label: str, value: str | int, width: int) -> str:
    return f"{label + ':':<{width}} {value}"


def _plain_group(group: DiceGroup) -> str:
    rolls = ", ".join(map(str, group.rolls))
    if not group.filter_name:
        return rolls

    selected = ", ".join(map(str, group.selected)) or "none"
    rule = FILTER_LABELS[group.filter_name]
    return f"{rolls} -> {selected} ({rule} {group.filter_count})"


def _rich_group(group: DiceGroup) -> Text:
    line = Text(f"├─ {group.expression}: ", style="dim")
    for index, value in enumerate(group.rolls):
        if index:
            line.append(", ", style="dim")
        if index in group.selected_indices:
            line.append(str(value), style="bold green")
        else:
            line.append(str(value), style="strike dim red")

    if not group.filter_name:
        return line

    selected = ", ".join(map(str, group.selected)) or "none"
    rule = FILTER_LABELS[group.filter_name]
    line.append(" → ", style="bold yellow")
    line.append(selected, style="bold green")
    line.append(f" ({rule} {group.filter_count})", style="cyan")
    return line


def _show_plain_details(details: RollDetails) -> None:
    calculation = details.calculation.replace("+", " + ").replace("-", " - ")
    rows: list[tuple[str, str | int]] = [("Roll", details.expression)]
    rows.extend((group.expression, _plain_group(group)) for group in details.groups)
    rows.extend((("Calculation", calculation), ("Result", details.result)))
    width = max(len(label) + 1 for label, _ in rows)
    for label, value in rows:
        click.echo(_plain_line(label, value, width))


def _show_rich_details(details: RollDetails) -> None:
    calculation = details.calculation.replace("+", " + ").replace("-", " - ")
    console = Console()
    console.print("🎲", f"[bold magenta]{details.expression}[/]")
    for group in details.groups:
        console.print(_rich_group(group))
    console.print(f"├─ [dim]Calculation:[/] [cyan]{calculation}[/]")
    console.print(f"└─ [dim]Result:[/] [bold yellow]{details.result}[/]")


def _group_record(group: DiceGroup) -> dict[str, object]:
    return {
        "expression": group.expression,
        "rolls": group.rolls,
        "selected_indices": group.selected_indices,
        "selected": group.selected,
        "filter": group.filter_name,
        "filter_count": group.filter_count,
    }


def _roll_record(details: RollDetails, include_details: bool) -> dict[str, object]:
    record: dict[str, object] = {
        "expression": details.expression,
        "result": details.result,
    }
    if include_details:
        record.update(
            operation=details.operation,
            calculation=details.calculation,
            groups=tuple(_group_record(group) for group in details.groups),
        )
    return record


def _show_roll(details: RollDetails, include_details: bool, output_format: OutputFormat) -> None:
    if output_format in {OutputFormat.JSON, OutputFormat.CSV}:
        render_record(_roll_record(details, include_details), output_format)
    elif include_details and output_format is OutputFormat.PLAIN:
        _show_plain_details(details)
    elif include_details:
        _show_rich_details(details)
    elif output_format is OutputFormat.PLAIN:
        click.echo(details.result)
    else:
        Console().print(f"🎲 [bold yellow]{details.result}[/]")


@click.command("roll")
@click.argument("dice")
@click.option("-d", "--details", help="Show every roll and the calculation.", is_flag=True)
@click.option("--plain", help="Alias for --format plain.", is_flag=True)
@format_option
@click.version_option(__version__)
@click.pass_context
def roll_command(
    context: click.Context,
    dice: str,
    details: bool,
    plain: bool,
    output_format: str | None,
) -> None:
    """Roll a dice expression."""
    selected_format = resolve_format(context, output_format, plain=plain)
    try:
        _show_roll(roll_details(dice), details, selected_format)
    except InvalidDiceError as error:
        if selected_format is OutputFormat.RICH:
            Console(stderr=True).print(f"❌ [bold red]Invalid roll:[/] {error}")
        else:
            click.echo(f"Error: Invalid roll: {error}", err=True)
        raise click.exceptions.Exit(1) from error
