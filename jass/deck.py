import random
from typing import Tuple

from jass.card import Card, Rank, Suit
from jass.hand import Hand


class Deck:
    def __init__(self):
        self.cards = [Card(rank, suit) for rank in list(Rank) for suit in list(Suit)]

    def shuffle(self) -> 'Deck':
        random.shuffle(self.cards)
        return self

    # @property
    # def cards(self) -> List[Card]:
    #     return self.__cards

    def give_hands(self) -> Tuple[Hand, Hand, Hand, Hand]:
        self.shuffle()
        hand1, hand2, hand3, hand4 = [Hand(self.cards[i * 9:(i + 1) * 9]) for i in range(4)]
        return hand1, hand2, hand3, hand4
