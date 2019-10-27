import random
from unittest import TestCase

from jass.agents.state import PlayCardState, ChooseTrumpState
from jass.logic.card import Suit
from jass.logic.deck import Deck


class StatesTest(TestCase):

    def test_random_play_card_state(self):
        deck = Deck()
        for _ in range(100):
            cards = deck.shuffle().cards()

            num_cards_hand = random.randint(2, 9)
            num_card_on_table = random.randint(0, 3)
            round_idx = num_cards_hand + num_card_on_table

            state = PlayCardState(
                trick_trump=random.choice(list(Suit)),
                trump_chooser_idx=random.randint(0, 3),
                player_hand=cards[:num_cards_hand],
                playable_cards=random.choices(cards[:num_cards_hand], k=random.randint(0, num_cards_hand)),
                trick_history=cards[num_cards_hand:num_cards_hand + num_card_on_table],
                round_history=[cards[round_idx + i * 4:round_idx + (i + 1) * 4] for i in range(9 - num_cards_hand)],
            )
            self.assertEqual(state.tensor.nelement(), state.tensor_size)

    def test_random_choose_trump_state(self):
        deck = Deck()
        for _ in range(100):
            cards = deck.shuffle().cards()
            state = ChooseTrumpState(
                hand=cards[:9],
                can_chibre=random.random() < 0.5,
            )
            self.assertEqual(state.tensor.nelement(), state.tensor_size)
