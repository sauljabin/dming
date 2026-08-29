import re
from dataclasses import dataclass


class InvalidProbabilityError(ValueError):
    pass


@dataclass(frozen=True)
class DieSpec:
    expression: str
    sides: int
    modifier: int


@dataclass(frozen=True)
class ProbabilityRow:
    target: int
    minimum_roll: int | None
    standard: float
    advantage: float
    disadvantage: float


def parse_die(expression: str) -> DieSpec:
    match = re.fullmatch(r"d(\d+)([+-]\d+)?", expression)
    if not match:
        raise InvalidProbabilityError("use dN, dN+M, or dN-M")

    sides = int(match.group(1))
    if sides < 1:
        raise InvalidProbabilityError("die must have at least one side")

    return DieSpec(
        expression=expression,
        sides=sides,
        modifier=int(match.group(2) or 0),
    )


def success_probability(spec: DieSpec, target: int) -> float:
    probability = (spec.sides + 1 + spec.modifier - target) / spec.sides
    return min(max(probability, 0.0), 1.0)


def probability_rows(
    spec: DieSpec,
    min_target: int = 1,
    max_target: int | None = None,
) -> tuple[ProbabilityRow, ...]:
    maximum = max_target if max_target is not None else max(spec.sides, spec.sides + spec.modifier)
    if min_target < 1 or maximum < 1:
        raise InvalidProbabilityError("targets must be positive")
    if min_target > maximum:
        raise InvalidProbabilityError("minimum target cannot exceed maximum target")

    rows = []
    for target in range(min_target, maximum + 1):
        standard = success_probability(spec, target)
        required_roll = target - spec.modifier
        rows.append(
            ProbabilityRow(
                target=target,
                minimum_roll=max(required_roll, 1) if required_roll <= spec.sides else None,
                standard=standard,
                advantage=1 - (1 - standard) ** 2,
                disadvantage=standard**2,
            )
        )
    return tuple(rows)
