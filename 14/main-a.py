from __future__ import annotations

import sys
from copy import deepcopy
from itertools import starmap
from typing import Hashable, Iterable, Iterator, List, Optional

Game = List[List[str]]


def parse(lines: Iterable[str]) -> Game:
    stripped = map(lambda s: s.strip(), lines)
    return [list(l) for l in stripped if l]


def pretty(game: Game):
    for l in game:
        print("".join(l))


def upper_stone_offset(game: Game, y: int, x: int) -> Optional[int]:
    for upper in range(y + 1, len(game), 1):
        cell = game[upper][x]
        if cell == "O":
            return upper

        if cell == "#":
            return None

    return None


def tilt_north(game: Game) -> Game:
    game = deepcopy(game)
    new_game: Game = []
    for y in range(len(game)):
        new_line: List[str] = []
        for x in range(len(game[y])):
            cell = game[y][x]
            if cell == "#" or cell == "O":
                new_line.append(cell)
            else:
                upper_offset = upper_stone_offset(game, y, x)
                if upper_offset is not None:
                    # we erase the stone in the original game, as it has been moved
                    game[upper_offset][x] = "."

                    # current location becomes the new stone
                    new_line.append("O")
                else:
                    new_line.append(".")
        new_game.append(new_line)

    return new_game


def count_items(items: Iterator[Hashable]) -> dict[Hashable, int]:
    result: dict[Hashable, int] = {}
    for i in items:
        result[i] = result.get(i, 0) + 1

    return result


def all_elems(game: Game) -> Iterator[str]:
    return (game[y][x] for y in range(len(game)) for x in range(len(game[0])))


def all_columns(game: Game) -> Iterator[Iterator[str]]:
    return ((game[y][x] for y in range(len(game))) for x in range(len(game[0])))


def assert_equivalent_games(left: Game, right: Game):
    # same elements
    left_elements = count_items(all_elems(left))
    right_elements = count_items(all_elems(right))
    assert left_elements == right_elements

    # same columns
    for l, r in zip(all_columns(left), all_columns(right)):
        assert count_items(l) == count_items(r)


def solve(game: Game) -> int:
    tilted = tilt_north(game)
    print()
    print("tilted:")
    pretty(tilted)

    assert_equivalent_games(game, tilted)

    count_stones = map(lambda l: l.count("O"), tilted)
    weights = range(len(game), 0, -1)

    return sum(
        starmap(lambda count, weight: count * weight, zip(count_stones, weights))
    )


if __name__ == "__main__":
    # Tests of the poor

    # End tests of the poor

    game = parse(sys.stdin)
    pretty(game)
    result = solve(game)

    print(result)
