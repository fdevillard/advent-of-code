from __future__ import annotations

import sys
from dataclasses import dataclass
from functools import reduce, total_ordering
from itertools import count, starmap
from typing import Dict, Iterable, List, Optional


@total_ordering
class Card:
    possible = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
    value: str

    def __init__(self, value):
        if value not in self.possible:
            raise ValueError(f"unknown card '{value}'")

        self.value = value

    def _fail_on_invalid_operand(self, other):
        if not isinstance(other, Card):
            raise NotImplementedError

    def __eq__(self, value: object) -> bool:
        self._fail_on_invalid_operand(value)
        return self.value == value.value

    def __gt__(self, value: object) -> bool:
        self._fail_on_invalid_operand(value)
        myPos = self.possible.index(self.value)
        otherPos = self.possible.index(value.value)

        return myPos < otherPos

    def __hash__(self) -> int:
        return hash(self.value)

    def __repr__(self) -> str:
        return self.value


@total_ordering
@dataclass
class Bid:
    hand: List[Card]
    bidValue: int

    @classmethod
    def from_line(cls, s: str) -> Bid:
        spl = s.split()
        rawHand = spl[0]
        bidValue = int(spl[1])

        hand = list(map(Card, rawHand))
        return cls(hand=hand, bidValue=bidValue)

    def grouped(self) -> Dict[Card, int]:
        result: Dict[Card, int] = {}
        for c in self.hand:
            result[c] = result.get(c, 0) + 1

        return result

    def handRank(self) -> int:
        grouped = sorted(self.grouped().values(), reverse=True)
        if grouped == [5]:
            return 7

        if 4 in grouped:
            return 6

        if grouped == [3, 2]:
            return 5

        if 3 in grouped:
            return 4

        if grouped == [2, 2, 1]:
            return 3

        if 2 in grouped:
            return 2

        if set(grouped) == {1}:
            return 1

        return 0

    def _fail_on_invalid_operand(self, other):
        if not isinstance(other, Bid):
            raise ValueError

    def __eq__(self, other: object) -> bool:
        self._fail_on_invalid_operand(other)

        return sorted(self.hand) == sorted(other.hand)

    def __gt__(self, other: object) -> bool:
        self._fail_on_invalid_operand(other)
        myRank = self.handRank()
        otherRank = other.handRank()

        if myRank == otherRank:
            for left, right in zip(self.hand, other.hand):
                if left == right:
                    continue

                return left > right

        return myRank > otherRank


Game = List[Bid]


def parse(lines: Iterable[str]) -> Game:
    result: Game = []

    for l in lines:
        l = l.strip()

        if not l:
            continue

        result.append(Bid.from_line(l))

    return result


def solve(game: Game) -> int:
    return sum(
        starmap(
            lambda a, b: a * b, zip(map(lambda h: h.bidValue, sorted(game)), count(1))
        )
    )


if __name__ == "__main__":
    # Tests of the poor

    # Card
    assert Card("K") > Card("T"), "a king is of higher value of a 10"
    assert Card("K") == Card("K"), "a king is a king"
    try:
        Card("O")
    except ValueError:
        pass
    else:
        assert False, "well, this is an invalid card."

    # Bid
    dummy = Bid(hand=[Card("K"), Card("K"), Card("Q")], bidValue=10)
    expectedGrouped = {Card("K"): 2, Card("Q"): 1}
    assert dummy.grouped() == expectedGrouped, "failed to compute the group properly"

    all_suits = parse(
        """
        23456 10
        AA234 10
        2QQAA 10
        98TTT 10
        98JJJ 10
        98222 10
        33322 10
        A2AAA 10
        AAAAA 10
        """.splitlines()
    )
    sorted_suits = sorted(all_suits, reverse=True)
    sorted_as_string = list(
        map(lambda suit: "".join(map(str, suit.hand)), sorted_suits)
    )
    assert sorted_as_string == [
        "AAAAA",
        "A2AAA",
        "33322",
        "98JJJ",
        "98TTT",
        "98222",
        "2QQAA",
        "AA234",
        "23456",
    ]

    # End tests of the poor

    game = parse(sys.stdin)
    result = solve(game)

    print(result)
