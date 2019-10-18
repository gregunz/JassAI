from unittest import TestCase

from jass.card import Suit
from jass.deck import Deck


class DeckTest(TestCase):
    def setUp(self) -> None:
        self.deck = Deck()

    def test_init(self):
        self.assertEqual(len(self.deck.cards), 36)

    def test_deck_points(self):
        deck = Deck()
        self.assertEqual(36, len(deck.shuffle().cards))
        for atout in list(Suit):
            self.assertEqual(sum([card.points(atout) for card in deck.cards]), 152)
