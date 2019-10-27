import torch

from jass.agents.impl.dqn_agent import DQNAgent
from jass.agents.impl.human_agent import HumanAgent
from jass.agents.impl.random_agent import RandomAgent
from jass.logic.game import Game

if __name__ == '__main__':
    state_dict = torch.load(f'/data/jass/policy_net_v1/policy_net_v1_ep_53260')
    print([(k, v.size()) for k, v in state_dict.items()])

    trained_agent = lambda: DQNAgent(train=False, state_dict=state_dict)
    agents = [HumanAgent()] + [trained_agent() for _ in range(3)]
    names = ['Jean', 'Anne', 'Luc', 'Sophie']

    game = Game(
        agents=agents,
        names=names,
        log_fn=print,
        goal=1e9
    )

    game.start()
