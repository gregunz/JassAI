from jass.agents.action import ChooseTrumpAction, PlayCardAction
from jass.agents.agent import Agent
from jass.agents.state import PlayCardState, ChooseTrumpState
from jass.logic.card import Card, Rank


class HumanAgent(Agent):
    def play_card(self, state: PlayCardState) -> PlayCardAction:
        print(f'My hand: {sorted(state.hand_cards)}')
        print(f'Cards playable: {sorted(state.playable_cards)}')
        print('Choose a card to play (e.g. 7d = 7♢)....')

        while True:
            try:
                inputs = input()
                if len(inputs) >= 2:
                    card_to_play = Card(inputs[:-1], inputs[-1])
                    if card_to_play in state.playable_cards:
                        return PlayCardAction(
                            card_to_play=card_to_play
                        )
            except ValueError:
                pass
            print('Invalid input or illegal card, starting over...')

    def choose_trump(self, state: ChooseTrumpState) -> ChooseTrumpAction:
        print(state.hand)
        print('Choose trump suit...')

        while True:
            try:
                return ChooseTrumpAction(
                    suit=Card(Rank.six, input()).__suit,  # small hack to parse string properly
                )
            except ValueError:
                print('Invalid trump suit...')
                pass
