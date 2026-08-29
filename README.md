# DMing

DMing is a CLI (command-line interface) collection useful when running a TTRPG (tabletop role-playing game).

> *[DMing](https://en.wiktionary.org/wiki/DMing)([Dungeon Mastering](https://en.wiktionary.org/wiki/Dungeon_Mastering#English)): Performing as a dungeon master, or running a tabletop role-playing game, especially Dungeons & Dragons.*

## Installation

```sh
pipx install dming
```

## Usage

DMing provides a grouped command for all tools. The standalone `roll` command
remains available as a shortcut for `dming roll`.

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
drop filter, and the complete arithmetic formula. Use `--plain` for output
without styling or emojis.

```console
$ roll --details 2d20kh1
🎲 2d20kh1
├─ 2d20kh1: 19, 9 → 19 (keep highest 1)
├─ Math: 19
└─ Result: 19

$ roll --details 2d20
🎲 2d20
├─ 2d20: 4, 4
├─ Math: 4 + 4
└─ Result: 8

$ roll --details --plain 2d20
Roll:   2d20
2d20:   4, 4
Math:   4 + 4
Result: 8
```

> [!NOTE]
> `kh`: keep highest \
> `kl`: keep lowest \
> `dh`: drop highest \
> `dl`: drop lowest

### Probability Tables

Use `dming table <die>` to show the chance of meeting or exceeding each target
with a standard roll, advantage, or disadvantage. Tables support one die with
an optional modifier.

```console
$ dming table d20
$ dming table d20+5
$ dming table d20-3 --min-target 5 --max-target 30
```

The default range starts at target 1 and ends at the greater of the die size or
the highest modified total. Override either boundary with `--min-target` and
`--max-target`. Percentages use ordinary threshold rules; natural minimum and
maximum rolls do not introduce automatic failure or success rules.

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
