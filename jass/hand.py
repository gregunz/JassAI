from typing import Sequence, List

from .card import Card


class Hand:
    def __init__(self, cards: Sequence[Card]):
        self.__cards = set(cards)
        if len(cards) != 9:
            raise ValueError('A hand must contains exactly 9 unique cards at the start')

    @property
    def cards(self) -> List[Card]:
        return list(self.__cards)

    def play_card(self, card: Card) -> 'Hand':
        assert card in self.__cards, 'Cannot play cards I do not have'
        self.__cards.remove(card)
        return self
