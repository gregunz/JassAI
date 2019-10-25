import random
from typing import Tuple, List

from jass.logic.card import Card
from jass.logic.hand import Hand


class Deck:
    __cards = list(Card)

    def shuffle(self) -> 'Deck':
        random.shuffle(self.__cards)
        return self

    def give_hands(self) -> Tuple[Hand, Hand, Hand, Hand]:
        hand1, hand2, hand3, hand4 = [Hand(self.__cards[i * 9:(i + 1) * 9]) for i in range(4)]
        return hand1, hand2, hand3, hand4

    @staticmethod
    def cards() -> List[Card]:
        return Deck().__cards
