from collections.abc import Callable

import click

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
from dming.output import Cell, Column, Row, TableOutput, format_option, render_table, resolve_format

CONVERSION_TABLE_WIDTH = 36
POSITIVE_FLOAT = click.FloatRange(min=0, min_open=True)


def _numeric(value: Cell) -> int | float:
    if not isinstance(value, (int, float)):
        raise TypeError("conversion value must be numeric")
    return value


def _source(value: Cell) -> str:
    return f"{_numeric(value):.10f}".rstrip("0").rstrip(".")


def _converted(value: Cell) -> str:
    return f"{_numeric(value):.2f}"


def _distance_output(
    *,
    title: str,
    source_key: str,
    source_label: str,
    metric_key: str,
    metric_label: str,
    values: tuple[float, ...],
    metric_conversion: Callable[[float], float],
    square_conversion: Callable[[float], float],
) -> TableOutput:
    rows: tuple[Row, ...] = tuple(
        {
            source_key: value,
            metric_key: metric_conversion(value),
            "squares": square_conversion(value),
        }
        for value in values
    )
    return TableOutput(
        title=f"📏 {title}",
        columns=(
            Column(source_key, source_label, style="cyan", display=_source),
            Column(metric_key, metric_label, style="green", display=_converted),
            Column("squares", "Squares", style="yellow", display=_converted),
        ),
        rows=rows,
        width=CONVERSION_TABLE_WIDTH,
    )


def _values(custom: tuple[float, ...], defaults: tuple[float, ...]) -> tuple[float, ...]:
    return sorted_unique(custom) if custom else defaults


@click.group("convert")
def convert() -> None:
    """Convert common US customary measurements."""


@convert.command("inches")
@click.argument("values", type=POSITIVE_FLOAT, nargs=-1)
@format_option
@click.pass_context
def inches(context: click.Context, values: tuple[float, ...], output_format: str | None) -> None:
    """Convert inches to meters and 5-foot squares."""
    output = _distance_output(
        title="Inches to Meters",
        source_key="inches",
        source_label="Inches\n(in.)",
        metric_key="meters",
        metric_label="Meters\n(m.)",
        values=_values(values, DEFAULT_INCHES),
        metric_conversion=inches_to_meters,
        square_conversion=inches_to_squares,
    )
    render_table(output, resolve_format(context, output_format))


@convert.command("feet")
@click.argument("values", type=POSITIVE_FLOAT, nargs=-1)
@format_option
@click.pass_context
def feet(context: click.Context, values: tuple[float, ...], output_format: str | None) -> None:
    """Convert feet to meters and 5-foot squares."""
    output = _distance_output(
        title="Feet to Meters",
        source_key="feet",
        source_label="Feet\n(ft.)",
        metric_key="meters",
        metric_label="Meters\n(m.)",
        values=_values(values, DEFAULT_FEET),
        metric_conversion=feet_to_meters,
        square_conversion=feet_to_squares,
    )
    render_table(output, resolve_format(context, output_format))


@convert.command("miles")
@click.argument("values", type=POSITIVE_FLOAT, nargs=-1)
@format_option
@click.pass_context
def miles(context: click.Context, values: tuple[float, ...], output_format: str | None) -> None:
    """Convert miles to kilometers and 5-foot squares."""
    output = _distance_output(
        title="Miles to Kilometers",
        source_key="miles",
        source_label="Miles\n(mi.)",
        metric_key="kilometers",
        metric_label="Kilometers\n(km.)",
        values=_values(values, DEFAULT_MILES),
        metric_conversion=miles_to_kilometers,
        square_conversion=miles_to_squares,
    )
    render_table(output, resolve_format(context, output_format))


@convert.command("pounds")
@click.argument("values", type=POSITIVE_FLOAT, nargs=-1)
@format_option
@click.pass_context
def pounds(context: click.Context, values: tuple[float, ...], output_format: str | None) -> None:
    """Convert pounds to kilograms."""
    selected = _values(values, DEFAULT_POUNDS)
    output = TableOutput(
        title="⚖️ Pounds to Kilograms",
        columns=(
            Column("pounds", "Pounds (lb.)", style="cyan", display=_source),
            Column("kilograms", "Kilograms (kg.)", style="green", display=_converted),
        ),
        rows=tuple(
            {"pounds": value, "kilograms": pounds_to_kilograms(value)} for value in selected
        ),
        width=CONVERSION_TABLE_WIDTH,
    )
    render_table(output, resolve_format(context, output_format))
