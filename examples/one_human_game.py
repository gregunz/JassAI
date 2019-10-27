from jass.agents.impl.human_agent import HumanAgent
from jass.agents.impl.random_agent import RandomAgent
from jass.logic.game import Game

if __name__ == '__main__':
    agents = [HumanAgent()] + [RandomAgent() for _ in range(3)]
    names = ['Jean', 'Anne', 'Luc', 'Sophie']

    game = Game(
        agents=agents,
        names=names,
        log_fn=print
    )

    game.start()
