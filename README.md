# DMing

DMing is a CLI (command-line interface) collection useful when running a TTRPG (tabletop role-playing game).

## Installation

```sh
pipx install dming
```

## Usage

DMing provides a grouped command for all tools. The standalone `roll` command
remains available as a shortcut for `dming roll`. Every leaf command supports
`--format rich|plain|json|csv`; the default is `rich`. The option can appear on
the root command or the leaf command, and the leaf value takes precedence.

```console
$ dming --format json rules advancement
$ dming chance d20 --format csv
```

### Roll Dice

> [!WARNING]
> DMing supports part of the [Roll20 Dice Specification](https://help.roll20.net/hc/en-us/articles/360037773133-Dice-Reference).

Use the command `roll <dice>`.

Examples:

* `roll 1d20`: roll a d20 die
* `roll 1d100`: roll a d100 die
* `roll 2d20kh1`: roll with advantage
* `roll 2d20kl1`: roll with disadvantage
* `roll 2d20dl1`: roll with advantage
* `roll 2d20dh1`: roll with disadvantage
* `roll 1d20+4`: roll a d20 die with a +4 modifier
* `roll 1d20-4`: roll a d20 die with a -4 modifier

Add `-d` or `--details` to show every die, which dice were selected by a keep or
drop filter, and the complete calculation. Use `--plain` as a shortcut
for `--format plain`. JSON emits one object; CSV emits one result row and stores
detailed groups as compact JSON in a quoted cell.

```console
$ roll --details 2d20kh1
🎲 2d20kh1
├─ 2d20kh1: 19, 9 → 19 (keep highest 1)
├─ Calculation: 19
└─ Result: 19

$ roll --details 2d20
🎲 2d20
├─ 2d20: 4, 4
├─ Calculation: 4 + 4
└─ Result: 8

$ roll --details --plain 2d20
Roll:        2d20
2d20:        4, 4
Calculation: 4 + 4
Result:      8
```

> [!NOTE]
> `kh`: keep highest \
> `kl`: keep lowest \
> `dh`: drop highest \
> `dl`: drop lowest

### Chance Tables

Use `dming chance <die>` to show the chance of meeting or exceeding each target
with a standard roll, advantage, or disadvantage. Tables support one die with
an optional modifier. The `Roll Needed` column shows the lowest natural roll
that reaches each target.

```console
$ dming chance d20
$ dming chance d20+5
$ dming chance d20-3 --min-target 5 --max-target 30
```

The default range starts at target 1 and ends at the greater of the die size or
the highest modified total. Override either boundary with `--min-target` and
`--max-target`. Percentages use ordinary threshold rules; natural minimum and
maximum rolls do not introduce automatic failure or success rules.

### Unit Conversions

Use a unit-specific `dming convert` command to convert common US customary
measurements to metric units.

```console
$ dming convert inches
$ dming convert feet
$ dming convert miles
$ dming convert pounds
```

The `Squares` column expresses each distance as a number of 5-foot grid spaces.
Pounds are converted to kilograms. Measurement units appear in the table
headers, such as `(ft.)`, `(m.)`, `(lb.)`, and `(kg.)`.

Supply one or more values as positional arguments to build a custom table.
Values must be positive and are sorted and deduplicated.

```console
$ dming convert feet 5 30
$ dming convert inches 6 12
$ dming convert pounds 2.5 10
```

### SRD 5.2.1 Rules References

Use `dming rules` for fifth-edition reference tables from SRD 5.2.1.

```console
$ dming rules abilities
$ dming rules advancement
$ dming rules carrying
$ dming rules difficulty
$ dming rules proficiency
$ dming rules sizes
```

The source tables are available in the
[System Reference Document 5.2.1](https://www.dndbeyond.com/srd). Character
Advancement includes levels 1–20, cumulative XP thresholds, and proficiency
bonuses.

Creature sizes also include metric dimensions. Carrying-capacity entries also
include kilogram equivalents for carrying and for dragging, lifting, or pushing.

### Using the Library

<a href="https://pypi.org/project/dming"><img alt="PyPI - Version" src="https://img.shields.io/pypi/v/dming?label=dming"></a>


```python
from dming.dice import roll

operation, result = roll("1d20+2")
```

## Alternatives

* JavaScript: [Dice Roller & Parser](https://www.npmjs.com/package/dice-roller-parser).

## Development

For development instructions, see the [DMing development guide](DEVELOPMENT.md).

## Releases

GitHub Releases are the canonical release history. See [DMing releases](https://github.com/sauljabin/dming/releases) for release notes and downloadable artifacts.

## Licensing

DMing's original code is available under the MIT License. SRD-derived reference
data is available under CC BY 4.0; see [NOTICE.md](NOTICE.md) for attribution and
details about modifications.

> This work includes material from the System Reference Document 5.2.1 (“SRD
> 5.2.1”) by Wizards of the Coast LLC, available at
> https://www.dndbeyond.com/srd. The SRD 5.2.1 is licensed under the Creative
> Commons Attribution 4.0 International License, available at
> https://creativecommons.org/licenses/by/4.0/legalcode.

## AI Assistance

This project uses AI-assisted development tools. Some code and documentation
may be generated or revised with AI assistance. All AI-assisted changes are
reviewed and tested by the maintainer before they are included.
