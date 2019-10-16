from random import randint
from unittest import TestCase

from card import Card, Suit, Rank, Deck


class CardTest(TestCase):

    def random_suit(self):
        suits = list(Suit)
        return suits[randint(0, len(suits) - 1)]

    def random_rank(self):
        ranks = list(Rank)
        return ranks[randint(0, len(ranks) - 1)]

    def test_card_repr(self):
        self.assertEqual(repr(Card(6, Suit.spades)), '6♠')
        self.assertEqual(repr(Card(Rank.ace, Suit.clubs)), 'A♣')
        self.assertEqual(repr(Card(10, Suit.diamonds)), '10♢')
        self.assertEqual(repr(Card(11, Suit.hearts)), 'J♡')

    def test_ranks(self):
        for i in range(Rank.six, Rank.ace):
            self.assertGreater(Rank(i + 1), Rank(i))

        for i in range(-5, Rank.six):
            with self.assertRaises(ValueError):
                Rank(i)

        for i in range(Rank.ace + 1, Rank.ace + 10):
            with self.assertRaises(ValueError):
                Rank(i)

    def test_card_init_bad(self):
        with self.assertRaises(ValueError):
            Card(5, Suit.clubs)
        with self.assertRaises(ValueError):
            Card(10, 4)

    def test_deck_points(self):
        deck = Deck()
        self.assertEqual(36, len(deck.cards))
        for atout in list(Suit):
            self.assertEqual(sum([card.points(atout) for card in deck.cards]), 152)
