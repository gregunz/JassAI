from typing import List, Dict

from jass.agents.agent import Agent
from jass.agents.state import PlayCardState, ChooseTrumpState
from jass.logic.card import Card, Suit
from jass.logic.exceptions import IllegalMoveError
from jass.logic.hand import Hand


class Player:
    def __init__(self, name: str, agent: Agent):
        self.__name: str = name
        self.__agent: Agent = agent
        self.__hand: Hand = None

    def give(self, hand: Hand) -> None:
        self.__hand = hand

    def play(self, trump: Suit, players: List['Player'], trick_cards: Dict['Player', Card],
             round_tricks: List[Dict['Player', Card]]) -> Card:
        assert self.__hand is not None
        assert self == players[0]

        cards_on_table = [trick_cards[p] for p in players if p in trick_cards]
        cards_playable = self.__hand.playable_cards(cards_played=cards_on_table, trump=trump)

        state = PlayCardState(
            trick_trump=trump,
            player_hand=self.__hand.cards,
            playable_cards=cards_playable,
            trick_history=cards_on_table,
            round_history=[[trick[p] for p in players] for trick in round_tricks]
        )
        card = self.__agent.play_card(state).card_to_play
        self.__hand.play(card, cards_played=cards_on_table, trump=trump)
        return card

    def choose_trump(self) -> Suit:
        if self.__hand is None:
            raise IllegalMoveError('Cannot choose trump before having cards')
        state = ChooseTrumpState(self.__hand, can_chibre=False)  # todo: allow chibre
        return self.__agent.choose_trump(state).suit

    def reward(self, value: int) -> None:
        pass

    def has_7_diamonds(self) -> bool:
        return self.__hand.has(Card(7, Suit.diamonds))

    def __eq__(self, other: 'Player') -> bool:
        return self.__name == other.__name

    def __hash__(self) -> int:
        return hash(self.__name)

    def __repr__(self) -> str:
        return self.__name
