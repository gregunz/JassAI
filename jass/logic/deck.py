import random
from typing import Tuple, List

from jass.logic.card import Card, Rank, Suit
from jass.logic.hand import Hand


class Deck:
    def __init__(self):
        self.__cards = [Card(rank, suit) for suit in list(Suit) for rank in list(Rank)]

    def __shuffle(self) -> None:
        random.shuffle(self.__cards)

    def __give_hands(self):
        hand1, hand2, hand3, hand4 = [Hand(self.__cards[i * 9:(i + 1) * 9]) for i in range(4)]
        return hand1, hand2, hand3, hand4

    @staticmethod
    def cards() -> List[Card]:
        deck = Deck()
        return deck.__cards

    @staticmethod
    def give_hands() -> Tuple[Hand, Hand, Hand, Hand]:
        deck = Deck()
        deck.__shuffle()
        return deck.__give_hands()
