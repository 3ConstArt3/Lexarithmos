# -*- coding: utf-8 -*-
from app.cli import LexarithmosCLI


def main() -> int:

    """
    Starts the Lexarithmos application.

    :return: The process exit code.
    """

    cli = LexarithmosCLI()
    return cli.run()


if __name__ == "__main__":
    raise SystemExit(main())
