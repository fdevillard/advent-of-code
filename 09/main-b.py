from __future__ import annotations

import sys
from typing import Generator, Iterable, List, Optional

Game = List[List[int]]


def parse(lines: Iterable[str]) -> Game:
    return [
        [int(elem.strip()) for elem in l.strip().split()] for l in lines if l.strip()
    ]


def solve(game: Game) -> int:
    results = []
    for i, g in enumerate(game, start=1):
        resolved = solve_single(g)
        results.append(resolved)

    return sum(results)


def solve_single(sensor_samples: List[int]) -> int:
    if all(map(lambda e: e == 0, sensor_samples)):
        return 0

    sums = list(compute_diff(sensor_samples))
    return sensor_samples[0] - solve_single(sums)


def compute_diff(samples: Iterable[int]) -> Generator[int, None, None]:
    last: Optional[int] = None
    for elem in samples:
        if last != None:
            yield elem - last

        last = elem


if __name__ == "__main__":
    # Tests of the poor

    # End tests of the poor

    game = parse(sys.stdin)
    result = solve(game)

    print(result)
