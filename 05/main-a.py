import sys
from typing import Iterable, List

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
            mappings.append(currentMap)
            currentMap = []

        else:
            currentMap.append([int(i) for i in line.split()])

    if currentMap:
        mappings.append(currentMap)

    return seeds, mappings


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


if __name__ == "__main__":
    seeds, mappings = parseInput(sys.stdin)

    results = list(computeLocation(s, mappings) for s in seeds)

    print(min(results))
