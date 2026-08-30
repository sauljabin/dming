import csv
import io
import json
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from enum import StrEnum
from typing import Literal, cast

import click
from rich.console import Console
from rich.table import Table


class OutputFormat(StrEnum):
    RICH = "rich"
    PLAIN = "plain"
    JSON = "json"
    CSV = "csv"


@dataclass(frozen=True)
class GlobalOptions:
    output_format: OutputFormat | None


type Cell = str | int | float | None
type Row = dict[str, Cell]


def _display(value: Cell) -> str:
    return "" if value is None else str(value)


@dataclass(frozen=True)
class Column:
    key: str
    label: str
    justify: Literal["left", "center", "right"] = "right"
    style: str = ""
    display: Callable[[Cell], str] = _display


@dataclass(frozen=True)
class TableOutput:
    title: str
    columns: tuple[Column, ...]
    rows: tuple[Row, ...]
    width: int | None = None
    min_width: int | None = None


def format_option[Command: Callable[..., object]](command: Command) -> Command:
    option = click.option(
        "--format",
        "output_format",
        type=click.Choice(tuple(OutputFormat), case_sensitive=False),
        help="Choose rich, plain, JSON, or CSV output.",
    )
    return cast(Command, option(command))


def resolve_format(
    context: click.Context,
    local_format: str | None,
    *,
    plain: bool = False,
) -> OutputFormat:
    root_options = context.find_root().obj
    global_format = root_options.output_format if isinstance(root_options, GlobalOptions) else None
    selected = OutputFormat(local_format) if local_format is not None else global_format
    if plain:
        if selected not in {None, OutputFormat.PLAIN}:
            raise click.UsageError("--plain cannot be combined with a non-plain --format")
        return OutputFormat.PLAIN
    return selected or OutputFormat.RICH


def _machine_value(value: object) -> object:
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return "" if value is None else value


def _render_json(value: object) -> None:
    click.echo(json.dumps(value, ensure_ascii=False, indent=2))


def _render_csv(rows: tuple[Mapping[str, object], ...], fieldnames: tuple[str, ...]) -> None:
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    for row in rows:
        writer.writerow({key: _machine_value(row.get(key)) for key in fieldnames})
    click.echo(stream.getvalue(), nl=False)


def render_record(record: dict[str, object], output_format: OutputFormat) -> None:
    if output_format is OutputFormat.JSON:
        _render_json(record)
        return
    if output_format is OutputFormat.CSV:
        _render_csv((record,), tuple(record))
        return
    raise ValueError(f"record rendering does not support {output_format}")


def render_table(output: TableOutput, output_format: OutputFormat) -> None:
    if output_format is OutputFormat.JSON:
        _render_json(output.rows)
        return
    if output_format is OutputFormat.CSV:
        _render_csv(output.rows, tuple(column.key for column in output.columns))
        return
    if output_format is OutputFormat.PLAIN:
        click.echo("\t".join(column.label.replace("\n", " ") for column in output.columns))
        for row in output.rows:
            click.echo("\t".join(column.display(row[column.key]) for column in output.columns))
        return

    table = Table(
        title=output.title,
        header_style="bold magenta",
        width=output.width,
        min_width=output.min_width,
    )
    for column in output.columns:
        table.add_column(
            column.label,
            justify=column.justify,
            style=column.style,
        )
    for row in output.rows:
        table.add_row(*(column.display(row[column.key]) for column in output.columns))
    Console().print(table)
