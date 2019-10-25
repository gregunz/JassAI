from jass.agents.human_agent import HumanAgent
from jass.agents.random_agent import RandomAgent
from jass.logic.game import Game

if __name__ == '__main__':
    agents = [HumanAgent()] + [RandomAgent() for _ in range(3)]
    names = ['Jean', 'Anne', 'Luc', 'Sophie']

    Game(names, agents, log_fn=print).play()
