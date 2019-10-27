import random
from typing import List

from jass.agents.action import Action
from jass.agents.state import State


class SARS:
    def __init__(self, state: State, action: Action, reward: int, next_state: State):
        self.state = state
        self.action = action
        self.next_state = next_state
        self.reward = reward

    @property
    def is_final(self) -> bool:
        return self.next_state is None


class ReplayMemory:
    def __init__(self, capacity):
        self.capacity = capacity
        self.memory = []
        self.position = 0

    def push(self, sars: SARS) -> None:
        """Saves a transition."""
        if len(self.memory) < self.capacity:
            self.memory.append(None)
        self.memory[self.position] = sars
        self.position = (self.position + 1) % self.capacity

    def sample(self, batch_size) -> List[SARS]:
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)
