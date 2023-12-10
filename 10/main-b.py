from __future__ import annotations

import sys
from dataclasses import dataclass
from math import ceil
from typing import Iterable, List, Optional, Set


@dataclass
class Pos:
    y: int
    x: int

    def __repr__(self) -> str:
        return f"({self.y}, {self.x})"

    def __hash__(self) -> int:
        return hash(self.x) + hash(self.y)


Path = List[Pos]
UnorderedPath = Set[Pos]


@dataclass
class Game:
    grid: List[List[str]]
    s_pos: Pos


def parse(lines: Iterable[str]) -> Game:
    start_pos: Optional[Pos] = None
    grid: List[List[str]] = []
    for y, line in enumerate(lines):
        line = line.strip()
        grid.append([])
        for x, cell in enumerate(line):
            if cell == "S":
                start_pos = Pos(y=y, x=x)

            grid[-1].append(cell)

    return Game(grid=grid, s_pos=start_pos)


def find_path(game: Game) -> Path:
    seen: UnorderedPath = {game.s_pos}
    path: Path = [game.s_pos]
    current: Optional[Pos] = game.s_pos

    while current is not None:
        not_already_visited_neighbors = list(
            filter(lambda p: p not in seen, neighbors(game, current))
        )
        if not not_already_visited_neighbors:
            break

        current = not_already_visited_neighbors[0]
        path.append(current)
        seen.add(current)

    return path


def solve(game: Game) -> int:
    return len(find_path(game)) / 2


def is_valid_pos(game: Game, pos: Pos) -> bool:
    return (
        pos.x >= 0
        and pos.y >= 0
        and pos.y < len(game.grid)
        and pos.x < len(game.grid[pos.y])
    )


def neighbors_naive(
    game: Game, pos: Pos, override_cell_value: Optional[str] = None
) -> List[Pos]:
    if not is_valid_pos(game, pos):
        return []

    match override_cell_value or game.grid[pos.y][pos.x]:
        case "|":
            return [Pos(y=pos.y + 1, x=pos.x), Pos(y=pos.y - 1, x=pos.x)]
        case "-":
            return [Pos(y=pos.y, x=pos.x + 1), Pos(y=pos.y, x=pos.x - 1)]
        case "L":
            return [Pos(y=pos.y - 1, x=pos.x), Pos(y=pos.y, x=pos.x + 1)]
        case "J":
            return [Pos(y=pos.y - 1, x=pos.x), Pos(y=pos.y, x=pos.x - 1)]
        case "7":
            return [Pos(y=pos.y + 1, x=pos.x), Pos(y=pos.y, x=pos.x - 1)]
        case "F":
            return [Pos(y=pos.y + 1, x=pos.x), Pos(y=pos.y, x=pos.x + 1)]
        case ".":
            return []
        case "S":
            possible_cell_values = ["|", "-", "L", "J", "7", "F"]
            for v in possible_cell_values:
                possible_neighbors = neighbors(game, pos, override_cell_value=v)
                if len(possible_neighbors) == 2:
                    return possible_neighbors

            raise ValueError("unknown starting cell value")


def neighbors(
    game: Game, pos: Pos, override_cell_value: Optional[str] = None
) -> List[Pos]:
    return list(
        filter(
            lambda p: is_valid_pos(game, p),
            neighbors_naive(game, pos, override_cell_value=override_cell_value),
        )
    )


if __name__ == "__main__":
    # Tests of the poor

    # End tests of the poor

    game = parse(sys.stdin)
    # print(game)
    result = solve(game)

    print(result)
