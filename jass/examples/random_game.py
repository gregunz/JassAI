from jass.agents.random_agent import RandomAgent
from jass.logic.game import Game

if __name__ == '__main__':
    humans = [RandomAgent() for _ in range(4)]
    names = ['Jean', 'Anne', 'Luc', 'Sophie']

    Game(names, humans).start()