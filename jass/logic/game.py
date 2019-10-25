from typing import List, Tuple, Any

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
    def __init__(self, names: List[str], agents: List[Agent], log_fn=None):
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

    def play(self) -> None:

        self.__log('Let\'s start a Jass Game :)')

        trump_chooser: Player = None
        deck = Deck()  # this reuses the same cards object -> slight memory/performance gain

        try:
            while True:

                #########################
                # GIVE CARDS TO PLAYERS #
                #########################

                for player, hand in zip(self.__players, deck.shuffle().give_hands()):
                    player.give(hand)

                ################
                # CHOOSE TRUMP #
                ################

                if trump_chooser is None:
                    for p in self.__players:
                        if p.has_7_diamonds():
                            trump_chooser = p
                            self.__log(f'{p} has the {Card(7, Suit.diamonds)}!')
                            break

                trump = trump_chooser.choose_trump(can_chibre=True)
                if trump is None:  # chibre!
                    self.__log(f'{trump_chooser} chibre!')
                    partner = self.__partner_of(trump_chooser)
                    trump = partner.choose_trump(can_chibre=False)
                    self.__log(f'{partner} choose trump suit = {trump}')
                else:
                    self.__log(f'{trump_chooser} choose trump suit = {trump}')

                #####################
                # PLAY THE 9 TRICKS #
                #####################

                next_trick_starter: Player = trump_chooser

                prev_tricks: List[Trick] = []

                for trick_idx in range(9):

                    trick, points = self.play_trick(
                        trump=trump,
                        trump_chooser=trump_chooser,
                        starter=next_trick_starter,
                        is_last_trick=trick_idx == 8,
                        prev_tricks=prev_tricks,
                    )
                    prev_tricks.append(trick)
                    winner = trick.winner

                    ##############
                    # ADD POINTS #
                    ##############

                    winning_team = self.__team_of(winner)
                    winning_team.score += points

                    for p in self.__players:
                        if p in winning_team:
                            p.reward(points)
                        else:
                            p.reward(0)

                    next_trick_starter = winner

                    if winning_team.has_won():
                        raise GameOver(f'{winning_team.player1}-{winning_team.player2} team won')

                ###########
                # RESTART #
                ###########

                trump_chooser = self.__next_player(trump_chooser)
                self.__log_score()

        except GameOver as e:
            self.__log(e)
            self.__log_score()

    def play_trick(self, trump: Suit, trump_chooser: Player, starter: Player, is_last_trick: bool,
                   prev_tricks: List[Trick]):

        trick = Trick(trump)

        ####################
        # PLAY EACH A CARD #
        ####################

        for player in self.__players_order_from(starter):
            card_played = player.play(
                trump=trump,
                trump_chooser=trump_chooser,
                players=self.__players_order_from(player),
                trick_cards=trick.played_cards,
                round_tricks=[trick.played_cards for trick in prev_tricks],
            )
            self.__log(f'{player} played {card_played}')
            trick.add_card(card_played, player)

        ####################
        # DETERMINE WINNER #
        ####################

        winner = trick.winner
        points = trick.points
        if is_last_trick:
            points += 5
            if all([self.__team_of(t.winner) == self.__team_of(winner) for t in prev_tricks]):
                points += 100
                self.__log(f'Match!')

        self.__log(f'{winner} wins the trick ({points} points)')

        return trick, points

    def __players_order_from(self, player: Player) -> List[Player]:
        player_idx = self.__players.index(player)
        return self.__players[player_idx:] + self.__players[:player_idx]

    def __next_player(self, player) -> Player:
        return self.__players_order_from(player)[1]

    def __partner_of(self, player: Player) -> Player:
        return self.__players_order_from(player)[2]

    def __team_of(self, player: Player) -> Team:
        return [t for t in self.teams if player in t][0]

    def __log(self, s: Any) -> None:
        if self.__log_fn is not None:
            self.__log_fn(s)

    def __log_score(self):
        for team in self.__teams:
            self.__log(f'{team.player1}-{team.player2} team score: {team.score}')
