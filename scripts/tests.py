from scripts import CommandProcessor


def main() -> None:
    commands = {
        "executing tests": ("python", "-m", "unittest", "discover", "-v", "tests"),
    }
    CommandProcessor(commands).run()


if __name__ == "__main__":
    main()
