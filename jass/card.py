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


default_points = {  # points of non-atout cards
    Rank.ace: 11,
    Rank.king: 4,
    Rank.queen: 3,
    Rank.jack: 2,
    Rank.ten: 10,
}

atout_points = {  # points of an atout cards
    Rank.ace: 11,
    Rank.king: 4,
    Rank.queen: 3,
    Rank.jack: 20,
    Rank.ten: 10,
    Rank.nine: 14,
}

atout_rank_order = {  # left is power order, right is value order
    Rank.jack: Rank.ace,
    Rank.nine: Rank.king,
    Rank.ace: Rank.queen,
    Rank.king: Rank.jack,
    Rank.queen: Rank.ten,
    Rank.ten: Rank.nine,
}


class Card:
    def __init__(self, rank: Union[int, Rank], suit: Union[str, Suit]):
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
            return (Rank.ace - Rank.six + 1) + atout_rank_order.get(self.rank, self.rank.value) - Rank.six
        if self.suit is served:
            return self.rank - Rank.six
        return 0

    def beats(self, other: 'Card', served: Suit, atout: Suit):
        return self.value(served=served, atout=atout) >= other.value(served=served, atout=atout)

    def __eq__(self, other):
        return isinstance(other, Card) \
               and other.rank == self.rank \
               and other.suit == self.suit

    def __hash__(self):
        return hash((self.rank, self.suit))
