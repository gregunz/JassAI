import random
from unittest import TestCase

from jass.logic.card import Suit
from jass.logic.deck import Deck


class DeckTest(TestCase):
    def setUp(self) -> None:
        self.deck = Deck()

    def test_36(self):
        self.assertEqual(len(Deck.cards()), 36)

    def test_deck_points(self):
        cards = Deck.cards()
        for trump in list(Suit):
            random.shuffle(cards)
            self.assertEqual(sum([card.points(trump) for card in cards]), 152)
