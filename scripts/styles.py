from scripts import CommandProcessor


def main() -> None:
    commands = {
        "black": ("black", ".", "--preview"),
        "ruff": ("ruff", "check", ".", "--fix"),
    }
    CommandProcessor(commands).run()


if __name__ == "__main__":
    main()
