from abc import abstractmethod, ABCMeta

import torch

from jass.agents.tensor_builder import TensorBuilder
from jass.logic.card import Suit, Card

_tb = TensorBuilder


class Action(metaclass=ABCMeta):
    tensor_size = NotImplemented

    @property
    @abstractmethod
    def tensor(self) -> torch.Tensor:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def from_tensor(action: torch.Tensor):
        raise NotImplementedError


class PlayCardAction(Action):
    tensor_size = 36

    def __init__(self, card_to_play: Card):
        self.card_to_play = card_to_play

    @property
    def tensor(self) -> torch.Tensor:
        return _tb.one_hot(self.card_to_play).squeeze()

    @staticmethod
    def from_tensor(action: torch.Tensor) -> 'PlayCardAction':
        card_idx = action.max(0)[1].item()
        return PlayCardAction(
            card_to_play=Card[card_idx],
        )


class ChooseTrumpAction(Action):
    tensor_size = 5

    def __init__(self, suit: Suit = None):
        self.suit = suit

    @property
    def tensor(self) -> torch.Tensor:
        vector = torch.zeros(5).long()
        if self.suit is None:
            vector[-1] = 1
        else:
            vector[self.suit.order_value] = 1
        return vector

    @staticmethod
    def from_tensor(action: torch.Tensor) -> 'ChooseTrumpAction':
        suit_idx = action.max(0)[1].item()
        return ChooseTrumpAction(
            suit=None if suit_idx > 3 else Suit[suit_idx],
        )
