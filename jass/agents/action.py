import torch

from jass.logic.card import Card, Suit


class PlayCardAction:
    tensor_size = 36

    def __init__(self, card_to_play: Card):
        self.card_to_play = card_to_play

    @staticmethod
    def from_tensor(action: torch.Tensor) -> 'PlayCardAction':
        card_idx = torch.arange(action.nelement())[action == 1].item()
        return PlayCardAction(
            card_to_play=Card[card_idx],
        )


class ChooseTrumpAction:
    tensor_size = 5

    def __init__(self, suit: Suit = None):
        self.suit = suit

    @staticmethod
    def from_tensor(action: torch.Tensor) -> 'ChooseTrumpAction':
        suit_idx = torch.arange(action.nelement())[action == 1].item()
        return ChooseTrumpAction(
            suit=None if suit_idx > 3 else Suit[suit_idx],
        )
