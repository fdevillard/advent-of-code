from __future__ import annotations

import sys
from typing import Iterable

Game = Iterable[str]


def parse(lines: Iterable[str]) -> Game:
    for l in lines:
        l = l.strip()
        if not l:
            continue

        for elem in l.split(","):
            yield elem


def compute_hash(s: str) -> int:
    current = 0
    for c in s:
        code = ord(c)
        current += code
        current *= 17
        current %= 256

    return current


def solve(game: Game) -> int:
    return sum(map(compute_hash, game))


if __name__ == "__main__":
    # Tests of the poor
    assert compute_hash("HASH") == 52
    # End tests of the poor

    game = list(parse(sys.stdin))
    result = solve(game)

    print(result)
