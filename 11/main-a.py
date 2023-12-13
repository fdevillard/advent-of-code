from __future__ import annotations

import sys
from dataclasses import dataclass
from functools import partial
from multiprocessing import Pool
from typing import Dict, Iterable, Iterator, List, Optional


@dataclass
class Pos:
    y: int
    x: int

    def __repr__(self) -> str:
        return f"({self.y}, {self.x})"

    def __hash__(self) -> int:
        return hash(self.x) + hash(self.y)

    def __add__(self, other) -> Pos:
        if isinstance(other, tuple):
            return Pos(y=self.y + other[0], x=self.x + other[1])

        return Pos(x=self.x + other.x, y=self.y + other.y)


IGame = Iterator[List[str]]
Game = List[List[str]]


def game_to_str(g: IGame) -> str:
    return "\n".join(map(lambda l: "".join(l), g))


def assign_cell_number(game: IGame) -> IGame:
    nextCellNumber = 1
    for l in game:
        new_line: List[str] = []
        for c in l:
            if c == "#":
                new_line.append(str(nextCellNumber))
                nextCellNumber += 1
            else:
                new_line.append(c)

        yield new_line


def expand_lines(g: IGame) -> IGame:
    for line in g:
        yield line

        if set(line) == {"."}:
            yield line


def rotate(igame: IGame) -> IGame:
    game = list(igame)
    length_y = len(game)
    length_x = len(game[0])
    for x in range(length_x):
        yield [game[y][x] for y in range(length_y)]


def parse(lines: Iterable[str]) -> Game:
    cleaned = filter(lambda s: bool(s), map(lambda s: s.strip(), lines))
    trivially_list: IGame = ([e for e in line] for line in cleaned)
    with_numbered = assign_cell_number(trivially_list)
    expanded_lines = expand_lines(with_numbered)
    expanded_cols = rotate(expand_lines(rotate(expanded_lines)))

    return list(expanded_cols)


DistanceMap = Dict[tuple[str, str], int]


def set_min(map: DistanceMap, key: tuple[str, str], dist: int):
    lkey, rkey = key
    if rkey < lkey:
        key = (rkey, lkey)

    current_min = map.get(key)
    if current_min is not None:
        dist = min(dist, current_min)

    map[key] = dist


def is_valid_pos(game: Game, pos: Pos) -> bool:
    return not (
        pos.y < 0 or pos.x < 0 or pos.y >= len(game) or pos.x >= len(game[pos.y])
    )


def at(game: Game, pos: Pos, delta: Optional[Pos] = None) -> Optional[str]:
    if delta is None:
        delta = Pos(y=0, x=0)

    pos = pos + delta

    if not is_valid_pos(game, pos):
        return None

    return game[pos.y][pos.x]


Neighbors = [Pos(1, 0), Pos(-1, 0), Pos(0, 1), Pos(0, -1)]


def compute_min(start_pos: Pos, game: Game) -> DistanceMap:
    start_label = game[start_pos.y][start_pos.x]
    min_distances: DistanceMap = {}

    if start_label in [".", "#"]:
        return min_distances

    assert start_label not in [".", "#"], "should be a numbered start"

    visited = {start_pos}
    to_visit = {start_pos}
    currentDist = 0

    while to_visit:
        steps = set(to_visit)
        visited.update(steps)
        to_visit = set()

        for s in steps:
            visited.add(s)

            c = at(game, s)
            assert c is not None, "well, what?"

            if c != ".":
                set_min(min_distances, (start_label, c), currentDist)

            for delta in Neighbors:
                n = s + delta
                if is_valid_pos(game, n) and n not in visited:
                    to_visit.add(n)

        currentDist += 1

    return min_distances


def solve(game: Game) -> int:
    min_distances: DistanceMap = {}

    all_pos = [Pos(y=y, x=x) for y, line in enumerate(game) for x in range(len(line))]
    with Pool() as p:
        for partial_result in p.map(partial(compute_min, game=game), all_pos):
            for k, v in partial_result.items():
                if k in min_distances:
                    min_distances[k] = min(min_distances[k], v)
                else:
                    min_distances[k] = v
    print(min_distances)

    return sum(min_distances.values())


if __name__ == "__main__":
    # Tests of the poor

    # End tests of the poor

    game = parse(sys.stdin)
    print(game)
    result = solve(game)

    print(result)
