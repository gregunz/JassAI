from jass.agents.action import ChooseTrumpAction, PlayCardAction
from jass.agents.agent import Agent
from jass.agents.impl.random_agent import RandomAgent
from jass.agents.state import ChooseTrumpState, PlayCardState
from jass.logic.card import Suit, Rank


class GreedyAgent(Agent):
    @classmethod
    def play_card(cls, state: PlayCardState) -> PlayCardAction:
        # todo: be greedier than random
        return RandomAgent.play_card(state)

    @classmethod
    def choose_trump(cls, state: ChooseTrumpState) -> ChooseTrumpAction:
        suit_to_points = {s: 0 for s in list(Suit)}
        for card in state.hand:
            suit_to_points[card.suit] += {
                Rank.jack: 2.5,
                Rank.nine: 2,
                Rank.ace: 1.5,
                Rank.king: 1.2,
                Rank.queen: 1.1,
            }.get(card.rank, 1)
        trump = max(suit_to_points.items(), key=lambda x: x[1])[0]
        return ChooseTrumpAction(suit=trump)
