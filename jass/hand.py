from itertools import groupby
from typing import Sequence, List, Optional, Tuple

from .card import Card, Rank, Suit


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

    def annonces(self, atout: Suit) -> Tuple[Optional['Annonce'], List['Annonce']]:
        annonce_lookup = AnnonceLookup(self.cards)
        annonces = annonce_lookup.lookup()
        n_annonces = len(annonces)
        if n_annonces == 0:
            return None, []
        elif n_annonces == 1:
            return annonces[0], annonces
        elif n_annonces == 2:
            pass


class Annonce:
    def __init__(self, top_card: Card, value: int, num_card: int):
        self.top_card = top_card
        self.value = value
        self.num_card = num_card

    def order_value(self) -> int:
        value_to_x00 = {v: i * 100 for i, v in enumerate([20, 50, 100, 150, 200])}
        num_card_to_x0 = {v: i * 100 for i, v in enumerate([20, 50, 100, 150, 200])}
        return value_to_x00[self.value] + \
               num_card_to_x0[self.num_card] + \
               self.top_card.order_value()

    def compare(self, other: 'Annonce') -> int:
        # check value
        if self.value > other.value:
            return 1
        elif self.value < other.value:
            return -1

        # same value -> check num cards
        if self.num_card > other.num_card:
            return 1
        elif self.num_card < other.num_card:
            return -1

        # same value & num cards -> check top card rank
        if self.top_card.rank > other.top_card.rank:
            return 1
        elif self.top_card.rank < other.top_card.rank:
            return -1

        # same strength -> atout or first to announce wins
        return 0


class AnnonceLookup:
    def __init__(self, cards: Sequence[Card]):
        assert len(cards) == len(set(cards)), 'cant do lookup if cards contain duplicates'
        self._sorted_cards = sorted(cards, key=lambda x: x.order_value())
        self._annonces: List[Annonce] = []

    def lookup(self) -> List[Annonce]:
        ###############################
        # checking for straight flush #
        ###############################

        flushes = list(groupby(
            enumerate(self._sorted_cards),
            key=lambda x: x[1].order_value() - x[0],
        ))
        for _, flush in flushes:
            flush = list(flush)
            self._check_flush(flush, 3, 20)
            self._check_flush(flush, 4, 50)
            self._check_flush(flush, 5, 100)

        ############################
        # checking for 4 of a kind #
        ############################
        all_n_of_a_kind = groupby(self._sorted_cards, key=lambda card: card.rank)
        for _, group in all_n_of_a_kind:
            self._check_4_of_a_kind(list(group))

        return self._annonces

    def _add_annonce(self, annonce: Annonce):
        self._annonces.append(annonce)
        # if len(self._annonces) == 0:
        #     self._annonces = [annonce]
        # else:
        #     cmp = self._annonces[0].compare(annonce)
        #     if cmp == 0:
        #         self._annonces += [annonce]
        #     elif cmp == -1:
        #         self._annonces = [annonce]

    def _check_flush(self, flush: List[Card], flush_size: int, flush_reward: int):
        if flush_size == 5:
            for i in range(6, 10):
                self._check_flush()
        if len(flush) == flush_size:
            top_card = flush[-1]
            annonce = Annonce(top_card=top_card, value=flush_reward, num_card=flush_size)
            self._add_annonce(annonce)

    def _check_4_of_a_kind(self, n_of_a_kind: List[Card]):
        if len(n_of_a_kind) == 4:
            top_card = n_of_a_kind[0]
            value = {
                Rank.jack: 200,
                Rank.nine: 150,
                Rank.ace: 100,
                Rank.king: 100,
                Rank.queen: 100,
                Rank.ten: 100
            }.get(top_card.rank, 0)
            self._add_annonce(Annonce(
                top_card=top_card,
                value=value,
                num_card=4,
            ))
