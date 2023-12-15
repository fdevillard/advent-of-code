from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import Iterable, List

Game = Iterable[str]


@dataclass
class Lens:
    label: str
    value: int

    def __repr__(self) -> str:
        return f"{self.label} {self.value}"


def parse(lines: Iterable[str]) -> Game:
    for l in lines:
        l = l.strip()
        if not l:
            continue

        for elem in l.split(","):
            yield elem


def compute_hash(s: str) -> int:
    current = 0
    for c in s:
        code = ord(c)
        current += code
        current *= 17
        current %= 256

    return current


def compute_boxes_weight(boxes: List[List[Lens]]) -> int:
    sum = 0
    for box_number, box in enumerate(boxes, start=1):
        for lens_number, lens in enumerate(box, start=1):
            sum += box_number * lens_number * lens.value

    return sum


def solve(game: Game) -> int:
    boxes: List[List[Lens]] = [list() for _ in range(256)]
    for v in game:
        if v[-1] == "-":
            # Remove the label
            label = v[:-1]
            hash = compute_hash(label)
            box_idx = hash % len(boxes)
            box = boxes[box_idx]
            boxes[box_idx] = list(filter(lambda l: l.label != label, box))
        else:
            # Add or update
            label, val = v.split("=")
            lens = Lens(label=label, value=int(val))
            box_idx = compute_hash(label) % len(boxes)

            labels = list(map(lambda l: l.label, boxes[box_idx]))
            try:
                idx = labels.index(lens.label)
                boxes[box_idx][idx] = lens
            except ValueError:
                boxes[box_idx].append(lens)

    return compute_boxes_weight(boxes)


if __name__ == "__main__":
    # Tests of the poor
    assert compute_hash("HASH") == 52
    # End tests of the poor

    game = list(parse(sys.stdin))
    result = solve(game)

    print(result)
