import random
from unittest import TestCase

import torch
from torch.nn import functional as F

from jass.agents.action import PlayCardAction, ChooseTrumpAction
from jass.logic.card import Suit, Card


class ActionsTest(TestCase):

    def test_random_play_card_action(self):
        for _ in range(100):
            card_idx = random.randint(0, PlayCardAction.tensor_size - 1)
            action = PlayCardAction.from_tensor(
                action=F.one_hot(torch.tensor(card_idx), num_classes=PlayCardAction.tensor_size)
            )
            self.assertEqual(action.card_to_play, Card[card_idx])

    def test_random_choose_trump_action(self):
        for _ in range(100):
            trump_idx = random.randint(0, ChooseTrumpAction.tensor_size - 1)
            action = ChooseTrumpAction.from_tensor(
                action=F.one_hot(torch.tensor(trump_idx), num_classes=ChooseTrumpAction.tensor_size)
            )
            self.assertEqual(action.suit, Suit[trump_idx] if trump_idx < 4 else None)
