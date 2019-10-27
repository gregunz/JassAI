import torch

from jass.agents.impl.dqn_agent import DQNAgent
from jass.agents.impl.greedy_agent import GreedyAgent
from jass.agents.impl.random_agent import RandomAgent
from jass.logic.game import Game

if __name__ == '__main__':
    # state_dict = torch.load(f'/Users/greg/Data/AI/jass/policy_net_v1/policy_net_v1_ep_53260')
    # print([(k, v.size()) for k, v in state_dict.items()])

    dqn_agent_builder = lambda: DQNAgent()  # DQNAgent(train=False, state_dict=state_dict)
    agents = [dqn_agent_builder(), RandomAgent(), dqn_agent_builder(), RandomAgent()]
    names = ['Jean', 'Anne', 'Luc', 'Sophie']

    game = Game(
        agents=agents,
        names=names,
        log_fn=None,
        goal=200000
    )

    game.start()
