from unittest import TestCase

from jass.agents.impl.random_agent import RandomAgent
from jass.logic.game import Game


class RandomGameTest(TestCase):

    def test_scores(self):
        random_agents = [RandomAgent() for _ in range(4)]

        for _ in range(10):
            game = Game(random_agents)
            game.start()

            team1, team2 = game.teams

            if team1.score > team2.score:
                high_score = team1.score
                low_score = team2.score
            else:
                high_score = team2.score
                low_score = team1.score

            self.assertGreater(high_score, low_score)
