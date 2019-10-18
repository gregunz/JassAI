from copy import deepcopy
from random import randint
from unittest import TestCase

from jass.deck import Deck
from jass.hand import Hand


class DeckTest(TestCase):
    def setUp(self) -> None:
        self.deck = Deck()
        self.deck.shuffle()
        self.hand = Hand(self.deck.cards[:9])

    def test_init(self):
        self.assertEqual(len(self.hand.cards), 9)

        with self.assertRaises(ValueError):
            Hand(self.deck.cards[:10])

        with self.assertRaises(ValueError):
            Hand(self.deck.cards[:8])

    def test_play(self):
        hand_before = deepcopy(self.hand)
        card_to_play = self.hand.cards[randint(0, len(self.hand.cards) - 1)]
        self.assertEqual(1 + len(self.hand.play_card(card_to_play).cards), len(hand_before.cards))

    def test_hands(self):
        n_cards = 0
        for hand in self.deck.give_hands():
            self.assertIsInstance(hand, Hand)
            n_cards += len(hand.cards)
        self.assertEqual(n_cards, 36)
