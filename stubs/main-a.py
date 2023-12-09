from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import Iterable


@dataclass
class Game:
    pass


def parse(lines: Iterable[str]) -> Game:
    pass


def solve(game: Game) -> int:
    pass


if __name__ == "__main__":
    # Tests of the poor

    # End tests of the poor

    game = parse(sys.stdin)
    print(game)
    result = solve(game)

    print(result)
