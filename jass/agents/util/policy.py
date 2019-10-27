import math
import random
from abc import ABCMeta
from typing import Type, Generic

from jass.agents.action import Action
from jass.agents.state import State


class Policy(metaclass=ABCMeta):
    def __call__(self, state: State) -> Action:
        raise NotImplementedError


class EpsilonGreedyPolicy(Policy):
    def __init__(self, original_policy: Policy, eps_start, eps_end, eps_decay):
        self.eps_start = eps_start
        self.eps_end = eps_end
        self.eps_decay = eps_decay
        self.steps_done = 0
        self.original_policy = original_policy

    def __call__(self, state: State) -> Action:
        eps_threshold = self.eps_end + (self.eps_start - self.eps_end) \
                        * math.exp(-1. * self.steps_done / self.eps_decay)
        self.steps_done += 1
        if random.random() > eps_threshold:
            return self.original_policy(state)
        else:
            random_action = random.choice(state.actions)
            return random_action
