import sys
from functools import partial
from multiprocessing import Pool
from typing import Iterable, List, Sequence

Seeds = List[int]
Mapping = List[List[int]]


def parseInput(lines: Iterable[str]) -> (Seeds, List[Mapping]):
    # process the seeds line
    seedsRaw = next(lines)
    seeds = [int(element.strip()) for element in seedsRaw.split(": ")[1].split(" ")]

    # process the maps
    mappings: List[Mapping] = []
    currentMap: Mapping = []
    for line in lines:
        line = line.strip()

        if not line:
            continue

        if "map" in line:
            if currentMap:
                mappings.append(currentMap)

            currentMap = []

        else:
            currentMap.append([int(i) for i in line.split()])

    if currentMap:
        mappings.append(currentMap)

    return seeds, mappings


def expandSeeds(seeds: List[int]) -> Iterable[Sequence[int]]:
    if len(seeds) % 2 != 0:
        raise ValueError("must be pairs")

    for idx in range(0, len(seeds), 2):
        yield seeds[idx], seeds[idx + 1]


def applyMapping(seed: int, mapping: Mapping) -> int:
    for rule in mapping:
        dest, source, l = rule[0], rule[1], rule[2]
        if source <= seed < source + l:
            return dest + (seed - source)

    return seed


def computeLocation(seed: int, mappings: List[Mapping]) -> int:
    for mapping in mappings:
        seed = applyMapping(seed, mapping)

    return seed


def computeLocationOnSlice(seeds: List[int], mappings: List[Mapping]) -> int:
    if len(seeds) != 2:
        raise ValueError("not a range")

    return min(
        (computeLocation(s, mappings) for s in range(seeds[0], seeds[0] + seeds[1], 1))
    )


if __name__ == "__main__":
    seeds, mappings = parseInput(sys.stdin)

    with Pool() as p:
        expanded = expandSeeds(seeds)
        result = min(
            p.map(partial(computeLocationOnSlice, mappings=mappings), expanded)
        )

    print(result)
