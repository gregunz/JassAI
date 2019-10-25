from enum import Enum, IntEnum, unique, EnumMeta
from typing import Union

from werkzeug.utils import cached_property


class _IndexEnumMeta(EnumMeta):
    def __getitem__(cls, item: int):
        return list(cls)[item]


@unique
class Suit(Enum, metaclass=_IndexEnumMeta):
    diamonds = '♢'
    spades = '♠'
    hearts = '♡'
    clubs = '♣'

    @cached_property
    def order_value(self) -> int:
        return {suit: i for i, suit in enumerate(Suit)}[self]

    @classmethod
    def __getitem__(cls, item: int) -> 'Suit':
        return list(Suit)[item]

    def __repr__(self):
        return f'Suit({self})'

    def __str__(self):
        return str(self.value)


@unique
class Rank(IntEnum, metaclass=_IndexEnumMeta):
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
    def order_value(self) -> int:
        return {rank: i for i, rank in enumerate(Rank)}[self]

    @cached_property
    def _trump_order_value(self) -> int:
        return {  # left is power order, right is value order
            Rank.jack: Rank.ace,
            Rank.nine: Rank.king,
            Rank.ace: Rank.queen,
            Rank.king: Rank.jack,
            Rank.queen: Rank.ten,
            Rank.ten: Rank.nine,
        }.get(self, self).order_value

    @classmethod
    def __getitem__(cls, item: int) -> 'Rank':
        return list(Rank)[item]

    def __repr__(self):
        return f'Rank({self})'

    def __str__(self):
        return {
            Rank.jack: 'J',
            Rank.queen: 'Q',
            Rank.king: 'K',
            Rank.ace: 'A',
        }.get(self, str(self.value))


class _MetaCard(type):

    def __getitem__(cls, item: int):
        rank_value = item % len(Rank)
        suit_value = item // len(Rank)
        return Card(rank=Rank[rank_value], suit=Suit[suit_value])

    def __iter__(cls):
        for i in range(len(cls)):
            yield Card[i]

    def __len__(cls):
        return len(Suit) * len(Rank)


class Card(object, metaclass=_MetaCard):
    def __init__(self, rank: Union[int, str, Rank], suit: Union[str, Suit]):

        if isinstance(rank, str):
            try:
                rank = int(rank)
            except ValueError:
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
            return self.rank._trump_order_value + Rank.ace.order_value + 2
        if self.suit is served:
            return self.rank.order_value + 1
        return 0

    @cached_property
    def order_value(self) -> int:
        return self.rank.order_value + self.suit.order_value * len(Rank)

    def __repr__(self) -> str:
        return f'Card({self.rank}{self.suit})'

    def __str__(self):
        return str(self.rank) + str(self.suit)

    def __eq__(self, other: 'Card') -> bool:
        return self.order_value == other.order_value

    def __lt__(self, other: 'Card') -> bool:
        return self.order_value < other.order_value

    def __gt__(self, other: 'Card') -> bool:
        return other.__lt__(self)

    def __le__(self, other: 'Card') -> bool:
        return self.order_value <= other.order_value

    def __ge__(self, other: 'Card') -> bool:
        return other.__le__(self)

    def __hash__(self) -> int:
        return hash((self.rank, self.suit))
