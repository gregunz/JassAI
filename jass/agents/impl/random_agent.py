import random

from jass.agents.action import ChooseTrumpAction, PlayCardAction
from jass.agents.agent import Agent
from jass.agents.state import ChooseTrumpState, PlayCardState


class RandomAgent(Agent):
    @classmethod
    def play_card(cls, state: PlayCardState) -> PlayCardAction:
        return random.choice(state.actions)

    @classmethod
    def choose_trump(cls, state: ChooseTrumpState) -> ChooseTrumpAction:
        return random.choice(state.actions)
