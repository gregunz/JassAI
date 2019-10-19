from copy import deepcopy
from random import randint
from unittest import TestCase

from jass.card import Card, Suit, Rank
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

    def test_annonce(self):
        hand20 = Hand([
            Card(6, Suit.hearts),
            Card(8, Suit.hearts),
            Card(9, Suit.hearts),
            Card(10, Suit.hearts),
            Card(Rank.ace, Suit.hearts),
            Card(Rank.ace, Suit.clubs),
            Card(Rank.ace, Suit.diamonds),
            Card(Rank.king, Suit.diamonds),
            Card(Rank.queen, Suit.hearts),
        ])
        annonces = hand20.annonces()
        annonce =
        self.assertEqual(annonce, 20)
        self.assertEqual(rank, 10)
