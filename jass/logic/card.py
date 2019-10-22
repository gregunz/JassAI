from enum import Enum, IntEnum
from typing import Union

from werkzeug.utils import cached_property


class Suit(Enum):
    diamonds = '♢'
    spades = '♠'
    hearts = '♡'
    clubs = '♣'

    @cached_property
    def _order_value(self) -> int:
        return {
            Suit.diamonds: 0,
            Suit.spades: 1,
            Suit.hearts: 2,
            Suit.clubs: 3,
        }[self]

    def __repr__(self):
        return str(self.value)

    def __str__(self):
        return self.__repr__()


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

    @cached_property
    def _order_value(self) -> int:
        return self.value - self.six + 1

    @cached_property
    def _trump_order_value(self) -> int:
        return {  # left is power order, right is value order
            Rank.jack: Rank.ace,
            Rank.nine: Rank.king,
            Rank.ace: Rank.queen,
            Rank.king: Rank.jack,
            Rank.queen: Rank.ten,
            Rank.ten: Rank.nine,
        }.get(self, self)._order_value

    def __repr__(self) -> str:
        return {
            Rank.jack: 'J',
            Rank.queen: 'Q',
            Rank.king: 'K',
            Rank.ace: 'A',
        }.get(self, str(self.value))

    def __str__(self):
        return self.__repr__()


class Card:
    def __init__(self, rank: Union[int, str, Rank], suit: Union[str, Suit]):
        try:
            rank = int(rank)
        except ValueError:
            pass

        if isinstance(rank, str):
            rank = {
                'J': Rank.jack,
                'Q': Rank.queen,
                'K': Rank.king,
                'A': Rank.ace,
            }.get(rank.upper(), rank)

        if isinstance(suit, str):
            suit = {
                'D': '♢',
                'S': '♠',
                'H': '♡',
                'C': '♣',
            }.get(suit.upper(), suit)

        self.__rank: Rank = Rank(rank)
        self.__suit: Suit = Suit(suit)

    @property
    def rank(self) -> Rank:
        return self.__rank

    @property
    def suit(self) -> Suit:
        return self.__suit

    def beats(self, other: 'Card', served: Suit, trump: Suit) -> bool:
        return self.__strength_value(served=served, trump=trump) >= other.__strength_value(served=served, trump=trump)

    def points(self, trump: Suit) -> int:
        points = {  # points of non-trump cards
            Rank.ace: 11,
            Rank.king: 4,
            Rank.queen: 3,
            Rank.jack: 2,
            Rank.ten: 10,
        }
        if self.suit is trump:  # editing trump points
            points.update({
                Rank.jack: 20,
                Rank.nine: 14,
            })
        return points.get(self.rank, 0)

    def __strength_value(self, served: Suit, trump: Suit) -> int:
        if self.suit is trump:
            return self.rank._trump_order_value + Rank.ace._order_value
        if self.suit is served:
            return self.rank._order_value
        return 0

    @cached_property
    def __order_value(self) -> int:
        # use 10 instead of 9 such that ace and 6 are separated by 2 when searching for sequences
        return self.rank._order_value + self.suit._order_value * 10

    def __repr__(self) -> str:
        return repr(self.rank) + repr(self.suit)

    def __eq__(self, other: 'Card') -> bool:
        return self.__order_value == other.__order_value

    def __lt__(self, other: 'Card') -> bool:
        return self.__order_value < other.__order_value

    def __gt__(self, other: 'Card') -> bool:
        return other.__lt__(self)

    def __le__(self, other: 'Card') -> bool:
        return self.__order_value <= other.__order_value

    def __ge__(self, other: 'Card') -> bool:
        return other.__le__(self)

    def __hash__(self) -> int:
        return hash((self.rank, self.suit))

    def __str__(self):
        return self.__repr__()
