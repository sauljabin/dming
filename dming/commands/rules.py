import click

from dming.conversion import pounds_to_kilograms
from dming.output import Cell, Column, Row, TableOutput, format_option, render_table, resolve_format
from dming.rules import (
    ABILITY_MODIFIERS,
    CARRYING_CAPACITIES,
    CREATURE_SIZES,
    DIFFICULTY_CLASSES,
    LEVEL_ADVANCEMENT,
    PROFICIENCY_BONUSES,
)


def _numeric(value: Cell) -> int | float:
    if not isinstance(value, (int, float)):
        raise TypeError("rule value must be numeric")
    return value


def _signed(value: Cell) -> str:
    return f"{int(_numeric(value)):+d}".replace("-", "−")


def _number(value: Cell) -> str:
    return f"{_numeric(value):.10f}".rstrip("0").rstrip(".")


def _multiplier(value: Cell) -> str:
    return f"Str. × {_number(value)}"


def _metric_multiplier(value: Cell) -> str:
    return f"Str. × {_numeric(value):.2f}"


def _rules_output(
    title: str,
    columns: tuple[Column, ...],
    rows: tuple[Row, ...],
) -> TableOutput:
    table_title = f"📖 {title} · SRD 5.2.1"
    return TableOutput(
        title=table_title,
        columns=columns,
        rows=rows,
        min_width=len(table_title) + 2,
    )


@click.group("rules", invoke_without_command=True)
@click.pass_context
def rules(context: click.Context) -> None:
    """Show fifth-edition reference tables from SRD 5.2.1."""
    if context.invoked_subcommand is None:
        click.echo(context.get_help())


@rules.command("abilities")
@format_option
@click.pass_context
def abilities(context: click.Context, output_format: str | None) -> None:
    """Show ability scores and their modifiers."""
    output = _rules_output(
        "Ability Modifiers",
        (
            Column("score", "Score", style="cyan"),
            Column("modifier", "Modifier", style="green", display=_signed),
        ),
        tuple({"score": score, "modifier": modifier} for score, modifier in ABILITY_MODIFIERS),
    )
    render_table(output, resolve_format(context, output_format))


@rules.command("advancement")
@format_option
@click.pass_context
def advancement(context: click.Context, output_format: str | None) -> None:
    """Show experience thresholds and proficiency bonuses by level."""
    output = _rules_output(
        "Character Advancement",
        (
            Column("level", "Level", style="cyan"),
            Column("experience_points", "Experience Points", style="green"),
            Column("proficiency_bonus", "Proficiency Bonus", style="yellow", display=_signed),
        ),
        tuple(
            {
                "level": level,
                "experience_points": experience,
                "proficiency_bonus": bonus,
            }
            for level, experience, bonus in LEVEL_ADVANCEMENT
        ),
    )
    render_table(output, resolve_format(context, output_format))


@rules.command("difficulty")
@format_option
@click.pass_context
def difficulty(context: click.Context, output_format: str | None) -> None:
    """Show typical Difficulty Classes."""
    output = _rules_output(
        "Typical Difficulty Classes",
        (
            Column("difficulty", "Task Difficulty", justify="left", style="cyan"),
            Column("difficulty_class", "DC", style="green"),
        ),
        tuple(
            {"difficulty": difficulty_name, "difficulty_class": difficulty_class}
            for difficulty_name, difficulty_class in DIFFICULTY_CLASSES
        ),
    )
    render_table(output, resolve_format(context, output_format))


@rules.command("proficiency")
@format_option
@click.pass_context
def proficiency(context: click.Context, output_format: str | None) -> None:
    """Show Proficiency Bonus by level or Challenge Rating."""
    output = _rules_output(
        "Proficiency Bonus",
        (
            Column("level_or_cr", "Level or CR", style="cyan"),
            Column("bonus", "Bonus", style="green", display=_signed),
        ),
        tuple({"level_or_cr": level, "bonus": bonus} for level, bonus in PROFICIENCY_BONUSES),
    )
    render_table(output, resolve_format(context, output_format))


@rules.command("sizes")
@format_option
@click.pass_context
def sizes(context: click.Context, output_format: str | None) -> None:
    """Show creature sizes and the space they control."""
    output = _rules_output(
        "Creature Size and Space",
        (
            Column("size", "Size", justify="left", style="cyan"),
            Column("space_feet", "Space (ft.)", style="green"),
            Column("space_meters", "Space (m.)", style="green"),
            Column("space_squares", "Space (Squares)", style="green"),
        ),
        tuple(
            {
                "size": size,
                "space_feet": feet,
                "space_meters": meters,
                "space_squares": squares,
            }
            for size, feet, meters, squares in CREATURE_SIZES
        ),
    )
    render_table(output, resolve_format(context, output_format))


@rules.command("carrying")
@format_option
@click.pass_context
def carrying(context: click.Context, output_format: str | None) -> None:
    """Show carrying and drag, lift, or push capacity by creature size."""
    rows: tuple[Row, ...] = tuple(
        {
            "creature_size": size,
            "carry_pounds_multiplier": carry,
            "carry_kilograms_multiplier": pounds_to_kilograms(carry),
            "drag_lift_push_pounds_multiplier": drag,
            "drag_lift_push_kilograms_multiplier": pounds_to_kilograms(drag),
        }
        for size, carry, drag in CARRYING_CAPACITIES
    )
    output = _rules_output(
        "Carrying Capacity",
        (
            Column("creature_size", "Creature Size", justify="left", style="cyan"),
            Column("carry_pounds_multiplier", "Carry\n(lb.)", style="green", display=_multiplier),
            Column(
                "carry_kilograms_multiplier",
                "Carry\n(kg.)",
                style="green",
                display=_metric_multiplier,
            ),
            Column(
                "drag_lift_push_pounds_multiplier",
                "Drag/Lift/Push\n(lb.)",
                style="green",
                display=_multiplier,
            ),
            Column(
                "drag_lift_push_kilograms_multiplier",
                "Drag/Lift/Push\n(kg.)",
                style="green",
                display=_metric_multiplier,
            ),
        ),
        rows,
    )
    render_table(output, resolve_format(context, output_format))
