from __future__ import annotations

import sys
from dataclasses import dataclass, replace
from functools import total_ordering
from itertools import count, starmap
from typing import Dict, Iterable, List, Optional


@total_ordering
class Card:
    possible = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]
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
        jokerCount = self.hand.count(Card("J"))
        handWithoutJoker = replace(
            self, hand=list(filter(lambda c: c.value != "J", self.hand))
        )
        grouped = sorted(handWithoutJoker.grouped().values(), reverse=True)

        if len(grouped) <= 1:
            return 7

        if grouped[0] + jokerCount == 4:
            return 6

        # other joker cases would be ranked higher than this.
        if (grouped[0] == 3 and grouped[1] == 2) or (
            jokerCount == 1 and grouped[0] == grouped[1] == 2
        ):
            return 5

        if grouped[0] + jokerCount >= 3:
            return 4

        if grouped[0] == grouped[1] == 2:
            # if jokerCount >= 2 or (jokerCount == 1 and grouped[0] == 2):
            return 3

        if grouped[0] == 2 or jokerCount >= 1:
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

    @dataclass
    class BidTest:
        bid_line: str
        expected_rank: int
        description: Optional[str] = None

    # five of a kind
    bid_tests = [
        BidTest("AAAAA 10", 7, "five of a kind without joker"),
        BidTest("AAAAJ 10", 7, "five of a kind with joker should work"),
        BidTest("AAAJJ 10", 7, "five of a kind with two jokers should work"),
        BidTest("AAJJJ 10", 7, "five of a kind with three jokers should work"),
        BidTest("AJJJJ 10", 7, "five of a kind with four jokers should work"),
        BidTest("JJJJJ 10", 7, "five of a kind with five jokers should work"),
        # four of a kind
        BidTest("2AAAA 10", 6, "four of a king without joker"),
        BidTest("2AAAJ 10", 6, "four of a king with one joker"),
        BidTest("2AAJJ 10", 6, "four of a king with two joker"),
        BidTest("2AJJJ 10", 6, "four of a king with three joker"),
        BidTest("AKJAA 10", 6, f"should be a four of a kind"),
        # full house
        BidTest("AKKAA 10", 5, "full house without joker should work"),
        BidTest("AKKJA 10", 5, "should be a full house with 1 joker"),
        # three of a kind
        BidTest("AAAQT 10", 4, "three of a kind without joker"),
        BidTest("AAJQT 10", 4, "three of a kind with one joker"),
        BidTest("AJJQT 10", 4, "three of a kind with two joker"),
        # double pair
        BidTest("2QQAA 10", 3, "double pair without joker"),
        # single pair
        BidTest("AA234 10", 2, "simple pair"),
        BidTest("AJ234 10", 2, "simple pair with joker"),
        # high card
        BidTest("23456 10", 1, "high card"),
    ]

    for i, t in enumerate(bid_tests, start=1):
        rank = Bid.from_line(t.bid_line).handRank()
        if rank != t.expected_rank:
            print(
                f"test {i} failed: {t.bid_line} should be {t.expected_rank} but is {rank}"
            )

    # End tests of the poor

    game = parse(sys.stdin)
    result = solve(game)

    print(result)
