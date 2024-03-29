from jass.agents.impl.random_agent import RandomAgent
from jass.logic.game import Game

if __name__ == '__main__':
    random_agents = [RandomAgent() for _ in range(4)]
    names = ['Jean', 'Anne', 'Luc', 'Sophie']

    game = Game(
        agents=random_agents,
        names=names,
        log_fn=print
    )

    game.start()
