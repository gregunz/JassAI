from enum import Enum, IntEnum
from typing import Union


class Suit(Enum):
    diamonds = '♢'
    spades = '♠'
    hearts = '♡'
    clubs = '♣'

    def order_value(self):
        return {
                   Suit.diamonds: 0,
                   Suit.spades: 1,
                   Suit.hearts: 2,
                   Suit.clubs: 3,
               }[self] * 10  # use 10 instead of 9 such that ace and 6 are separated

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

    def order_value(self):
        return self.value - self.six + 1

    def atout_order_value(self):
        return {  # left is power order, right is value order
            Rank.jack: Rank.ace,
            Rank.nine: Rank.king,
            Rank.ace: Rank.queen,
            Rank.king: Rank.jack,
            Rank.queen: Rank.ten,
            Rank.ten: Rank.nine,
        }.get(self, self).order_value()

    def __repr__(self):
        return {
            Rank.jack: 'J',
            Rank.queen: 'Q',
            Rank.king: 'K',
            Rank.ace: 'A',
        }.get(self, str(self.value))


class Card:
    def __init__(self, rank: Union[int, Rank], suit: Union[str, Suit]):
        self.rank: Rank = Rank(rank)
        self.suit: Suit = Suit(suit)

    def order_value(self):
        return self.rank.order_value() + self.suit.order_value()

    def game_value(self, served: Suit, atout: Suit):
        if self.suit is atout:
            return self.rank.atout_order_value() + Rank.ace.order_value()
        if self.suit is served:
            return self.rank.order_value()
        return 0

    def beats(self, other: 'Card', served: Suit, atout: Suit):
        return self.game_value(served=served, atout=atout) >= other.game_value(served=served, atout=atout)

    def points(self, atout: Suit) -> int:
        points = {  # points of non-atout cards
            Rank.ace: 11,
            Rank.king: 4,
            Rank.queen: 3,
            Rank.jack: 2,
            Rank.ten: 10,
        }
        if self.suit is atout:
            points.update({
                Rank.jack: 20,
                Rank.nine: 14,
            })
        return points.get(self.rank, 0)

    def __repr__(self):
        return repr(self.rank) + repr(self.suit)

    def __eq__(self, other: 'Card'):
        return self.order_value() == other.order_value()

    def __hash__(self):
        return hash((self.rank, self.suit))
