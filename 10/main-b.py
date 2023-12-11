from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from itertools import pairwise
from typing import Iterable, List, Optional, Set

PRINT = os.environ.get("PRINT", "false").lower() in ["true", "y"]


@dataclass
class Pos:
    y: int
    x: int

    def __repr__(self) -> str:
        return f"({self.y}, {self.x})"

    def __hash__(self) -> int:
        return hash(self.x) + hash(self.y)

    def __add__(self, other):
        return Pos(self.y + other.y, self.x + other.x)


Path = List[Pos]
UnorderedPath = Set[Pos]


@dataclass
class Game:
    grid: List[List[str]]
    s_pos: Pos

    def at(self, pos: Pos) -> Optional[str]:
        if is_valid_pos(self, pos):
            return self.grid[pos.y][pos.x]

        return None


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
    # we first compute the path that circles in the game
    path = find_path(game)
    if PRINT:
        print(path)

    # we are now only interested in the path in the grid, where we mark the path (P) cells
    # and unknown (?) cells.
    zone_grid = [
        [("B" if Pos(y=y, x=x) in path else "?") for x in range(len(line))]
        for y, line in enumerate(game.grid)
    ]
    zone_game = Game(grid=zone_grid, s_pos=Pos(0, 0))
    if PRINT:
        for l in zone_game.grid:
            print("".join(l))

    def assign_if_free(pos: Pos, label: str) -> bool:
        if not is_valid_pos(zone_game, pos):
            return False

        if zone_game.grid[pos.y][pos.x] != "?":
            return False

        zone_game.grid[pos.y][pos.x] = label
        return True

    # we _color_ each direct neighbors of our path with A or B (could be internal/external, but we
    # don't know here if it's internal/external)
    for current, next in pairwise(path):
        dx = next.x - current.x
        dy = next.y - current.y

        assert dx == 0 or dy == 0, "well we only move to one cell. Or, am I wrong?"

        if dx == 1:
            assign_if_free(Pos(y=current.y - 1, x=current.x), "I")
            assign_if_free(Pos(y=current.y + 1, x=current.x), "O")
        elif dx == -1:
            assign_if_free(Pos(y=current.y - 1, x=current.x), "O")
            assign_if_free(Pos(y=current.y + 1, x=current.x), "I")
        elif dy == 1:
            assign_if_free(Pos(y=current.y, x=current.x + 1), "I")
            assign_if_free(Pos(y=current.y, x=current.x - 1), "O")
        elif dy == -1:
            assign_if_free(Pos(y=current.y, x=current.x + 1), "O")
            assign_if_free(Pos(y=current.y, x=current.x - 1), "I")
        else:
            ValueError("don't know in which direction we are going.")

    # then, we propagate the solution iteratively
    for epoch in range(100):
        did_change = False
        if PRINT:
            print(epoch, ":")
            for l in zone_game.grid:
                print("".join(l))
        for y, line in enumerate(zone_game.grid):
            for x, cell in enumerate(line):
                if cell != "?":
                    continue

                neighbors_value = {
                    zone_game.grid[y + dy][x + dx]
                    for dy, dx in [(1, 0), (-1, 0), (0, 1), (0, -1)]
                    if is_valid_pos(zone_game, Pos(y=y + dy, x=x + dx))
                }
                assert not (
                    "I" in neighbors_value and "O" in neighbors_value
                ), "well, the logic is flawed as we are both internal and external"

                for possible in ["I", "O"]:
                    if possible in neighbors_value:
                        did_change |= assign_if_free(Pos(y=y, x=x), possible)

        if not did_change:
            print(f"early stop after {epoch} steps")
            break

    for l in zone_game.grid:
        print("".join(l))

    counts = {k: 0 for k in ["I", "O", "?"]}

    for l in zone_game.grid:
        for c in l:
            if c in counts:
                counts[c] = counts[c] + 1

    print(counts)

    return counts["I"]


def is_valid_pos(game: Game, pos: Pos) -> bool:
    return (
        pos.x >= 0
        and pos.y >= 0
        and pos.y < len(game.grid)
        and pos.x < len(game.grid[pos.y])
    )


def neighbors_naive(game: Game, pos: Pos) -> List[Pos]:
    if not is_valid_pos(game, pos):
        return []

    match game.grid[pos.y][pos.x]:
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
            checks = {
                # south
                Pos(y=1, x=0): ["|", "L", "J"],
                # north
                Pos(y=-1, x=0): ["|", "7", "F"],
                # east
                Pos(y=0, x=1): ["-", "J", "7"],
                # west
                Pos(y=0, x=-1): ["-", "L", "F"],
            }

            valid_neighbors = []
            for delta, expected in checks.items():
                location = pos + delta
                if game.at(location) in expected:
                    valid_neighbors.append(location)

            assert (
                len(valid_neighbors) == 2
            ), "we should always have two working neighbors around the start"
            return valid_neighbors


def neighbors(game: Game, pos: Pos) -> List[Pos]:
    return list(
        filter(
            lambda p: is_valid_pos(game, p),
            neighbors_naive(game, pos),
        )
    )


if __name__ == "__main__":
    # Tests of the poor

    # End tests of the poor

    game = parse(sys.stdin)
    # print(game)
    result = solve(game)

    print(result)
