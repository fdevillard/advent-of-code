import re
import sys
from dataclasses import dataclass
from functools import reduce
from typing import Iterable, List, Optional


@dataclass
class Race:
    time: int
    distance: int


def parseRaces(lines: Iterable[str]) -> List[Race]:
    time: Optional[int] = None
    distance: Optional[int] = None

    for l in lines:
        l = l.strip()
        if not l:
            continue

        split = l.split(":")
        key = split[0].strip().lower()
        elem = int("".join(re.findall(r"\d+", split[1])))

        if key == "time":
            time = elem
        elif key == "distance":
            distance = elem
        else:
            raise ValueError(f"unknown key: {key}")

    if time is None:
        raise ValueError("unknown times")

    if distance is None:
        raise ValueError("unknown distances")

    return [Race(time=time, distance=distance)]


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
    result = reduce(lambda a, b: a * b, allCountBetterRuns)

    print(result)
