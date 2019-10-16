from enum import Enum, IntEnum
from typing import Union


class Suit(Enum):
    diamonds = '♢'
    spades = '♠'
    hearts = '♡'
    clubs = '♣'

    def __repr__(self):
        return self.value


class Rank(IntEnum):
    six = 6
    seven = 7
    eight = 8
    nine = 9
    ten = 10
    jack = 11
    queen = 12
    king = 13
    ace = 14

    def __repr__(self):
        return {
            self.jack: 'J',
            self.queen: 'Q',
            self.king: 'K',
            self.ace: 'A',
        }.get(self.value, str(self.value))


default_points = {
    Rank.ace: 11,
    Rank.king: 4,
    Rank.queen: 3,
    Rank.jack: 2,
    Rank.ten: 10,
}

atout_points = {
    Rank.ace: 11,
    Rank.king: 4,
    Rank.queen: 3,
    Rank.jack: 20,
    Rank.ten: 10,
    Rank.nine: 14,
}


class Card:
    def __init__(self, rank: Union[int, Rank], suit: Union[int, Suit]):
        self.rank: Rank = Rank(rank)
        self.suit: Suit = Suit(suit)

    def __repr__(self):
        return repr(self.rank) + repr(self.suit)

    def points(self, atout: Suit) -> int:
        points = default_points
        if self.suit is atout:
            points = atout_points
        return points.get(self.rank, 0)

    def value(self, served: Suit, atout: Suit):
        if self.suit is atout:
            return self.rank - Rank.six + Rank.ace - Rank.six + 1
        if self.suit is served:
            return self.rank - Rank.six
        return 0

    def is_greater(self, other: 'Card', served: Suit, atout: Suit):
        return self.value(served, atout) > other.value(served, atout)


class Deck:
    def __init__(self):
        self.cards = [Card(rank, suit) for rank in list(Rank) for suit in list(Suit)]
