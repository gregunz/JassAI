from jass.agents.impl.human_agent import HumanAgent
from jass.logic.game import Game

if __name__ == '__main__':
    humans = [HumanAgent() for _ in range(4)]
    names = ['Jean', 'Anne', 'Luc', 'Sophie']

    game = Game(
        agents=humans,
        names=names,
        log_fn=print
    )

    game.start()
