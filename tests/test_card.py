from random import randint
from unittest import TestCase

from jass.logic.card import Card, Suit, Rank


class CardTest(TestCase):

    def random_suit(self):
        suits = list(Suit)
        return suits[randint(0, len(suits) - 1)]

    def random_rank(self):
        ranks = list(Rank)
        return ranks[randint(0, len(ranks) - 1)]

    def test_card_str(self):
        self.assertEqual(str(Card(6, Suit.spades)), '6♠')
        self.assertEqual(str(Card(Rank.ace, Suit.clubs)), 'A♣')
        self.assertEqual(str(Card(10, Suit.diamonds)), '10♢')
        self.assertEqual(str(Card(11, Suit.hearts)), 'J♡')
        self.assertEqual(str(Card('q', 'h')), 'Q♡')

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
            Card(10, 'hearts')

    def test_equal(self):
        self.assertEqual(Suit.hearts, Suit('♡'))
        self.assertEqual(Rank.queen, Rank(12))
        self.assertEqual(Card(Rank.eight, Suit.hearts), Card(Rank(8), Suit('♡')))

    def test_hash(self):
        self.assertEqual(hash(Suit.hearts), hash(Suit('♡')))
        self.assertEqual(hash(Rank.queen), hash(Rank(12)))
        self.assertEqual(hash(Card(Rank.eight, Suit.hearts)), hash(Card(Rank(8), Suit('♡'))))

    def test_beats(self):
        def checks(card1, card2, trump, served):
            if card1.suit is trump and card2.suit is not trump:
                self.assertTrue(card1.beats(card2, served=served, trump=trump),
                                msg=f'{card1} should beat {card2} (trump={trump}, served={served})')
            if card1.suit is served and card2.suit is not trump and card2.suit is not served:
                self.assertTrue(card1.beats(card2, served=served, trump=trump),
                                msg=f'{card1} should beat {card2} (trump={trump}, served={served})')
            if card1.suit is not trump and card1.suit is card2.suit and card1.rank >= card2.rank:
                self.assertTrue(card1.beats(card2, served=served, trump=trump),
                                msg=f'{card1} should beat {card2} (trump={trump}, served={served})')
            if card1.suit is trump and card2.suit is trump:
                if card1.rank is Rank.jack:
                    self.assertTrue(card1.beats(card2, served=served, trump=trump),
                                    msg=f'{card1} should beat {card2} (trump={trump}, served={served})')
                elif card1.rank is Rank.nine and card2.rank is not Rank.jack:
                    self.assertTrue(card1.beats(card2, served=served, trump=trump),
                                    msg=f'{card1} should beat {card2} (trump={trump}, served={served})')
                elif card2.rank is not Rank.jack and card2.rank is not Rank.nine and card1.rank >= card2.rank:
                    self.assertTrue(card1.beats(card2, served=served, trump=trump),
                                    msg=f'{card1} should beat {card2} (trump={trump}, served={served})')

        for _ in range(1000):
            card1 = Card(self.random_rank(), self.random_suit())
            card2 = Card(self.random_rank(), self.random_suit())
            checks(card1, card2, trump=self.random_suit(), served=self.random_suit())
            checks(card2, card1, trump=self.random_suit(), served=self.random_suit())

    def test_sorted(self):
        cards = sorted(
            [Card(self.random_rank(), self.random_suit()) for _ in range(1000)],
            reverse=True
        )
        trump = Suit.clubs
        served = Suit.hearts

        def is_not_special(card):
            return not (card.suit is trump and (card.rank is Rank.jack or card.rank is Rank.nine))

        for card1, card2 in zip(cards[:-1], cards[1:]):
            if is_not_special(card1) and is_not_special(card2):
                self.assertTrue(card1.beats(card2, served=served, trump=trump),
                                msg=f'{card1} should beat {card2} (trump={trump}, served={served})')
