from jass.agents.impl.dqn_agent import DQNAgent
from jass.agents.impl.random_agent import RandomAgent
from jass.logic.game import Game

if __name__ == '__main__':
    agents = [DQNAgent(train=True) for _ in range(4)]
    names = ['Jean', 'Anne', 'Luc', 'Sophie']

    game = Game(
        agents=agents,
        names=names,
        log_fn=None,
        goal=1e9
    )

    game.start()
