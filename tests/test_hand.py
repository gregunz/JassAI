from copy import deepcopy
from random import randint
from unittest import TestCase

from jass.logic.deck import Deck
from jass.logic.hand import Hand


class HandTest(TestCase):
    def setUp(self) -> None:
        self.hand = Hand(Deck.cards()[:9])

    def test_init(self):
        self.assertEqual(len(self.hand.cards), 9)

        with self.assertRaises(ValueError):
            Hand(Deck.cards()[:10])

        with self.assertRaises(ValueError):
            Hand(Deck.cards()[:8])

    def test_play(self):
        hand_before = deepcopy(self.hand)
        card_to_play = self.hand.cards[randint(0, len(self.hand.cards) - 1)]
        self.hand.play(card_to_play, [], card_to_play.suit)
        self.assertEqual(1 + len(self.hand.cards), len(hand_before.cards))

    def test_hands(self):
        n_cards = 0
        for hand in Deck.give_hands():
            self.assertIsInstance(hand, Hand)
            n_cards += len(hand.cards)
        self.assertEqual(n_cards, 36)
