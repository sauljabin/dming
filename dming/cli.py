from collections.abc import Callable

import click
from rich.console import Console
from rich.table import Table
from rich.text import Text

from dming import __version__
from dming.conversion import (
    DEFAULT_FEET,
    DEFAULT_INCHES,
    DEFAULT_MILES,
    DEFAULT_POUNDS,
    feet_to_meters,
    feet_to_squares,
    inches_to_meters,
    inches_to_squares,
    miles_to_kilometers,
    miles_to_squares,
    pounds_to_kilograms,
    sorted_unique,
)
from dming.dice import DiceGroup, InvalidDiceError, RollDetails, roll_details
from dming.probability import InvalidProbabilityError, parse_die, probability_rows
from dming.rules import (
    ABILITY_MODIFIERS,
    CARRYING_CAPACITIES,
    CREATURE_SIZES,
    DIFFICULTY_CLASSES,
    PROFICIENCY_BONUSES,
)

FILTER_LABELS = {
    "kh": "keep highest",
    "kl": "keep lowest",
    "dh": "drop highest",
    "dl": "drop lowest",
}
CONVERSION_TABLE_WIDTH = 36


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


def _minimum_roll(value: int | None) -> str:
    if value is None:
        return "Impossible"
    return f"{value}+"


def _show_chance_table(dice: str, min_target: int, max_target: int | None) -> None:
    spec = parse_die(dice)
    rows = probability_rows(spec, min_target, max_target)
    table = Table(title=f"🎲 Chance · {spec.expression}", header_style="bold magenta")
    table.add_column("Target", justify="right", style="bold")
    table.add_column("Roll Needed", justify="right", style="yellow")
    table.add_column(spec.expression, justify="right", style="cyan")
    table.add_column("Advantage", justify="right", style="green")
    table.add_column("Disadvantage", justify="right", style="red")
    for row in rows:
        table.add_row(
            str(row.target),
            _minimum_roll(row.minimum_roll),
            _percentage(row.standard),
            _percentage(row.advantage),
            _percentage(row.disadvantage),
        )
    Console().print(table)


def _format_source(value: float) -> str:
    return f"{value:.10f}".rstrip("0").rstrip(".")


def _distance_table(
    title: str,
    source_label: str,
    metric_label: str,
    values: tuple[float, ...],
    metric_conversion: Callable[[float], float],
    square_conversion: Callable[[float], float],
) -> Table:
    table = Table(
        title=f"📏 {title}",
        header_style="bold magenta",
        width=CONVERSION_TABLE_WIDTH,
    )
    table.add_column(source_label, justify="right", style="cyan")
    table.add_column(metric_label, justify="right", style="green")
    table.add_column("Squares", justify="right", style="yellow")
    for value in values:
        table.add_row(
            _format_source(value),
            f"{metric_conversion(value):.2f}",
            f"{square_conversion(value):.2f}",
        )
    return table


def _show_distance_tables(
    inches: tuple[float, ...],
    feet: tuple[float, ...],
    miles: tuple[float, ...],
) -> None:
    custom_values = bool(inches or feet or miles)
    tables = []
    if inches or not custom_values:
        values = sorted_unique(inches) if inches else DEFAULT_INCHES
        tables.append(
            _distance_table(
                "Inches to Meters",
                "Inches\n(in.)",
                "Meters\n(m.)",
                values,
                inches_to_meters,
                inches_to_squares,
            )
        )
    if feet or not custom_values:
        values = sorted_unique(feet) if feet else DEFAULT_FEET
        tables.append(
            _distance_table(
                "Feet to Meters",
                "Feet\n(ft.)",
                "Meters\n(m.)",
                values,
                feet_to_meters,
                feet_to_squares,
            )
        )
    if miles or not custom_values:
        values = sorted_unique(miles) if miles else DEFAULT_MILES
        tables.append(
            _distance_table(
                "Miles to Kilometers",
                "Miles\n(mi.)",
                "Kilometers\n(km.)",
                values,
                miles_to_kilometers,
                miles_to_squares,
            )
        )

    console = Console()
    for index, table in enumerate(tables):
        if index:
            console.print()
        console.print(table)


def _show_weight_table(pounds: tuple[float, ...]) -> None:
    values = sorted_unique(pounds) if pounds else DEFAULT_POUNDS
    table = Table(
        title="⚖️ Pounds to Kilograms",
        header_style="bold magenta",
        width=CONVERSION_TABLE_WIDTH,
    )
    table.add_column("Pounds (lb.)", justify="right", style="cyan")
    table.add_column("Kilograms (kg.)", justify="right", style="green")
    for value in values:
        table.add_row(
            _format_source(value),
            f"{pounds_to_kilograms(value):.2f}",
        )
    Console().print(table)


def _show_rules_table(
    title: str,
    columns: tuple[str, ...],
    rows: tuple[tuple[str, ...], ...],
    right_align_first: bool = False,
) -> None:
    table_title = f"📖 {title} · 2024"
    table = Table(
        title=table_title,
        header_style="bold magenta",
        min_width=len(table_title) + 2,
    )
    for index, column in enumerate(columns):
        style = "cyan" if index == 0 else "green"
        if index or right_align_first:
            table.add_column(column, justify="right", style=style)
        else:
            table.add_column(column, justify="left", style=style)
    for row in rows:
        table.add_row(*row)
    Console().print(table)


def _signed(value: int) -> str:
    return f"{value:+d}".replace("-", "−")


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


@click.command("chance")
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
def _chance(dice: str, min_target: int, max_target: int | None) -> None:
    """Show success chances for a single die and optional modifier."""
    try:
        _show_chance_table(dice, min_target, max_target)
    except InvalidProbabilityError as e:
        Console(stderr=True).print(f"❌ [bold red]Invalid chance table:[/] {e}")
        raise click.exceptions.Exit(1) from e


POSITIVE_FLOAT = click.FloatRange(min=0, min_open=True)


@click.group("convert")
def _convert() -> None:
    """Show US customary to metric conversion tables."""


@_convert.command("distance")
@click.option("--inch", "inches", type=POSITIVE_FLOAT, multiple=True, help="Custom inches.")
@click.option("--foot", "feet", type=POSITIVE_FLOAT, multiple=True, help="Custom feet.")
@click.option("--mile", "miles", type=POSITIVE_FLOAT, multiple=True, help="Custom miles.")
def _distance(
    inches: tuple[float, ...],
    feet: tuple[float, ...],
    miles: tuple[float, ...],
) -> None:
    """Convert distances and show their 5-foot Square equivalents."""
    _show_distance_tables(inches, feet, miles)


@_convert.command("weight")
@click.option("--pound", "pounds", type=POSITIVE_FLOAT, multiple=True, help="Custom pounds.")
def _weight(pounds: tuple[float, ...]) -> None:
    """Convert pounds to kilograms."""
    _show_weight_table(pounds)


@click.group("rules", invoke_without_command=True)
@click.pass_context
def _rules(context: click.Context) -> None:
    """Show official 2024 D&D rules reference tables."""
    if context.invoked_subcommand is None:
        click.echo(context.get_help())


@_rules.command("abilities")
def _abilities() -> None:
    """Show ability scores and their modifiers."""
    rows = tuple((score, _signed(modifier)) for score, modifier in ABILITY_MODIFIERS)
    _show_rules_table("Ability Modifiers", ("Score", "Modifier"), rows, right_align_first=True)


@_rules.command("difficulty")
def _difficulty() -> None:
    """Show typical Difficulty Classes."""
    rows = tuple((difficulty, str(dc)) for difficulty, dc in DIFFICULTY_CLASSES)
    _show_rules_table("Typical Difficulty Classes", ("Task Difficulty", "DC"), rows)


@_rules.command("proficiency")
def _proficiency() -> None:
    """Show Proficiency Bonus by level or Challenge Rating."""
    rows = tuple((level, _signed(bonus)) for level, bonus in PROFICIENCY_BONUSES)
    _show_rules_table("Proficiency Bonus", ("Level or CR", "Bonus"), rows, right_align_first=True)


@_rules.command("sizes")
def _sizes() -> None:
    """Show creature sizes and the space they control."""
    _show_rules_table(
        "Creature Size and Space",
        ("Size", "Space (ft.)", "Space (m.)", "Space (Squares)"),
        CREATURE_SIZES,
    )


@_rules.command("carrying")
def _carrying() -> None:
    """Show carrying and drag, lift, or push capacity by creature size."""
    rows = tuple(
        (
            size,
            f"Str. × {_format_source(carry)}",
            f"Str. × {pounds_to_kilograms(carry):.2f}",
            f"Str. × {_format_source(drag)}",
            f"Str. × {pounds_to_kilograms(drag):.2f}",
        )
        for size, carry, drag in CARRYING_CAPACITIES
    )
    _show_rules_table(
        "Carrying Capacity",
        (
            "Creature Size",
            "Carry\n(lb.)",
            "Carry\n(kg.)",
            "Drag/Lift/Push\n(lb.)",
            "Drag/Lift/Push\n(kg.)",
        ),
        rows,
    )


@click.group()
@click.version_option(__version__)
def dming() -> None:
    """Tools for running tabletop role-playing games."""


dming.add_command(_roll, name="roll")
dming.add_command(_chance)
dming.add_command(_convert)
dming.add_command(_rules)
