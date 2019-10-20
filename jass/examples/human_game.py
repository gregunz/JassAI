from jass.agents.human_agent import HumanAgent
from jass.logic.game import Game

if __name__ == '__main__':
    humans = [HumanAgent() for _ in range(4)]
    names = ['Jean', 'Anne', 'Luc', 'Sophie']

    Game(names, humans).start()
