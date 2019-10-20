import random

from jass.agents.action import ChooseTrumpAction, PlayCardAction
from jass.agents.agent import Agent
from jass.agents.state import ChooseTrumpState, PlayCardState
from jass.logic.card import Suit


class RandomAgent(Agent):
    def play_card(self, state: PlayCardState) -> PlayCardAction:
        return PlayCardAction(
            card_to_play=random.choice(state.playable_cards)
        )

    def choose_trump(self, state: ChooseTrumpState) -> ChooseTrumpAction:
        return ChooseTrumpAction(
            suit=random.choice(list(Suit)),
        )
