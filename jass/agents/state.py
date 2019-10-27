from abc import ABCMeta, abstractmethod
from typing import List

import torch
from torch.nn import functional as F
from werkzeug.utils import cached_property

from jass.agents.action import ChooseTrumpAction, PlayCardAction, Action
from jass.agents.tensor_builder import TensorBuilder
from jass.logic.card import Suit, Card

_tb = TensorBuilder


class State(metaclass=ABCMeta):
    tensor_size: int = NotImplemented
    action_type: Action = NotImplemented

    @property
    @abstractmethod
    def actions(self) -> List[Action]:
        raise NotImplementedError

    @property
    @abstractmethod
    def tensor(self) -> torch.Tensor:
        raise NotImplementedError

    @property
    def action_tensor_mask(self) -> torch.Tensor:
        return torch.ones(self.action_type.tensor_size, dtype=torch.bool)


class PlayCardState(State):
    tensor_size = 4 + 4 + 36 * (1 + 3 + 28)
    action_type = PlayCardAction

    def __init__(self, trick_trump: Suit, trump_chooser_idx: int, player_hand: List[Card], playable_cards: List[Card],
                 trick_history: List[Card], round_history: List[List[Card]]):
        assert len(trick_history) < 4, 'at most 3 players played before me'
        assert len(round_history) < 8, 'at most 7 rounds were played before this onef'

        self.trump = trick_trump
        self.trump_chooser = trump_chooser_idx
        self.hand_cards = player_hand
        self.playable_cards = playable_cards
        self.trick_history = trick_history
        self.round_history = round_history

    @cached_property
    def actions(self) -> List[PlayCardAction]:
        return [PlayCardAction(card_to_play=card) for card in self.playable_cards]

    @cached_property
    def tensor(self) -> torch.Tensor:
        trump = _tb.one_hot(self.trump)  # size = (4)
        trump_chooser = F.one_hot(torch.tensor(self.trump_chooser), num_classes=4)  # size = (4)

        hand = _tb.bow(*self.hand_cards)  # size = (36)

        table_cards = _tb.empty(3 - len(self.trick_history), obj_type=Card)
        if len(self.trick_history) > 0:
            cards_played = _tb.one_hot(*self.trick_history)
            table_cards = torch.cat([cards_played, table_cards])  # size = (3, 36)

        trick_cards = _tb.empty(4, 7 - len(self.round_history), obj_type=Card)
        if len(self.round_history) > 0:
            trick_played = _tb.one_hot(*[c for trick in self.round_history for c in trick]).view(4, -1, len(Card))
            trick_cards = torch.cat([trick_played, trick_cards], dim=1)  # size = (4, 8, 36)

        vectors = [trump, trump_chooser, hand, table_cards, trick_cards]
        return torch.cat([v.view(-1) for v in vectors])

    @cached_property
    def action_tensor_mask(self) -> torch.Tensor:
        return _tb.bow(*self.playable_cards).bool()


class ChooseTrumpState(State):
    tensor_size = 36 + 1
    action_type = ChooseTrumpAction

    def __init__(self, hand: List[Card], can_chibre: bool):
        assert len(hand) == 9, 'always all (9) cards in hand when choosing trump suit'
        self.hand = hand
        self.can_chibre = can_chibre

    @cached_property
    def actions(self) -> List[ChooseTrumpAction]:
        actions = [ChooseTrumpAction(suit=s) for s in list(Suit)]
        if self.can_chibre:
            actions.append(ChooseTrumpAction(suit=None))
        return actions

    @cached_property
    def tensor(self) -> torch.Tensor:
        hand = _tb.bow(*self.hand)  # size = (36)
        can_chibre = torch.tensor([self.can_chibre], dtype=torch.long)  # size = (1)
        return torch.cat((hand, can_chibre))

    @cached_property
    def action_tensor_mask(self) -> torch.Tensor:
        mask = torch.ones(5, dtype=torch.bool)
        mask[-1] = self.can_chibre
        return mask
