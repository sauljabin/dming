import heapq
import re
import random


def roll(dice: str) -> tuple[str, int]:
    def replacer(expression: re.Match[str]):
        total, die, keep, total_keep = expression.groups()
        dice = [random.randint(1, int(die)) for _ in range(int(total) if total else 1)]
        filtered_dice = (
            {"kh": heapq.nlargest, "kl": heapq.nsmallest}[keep](
                int(total_keep) if total_keep else 1, dice
            )
            if keep
            else dice
        )
        return str(sum(filtered_dice))

    expression = re.sub(r"(\d+)?d(\d+)(kh|kl)?(\d+)?", replacer, dice)

    if not re.match(r"^[0-9+-]+$", expression):
        raise Exception("not allowed characters")

    return expression, eval(expression)
