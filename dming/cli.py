import click
from rich.console import Console
from rich.table import Table
from rich.text import Text

from dming import __version__
from dming.dice import DiceGroup, InvalidDiceError, RollDetails, roll_details
from dming.probability import InvalidProbabilityError, parse_die, probability_rows

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


def _show_details(details: RollDetails, plain: bool) -> None:
    formula = details.formula.replace("+", " + ").replace("-", " - ")
    if plain:
        rows: list[tuple[str, str | int]] = [("Roll", details.expression)]
        rows.extend((group.expression, _plain_group(group)) for group in details.groups)
        rows.extend((("Math", formula), ("Result", details.result)))
        width = max(len(label) + 1 for label, _ in rows)
        for label, value in rows:
            click.echo(_plain_line(label, value, width))
        return
    console = Console()
    console.print("🎲", f"[bold magenta]{details.expression}[/]")
    for group in details.groups:
        console.print(_rich_group(group))
    console.print(f"├─ [dim]Math:[/] [cyan]{formula}[/]")
    console.print(f"└─ [dim]Result:[/] [bold yellow]{details.result}[/]")


def _show_result(result: int, plain: bool) -> None:
    if plain:
        click.echo(result)
        return
    Console().print(f"🎲 [bold yellow]{result}[/]")


def _percentage(value: float) -> str:
    return f"{value:.2%}"


def _show_probability_table(dice: str, min_target: int, max_target: int | None) -> None:
    spec = parse_die(dice)
    rows = probability_rows(spec, min_target, max_target)
    table = Table(title=f"🎲 Probability · {spec.expression}", header_style="bold magenta")
    table.add_column("Target", justify="right", style="bold")
    table.add_column(spec.expression, justify="right", style="cyan")
    table.add_column("Advantage", justify="right", style="green")
    table.add_column("Disadvantage", justify="right", style="red")
    for row in rows:
        table.add_row(
            str(row.target),
            _percentage(row.standard),
            _percentage(row.advantage),
            _percentage(row.disadvantage),
        )
    Console().print(table)


@click.command()
@click.argument("dice")
@click.option("-d", "--details", help="Show every roll and the complete formula.", is_flag=True)
@click.option("--plain", help="Disable styling and emojis for plain-text output.", is_flag=True)
@click.version_option(__version__)
def _roll(dice: str, details: bool, plain: bool) -> None:
    """
    Allows you to roll dice from your terminal.

    \b
    Examples:
         roll 1d20    # roll a d20 die
         roll 1d100   # roll a d100 die
         roll 2d20kh1 # roll with advantage
         roll 2d20kl1 # roll with disadvantage
         roll 2d20dl1 # roll with advantage
         roll 2d20dh1 # roll with disadvantage
         roll 1d20+4  # roll a d20 die with a +4 modifier
         roll 1d20-4  # roll a d20 die with a -4 modifier
    """
    try:
        rolled = roll_details(dice)
        if details:
            _show_details(rolled, plain)
        else:
            _show_result(rolled.result, plain)
    except InvalidDiceError as e:
        if plain:
            raise click.ClickException(f"Invalid roll: {e}") from e
        Console(stderr=True).print(f"❌ [bold red]Invalid roll:[/] {e}")
        raise click.exceptions.Exit(1) from e


@click.command("table")
@click.argument("dice")
@click.option(
    "--min-target",
    type=click.IntRange(min=1),
    default=1,
    show_default=True,
    help="First target to include.",
)
@click.option(
    "--max-target",
    type=click.IntRange(min=1),
    help="Last target to include.",
)
def _table(dice: str, min_target: int, max_target: int | None) -> None:
    """Show success probabilities for a single die and optional modifier."""
    try:
        _show_probability_table(dice, min_target, max_target)
    except InvalidProbabilityError as e:
        Console(stderr=True).print(f"❌ [bold red]Invalid probability table:[/] {e}")
        raise click.exceptions.Exit(1) from e


@click.group()
@click.version_option(__version__)
def dming() -> None:
    """Tools for running tabletop role-playing games."""


dming.add_command(_roll, name="roll")
dming.add_command(_table)
