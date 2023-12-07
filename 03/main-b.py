import sys
from dataclasses import dataclass
from functools import reduce
from itertools import product, starmap
from typing import Generator, Iterable, List, Optional


class Cell:
    # We explicitly want referential equality.
    def __eq__(self, __value: object) -> bool:
        return self is __value

    def __hash__(self) -> int:
        # well, it's a trivial hash, but it's an hash :]
        return 0


class NumericCell(Cell):
    def __init__(self, value: int):
        self.value = value


class SymbolCell(Cell):
    def __init__(self, symbol: str):
        self.symbol = symbol


Grid = List[List[Cell]]


def parse(lines: Iterable[str]) -> Grid:
    rawGrid = [l.strip() for l in lines if l.strip()]
    parsedGrid: Grid = []

    for line in rawGrid:
        generatedLine: List[Cell] = []
        currentNumericCell: Optional[NumericCell] = None

        for c in line:
            if "0" <= c <= "9":
                # If we're hitting a new number, then we create a new instance of the numeric cell
                if currentNumericCell is None:
                    currentNumericCell = NumericCell(int(c))
                # Otherwise, we mutate it's value to ensure every other equivalent cell has the same value
                else:
                    currentNumericCell.value = int(str(currentNumericCell.value) + c)

                # in both case, we want to keep the equivalence reference
                generatedLine.append(currentNumericCell)
            else:
                currentNumericCell = None
                generatedLine.append(SymbolCell(c))

        parsedGrid.append(generatedLine)

    return parsedGrid


def resolve(grid: Grid) -> Generator[int, None, None]:
    for y, line in enumerate(grid):
        for x, cell in enumerate(line):
            if isinstance(cell, SymbolCell) and cell.symbol == "*":
                yield gear_ratio(grid, y, x)


def gear_ratio(grid: Grid, y: int, x: int) -> int:
    def get_numeric_cell(ny: int, nx: int) -> Optional[NumericCell]:
        ny = y + ny
        nx = x + nx
        if ny < 0 or nx < 0 or ny >= len(grid) or nx >= len(grid[y]):
            return None

        c = grid[ny][nx]

        if isinstance(c, NumericCell):
            return c

        return None

    all_neighbors_offsets = list(
        filter(lambda s: s[0] != 0 or s[1] != 0, product([-1, 0, 1], [-1, 0, 1]))
    )
    all_neighbors_numeric_cells = {
        cell
        for cell in starmap(get_numeric_cell, all_neighbors_offsets)
        if cell is not None
    }

    if len(all_neighbors_numeric_cells) != 2:
        return 0

    return reduce(lambda x, y: x.value * y.value, all_neighbors_numeric_cells)


if __name__ == "__main__":
    grid = parse(sys.stdin)
    result = sum(resolve(grid))

    print(result)
