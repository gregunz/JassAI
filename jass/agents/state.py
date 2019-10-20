from typing import List

from jass.logic.card import Suit, Card
from jass.logic.hand import Hand


class PlayCardState:
    def __init__(self, trick_trump: Suit, player_hand: List[Card], playable_cards: List[Card],
                 trick_history: List[Card], round_history: List[List[Card]]):
        assert len(trick_history) < 4, 'at most 3 players played before me'
        assert len(round_history) < 9, 'at most 8 rounds were played before this one'

        self.trump = trick_trump
        self.hand_cards = player_hand
        self.playable_cards = playable_cards
        self.trick_history = trick_history
        self.round_history = round_history


class ChooseTrumpState:
    def __init__(self, hand: Hand, can_chibre: bool):
        self.hand = hand
        self.can_chibre = can_chibre
