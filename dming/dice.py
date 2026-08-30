import random
import re
from dataclasses import dataclass


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
    calculation: str
    result: int
    groups: tuple[DiceGroup, ...]


@dataclass(frozen=True)
class _DiceTerm:
    sign: int
    expression: str
    count: int
    sides: int
    filter_name: str | None
    filter_count: int


@dataclass(frozen=True)
class _IntegerTerm:
    sign: int
    value: int


_DICE_TERM = re.compile(
    r"(?P<count>\d*)d(?P<sides>\d+)(?:(?P<filter>kh|kl|dh|dl)(?P<filter_count>\d*))?"
)


def _integer(value: str) -> int:
    try:
        return int(value)
    except ValueError as error:
        raise InvalidDiceError("number is too large") from error


def _parse_term(expression: str, sign: int) -> _DiceTerm | _IntegerTerm:
    if expression.isdigit():
        return _IntegerTerm(sign=sign, value=_integer(expression))

    match = _DICE_TERM.fullmatch(expression)
    if match is None:
        raise InvalidDiceError(f"invalid term: {expression}")

    count = _integer(match.group("count") or "1")
    sides = _integer(match.group("sides"))
    filter_name = match.group("filter")
    filter_count = _integer(match.group("filter_count") or "1")
    if count < 1:
        raise InvalidDiceError("dice count must be at least 1")
    if sides < 1:
        raise InvalidDiceError("die must have at least 1 side")
    if filter_name is not None and filter_count < 1:
        raise InvalidDiceError("filter count must be at least 1")
    if filter_name is not None and filter_count > count:
        raise InvalidDiceError("filter count cannot exceed dice count")

    return _DiceTerm(
        sign=sign,
        expression=expression,
        count=count,
        sides=sides,
        filter_name=filter_name,
        filter_count=filter_count,
    )


def _parse(expression: str) -> tuple[_DiceTerm | _IntegerTerm, ...]:
    compact = "".join(expression.split())
    if not compact:
        raise InvalidDiceError("roll expression cannot be empty")

    position = 0
    sign = 1
    if compact[0] in "+-":
        sign = -1 if compact[0] == "-" else 1
        position = 1
    if position == len(compact):
        raise InvalidDiceError("an operator must be followed by a term")

    terms: list[_DiceTerm | _IntegerTerm] = []
    while position < len(compact):
        end = position
        while end < len(compact) and compact[end] not in "+-":
            end += 1
        if end == position:
            raise InvalidDiceError("operators must appear between terms")

        terms.append(_parse_term(compact[position:end], sign))
        if end == len(compact):
            break

        sign = -1 if compact[end] == "-" else 1
        position = end + 1
        if position == len(compact):
            raise InvalidDiceError("an operator must be followed by a term")

    return tuple(terms)


def _selected_indices(filter_name: str | None, count: int, rolls: list[int]) -> set[int]:
    if filter_name is None:
        return set(range(len(rolls)))

    reverse = filter_name in {"kh", "dh"}
    ranked = sorted(range(len(rolls)), key=lambda index: rolls[index], reverse=reverse)
    if filter_name.startswith("k"):
        return set(ranked[:count])
    return set(ranked[count:])


def _signed_component(value: str, sign: int, first: bool) -> str:
    if first:
        return f"-{value}" if sign < 0 else value
    return f"{'-' if sign < 0 else '+'}{value}"


def roll_details(dice: str) -> RollDetails:
    terms = _parse(dice)
    groups: list[DiceGroup] = []
    operation_parts: list[str] = []
    calculation_parts: list[str] = []
    result = 0

    for term in terms:
        if isinstance(term, _IntegerTerm):
            value = term.value
            calculation = str(value)
        else:
            rolls = [random.randint(1, term.sides) for _ in range(term.count)]
            selected_indices = _selected_indices(term.filter_name, term.filter_count, rolls)
            selected = tuple(roll for index, roll in enumerate(rolls) if index in selected_indices)
            groups.append(
                DiceGroup(
                    expression=term.expression,
                    rolls=tuple(rolls),
                    selected_indices=tuple(sorted(selected_indices)),
                    selected=selected,
                    filter_name=term.filter_name,
                    filter_count=term.filter_count,
                )
            )
            value = sum(selected)
            calculation = "+".join(map(str, selected)) or "0"
            if term.sign < 0 and len(selected) > 1:
                calculation = f"({calculation})"

        first = not operation_parts
        operation_parts.append(_signed_component(str(value), term.sign, first))
        calculation_parts.append(_signed_component(calculation, term.sign, first))
        result += term.sign * value

    return RollDetails(
        expression=dice.strip(),
        operation="".join(operation_parts),
        calculation="".join(calculation_parts),
        result=result,
        groups=tuple(groups),
    )


def roll(dice: str) -> tuple[str, int]:
    details = roll_details(dice)
    return details.operation, details.result
