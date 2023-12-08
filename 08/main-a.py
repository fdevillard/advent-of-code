from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from typing import Dict, Iterable, List


@dataclass
class Node:
    value: str
    left: str
    right: str

    def __repr__(self) -> str:
        return f"{self.value} = ({self.left}, {self.right})"


@dataclass
class Game:
    instructions: str
    nodes: Dict[str, Node]

    def __repr__(self) -> str:
        s = self.instructions + "\n\n"

        for n in self.nodes.values():
            s += str(n)
            s += "\n"

        return s


def parse(lines: Iterable[str]) -> Game:
    instructions = next(lines).strip()
    nodes: List[Node] = []

    for l in lines:
        l = l.strip()
        if not l:
            continue

        matched = re.search(r"(\w+) = \((\w+), (\w+)\)", l)
        nodes.append(
            Node(value=matched.group(1), left=matched.group(2), right=matched.group(3))
        )

    return Game(instructions=instructions, nodes={n.value: n for n in nodes})


def solve(game: Game) -> int:
    n_hops = 0
    here = game.nodes["AAA"]

    while here.value != "ZZZ":
        match game.instructions[n_hops % len(game.instructions)]:
            case "L":
                here = game.nodes[here.left]
            case "R":
                here = game.nodes[here.right]
            case e:
                raise ValueError(f"unknown instruction: {e}")
        n_hops += 1

    return n_hops


if __name__ == "__main__":
    # Tests of the poor

    # End tests of the poor

    game = parse(sys.stdin)
    # print(game)
    result = solve(game)

    print(result)
