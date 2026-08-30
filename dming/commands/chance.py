import click

from dming.output import Cell, Column, Row, TableOutput, format_option, render_table, resolve_format
from dming.probability import InvalidProbabilityError, parse_die, probability_rows


def _percentage(value: Cell) -> str:
    if not isinstance(value, (int, float)):
        raise TypeError("percentage must be numeric")
    return f"{value:.2%}"


def _minimum_roll(value: Cell) -> str:
    return "Impossible" if value is None else f"{value}+"


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
@format_option
@click.pass_context
def chance(
    context: click.Context,
    dice: str,
    min_target: int,
    max_target: int | None,
    output_format: str | None,
) -> None:
    """Show success chances for a single die and optional modifier."""
    try:
        spec = parse_die(dice)
        rows: tuple[Row, ...] = tuple(
            {
                "target": row.target,
                "roll_needed": row.minimum_roll,
                "standard": row.standard,
                "advantage": row.advantage,
                "disadvantage": row.disadvantage,
            }
            for row in probability_rows(spec, min_target, max_target)
        )
    except InvalidProbabilityError as error:
        click.echo(f"Error: Invalid chance table: {error}", err=True)
        raise click.exceptions.Exit(1) from error

    output = TableOutput(
        title=f"🎲 Chance · {spec.expression}",
        columns=(
            Column("target", "Target", style="bold"),
            Column("roll_needed", "Roll Needed", style="yellow", display=_minimum_roll),
            Column("standard", spec.expression, style="cyan", display=_percentage),
            Column("advantage", "Advantage", style="green", display=_percentage),
            Column("disadvantage", "Disadvantage", style="red", display=_percentage),
        ),
        rows=rows,
    )
    render_table(output, resolve_format(context, output_format))
