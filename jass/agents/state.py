from typing import List, Union, Type

import torch
from torch.nn import functional as F

from jass.logic.card import Suit, Card


class PlayCardState:
    tensor_size = 4 + 4 + 36 * (1 + 3 + 32)

    def __init__(self, trick_trump: Suit, trump_chooser_idx: int, player_hand: List[Card], playable_cards: List[Card],
                 trick_history: List[Card], round_history: List[List[Card]]):
        assert len(trick_history) < 4, 'at most 3 players played before me'
        assert len(round_history) < 9, 'at most 8 rounds were played before this one'

        self.trump = trick_trump
        self.trump_chooser = trump_chooser_idx
        self.hand_cards = player_hand
        self.playable_cards = playable_cards
        self.trick_history = trick_history
        self.round_history = round_history

    def to_tensor(self) -> torch.Tensor:
        trump = _tb.new(self.trump)  # size = (4)
        trump_chooser = F.one_hot(torch.tensor(self.trump_chooser), num_classes=4)  # size = (4)

        hand = _tb.new(*self.hand_cards)  # size = (36)

        table_cards = _tb.empty(3 - len(self.trick_history), obj_type=Card)
        if len(self.trick_history) > 0:
            cards_played = _tb.one_hot(*self.trick_history)
            table_cards = torch.cat([cards_played, table_cards])  # size = (3, 36)

        trick_cards = _tb.empty(4, 8 - len(self.round_history), obj_type=Card)
        if len(self.round_history) > 0:
            trick_played = _tb.one_hot(*[card for trick in self.round_history for card in trick]).view(4, -1,
                                                                                                       len(Card))
            trick_cards = torch.cat([trick_played, trick_cards], dim=1)  # size = (4, 8, 36)

        vectors = [trump, trump_chooser, hand, table_cards, trick_cards]
        return torch.cat([v.view(-1) for v in vectors])


class ChooseTrumpState:
    tensor_size = 36 + 1

    def __init__(self, hand: List[Card], can_chibre: bool):
        assert len(hand) == 9, 'always all (9) cards in hand when choosing trump suit'
        self.hand = hand
        self.can_chibre = can_chibre

    def to_tensor(self) -> torch.Tensor:
        hand = _tb.new(*self.hand)  # size = (36)
        can_chibre = torch.tensor([self.can_chibre], dtype=torch.long)  # size = (1)
        return torch.cat((hand, can_chibre))


class _TensorBuilder:
    @staticmethod
    def new(*objects: Union[Suit, Card]) -> torch.Tensor:
        obj_type = type(objects[0])
        vector = torch.zeros(len(obj_type), dtype=torch.long)
        for o in objects:
            assert obj_type == type(o), \
                f'cannot create a vector with objects of different type ({obj_type} != {type(o)})'
            vector[o.order_value] = 1

        return vector

    @staticmethod
    def one_hot(*objects: Union[Suit, Card]) -> torch.Tensor:
        obj_type = type(objects[0])
        obj_values = []
        for o in objects:
            assert obj_type == type(o), \
                f'cannot create a vector with objects of different type ({obj_type} != {type(o)})'
            obj_values.append(o.order_value)
        return F.one_hot(torch.tensor(obj_values), num_classes=len(obj_type))

    @staticmethod
    def empty(*size: int, obj_type: Type[Union[Suit, Card]]) -> torch.Tensor:
        return torch.zeros(*size, len(obj_type), dtype=torch.long)


_tb = _TensorBuilder
