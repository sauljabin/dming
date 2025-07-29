import heapq
import re
import random

import click

# TODO:
# 1. ADD RICH
# 2. SIMPLIFY THE CODE
# 3. PRINT A BETTER EXPRESSION
# 4. RELEASE
# 5. DOCUMENTATION
# 6. ADD TESTS


def grouped_roll(match):
    total, die, kind, keep = match.groups()
    dice = [random.randint(1, int(die)) for _ in range(int(total))]
    result = (
        heapq.nlargest(int(keep), dice)
        if kind == "kh"
        else heapq.nsmallest(int(keep), dice)
    )
    return str(sum(result))


def roll(match):
    total, die = map(int, match.groups())
    return str(sum([random.randint(1, die) for _ in range(total)]))


EXPRESSIONS = [(r"(\d+)d(\d+)(kh|kl)(\d+)", grouped_roll), (r"(\d+)d(\d+)", roll)]
"""In order"""


@click.command()
@click.argument("dice")
@click.option(
    "-v", "verbose", help="Show the expression in verbose mode.", is_flag=True
)
def main(dice: str, verbose: bool) -> None:
    """
    Allows you to roll dice from your terminal.

    \b
    Examples:
         roll 1d20    # roll a d20 die
         roll 1d100   # roll a d100 die
         roll 2d20kh1 # roll with advantage
         roll 2d20kl1 # roll with disadvantage
         roll 1d20+4  # roll a d20 die with a +4 modifier
         roll 1d20-4  # roll a d20 die with a -4 modifier
    """
    for expression, roller in EXPRESSIONS:
        dice = re.sub(expression, roller, dice)
    try:
        print(f"{dice + '=' if verbose else ''}{eval(dice)}")
    except Exception as e:
        print(f"Invalid expression: {e}")
        exit(-1)


if __name__ == "__main__":
    main()
