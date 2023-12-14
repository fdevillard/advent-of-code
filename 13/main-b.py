from __future__ import annotations

import sys
from dataclasses import dataclass
from itertools import pairwise
from typing import Iterable, Iterator, List, Optional

Pattern = List[str]

Game = List[Pattern]


@dataclass
class Reflection:
    beginning: int
    size: int


def pretty_print(title: str, pattern: Pattern):
    print(title, ":")
    for l in pattern:
        print("".join(l))


def parse(lines: Iterable[str]) -> Game:
    game: Game = []
    current: Pattern = []

    for l in lines:
        l = l.strip()
        if not l and current:
            game.append(current)
            current = []
        else:
            current.append(l)

    if current:
        game.append(current)

    return game


def safe_get(l: List[str], idx: int) -> Optional[str]:
    if idx < 0 or idx >= len(l):
        return None

    return l[idx]


def has_single_diff(left: str, right: str):
    saw_a_diff = False
    for l, r in zip(left, right):
        if l == r:
            continue

        if saw_a_diff:
            return False

        saw_a_diff = True

    return saw_a_diff


def find_reflection_offsets(pattern: Pattern) -> Iterator[int]:
    for i, (current, next) in enumerate(pairwise(pattern)):
        if current == next or has_single_diff(current, next):
            yield i


def count_reflections(pattern: Pattern) -> Iterator[Reflection]:
    for first_reflection in find_reflection_offsets(pattern):
        saw_single_diff = False
        count = 0
        while True:
            small = safe_get(pattern, first_reflection - count)
            high = safe_get(pattern, first_reflection + count + 1)
            if (small is None or high is None) and not saw_single_diff:
                # A normal symmetry with no change is not supported anymore.
                break

            if (small is None or high is None) and saw_single_diff:
                pretty_print(f"reflection: {first_reflection} (size {count})", pattern)
                yield Reflection(beginning=first_reflection, size=count)

            if small != high and saw_single_diff:
                break

            if small is not None and high is not None and has_single_diff(small, high):
                saw_single_diff = True

            count += 1


def rotate(pattern: Pattern) -> Pattern:
    # pretty_print("before rotation", pattern)
    length_y = len(pattern)
    length_x = len(pattern[0])
    ans = ["".join([pattern[y][x] for y in range(length_y)]) for x in range(length_x)]
    # pretty_print("after rotation", ans)
    assert len(pattern) == len(ans[0])
    assert len(pattern[0]) == len(ans)
    return ans


def solve_single(pattern: Pattern) -> int:
    horizontal_all = sorted(
        count_reflections(pattern), key=lambda e: e.size, reverse=True
    )
    horizontal = horizontal_all[0] if horizontal_all else None
    vertical_all = sorted(
        count_reflections(rotate(pattern)), key=lambda e: e.size, reverse=True
    )
    vertical = vertical_all[0] if vertical_all else None

    if horizontal is None and vertical is None:
        return 0

    print(f"hor: {horizontal}, ver: {vertical}")

    if horizontal and vertical:
        if horizontal.size > vertical.size:
            vertical = None
        else:
            horizontal = None

    if horizontal is None and vertical:  # `vertical` check is for typing.
        return vertical.beginning + 1

    if horizontal:
        return (horizontal.beginning + 1) * 100

    raise ValueError("Unexpected case.")


def solve(game: Game) -> int:
    return sum(map(solve_single, game))


if __name__ == "__main__":
    # Tests of the poor

    # End tests of the poor

    game = parse(sys.stdin)
    print(game)
    result = solve(game)

    print(result)
