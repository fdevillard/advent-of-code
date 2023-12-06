import sys
from dataclasses import dataclass
from typing import Iterable, List, Optional, Generator
from functools import reduce
from itertools import product, starmap

Grid = List[str]

def parse(lines: Iterable[str]) -> Grid:
    return [l.strip() for l in lines if l.strip()]

def resolve(grid: Grid) -> Generator[int, None, None]:
    for y, line in enumerate(grid):
        currentNumber = ""
        isAdjacent = False
        for x, c in enumerate(line):
            if '0' <= c <= '9':
                currentNumber += c
                isAdjacent |= is_adjacent(grid, y, x)
            elif isAdjacent:
                yield int(currentNumber)
                currentNumber = ""
                isAdjacent = False
            else:
                currentNumber = ""
                isAdjacent = False

        if isAdjacent:
            yield int(currentNumber)
            currentNumber = ""
            isAdjacent = False

def is_adjacent(grid: Grid, y: int, x: int) -> bool:
    def is_special(ny: int, nx: int) -> bool:
        ny = y + ny
        nx = x + nx
        if ny < 0 or nx < 0 or ny >= len(grid) or nx >= len(grid[y]):
            return False

        c = grid[ny][nx]
        if c == ".":
            return False

        if "0" <= c <= "9":
            return False

        return True

    all_neighbors = list(filter(lambda s: s[0] != 0 or s[1] != 0, product([-1, 0, 1], [-1, 0, 1])))
    return any(starmap(is_special, all_neighbors))


if __name__ == "__main__":
    grid = parse(sys.stdin)
    result = sum(resolve(grid))

    print(result)

