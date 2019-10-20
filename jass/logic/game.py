from typing import List, Tuple

from jass.agents.agent import Agent
from jass.logic.card import Card, Suit
from jass.logic.deck import Deck
from jass.logic.exceptions import GameOver
from jass.logic.player import Player
from jass.logic.trick import Trick

GOAL = 1000


class Team:
    def __init__(self, player1: Player, player2: Player):
        self.player1 = player1
        self.player2 = player2
        self.score = 0

    def has_won(self) -> bool:
        return self.score >= GOAL

    @property
    def players(self) -> List[Player]:
        return [self.player1, self.player2]

    def __contains__(self, player: Player):
        return self.player1 == player or self.player2 == player


class Game:
    def __init__(self, names: List[str], agents: List[Agent], log_fn=print):
        assert len(set(names)) == 4, 'It is a 4 players game, need 4 unique names'
        assert len(agents) == 4, 'It is a 4 players game, need 4 agents'

        self.__players = [Player(name, agent) for name, agent in zip(names, agents)]
        team1 = Team(
            player1=self.__players[0],
            player2=self.__players[2],
        )
        team2 = Team(
            player1=self.__players[1],
            player2=self.__players[3],
        )
        self.__teams = (team1, team2)
        self.__log_fn = log_fn

    @property
    def players(self) -> Tuple[Player, Player, Player, Player]:
        p1, p2, p3, p4 = self.__players
        return p1, p2, p3, p4

    @property
    def teams(self) -> Tuple[Team, Team]:
        return self.__teams

    def start(self) -> None:

        self.__log_fn('Let\'s start a Jass Game :)')

        trump_chooser: Player = None

        try:
            while True:

                #########################
                # GIVE CARDS TO PLAYERS #
                #########################

                for player, hand in zip(self.__players, Deck.give_hands()):
                    player.give(hand)

                ################
                # CHOOSE TRUMP #
                ################

                if trump_chooser is None:
                    for p in self.__players:
                        if p.has_7_diamonds():
                            trump_chooser = p
                            self.__log_fn(f'{p} has the {Card(7, Suit.diamonds)}!')
                            break

                next_trick_starter: Player = trump_chooser
                trump = trump_chooser.choose_trump()
                self.__log_fn(f'{trump_chooser} choose trump suit = {trump}')

                #####################
                # PLAY THE 9 TRICKS #
                #####################

                round: List[Trick] = []
                for trick_idx in range(9):
                    trick = Trick(trump)

                    ####################
                    # PLAY EACH A CARD #
                    ####################

                    for player in self.__players_order_from(next_trick_starter):
                        card_played = player.play(
                            trump=trump,
                            players=self.__players_order_from(player),
                            trick_cards=trick.played_cards,
                            round_tricks=[trick.played_cards for trick in round],
                        )
                        self.__log_fn(f'{player} played {card_played}')
                        trick.add_card(card_played, player)

                    ####################
                    # DETERMINE WINNER #
                    ####################

                    winner = trick.winner()
                    points = trick.points(is_last=trick_idx == 8)
                    self.__log_fn(f'{winner} wins the trick ({points} points)')

                    ##############
                    # ADD POINTS #
                    ##############

                    winning_team = [t for t in self.__teams if winner in t][0]
                    winning_team.score += points

                    for p in self.__players:
                        if p in winning_team:
                            p.reward(points)
                        else:
                            p.reward(0)

                    if winning_team.has_won():
                        raise GameOver(f'{winning_team.player1}-{winning_team.player2} team won')

                    next_trick_starter = winner

                ###########
                # RESTART #
                ###########

                trump_chooser = self.__next_player(trump_chooser)
                self.__log_score()

        except GameOver as e:
            self.__log_fn(e)
            self.__log_score()

    def __players_order_from(self, player: Player) -> List[Player]:
        player_idx = self.__players.index(player)
        return self.__players[player_idx:] + self.__players[:player_idx]

    def __next_player(self, player) -> Player:
        return self.__players_order_from(player)[1]

    def __log_score(self):
        for team in self.__teams:
            self.__log_fn(f'{team.player1}-{team.player2} team score: {team.score}')
