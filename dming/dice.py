import re
import random


def kh(n: int, dice: list[int]) -> list[int]:
    return sorted(dice, reverse=True)[:n]


def kl(n: int, dice: list[int]) -> list[int]:
    return sorted(dice)[:n]


def dh(n: int, dice: list[int]) -> list[int]:
    return sorted(dice, reverse=True)[n:]


def dl(n: int, dice: list[int]) -> list[int]:
    return sorted(dice)[n:]


REDUCERS = {"kh": kh, "kl": kl, "dh": dh, "dl": dl}


def roll(dice: str) -> tuple[str, int]:
    def replacer(expression: re.Match[str]):
        total, die, reducer, total_keep = expression.groups()
        dice = [random.randint(1, int(die)) for _ in range(int(total) if total else 1)]
        filtered_dice = (
            REDUCERS[reducer](int(total_keep) if total_keep else 1, dice)
            if reducer
            else dice
        )
        return str(sum(filtered_dice))

    operation = re.sub(r"(\d+)?d(\d+)(kh|kl|dh|dl)?(\d+)?", replacer, dice)

    if not re.match(r"^[0-9+-]+$", operation):
        raise Exception("not allowed characters")

    return operation, eval(operation)
