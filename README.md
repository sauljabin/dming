# DMing

DMing is a CLI (command-line interface) collection useful when running a TTRPG (tabletop role-playing games).

> *[DMing](https://en.wiktionary.org/wiki/DMing)([Dungeon Mastering](https://en.wiktionary.org/wiki/Dungeon_Mastering#English)): Performing as a dungeon master, or running a tabletop role-playing game, especially Dungeons & Dragons.*

## Installation

```sh
pipx install dming
```

## Usage

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

> [!NOTE]
> `kh`: keep highest \
> `kl`: keep lowest \
> `dh`: drop highest \
> `dl`: drop lowest

### Using the Library

<a href="https://pypi.org/project/dming"><img alt="PyPI - Version" src="https://img.shields.io/pypi/v/dming?label=dming"></a>


```python
from dming.dice import roll

operation, result = roll("1d20+2")
```

## Alternatives

* JavaScript: [Dice Roller & Parser](https://www.npmjs.com/package/dice-roller-parser).

## Development

Installing poetry:

```shell
pipx install poetry
```

Installing development dependencies:

```shell
poetry install
```

Run:

```shell
poetry run roll <dice>
```

## Release a new version

> Check https://python-poetry.org/docs/cli/#version

```shell
poetry run python -m scripts.bump --help
poetry run python -m scripts.bump <major|minor|patch>
```
