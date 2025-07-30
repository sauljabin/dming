import click

from dming.dice import roll

from rich.console import Console


@click.command()
@click.argument("dice")
@click.option("-v", "verbose", help="Show the expression.", is_flag=True)
def _roll(dice: str, verbose: bool) -> None:
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
    try:
        expression, result = roll(dice)
        if verbose:
            console = Console()
            console.print(f"{expression}={result}")
        else:
            print(f"{result}")
    except Exception as e:
        print(f"Invalid expression: {e}")
        exit(-1)
