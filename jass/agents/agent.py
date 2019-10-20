from abc import abstractmethod, ABCMeta

from jass.agents.action import PlayCardAction, ChooseTrumpAction
from jass.agents.state import PlayCardState, ChooseTrumpState


class Agent(metaclass=ABCMeta):
    @abstractmethod
    def play_card(self, state: PlayCardState) -> PlayCardAction:
        raise NotImplementedError

    @abstractmethod
    def choose_trump(self, state: ChooseTrumpState) -> ChooseTrumpAction:
        raise NotImplementedError
