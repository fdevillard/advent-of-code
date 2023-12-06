import sys
from dataclasses import dataclass
from typing import Iterable, List, Optional
from functools import reduce

@dataclass
class Race:
    time: int
    distance: int

def parseRaces(lines: Iterable[str]) -> List[Race]:
    times: Optional[List[int]] = None
    distances: Optional[List[int]] = None

    for l in lines:
        l = l.strip()
        if not l:
            continue

        split = l.split(":")
        key = split[0].strip().lower()
        elems = [
            int(elem.strip())
            for elem
            in split[1].split()
            if elem.strip()
        ]

        if key == "time":
            times = elems
        elif key == "distance":
            distances = elems
        else:
            raise ValueError(f"unknown key: {key}")

    if times is None:
        raise ValueError("unknown times")

    if distances is None:
        raise ValueError("unknown distances")

    return list(map(lambda tpl: Race(time=tpl[0], distance=tpl[1]), zip(times, distances)))

def countBetterRuns(race: Race) -> int:
    betterRuns = 0

    for waitTime in range(1, race.time):
        runtime = race.time - waitTime
        speed = waitTime
        length = speed * runtime
        if length > race.distance:
            betterRuns += 1

    return betterRuns

if __name__ == "__main__":

    races = parseRaces(sys.stdin)
    allCountBetterRuns = map(countBetterRuns, races)
    result = reduce(lambda a, b: a*b, allCountBetterRuns)

    print(result)

