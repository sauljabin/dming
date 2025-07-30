import heapq
import re
import random


# TODO:
# 1. ADD RICH
# 3. PRINT A BETTER EXPRESSION
# 4. RELEASE
# 5. DOCUMENTATION
# 6. ADD TESTS


def roll(dice: str) -> tuple[str, int]:
    def kh(total_keep: int, dice: list[int]) -> list[int]:
        return heapq.nlargest(total_keep, dice)

    def kl(total_keep: int, dice: list[int]) -> list[int]:
        return heapq.nsmallest(total_keep, dice)

    def parser(
        total: str, die: str, keep: str, total_keep: str
    ) -> tuple[int, int, str, int]:
        return (
            int(total) if total else 1,
            int(die),
            keep,
            int(total_keep) if total_keep else 1,
        )

    def replacer(expression: re.Match[str]):
        total, die, keep, total_keep = parser(*expression.groups())
        dice = [random.randint(1, die) for _ in range(total)]
        filtered_dice = {"kh": kh, "kl": kl}[keep](total_keep, dice) if keep else dice
        return str(sum(filtered_dice))

    expression = re.sub(r"(\d+)?d(\d+)(kh|kl)?(\d+)?", replacer, dice)

    if not re.match(r"^[0-9+-]+$", expression):
        raise Exception("not allowed characters")

    return expression, eval(expression)
