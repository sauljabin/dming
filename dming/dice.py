import random
import re
from dataclasses import dataclass


def kh(n: int, dice: list[int]) -> list[int]:
    return sorted(dice, reverse=True)[:n]


def kl(n: int, dice: list[int]) -> list[int]:
    return sorted(dice)[:n]


def dh(n: int, dice: list[int]) -> list[int]:
    return sorted(dice, reverse=True)[n:]


def dl(n: int, dice: list[int]) -> list[int]:
    return sorted(dice)[n:]


FILTERS = {"kh": kh, "kl": kl, "dh": dh, "dl": dl}


class InvalidDiceError(ValueError):
    pass


@dataclass(frozen=True)
class DiceGroup:
    expression: str
    rolls: tuple[int, ...]
    selected_indices: tuple[int, ...]
    selected: tuple[int, ...]
    filter_name: str | None
    filter_count: int


@dataclass(frozen=True)
class RollDetails:
    expression: str
    operation: str
    formula: str
    result: int
    groups: tuple[DiceGroup, ...]


def _selected_indices(filter_name: str | None, count: int, rolls: list[int]) -> set[int]:
    if filter_name is None:
        return set(range(len(rolls)))

    reverse = filter_name in {"kh", "dh"}
    ranked = sorted(range(len(rolls)), key=lambda index: rolls[index], reverse=reverse)
    if filter_name.startswith("k"):
        return set(ranked[:count])
    return set(ranked[count:])


def roll_details(dice: str) -> RollDetails:
    groups: list[DiceGroup] = []

    def replacer(expression: re.Match[str]) -> str:
        total, die, filter_name, total_keep = expression.groups()
        rolls = [random.randint(1, int(die)) for _ in range(int(total) if total else 1)]
        filter_count = int(total_keep) if total_keep else 1
        selected_indices = _selected_indices(filter_name, filter_count, rolls)
        selected = tuple(roll for index, roll in enumerate(rolls) if index in selected_indices)
        groups.append(
            DiceGroup(
                expression=expression.group(0),
                rolls=tuple(rolls),
                selected_indices=tuple(sorted(selected_indices)),
                selected=selected,
                filter_name=filter_name,
                filter_count=filter_count,
            )
        )
        return str(sum(selected))

    operation = re.sub(r"(\d+)?d(\d+)(kh|kl|dh|dl)?(\d+)?", replacer, dice)

    if not re.fullmatch(r"[0-9+-]+", operation):
        raise InvalidDiceError("not allowed characters")

    group_iterator = iter(groups)

    def formula_replacer(expression: re.Match[str]) -> str:
        selected = next(group_iterator).selected
        formula = "+".join(str(value) for value in selected) or "0"
        if expression.start() > 0 and dice[expression.start() - 1] == "-" and len(selected) > 1:
            return f"({formula})"
        return formula

    formula = re.sub(r"(\d+)?d(\d+)(kh|kl|dh|dl)?(\d+)?", formula_replacer, dice)

    return RollDetails(
        expression=dice,
        operation=operation,
        formula=formula,
        result=eval(operation),
        groups=tuple(groups),
    )


def roll(dice: str) -> tuple[str, int]:
    details = roll_details(dice)
    return details.operation, details.result
