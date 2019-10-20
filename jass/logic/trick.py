from collections import OrderedDict
from typing import Dict

from jass.logic.card import Card, Suit
from jass.logic.exceptions import IllegalMoveError
from jass.logic.player import Player


class Trick:
    def __init__(self, trump: Suit):
        self.__played_cards: Dict[Player, Card] = OrderedDict()
        self.__trump = trump
        self.__served = None

    @property
    def trump(self):
        return self.__trump

    @property
    def played_cards(self) -> Dict[Player, Card]:
        return self.__played_cards

    def add_card(self, card: Card, player: Player) -> None:
        if len(self.played_cards) == 0:
            self.__served = card.suit
        if self.__is_complete():
            raise IllegalMoveError('A trick can have at most 4 cards')
        if player in self.played_cards:
            raise IllegalMoveError('A player can only play once per trick')
        self.played_cards[player] = card

    def winner(self) -> Player:
        if not self.__is_complete():
            raise IllegalMoveError('Should not determine the winner of an incomplete trick')
        played_card_list = list(self.played_cards.items())
        best_player, _ = played_card_list[0]
        for player, card in played_card_list[1:]:
            if card.beats(self.played_cards[best_player], served=self.__served, trump=self.__trump):
                best_player = player
        return best_player

    def points(self, is_last=False) -> int:
        if not self.__is_complete():
            raise IllegalMoveError('Should not compute points of an incomplete trick')
        points = sum([c.points(self.__trump) for c in self.played_cards.values()])
        if is_last:
            points += 5
        return points

    def __is_complete(self) -> bool:
        return len(self.played_cards) == 4
