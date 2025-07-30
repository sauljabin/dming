import click

from dming.dice import roll
from dming import __version__

from rich.console import Console


@click.command()
@click.argument("dice")
@click.option(
    "-v", "verbose", help="Verbose output. Show the arithmetic operation.", is_flag=True
)
@click.version_option(__version__)
def _roll(dice: str, verbose: bool) -> None:
    """
    Allows you to roll dice from your terminal.

    \b
    Examples:
         roll 1d20    # roll a d20 die
         roll 1d100   # roll a d100 die
         roll 2d20kh1 # roll with advantage
         roll 2d20kl1 # roll with disadvantage
         roll 2d20dl1 # roll with advantage
         roll 2d20dh1 # roll with disadvantage
         roll 1d20+4  # roll a d20 die with a +4 modifier
         roll 1d20-4  # roll a d20 die with a -4 modifier
    """
    try:
        operation, result = roll(dice)
        if verbose:
            console = Console()
            console.print(f"{operation}={result}")
        else:
            print(f"{result}")
    except Exception as e:
        print(f"Invalid operation: {e}")
        exit(-1)
